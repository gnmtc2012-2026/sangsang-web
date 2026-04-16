from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from cozepy import load_oauth_app_from_config

# 官方配置全量硬编码：彻底杜绝环境变量带来的任何格式和 PEM 报错
COZE_CONFIG = {
    "client_type": "jwt",
    "client_id": "1111557339016",
    "coze_www_base": "https://www.coze.cn",
    "coze_api_base": "https://api.coze.cn",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC+/HIN8g4KFqss\n/tLC5xuCTF9WqZDuxwIWR4Z2c2NUEvdXtC7sozXUx0FJHAU3pG6+nD6kWeA5ZUjP\n6OjbDpWAeoY7di7dkLAyH0m0TSMWuVOrsxYsnNwplZBScePgjEBVYcAFsLo//sCG\n8e95dF950FAJu9BAyLg3khnpBhuRm25rj4SCVHz5p1GY9f7p+AvMJwa+QYAbS1CG\nYW+A2ariYUIAovGE3ruJRZneIOjFd4TQY9u4ssROppyi/xXA3P6qbsGizYNiwE86\nU0puS/LNN0hahQgpvKyWUZ8mecf4CaTUvuJmRzvY/c0aottPL7AaOgPtqZ9lVr/H\nfi6/O7fzAgMBAAECggEACS9bODLPHGAZDQ8XnsT+QdwfbQEMVdd0pmf73lV6o5qi\nkka5nQAqa23Gb4LX+LmWk+Hax2JafMLTZ3Wu694TMDx0Q9wmsS7aB8cRGd6TKe7G\nyIf9MIRouDKXtXIBwL+uAQ00RBx1kJ9VWLK+TsvbIvYdlfeWMo9qAKOCTdPRM/A9\nl3AgXYXdSEm9lojzXKTJ4u+2MMI4j0S5crlm3N2oTsh/TqfyygQ0cM87goHJeUNE\ncGbSDLTzRFv4djgenoRopyRopOoZK1eW6ll88DtFwPjOtOudzwJ+riGg6fMYx1bs\nzDHPBc2w8qMlZMNwjbRJ8zoGCE4mQyhD7IoR+ys9+QKBgQDlrVoVjX1ellFmAta2\ngDKLhER9o7bq7aCL87eD22KeE3Ava2l7BbYLmFHSfqSygHovecoHQKYvD8vVRnG3\nor34+ceiaMFv0ouxrcR1wfdqzJrPc0V4SAHIejqF8gEXmWVgjR6rXR3AvKrMyOlQ\nAsYfaKOf+AGSxAZERTTidAWoOQKBgQDU3+lzv/yCrAcocLrHP4KOxjf4rccplh+P\n1iiKFv+/PuHZfAnKKKhKmfLmaFrfJ3x4jE78wMwpff/YJUmE8cjwhwVwUJSM9Ixs\nVUfAS6iAx+LE+hDQOhNXLaZbnJIiOMn4TMZbwLig+WsAAG89h5v97FqoRKTnOrNy\nD/dNW3ppiwKBgHjOGG7zr/ibag8U+Sie/3cAyCGpheHFwUc7ltAlCZcJtF1Myvtp\nQpqQsKDd+fTlvN7R2WC9MWvZjCYO2mtzjyaxAr87CFuvy8hWFNq3flLPcbIh+G1O\nuplfKP8hDlACYB9LutD5tleVJOV327g47UrB+CaBBRrUPlOUbz+ZNQyJAoGAOwg0\n9xJgdeQ6v+4y/ZoRHIK/dsjKGDA3ZG3hJBoopeJMQ0FwfY00zitO/rIlsQiELfHK\n3bChbUgxsMD2WFWsgXcP/Qt7hnMylcA4e4z/l2bW7gTisLvKLTzNi04qAC97Ys33\nm+4fxRQlpgR41LlMeugWY99VU4IlzRW8YMljcu0CgYAWbulysvPkAGpKaldHy7l/\nesNaZLBHGWRG43mWFumQrYq3Fqh3LbFgJKWU0WheGMsxOIe5zOup8ql+3h/pRc5H\n7h00pgiGG1aWChaFHGw2w//8+mONuEnHgq034x069m2a8XfM8gjDCvCdknCXP+qv\n1uJnHyigVe0dhO3acFiGjQ==\n-----END PRIVATE KEY-----",
    "public_key_id": "Sx8jlreFOAkRXtJH0jrTbEhJ-tWn4mwuPjJfKZqsyxg"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 获取名字
            query = parse_qs(urlparse(self.path).query)
            student_name = query.get('name', ['default'])[0]

            # 启动扣子 SDK，传入名字锁定独立聊天档案
            oauth_app = load_oauth_app_from_config(COZE_CONFIG)
            oauth_token = oauth_app.get_access_token(session_name=student_name)
            
            # 成功发卡
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"token": oauth_token.access_token}).encode('utf-8'))
        except Exception as e:
            # 报错
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
