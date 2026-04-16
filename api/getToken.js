const jwt = require('jsonwebtoken');
const axios = require('axios');

module.exports = async function (req, res) {
    // 👇 终极护盾：强制剥离所有因复制带来的双引号、单引号和隐藏空格！
    let clientId = (process.env.COZE_CLIENT_ID || '').replace(/['"]/g, '').trim();
    let kid = (process.env.COZE_KID || '').replace(/['"]/g, '').trim();
    let privateKey = (process.env.COZE_PRIVATE_KEY || '')
        .replace(/"/g, '')        // 去除首尾可能的双引号
        .replace(/\\n/g, '\n')    // 完美处理换行符
        .trim();

    if (!clientId || !kid || !privateKey) {
        return res.status(500).json({ error: '环境变量未正确读取，请检查 Vercel' });
    }

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
            res.status(500).json({ error: '扣子验证通过但未发卡' });
        }
    } catch (error) {
        let realReason = error.message;
        if (error.response && error.response.data) {
            realReason = JSON.stringify(error.response.data);
        }
        res.status(500).json({ error: '真凶找到了：' + realReason });
    }
};
