const jwt = require('jsonwebtoken');
const axios = require('axios');

module.exports = async function (req, res) {
    const clientId = (process.env.COZE_CLIENT_ID || '').replace(/['"]/g, '').trim();
    const kid = (process.env.COZE_KID || '').replace(/['"]/g, '').trim();
    let rawKey = process.env.COZE_PRIVATE_KEY || '';

    // 👇 终极护盾 2.0：无论 Vercel 把格式揉搓成什么样，强行重组完美钥匙！
    let privateKey = '';
    let keyMatch = rawKey.match(/-----BEGIN PRIVATE KEY-----([\s\S]*?)-----END PRIVATE KEY-----/);
    if (keyMatch) {
        // 1. 把中间的核心乱码提出来，删掉所有空格、换行符和错乱的斜杠
        let cleanBase64 = keyMatch[1].replace(/\s+/g, '').replace(/\\n/g, '');
        // 2. 像搭积木一样，强行用回车符把首尾和内容重新组装成官方标准
        privateKey = `-----BEGIN PRIVATE KEY-----\n${cleanBase64}\n-----END PRIVATE KEY-----`;
    } else {
        // 如果没匹配到，使用基础清洗
        privateKey = rawKey.replace(/"/g, '').replace(/\\n/g, '\n').trim();
    }

    if (!clientId || !kid || !privateKey) {
        return res.status(500).json({ error: '环境变量未正确读取' });
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
