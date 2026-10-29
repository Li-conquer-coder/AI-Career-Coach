# AI Career Coach Agent (人生规划智能体)

基于大语言模型（LLM）构建的个性化 AI 导师后端服务。旨在为大学生提供务实的职业规划与情绪疏导，具备**长期记忆**、**多用户隔离**、**流式交互**以及**自主工具调用**能力。

## ✨ 核心功能 (Features)

- **🧠 长期记忆管理 (Memory)**：基于 `MySQL` + `SQLAlchemy` 实现对话历史的持久化存储。通过倒序提取最近 N 条上下文，在保证 AI 连贯记忆的同时，有效控制大模型 Token 成本。
- **🛡️ 多用户数据隔离 (Multi-User Isolation)**：前端生成 UUID 标识用户，后端在 CRUD 层强制通过 `user_id` 进行行级数据过滤，确保不同用户的上下文记忆绝对隔离，保障隐私安全。
- **🛠️ Agent 工具调用 (Function Calling)**：深度集成大模型 Function Calling 能力。大模型可根据用户意图，自主决策并调用本地 Python 函数（如 `get_current_time`），实现从“纯聊天”到“执行任务”的跨越。
- **⚡ 流式响应 (SSE)**：基于 `StreamingResponse` 实现 Server-Sent Events 流式输出，并在流式结束后异步拼接完整回复落库，提供类似 ChatGPT 的打字机体验。
- **🏗️ 企业级分层架构**：采用 `Router` / `CRUD` 分层设计，实现路由业务逻辑与底层数据库操作解耦，代码高度可维护。
- **🔒 安全隔离**：使用 `dotenv` 进行 API Key 环境变量管理，防止敏感信息泄露。

## 🛠 技术栈 (Tech Stack)

- **核心框架**: Python 3.10+, FastAPI
- **数据库**: MySQL 8.0, SQLAlchemy (ORM)
- **大模型交互**: AsyncOpenAI SDK, DeepSeek API (兼容 OpenAI 格式)
- **前端交互**: Gradio
- **环境管理**: python-dotenv

## 📂 项目结构 (Project Structure)

```text
AI-Career-Coach/
├── crud/                # 数据访问层 (数据库增删改查封装)
│   └── chat.py
├── db/                  # 数据库连接配置
│   └── session.py
├── models/              # SQLAlchemy 数据表模型
│   └── chat.py
├── routers/             # FastAPI 路由层 (业务逻辑)
│   └── chat.py
├── .env                 # 环境变量 (存放 API Key, 不提交至 Git)
├── .gitignore
├── main.py              # FastAPI 启动入口
├── requirements.txt     # 依赖清单
├── ui_app.py            # Gradio 测试前端
└── README.md