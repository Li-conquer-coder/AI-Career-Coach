# AI Career Coach Agent — 人生规划智能体

基于大语言模型（LLM）构建的个性化 AI 导师后端服务，旨在为大学生提供务实的职业规划与情绪疏导支持。项目具备**长期记忆、多用户数据隔离、流式交互以及自主工具调用**等能力。

## ✨ 核心功能（Features）

- **🧠 长期记忆管理（Memory）**：基于 MySQL 和 SQLAlchemy 实现对话历史的持久化存储。通过倒序提取最近 N 条对话记录（`limit`），在保证 AI 对话连贯性的同时，有效控制大模型 Token 成本。
- **🛡️ 多用户数据隔离（Multi-User Isolation）**：前端生成 UUID 作为用户标识，后端在 CRUD 数据访问层通过 `user_id` 进行数据过滤，确保不同用户的对话历史相互隔离。
- **🛠️ Agent 工具调用（Function Calling）**：集成大模型 Function Calling 能力。模型可根据用户意图自主选择并调用本地 Python 函数，例如 `get_current_time`，实现从自然语言对话到实际任务执行的扩展。
- **⚡ 流式响应（SSE）**：基于 FastAPI 的 `StreamingResponse` 实现 Server-Sent Events（SSE）流式输出，并在流式生成结束后保存完整回复，提供类似 ChatGPT 的实时交互体验。
- **🏗️ 分层架构设计（Layered Architecture）**：采用 `Router` / `CRUD` 分层设计，将 API 路由与数据库操作解耦，提高代码的可维护性与可扩展性。
- **🔒 敏感信息保护（Configuration Security）**：使用 `python-dotenv` 管理 API Key 等敏感配置信息，避免将密钥直接硬编码在源代码中。

## 🛠️ 技术栈（Tech Stack）

| 技术类别 | 使用技术 |
| --- | --- |
| 编程语言 | Python 3.10+ |
| 后端框架 | FastAPI |
| 数据库 | MySQL 8.0 |
| ORM | SQLAlchemy |
| 大模型交互 | AsyncOpenAI SDK、DeepSeek API |
| 流式响应 | Server-Sent Events（SSE）、StreamingResponse |
| 前端交互 | Gradio |
| 环境配置 | python-dotenv |

## 📂 项目结构（Project Structure）

```text
AI-Career-Coach/
├── crud/                  # 数据访问层：封装数据库 CRUD 操作
│   └── chat.py
├── db/                    # 数据库连接与会话配置
│   └── session.py
├── models/                # SQLAlchemy 数据模型
│   └── chat.py
├── routers/               # FastAPI 路由与业务逻辑
│   └── chat.py
├── .env                   # 环境变量配置（不提交至 Git）
├── .gitignore             # Git 忽略规则
├── main.py                # FastAPI 应用入口
├── requirements.txt       # Python 依赖清单
├── ui_app.py              # Gradio 测试前端
└── README.md              # 项目说明文档
```

## 🚀 快速启动（Quick Start）

### 1. 克隆仓库

```bash
git clone https://github.com/Li-conquer-coder/AI-Career-Coach.git
cd AI-Career-Coach
```

### 2. 创建并激活虚拟环境

**Windows（PowerShell）：**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

如果使用 Windows CMD：

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux：**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录下创建 `.env` 文件，并配置 DeepSeek API Key：

```dotenv
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

请将示例值替换为你自己的 API Key。**不要将真实 API Key 提交到 GitHub。**

### 5. 初始化数据库

确保本地 MySQL 服务已经启动，并创建名为 `agent_db` 的数据库。

例如，登录 MySQL 后执行：

```sql
CREATE DATABASE agent_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

启动后端服务时，项目会通过 SQLAlchemy 自动创建所配置的数据表（前提是项目代码中已配置相应的建表逻辑）。

请根据 `db/session.py` 中的实际配置，确认数据库连接地址、用户名、密码及数据库名称正确。

### 6. 启动后端服务

在项目根目录下运行：

```bash
uvicorn main:app --reload
```

启动成功后，可以通过以下地址访问 FastAPI 自动生成的接口文档：

- **Swagger UI：** http://127.0.0.1:8000/docs
- **ReDoc：** http://127.0.0.1:8000/redoc

你可以在接口文档中查看 API 定义并测试接口。

### 7. 启动前端界面（可选）

保持后端服务运行，打开一个新的终端，并进入项目根目录：

```bash
python ui_app.py
```

启动成功后，根据终端输出访问 Gradio Web 界面，默认地址通常为：

http://127.0.0.1:7860

## 🔐 安全说明（Security）

- 不要将 `.env` 文件、真实 API Key 或数据库密码提交至 GitHub。
- 建议在 `.gitignore` 中加入以下规则：

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
```

- 多用户数据隔离依赖后端对用户身份和数据访问权限的正确校验。生产环境中应进一步结合可靠的身份认证机制，避免仅依赖前端生成的 UUID 作为用户身份凭证。

## 📌 项目说明（Project Notes）

本项目是一个面向大学生职业规划与成长复盘场景的 AI Agent 后端实践项目，重点探索大语言模型接入、对话历史管理、流式响应、工具调用及后端分层架构设计。

