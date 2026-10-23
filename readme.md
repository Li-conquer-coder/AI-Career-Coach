**# AI Career Coach Agent (人生规划 AI 智能体)

这是一个基于大语言模型（LLM）的个性化 AI 导师后端服务。旨在为大学生提供务实的职业规划与情绪疏导。

## 🛠 技术栈
- **后端框架**: Python, FastAPI
- **数据库**: MySQL, SQLAlchemy (ORM)
- **大模型与 AI**: DeepSeek API (AsyncOpenAI SDK), Prompt Engineering
- **流式交互**: Server-Sent Events (SSE), StreamingResponse
- **前端界面**: Gradio

## ✨ 核心功能
1. **持久化长期记忆 (Memory)**：基于 MySQL 数据库实现多轮对话历史存储，通过倒序提取最近上下文，在保证 AI 记忆连贯性的同时，有效控制大模型 Token 成本。
2. **丝滑流式响应 (SSE)**：基于 `StreamingResponse` 实现打字机效果，提升用户体验。
3. **分层架构设计**：采用 Router / CRUD 分层架构，实现路由业务逻辑与底层数据库操作的完全解耦。
4. **安全隔离**：使用 `dotenv` 进行 API Key 环境变量管理，避免敏感信息泄露。

## 🚀 快速启动
1. 安装依赖：`pip install -r requirements.txt`
2. 配置环境变量：在根目录创建 `.env` 文件并添加 `DEEPSEEK_API_KEY=你的密钥`
3. 启动后端服务：`uvicorn main:app --reload`
4. 启动前端界面：`python ui_app.py`**