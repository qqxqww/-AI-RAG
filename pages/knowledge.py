# =============================================================================
# 知识库管理 - 企业 AI 助手
# 文档上传、预览、入库管理
# =============================================================================

import time
import streamlit as st
from knowledge_base import KnowledgeBaseService

# ── 页面专属 CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* 页头 */
    .page-hero {
        text-align: center;
        padding: 1.2rem 0 .6rem 0;
    }
    .page-hero h1 {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: .2rem;
        letter-spacing: -.02em;
    }
    .page-hero p {
        color: #64748b;
        font-size: .9rem;
    }

    /* 上传拖拽区 */
    div[data-testid="stFileUploader"] section {
        border: 2px dashed #cbd5e1 !important;
        border-radius: 14px !important;
        background: #f8fafc !important;
        padding: 2rem 1.5rem !important;
        transition: all .25s !important;
    }
    div[data-testid="stFileUploader"] section:hover {
        border-color: #2563eb !important;
        background: #eff6ff !important;
    }
    div[data-testid="stFileUploader"] section small {
        color: #94a3b8 !important;
    }

    /* 文件预览卡片 */
    .file-preview {
        display: flex;
        align-items: center;
        gap: 16px;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border-radius: 12px;
        padding: 18px 22px;
        color: #fff;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(37,99,235,.25);
    }
    .file-preview .fp-icon {
        font-size: 2.2rem;
    }
    .file-preview .fp-name {
        font-size: 1rem;
        font-weight: 700;
    }
    .file-preview .fp-meta {
        font-size: .78rem;
        opacity: .85;
        margin-top: 2px;
    }
    .file-preview .fp-badge {
        margin-left: auto;
        background: rgba(255,255,255,.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: .75rem;
        font-weight: 600;
    }

    /* 结果提示 */
    .result-box {
        border-radius: 10px;
        padding: 14px 18px;
        font-weight: 500;
        font-size: .9rem;
        margin: .8rem 0;
    }
    .result-success {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        color: #065f46;
    }
    .result-error {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        color: #991b1b;
    }
    .result-info {
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        color: #1e40af;
    }

    /* 统计小卡片 */
    .stat-card {
        text-align: center;
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 10px;
    }
    .stat-card .stat-num {
        font-size: 1.5rem;
        font-weight: 800;
        color: #2563eb;
    }
    .stat-card .stat-label {
        font-size: .75rem;
        color: #64748b;
        margin-top: 4px;
    }

    /* 空态 */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #94a3b8;
    }
    .empty-state .empty-icon {
        font-size: 3.5rem;
        margin-bottom: .8rem;
        opacity: .6;
    }

    /* 上传状态提示条 */
    .kb-status-bar {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 24px;
        padding: 0 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── 初始化知识库服务 ────────────────────────────────────────────────────────
if "system" not in st.session_state:
    st.session_state["system"] = KnowledgeBaseService()

# ── 页头 ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-hero">
    <h1>📚 知识库管理</h1>
    <p>上传企业文档，构建专属智能知识库，赋能 AI 精准问答</p>
</div>
""", unsafe_allow_html=True)

# ── 上传卡片 ────────────────────────────────────────────────────────────────
st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)

col_upload_left, col_upload_center, col_upload_right = st.columns([1, 4, 1])
with col_upload_center:
    uploader_file = st.file_uploader(
        label="拖拽文档到此处，或点击选择文件",
        type=['txt'],
        accept_multiple_files=False,
        help="支持 UTF-8 编码的 .txt 文本文件",
        key="kb_uploader",
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── 处理上传 ────────────────────────────────────────────────────────────────
if uploader_file is not None:
    file_name = uploader_file.name
    file_size = uploader_file.size / 1024

    # 文件预览卡片
    size_label = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"
    st.markdown(f"""
    <div class="file-preview">
        <div class="fp-icon">📄</div>
        <div>
            <div class="fp-name">{file_name}</div>
            <div class="fp-meta">📦 {size_label} &nbsp;·&nbsp; UTF-8 编码</div>
        </div>
        <div class="fp-badge">待入库</div>
    </div>
    """, unsafe_allow_html=True)

    # 进度条
    progress = st.progress(0, text="⏳ 准备解析文档...")
    text = uploader_file.getvalue().decode("utf-8")

    steps = [
        (20, "🔍 正在解析文档结构..."),
        (55, "🧠 正在生成向量嵌入..."),
        (80, "💾 正在写入向量数据库..."),
    ]
    for pct, msg in steps:
        time.sleep(0.35)
        progress.progress(pct, text=msg)

    result = st.session_state["system"].upload_by_str(text, file_name)

    for pct in range(85, 101, 3):
        time.sleep(0.05)
        progress.progress(min(pct, 100), text="✅ 入库完成")

    progress.empty()

    # 结果展示
    is_success = "成功" in str(result) or "ok" in str(result).lower()
    cls = "result-success" if is_success else "result-error"
    st.markdown(f'<div class="result-box {cls}">{result}</div>', unsafe_allow_html=True)

    if is_success:
        st.success("🎉 文档已成功入库，现在可以前往「AI 对话」页面进行提问了！")

else:
    # 空态
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📂</div>
        <p style="font-size:1rem; font-weight:500; color:#64748b;">暂无上传记录</p>
        <p style="font-size:.82rem;">拖拽 .txt 文件到上方区域，开始构建知识库</p>
    </div>
    """, unsafe_allow_html=True)
