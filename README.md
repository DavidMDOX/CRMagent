# CopperTrade Agent AI - Render / Railway Deployment Edition

这是一个可直接部署的铜贸易智能经营系统基础版，包含登录系统、经营仪表盘、多 Agent 问答控制台、OpenAI 接入与 Render / Railway 配置。

## 本地运行
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

打开 `http://127.0.0.1:8000`

演示账号：`admin/admin123`、`buyer/buyer123`、`sales/sales123`、`boss/boss123`

## 启用真实大模型
```bash
export OPENAI_API_KEY="你的key"
export OPENAI_MODEL="gpt-5.4"
uvicorn app.main:app --reload
```

没有 `OPENAI_API_KEY` 时，系统自动切到 fallback 演示模式。

## 部署到 Render
1. 上传到 GitHub
2. Render 里选择 New + → Blueprint
3. 连接仓库
4. 自动识别 `render.yaml`
5. 填环境变量：`SECRET_KEY`、`OPENAI_API_KEY`（可选）、`OPENAI_MODEL`、`ADMIN_PASSWORD`（可选）

## 部署到 Railway
1. 上传到 GitHub
2. Railway 里选择 Deploy from GitHub Repo
3. 自动识别 `Dockerfile` / `railway.json`
4. 填环境变量：`SECRET_KEY`、`OPENAI_API_KEY`（可选）、`OPENAI_MODEL`、`ADMIN_PASSWORD`（可选）
