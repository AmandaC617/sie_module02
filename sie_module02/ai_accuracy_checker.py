# -*- coding: utf-8 -*-
import os
import json
import requests
import fitz  # PyMuPDF
import spacy
import google.generativeai as genai
from bs4 import BeautifulSoup
import hashlib
import time

# --- 環境設定 ---
# 建議將 API 金鑰儲存在環境變數中，而不是寫在程式碼裡
# 在您的終端機中執行: export GOOGLE_API_KEY="您的API金鑰"
API_KEY = os.getenv("GOOGLE_API_KEY")
CACHE_DIR = "cache"
CACHE_EXPIRATION_SECONDS = 86400  # 24 小時

# --- 初始化快取目錄 ---
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# 確保 spaCy 中文模型已下載
# python -m spacy download zh_core_web_sm
try:
    nlp = spacy.load("zh_core_web_sm")
except OSError:
    print("spaCy 中文模型 'zh_core_web_sm' 未找到。")
    print("請執行: python -m spacy download zh_core_web_sm")
    nlp = None

class AIAccuracyChecker:
    """
    一個用於深度比對 LLM 認知與權威原始資料的工具。
    它從「精準詞組」與「廣泛語意」兩個維度進行評分，並具備快取與進階不匹配分析功能。
    """

    def __init__(self, config_data: dict, api_key: str):
        """
        初始化檢查器。

        :param config_data: 包含 'accuracy_source' 和 'supplemental_info' 的字典。
        :param api_key: Google Gemini API 金鑰。
        """
        if not api_key:
            raise ValueError("API 金鑰未提供。請設定 GOOGLE_API_KEY 環境變數。")
        self.config = config_data
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        print("AIAccuracyChecker 初始化完成。")

    def _get_cache_path(self, url: str) -> str:
        """根據 URL 生成快取檔案路徑。"""
        hashed_url = hashlib.md5(url.encode('utf-8')).hexdigest()
        return os.path.join(CACHE_DIR, f"{hashed_url}.txt")

    def _ingest_source(self) -> str:
        """
        根據設定抓取、解析並合併原始資料，形成「事實基礎」。
        *** 新增快取機制 ***
        """
        source = self.config.get("accuracy_source", {})
        source_type = source.get("type")
        source_value = source.get("value")
        
        print(f"正在擷取資料來源... 類型: {source_type}")

        content = ""
        try:
            if source_type == "url":
                cache_path = self._get_cache_path(source_value)
                # 檢查快取是否存在且未過期
                if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path)) < CACHE_EXPIRATION_SECONDS:
                    print(f"從快取載入: {cache_path}")
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                else:
                    print(f"從網路抓取: {source_value}")
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                    response = requests.get(source_value, headers=headers, timeout=20)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    for script_or_style in soup(["script", "style"]):
                        script_or_style.decompose()
                    content = soup.get_text(separator='\n', strip=True)
                    # 寫入快取
                    with open(cache_path, 'w', encoding='utf-8') as f:
                        f.write(content)
            
            elif source_type == "pdf":
                # PDF 暫不實作快取，但邏輯類似
                response = requests.get(source_value, timeout=20)
                response.raise_for_status()
                with fitz.open(stream=response.content, filetype="pdf") as doc:
                    content = "".join(page.get_text() for page in doc)

            elif source_type == "text":
                content = source_value
            
            else:
                raise ValueError(f"不支援的來源類型: {source_type}")

        except requests.RequestException as e:
            print(f"錯誤: 無法從 {source_value} 擷取資料。 {e}")
            return ""
        except Exception as e:
            print(f"處理來源時發生未預期的錯誤: {e}")
            return ""

        supplemental_info = self.config.get("supplemental_info", "")
        if supplemental_info:
            content += "\n\n--- 補充資訊 ---\n" + supplemental_info
        
        print(f"資料擷取完成，總字數: {len(content)}")
        return content

    def _call_gemini(self, prompt: str, model_name: str = "gemini-1.5-flash", is_json_output: bool = False) -> str:
        """通用的 Gemini API 呼叫函式。"""
        try:
            model = genai.GenerativeModel(model_name)
            generation_config = genai.types.GenerationConfig(
                response_mime_type="application/json" if is_json_output else "text/plain"
            )
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            print(f"呼叫 Gemini API 時發生錯誤 ({model_name}): {e}")
            return ""

    def _classify_information(self, ground_truth_text: str) -> str:
        """使用 LLM 對「事實基礎」文本進行分類。"""
        print("正在進行資訊分類...")
        prompt = f"""
        你是一位資訊分類專家。請根據以下提供的「事實基礎」文本，將其主要內容歸類到以下其中一個類別中：
        "功能/規格型", "價格/優惠型", "公司/品牌歷史型", "客戶服務/支援型", "通用描述型"。
        請僅回傳最適合的類別名稱，不要包含任何其他解釋。
        「事實基礎」文本:
        ---
        {ground_truth_text[:4000]} 
        ---
        """
        classification = self._call_gemini(prompt)
        print(f"資訊分類結果: {classification.strip()}")
        return classification.strip()

    def _get_llm_response(self, ground_truth_text: str, model_name: str) -> str:
        """讓目標 LLM 根據「事實基礎」生成回答。"""
        print(f"正在從目標模型 {model_name} 生成回答...")
        prompt = f"""
        請你扮演一個AI助理，並根據以下提供的「上下文」資料，用一段通順的摘要來總結其核心內容。
        你的回答必須完全基於「上下文」，不可捏造或引用外部資訊。
        「上下文」:
        ---
        {ground_truth_text}
        ---
        摘要:
        """
        response = self._call_gemini(prompt, model_name=model_name)
        print("已取得 AI 回答。")
        return response

    def _calculate_phrase_matching_score(self, ground_truth_text: str, llm_answer: str) -> tuple:
        """計算精準詞組比對分數。"""
        if not nlp:
            print("警告: spaCy 模型未載入，跳過精準詞組比對。")
            return 0, []

        print("正在計算精準詞組比對分數...")
        doc = nlp(ground_truth_text)
        
        key_phrases = set()
        for ent in doc.ents:
            if ent.label_ in ["PRODUCT", "ORG", "MONEY", "QUANTITY", "CARDINAL", "GPE", "DATE"]:
                key_phrases.add(ent.text.strip())
        for token in doc:
            if token.is_digit or token.like_num:
                 key_phrases.add(token.text.strip())
        for chunk in doc.noun_chunks:
            # 增加一些過濾條件，避免太多無意義的名詞片語
            if len(chunk.text.strip()) > 2 and not chunk.text.strip().isnumeric():
                key_phrases.add(chunk.text.strip())
        
        key_phrases = {p for p in key_phrases if len(p) > 1 and not p.isspace()}

        if not key_phrases:
            return 100, []

        found_count = 0
        mismatched_phrases_list = []
        for phrase in key_phrases:
            if phrase.lower() in llm_answer.lower():
                found_count += 1
            else:
                mismatched_phrases_list.append(phrase)
        
        score = (found_count / len(key_phrases)) * 100
        print(f"精準詞組比對完成。找到 {found_count}/{len(key_phrases)} 個關鍵詞組。")
        return round(score), mismatched_phrases_list

    def _analyze_mismatches_semantically(self, mismatched_phrases: list, llm_answer: str) -> list:
        """
        *** 新增功能：使用 LLM 分析不匹配的詞組，尋找語意對應詞 ***
        """
        if not mismatched_phrases:
            return []
        
        print("正在進行進階不匹配分析...")
        
        # 將 list 轉換為 JSON 字符串，以便在 prompt 中使用
        mismatched_json_str = json.dumps(mismatched_phrases, ensure_ascii=False)

        prompt = f"""
        你是一位語意分析專家。請將「AI 回應」與「預期詞組列表」進行比對。
        對於列表中的每一個「預期詞組」，請在「AI 回應」中找出與其語意最相近的表達方式。

        請嚴格遵循以下 JSON 格式回傳結果，不要有任何其他文字。
        如果找不到語意相近的表達，請將 "actual" 欄位的值設為 "語意上未找到"。

        [
          {{
            "expected": "<預期詞組1>",
            "actual": "<在AI回應中找到的語意對應詞1>"
          }},
          {{
            "expected": "<預_期詞組2>",
            "actual": "語意上未找到"
          }}
        ]

        「AI 回應」:
        ---
        {llm_answer}
        ---

        「預期詞組列表」:
        {mismatched_json_str}
        """
        
        response_str = self._call_gemini(prompt, model_name="gemini-1.5-pro", is_json_output=True)
        try:
            if response_str.strip().startswith("```json"):
                response_str = response_str.strip()[7:-3].strip()
            
            analysis_result = json.loads(response_str)
            print("進階不匹配分析完成。")
            return analysis_result
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"錯誤: 無法解析不匹配分析的回應。 {e}\n收到的回應: {response_str}")
            # 如果解析失敗，回傳原始的不匹配列表
            return [{"expected": p, "actual": "分析失敗"} for p in mismatched_phrases]


    def _calculate_semantic_consistency_score(self, ground_truth_text: str, llm_answer: str) -> tuple:
        """使用 LLM 評估語意一致性。"""
        print("正在計算廣泛語意一致性分數...")
        prompt = f"""
        請扮演一位專業且嚴格的事實查核員。
        你的任務是評估「AI 回應」在語意上是否完整、準確地傳達了「原始資料」的核心思想，且沒有產生誤導或遺漏重要資訊。
        請遵循以下 JSON 格式回傳你的評估結果，不要有任何其他文字：
        {{
          "semantic_consistency_score": <一個 0 到 100 之間的整數分數>,
          "reasoning": "<一段簡潔但具體的評分理由，說明扣分或給分的原因>"
        }}
        「原始資料」:
        ---
        {ground_truth_text}
        ---
        「AI 回應」:
        ---
        {llm_answer}
        ---
        """
        response_str = self._call_gemini(prompt, model_name="gemini-1.5-pro", is_json_output=True)
        
        try:
            if response_str.strip().startswith("```json"):
                response_str = response_str.strip()[7:-3].strip()
            
            result = json.loads(response_str)
            score = result.get("semantic_consistency_score", 0)
            reasoning = result.get("reasoning", "無法解析評分理由。")
            print("廣泛語意一致性分數計算完成。")
            return score, reasoning
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"錯誤: 無法解析語意評分的回應。 {e}\n收到的回應: {response_str}")
            return 0, "無法從 LLM 獲得有效的 JSON 格式評分。"

    def run_check(self) -> dict:
        """執行完整的正確度檢查流程。"""
        print("--- 開始執行 AI 資訊正確度檢查 v2.1 ---")
        model_to_check = self.config.get("model_to_check", "gemini-1.5-flash")

        ground_truth = self._ingest_source()
        if not ground_truth:
            return {"error": "無法建立事實基礎，檢查中止。"}

        classification = self._classify_information(ground_truth)
        llm_answer = self._get_llm_response(ground_truth, model_name=model_to_check)

        # 雙維度評分
        phrase_score, initial_mismatches = self._calculate_phrase_matching_score(ground_truth, llm_answer)
        semantic_score, semantic_reasoning = self._calculate_semantic_consistency_score(ground_truth, llm_answer)
        
        # *** 執行新的進階不匹配分析 ***
        final_mismatches = self._analyze_mismatches_semantically(initial_mismatches, llm_answer)

        overall_score = round((phrase_score * 0.4) + (semantic_score * 0.6))
        
        result = {
            "ai_accuracy_v2": {
                "source_info": {
                    "type": self.config["accuracy_source"]["type"],
                    "value": self.config["accuracy_source"]["value"],
                    "classification": classification
                },
                "model_used": model_to_check,
                "accuracy_scores": {
                    "overall_score": overall_score,
                    "phrase_matching_score": phrase_score,
                    "semantic_consistency_score": semantic_score
                },
                "semantic_score_reasoning": semantic_reasoning,
                "mismatched_phrases_analysis": final_mismatches, # 欄位更新為更具描述性的名稱
            }
        }
        print("--- 檢查完成 ---")
        return result

def run_ai_accuracy_check(config_data: dict, gemini_api_key: str) -> dict:
    """執行 AI 資訊正確度檢查的主函式"""
    try:
        checker = AIAccuracyChecker(config_data, gemini_api_key)
        return checker.run_check()
    except Exception as e:
        return {"error": f"AI 資訊正確度檢查失敗: {str(e)}"}

# --- 主程式執行區塊 ---
if __name__ == "__main__":
    # 範例 1: 檢查一個 URL (可能會觸發快取)
    print("\n" + "="*20 + " 範例 1: 檢查 URL " + "="*20)
    config_url = {
      "accuracy_source": {
        "type": "url",
        "value": "https://zh.wikipedia.org/wiki/%E5%8F%B0%E7%A9%8D%E9%9B%BB"
      },
      "supplemental_info": "台積電是全球最大的專業積體電路製造服務公司。",
      "model_to_check": "gemini-1.5-flash"
    }
    
    if API_KEY and nlp:
        checker_url = AIAccuracyChecker(config_url, API_KEY)
        report_url = checker_url.run_check()
        print("\n最終報告 (JSON):")
        print(json.dumps(report_url, indent=2, ensure_ascii=False))
    else:
        print("跳過範例 1，因為缺少 API 金鑰或 spaCy 模型。")

    # 範例 2: 檢查一段文字 (測試進階不匹配分析)
    print("\n" + "="*20 + " 範例 2: 檢查 TEXT " + "="*20)
    config_text = {
      "accuracy_source": {
        "type": "text",
        "value": """
        我們的最新款智慧手錶「Vision Pro X」，配備了 1.9 吋的 AMOLED 螢幕，解析度為 480x480。
        電池容量為 5000mAh，在正常使用下可提供長達 7 天的續航力。
        它內建 GPS 和心率感測器，並支援超過 100 種運動模式。
        防水等級達到 5ATM，適合游泳時配戴。售價為新台幣 8,800 元。
        """
      },
      "supplemental_info": "這是我們 2024 年的旗艦產品。",
      "model_to_check": "gemini-1.5-flash"
    }

    if API_KEY and nlp:
        checker_text = AIAccuracyChecker(config_text, API_KEY)
        # 為了展示效果，我們手動讓 AI 的回答模糊化
        checker_text._get_llm_response = lambda gt, mn: "這款 Vision Pro X 手錶有高解析度螢幕和超大容量電池，續航很久，防水能力也不錯，售價約八千多元。"
        report_text = checker_text.run_check()
        print("\n最終報告 (JSON):")
        print(json.dumps(report_text, indent=2, ensure_ascii=False))
    else:
        print("跳過範例 2，因為缺少 API 金鑰或 spaCy 模型。") 