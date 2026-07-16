# 项目主程序（streamlit），启动对话WEB页面
import time
from rag import RagService
import config_data as config
import streamlit as st

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="企业AI助手 - 对话",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== 自定义CSS ====================
st.markdown("""
<style>
    .stApp { background: #f8fafc; font-family: "Inter","PingFang SC","Microsoft YaHei",sans-serif; }
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stHeader"] { background: transparent; }

    /* 侧边栏 */
    [data-testid="stSidebar"] { background: linear-gradient(180deg,#0f172a 0%,#1a2744 100%) !important; }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] h4 { color:#f1f5f9 !important; }
    [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.1) !important; }
    [data-testid="stSidebar"] .stButton > button {
        background:rgba(255,255,255,.08) !important; color:#e2e8f0 !important;
        border:1px solid rgba(255,255,255,.12) !important; border-radius:10px !important;
    }

    .chat-hero { display:flex; align-items:center; justify-content:center; gap:10px;
        padding:.8rem 0 .5rem 0; border-bottom:1px solid #e2e8f0; margin-bottom:.6rem; }
    .chat-hero .ch-icon { font-size:1.8rem; }
    .chat-hero .ch-title { font-size:1.5rem; font-weight:800; color:#0f172a; }
    .chat-hero .ch-badge { background:linear-gradient(135deg,#2563eb,#1d4ed8); color:#fff;
        font-size:.68rem; padding:3px 10px; border-radius:20px; font-weight:700; }

    .chat-wrapper { max-width:820px; margin:0 auto; padding:0 .5rem; }
    section[data-testid="stChatMessage"] { margin-bottom:.7rem !important; }

    [data-testid="stChatInput"] { max-width:820px; margin:0 auto; }
    [data-testid="stChatInput"] textarea { border-radius:14px !important; border:1.5px solid #e2e8f0 !important;
        padding:.7rem 1rem !important; font-size:.93rem !important; background:#fff !important; color:#1e293b !important; }
    [data-testid="stChatInput"] textarea:focus { border-color:#2563eb !important;
        box-shadow:0 0 0 3px rgba(37,99,235,.1) !important; }

    .welcome-screen { text-align:center; padding:2rem 1rem 1rem 1rem; }
    .ws-chip { display:inline-block; background:#fff; border:1px solid #e2e8f0; border-radius:20px;
        padding:7px 16px; font-size:.82rem; color:#475569; margin:4px; }

    .stProgress > div > div > div { background:linear-gradient(90deg,#2563eb,#1d4ed8) !important; }
    .stSpinner > div { color:#2563eb !important; }
</style>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:8px 0;">
        <div style="width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#2563eb,#1d4ed8);
            display:flex;align-items:center;justify-content:center;font-size:18px;">🏢</div>
        <div><div style="font-size:.95rem;font-weight:700;color:#f1f5f9;">企业 AI 助手</div>
        <div style="font-size:.68rem;color:#94a3b8;">Enterprise RAG Assistant</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    msg_count = len(st.session_state.get("message", []))
    st.caption(f"会话 · {msg_count} 条消息")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state["message"] = [{"role":"assistant","content":"对话已清空。"}]; st.rerun()
    with col2:
        if st.button("🔄 新建", use_container_width=True):
            st.session_state["message"] = [{"role":"assistant","content":"你好！我是企业 AI 助手。"}]; st.rerun()
    st.markdown("---")
    st.caption("💡 配合「知识库管理」页面使用效果更佳")

# ==================== 标题 ====================
st.markdown("""
<div class="chat-hero">
    <span class="ch-icon">💬</span><span class="ch-title">AI 对话</span><span class="ch-badge">RAG</span>
</div>""", unsafe_allow_html=True)

# ==================== 初始化 ====================
if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant", "content": "你好！我是企业 AI 助手，基于 RAG 技术为您的企业知识库提供智能问答服务。"}
    ]
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# ==================== 聊天区域 ====================
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
for message in st.session_state["message"]:
    role = "human" if message["role"] == "human" else "assistant"
    with st.chat_message(role):
        st.write(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# 欢迎引导
if len(st.session_state["message"]) == 1:
    st.markdown("""
    <div class="welcome-screen">
        <div style="color:#94a3b8;font-size:.88rem;margin-bottom:.5rem;">试试这些问题：</div>
        <span class="ws-chip">📋 请总结知识库核心内容</span>
        <span class="ws-chip">🔍 知识库中有关于XX的信息？</span>
        <span class="ws-chip">📊 列出所有文档要点</span>
    </div>""", unsafe_allow_html=True)

# ==================== 用户输入 ====================
prompt = st.chat_input(placeholder="输入问题，按 Enter 发送…")
if prompt:
    st.chat_message("human").write(prompt)
    st.session_state["message"].append({"role": "human", "content": prompt})

    ai_res_list = []
    with st.chat_message("assistant"):
        with st.spinner("AI 正在分析知识库..."):
            time.sleep(1)
            res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_id)

            def capture(generator, cache_list):
                for chunk in generator:
                    ai_res_list.append(chunk)
                    yield chunk

            st.write_stream(capture(res_stream, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})
