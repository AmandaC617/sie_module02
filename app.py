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
                "🔍 模組 3: AI 資訊正確度檢查",
                "🎯 模組 4: 完整 E-E-A-T 分析",
                "📈 分析報告"
            ]
        )
        
        st.markdown("---")
        st.markdown("### 📋 使用說明")
        st.markdown("""
        1. **模組 1**: 分析網站技術健康度與 AI 就緒度
        2. **模組 2**: 動態 E-E-A-T 評估與競爭基準分析
        3. **模組 3**: AI 資訊正確度檢查與深度比對
        4. **模組 4**: 傳統 E-E-A-T 分析
        5. **報告**: 查看歷史分析結果
        """)
    
    # 主內容區域
    if page == "🏠 首頁":
        show_homepage()
    elif page == "🔧 模組 1: 網站 AI 就緒度分析":
        show_module1_page(gemini_api_key)
    elif page == "📊 模組 2: E-E-A-T 基準分析":
        show_module2_page(gemini_api_key)
    elif page == "🔍 模組 3: AI 資訊正確度檢查":
        show_module3_page(gemini_api_key)
    elif page == "🎯 模組 4: 完整 E-E-A-T 分析":
        show_full_eeat_page(gemini_api_key)
    elif page == "📈 分析報告":
        show_reports_page()

def show_homepage():
    """顯示首頁"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🚀 SIE 平台")
    st.markdown("### 智能搜尋引擎優化分析系統")
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
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 🔍 模組 3: AI 資訊正確度檢查")
        st.markdown("""
        - 📚 權威資料來源整合
        - 🎯 精準詞組比對分析
        - 🧠 語意一致性評估
        - 📊 深度不匹配分析
        - 🔄 快取機制優化
        - 💡 改進建議生成
        - 📈 多維度評分系統
        - 🎯 事實基礎驗證
        """)
    
    with col4:
        st.markdown("### 🎯 模組 4: 完整 E-E-A-T 分析")
        st.markdown("""
        - 📚 Experience 經驗評估
        - 🎓 Expertise 專業度分析
        - 🏆 Authoritativeness 權威性檢查
        - ✅ Trustworthiness 可信度驗證
        - 📊 綜合評分系統
        - 🎯 改進建議
        - 📈 歷史趨勢追蹤
        - 🔍 詳細分析報告
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
        
        product_category = st.text_input(
            "🏷️ 產品品類 (可選)",
            placeholder="例如: 除濕機、冷氣、洗衣機、手機、筆電...",
            help="輸入要分析的產品品類，用於檢查產品權威性"
        )
        
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    
    if submitted and website_url:
        with st.spinner("🔍 正在分析網站 AI 就緒度..."):
            try:
                # 執行分析
                result = run_website_analysis(website_url, product_category if product_category else None, gemini_api_key)
                
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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📁 根檔案", "🏗️ 架構", "🤖 LLM 友善度", "🏆 產品權威", "❓ FAQ 分析", "💡 建議"])
    
    with tab1:
        display_root_files_analysis(analysis_data.get("root_files", {}))
    
    with tab2:
        display_architecture_analysis(analysis_data.get("architecture_signals", {}))
    
    with tab3:
        display_llm_friendliness_analysis(analysis_data.get("llm_friendliness", {}))
    
    with tab4:
        display_product_authority_analysis(analysis_data.get("product_authority", {}))
    
    with tab5:
        display_faq_analysis(analysis_data.get("faq_analysis", {}))
    
    with tab6:
        display_recommendations(analysis_data.get("actionable_recommendations", []))
        display_seo_llm_recommendations(analysis_data.get("seo_llm_recommendations", []))

def show_module2_page(gemini_api_key: Optional[str]):
    """顯示模組 2 頁面"""
    st.title("📊 模組 2: E-E-A-T 基準分析")
    st.markdown("動態 E-E-A-T 評估與競爭基準分析")
    
    # 輸入區域
    with st.form("module2_form"):
        target_website = st.text_input(
            "🎯 目標網站",
            placeholder="例如: example.com",
            help="輸入要分析的主要網站"
        )
        
        competitors = st.text_area(
            "🏆 競爭對手 (每行一個)",
            placeholder="competitor1.com\ncompetitor2.com\ncompetitor3.com",
            help="輸入競爭對手網站，每行一個"
        )
        
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    
    if submitted and target_website:
        # 處理競爭對手列表
        competitor_list = []
        if competitors:
            competitor_list = [comp.strip() for comp in competitors.split('\n') if comp.strip()]
        
        with st.spinner("🔍 正在執行 E-E-A-T 基準分析..."):
            try:
                # 執行分析
                result = run_eeat_benchmarking(target_website, competitor_list, gemini_api_key)
                
                if "error" in result:
                    st.error(f"分析失敗: {result['error']}")
                    return
                
                analysis_data = result.get("eeat_benchmarking", {})
                
                # 顯示分析結果
                display_module2_results(analysis_data, target_website)
                
                # 儲存結果
                save_analysis_result("module2", target_website, result)
                
            except Exception as e:
                st.error(f"分析過程中發生錯誤: {str(e)}")

def display_module2_results(analysis_data: Dict, target_website: str):
    """顯示模組 2 分析結果"""
    st.success(f"✅ 分析完成: {target_website}")
    
    # 總體評分
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ai_leader = analysis_data.get("ai_leader_analysis", {})
        ai_score = ai_leader.get("ai_leader_score", 0)
        st.metric("AI 領導者分數", f"{ai_score}/100", "🤖")
    
    with col2:
        media_weights = analysis_data.get("dynamic_media_weights", {})
        media_score = media_weights.get("media_mentions", {}).get("media_coverage_score", 0)
        st.metric("媒體覆蓋分數", f"{media_score:.1f}/100", "📰")
    
    with col3:
        social_score = media_weights.get("social_media_presence", {}).get("social_authority_score", 0)
        st.metric("社交媒體權威", f"{social_score:.1f}/100", "📱")
    
    with col4:
        competitor_bench = analysis_data.get("competitor_benchmarking", {})
        market_position = competitor_bench.get("market_position", "unknown")
        st.metric("市場地位", market_position.title(), "🏆")
    
    st.markdown("---")
    
    # 詳細分析結果
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 AI 領導者", "📊 媒體權重", "🏆 競爭分析", "📈 趨勢", "💡 策略"])
    
    with tab1:
        display_ai_leader_analysis(analysis_data.get("ai_leader_analysis", {}))
    
    with tab2:
        display_media_weights_analysis(analysis_data.get("dynamic_media_weights", {}))
    
    with tab3:
        display_competitor_analysis(analysis_data.get("competitor_benchmarking", {}))
    
    with tab4:
        display_trend_analysis(analysis_data.get("trend_analysis", {}))
    
    with tab5:
        display_strategic_recommendations(analysis_data.get("strategic_recommendations", []))

def show_module3_page(gemini_api_key: Optional[str]):
    """顯示模組 3 頁面"""
    st.title("🔍 模組 3: AI 資訊正確度檢查")
    st.markdown("深度比對 LLM 認知與權威原始資料")
    
    # 輸入區域
    with st.form("module3_form"):
        # 資料來源設定
        st.subheader("📚 權威資料來源")
        source_type = st.selectbox(
            "來源類型",
            ["url", "pdf", "text"],
            help="選擇權威資料的來源類型"
        )
        
        source_value = st.text_input(
            "來源值",
            placeholder="URL、PDF 連結或直接輸入文字",
            help="輸入權威資料的來源"
        )
        
        # 補充資訊
        supplemental_info = st.text_area(
            "補充資訊 (可選)",
            placeholder="額外的權威資訊或背景資料",
            help="提供額外的權威資訊來增強事實基礎"
        )
        
        # 目標 LLM 模型
        target_model = st.selectbox(
            "目標 LLM 模型",
            ["gemini-1.5-flash", "gemini-1.5-pro"],
            help="選擇要檢查的目標 LLM 模型"
        )
        
        submitted = st.form_submit_button("🚀 開始檢查", type="primary")
    
    if submitted and source_value:
        if not gemini_api_key:
            st.error("❌ 請先輸入 Gemini API 金鑰")
            return
            
        with st.spinner("🔍 正在進行 AI 資訊正確度檢查..."):
            try:
                # 創建配置數據
                config_data = {
                    "accuracy_source": {
                        "type": source_type,
                        "value": source_value
                    },
                    "supplemental_info": supplemental_info
                }
                
                # 執行檢查
                result = run_ai_accuracy_check(config_data, gemini_api_key)
                
                if "error" in result:
                    st.error(f"檢查失敗: {result['error']}")
                    return
                
                # 提取實際的檢查結果
                if "ai_accuracy_v2" in result:
                    actual_result = result["ai_accuracy_v2"]
                    # 轉換為前端期望的格式
                    display_result = {
                        "phrase_matching_score": actual_result.get("accuracy_scores", {}).get("phrase_matching_score", 0),
                        "semantic_consistency_score": actual_result.get("accuracy_scores", {}).get("semantic_consistency_score", 0),
                        "overall_accuracy_score": actual_result.get("accuracy_scores", {}).get("overall_score", 0),
                        "information_classification": actual_result.get("source_info", {}).get("classification", "未知"),
                        "llm_response": actual_result.get("llm_response", ""),
                        "phrase_matching_details": actual_result.get("phrase_matching_details", {
                            "total_phrases": 0,
                            "found_phrases": [],
                            "missing_phrases": []
                        }),
                        "mismatch_analysis": actual_result.get("mismatched_phrases_analysis", []),
                        "semantic_consistency_details": {
                            "reasoning": actual_result.get("semantic_score_reasoning", "")
                        },
                        "recommendations": []
                    }
                else:
                    display_result = result
                
                # 顯示檢查結果
                display_module3_results(display_result, source_value, target_model)
                
                # 儲存結果
                save_analysis_result("module3", source_value, result)
                
            except Exception as e:
                st.error(f"檢查過程中發生錯誤: {str(e)}")

def display_module3_results(result: Dict, source_value: str, target_model: str):
    """顯示模組 3 檢查結果"""
    st.success(f"✅ 檢查完成: {source_value}")
    
    # 總體評分
    col1, col2, col3 = st.columns(3)
    
    with col1:
        phrase_score = result.get("phrase_matching_score", 0)
        st.metric("精準詞組比對", f"{phrase_score}/100", "🎯")
    
    with col2:
        semantic_score = result.get("semantic_consistency_score", 0)
        st.metric("語意一致性", f"{semantic_score}/100", "🧠")
    
    with col3:
        overall_score = result.get("overall_accuracy_score", 0)
        st.metric("整體正確度", f"{overall_score}/100", "📊")
    
    st.markdown("---")
    
    # 詳細分析結果
    tab1, tab2, tab3, tab4 = st.tabs(["📝 比對詳情", "🔍 不匹配分析", "📊 評分細項", "💡 建議"])
    
    with tab1:
        st.subheader("📝 比對詳情")
        
        # 資訊分類
        info_classification = result.get("information_classification", "未知")
        st.info(f"**資訊分類**: {info_classification}")
        
        # LLM 回答
        llm_response = result.get("llm_response", "")
        st.text_area("LLM 回答", llm_response, height=150, disabled=True)
        
        # 關鍵詞組比對
        phrase_matching = result.get("phrase_matching_details", {})
        if phrase_matching:
            st.subheader("關鍵詞組比對")
            found_phrases = phrase_matching.get("found_phrases", [])
            missing_phrases = phrase_matching.get("missing_phrases", [])
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"✅ 找到的詞組 ({len(found_phrases)}):")
                for phrase in found_phrases[:10]:  # 只顯示前10個
                    st.write(f"• {phrase}")
                if len(found_phrases) > 10:
                    st.write(f"... 還有 {len(found_phrases) - 10} 個")
            
            with col2:
                st.error(f"❌ 缺失的詞組 ({len(missing_phrases)}):")
                for phrase in missing_phrases[:10]:  # 只顯示前10個
                    st.write(f"• {phrase}")
                if len(missing_phrases) > 10:
                    st.write(f"... 還有 {len(missing_phrases) - 10} 個")
    
    with tab2:
        st.subheader("🔍 不匹配分析")
        
        mismatch_analysis = result.get("mismatch_analysis", [])
        if mismatch_analysis:
            for i, analysis in enumerate(mismatch_analysis):
                with st.expander(f"不匹配 #{i+1}: {analysis.get('phrase', 'N/A')}"):
                    st.write(f"**類型**: {analysis.get('type', 'N/A')}")
                    st.write(f"**嚴重程度**: {analysis.get('severity', 'N/A')}")
                    st.write(f"**分析**: {analysis.get('analysis', 'N/A')}")
        else:
            st.info("沒有發現不匹配項目")
    
    with tab3:
        st.subheader("📊 評分細項")
        
        # 精準詞組比對詳情
        phrase_details = result.get("phrase_matching_details", {})
        if phrase_details:
            total_phrases = phrase_details.get("total_phrases", 0)
            found_phrases = phrase_details.get("found_phrases", [])
            st.metric("總關鍵詞組", total_phrases)
            st.metric("找到詞組", len(found_phrases))
            st.metric("準確率", f"{(len(found_phrases) / total_phrases * 100):.1f}%" if total_phrases > 0 else "0%")
        
        # 語意一致性詳情
        semantic_details = result.get("semantic_consistency_details", {})
        if semantic_details:
            st.write("**語意一致性分析**:")
            st.write(f"• 主題一致性: {semantic_details.get('topic_consistency', 'N/A')}")
            st.write(f"• 事實準確性: {semantic_details.get('factual_accuracy', 'N/A')}")
            st.write(f"• 邏輯連貫性: {semantic_details.get('logical_coherence', 'N/A')}")
    
    with tab4:
        st.subheader("💡 建議")
        
        recommendations = result.get("recommendations", [])
        if recommendations:
            for i, rec in enumerate(recommendations):
                st.write(f"{i+1}. **{rec.get('category', 'N/A')}**: {rec.get('suggestion', 'N/A')}")
        else:
            st.info("沒有特定建議")

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
                # 創建配置數據
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
                
                # 模擬模組1輸出
                module1_output = {
                    "site_analysis": {
                        "uses_https": website_url.startswith('https://')
                    }
                }
                
                result = run_eeat_analysis(config_data, module1_output)
                
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

def display_product_authority_analysis(product_authority: Dict):
    """顯示產品權威性分析"""
    st.subheader("🏆 產品權威性分析")
    
    if not product_authority:
        st.info("沒有產品權威性分析數據")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("產品頁面數量", product_authority.get("product_pages_found", 0))
        st.metric("權威分數", f"{product_authority.get('authority_score', 0)}/100")
    
    with col2:
        completeness = product_authority.get("product_info_completeness", "unknown")
        completeness_icon = {
            "excellent": "🟢",
            "good": "🟡",
            "fair": "🟠",
            "poor": "🔴"
        }.get(completeness, "⚪")
        st.metric("資訊完整性", f"{completeness_icon} {completeness}")
    
    # 詳細檢查項目
    st.markdown("### 📋 詳細檢查項目")
    
    checks = [
        ("技術規格", product_authority.get("technical_specs_available", False)),
        ("比較功能", product_authority.get("comparison_features", False)),
        ("專家內容", product_authority.get("expert_content", False))
    ]
    
    for check_name, check_result in checks:
        if check_result:
            st.success(f"✅ {check_name}")
        else:
            st.error(f"❌ {check_name}")

def display_faq_analysis(faq_analysis: Dict):
    """顯示 FAQ 分析"""
    st.subheader("❓ FAQ 與消費者問題分析")
    
    if not faq_analysis:
        st.info("沒有 FAQ 分析數據")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("FAQ 數量", faq_analysis.get("faq_count", 0))
        st.metric("FAQ 區塊", "✅ 已找到" if faq_analysis.get("faq_section_found", False) else "❌ 未找到")
    
    with col2:
        qa_quality = faq_analysis.get("qa_content_quality", "unknown")
        qa_icon = {
            "excellent": "🟢",
            "good": "🟡",
            "fair": "🟠",
            "poor": "🔴"
        }.get(qa_quality, "⚪")
        st.metric("QA 品質", f"{qa_icon} {qa_quality}")
        st.metric("QA 分數", f"{faq_analysis.get('qa_score', 0)}/100")
    
    # 詳細檢查項目
    st.markdown("### 📋 詳細檢查項目")
    
    checks = [
        ("產品特定問題", faq_analysis.get("product_specific_qa", False)),
        ("常見問題覆蓋", faq_analysis.get("common_questions_covered", False))
    ]
    
    for check_name, check_result in checks:
        if check_result:
            st.success(f"✅ {check_name}")
        else:
            st.error(f"❌ {check_name}")

def display_seo_llm_recommendations(seo_llm_recommendations: List[Dict]):
    """顯示 SEO 與 LLM 友善度建議"""
    st.subheader("🎯 SEO 與 LLM 友善度改善建議")
    
    if not seo_llm_recommendations:
        st.info("沒有 SEO 與 LLM 友善度建議")
        return
    
    for category in seo_llm_recommendations:
        with st.expander(f"📂 {category.get('category', 'General')}"):
            recommendations = category.get('recommendations', [])
            for rec in recommendations:
                st.markdown(f"• {rec}")

def display_ai_leader_analysis(ai_leader: Dict):
    """顯示 AI 領導者分析"""
    st.subheader("🤖 AI 領導者分析")
    
    # AI 領導者分數
    ai_score = ai_leader.get("ai_leader_score", 0)
    st.metric("AI 領導者分數", f"{ai_score}/100")
    
    # AI 技術指標
    tech_indicators = ai_leader.get("ai_technology_indicators", [])
    if tech_indicators:
        st.success(f"✅ 發現 AI 技術指標: {', '.join(tech_indicators)}")
    else:
        st.warning("⚠️ 未發現 AI 技術指標")
    
    # AI 內容信號
    content_signals = ai_leader.get("ai_content_signals", [])
    if content_signals:
        st.success(f"✅ 發現 AI 內容信號: {', '.join(content_signals)}")
    else:
        st.info("ℹ️ 未發現 AI 相關內容")
    
    # AI 領導地位
    position = ai_leader.get("ai_leadership_position", "unknown")
    position_emoji = {
        "leader": "🏆",
        "emerging": "📈",
        "follower": "📊",
        "laggard": "⚠️"
    }.get(position, "❓")
    
    st.markdown(f"**AI 領導地位**: {position_emoji} {position.title()}")

def display_media_weights_analysis(media_weights: Dict):
    """顯示媒體權重分析"""
    st.subheader("📊 媒體權重分析")
    
    # 媒體提及
    mentions = media_weights.get("media_mentions", {})
    media_score = mentions.get("media_coverage_score", 0)
    st.metric("媒體覆蓋分數", f"{media_score:.1f}/100")
    
    recent_mentions = mentions.get("recent_mentions", [])
    if recent_mentions:
        st.markdown("### 📰 最近媒體提及")
        for mention in recent_mentions:
            sentiment_emoji = "✅" if mention.get("sentiment") == "positive" else "⚠️"
            st.markdown(f"""
            {sentiment_emoji} **{mention.get('source', 'Unknown')}** - {mention.get('date', 'Unknown')}
            {mention.get('title', 'No title')}
            """)
    
    # 社交媒體
    social = media_weights.get("social_media_presence", {})
    social_score = social.get("social_authority_score", 0)
    st.metric("社交媒體權威分數", f"{social_score:.1f}/100")
    
    platforms = social.get("platforms", [])
    if platforms:
        st.success(f"✅ 發現社交媒體平台: {', '.join(platforms)}")
    else:
        st.warning("⚠️ 未發現社交媒體連結")

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