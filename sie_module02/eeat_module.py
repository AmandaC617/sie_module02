import json
import datetime
import random
import time
import sys
from dateutil import parser as date_parser

try:
    import wikipediaapi
except ImportError:
    print("警告: 'wikipedia-api' 函式庫未安裝。維基百科檢查功能將無法運作。")
    print("請執行: pip install wikipedia-api")
    wikipediaapi = None

def mock_google_custom_search(query: str, media_type: str) -> dict:
    """
    模擬 Google Custom Search JSON API 的回應。
    在真實情境中，這裡會是實際的 API 呼叫。
    """
    print(f"--- 模擬 Google 搜尋: 媒體類型='{media_type}', 關鍵字='{query}' ---")
    time.sleep(0.1) # 模擬網路延遲
    
    # 根據媒體類型回傳不同的模擬資料
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
            },
            {
                "title": f"消費者報告：{query} 客戶服務滿意度調查",
                "link": f"https://consumer.example.com/{query.lower()}-service-review",
                "snippet": f"一份最新的報告顯示，約有 5% 的使用者回報核心產品B在特定情況下有過熱問題，{query}官方已回應將提供軟體更新。",
                "pagemap": {"metatags": [{"article:published_time": "2025-06-10T18:00:00Z"}]}
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
        "ecommerce_retail": [] # 假設電商平台搜尋沒有相關新聞
    }
    
    # 模擬某些查詢沒有結果的情況
    if random.random() > 0.8 and media_type not in ["industry_news", "mainstream_news"]:
        return {"items": []}
        
    return {"items": results.get(media_type, [])}

def mock_gemini_api(snippet: str, official_info: str) -> str:
    """
    模擬 Gemini API 進行內容正確性比對。
    """
    # print(f"--- 模擬 Gemini 比對: Snippet='{snippet[:30]}...' ---")
    time.sleep(0.05) # 模擬 API 延遲
    
    negative_keywords = ["過熱", "災情", "下跌", "電池續航力沒有想像中好"]
    if any(keyword in snippet for keyword in negative_keywords):
        return "Uncertain"
    
    positive_keywords = ["革命性", "新功能", "最佳雇主", "CP值超高"]
    if any(keyword in snippet for keyword in positive_keywords):
        return "Correct"
        
    return "Correct"

def check_wikipedia_presence(entities: list, user_agent: str) -> dict:
    """
    使用 Wikipedia API 檢查品牌和相關實體是否被維基百科收錄。
    """
    if not wikipediaapi:
        print("--- Wikipedia 檢查已跳過 (函式庫未安裝) ---")
        return {"brand_found": False, "related_entities_found": []}

    print("\n--- 正在執行 Wikipedia 收錄檢查 ---")
    wiki_client = wikipediaapi.Wikipedia(
        language='zh-tw',
        user_agent=user_agent
    )
    
    presence = {"brand_found": False, "related_entities_found": []}
    
    brand_name = entities[0]
    page_brand = wiki_client.page(brand_name)
    if page_brand.exists():
        presence["brand_found"] = True
        print(f"[成功] 品牌 '{brand_name}' 在維基百科存在。")
    else:
        print(f"[失敗] 品牌 '{brand_name}' 在維基百科不存在。")

    for entity in entities[1:]:
        page_entity = wiki_client.page(entity)
        if page_entity.exists():
            presence["related_entities_found"].append(entity)
            print(f"[成功] 相關實體 '{entity}' 在維基百科存在。")
        else:
            print(f"[失敗] 相關實體 '{entity}' 在維基百科不存在。")
            
    return presence

def analyze_media_mentions(brand_name: str, related_entities: list, media_weights: dict, official_info: str) -> dict:
    """
    遍歷各媒體類型，分析媒體提及並進行正確性檢查。
    """
    print("\n--- 正在執行媒體提及分析 ---")
    all_mentions = {}
    search_entities = [brand_name] + related_entities

    for media_type in media_weights.keys():
        all_mentions[media_type] = []
        for entity in search_entities:
            # 實際應用中，您會呼叫真實的 Google API
            response = mock_google_custom_search(entity, media_type)
            
            if "items" in response:
                for item in response["items"]:
                    # 解析日期
                    date_str = ""
                    try:
                        # Google Custom Search API 通常將日期放在 pagemap 中
                        date_str = item.get("pagemap", {}).get("metatags", [{}])[0].get("article:published_time", "")
                        parsed_date = date_parser.parse(date_str).date()
                    except (ValueError, TypeError):
                        # 如果解析失敗，使用一個預設的舊日期以便排序
                        parsed_date = datetime.date(1970, 1, 1)

                    # 進行正確性檢查
                    accuracy = mock_gemini_api(item.get("snippet", ""), official_info)

                    all_mentions[media_type].append({
                        "title": item.get("title", "無標題"),
                        "url": item.get("link", "#"),
                        "date_obj": parsed_date,
                        "date": parsed_date.isoformat() if parsed_date != datetime.date(1970, 1, 1) else "N/A",
                        "accuracy_check": accuracy,
                        "snippet": item.get("snippet", "")
                    })

    # 格式化最終輸出
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

        # 依日期排序，最新的在最前面
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
        "raw_mentions": all_mentions # 將原始資料傳遞給評分函式
    }

def calculate_eeat_scores(media_analysis: dict, wiki_presence: dict, uses_https: bool) -> dict:
    """
    根據媒體分析、維基百科收錄和 HTTPS 使用情況計算 E-E-A-T 分數。
    """
    print("\n--- 正在計算 E-E-A-T 分數 ---")
    scores = {
        "experience": 0, "expertise": 0, "authoritativeness": 0, "trustworthiness": 0
    }
    
    # 1. Authoritativeness (權威性)
    auth_score = 0
    for item in media_analysis["mentions_by_type"]:
        auth_score += item["count"] * item["weight"]
    # 維基百科加分
    if wiki_presence["brand_found"]:
        auth_score += 20
    auth_score += len(wiki_presence["related_entities_found"]) * 10
    scores["authoritativeness"] = min(100, int(auth_score))

    # 2. Expertise (專業性)
    industry_mentions = media_analysis["raw_mentions"].get("industry_news", [])
    # 分數基於產業新聞的數量，假設每篇5分，上限為100
    scores["expertise"] = min(100, len(industry_mentions) * 5)

    # 3. Experience (經驗)
    social_mentions = media_analysis["raw_mentions"].get("social_media", [])
    video_mentions = media_analysis["raw_mentions"].get("video_sites", [])
    experience_mentions = social_mentions + video_mentions
    # 分數基於社群和影音的提及數，每篇2分，上限為100
    scores["experience"] = min(100, len(experience_mentions) * 2)

    # 4. Trustworthiness (信任度)
    trust_score = 0
    # HTTPS基礎分數
    if uses_https:
        trust_score += 40
    mainstream_mentions = media_analysis["raw_mentions"].get("mainstream_news", [])
    if mainstream_mentions:
        positive_or_neutral_count = sum(1 for m in mainstream_mentions if m["accuracy_check"] == "Correct")
        negative_count = len(mainstream_mentions) - positive_or_neutral_count
        
        # 正面/中立提及加分，負面提及扣分
        trust_score += positive_or_neutral_count * 5
        trust_score -= negative_count * 15 # 負面新聞的懲罰較重
    
    scores["trustworthiness"] = max(0, min(100, int(trust_score)))
    
    # 5. Overall Score (總分)
    overall = sum(scores.values()) / len(scores)
    scores["overall_score"] = int(overall)
    
    return scores

def run_module_2(config_data: dict, module1_output: dict):
    """
    執行模組2的主函式。
    """
    brand_name = config_data["brand_name"]
    related_entities = config_data["related_entities"]
    media_weights = config_data["media_weights"]
    official_info = config_data["official_info"]
    user_agent = "SIE-Diagnostic-Tool/1.0 (contact@example.com)"
    
    # 從模組1獲取 HTTPS 資訊
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

def main():
    if len(sys.argv) != 3:
        print("用法: python eeat_module.py <config.json> <module1_output.json>")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        module1_output = json.load(f)
    result = run_module_2(config_data, module1_output)
    print("\n--- E-E-A-T 評分結果 ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 