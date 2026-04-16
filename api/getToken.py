from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs
from cozepy import load_oauth_app_from_config

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. 获取前端传来的学生唯一标识（姓名）
            query = parse_qs(urlparse(self.path).query)
            student_uid = query.get('name', ['default_student'])[0]

            # 2. 定位并读取同目录下的官方原装配置文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(current_dir)
            config_path = os.path.join(root_dir, 'coze_oauth_config.json')
            
            with open(config_path, 'r', encoding='utf-8') as f:
                coze_config = json.load(f)

            # 3. 调用官方 SDK，关键点：通过 session_name 实现云端会话隔离
            oauth_app = load_oauth_app_from_config(coze_config)
            oauth_token = oauth_app.get_access_token(session_name=student_uid)
            
            # 4. 返回专属 Token
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"token": oauth_token.access_token}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"后台发卡异常: {str(e)}"}).encode('utf-8'))
