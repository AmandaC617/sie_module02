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
from sie_module02.website_ai_readiness import run_website_analysis
from sie_module02.eeat_benchmarking import run_eeat_benchmarking
from sie_module02.eeat_module import run_module_2 as run_eeat_analysis
from sie_module02.ai_accuracy_checker import run_ai_accuracy_check

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
        gemini_api_key = st.text_input(
            "🔑 Gemini API 金鑰",
            type="password",
            help="輸入您的 Gemini API 金鑰以啟用 AI 建議功能"
        )
        st.markdown("---")
        page = st.selectbox(
            "📄 選擇分析模組",
            [
                "🏠 首頁",
                "🔧 模組 1: 網站 AI 就緒度分析",
                "📊 模組 2: E-E-A-T 基準分析",
                "🎯 完整 E-E-A-T 分析",
                "🔍 模組 3: AI 資訊正確度檢查",
                "📈 分析報告"
            ]
        )
        st.markdown("---")
        st.markdown("### 📋 使用說明")
        st.markdown("""
        1. **模組 1**: 分析網站技術健康度與 AI 就緒度
        2. **模組 2**: 動態 E-E-A-T 評估與競爭基準分析
        3. **完整分析**: 傳統 E-E-A-T 分析
        4. **模組 3**: AI 資訊正確度檢查與深度比對
        5. **報告**: 查看歷史分析結果
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
    elif page == "🔍 模組 3: AI 資訊正確度檢查":
        show_module3_page(gemini_api_key)
    elif page == "📈 分析報告":
        show_reports_page()

def show_homepage():
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🚀 SIE 平台")
    st.markdown("### 智能搜尋引擎優化分析系統")
    st.markdown("</div>", unsafe_allow_html=True)
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
    with col2:
        st.markdown("### 🔍 模組 3: AI 資訊正確度檢查")
        st.markdown("""
        - 📚 權威原始資料擷取
        - 🔍 精準詞組比對分析
        - 🧠 廣泛語意一致性評估
        - 📊 雙維度評分系統
        - 🔄 進階不匹配分析
        - 💾 智能快取機制
        - 📋 詳細分析報告
        - 🎯 事實查核建議
        """)
    st.markdown("---")
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
    st.title("🔧 模組 1: 網站 AI 就緒度分析")
    st.markdown("分析網站的技術健康度與 AI 就緒度")
    with st.form("module1_form"):
        website_url = st.text_input("🌐 網站 URL", placeholder="例如: example.com 或 https://example.com", help="輸入要分析的網站 URL")
        product_category = st.text_input("🏷️ 產品品類 (可選)", placeholder="例如: 除濕機、冷氣、洗衣機、手機、筆電...", help="輸入要分析的產品品類，用於檢查產品權威性")
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    if submitted and website_url:
        with st.spinner("🔍 正在分析網站 AI 就緒度..."):
            try:
                result = run_website_analysis(website_url, product_category if product_category else None, gemini_api_key)
                if "error" in result:
                    st.error(f"分析失敗: {result['error']}")
                    return
                analysis_data = result.get("technical_seo_ai_readiness", {})
                st.success(f"✅ 分析完成: {website_url}")
                st.json(analysis_data)
            except Exception as e:
                st.error(f"分析過程中發生錯誤: {str(e)}")

def show_module2_page(gemini_api_key: Optional[str]):
    st.title("📊 模組 2: E-E-A-T 基準分析")
    st.markdown("動態 E-E-A-T 評估與競爭基準分析")
    with st.form("module2_form"):
        market = st.selectbox("🌏 市場", ["台灣", "全球"], index=0)
        product_category = st.text_input("🏷️ 產品品類", placeholder="如：半導體、家電、手機")
        brand = st.text_input("🏢 品牌名稱", placeholder="如：台積電、聯電")
        target_website = st.text_input("🎯 目標網站", placeholder="例如: example.com", help="輸入要分析的主要網站")
        competitors = st.text_area("🏆 競爭對手 (每行一個)", placeholder="competitor1.com\ncompetitor2.com\ncompetitor3.com", help="輸入競爭對手網站，每行一個")
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    if submitted and target_website:
        competitor_list = [comp.strip() for comp in competitors.split('\n') if comp.strip()] if competitors else []
        with st.spinner("🔍 正在執行 E-E-A-T 基準分析..."):
            try:
                result = run_eeat_benchmarking(
                    target_website,
                    competitor_list,
                    gemini_api_key,
                    market,
                    product_category,
                    brand
                )
                if "error" in result:
                    st.error(f"分析失敗: {result['error']}")
                    return
                analysis_data = result.get("eeat_benchmarking", {})
                st.success(f"✅ 分析完成: {target_website}")

                # UI 區塊化顯示
                if analysis_data:
                    st.markdown(f"**市場：** {analysis_data.get('market', '')}")
                    st.markdown(f"**產品品類：** {product_category}")
                    st.markdown(f"**品牌：** {brand}")

                    with st.expander("🏆 行業/市場/產品領導者推薦（LLM 推薦）", expanded=True):
                        leaders = analysis_data.get("leaders_recommendation", [])
                        if leaders:
                            st.table([{k: v for k, v in leader.items()} for leader in leaders])
                        else:
                            st.info("無領導者推薦資料")

                    with st.expander("📊 標竿差異分析（LLM 標竿比對）", expanded=False):
                        gap = analysis_data.get("brand_gap_analysis", {})
                        if gap:
                            st.write(f"差距分數：{gap.get('gap_score', 'N/A')}")
                            st.write(f"優勢：{', '.join(gap.get('advantages', []))}")
                            st.write(f"劣勢：{', '.join(gap.get('disadvantages', []))}")
                            st.write(f"建議：{', '.join(gap.get('recommendations', []))}")
                            st.caption(gap.get('summary', ''))
                        else:
                            st.info("無標竿比對資料")

                    with st.expander("🤖 AI 領導者分析", expanded=False):
                        ai_leader = analysis_data.get("ai_leader_analysis", {})
                        if ai_leader:
                            st.json(ai_leader)
                        else:
                            st.info("無 AI 領導者分析資料")

                    with st.expander("📰 動態媒體權重評估", expanded=False):
                        media = analysis_data.get("dynamic_media_weights", {})
                        if media:
                            st.metric("媒體覆蓋分數", media.get("media_coverage_score", 0))
                            st.metric("覆蓋率", f"{media.get('coverage_rate', 0)*100:.1f}%")
                            st.write(f"來源數量：{media.get('covered_count', 0)}/{media.get('total_count', 0)}")
                            for k, v in media.get("sources", {}).items():
                                st.write(f"**{k}**")
                                st.table(v)
                        else:
                            st.info("無媒體權重資料")

                    with st.expander("📰 真實媒體曝光紀錄", expanded=False):
                        real_media = analysis_data.get("real_media_mentions", {})
                        if real_media:
                            for k, v in real_media.items():
                                st.write(f"**{k}**")
                                if v:
                                    st.table(v)
                                else:
                                    st.info("無曝光紀錄")
                        else:
                            st.info("無媒體曝光資料")

                    with st.expander("🏆 競爭對手基準分析", expanded=False):
                        comp = analysis_data.get("competitor_benchmarking", {})
                        if comp:
                            st.write(f"市場地位：{comp.get('market_position', 'N/A')}")
                            st.write(f"競爭優勢：{', '.join(comp.get('competitive_advantages', []))}")
                            st.write(f"改善機會：{', '.join(comp.get('improvement_opportunities', []))}")
                            st.write("**詳細分析**")
                            st.table(comp.get("competitor_analysis", []))
                        else:
                            st.info("無競爭對手分析資料")

                    with st.expander("📈 趨勢追蹤與預測", expanded=False):
                        trend = analysis_data.get("trend_analysis", {})
                        if trend:
                            st.write("**當前趨勢**")
                            st.write(", ".join(trend.get("current_trends", [])))
                            st.write("**預測成長**")
                            st.json(trend.get("predicted_growth", {}))
                            st.write("**市場機會**")
                            st.write(", ".join(trend.get("market_opportunities", [])))
                            st.write("**風險因素**")
                            st.write(", ".join(trend.get("risk_factors", [])))
                        else:
                            st.info("無趨勢分析資料")

                    with st.expander("🎯 策略建議", expanded=True):
                        recs = analysis_data.get("strategic_recommendations", [])
                        if recs:
                            for rec in recs:
                                st.markdown(f"**策略：{rec.get('strategy', '')}**")
                                st.write(f"說明：{rec.get('description', '')}")
                                st.write(f"優先級：{rec.get('priority', '')}，時程：{rec.get('timeline', '')}")
                                st.write(f"預期影響：{rec.get('expected_impact', '')}")
                                st.write(f"步驟：{', '.join(rec.get('implementation_steps', []))}")
                                st.markdown("---")
                        else:
                            st.info("無策略建議")

                    with st.expander("📋 市場媒體與競爭對手清單", expanded=False):
                        st.write("**市場媒體清單**")
                        st.json(analysis_data.get("market_media", {}))
                        st.write("**市場競爭對手清單**")
                        st.json(analysis_data.get("market_competitors", []))

            except Exception as e:
                st.error(f"分析過程中發生錯誤: {str(e)}")

def show_full_eeat_page(gemini_api_key: Optional[str]):
    st.title("🎯 完整 E-E-A-T 分析")
    st.markdown("傳統 E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) 分析")
    with st.form("full_eeat_form"):
        website_url = st.text_input("🌐 網站 URL", placeholder="例如: example.com", help="輸入要分析的網站 URL")
        company_name = st.text_input("🏢 公司名稱", placeholder="例如: Example Corp", help="輸入公司或組織名稱")
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    if submitted and website_url and company_name:
        with st.spinner("🔍 正在執行完整 E-E-A-T 分析..."):
            try:
                config_data = {
                    "brand_name": company_name,
                    "related_entities": [company_name],
                    "media_weights": {
                        "industry_news": 0.3,
                        "mainstream_news": 0.4,
                        "social_media": 0.2,
                        "video_sites": 0.1
                    },
                    "official_info": f"Official information about {company_name}"
                }
                module1_output = {
                    "site_analysis": {
                        "uses_https": website_url.startswith('https://')
                    }
                }
                result = run_eeat_analysis(config_data, module1_output)
                if "error" in result:
                    st.error(f"分析失敗: {result['error']}")
                    return
                st.success(f"✅ 分析完成: {company_name} ({website_url})")
                st.json(result)
            except Exception as e:
                st.error(f"分析過程中發生錯誤: {str(e)}")

def show_module3_page(gemini_api_key: Optional[str]):
    st.title("🔍 模組 3: AI 資訊正確度檢查")
    st.markdown("深度比對 LLM 認知與權威原始資料，從精準詞組與廣泛語意兩個維度進行評分")
    
    with st.form("module3_form"):
        source_type = st.selectbox("📚 資料來源類型", ["url", "text", "pdf"], index=0)
        
        if source_type == "url":
            source_value = st.text_input("🌐 網址", placeholder="https://example.com", help="輸入要分析的網址")
        elif source_type == "text":
            source_value = st.text_area("📝 文字內容", placeholder="輸入要分析的文字內容...", help="輸入要分析的文字內容")
        else:  # pdf
            source_value = st.text_input("📄 PDF 網址", placeholder="https://example.com/document.pdf", help="輸入 PDF 檔案的網址")
        
        supplemental_info = st.text_area("📋 補充資訊 (可選)", placeholder="額外的補充資訊...", help="可選的補充資訊，會與主要資料合併")
        model_to_check = st.selectbox("🤖 目標 LLM 模型", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)
        
        submitted = st.form_submit_button("🚀 開始檢查", type="primary")
    
    if submitted and source_value:
        if not gemini_api_key:
            st.error("❌ 請先輸入 Gemini API 金鑰")
            return
            
        config_data = {
            "accuracy_source": {
                "type": source_type,
                "value": source_value
            },
            "supplemental_info": supplemental_info if supplemental_info else "",
            "model_to_check": model_to_check
        }
        
        with st.spinner("🔍 正在執行 AI 資訊正確度檢查..."):
            try:
                result = run_ai_accuracy_check(config_data, gemini_api_key)
                if "error" in result:
                    st.error(f"檢查失敗: {result['error']}")
                    return
                
                analysis_data = result.get("ai_accuracy_v2", {})
                st.success(f"✅ 檢查完成")
                
                # UI 區塊化顯示
                if analysis_data:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("整體分數", analysis_data.get("accuracy_scores", {}).get("overall_score", 0))
                    with col2:
                        st.metric("詞組比對分數", analysis_data.get("accuracy_scores", {}).get("phrase_matching_score", 0))
                    with col3:
                        st.metric("語意一致性分數", analysis_data.get("accuracy_scores", {}).get("semantic_consistency_score", 0))
                    
                    with st.expander("📊 詳細分析結果", expanded=True):
                        st.write(f"**資料來源類型：** {analysis_data.get('source_info', {}).get('type', '')}")
                        st.write(f"**資料來源：** {analysis_data.get('source_info', {}).get('value', '')}")
                        st.write(f"**資訊分類：** {analysis_data.get('source_info', {}).get('classification', '')}")
                        st.write(f"**目標模型：** {analysis_data.get('model_used', '')}")
                        
                        st.markdown("**語意評分理由：**")
                        st.info(analysis_data.get("semantic_score_reasoning", ""))
                        
                        mismatched = analysis_data.get("mismatched_phrases_analysis", [])
                        if mismatched:
                            st.markdown("**不匹配詞組分析：**")
                            st.table(mismatched)
                        else:
                            st.success("✅ 所有關鍵詞組都正確匹配")
                
            except Exception as e:
                st.error(f"檢查過程中發生錯誤: {str(e)}")

def show_reports_page():
    st.title("📈 分析報告")
    st.markdown("查看歷史分析結果與趨勢")
    st.info("📝 尚無分析報告，請先執行分析")

if __name__ == "__main__":
    main() 