from http.server import BaseHTTPRequestHandler
import json
from cozepy import load_oauth_app_from_config

# 这里的配置完全提取自您上传的 coze_oauth_config.json
COZE_CONFIG = {
    "client_type": "jwt",
    "client_id": "1111557339016",
    "coze_www_base": "https://www.coze.cn",
    "coze_api_base": "https://api.coze.cn",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC+/HIN8g4KFqss
/tLC5xuCTF9WqZDuxwIWR4Z2c2NUEvdXtC7sozXUx0FJHAU3pG6+nD6kWeA5ZUjP
6OjbDpWAeoY7di7dkLAyH0m0TSMWuVOrsxYsnNwplZBScePgjEBVYcAFsLo//sCG
8e95dF950FAJu9BAyLg3khnpBhuRm25rj4SCVHz5p1GY9f7p+AvMJwa+QYAbS1CG
YW+A2ariYUIAovGE3ruJRZneIOjFd4TQY9u4ssROppyi/xXA3P6qbsGizYNiwE86
U0puS/LNN0hahQgpvKyWUZ8mecf4CaTUvuJmRzvY/c0aottPL7AaOgPtqZ9lVr/H
fi6/O7fzAgMBAAECggEACS9bODLPHGAZDQ8XnsT+QdwfbQEMVdd0pmf73lV6o5qi
kka5nQAqa23Gb4LX+LmWk+Hax2JafMLTZ3Wu694TMDx0Q9wmsS7aB8cRGd6TKe7G
yIf9MIRouDKXtXIBwL+uAQ00RBx1kJ9VWLK+TsvbIvYdlfeWMo9qAKOCTdPRM/A9
nl3AgXYXdSEm9lojzXKTJ4u+2MMI4j0S5crlm3N2oTsh/TqfyygQ0cM87goHJeUNE
cGGbSDLTzRFv4djgenoRopyRopOoZK1eW6ll88DtFwPjOtOudzwJ+riGg6fMYx1bs
zDHPBc2w8qMlZMNwjbRJ8zoGCE4mQyhD7IoR+ys9+QKBgQDlrVoVjX1ellFmAta2
gDKLhER9o7bq7aCL87eD22KeE3Ava2l7BbYLmFHSfqSygHovecoHQKYvD8vVRnG3
or34+ceiaMFv0ouxrcR1wfdqzJrPc0V4SAHIejqF8gEXmWVgjR6rXR3AvKrMyOlQ
AsYfaKOf+AGSxAZERTTidAWoOQKBgQDU3+lzv/yCrAcocLrHP4KOxjf4rccplh+P
1iiKFv+/PuHZfAnKKKhKmfLmaFrfJ3x4jE78wMwpff/YJUmE8cjwhwVwUJSM9Ixs
VUfAS6iAx+LE+hDQOhNXLaZbnJIiOMn4TMZbwLig+WsAAG89h5v97FqoRKTnOrNy
D/dNW3ppiwKBgHjOGG7zr/ibag8U+Sie/3cAyCGpheHFwUc7ltAlCZcJtF1Myvtp
QpqQsKDd+fTlvN7R2WC9MWvZjCYO2mtzjyaxAr87CFuvy8hWFNq3flLPcbIh+G1O
nuplfKP8hDlACYB9LutD5tleVJOV327g47UrB+CaBBRrUPlOUbz+ZNQyJAoGAOwg0
9xJgdeQ6v+4y/ZoRHIK/dsjKGDA3ZG3hJBoopeJMQ0FwfY00zitO/rIlsQiELfHK
3bChbUgxsMD2WFWsgXcP/Qt7hnMylcA4e4z/l2bW7gTisLvKLTzNi04qAC97Ys33
m+4fxRQlpgR41LlMeugWY99VU4IlzRW8YMljcu0CgYAWbulysvPkAGpKaldHy7l/
esNaZLBHGWRG43mWFumQrYq3Fqh3LbFgJKWU0WheGMsxOIe5zOup8ql+3h/pRc5H
7h00pgiGG1aWChaFHGw2w//8+mONuEnHgq034x069m2a8XfM8gjDCvCdknCXP+qv
1uJnHyigVe0dhO3acFiGjQ==
-----END PRIVATE KEY-----""",
    "public_key_id": "Sx8jlreFOAkRXtJH0jrTbEhJ-tWn4mwuPjJfKZqsyxg"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. 使用官方 SDK 加载配置
            oauth_app = load_oauth_app_from_config(COZE_CONFIG)
            
            # 2. 获取 Access Token
            oauth_token = oauth_app.get_access_token()
            
            # 3. 返回 JSON 响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {"token": oauth_token.access_token}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_message = {"error": f"Failed to get access token: {str(e)}"}
            self.wfile.write(json.dumps(error_message).encode('utf-8'))
