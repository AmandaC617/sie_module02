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
        target_website = st.text_input("🎯 目標網站", placeholder="例如: example.com", help="輸入要分析的主要網站")
        competitors = st.text_area("🏆 競爭對手 (每行一個)", placeholder="competitor1.com\ncompetitor2.com\ncompetitor3.com", help="輸入競爭對手網站，每行一個")
        submitted = st.form_submit_button("🚀 開始分析", type="primary")
    if submitted and target_website:
        competitor_list = [comp.strip() for comp in competitors.split('\n') if comp.strip()] if competitors else []
        with st.spinner("🔍 正在執行 E-E-A-T 基準分析..."):
            try:
                result = run_eeat_benchmarking(target_website, competitor_list, gemini_api_key)
                if "error" in result:
                    st.error(f"分析失敗: {result['error']}")
                    return
                analysis_data = result.get("eeat_benchmarking", {})
                st.success(f"✅ 分析完成: {target_website}")
                st.json(analysis_data)
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

def show_reports_page():
    st.title("📈 分析報告")
    st.markdown("查看歷史分析結果與趨勢")
    st.info("📝 尚無分析報告，請先執行分析")

if __name__ == "__main__":
    main() 