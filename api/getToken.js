const jwt = require('jsonwebtoken');
const axios = require('axios');

module.exports = async function (req, res) {
    // 国内版扣子官方认证的真实身份信息
    const clientId = "1204993694888";
    const kid = "c1wTGni_1YToa6HONcPMroUCBuF9oJbRTvI1BYGnjgE";
    
    // 👇 终极武器：物理换行！不使用任何 \n 符号，原封不动保留真实格式，彻底杜绝转义损坏！
    const privateKey = `-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDiwh7TrJLodHIO
kGualtSi9i76F4TfTaDR75PctmHjHQko2GH9rvdEkHnG/7EunBpgFCQnFsWF39Ia
J7tORswqVmeU7/8P5BtOcH96EGW1FmLSj8YsmX/vIU8UD7K8pbZkKFOCOFRYENfl
pQzvx+Tqj3P10SUMfKocQ0M6ZvI1NKEHPd+oYNuVv9htccnRfHVLqGI0wKitq4FU
H6zGEv+FDyHrEVg1fUbhlSY1b9yLPBo+TRlIYDJYPVkCX2gu8ojtcbMgAnaJ7X4H
vUrM55lUUoS87MFDsNUZPCYs6SnmpFE+q908fBQZFZ3V7fPynLz1ZICcBqU7cNS/
dBcaHcdxAgMBAAECggEASkjYq3Rt/gvjr4S9U3vU9fvbQN/CjhrSs+Od12DCKZJC
BWj5lQ8j/wirdDcgdsn50/7VJx8NH0HHBP1+HXMRAE+lCEQlFTIfhe9Ru42ynAPU
5PDntYWlxRNu4f4Qij9pRF93mAHXE7CU4azT05tzESpkjSNyVShj2/VnCTNfZnEU
7MObP3ZiWvv/Y3Jw7CgDW+Ja7/vJ8ApjTVemYdZurg/E4NY/r/hv5TbsevDygNkm
WRSgSHSt6iR4VOLbZU9ogMcyXoBCj4V0HqN0jDo32mV43875u/QjHWlF98Ck/LeL
VdhntjGsCM8GMt2MtWkNRCmn/YRfNcKd/rv8uRNeRwKBgQD0kmwPL9UQQJndGqa2
T7/3sTQGGFJUz3rOeJkuA1RSB8uQNP2j5uYeRJYachipzMA5n/QvN1MDwoBixG+p
GYzgudr2N+L04YV2U/MzWBrywWYPV/PEz1xa5kqHouCZjwbyOX+Ze19xEITbJ17g
qZu8MXK3uE+J9yTlJtyKbM/x/wKBgQDtWpxJsDeXBKJQTLhW4CgJumn56ey0M/2c
1NMgmQ+ljE55a8cWSfl0cQLdf/1H4zg2g/jTx6YBjnQ5+KsaaaLB3Y+/rsF0vzLf
J20qoLAm0GMv//81vNWyHAuaV3gGiJRu/+G9Wl78EDzgNO0fyCnEx5sk1qqMRh34
5HtYFHZmjwKBgQCoHF2ass5JtZ4NlVwyxO63W17fMaimE1fexJbGQhObrzAFl+cg
2n4jIBHta6/4R316HrDCI800MGX/ffcizSVA83/G7vNaUAplI59wE4eyha2ZrmMp
TT+2W8WvJg4sf1vO9Cb5YQxhs3EfExjsZKlf2r13+4Dw3KjHusatf84QEQKBgQCJ
BNreKy0cMB+nbXKpLEPQwd112RW9PZo1lCLBWbrPnbybmZ1Xf6LTFn5J8h38Bu6n
ge3+C+4ITf1IjgXwfHTpp4bZZ//j7pBmhHMfvZ2S+o+X4ReqJPXUGR6VndL7KpNN
tMfTML1Ok+0gnU0aIMoEABrO3GGeEsgwq22M/lsPfwKBgD+rDuI62m/FCcXQ4dXV
Neoo+9g1HD6wNcVExwz/zkY67e9qvBQyQjkb4l8103F5QMskOhSrCOjdt5RVo3iw
Irb4kjTdtd4S+MZGznFKD5QpbHqAbZdtQWvuP34DPvPaoy3oFZjN/Q8aKzzf0RIW
KlJpbm9suRMtpCxylOpVODhm
-----END PRIVATE KEY-----`;

    // 严格补全：加入国内版官方要求的生成时间(iat)和过期时间(exp)
    const now = Math.floor(Date.now() / 1000);
    const payload = {
        iss: clientId,
        aud: "api.coze.cn",
        iat: now,
        exp: now + 3600,
        jti: Math.random().toString(36).substring(2)
    };

    try {
        // 使用最标准的签发方式，自动注入 Header，绝不覆盖算法标识
        const token = jwt.sign(payload, privateKey, {
            algorithm: 'RS256',
            keyid: kid
        });

        // 将制作完美的房卡原封不动投递给国内版扣子
        const response = await axios.post('https://api.coze.cn/api/permission/oauth2/token', {
            duration_seconds: 3600,
            grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            assertion: token
        }, {
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        if (response.data && response.data.access_token) {
            res.status(200).json({ token: response.data.access_token });
        } else {
            res.status(500).json({ error: '扣子返回异常：' + JSON.stringify(response.data) });
        }
    } catch (error) {
        let realReason = error.message;
        if (error.response && error.response.data) {
            realReason = JSON.stringify(error.response.data);
        }
        res.status(500).json({ error: '排错监控：' + realReason });
    }
};
