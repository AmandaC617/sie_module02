import streamlit as st
import json
import datetime
import random
import time
from dateutil import parser as date_parser

try:
    import wikipediaapi
except ImportError:
    print("警告: 'wikipedia-api' 函式庫未安裝。維基百科檢查功能將無法運作。")
    print("請執行: pip install wikipedia-api")
    wikipediaapi = None

def mock_google_custom_search(query: str, media_type: str) -> dict:
    """模擬 Google Custom Search JSON API 的回應。"""
    time.sleep(0.1) # 模擬網路延遲
    
    results = {
        "industry_news": [
            {
                "title": f"{query} 發布革命性核心產品B，引領產業新標準",
                "link": f"https://news.example-industry.com/{query.lower()}-product-b-launch",
                "snippet": f"台灣領先品牌 {query} 今日宣布推出其劃時代的核心產品B，該產品採用最新AI晶片，效能提升200%。",
                "pagemap": {"metatags": [{"article:published_time": "2025-07-01T10:00:00Z"}]}
            },
            {
                "title": f"專家分析：{query} 的市場策略如何顛覆現狀",
                "link": f"https://analysis.example-industry.com/{query.lower()}-strategy",
                "snippet": f"產業分析師指出，{query} 近期的多角化經營策略，特別是在綠色能源領域的投入，展現其強大企圖心。",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-15T14:30:00Z"}]}
            }
        ],
        "mainstream_news": [
            {
                "title": f"{query} 連續三年榮獲最佳雇主獎",
                "link": f"https://mainstream.example.com/{query.lower()}-best-employer-2025",
                "snippet": f"知名人力資源顧問公司公布年度最佳雇主，{query} 因其優異的員工福利與企業文化再次上榜。",
                "pagemap": {"metatags": [{"article:published_time": "2025-05-20T11:00:00Z"}]}
            },
            {
                "title": f"{query} 股價今日小幅波動",
                "link": f"https://finance.example.com/{query.lower()}-stock-today",
                "snippet": f"受到國際市場影響，{query} 股價今日收盤時下跌 0.5%，市場普遍認為屬於正常技術性回檔。",
                "pagemap": {"metatags": [{"article:published_time": "2025-07-02T08:00:00Z"}]}
            }
        ],
        "social_media": [
            {
                "title": f"Dcard 網友熱議 {query} 的新功能，CP值超高！",
                "link": f"https://dcard.tw/f/tech/p/123456789",
                "snippet": f"最近剛入手{query}的核心產品B，真心覺得不錯，操作很順暢，而且外型也好看，不知道大家覺得如何？ #開箱 #{query}",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-28T22:15:00Z"}]}
            }
        ],
        "video_sites": [
            {
                "title": f"【知名 YouTuber】{query} 核心產品B 深度開箱！真的值得買嗎？",
                "link": f"https://youtube.com/watch?v=abcdef123",
                "snippet": f"這次我們搶先拿到了 {query} 的年度旗艦產品B，從外觀設計到內部效能，進行一個全面的實測！",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-20T20:00:00Z"}]}
            }
        ],
        "ecommerce_retail": []
    }
    
    if random.random() > 0.8 and media_type not in ["industry_news", "mainstream_news"]:
        return {"items": []}
        
    return {"items": results.get(media_type, [])}

def mock_gemini_api(snippet: str, official_info: str) -> str:
    """模擬 Gemini API 進行內容正確性比對。"""
    time.sleep(0.05)
    
    negative_keywords = ["過熱", "災情", "下跌", "電池續航力沒有想像中好"]
    if any(keyword in snippet for keyword in negative_keywords):
        return "Uncertain"
    
    positive_keywords = ["革命性", "新功能", "最佳雇主", "CP值超高"]
    if any(keyword in snippet for keyword in positive_keywords):
        return "Correct"
        
    return "Correct"

def check_wikipedia_presence(entities: list, user_agent: str) -> dict:
    """使用 Wikipedia API 檢查品牌和相關實體是否被維基百科收錄。"""
    if not wikipediaapi:
        return {"brand_found": False, "related_entities_found": []}

    wiki_client = wikipediaapi.Wikipedia(language='zh-tw', user_agent=user_agent)
    presence = {"brand_found": False, "related_entities_found": []}
    
    brand_name = entities[0]
    page_brand = wiki_client.page(brand_name)
    if page_brand.exists():
        presence["brand_found"] = True

    for entity in entities[1:]:
        page_entity = wiki_client.page(entity)
        if page_entity.exists():
            presence["related_entities_found"].append(entity)
            
    return presence

def analyze_media_mentions(brand_name: str, related_entities: list, media_weights: dict, official_info: str) -> dict:
    """遍歷各媒體類型，分析媒體提及並進行正確性檢查。"""
    all_mentions = {}
    search_entities = [brand_name] + related_entities

    for media_type in media_weights.keys():
        all_mentions[media_type] = []
        for entity in search_entities:
            response = mock_google_custom_search(entity, media_type)
            
            if "items" in response:
                for item in response["items"]:
                    try:
                        date_str = item.get("pagemap", {}).get("metatags", [{}])[0].get("article:published_time", "")
                        parsed_date = date_parser.parse(date_str).date()
                    except (ValueError, TypeError):
                        parsed_date = datetime.date(1970, 1, 1)

                    accuracy = mock_gemini_api(item.get("snippet", ""), official_info)

                    all_mentions[media_type].append({
                        "title": item.get("title", "無標題"),
                        "url": item.get("link", "#"),
                        "date_obj": parsed_date,
                        "date": parsed_date.isoformat() if parsed_date != datetime.date(1970, 1, 1) else "N/A",
                        "accuracy_check": accuracy,
                        "snippet": item.get("snippet", "")
                    })

    mentions_by_type = []
    total_mentions = 0
    for media_type, mentions in all_mentions.items():
        if not mentions:
            mentions_by_type.append({
                "type": media_type,
                "count": 0,
                "weight": media_weights[media_type],
                "latest_mention": None
            })
            continue

        mentions.sort(key=lambda x: x["date_obj"], reverse=True)
        
        count = len(mentions)
        total_mentions += count
        latest = mentions[0]
        
        mentions_by_type.append({
            "type": media_type,
            "count": count,
            "weight": media_weights[media_type],
            "latest_mention": {
                "title": latest["title"],
                "url": latest["url"],
                "date": latest["date"],
                "accuracy_check": latest["accuracy_check"]
            }
        })

    return {
        "total_mentions": total_mentions,
        "mentions_by_type": mentions_by_type,
        "raw_mentions": all_mentions
    }

def calculate_eeat_scores(media_analysis: dict, wiki_presence: dict, uses_https: bool) -> dict:
    """根據媒體分析、維基百科收錄和 HTTPS 使用情況計算 E-E-A-T 分數。"""
    scores = {
        "experience": 0, "expertise": 0, "authoritativeness": 0, "trustworthiness": 0
    }
    
    # 1. Authoritativeness (權威性)
    auth_score = 0
    for item in media_analysis["mentions_by_type"]:
        auth_score += item["count"] * item["weight"]
    if wiki_presence["brand_found"]:
        auth_score += 20
    auth_score += len(wiki_presence["related_entities_found"]) * 10
    scores["authoritativeness"] = min(100, int(auth_score))

    # 2. Expertise (專業性)
    industry_mentions = media_analysis["raw_mentions"].get("industry_news", [])
    scores["expertise"] = min(100, len(industry_mentions) * 5)

    # 3. Experience (經驗)
    social_mentions = media_analysis["raw_mentions"].get("social_media", [])
    video_mentions = media_analysis["raw_mentions"].get("video_sites", [])
    experience_mentions = social_mentions + video_mentions
    scores["experience"] = min(100, len(experience_mentions) * 2)

    # 4. Trustworthiness (信任度)
    trust_score = 0
    if uses_https:
        trust_score += 40
    mainstream_mentions = media_analysis["raw_mentions"].get("mainstream_news", [])
    if mainstream_mentions:
        positive_or_neutral_count = sum(1 for m in mainstream_mentions if m["accuracy_check"] == "Correct")
        negative_count = len(mainstream_mentions) - positive_or_neutral_count
        
        trust_score += positive_or_neutral_count * 5
        trust_score -= negative_count * 15
    
    scores["trustworthiness"] = max(0, min(100, int(trust_score)))
    
    # 5. Overall Score (總分)
    overall = sum(scores.values()) / len(scores)
    scores["overall_score"] = int(overall)
    
    return scores

def run_eeat_analysis(config_data: dict, module1_output: dict):
    """執行 E-E-A-T 分析的主函式。"""
    brand_name = config_data["brand_name"]
    related_entities = config_data["related_entities"]
    media_weights = config_data["media_weights"]
    official_info = config_data["official_info"]
    user_agent = "SIE-Diagnostic-Tool/1.0 (contact@example.com)"
    
    uses_https = module1_output.get("site_analysis", {}).get("uses_https", False)

    # 步驟 1: 檢查維基百科收錄
    wiki_presence = check_wikipedia_presence([brand_name] + related_entities, user_agent)
    
    # 步驟 2: 分析媒體提及
    media_analysis = analyze_media_mentions(brand_name, related_entities, media_weights, official_info)
    
    # 步驟 3: 計算 E-E-A-T 分數
    eeat_scores = calculate_eeat_scores(media_analysis, wiki_presence, uses_https)
    
    # 步驟 4: 組合最終的 JSON 輸出
    result = {
        "eeat_scores": eeat_scores,
        "media_analysis": media_analysis,
        "wiki_presence": wiki_presence,
        "uses_https": uses_https
    }
    
    return result

# Streamlit 應用程式
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
        result = run_eeat_analysis(config_data, module1_output)
    
    st.success("分析完成！")
    
    # 顯示 E-E-A-T 分數
    st.subheader("🎯 E-E-A-T 分數")
    scores = result["eeat_scores"]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("經驗 (Experience)", f"{scores['experience']}/100")
    with col2:
        st.metric("專業 (Expertise)", f"{scores['expertise']}/100")
    with col3:
        st.metric("權威 (Authoritativeness)", f"{scores['authoritativeness']}/100")
    with col4:
        st.metric("信任 (Trustworthiness)", f"{scores['trustworthiness']}/100")
    with col5:
        st.metric("總分 (Overall)", f"{scores['overall_score']}/100")
    
    # 顯示詳細分析結果
    with st.expander("📊 詳細分析結果（點擊展開）"):
        st.json(result)
    
    st.markdown("---")
    st.caption("本工具由 Streamlit 製作，程式碼已開源於 GitHub。") 