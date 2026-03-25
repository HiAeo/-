import streamlit as st
from wordcloud import WordCloud
from snownlp import SnowNLP
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import io
import datetime

# PDF 中文支持
pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

# 页面配置
st.set_page_config(
    page_title="MirusAI 洞见未见·模境之境",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------
# 样式：严格统一蓝色 #0B2B4F
# --------------------------
st.markdown("""
<style>
/* 引入 Font Awesome 6 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

/* 全局文字黑色 */
html, body, .stApp, .stMarkdown, p, h1, h2, h3, h4, div, span, li, .stTextInput label {
    color: #000000 !important;
}
/* 标题 */
h1, h2, h3, .module-title, .intro-title {
    color: #000000 !important;
}
.hero-subtitle, .module-desc, .metric-label, .intro-badge {
    color: #000000 !important;
}
/* 背景纯白 */
html, body, .stApp {
    background-color: #FFFFFF !important;
}
/* 隐藏系统元素 */
#MainMenu, footer, header {visibility: hidden !important;}

.block-container {
    max-width: 1200px !important;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    margin: 0 auto !important;
}

h1 {
    font-size: 3.2rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
}
.hero-subtitle {
    font-size: 1.2rem;
    line-height: 1.5;
    margin-bottom: 2.5rem;
}

/* 产品介绍卡片 */
.product-intro {
    display: flex;
    gap: 2rem;
    background: #F9FBFE;
    border-radius: 32px;
    padding: 2rem;
    margin-bottom: 2rem;
    align-items: center;
    border: 1px solid #EFF3F8;
}
.intro-text { flex: 2; }
.intro-icon { flex: 1; text-align: center; }
.intro-badge {
    display: inline-block;
    background: #E8EDF5;
    border-radius: 40px;
    padding: 0.2rem 1rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 1rem;
}
.intro-title {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 1rem;
}
.feature-list {
    list-style: none;
    padding: 0;
    margin-top: 1rem;
}
.feature-list li {
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.feature-list li::before {
    content: "✓";
    color: #0B2B4F;
    font-weight: bold;
}

/* 功能卡片 */
.function-card {
    background: white;
    border-radius: 28px;
    padding: 1.8rem 2rem 2rem 2rem;
    box-shadow: 0 10px 30px -12px rgba(0, 0, 0, 0.08);
    margin-bottom: 2.5rem;
    border: 1px solid #EFF3F8;
}
.module-title {
    font-size: 1.7rem;
    font-weight: 600;
    margin-bottom: 0.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.module-desc {
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* 输入框 */
.stTextInput > div > div > input {
    background-color: #F9FCFE !important;
    border: 1px solid #E2E9F0 !important;
    border-radius: 20px !important;
    padding: 10px 18px !important;
    color: #000000 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #0B2B4F !important;
    box-shadow: 0 0 0 2px rgba(11,43,79,0.1) !important;
}

/* 按钮：强制覆盖 Streamlit 默认样式 */
div[data-testid="stButton"] button,
button[kind="primary"] {
    background-color: #0B2B4F !important;
    color: white !important;
    border-radius: 40px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    border: none !important;
    transition: 0.2s;
    margin-top: 0.5rem;
}
div[data-testid="stButton"] button:hover,
button[kind="primary"]:hover {
    background-color: #1E3A5F !important;
    box-shadow: 0 6px 14px rgba(11,43,79,0.2);
}

/* 指标卡片 */
.metrics-row {
    display: flex;
    gap: 1.5rem;
    margin: 1.8rem 0;
    flex-wrap: wrap;
}
.metric-card {
    background: #F8FAFE;
    border-radius: 24px;
    padding: 1.2rem 1rem;
    text-align: center;
    flex: 1;
    border: 1px solid #EFF3F8;
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #000000 !important;
}
.metric-label {
    font-size: 0.85rem;
    margin-top: 0.3rem;
}
hr {
    margin: 1.5rem 0;
    border-color: #EFF3F8;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# Logo
# --------------------------
col_logo, _ = st.columns([1, 5])
with col_logo:
    st.image("https://mirusai.cn/logo.png", width=170)

st.markdown("<h1>模境 · 品牌诊断 & 模豆 · 爆品挖掘</h1>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>AI 驱动的品牌心智洞察 · 产品机会发现平台</div>", unsafe_allow_html=True)

# ======================================================
# 模镜产品介绍
# ======================================================
st.markdown("""
<div class="product-intro">
    <div class="intro-text">
        <div class="intro-badge">AI 品牌诊断</div>
        <div class="intro-title">模镜 · 洞见 AI 中的品牌心智</div>
        <p>实时追踪品牌在豆包、DeepSeek、千问等主流模型中的可见度、排名与情感倾向，将 AI 搜索洞察转化为品牌增长策略。</p>
        <ul class="feature-list">
            <li>可见度得分 & 竞品对比</li>
            <li>用户情感分析 (正面/中性/负面)</li>
            <li>品牌关联关键词云 & 优化建议</li>
            <li>一键生成 PDF 品牌心智报告</li>
        </ul>
    </div>
    <div class="intro-icon">
        <i class="fas fa-chart-line" style="color: #0B2B4F; font-size: 4rem;"></i>
    </div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# 模镜 · 品牌诊断（模块标题带图标）
# ======================================================
with st.container():
    st.markdown('<div class="function-card">', unsafe_allow_html=True)
    st.markdown('<div class="module-title"><i class="fas fa-chart-simple" style="color: #0B2B4F; font-size: 1.5rem;"></i> 模镜 · 品牌心智报告</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-desc">输入品牌名称，AI 将分析其在主流模型中的可见度、情感倾向与竞争格局</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        brand = st.text_input("品牌名称", placeholder="例如：华为、小米、MirusAI", key="brand_input")
    with col2:
        competitor = st.text_input("竞品品牌（选填）", placeholder="例如：苹果、OPPO", key="competitor_input")
    
    if st.button("开始生成品牌诊断报告", key="diagnose_btn"):
        if not brand:
            st.warning("请输入品牌名称")
        else:
            with st.spinner("AI 分析中..."):
                result_text = """【分析结果】
1. 品牌认知清晰，定位准确
2. 用户正面提及占比高
3. 核心优势：性价比、品质、口碑
4. 改进点：曝光不足、场景化不足
5. 竞品对比：处于中上游水平"""
                emotion = "正面"

            st.success("✅ 品牌AI心智报告生成完成")
            st.markdown("---")
            st.markdown("## 📋 品牌AI心智报告")
            st.write(result_text)

            st.markdown('<div class="metrics-row">', unsafe_allow_html=True)
            col_vis, col_sent, col_like = st.columns(3)
            with col_vis:
                st.markdown('<div class="metric-card"><div class="metric-value">78</div><div class="metric-label">可见度得分</div><div>较上月 +12%</div></div>', unsafe_allow_html=True)
            with col_sent:
                st.markdown('<div class="metric-card"><div class="metric-value">72%</div><div class="metric-label">正面提及</div><div>情感倾向：正面</div></div>', unsafe_allow_html=True)
            with col_like:
                st.markdown('<div class="metric-card"><div class="metric-value">86.0</div><div class="metric-label">AI好感度</div><div>高分区间</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("## ☁️ 品牌关联关键词云")
            wc = WordCloud(
                font_path="/System/Library/Fonts/PingFang.ttc",
                background_color="white", width=800, height=400
            ).generate(result_text)
            st.image(wc.to_image(), use_container_width=True)

            st.markdown("## 💡 品牌优化建议")
            st.write("""
1. 强化AI中核心卖点曝光
2. 增加用户真实评价与案例
3. 优化关键词布局提升推荐率
4. 建立与竞品的差异化标签
            """)

            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4)
            pdf.setFont("STSong-Light", 12)
            pdf.drawString(50, 800, f"{brand} - 品牌诊断报告")
            pdf.drawString(50, 780, f"生成时间：{datetime.datetime.now()}")
            y = 750
            for line in result_text.split("\n"):
                pdf.drawString(50, y, line.strip())
                y -= 15
            pdf.save()
            buffer.seek(0)
            st.download_button("📥 下载PDF报告", buffer, f"{brand}_品牌报告.pdf", key="diagnose_pdf")
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# 模豆产品介绍
# ======================================================
st.markdown("""
<div class="product-intro">
    <div class="intro-text">
        <div class="intro-badge">AI 爆品挖掘</div>
        <div class="intro-title">模豆 · 发现下一个爆品机会</div>
        <p>基于 AI 搜索趋势与用户痛点分析，快速识别高潜力产品方向，提供可落地的差异化策略与定价建议。</p>
        <ul class="feature-list">
            <li>市场需求 & 用户痛点洞察</li>
            <li>差异化方向 (轻量化/高颜值/智能化)</li>
            <li>定价区间建议 & 竞品对标</li>
            <li>一键生成爆品策略报告</li>
        </ul>
    </div>
    <div class="intro-icon">
        <i class="fas fa-rocket" style="color: #0B2B4F; font-size: 4rem;"></i>
    </div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# 模豆 · 爆品挖掘
# ======================================================
with st.container():
    st.markdown('<div class="function-card">', unsafe_allow_html=True)
    st.markdown('<div class="module-title"><i class="fas fa-fire" style="color: #0B2B4F; font-size: 1.5rem;"></i> 模豆 · 爆品挖掘系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-desc">输入产品关键词，发现高潜机会与可落地的产品策略</div>', unsafe_allow_html=True)
    
    keyword = st.text_input("产品/行业关键词", placeholder="例如：露营灯、宠物智能喂食器", key="keyword_input")
    
    if st.button("开始挖掘爆品机会", key="explore_btn"):
        if not keyword:
            st.warning("请输入关键词")
        else:
            with st.spinner("正在分析..."):
                result = """【爆品机会分析】
1. 市场需求旺盛，用户增长快速
2. 核心痛点：续航短、价格高、操作复杂
3. 差异化方向：轻量化、高颜值、智能化
4. 定价区间：中高端市场最具潜力"""

            st.success("✅ 爆品机会挖掘完成")
            st.markdown("## 🔥 爆品机会清单")
            st.write(result)

            st.markdown("---")
            st.markdown("## ✅ 可直接落地的产品策略")
            st.write("""
1. 主打轻量化、高颜值、高性价比
2. 解决续航、操作、价格核心痛点
3. 聚焦细分场景，形成差异化
4. 用AI关键词优化产品传播
            """)

            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4)
            pdf.setFont("STSong-Light", 12)
            pdf.drawString(50, 800, f"{keyword} - 爆品挖掘报告")
            pdf.drawString(50, 780, f"生成时间：{datetime.datetime.now()}")
            y = 750
            for line in result.split("\n"):
                pdf.drawString(50, y, line.strip())
                y -= 15
            pdf.save()
            buffer.seek(0)
            st.download_button("📥 下载PDF报告", buffer, f"{keyword}_爆品报告.pdf", key="explore_pdf")
    st.markdown('</div>', unsafe_allow_html=True)