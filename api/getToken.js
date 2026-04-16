const jwt = require('jsonwebtoken');
const axios = require('axios');

module.exports = async function (req, res) {
    const sessionName = req.query.name || 'default_user';

    // 核心安全机制：读取 Vercel 的系统保险柜，不在代码里暴露真实密码
    const clientId = process.env.COZE_CLIENT_ID; 
    const kid = process.env.COZE_KID; 
    let privateKey = process.env.COZE_PRIVATE_KEY;
    
    // 自动修复环境变量中私钥可能的换行符丢失问题
    if (privateKey && privateKey.includes('\\n')) {
        privateKey = privateKey.replace(/\\n/g, '\n');
    }

    // 安全校验：如果 Vercel 没配置环境变量，直接拦截并报错
    if (!clientId || !kid || !privateKey) {
        console.error("安全警报：Vercel 环境变量未配置！");
        return res.status(500).json({ error: '系统安全配置缺失，请检查 Vercel 环境变量' });
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

        // 成功发放，扔给前端网页
        if (response.data && response.data.access_token) {
            res.status(200).json({ token: response.data.access_token });
        } else {
            res.status(500).json({ error: '扣子拒绝发卡，请检查 OAuth 权限配置' });
        }
    } catch (error) {
        console.error("生成 Token 报错", error);
        res.status(500).json({ error: '后台服务器通信错误' });
    }
};
