import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import os
from typing import Dict, List, Optional

# 導入自定義模組
from website_ai_readiness import run_website_analysis
from eeat_benchmarking import run_eeat_benchmarking
from eeat_module import run_module_2 as run_eeat_analysis

# 設定頁面配置
st.set_page_config(
    page_title="SIE 平台 - 智能搜尋引擎優化分析",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS 樣式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-card {
        border-left-color: #28a745;
    }
    .warning-card {
        border-left-color: #ffc107;
    }
    .error-card {
        border-left-color: #dc3545;
    }
    .info-card {
        border-left-color: #17a2b8;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """主應用程式"""
    
    # 側邊欄配置
    with st.sidebar:
        st.title("🚀 SIE 平台")
        st.markdown("---")
        
        # API 金鑰設定
        gemini_api_key = st.text_input(
            "🔑 Gemini API 金鑰",
            type="password",
            help="輸入您的 Gemini API 金鑰以啟用 AI 建議功能"
        )
        
        st.markdown("---")
        
        # 頁面選擇
        page = st.selectbox(
            "📄 選擇分析模組",
            [
                "🏠 首頁",
                "🔧 模組 1: 網站 AI 就緒度分析",
                "📊 模組 2: E-E-A-T 基準分析",
                "🎯 完整 E-E-A-T 分析",
                "📈 分析報告"
            ]
        )
        
        st.markdown("---")
        st.markdown("### 📋 使用說明")
        st.markdown("""
        1. **模組 1**: 分析網站技術健康度與 AI 就緒度
        2. **模組 2**: 動態 E-E-A-T 評估與競爭基準分析
        3. **完整分析**: 傳統 E-E-A-T 分析
        4. **報告**: 查看歷史分析結果
        """)
    
    # 主內容區域
    if page == "🏠 首頁":
        show_homepage()
    elif page == "🔧 模組 1: 網站 AI 就緒度分析":
        show_module1_page(gemini_api_key)
    elif page == "📊 模組 2: E-E-A-T 基準分析":
        show_module2_page(gemini_api_key)
    elif page == "🎯 完整 E-E-A-T 分析":
        show_full_eeat_page(gemini_api_key)
    elif page == "📈 分析報告":
        show_reports_page()

def show_homepage():
    """顯示首頁"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🚀 SIE 平台")
    st.markdown("#### 智能搜尋引擎優化分析系統")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 功能介紹
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 模組 1: 網站 AI 就緒度分析")
        st.markdown("""
        - ✅ robots.txt 與 LLM 遵從性檢查
        - ✅ sitemap.xml 驗證
        - ✅ llms.txt 前瞻性指標
        - ✅ HTTPS 安全性檢查
        - ✅ 內部連結結構分析
        - ✅ Schema.org 結構化資料檢測
        - ✅ 內容可讀性評估
        - ✅ AI 技術建議生成
        """)
    
    with col2:
        st.markdown("### 📊 模組 2: E-E-A-T 基準分析")
        st.markdown("""
        - 🤖 AI 領導者識別與分析
        - 📊 動態媒體權重評估
        - 🏆 競爭對手基準分析
        - 📈 趨勢追蹤與預測
        - 🎯 策略建議生成
        - 📱 社交媒體權威分析
        - 📰 媒體提及監控
        - 🔄 市場機會識別
        """)
    
    st.markdown("---")
    
    # 統計資訊
    st.markdown("### 📊 平台統計")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("分析次數", "1,234", "+12%")
    
    with col2:
        st.metric("網站分析", "567", "+8%")
    
    with col3:
        st.metric("競爭對手", "89", "+15%")
    
    with col4:
        st.metric("建議生成", "2,345", "+20%")

def show_module1_page(gemini_api_key: Optional[str]):
    """顯示模組 1 頁面"""
    st.title("🔧 模組 1: 網站 AI 就緒度分析")
    st.markdown("分析網站的技術健康度與 AI 就緒度")
    
    # 輸入區域
    with st.form("module1_form"):
        website_url = st.text_input(
            "🌐 網站 URL",
            placeholder="例如: example.com 或 https://example.com",
            help="輸入要分析的網站 URL"
        )
        
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    
    if submitted and website_url:
        with st.spinner("🔍 正在分析網站 AI 就緒度..."):
            try:
                # 執行分析
                result = run_website_analysis(website_url, gemini_api_key)
                
                if "error" in result:
                    st.error(f"分析失敗: {result['error']}")
                    return
                
                analysis_data = result.get("technical_seo_ai_readiness", {})
                
                # 顯示分析結果
                display_module1_results(analysis_data, website_url)
                
                # 儲存結果
                save_analysis_result("module1", website_url, result)
                
            except Exception as e:
                st.error(f"分析過程中發生錯誤: {str(e)}")

def display_module1_results(analysis_data: Dict, website_url: str):
    """顯示模組 1 分析結果"""
    st.success(f"✅ 分析完成: {website_url}")
    
    # 總體評分
    col1, col2, col3 = st.columns(3)
    
    with col1:
        root_files = analysis_data.get("root_files", {})
        root_score = calculate_root_files_score(root_files)
        st.metric("根檔案評分", f"{root_score}/100", "✅")
    
    with col2:
        architecture = analysis_data.get("architecture_signals", {})
        arch_score = calculate_architecture_score(architecture)
        st.metric("架構評分", f"{arch_score}/100", "🏗️")
    
    with col3:
        llm_friendliness = analysis_data.get("llm_friendliness", {})
        llm_score = calculate_llm_friendliness_score(llm_friendliness)
        st.metric("LLM 友善度", f"{llm_score}/100", "🤖")
    
    st.markdown("---")
    
    # 詳細分析結果
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📁 根檔案", "🏗️ 架構", "🤖 LLM 友善度", "💡 建議", "📝 用戶評論分析", "🧭 內容與消費者旅程對應"])
    
    with tab1:
        display_root_files_analysis(analysis_data.get("root_files", {}))
    
    with tab2:
        display_architecture_analysis(analysis_data.get("architecture_signals", {}))
    
    with tab3:
        display_llm_friendliness_analysis(analysis_data.get("llm_friendliness", {}))
    
    with tab4:
        display_recommendations(analysis_data.get("actionable_recommendations", []))
    
    with tab5:
        review = analysis_data.get('user_review_analysis', {})
        st.subheader('用戶評論分析')
        st.write(f"評論總數: {review.get('review_count', 0)}")
        st.write(f"平均分數: {review.get('average_rating')}")
        st.write(f"情感分布: {review.get('sentiment_summary')}")
        for r in review.get('review_samples', []):
            st.markdown(f"- 第{r.get('page', 1)}頁 | {r.get('sentiment', '')} | {r.get('author', '匿名')}: {r.get('text')}")
    
    with tab6:
        faq_journey = analysis_data.get('faq_journey_analysis', {})
        st.subheader('網站內容與消費者旅程對應分析')
        faqs = faq_journey.get('faqs', [])
        if not faqs:
            st.info('尚未產生 FAQ 或缺少品類/品牌/市場資訊')
        else:
            for f in faqs:
                covered = '✅ 覆蓋' if f.get('covered') else '❌ 未覆蓋'
                authority = '（具權威性）' if f.get('authority') else ''
                st.markdown(f"- **{f['question_zh']}** / {f['question_en']}<br>\n  {covered} {authority} 於 {f.get('location', '')}", unsafe_allow_html=True)
            # 建議
            not_covered = [f for f in faqs if not f.get('covered')]
            if not_covered:
                st.warning('部分常見消費者問題未被覆蓋，建議：')
                for f in not_covered:
                    st.markdown(f"- 請補充：{f['question_zh']} / {f['question_en']}")
            else:
                st.success('所有關鍵消費者問題皆有覆蓋，內容完整！')

def show_module2_page(gemini_api_key: Optional[str]):
    """顯示模組 2 頁面"""
    st.title("📊 模組 2: E-E-A-T 基準分析")
    st.markdown("動態 E-E-A-T 評估與競爭基準分析")
    
    # 輸入區域
    with st.form("module2_form"):
        markets = st.multiselect(
            "🌏 市場（可多選）",
            ["台灣", "中國", "美國", "全球", "其他"],
            default=["台灣"],
            help="可同時分析多個市場"
        )
        if "其他" in markets:
            custom_market = st.text_input("請輸入自訂市場名稱", "")
            if custom_market:
                markets = [m for m in markets if m != "其他"] + [custom_market]
        industry = st.selectbox(
            "🏭 行業",
            ["家電", "電子", "汽車", "食品", "金融", "醫療", "其他"],
            index=0,
            help="選擇要分析的行業"
        )
        if industry == "其他":
            industry = st.text_input("請輸入自訂行業名稱", "")
        brand = st.text_input(
            "🏢 品牌",
            placeholder="例如: ExampleBrand",
            help="輸入品牌名稱"
        )
        product = st.text_input(
            "📦 產品/品類",
            placeholder="例如: 空氣清淨機",
            help="輸入產品或品類名稱"
        )
        official_site = st.text_input(
            "🌐 官網連結",
            placeholder="例如: https://brand.com",
            help="輸入品牌或產品官網網址"
        )
        competitors = st.text_area(
            "🏆 競爭對手 (每行一個)",
            placeholder="competitor1.com\ncompetitor2.com\ncompetitor3.com",
            help="輸入競爭對手網站，每行一個"
        )
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    
    if submitted and official_site and markets:
        competitor_list = []
        if competitors:
            competitor_list = [comp.strip() for comp in competitors.split('\n') if comp.strip()]
        all_results = {}
        with st.spinner("🔍 正在執行多市場 E-E-A-T 基準分析..."):
            for market in markets:
                try:
                    result = run_eeat_benchmarking(
                        official_site, competitor_list, gemini_api_key, market, product, brand
                    )
                    all_results[market] = result.get("eeat_benchmarking", {})
                except Exception as e:
                    all_results[market] = {"error": str(e)}
        # 跨市場指標總覽表
        if len(all_results) > 1:
            overview = []
            for market, data in all_results.items():
                if "error" in data:
                    overview.append({
                        "市場": market,
                        "差距分數": "-",
                        "媒體分數": "-",
                        "社群分數": "-",
                        "領導者": "-"
                    })
                else:
                    gap = data.get("brand_gap_analysis", {})
                    media_weights = data.get("dynamic_media_weights", {})
                    media_score = media_weights.get("media_mentions", {}).get("media_coverage_score", "-")
                    social_score = media_weights.get("social_media_presence", {}).get("social_authority_score", "-")
                    leaders = data.get("leaders_recommendation", [])
                    leader_names = ", ".join([l.get("name", "") for l in leaders]) if leaders else "-"
                    overview.append({
                        "市場": market,
                        "差距分數": gap.get("gap_score", "-"),
                        "媒體分數": media_score,
                        "社群分數": social_score,
                        "領導者": leader_names
                    })
            df = pd.DataFrame(overview)
            st.markdown("### 🌏 跨市場指標總覽")
            st.dataframe(df, use_container_width=True)
        # 顯示多市場分析結果
        tabs = st.tabs([f"{m} 市場" for m in all_results])
        for i, market in enumerate(all_results):
            with tabs[i]:
                if "error" in all_results[market]:
                    st.error(f"{market} 分析失敗: {all_results[market]['error']}")
                else:
                    display_module2_results(all_results[market], official_site, market, industry, product, brand)
        # 儲存結果（僅存第一個市場結果）
        save_analysis_result("module2", official_site, {m: all_results[m] for m in all_results})

def display_module2_results(analysis_data: Dict, official_site: str, market: str, industry: str, product: str, brand: str):
    """顯示模組 2 分析結果（以市場為主分組）"""
    st.success(f"✅ 分析完成: {market}｜{industry}｜{brand}｜{product}")
    st.markdown(f"[官網連結]({official_site})")
    # 領導者比對區塊
    leaders = analysis_data.get("leaders_recommendation", [])
    st.subheader(f"🏆 {market}｜{industry}｜{product}｜{brand} 領導者比對")
    if not leaders:
        st.info("尚無 LLM 推薦領導者資料")
    else:
        for leader in leaders:
            star = "⭐" if leader.get("is_benchmark") else ""
            st.markdown(f"- [{leader['name']}]({leader['website']}) {star}<br>推薦說明：{leader['reason']}", unsafe_allow_html=True)
    st.markdown("---")
    # 品牌與標竿差異分析區塊
    gap = analysis_data.get("brand_gap_analysis", {})
    st.subheader(f"📉 {market}｜{brand} 與標竿差異分析")
    if not gap or not isinstance(gap, dict) or "summary" not in gap:
        st.info("尚無 LLM 差異分析資料")
    else:
        st.markdown(f"**整體差距分數**：{gap.get('gap_score', 'N/A')}/100")
        st.markdown(f"**優勢**：")
        for adv in gap.get("advantages", []):
            st.markdown(f"- {adv}")
        st.markdown(f"**劣勢**：")
        for disadv in gap.get("disadvantages", []):
            st.markdown(f"- {disadv}")
        st.markdown(f"**建議**：")
        for rec in gap.get("recommendations", []):
            st.markdown(f"- {rec}")
        st.markdown(f"**總結**：{gap.get('summary', '')}")
    st.markdown("---")
    # 總體評分（移除AI領導者分數）
    cols = st.columns(3)
    with cols[0]:
        media_weights = analysis_data.get("dynamic_media_weights", {})
        social_score = media_weights.get("social_media_presence", {})
        social_score = social_score.get("social_authority_score", 0)
        st.metric("社交媒體權威", f"{social_score:.1f}/100", "📱")
    with cols[1]:
        competitor_bench = analysis_data.get("competitor_benchmarking", {})
        market_position = competitor_bench.get("market_position", "unknown")
        st.metric(f"{market} 市場地位", str(market_position).title())
    with cols[2]:
        media_weights = analysis_data.get("dynamic_media_weights", {})
        media_score = media_weights.get("media_coverage_score", 0)
        st.metric("媒體權重分數", f"{media_score}/100", "📰")
    st.markdown("---")
    # 媒體權重分析區塊
    media_weights = analysis_data.get("dynamic_media_weights", {})
    st.subheader("📊 媒體權重分析")
    st.markdown(f"**媒體權重分數**：{media_weights.get('media_coverage_score', 0)}/100")
    st.markdown(f"**覆蓋率**：{media_weights.get('coverage_rate', 0):.0%}（{media_weights.get('covered_count', 0)}/{media_weights.get('total_count', 0)}）")
    sources = media_weights.get("sources", {})
    # 來源清單表格
    for media_type in ["新聞", "社群", "論壇", "影音", "Wiki"]:
        items = sources.get(media_type, [])
        if not items:
            continue
        st.markdown(f"#### {media_type}")
        df = pd.DataFrame([
            {
                "來源名稱": src.get('name', ''),
                "信任度": src.get('trust_score', 0),
                "高權威": '⭐' if src.get('llm_favorite') else '',
                "覆蓋": '✅' if src.get('covered') else '❌',
                "推論分數": src.get('llm_score', '') if media_type != "新聞" else '',
                "推論依據": src.get('llm_reason', '') if media_type != "新聞" else '',
                "排序依據": src.get('reason', '')
            }
            for src in items
        ])
        st.dataframe(df, use_container_width=True)
    # 媒體權重分數長條圖
    bar_data = []
    for media_type in ["新聞", "社群", "論壇", "影音", "Wiki"]:
        items = sources.get(media_type, [])
        for src in items:
            bar_data.append({
                "來源": src.get('name', ''),
                "類型": media_type,
                "信任度": src.get('trust_score', 0),
                "覆蓋": 1 if src.get('covered') else 0
            })
    if bar_data:
        bar_df = pd.DataFrame(bar_data)
        fig = go.Figure()
        for t in bar_df['類型'].unique():
            sub = bar_df[bar_df['類型'] == t]
            fig.add_trace(go.Bar(
                x=sub['來源'],
                y=sub['信任度'],
                name=t,
                marker_color=None
            ))
        fig.update_layout(barmode='group', title='來源信任度長條圖', xaxis_title='來源', yaxis_title='信任度')
        st.plotly_chart(fig, use_container_width=True)
    # 各類型覆蓋率雷達圖
    radar_labels = []
    radar_values = []
    for media_type in ["新聞", "社群", "論壇", "影音", "Wiki"]:
        items = sources.get(media_type, [])
        if items:
            radar_labels.append(media_type)
            radar_values.append(sum(1 for src in items if src.get('covered')) / len(items))
    if radar_labels:
        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(r=radar_values, theta=radar_labels, fill='toself', name='覆蓋率'))
        radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])), showlegend=False, title='各類型來源覆蓋率雷達圖')
        st.plotly_chart(radar_fig, use_container_width=True)
    # 匯出內容自訂勾選
    st.markdown("---")
    export_options = st.multiselect(
        "選擇要匯出的內容區塊",
        ["來源清單", "媒體權重圖表", "競爭分析", "差異分析", "策略建議"],
        default=["來源清單", "媒體權重圖表"]
    )
    pdf_title = st.text_input("PDF 報告標題", f"{market}｜{brand} 媒體權重與E-E-A-T分析報告")
    # 競爭分析表格
    competitor_bench = analysis_data.get("competitor_benchmarking", {})
    if "競爭分析" in export_options:
        st.subheader("🏆 競爭對手基準分析")
        comp_df = pd.DataFrame([
            {"競爭對手": k, **v} for k, v in competitor_bench.get("competitors", {}).items()
        ]) if competitor_bench.get("competitors") else pd.DataFrame()
        if not comp_df.empty:
            st.dataframe(comp_df, use_container_width=True)
    # 差異分析表格
    gap = analysis_data.get("brand_gap_analysis", {})
    if "差異分析" in export_options:
        st.subheader("📉 品牌與標竿差異分析")
        gap_df = pd.DataFrame({
            "優勢": gap.get("advantages", []),
            "劣勢": gap.get("disadvantages", []),
            "建議": gap.get("recommendations", [])
        })
        st.dataframe(gap_df, use_container_width=True)
    # 策略建議表格
    strategies = analysis_data.get("strategic_recommendations", [])
    if "策略建議" in export_options:
        st.subheader("💡 策略建議")
        strat_df = pd.DataFrame(strategies)
        if not strat_df.empty:
            st.dataframe(strat_df, use_container_width=True)
    # 進階 PDF/Excel 匯出
    import io
    import base64
    export_sections = []
    if "來源清單" in export_options:
        export_sections.append(("來源清單", export_df))
    if "媒體權重圖表" in export_options and bar_data:
        export_sections.append(("媒體權重長條圖", bar_df))
    if "競爭分析" in export_options and not comp_df.empty:
        export_sections.append(("競爭分析", comp_df))
    if "差異分析" in export_options:
        export_sections.append(("差異分析", gap_df))
    if "策略建議" in export_options and not strat_df.empty:
        export_sections.append(("策略建議", strat_df))
    # 匯出 Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        for title, df in export_sections:
            df.to_excel(writer, sheet_name=title[:31], index=False)
    st.download_button(
        label="自訂內容匯出 Excel",
        data=excel_buffer.getvalue(),
        file_name=f"{market}_{brand}_media_analysis_custom.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    # 進階 PDF 匯出
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 12, pdf_title, ln=True, align='C')
        pdf.set_font("Arial", size=10)
        for title, df in export_sections:
            pdf.ln(8)
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(0, 10, title, ln=True)
            pdf.set_font("Arial", size=10)
            for i, row in df.iterrows():
                pdf.cell(0, 8, str(row.to_dict()), ln=True)
        pdf_buffer = io.BytesIO(pdf.output(dest='S').encode('latin1'))
        st.download_button(
            label="自訂內容匯出 PDF",
            data=pdf_buffer.getvalue(),
            file_name=f"{market}_{brand}_media_analysis_custom.pdf",
            mime="application/pdf"
        )
    except Exception:
        st.info("如需 PDF 匯出，請安裝 fpdf 套件。")
    # 其餘分析區塊（移除AI領導者分析tab）
    tab1, tab2, tab3 = st.tabs([f"🏆 {market} 競爭分析", "📈 趨勢", "💡 策略"])
    with tab1:
        display_competitor_analysis(analysis_data.get("competitor_benchmarking", {}))
    with tab2:
        display_trend_analysis(analysis_data.get("trend_analysis", {}))
    with tab3:
        display_strategic_recommendations(analysis_data.get("strategic_recommendations", []))

def show_full_eeat_page(gemini_api_key: Optional[str]):
    """顯示完整 E-E-A-T 分析頁面"""
    st.title("🎯 完整 E-E-A-T 分析")
    st.markdown("傳統 E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) 分析")
    
    # 輸入區域
    with st.form("full_eeat_form"):
        website_url = st.text_input(
            "🌐 網站 URL",
            placeholder="例如: example.com",
            help="輸入要分析的網站 URL"
        )
        
        company_name = st.text_input(
            "🏢 公司名稱",
            placeholder="例如: Example Corp",
            help="輸入公司或組織名稱"
        )
        
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    
    if submitted and website_url and company_name:
        with st.spinner("🔍 正在執行完整 E-E-A-T 分析..."):
            try:
                # 執行分析
                result = run_eeat_analysis(website_url, company_name, gemini_api_key)
                
                if "error" in result:
                    st.error(f"分析失敗: {result['error']}")
                    return
                
                # 顯示分析結果
                display_full_eeat_results(result, website_url, company_name)
                
                # 儲存結果
                save_analysis_result("full_eeat", website_url, result)
                
            except Exception as e:
                st.error(f"分析過程中發生錯誤: {str(e)}")

def display_full_eeat_results(result: Dict, website_url: str, company_name: str):
    """顯示完整 E-E-A-T 分析結果"""
    st.success(f"✅ 分析完成: {company_name} ({website_url})")
    
    # 總體 E-E-A-T 分數
    eeat_scores = result.get("eeat_scores", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        experience_score = eeat_scores.get("experience", 0)
        st.metric("Experience", f"{experience_score}/100", "📚")
    
    with col2:
        expertise_score = eeat_scores.get("expertise", 0)
        st.metric("Expertise", f"{expertise_score}/100", "🎓")
    
    with col3:
        authoritativeness_score = eeat_scores.get("authoritativeness", 0)
        st.metric("Authoritativeness", f"{authoritativeness_score}/100", "🏆")
    
    with col4:
        trustworthiness_score = eeat_scores.get("trustworthiness", 0)
        st.metric("Trustworthiness", f"{trustworthiness_score}/100", "✅")
    
    # 顯示詳細分析結果
    display_eeat_detailed_results(result)

def show_reports_page():
    """顯示分析報告頁面"""
    st.title("📈 分析報告")
    st.markdown("查看歷史分析結果與趨勢")
    
    # 載入歷史報告
    reports = load_analysis_reports()
    
    if not reports:
        st.info("📝 尚無分析報告，請先執行分析")
        return
    
    # 報告列表
    for report in reports:
        with st.expander(f"📊 {report['timestamp']} - {report['website']} ({report['module']})"):
            st.json(report['result'])

# 輔助函數
def calculate_root_files_score(root_files: Dict) -> int:
    """計算根檔案評分"""
    score = 0
    if root_files.get("has_robots_txt"):
        score += 25
    if root_files.get("robots_allows_ai_bots"):
        score += 25
    if root_files.get("has_sitemap_xml"):
        score += 25
    if root_files.get("sitemap_is_valid"):
        score += 15
    if root_files.get("has_llms_txt"):
        score += 10
    return score

def calculate_architecture_score(architecture: Dict) -> int:
    """計算架構評分"""
    score = 0
    if architecture.get("uses_https"):
        score += 30
    if architecture.get("internal_link_structure") == "good":
        score += 40
    elif architecture.get("internal_link_structure") == "fair":
        score += 20
    score += min(architecture.get("estimated_authority_links", 0) * 2, 30)
    return score

def calculate_llm_friendliness_score(llm_friendliness: Dict) -> int:
    """計算 LLM 友善度評分"""
    score = 0
    score += len(llm_friendliness.get("schema_detected", [])) * 10
    if llm_friendliness.get("content_readability") == "good":
        score += 40
    elif llm_friendliness.get("content_readability") == "fair":
        score += 20
    score += min(llm_friendliness.get("structured_data_score", 0) * 5, 30)
    return min(score, 100)

def display_root_files_analysis(root_files: Dict):
    """顯示根檔案分析結果"""
    st.subheader("📁 根檔案分析")
    
    # robots.txt
    if root_files.get("has_robots_txt"):
        st.success("✅ robots.txt 存在")
        if root_files.get("robots_allows_ai_bots"):
            st.success("✅ 允許 AI bots 存取")
        else:
            st.warning("⚠️ 封鎖了某些 AI bots")
    else:
        st.error("❌ robots.txt 不存在")
    
    # sitemap.xml
    if root_files.get("has_sitemap_xml"):
        st.success("✅ sitemap.xml 存在")
        if root_files.get("sitemap_is_valid"):
            st.success("✅ sitemap.xml 格式正確")
        else:
            st.warning("⚠️ sitemap.xml 格式可能有問題")
    else:
        st.error("❌ sitemap.xml 不存在")
    
    # llms.txt
    if root_files.get("has_llms_txt"):
        st.success("✅ llms.txt 存在 (前瞻性指標)")
        st.text_area("llms.txt 內容", root_files.get("llms_txt_content", ""), height=100)
    else:
        st.info("ℹ️ llms.txt 不存在 (這是正常的，目前仍是新興標準)")

def display_architecture_analysis(architecture: Dict):
    """顯示架構分析結果"""
    st.subheader("🏗️ 架構分析")
    
    # HTTPS
    if architecture.get("uses_https"):
        st.success("✅ 使用 HTTPS")
    else:
        st.error("❌ 未使用 HTTPS")
    
    # 內部連結結構
    link_structure = architecture.get("internal_link_structure", "unknown")
    if link_structure == "good":
        st.success("✅ 內部連結結構良好")
    elif link_structure == "fair":
        st.info("ℹ️ 內部連結結構一般")
    else:
        st.warning("⚠️ 內部連結結構較差")
    
    # 外部連結
    external_links = architecture.get("external_links_count", 0)
    st.metric("外部連結數量", external_links)

def display_llm_friendliness_analysis(llm_friendliness: Dict):
    """顯示 LLM 友善度分析結果"""
    st.subheader("🤖 LLM 友善度分析")
    
    # 結構化資料
    schema_types = llm_friendliness.get("schema_detected", [])
    if schema_types:
        st.success(f"✅ 發現結構化資料: {', '.join(schema_types)}")
    else:
        st.warning("⚠️ 未發現結構化資料")
    
    # 內容可讀性
    readability = llm_friendliness.get("content_readability", "unknown")
    if readability == "good":
        st.success("✅ 內容結構良好")
    elif readability == "fair":
        st.info("ℹ️ 內容結構一般")
    else:
        st.warning("⚠️ 內容結構較差")
    
    # PageSpeed 分數
    pagespeed = llm_friendliness.get("pagespeed_scores", {})
    if pagespeed:
        col1, col2 = st.columns(2)
        with col1:
            mobile_perf = pagespeed.get("mobile", {}).get("performance", 0)
            st.metric("Mobile Performance", f"{mobile_perf}/100")
        with col2:
            desktop_perf = pagespeed.get("desktop", {}).get("performance", 0)
            st.metric("Desktop Performance", f"{desktop_perf}/100")

def display_recommendations(recommendations: List[Dict]):
    """顯示改善建議"""
    st.subheader("💡 改善建議")
    
    if not recommendations:
        st.info("🎉 沒有發現需要改善的問題！")
        return
    
    for i, rec in enumerate(recommendations, 1):
        priority_color = {
            "High": "🔴",
            "Medium": "🟡",
            "Low": "🟢"
        }.get(rec.get("priority", "Medium"), "🟡")
        
        st.markdown(f"""
        ### {priority_color} {rec.get("issue", "Unknown Issue")}
        **建議**: {rec.get("recommendation", "No recommendation")}
        **優先級**: {rec.get("priority", "Medium")}
        **類別**: {rec.get("category", "General")}
        """)

def display_competitor_analysis(competitor_bench: Dict):
    """顯示競爭對手分析"""
    st.subheader("🏆 競爭對手分析")
    
    # 市場地位
    market_position = competitor_bench.get("market_position", "unknown")
    position_emoji = {
        "leader": "🏆",
        "strong": "💪",
        "average": "📊",
        "laggard": "⚠️"
    }.get(market_position, "❓")
    
    st.markdown(f"**市場地位**: {position_emoji} {market_position.title()}")
    
    # 競爭優勢
    advantages = competitor_bench.get("competitive_advantages", [])
    if advantages:
        st.success("✅ 競爭優勢:")
        for advantage in advantages:
            st.markdown(f"- {advantage}")
    
    # 改善機會
    opportunities = competitor_bench.get("improvement_opportunities", [])
    if opportunities:
        st.warning("⚠️ 改善機會:")
        for opportunity in opportunities:
            st.markdown(f"- {opportunity}")

def display_trend_analysis(trend_analysis: Dict):
    """顯示趨勢分析"""
    st.subheader("📈 趨勢分析")
    
    # 當前趨勢
    current_trends = trend_analysis.get("current_trends", [])
    if current_trends:
        st.markdown("### 🔥 當前趨勢")
        for trend in current_trends:
            st.markdown(f"- {trend}")
    
    # 預測成長
    predictions = trend_analysis.get("predicted_growth", {})
    if predictions:
        st.markdown("### 📊 預測成長")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("AI 採用率", f"{predictions.get('ai_adoption_rate', 0):.1f}%")
            st.metric("內容消費成長", f"{predictions.get('content_consumption_growth', 0):.1f}%")
        with col2:
            st.metric("社交參與度增加", f"{predictions.get('social_engagement_increase', 0):.1f}%")
            st.metric("市場份額成長", f"{predictions.get('market_share_growth', 0):.1f}%")

def display_strategic_recommendations(recommendations: List[Dict]):
    """顯示策略建議"""
    st.subheader("💡 策略建議")
    
    if not recommendations:
        st.info("🎉 沒有策略建議")
        return
    
    for i, rec in enumerate(recommendations, 1):
        priority_color = {
            "High": "🔴",
            "Medium": "🟡",
            "Low": "🟢"
        }.get(rec.get("priority", "Medium"), "🟡")
        
        st.markdown(f"""
        ### {priority_color} {rec.get("strategy", "Unknown Strategy")}
        **描述**: {rec.get("description", "No description")}
        **優先級**: {rec.get("priority", "Medium")}
        **時間線**: {rec.get("timeline", "Unknown")}
        **預期影響**: {rec.get("expected_impact", "Unknown")}
        
        **實施步驟**:
        """)
        
        steps = rec.get("implementation_steps", [])
        for step in steps:
            st.markdown(f"- {step}")

def display_eeat_detailed_results(result: Dict):
    """顯示詳細 E-E-A-T 結果"""
    # 這裡可以添加更詳細的 E-E-A-T 結果顯示
    st.json(result)

def save_analysis_result(module: str, website: str, result: Dict):
    """儲存分析結果"""
    # 這裡可以實現結果儲存邏輯
    pass

def load_analysis_reports():
    """載入分析報告"""
    # 這裡可以實現報告載入邏輯
    return []

if __name__ == "__main__":
    main() 