from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from cozepy import load_oauth_app_from_config

# 这里完全复制了您下载的 coze_oauth_config.json 官方配置，一行未改！
coze_config = {
    "client_type": "jwt",
    "client_id": "1204993694888",
    "coze_www_base": "https://www.coze.cn",
    "coze_api_base": "https://api.coze.cn",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDiwh7TrJLodHIO\nkGualtSi9i76F4TfTaDR75PctmHjHQko2GH9rvdEkHnG/7EunBpgFCQnFsWF39Ia\nJ7tORswqVmeU7/8P5BtOcH96EGW1FmLSj8YsmX/vIU8UD7K8pbZkKFOCOFRYENfl\npQzvx+Tqj3P10SUMfKocQ0M6ZvI1NKEHPd+oYNuVv9htccnRfHVLqGI0wKitq4FU\nH6zGEv+FDyHrEVg1fUbhlSY1b9yLPBo+TRlIYDJYPVkCX2gu8ojtcbMgAnaJ7X4H\nvUrM55lUUoS87MFDsNUZPCYs6SnmpFE+q908fBQZFZ3V7fPynLz1ZICcBqU7cNS/\ndBcaHcdxAgMBAAECggEASkjYq3Rt/gvjr4S9U3vU9fvbQN/CjhrSs+Od12DCKZJC\nBWj5lQ8j/wirdDcgdsn50/7VJx8NH0HHBP1+HXMRAE+lCEQlFTIfhe9Ru42ynAPU\n5PDntYWlxRNu4f4Qij9pRF93mAHXE7CU4azT05tzESpkjSNyVShj2/VnCTNfZnEU\n7MObP3ZiWvv/Y3Jw7CgDW+Ja7/vJ8ApjTVemYdZurg/E4NY/r/hv5TbsevDygNkm\nWRSgSHSt6iR4VOLbZU9ogMcyXoBCj4V0HqN0jDo32mV43875u/QjHWlF98Ck/LeL\nVdhntjGsCM8GMt2MtWkNRCmn/YRfNcKd/rv8uRNeRwKBgQD0kmwPL9UQQJndGqa2\nT7/3sTQGGFJUz3rOeJkuA1RSB8uQNP2j5uYeRJYachipzMA5n/QvN1MDwoBixG+p\nGYzgudr2N+L04YV2U/MzWBrywWYPV/PEz1xa5kqHouCZjwbyOX+Ze19xEITbJ17g\nqZu8MXK3uE+J9yTlJtyKbM/x/wKBgQDtWpxJsDeXBKJQTLhW4CgJumn56ey0M/2c\n1NMgmQ+ljE55a8cWSfl0cQLdf/1H4zg2g/jTx6YBjnQ5+KsaaaLB3Y+/rsF0vzLf\nJ20qoLAm0GMv//81vNWyHAuaV3gGiJRu/+G9Wl78EDzgNO0fyCnEx5sk1qqMRh34\n5HtYFHZmjwKBgQCoHF2ass5JtZ4NlVwyxO63W17fMaimE1fexJbGQhObrzAFl+cg\n2n4jIBHta6/4R316HrDCI800MGX/ffcizSVA83/G7vNaUAplI59wE4eyha2ZrmMp\nTT+2W8WvJg4sf1vO9Cb5YQxhs3EfExjsZKlf2r13+4Dw3KjHusatf84QEQKBgQCJ\nBNreKy0cMB+nbXKpLEPQwd112RW9PZo1lCLBWbrPnbybmZ1Xf6LTFn5J8h38Bu6n\nge3+C+4ITf1IjgXwfHTpp4bZZ//j7pBmhHMfvZ2S+o+X4ReqJPXUGR6VndL7KpNN\ntMfTML1Ok+0gnU0aIMoEABrO3GGeEsgwq22M/lsPfwKBgD+rDuI62m/FCcXQ4dXV\nNeoo+9g1HD6wNcVExwz/zkY67e9qvBQyQjkb4l8103F5QMskOhSrCOjdt5RVo3iw\nIrb4kjTdtd4S+MZGznFKD5QpbHqAbZdtQWvuP34DPvPaoy3oFZjN/Q8aKzzf0RIW\nKlJpbm9suRMtpCxylOpVODhm\n-----END PRIVATE KEY-----",
    "public_key_id": "c1wTGni_1YToa6HONcPMroUCBuF9oJbRTvI1BYGnjgE"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. 拦截前端网页发来的请求
            parsed_path = urlparse(self.path)
            
            # 2. 调用国内扣子官方 SDK (cozepy)，绝不手写加密！
            oauth_app = load_oauth_app_from_config(coze_config)
            oauth_token = oauth_app.get_access_token()
            
            # 3. 拿到官方发下来的 token，打包发给前端
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {"token": oauth_token.access_token}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            # 万一官方 SDK 报错，把中文错误直接弹回给前端
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_data = {"error": f"官方SDK配置异常: {str(e)}"}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
