# api/getToken.py
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from cozepy import load_oauth_app_from_config

# 配置信息保持不变（使用您上传的 coze_oauth_config.json 里的数据）
COZE_CONFIG = { ... } 

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 第一步：获取前端通过 URL 传过来的学生姓名
            query = parse_qs(urlparse(self.path).query)
            # 获取前端传来的 name 参数，如果没有则默认为 'anonymous'
            user_uid = query.get('name', ['anonymous'])[0]

            oauth_app = load_oauth_app_from_config(COZE_CONFIG)
            
            # 第二步：签署 JWT 时注入 session_name
            # 这是实现会话隔离的关键，扣子会根据此字段区分不同用户的记录
            oauth_token = oauth_app.get_access_token(session_name=user_uid)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"token": oauth_token.access_token}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
