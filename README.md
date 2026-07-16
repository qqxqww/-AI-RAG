# 企业 AI 助手

基于 RAG（检索增强生成）的企业级智能问答助手，结合本地知识库与大模型，提供精准的企业知识检索与对话服务。

## 功能特性

- **AI 智能对话**：基于企业知识库的上下文感知问答
- **知识库管理**：支持上传、管理企业文档，自动构建向量索引
- **多轮对话**：支持会话历史记录，上下文连续对话
- **流式输出**：大模型回答实时流式展示

## 技术栈

| 组件 | 技术选型 |
|------|----------|
| Web 框架 | Streamlit |
| 大模型 | DeepSeek（LangChain 集成） |
| Embedding | 阿里云 DashScope |
| 向量数据库 | ChromaDB |
| 框架 | LangChain |

## 快速开始

### 环境要求

- Python 3.10+
- Windows / macOS / Linux

### 安装

```bash
# 克隆仓库
git clone https://github.com/qqxqww/-AI-RAG.git
cd -AI-RAG

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 配置 API 密钥

```bash
# Windows
set DASHSCOPE_API_KEY=你的阿里云DashScope密钥
set DEEPSEEK_API_KEY=你的DeepSeek密钥

# macOS/Linux
export DASHSCOPE_API_KEY=你的阿里云DashScope密钥
export DEEPSEEK_API_KEY=你的DeepSeek密钥
```

### 启动

```bash
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`，即可使用。

## 项目结构

```
├── app.py                 # 主入口，页面配置 & 全局样式
├── app_qa.py              # 对话服务
├── app_file_uploader.py   # 文件上传服务
├── rag.py                 # RAG 核心：检索 + 生成
├── knowledge_base.py      # 知识库管理（文档解析、分块、向量化）
├── config_data.py         # 全局配置（模型、向量库、分块参数）
├── file_history_store.py  # 聊天历史持久化
├── vector_stores.py       # 向量库操作封装
├── pages/
│   ├── chat.py            # AI 对话页面
│   └── knowledge.py       # 知识库管理页面
├── data/                  # 知识库原始文档
└── requirements.txt       # 项目依赖
```
