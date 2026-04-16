from http.server import BaseHTTPRequestHandler
import json
import os
import re
from cozepy import load_oauth_app_from_config

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. 从环境变量读取并强力清洗数据，剔除任何不可见干扰字符
            client_id = os.environ.get("COZE_CLIENT_ID", "").strip().replace('"', '')
            kid = os.environ.get("COZE_KID", "").strip().replace('"', '')
            raw_key = os.environ.get("COZE_PRIVATE_KEY", "").strip()

            # 2. 核心修复：还原被压缩或损坏的私钥格式
            # 提取中间的 Base64 内容
            key_body = re.search(r'-----BEGIN PRIVATE KEY-----([\s\S]*?)-----END PRIVATE KEY-----', raw_key)
            if key_body:
                # 去掉所有空格、反斜杠n、以及可能存在的转义符
                clean_content = key_body.group(1).replace('\n', '').replace('\\n', '').replace(' ', '').strip()
                # 重新按标准格式缝合
                private_key = f"-----BEGIN PRIVATE KEY-----\n{clean_content}\n-----END PRIVATE KEY-----"
            else:
                private_key = raw_key.replace('\\n', '\n')

            # 3. 构造官方配置对象
            coze_config = {
                "client_type": "jwt",
                "client_id": client_id,
                "coze_www_base": "https://www.coze.cn",
                "coze_api_base": "https://api.coze.cn",
                "private_key": private_key,
                "public_key_id": kid
            }

            # 4. 调用官方 SDK
            oauth_app = load_oauth_app_from_config(coze_config)
            oauth_token = oauth_app.get_access_token()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"token": oauth_token.access_token}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"SDK接入错误: {str(e)}"}).encode('utf-8'))
