# =============================================================================
# AI 对话 — 企业 AI 助手
# 基于 RAG 的企业级智能问答
# =============================================================================

import time
from rag import RagService
import config_data as config
import streamlit as st

# ── 页面专属 CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* 页头 */
    .chat-hero {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: .8rem 0 .5rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: .6rem;
    }
    .chat-hero .ch-icon {
        font-size: 1.8rem;
    }
    .chat-hero .ch-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -.02em;
    }
    .chat-hero .ch-badge {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #fff;
        font-size: .68rem;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 700;
        letter-spacing: .04em;
    }

    /* 聊天容器居中 */
    .chat-wrapper {
        max-width: 820px;
        margin: 0 auto;
        padding: 0 .5rem;
    }

    /* ── 聊天消息通用 ── */
    section[data-testid="stChatMessage"] {
        margin-bottom: .7rem !important;
        animation: fadeInUp .3s ease;
    }
    /* 强制锁死 chat message 内所有文字为深色 */
    [data-testid="stChatMessage"] * {
        color: #1e293b !important;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── 输入框 ── */
    [data-testid="stChatInput"] {
        max-width: 820px;
        margin: 0 auto;
    }
    [data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
        border: 1.5px solid #e2e8f0 !important;
        padding: .7rem 1rem !important;
        font-size: .93rem !important;
        transition: all .25s !important;
        background: #fff !important;
        color: #1e293b !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,.1) !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* ── 欢迎横幅 ── */
    .welcome-screen {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
    }
    .welcome-screen .ws-icon {
        font-size: 3.5rem;
        margin-bottom: .8rem;
    }
    .welcome-screen .ws-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: .3rem;
    }
    .welcome-screen .ws-sub {
        color: #94a3b8;
        font-size: .88rem;
        max-width: 460px;
        margin: 0 auto;
    }
    .ws-suggestions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin-top: 1.2rem;
    }
    .ws-chip {
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 7px 16px;
        font-size: .82rem;
        color: #475569;
        cursor: default;
        transition: all .15s;
    }
    .ws-chip:hover {
        border-color: #2563eb;
        color: #2563eb;
        background: #eff6ff;
    }

    /* ── 底部状态栏 ── */
    .chat-footer {
        text-align: center;
        padding: .4rem 0;
        color: #94a3b8;
        font-size: .72rem;
    }

    /* ── 分隔线 ── */
    hr { border-color: #e2e8f0 !important; }

    /* ── 消息计数徽章 ── */
    .msg-counter {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        font-size: .72rem;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── 初始化 ──────────────────────────────────────────────────────────────────
if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant", "content": "你好！我是企业 AI 助手，基于 RAG 技术为您的企业知识库提供智能问答服务。请随时向我提问！"}
    ]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# ── 侧边栏（会话管理） ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")

    # 会话信息
    msg_count = len(st.session_state.get("message", []))
    session_label = getattr(config, 'session_id', {}).get('configurable', {}).get('session_id', 'default')
    st.markdown(f"""
    <div style="margin-top:4px;">
        <div style="font-size:.78rem; color:#94a3b8; margin-bottom:6px;">📊 当前会话</div>
        <div style="font-size:.82rem; color:#cbd5e1;">ID: <code style="background:rgba(255,255,255,.06); padding:2px 6px; border-radius:4px;">{session_label}</code></div>
        <div style="font-size:.82rem; color:#cbd5e1; margin-top:4px;">消息数: <span class="msg-counter">{msg_count}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 操作按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ 清空对话", use_container_width=True, key="btn_clear"):
            st.session_state["message"] = [
                {"role": "assistant", "content": "对话已清空。有什么可以帮您？"}
            ]
            st.rerun()
    with col2:
        if st.button("🔄 重新开始", use_container_width=True, key="btn_new"):
            st.session_state["message"] = [
                {"role": "assistant", "content": "你好！我是企业 AI 助手，基于 RAG 技术为您的企业知识库提供智能问答服务。请随时向我提问！"}
            ]
            st.rerun()

    st.markdown("---")

    # 提示
    st.markdown("""
    <div style="font-size:.78rem; color:#94a3b8; line-height:1.5;">
        <b style="color:#cbd5e1;">💡 使用提示</b><br>
        · 先到「知识库管理」上传文档<br>
        · 提问越具体，AI 回答越准确<br>
        · 基于已入库的文档内容作答
    </div>
    """, unsafe_allow_html=True)

# ── 页面标题栏 ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-hero">
    <span class="ch-icon">💬</span>
    <span class="ch-title">AI 对话</span>
    <span class="ch-badge">RAG</span>
</div>
""", unsafe_allow_html=True)

# ── 聊天消息区域 ────────────────────────────────────────────────────────────
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

is_first_message = len(st.session_state["message"]) == 1

for message in st.session_state["message"]:
    role = "human" if message["role"] == "human" else "assistant"
    with st.chat_message(role):
        st.write(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# ── 首次进入时的欢迎引导（无历史消息时） ───────────────────────────────────
if is_first_message:
    st.markdown("""
    <div class="welcome-screen">
        <div class="ws-sub">试试这些问题，快速体验 RAG 智能问答</div>
        <div class="ws-suggestions">
            <span class="ws-chip">📋 请帮我总结知识库中的核心内容</span>
            <span class="ws-chip">🔍 知识库里有关于XX的信息吗？</span>
            <span class="ws-chip">📊 列出知识库中所有文档的要点</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── 用户输入 ────────────────────────────────────────────────────────────────
prompt = st.chat_input(placeholder="输入你的问题，按 Enter 发送…")

if prompt:
    # 用户消息
    with st.chat_message("human"):
        st.write(prompt)
    st.session_state["message"].append({"role": "human", "content": prompt})

    # AI 流式回复
    ai_res_list = []
    with st.chat_message("assistant"):
        with st.spinner("AI 正在分析知识库..."):
            time.sleep(1)
            res_stream = st.session_state["rag"].chain.stream(
                {"input": prompt}, config.session_id
            )

            def capture(generator, cache_list):
                for chunk in generator:
                    ai_res_list.append(chunk)
                    yield chunk

            st.write_stream(capture(res_stream, ai_res_list))

    st.session_state["message"].append({
        "role": "assistant",
        "content": "".join(ai_res_list)
    })

# ── 底部 ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-footer">
    企业 AI 助手 · 基于 RAG 技术 · 回答内容来自已入库知识库
</div>
""", unsafe_allow_html=True)
