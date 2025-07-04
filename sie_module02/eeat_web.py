import streamlit as st
import json
import datetime
from eeat_module import run_module_2

st.set_page_config(page_title="E-E-A-T 分析互動網頁", layout="centered")
st.title("🔎 E-E-A-T 分析互動網頁版")
st.markdown("""
本工具可即時分析品牌網站的 E-E-A-T（經驗、專業、權威、信任）分數。\
請輸入下列資訊並點擊「分析」！
""")

with st.form("eeat_form"):
    brand_name = st.text_input("品牌名稱", "台灣品牌A")
    related_entities = st.text_area("相關實體（每行一個）", "產品B\n集團C").splitlines()
    official_info = st.text_area("官方資訊", "台灣品牌A是台灣領先的科技公司，主力產品為產品B。")
    st.markdown("**媒體權重設定**（數字越大代表越重要）")
    col1, col2, col3 = st.columns(3)
    with col1:
        industry_news = st.number_input("產業新聞", min_value=0, max_value=20, value=10)
        mainstream_news = st.number_input("主流新聞", min_value=0, max_value=20, value=8)
    with col2:
        social_media = st.number_input("社群媒體", min_value=0, max_value=20, value=5)
        video_sites = st.number_input("影音網站", min_value=0, max_value=20, value=5)
    with col3:
        ecommerce_retail = st.number_input("電商零售", min_value=0, max_value=20, value=2)
    uses_https = st.checkbox("網站是否支援 HTTPS？", value=True)
    submitted = st.form_submit_button("分析")

if submitted:
    config_data = {
        "brand_name": brand_name,
        "related_entities": [e for e in related_entities if e.strip()],
        "media_weights": {
            "industry_news": industry_news,
            "mainstream_news": mainstream_news,
            "social_media": social_media,
            "video_sites": video_sites,
            "ecommerce_retail": ecommerce_retail
        },
        "official_info": official_info
    }
    module1_output = {"site_analysis": {"uses_https": uses_https}}
    with st.spinner("分析中，請稍候..."):
        result = run_module_2(config_data, module1_output)
    st.success("分析完成！")
    st.subheader("E-E-A-T 分數")
    st.json(result["eeat_scores"])
    with st.expander("詳細分析結果（點擊展開）"):
        st.json(result)
    st.markdown("---")
    st.caption("本工具由 Streamlit 製作，程式碼已開源於 GitHub。") 