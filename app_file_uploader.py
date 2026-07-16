#知识库更新主程序
"""
基于Streamlit完成WEB网页上传服务
pip install streamlit
"""
import time
import streamlit as st
from knowledge_base import KnowledgeBaseService

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="企业AI助手 - 知识库",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ==================== 自定义CSS ====================
st.markdown("""
<style>
    .stApp { background: #f8fafc; font-family: "Inter","PingFang SC","Microsoft YaHei",sans-serif; }
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stHeader"] { background: transparent; }

    [data-testid="stSidebar"] { background: linear-gradient(180deg,#0f172a 0%,#1a2744 100%) !important; }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h3 { color:#f1f5f9 !important; }

    .page-hero { text-align:center; padding:1.2rem 0 .6rem 0; }
    .page-hero h1 { font-size:1.8rem; font-weight:800; color:#0f172a; margin-bottom:.2rem; }
    .page-hero p { color:#64748b; font-size:.9rem; }

    .enterprise-card { background:#fff; border-radius:14px; padding:1.8rem 2rem;
        box-shadow:0 4px 16px rgba(0,0,0,.06); border:1px solid #e2e8f0; margin-bottom:1.2rem; }

    div[data-testid="stFileUploader"] section {
        border:2px dashed #cbd5e1 !important; border-radius:14px !important;
        background:#f8fafc !important; padding:2rem 1.5rem !important; }
    div[data-testid="stFileUploader"] section:hover { border-color:#2563eb !important; background:#eff6ff !important; }

    .file-preview { display:flex; align-items:center; gap:16px;
        background:linear-gradient(135deg,#2563eb 0%,#1d4ed8 100%);
        border-radius:12px; padding:18px 22px; color:#fff; margin:1rem 0;
        box-shadow:0 4px 20px rgba(37,99,235,.25); }
    .file-preview .fp-icon { font-size:2.2rem; }
    .file-preview .fp-name { font-size:1rem; font-weight:700; }
    .file-preview .fp-meta { font-size:.78rem; opacity:.85; margin-top:2px; }
    .file-preview .fp-badge { margin-left:auto; background:rgba(255,255,255,.2);
        padding:4px 12px; border-radius:20px; font-size:.75rem; font-weight:600; }

    .result-box { border-radius:10px; padding:14px 18px; font-weight:500; font-size:.9rem; margin:.8rem 0; }
    .result-success { background:#ecfdf5; border-left:4px solid #10b981; color:#065f46; }
    .result-error { background:#fef2f2; border-left:4px solid #ef4444; color:#991b1b; }
    .result-info { background:#eff6ff; border-left:4px solid #2563eb; color:#1e40af; }

    .empty-state { text-align:center; padding:3rem 1rem; color:#94a3b8; }

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
    st.markdown("""
    **📋 使用说明**
    1. 上传 `.txt` 格式文档
    2. 系统自动解析并向量化入库
    3. 前往「AI 对话」页面提问
    """)
    st.markdown("---")
    st.caption("💡 配合「AI 对话」页面使用效果更佳")

# ==================== 页面标题 ====================
st.markdown("""
<div class="page-hero">
    <h1>📚 知识库管理</h1>
    <p>上传企业文档，构建专属智能知识库</p>
</div>
""", unsafe_allow_html=True)

# ==================== 初始化 ====================
if "system" not in st.session_state:
    st.session_state["system"] = KnowledgeBaseService()

# ==================== 上传区域 ====================
st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 4, 1])
with c2:
    uploader_file = st.file_uploader(
        label="拖拽文档到此处，或点击选择文件",
        type=['txt'],
        accept_multiple_files=False,
        help="仅支持 .txt 格式，UTF-8 编码",
        key="kb_uploader",
    )
st.markdown('</div>', unsafe_allow_html=True)

# ==================== 处理上传 ====================
if uploader_file is not None:
    file_name = uploader_file.name
    file_size = uploader_file.size / 1024
    size_label = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"

    st.markdown(f"""
    <div class="file-preview">
        <div class="fp-icon">📄</div>
        <div><div class="fp-name">{file_name}</div>
        <div class="fp-meta">📦 {size_label} · UTF-8</div></div>
        <div class="fp-badge">待入库</div>
    </div>
    """, unsafe_allow_html=True)

    progress = st.progress(0, text="⏳ 准备解析文档...")
    text = uploader_file.getvalue().decode("utf-8")

    steps = [(20, "🔍 解析文档结构..."), (55, "🧠 生成向量嵌入..."), (80, "💾 写入向量数据库...")]
    for pct, msg in steps:
        time.sleep(0.35)
        progress.progress(pct, text=msg)

    result = st.session_state["system"].upload_by_str(text, file_name)

    for pct in range(85, 101, 3):
        time.sleep(0.05)
        progress.progress(min(pct, 100), text="✅ 入库完成")
    progress.empty()

    is_success = "成功" in str(result) or "ok" in str(result).lower()
    cls = "result-success" if is_success else "result-error"
    st.markdown(f'<div class="result-box {cls}">{result}</div>', unsafe_allow_html=True)
    if is_success:
        st.success("🎉 文档已成功入库，可前往「AI 对话」页面提问！")
else:
    st.markdown("""
    <div class="empty-state">
        <div style="font-size:3rem;opacity:.5;margin-bottom:.8rem;">📂</div>
        <p style="font-weight:500;">暂无上传记录</p>
        <p style="font-size:.82rem;">拖拽 .txt 文件到上方区域</p>
    </div>
    """, unsafe_allow_html=True)
