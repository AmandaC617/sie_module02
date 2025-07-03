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
    # ... existing code ...
    # (原本的 mock_google_custom_search 內容)
    # ... existing code ...
    negative_keywords = ["過熱", "災情", "下跌", "電池續航力沒有想像中好"]
    # ... existing code ...

def mock_gemini_api(snippet: str, official_info: str) -> str:
    # ... existing code ...
    # (原本的 mock_gemini_api 內容)
    # ... existing code ...

def check_wikipedia_presence(entities: list, user_agent: str) -> dict:
    # ... existing code ...
    # (原本的 check_wikipedia_presence 內容)
    # ... existing code ...

def analyze_media_mentions(brand_name: str, related_entities: list, media_weights: dict, official_info: str) -> dict:
    # ... existing code ...
    # (原本的 analyze_media_mentions 內容)
    # ... existing code ...

def calculate_eeat_scores(media_analysis: dict, wiki_presence: dict, uses_https: bool) -> dict:
    # ... existing code ...
    # (原本的 calculate_eeat_scores 內容)
    # ... existing code ...

def run_module_2(config_data: dict, module1_output: dict):
    brand_name = config_data["brand_name"]
    related_entities = config_data["related_entities"]
    media_weights = config_data["media_weights"]
    official_info = config_data["official_info"]
    user_agent = "SIE-Diagnostic-Tool/1.0 (contact@example.com)"
    uses_https = module1_output.get("site_analysis", {}).get("uses_https", False)
    wiki_presence = check_wikipedia_presence([brand_name] + related_entities, user_agent)
    media_analysis = analyze_media_mentions(brand_name, related_entities, media_weights, official_info)
    eeat_scores = calculate_eeat_scores(media_analysis, wiki_presence, uses_https)
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