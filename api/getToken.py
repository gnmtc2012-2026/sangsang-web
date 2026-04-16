from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs
from cozepy import load_oauth_app_from_config

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. 获取前端传来的名字（用于隔离档案）
            query = parse_qs(urlparse(self.path).query)
            student_name = query.get('name', ['default'])[0]

            # 2. 自动定位并读取原装的 JSON 文件，100% 避免格式错误
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(current_dir)
            config_path = os.path.join(root_dir, 'coze_oauth_config.json')
            
            with open(config_path, 'r', encoding='utf-8') as f:
                coze_config = json.load(f)

            # 3. 启动扣子 SDK，传入名字锁定独立聊天档案
            oauth_app = load_oauth_app_from_config(coze_config)
            oauth_token = oauth_app.get_access_token(session_name=student_name)
            
            # 4. 成功发卡
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"token": oauth_token.access_token}).encode('utf-8'))
            
        except Exception as e:
            # 报错反馈
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
