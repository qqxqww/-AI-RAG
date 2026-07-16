# =============================================================================
# 企业 AI 助手 — 统一入口
# 基于 Streamlit 多页面导航，整合「AI 对话」与「知识库管理」
# 启动方式: streamlit run app.py
# =============================================================================

import streamlit as st

# ── 页面全局配置（仅入口文件设置） ──────────────────────────────────────────
st.set_page_config(
    page_title="企业 AI 助手",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 全局 CSS（所有子页面共享） ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ===== 根变量 & 全局 ===== */
    :root {
        --navy-900: #0f172a;
        --navy-800: #1e293b;
        --navy-700: #334155;
        --gold:      #ca8a04;
        --gold-lt:   #fef3c7;
        --blue:      #2563eb;
        --blue-lt:   #dbeafe;
        --slate-50:  #f8fafc;
        --slate-100: #f1f5f9;
        --slate-200: #e2e8f0;
        --slate-500: #64748b;
        --slate-700: #334155;
        --radius:    14px;
        --shadow-sm: 0 1px 2px rgba(0,0,0,.05);
        --shadow-md: 0 4px 16px rgba(0,0,0,.06);
    }

    .stApp {
        background: var(--slate-50);
        font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
    }

    /* ===== 隐藏 Streamlit 默认冗余元素（保留顶部工具栏以支持侧边栏折叠） ===== */
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stHeader"] { background: transparent; }

    /* ===== 侧边栏全局 ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--navy-900) 0%, #1a2744 100%) !important;
        color: #cbd5e1 !important;
    }
    /* 只影响侧边栏内的直接 Streamlit 文本组件，避免泄漏到主内容区 */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .st-caption {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        color: #f1f5f9 !important;
    }
    /* 主内容区文字锁定为深色，防御侧边栏样式泄漏 */
    [data-testid="stAppViewContainer"] {
        color: #1e293b;
    }
    [data-testid="stAppViewContainer"] [data-testid="stChatMessage"] * {
        color: #1e293b;
    }
    [data-testid="stAppViewContainer"] [data-testid="stChatMessage"][aria-label*="human"] * {
        color: #1e293b;
    }

    /* 侧边栏导航项高亮 */
    [data-testid="stSidebarNav"] a {
        border-radius: 10px !important;
        margin: 2px 6px !important;
        padding: 8px 14px !important;
        transition: all .2s !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255,255,255,.08) !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(37,99,235,.25) !important;
        color: #fff !important;
    }

    /* 侧边栏分割线 */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.1) !important;
        margin: 1rem 0 !important;
    }

    /* ===== 全局按钮 ===== */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: .88rem !important;
        transition: all .2s !important;
        border: none !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(37,99,235,.3) !important;
    }

    /* ===== 全局卡片容器 ===== */
    .enterprise-card {
        background: #fff;
        border-radius: var(--radius);
        padding: 1.8rem 2rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--slate-200);
        margin-bottom: 1.2rem;
    }

    /* ===== 全局进度条 ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
        border-radius: 8px !important;
    }

    /* ===== Spinner ===== */
    .stSpinner > div { color: var(--blue) !important; }
</style>
""", unsafe_allow_html=True)

# ── 侧边栏品牌区 ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; padding:8px 0 4px 0;">
        <div style="width:40px; height:40px; border-radius:10px;
                    background:linear-gradient(135deg, #2563eb, #1d4ed8);
                    display:flex; align-items:center; justify-content:center; font-size:20px;">
            🏢
        </div>
        <div>
            <div style="font-size:1rem; font-weight:700; color:#f1f5f9; line-height:1.2;">企业 AI 助手</div>
            <div style="font-size:.72rem; color:#94a3b8;">Enterprise RAG Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("基于 RAG 的企业级智能知识检索系统")

# ── 多页面导航 ────────────────────────────────────────────────────────────
pg = st.navigation({
    "": [
        st.Page("pages/chat.py",      title="AI 对话",      icon="💬", default=True),
        st.Page("pages/knowledge.py", title="知识库管理",    icon="📚"),
    ]
})
pg.run()
