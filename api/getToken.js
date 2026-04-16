const jwt = require('jsonwebtoken');
const axios = require('axios');

module.exports = async function (req, res) {
    // 核心安全机制：读取 Vercel 的系统保险柜
    const clientId = process.env.COZE_CLIENT_ID; 
    const kid = process.env.COZE_KID; 
    let privateKey = process.env.COZE_PRIVATE_KEY;
    
    // 自动修复环境变量中私钥可能的换行符丢失问题
    if (privateKey && privateKey.includes('\\n')) {
        privateKey = privateKey.replace(/\\n/g, '\n');
    }

    if (!clientId || !kid || !privateKey) {
        return res.status(500).json({ error: '系统安全配置缺失' });
    }

    // 👇 核心修复：去掉了 session_name，纯净的国际标准格式，绝对不会引发乱码崩溃！
    const payload = {
        iss: clientId,
        aud: "api.coze.cn",
        jti: Math.random().toString(36).substring(2)
    };

    try {
        const token = jwt.sign(payload, privateKey, {
            algorithm: 'RS256',
            expiresIn: '1h',
            keyid: kid,
            header: { typ: 'JWT' }
        });

        const response = await axios.post('https://api.coze.cn/api/permission/oauth2/token', {
            duration_seconds: 3600,
            grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            assertion: token
        }, {
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.data && response.data.access_token) {
            res.status(200).json({ token: response.data.access_token });
        } else {
            res.status(500).json({ error: '扣子拒绝发卡' });
        }
    } catch (error) {
        let realReason = error.message;
        if (error.response && error.response.data) {
            realReason = JSON.stringify(error.response.data);
        }
        res.status(500).json({ error: '真凶找到了：' + realReason });
    }
};
