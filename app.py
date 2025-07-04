import streamlit as st
import json
import datetime
import random
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dateutil import parser as date_parser

try:
    import wikipediaapi
except ImportError:
    print("警告: 'wikipedia-api' 函式庫未安裝。維基百科檢查功能將無法運作。")
    print("請執行: pip install wikipedia-api")
    wikipediaapi = None

# 頁面設定
st.set_page_config(
    page_title="E-E-A-T 分析工具",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS
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
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .score-high { color: #28a745; }
    .score-medium { color: #ffc107; }
    .score-low { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

def mock_google_custom_search(query: str, media_type: str) -> dict:
    """模擬 Google Custom Search JSON API 的回應。"""
    time.sleep(0.1)
    
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
            },
            {
                "title": f"{query} 榮獲年度最佳創新企業獎",
                "link": f"https://awards.example-industry.com/{query.lower()}-innovation-2025",
                "snippet": f"在年度產業評選中，{query} 憑藉其創新的技術研發和市場表現，榮獲最佳創新企業獎項。",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-20T09:00:00Z"}]}
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
            },
            {
                "title": f"消費者報告：{query} 客戶服務滿意度調查",
                "link": f"https://consumer.example.com/{query.lower()}-service-review",
                "snippet": f"一份最新的報告顯示，約有 5% 的使用者回報核心產品B在特定情況下有過熱問題，{query}官方已回應將提供軟體更新。",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-10T18:00:00Z"}]}
            },
            {
                "title": f"{query} 宣布擴大投資研發中心",
                "link": f"https://business.example.com/{query.lower()}-rd-investment",
                "snippet": f"{query} 今日宣布將投資 50 億元擴建研發中心，預計將創造 500 個就業機會。",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-25T14:00:00Z"}]}
            }
        ],
        "social_media": [
            {
                "title": f"Dcard 網友熱議 {query} 的新功能，CP值超高！",
                "link": f"https://dcard.tw/f/tech/p/123456789",
                "snippet": f"最近剛入手{query}的核心產品B，真心覺得不錯，操作很順暢，而且外型也好看，不知道大家覺得如何？ #開箱 #{query}",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-28T22:15:00Z"}]}
            },
            {
                "title": f"PTT MobileComm版 - {query} 產品B災情回報？",
                "link": f"https://www.ptt.cc/bbs/MobileComm/M.1234567890.A.ABC.html",
                "snippet": f"我的{query}產品B用了一週，感覺電池續航力沒有想像中好，有人也一樣嗎？還是我拿到機王了...",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-25T13:00:00Z"}]}
            },
            {
                "title": f"Facebook 網友分享 {query} 使用心得",
                "link": f"https://facebook.com/groups/tech/posts/123456789",
                "snippet": f"用了{query}的產品三個月，整體來說很滿意，客服也很專業，推薦給大家！",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-30T10:30:00Z"}]}
            }
        ],
        "video_sites": [
            {
                "title": f"【知名 YouTuber】{query} 核心產品B 深度開箱！真的值得買嗎？",
                "link": f"https://youtube.com/watch?v=abcdef123",
                "snippet": f"這次我們搶先拿到了 {query} 的年度旗艦產品B，從外觀設計到內部效能，進行一個全面的實測！",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-20T20:00:00Z"}]}
            },
            {
                "title": f"【科技頻道】{query} 產品評測：性價比之王？",
                "link": f"https://youtube.com/watch?v=defghi456",
                "snippet": f"深入分析 {query} 最新產品的優缺點，看看是否真的值得入手！",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-22T15:00:00Z"}]}
            }
        ],
        "ecommerce_retail": [
            {
                "title": f"PChome {query} 產品熱銷中",
                "link": f"https://pchome.com.tw/prod/123456",
                "snippet": f"{query} 產品在 PChome 24h 購物熱銷，網友評價平均 4.5 顆星。",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-15T12:00:00Z"}]}
            }
        ]
    }
    
    if random.random() > 0.8 and media_type not in ["industry_news", "mainstream_news"]:
        return {"items": []}
        
    return {"items": results.get(media_type, [])}

def mock_gemini_api(snippet: str, official_info: str) -> str:
    """模擬 Gemini API 進行內容正確性比對。"""
    time.sleep(0.05)
    
    negative_keywords = ["過熱", "災情", "下跌", "電池續航力沒有想像中好", "問題", "故障"]
    if any(keyword in snippet for keyword in negative_keywords):
        return "Uncertain"
    
    positive_keywords = ["革命性", "新功能", "最佳雇主", "CP值超高", "滿意", "推薦", "優秀"]
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

def generate_recommendations(scores: dict, media_analysis: dict, wiki_presence: dict) -> list:
    """根據分析結果生成改進建議。"""
    recommendations = []
    
    # Experience 建議
    if scores["experience"] < 50:
        recommendations.append({
            "category": "Experience",
            "priority": "高",
            "title": "增加社群媒體曝光",
            "description": "建議加強在社群媒體平台的品牌曝光，包括 Facebook、Instagram、YouTube 等平台。",
            "actions": ["建立官方社群帳號", "定期發布內容", "與網紅合作", "舉辦線上活動"]
        })
    
    # Expertise 建議
    if scores["expertise"] < 60:
        recommendations.append({
            "category": "Expertise",
            "priority": "高",
            "title": "提升產業專業形象",
            "description": "需要增加在產業媒體的曝光度，建立專業權威形象。",
            "actions": ["發布產業白皮書", "參與產業論壇", "與專業媒體合作", "建立技術部落格"]
        })
    
    # Authoritativeness 建議
    if scores["authoritativeness"] < 70:
        recommendations.append({
            "category": "Authoritativeness",
            "priority": "中",
            "title": "建立維基百科頁面",
            "description": "建議為品牌建立維基百科頁面，提升權威性。",
            "actions": ["準備完整的品牌資料", "遵循維基百科編輯規範", "定期更新內容"]
        })
    
    # Trustworthiness 建議
    if scores["trustworthiness"] < 80:
        recommendations.append({
            "category": "Trustworthiness",
            "priority": "高",
            "title": "改善客戶服務",
            "description": "根據負面評論，建議改善客戶服務和產品品質。",
            "actions": ["建立 24/7 客服系統", "改善產品品質", "增加客戶回饋機制", "建立危機處理流程"]
        })
    
    return recommendations

def create_radar_chart(scores: dict):
    """建立雷達圖。"""
    categories = ['Experience', 'Expertise', 'Authoritativeness', 'Trustworthiness']
    values = [scores['experience'], scores['expertise'], scores['authoritativeness'], scores['trustworthiness']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='E-E-A-T 分數',
        line_color='rgb(102, 126, 234)',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="E-E-A-T 雷達圖分析",
        height=400
    )
    
    return fig

def create_bar_chart(media_analysis: dict):
    """建立媒體提及長條圖。"""
    media_types = []
    counts = []
    
    for item in media_analysis["mentions_by_type"]:
        media_types.append(item["type"])
        counts.append(item["count"])
    
    df = pd.DataFrame({
        '媒體類型': media_types,
        '提及次數': counts
    })
    
    fig = px.bar(df, x='媒體類型', y='提及次數',
                 title="各媒體類型提及次數",
                 color='提及次數',
                 color_continuous_scale='Blues')
    
    fig.update_layout(height=400)
    return fig

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
    
    # 步驟 4: 生成建議
    recommendations = generate_recommendations(eeat_scores, media_analysis, wiki_presence)
    
    # 步驟 5: 組合最終結果
    result = {
        "eeat_scores": eeat_scores,
        "media_analysis": media_analysis,
        "wiki_presence": wiki_presence,
        "uses_https": uses_https,
        "recommendations": recommendations
    }
    
    return result

# 主應用程式
def main():
    # 標題區域
    st.markdown("""
    <div class="main-header">
        <h1>🔍 E-E-A-T 分析工具</h1>
        <p>專業的品牌權威性、專業性、經驗與信任度分析平台</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 側邊欄
    with st.sidebar:
        st.header("⚙️ 設定")
        st.markdown("---")
        
        # 基本資訊
        brand_name = st.text_input("品牌名稱", "台灣品牌A")
        related_entities = st.text_area("相關實體（每行一個）", "產品B\n集團C").splitlines()
        official_info = st.text_area("官方資訊", "台灣品牌A是台灣領先的科技公司，主力產品為產品B。")
        
        st.markdown("---")
        
        # 媒體權重設定
        st.subheader("📊 媒體權重設定")
        st.caption("數字越大代表該媒體類型越重要")
        
        industry_news = st.slider("產業新聞", 0, 20, 10)
        mainstream_news = st.slider("主流新聞", 0, 20, 8)
        social_media = st.slider("社群媒體", 0, 20, 5)
        video_sites = st.slider("影音網站", 0, 20, 5)
        ecommerce_retail = st.slider("電商零售", 0, 20, 2)
        
        st.markdown("---")
        
        # 技術設定
        st.subheader("🔧 技術設定")
        uses_https = st.checkbox("網站支援 HTTPS", value=True)
        
        st.markdown("---")
        
        # 分析按鈕
        if st.button("🚀 開始分析", type="primary", use_container_width=True):
            st.session_state.analyze = True
    
    # 主要內容區域
    if 'analyze' in st.session_state and st.session_state.analyze:
        with st.spinner("🔍 正在進行深度分析..."):
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
            
            result = run_eeat_analysis(config_data, module1_output)
        
        # 顯示結果
        st.success("✅ 分析完成！")
        
        # E-E-A-T 分數卡片
        st.subheader("🎯 E-E-A-T 評分結果")
        scores = result["eeat_scores"]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            score_class = "score-high" if scores['experience'] >= 70 else "score-medium" if scores['experience'] >= 40 else "score-low"
            st.markdown(f"""
            <div class="metric-card">
                <h3>經驗 (Experience)</h3>
                <h2 class="{score_class}">{scores['experience']}/100</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            score_class = "score-high" if scores['expertise'] >= 70 else "score-medium" if scores['expertise'] >= 40 else "score-low"
            st.markdown(f"""
            <div class="metric-card">
                <h3>專業 (Expertise)</h3>
                <h2 class="{score_class}">{scores['expertise']}/100</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            score_class = "score-high" if scores['authoritativeness'] >= 70 else "score-medium" if scores['authoritativeness'] >= 40 else "score-low"
            st.markdown(f"""
            <div class="metric-card">
                <h3>權威 (Authoritativeness)</h3>
                <h2 class="{score_class}">{scores['authoritativeness']}/100</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            score_class = "score-high" if scores['trustworthiness'] >= 70 else "score-medium" if scores['trustworthiness'] >= 40 else "score-low"
            st.markdown(f"""
            <div class="metric-card">
                <h3>信任 (Trustworthiness)</h3>
                <h2 class="{score_class}">{scores['trustworthiness']}/100</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            score_class = "score-high" if scores['overall_score'] >= 70 else "score-medium" if scores['overall_score'] >= 40 else "score-low"
            st.markdown(f"""
            <div class="metric-card">
                <h3>總分 (Overall)</h3>
                <h2 class="{score_class}">{scores['overall_score']}/100</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # 視覺化圖表
        st.subheader("📊 視覺化分析")
        col1, col2 = st.columns(2)
        
        with col1:
            radar_fig = create_radar_chart(scores)
            st.plotly_chart(radar_fig, use_container_width=True)
        
        with col2:
            bar_fig = create_bar_chart(result["media_analysis"])
            st.plotly_chart(bar_fig, use_container_width=True)
        
        # 詳細分析報告
        st.subheader("📋 詳細分析報告")
        
        # 維基百科檢查結果
        with st.expander("🌐 維基百科收錄狀況", expanded=True):
            wiki_presence = result["wiki_presence"]
            if wiki_presence["brand_found"]:
                st.success(f"✅ 品牌 '{brand_name}' 在維基百科有收錄")
            else:
                st.warning(f"⚠️ 品牌 '{brand_name}' 在維基百科無收錄")
            
            if wiki_presence["related_entities_found"]:
                st.info(f"📚 相關實體收錄：{', '.join(wiki_presence['related_entities_found'])}")
            else:
                st.info("📚 相關實體均無維基百科收錄")
        
        # 媒體提及分析
        with st.expander("📰 媒體提及分析", expanded=True):
            media_analysis = result["media_analysis"]
            st.write(f"**總提及次數：{media_analysis['total_mentions']}**")
            
            for item in media_analysis["mentions_by_type"]:
                if item["count"] > 0:
                    st.write(f"- **{item['type']}**: {item['count']} 次提及")
                    if item["latest_mention"]:
                        st.caption(f"  最新：{item['latest_mention']['title']}")
        
        # 改進建議
        if result["recommendations"]:
            st.subheader("💡 改進建議")
            for i, rec in enumerate(result["recommendations"], 1):
                with st.expander(f"{i}. {rec['title']} ({rec['priority']}優先級)", expanded=True):
                    st.write(f"**類別：{rec['category']}**")
                    st.write(rec['description'])
                    st.write("**建議行動：**")
                    for action in rec['actions']:
                        st.write(f"- {action}")
        
        # 原始資料
        with st.expander("🔍 原始分析資料", expanded=False):
            st.json(result)
        
        st.markdown("---")
        st.caption("本工具由 Streamlit 製作，程式碼已開源於 GitHub。")

if __name__ == "__main__":
    main() 