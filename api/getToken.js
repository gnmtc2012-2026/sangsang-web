const jwt = require('jsonwebtoken');
const axios = require('axios');

module.exports = async function (req, res) {
    const sessionName = req.query.name || 'default_user';

    // 核心安全机制：读取 Vercel 的系统保险柜，不在代码里暴露真实密码
    const clientId = process.env.COZE_CLIENT_ID; 
    const kid = process.env.COZE_KID; 
    let privateKey = process.env.COZE_PRIVATE_KEY;
    
    if (privateKey && privateKey.includes('\\n')) {
        privateKey = privateKey.replace(/\\n/g, '\n');
    }

    if (!clientId || !kid || !privateKey) {
        console.error("安全警报：Vercel 环境变量未配置！");
        return res.status(500).json({ error: '系统安全配置缺失' });
    }

    const payload = {
        iss: clientId,
        aud: "api.coze.cn",
        jti: Math.random().toString(36).substring(2),
        session_name: sessionName
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
            res.status(500).json({ error: '换取 Token 失败' });
        }
    } catch (error) {
        console.error("生成 Token 报错", error);
        res.status(500).json({ error: '服务器错误' });
    }
};
