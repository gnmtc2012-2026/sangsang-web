export default function handler(req, res) {
    // 这里的 COZE_TOKEN 就是我们要去 Vercel 后台填写的环境变量
    res.status(200).json({ token: process.env.COZE_TOKEN });
}