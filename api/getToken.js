const jwt = require('jsonwebtoken');
const axios = require('axios');

module.exports = async function (req, res) {
    // 官方实锤的钥匙数据
    const clientId = "1204993694888";
    const kid = "c1wTGni_1YToa6HONcPMroUCBuF9oJbRTvI1BYGnjgE";
    const privateKey = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDiwh7TrJLodHIO\nkGualtSi9i76F4TfTaDR75PctmHjHQko2GH9rvdEkHnG/7EunBpgFCQnFsWF39Ia\nJ7tORswqVmeU7/8P5BtOcH96EGW1FmLSj8YsmX/vIU8UD7K8pbZkKFOCOFRYENfl\npQzvx+Tqj3P10SUMfKocQ0M6ZvI1NKEHPd+oYNuVv9htccnRfHVLqGI0wKitq4FU\nH6zGEv+FDyHrEVg1fUbhlSY1b9yLPBo+TRlIYDJYPVkCX2gu8ojtcbMgAnaJ7X4H\nvUrM55lUUoS87MFDsNUZPCYs6SnmpFE+q908fBQZFZ3V7fPynLz1ZICcBqU7cNS/\ndBcaHcdxAgMBAAECggEASkjYq3Rt/gvjr4S9U3vU9fvbQN/CjhrSs+Od12DCKZJC\nBWj5lQ8j/wirdDcgdsn50/7VJx8NH0HHBP1+HXMRAE+lCEQlFTIfhe9Ru42ynAPU\n5PDntYWlxRNu4f4Qij9pRF93mAHXE7CU4azT05tzESpkjSNyVShj2/VnCTNfZnEU\n7MObP3ZiWvv/Y3Jw7CgDW+Ja7/vJ8ApjTVemYdZurg/E4NY/r/hv5TbsevDygNkm\nWRSgSHSt6iR4VOLbZU9ogMcyXoBCj4V0HqN0jDo32mV43875u/QjHWlF98Ck/LeL\nVdhntjGsCM8GMt2MtWkNRCmn/YRfNcKd/rv8uRNeRwKBgQD0kmwPL9UQQJndGqa2\nT7/3sTQGGFJUz3rOeJkuA1RSB8uQNP2j5uYeRJYachipzMA5n/QvN1MDwoBixG+p\nGYzgudr2N+L04YV2U/MzWBrywWYPV/PEz1xa5kqHouCZjwbyOX+Ze19xEITbJ17g\nqZu8MXK3uE+J9yTlJtyKbM/x/wKBgQDtWpxJsDeXBKJQTLhW4CgJumn56ey0M/2c\n1NMgmQ+ljE55a8cWSfl0cQLdf/1H4zg2g/jTx6YBjnQ5+KsaaaLB3Y+/rsF0vzLf\nJ20qoLAm0GMv//81vNWyHAuaV3gGiJRu/+G9Wl78EDzgNO0fyCnEx5sk1qqMRh34\n5HtYFHZmjwKBgQCoHF2ass5JtZ4NlVwyxO63W17fMaimE1fexJbGQhObrzAFl+cg\n2n4jIBHta6/4R316HrDCI800MGX/ffcizSVA83/G7vNaUAplI59wE4eyha2ZrmMp\nTT+2W8WvJg4sf1vO9Cb5YQxhs3EfExjsZKlf2r13+4Dw3KjHusatf84QEQKBgQCJ\nBNreKy0cMB+nbXKpLEPQwd112RW9PZo1lCLBWbrPnbybmZ1Xf6LTFn5J8h38Bu6n\nge3+C+4ITf1IjgXwfHTpp4bZZ//j7pBmhHMfvZ2S+o+X4ReqJPXUGR6VndL7KpNN\ntMfTML1Ok+0gnU0aIMoEABrO3GGeEsgwq22M/lsPfwKBgD+rDuI62m/FCcXQ4dXV\nNeoo+9g1HD6wNcVExwz/zkY67e9qvBQyQjkb4l8103F5QMskOhSrCOjdt5RVo3iw\nIrb4kjTdtd4S+MZGznFKD5QpbHqAbZdtQWvuP34DPvPaoy3oFZjN/Q8aKzzf0RIW\nKlJpbm9suRMtpCxylOpVODhm\n-----END PRIVATE KEY-----";

    // 扣子严格要求的格式
    const payload = {
        iss: clientId,
        aud: "api.coze.cn", // 必须是短写
        jti: Math.random().toString(36).substring(2)
    };

    try {
        const token = jwt.sign(payload, privateKey, {
            algorithm: 'RS256',
            expiresIn: '1h',
            keyid: kid 
        });

        const response = await axios.post('https://api.coze.cn/api/permission/oauth2/token', {
            duration_seconds: 3600,
            grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        }, {
            headers: { 
                'Content-Type': 'application/json',
                // 👇 破案核心！扣子强制要求把 JWT 挂在 Header 的 Authorization 里！
                'Authorization': `Bearer ${token}` 
            }
        });

        if (response.data && response.data.access_token) {
            res.status(200).json({ token: response.data.access_token });
        } else {
            res.status(500).json({ error: '扣子已放行，但未返回正确 token' });
        }
    } catch (error) {
        let realReason = error.message;
        if (error.response && error.response.data) {
            realReason = JSON.stringify(error.response.data);
        }
        res.status(500).json({ error: '真凶找到了：' + realReason });
    }
};
