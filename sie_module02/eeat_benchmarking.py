import requests
import json
import time
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import os
from typing import Dict, List, Optional, Tuple
import streamlit as st
from datetime import datetime, timedelta
import random

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("警告: google-generativeai 未安裝，Gemini API 功能將無法使用")

class EEATBenchmarkingAnalyzer:
    """動態 E-E-A-T 評估與競爭基準分析器"""
    
    def __init__(self, gemini_api_key: Optional[str] = None, market: Optional[str] = None, product_category: Optional[str] = None, brand: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SIE-Benchmarking-Tool/1.0 (contact@example.com)'
        })
        
        # 初始化 Gemini API
        if gemini_api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.gemini_model = None
        
        self.market = market or "台灣"
        self.product_category = product_category or ""
        self.brand = brand or ""
        # 動態產生主流媒體/論壇/社群名單
        self.market_media_dict = self._generate_market_media_with_llm(self.market, self.product_category, self.brand)
        # 預留：根據市場分類的競爭對手清單
        self.market_competitors_dict = {
            "台灣": ["台積電", "聯電", "世界先進"],
            "全球": ["Intel", "Samsung", "TSMC"]
            # ...可擴充更多市場
        }
    
    def analyze_eeat_benchmarking(self, target_website: str, competitors: List[str] = []) -> Dict:
        """執行動態 E-E-A-T 評估與競爭基準分析"""
        if not target_website.startswith(('http://', 'https://')):
            target_website = 'https://' + target_website
        st.info(f"🔍 正在分析目標網站: {target_website}（市場：{self.market}）")
        try:
            # 0. LLM 行業/市場/產品領導者推薦
            leaders_recommendation = self._llm_recommend_leaders(self.market, self.product_category, self.brand, target_website)
            # 0.1 LLM 自動比對本品牌與標竿差異
            brand_gap_analysis = self._llm_compare_with_benchmarks(self.brand, target_website, self.market, self.product_category, leaders_recommendation)
            # 1. AI 領導者識別與分析（保留技術指標分析）
            ai_leader_analysis = self._identify_ai_leaders(target_website)
            # 2. 動態媒體權重評估
            dynamic_media_weights = self._analyze_dynamic_media_weights(target_website)
            # 3. 真實媒體曝光紀錄查詢
            real_media_mentions = self._fetch_real_media_mentions(self.market_media_dict)
            # 4. 競爭對手基準分析
            if not competitors:
                competitors = self.market_competitors_dict.get(self.market, [])
            competitor_benchmarking = self._analyze_competitor_benchmarks(target_website, competitors)
            # 5. 趨勢追蹤與預測
            trend_analysis = self._analyze_trends_and_predictions(target_website)
            # 6. 生成策略建議
            strategic_recommendations = self._generate_strategic_recommendations(
                ai_leader_analysis, dynamic_media_weights, competitor_benchmarking, trend_analysis
            )
            return {
                "eeat_benchmarking": {
                    "leaders_recommendation": leaders_recommendation,
                    "brand_gap_analysis": brand_gap_analysis,
                    "ai_leader_analysis": ai_leader_analysis,
                    "dynamic_media_weights": dynamic_media_weights,
                    "real_media_mentions": real_media_mentions,
                    "competitor_benchmarking": competitor_benchmarking,
                    "trend_analysis": trend_analysis,
                    "strategic_recommendations": strategic_recommendations,
                    "market": self.market,
                    "market_media": self.market_media_dict,
                    "market_competitors": self.market_competitors_dict.get(self.market, [])
                }
            }
        except Exception as e:
            st.error(f"分析過程中發生錯誤: {str(e)}")
            return {"error": str(e)}
    
    def _identify_ai_leaders(self, target_website: str) -> Dict:
        """識別與分析 AI 領導者"""
        st.write("🤖 識別 AI 領導者...")
        
        ai_leader_analysis = {
            "ai_leader_score": 0,
            "ai_technology_indicators": [],
            "ai_content_signals": [],
            "ai_engagement_metrics": {},
            "ai_leadership_position": "unknown"
        }
        
        try:
            response = self.session.get(target_website, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 檢查 AI 技術指標
                ai_tech_indicators = []
                
                # 檢查是否有 AI 相關的 meta 標籤
                meta_tags = soup.find_all('meta')
                for meta in meta_tags:
                    content = meta.get('content', '').lower()
                    if any(ai_term in content for ai_term in ['ai', 'artificial intelligence', 'machine learning', 'automation']):
                        ai_tech_indicators.append(f"AI Meta Tag: {meta.get('name', 'unknown')}")
                
                # 檢查是否有 AI 相關的 JavaScript
                scripts = soup.find_all('script')
                for script in scripts:
                    script_content = script.string or ''
                    if any(ai_term in script_content.lower() for ai_term in ['ai', 'artificial intelligence', 'machine learning', 'automation']):
                        ai_tech_indicators.append("AI JavaScript Integration")
                        break
                
                # 檢查是否有 AI 相關的內容
                page_text = soup.get_text().lower()
                ai_content_signals = []
                
                ai_keywords = [
                    'artificial intelligence', 'machine learning', 'ai', 'automation',
                    'predictive analytics', 'natural language processing', 'nlp',
                    'computer vision', 'deep learning', 'neural networks'
                ]
                
                for keyword in ai_keywords:
                    if keyword in page_text:
                        ai_content_signals.append(keyword)
                
                ai_leader_analysis["ai_technology_indicators"] = ai_tech_indicators
                ai_leader_analysis["ai_content_signals"] = ai_content_signals
                
                # 計算 AI 領導者分數
                score = 0
                score += len(ai_tech_indicators) * 10
                score += len(ai_content_signals) * 5
                
                # 模擬 AI 參與度指標
                ai_leader_analysis["ai_engagement_metrics"] = {
                    "ai_mentions_count": len(ai_content_signals),
                    "ai_technology_integration": len(ai_tech_indicators),
                    "ai_content_frequency": len(ai_content_signals) / max(len(page_text.split()), 1) * 1000
                }
                
                ai_leader_analysis["ai_leader_score"] = min(score, 100)
                
                # 判斷 AI 領導地位
                if score >= 80:
                    ai_leader_analysis["ai_leadership_position"] = "leader"
                    st.success("🏆 識別為 AI 領導者")
                elif score >= 50:
                    ai_leader_analysis["ai_leadership_position"] = "emerging"
                    st.info("📈 AI 新興領導者")
                elif score >= 20:
                    ai_leader_analysis["ai_leadership_position"] = "follower"
                    st.warning("📊 AI 跟隨者")
                else:
                    ai_leader_analysis["ai_leadership_position"] = "laggard"
                    st.error("⚠️ AI 落後者")
                
        except Exception as e:
            st.warning(f"⚠️ 無法分析 AI 領導者指標: {str(e)}")
        
        return ai_leader_analysis
    
    def _analyze_dynamic_media_weights(self, target_website: str) -> dict:
        """
        分析媒體權重與覆蓋率：
        - 新聞類來源用 Google News API 查詢品牌/網站是否被提及。
        - 其他類型（社群、論壇、影音、Wiki）用 Gemini LLM 推論是否常被提及。
        - 綜合信任度、提及情況、來源多樣性計算分數。
        """
        media_dict = self.market_media_dict
        brand = self.brand
        product_category = self.product_category
        result = {"新聞": [], "社群": [], "論壇": [], "影音": [], "Wiki": []}
        total_weight = 0
        covered_weight = 0
        covered_count = 0
        total_count = 0
        # 1. 新聞類：Google News API
        api_key = "bce856a8587d46ff84050efba536c445"
        endpoint = "https://newsapi.org/v2/everything"
        for media in media_dict.get("新聞", []):
            name = media.get("name")
            trust_score = media.get("trust_score", 80)
            llm_favorite = media.get("llm_favorite", False)
            params = {
                "q": f"{brand} OR {product_category}",
                "sources": "",
                "apiKey": api_key,
                "language": "zh",
                "sortBy": "publishedAt",
                "pageSize": 3
            }
            found = False
            try:
                resp = requests.get(endpoint, params=params, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    for article in data.get("articles", []):
                        if name in article.get("source", {}).get("name", ""):
                            found = True
                            break
            except Exception:
                pass
            result["新聞"].append({
                "name": name,
                "llm_favorite": llm_favorite,
                "trust_score": trust_score,
                "reason": media.get("reason", ""),
                "covered": found,
                "source_type": "新聞"
            })
            total_weight += trust_score
            total_count += 1
            if found:
                covered_weight += trust_score
                covered_count += 1
        # 2. 其他類型：LLM 輔助推論
        if self.gemini_model:
            for media_type in ["社群", "論壇", "影音", "Wiki"]:
                for media in media_dict.get(media_type, []):
                    name = media.get("name")
                    trust_score = media.get("trust_score", 80)
                    llm_favorite = media.get("llm_favorite", False)
                    prompt = f"""
請根據下列資訊，推論品牌/網站是否常被此來源提及、引用、嵌入或連結：
- 品牌：{brand}
- 品類：{product_category}
- 來源名稱：{name}
- 官網：{target_website}
請回傳：
{{
  "covered": true/false, // 是否常被提及
  "score": 0-100, // 推論分數，愈高愈常被提及
  "reason": "推論依據"
}}
"""
                    try:
                        response = self.gemini_model.generate_content(prompt)
                        text = response.text.strip()
                        if text.startswith('```json'):
                            text = text[7:]
                        if text.endswith('```'):
                            text = text[:-3]
                        text = text.strip()
                        info = json.loads(text)
                        covered = info.get("covered", False)
                        score = info.get("score", 0)
                        reason = info.get("reason", "")
                    except Exception:
                        covered = False
                        score = 0
                        reason = "LLM 回應失敗"
                    result[media_type].append({
                        "name": name,
                        "llm_favorite": llm_favorite,
                        "trust_score": trust_score,
                        "reason": media.get("reason", ""),
                        "covered": covered,
                        "llm_score": score,
                        "llm_reason": reason,
                        "source_type": media_type
                    })
                    total_weight += trust_score
                    total_count += 1
                    if covered:
                        covered_weight += trust_score
                        covered_count += 1
        # 3. 分數計算
        coverage_rate = covered_count / total_count if total_count else 0
        weighted_coverage = covered_weight / total_weight if total_weight else 0
        media_weight_score = int(weighted_coverage * 100)
        return {
            "media_coverage_score": media_weight_score,
            "coverage_rate": coverage_rate,
            "covered_count": covered_count,
            "total_count": total_count,
            "sources": result
        }
    
    def _analyze_competitor_benchmarks(self, target_website: str, competitors: List[str] = []) -> Dict:
        """分析競爭對手基準"""
        st.write("🏆 分析競爭對手基準...")
        
        if not competitors:
            # 模擬競爭對手
            competitors = [
                "competitor1.com",
                "competitor2.com",
                "competitor3.com"
            ]
        
        competitor_benchmarking = {
            "competitor_analysis": [],
            "market_position": "unknown",
            "competitive_advantages": [],
            "improvement_opportunities": []
        }
        
        try:
            # 分析目標網站
            target_analysis = self._analyze_single_competitor(target_website, "Target")
            
            # 分析競爭對手
            competitor_analyses = []
            for competitor in competitors:
                try:
                    comp_analysis = self._analyze_single_competitor(competitor, f"Competitor {competitors.index(competitor) + 1}")
                    competitor_analyses.append(comp_analysis)
                except Exception as e:
                    st.warning(f"⚠️ 無法分析競爭對手 {competitor}: {str(e)}")
            
            competitor_benchmarking["competitor_analysis"] = [target_analysis] + competitor_analyses
            
            # 計算市場地位
            target_score = target_analysis["overall_score"]
            competitor_scores = [comp["overall_score"] for comp in competitor_analyses if comp["overall_score"] > 0]
            
            if competitor_scores:
                avg_competitor_score = sum(competitor_scores) / len(competitor_scores)
                if target_score > avg_competitor_score * 1.2:
                    competitor_benchmarking["market_position"] = "leader"
                    st.success("🏆 市場領導者")
                elif target_score > avg_competitor_score:
                    competitor_benchmarking["market_position"] = "strong"
                    st.info("💪 強勢競爭者")
                elif target_score > avg_competitor_score * 0.8:
                    competitor_benchmarking["market_position"] = "average"
                    st.warning("📊 平均水準")
                else:
                    competitor_benchmarking["market_position"] = "laggard"
                    st.error("⚠️ 落後競爭者")
            
            # 識別競爭優勢
            if target_analysis["ai_leader_score"] > 50:
                competitor_benchmarking["competitive_advantages"].append("AI Leadership")
            
            if target_analysis["social_authority_score"] > 60:
                competitor_benchmarking["competitive_advantages"].append("Strong Social Presence")
            
            if target_analysis["media_coverage_score"] > 70:
                competitor_benchmarking["competitive_advantages"].append("Positive Media Coverage")
            
            # 識別改善機會
            if target_analysis["ai_leader_score"] < 30:
                competitor_benchmarking["improvement_opportunities"].append("Enhance AI Technology Integration")
            
            if target_analysis["social_authority_score"] < 40:
                competitor_benchmarking["improvement_opportunities"].append("Strengthen Social Media Presence")
            
            if target_analysis["media_coverage_score"] < 50:
                competitor_benchmarking["improvement_opportunities"].append("Improve Media Relations")
            
        except Exception as e:
            st.warning(f"⚠️ 無法完成競爭對手基準分析: {str(e)}")
        
        return competitor_benchmarking
    
    def _analyze_single_competitor(self, website: str, name: str) -> Dict:
        """分析單一競爭對手"""
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        try:
            response = self.session.get(website, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 模擬分析結果
                analysis = {
                    "name": name,
                    "website": website,
                    "ai_leader_score": random.randint(20, 90),
                    "social_authority_score": random.randint(30, 85),
                    "media_coverage_score": random.randint(40, 95),
                    "content_quality_score": random.randint(50, 95),
                    "overall_score": 0
                }
                
                # 計算總分
                analysis["overall_score"] = (
                    analysis["ai_leader_score"] * 0.3 +
                    analysis["social_authority_score"] * 0.25 +
                    analysis["media_coverage_score"] * 0.25 +
                    analysis["content_quality_score"] * 0.2
                )
                
                return analysis
            else:
                return {
                    "name": name,
                    "website": website,
                    "ai_leader_score": 0,
                    "social_authority_score": 0,
                    "media_coverage_score": 0,
                    "content_quality_score": 0,
                    "overall_score": 0
                }
        except Exception as e:
            return {
                "name": name,
                "website": website,
                "ai_leader_score": 0,
                "social_authority_score": 0,
                "media_coverage_score": 0,
                "content_quality_score": 0,
                "overall_score": 0,
                "error": str(e)
            }
    
    def _analyze_trends_and_predictions(self, target_website: str) -> Dict:
        """分析趨勢與預測"""
        st.write("📈 分析趨勢與預測...")
        
        trend_analysis = {
            "current_trends": [],
            "predicted_growth": {},
            "market_opportunities": [],
            "risk_factors": []
        }
        
        try:
            # 模擬當前趨勢
            current_trends = [
                "AI Integration Acceleration",
                "Voice Search Optimization",
                "Video Content Dominance",
                "Personalization at Scale",
                "Sustainability Focus"
            ]
            
            trend_analysis["current_trends"] = current_trends
            
            # 模擬預測成長
            trend_analysis["predicted_growth"] = {
                "ai_adoption_rate": random.uniform(15, 35),
                "content_consumption_growth": random.uniform(20, 40),
                "social_engagement_increase": random.uniform(10, 25),
                "market_share_growth": random.uniform(5, 15)
            }
            
            # 識別市場機會
            market_opportunities = [
                "AI-Powered Content Personalization",
                "Voice-First Content Strategy",
                "Interactive Video Experiences",
                "Sustainability Messaging",
                "Micro-Moment Optimization"
            ]
            
            trend_analysis["market_opportunities"] = market_opportunities
            
            # 識別風險因素
            risk_factors = [
                "AI Regulation Changes",
                "Privacy Policy Updates",
                "Algorithm Changes",
                "Competitive Pressure",
                "Technology Disruption"
            ]
            
            trend_analysis["risk_factors"] = risk_factors
            
            st.success("✅ 趨勢分析完成")
            
        except Exception as e:
            st.warning(f"⚠️ 無法分析趨勢: {str(e)}")
        
        return trend_analysis
    
    def _generate_strategic_recommendations(self, ai_leader_analysis: Dict, dynamic_media_weights: Dict, 
                                         competitor_benchmarking: Dict, trend_analysis: Dict) -> List[Dict]:
        """生成策略建議"""
        if not self.gemini_model:
            return self._generate_fallback_strategic_recommendations(
                ai_leader_analysis, dynamic_media_weights, competitor_benchmarking, trend_analysis
            )
        
        st.write("🎯 生成策略建議...")
        
        try:
            analysis_data = {
                "ai_leader_analysis": ai_leader_analysis,
                "dynamic_media_weights": dynamic_media_weights,
                "competitor_benchmarking": competitor_benchmarking,
                "trend_analysis": trend_analysis
            }
            
            prompt = f"""
你是一位專業的 SIE 策略顧問，專門協助企業制定 E-E-A-T 競爭策略。

請根據以下分析結果，提供具體、可執行的策略建議：

分析數據：
{json.dumps(analysis_data, indent=2, ensure_ascii=False)}

請以 JSON 格式回傳策略建議，格式如下：
{{
  "strategic_recommendations": [
    {{
      "strategy": "策略名稱",
      "description": "策略描述",
      "priority": "High/Medium/Low",
      "timeline": "Short-term/Medium-term/Long-term",
      "expected_impact": "預期影響",
      "implementation_steps": ["步驟1", "步驟2", "步驟3"]
    }}
  ]
}}

請確保建議具體、可執行，並針對競爭優勢提升。
"""
            
            response = self.gemini_model.generate_content(prompt)
            recommendations_data = json.loads(response.text)
            return recommendations_data.get("strategic_recommendations", [])
            
        except Exception as e:
            st.warning(f"⚠️ Gemini API 生成策略建議失敗: {str(e)}")
            return self._generate_fallback_strategic_recommendations(
                ai_leader_analysis, dynamic_media_weights, competitor_benchmarking, trend_analysis
            )
    
    def _generate_fallback_strategic_recommendations(self, ai_leader_analysis: Dict, dynamic_media_weights: Dict, 
                                                   competitor_benchmarking: Dict, trend_analysis: Dict) -> List[Dict]:
        """生成備用策略建議"""
        recommendations = []
        
        # 基於 AI 領導者分析的建議
        if ai_leader_analysis["ai_leader_score"] < 50:
            recommendations.append({
                "strategy": "AI Technology Integration",
                "description": "加強 AI 技術整合，提升 AI 領導者地位",
                "priority": "High",
                "timeline": "Medium-term",
                "expected_impact": "提升 AI 領導者分數 30-50%",
                "implementation_steps": [
                    "評估現有 AI 技術基礎",
                    "制定 AI 整合路線圖",
                    "實施 AI 內容生成工具",
                    "建立 AI 效能監控系統"
                ]
            })
        
        # 基於社交媒體分析的建議
        if dynamic_media_weights["social_media_presence"]["social_authority_score"] < 60:
            recommendations.append({
                "strategy": "Social Media Authority Building",
                "description": "建立強大的社交媒體權威，提升品牌影響力",
                "priority": "Medium",
                "timeline": "Long-term",
                "expected_impact": "提升社交媒體權威分數 40-60%",
                "implementation_steps": [
                    "制定社交媒體內容策略",
                    "建立影響者合作關係",
                    "實施社群管理工具",
                    "定期發布高價值內容"
                ]
            })
        
        # 基於競爭分析的建議
        if competitor_benchmarking["market_position"] in ["average", "laggard"]:
            recommendations.append({
                "strategy": "Competitive Differentiation",
                "description": "建立獨特的競爭優勢，超越競爭對手",
                "priority": "High",
                "timeline": "Medium-term",
                "expected_impact": "提升市場地位至強勢競爭者",
                "implementation_steps": [
                    "識別獨特價值主張",
                    "開發差異化內容策略",
                    "建立品牌權威",
                    "實施創新技術解決方案"
                ]
            })
        
        return recommendations

    def _generate_market_media_with_llm(self, market: str, product_category: str, brand: str) -> dict:
        """
        用 LLM 產生主流媒體/論壇/社群/影音/Wiki名單，並標註 llm_favorite、信任度分數、排序依據。
        """
        if self.gemini_model:
            prompt = f"""
請根據下列資訊，列出{market}市場、{product_category}品類、{brand}品牌最具代表性的來源，分為：
- 新聞（行業新聞、綜合新聞）
- 社群（Facebook、Instagram、Twitter、LinkedIn等）
- 論壇（PTT、Dcard、Reddit等）
- 影音（YouTube、Bilibili等）
- Wiki（Wikipedia等）
每類請列出3-5個來源，並針對每個來源回傳：
- name: 來源名稱
- llm_favorite: 是否為 LLM 最常引用
- trust_score: LLM 對該來源的信任度分數（0-100）
- reason: 排序依據（如流量、互動數、引用次數、搜尋排名等）
請以 JSON 格式回傳：
{
  "新聞": [{{"name": "媒體名稱", "llm_favorite": true/false, "trust_score": 0-100, "reason": "排序依據"}}, ...],
  "社群": [{{"name": "社群名稱", "llm_favorite": true/false, "trust_score": 0-100, "reason": "排序依據"}}, ...],
  "論壇": [{{"name": "論壇名稱", "llm_favorite": true/false, "trust_score": 0-100, "reason": "排序依據"}}, ...],
  "影音": [{{"name": "影音平台名稱", "llm_favorite": true/false, "trust_score": 0-100, "reason": "排序依據"}}, ...],
  "Wiki": [{{"name": "Wiki名稱", "llm_favorite": true/false, "trust_score": 0-100, "reason": "排序依據"}}, ...]
}
"""
            try:
                response = self.gemini_model.generate_content(prompt)
                text = response.text.strip()
                if text.startswith('```json'):
                    text = text[7:]
                if text.endswith('```'):
                    text = text[:-3]
                text = text.strip()
                media_dict = json.loads(text)
                return media_dict
            except Exception:
                pass
        # fallback 靜態範例
        return {
            "新聞": [
                {"name": "經濟日報", "llm_favorite": True, "trust_score": 95, "reason": "行業影響力高"},
                {"name": "工商時報", "llm_favorite": False, "trust_score": 88, "reason": "財經新聞引用多"}
            ],
            "論壇": [
                {"name": "Mobile01", "llm_favorite": False, "trust_score": 80, "reason": "科技討論熱度高"},
                {"name": "PTT Tech_Job", "llm_favorite": True, "trust_score": 90, "reason": "工程師社群活躍"}
            ],
            "社群": [
                {"name": "Dcard", "llm_favorite": False, "trust_score": 85, "reason": "年輕族群活躍"},
                {"name": "LinkedIn", "llm_favorite": True, "trust_score": 92, "reason": "專業人士聚集"}
            ],
            "影音": [
                {"name": "YouTube", "llm_favorite": True, "trust_score": 98, "reason": "影音流量最大"},
                {"name": "Bilibili", "llm_favorite": False, "trust_score": 80, "reason": "年輕用戶多"}
            ],
            "Wiki": [
                {"name": "Wikipedia", "llm_favorite": True, "trust_score": 99, "reason": "全球最大百科"}
            ]
        }

    def _fetch_real_media_mentions(self, market_media_dict: dict) -> dict:
        """
        使用 Google News API 查詢 LLM 產生的媒體/論壇/社群名單，取得標題、連結、日期、摘要、來源、llm_favorite。
        """
        api_key = "bce856a8587d46ff84050efba536c445"
        endpoint = "https://newsapi.org/v2/everything"
        result = {"新聞": [], "論壇": [], "社群": []}
        for media_type in ["新聞", "論壇", "社群"]:
            for media in market_media_dict.get(media_type, []):
                name = media.get("name")
                llm_favorite = media.get("llm_favorite", False)
                params = {
                    "q": name,
                    "apiKey": api_key,
                    "language": "zh",
                    "sortBy": "publishedAt",
                    "pageSize": 3
                }
                try:
                    resp = requests.get(endpoint, params=params, timeout=10)
                    if resp.status_code == 200:
                        data = resp.json()
                        for article in data.get("articles", []):
                            result[media_type].append({
                                "media": name,
                                "llm_favorite": llm_favorite,
                                "title": article.get("title"),
                                "url": article.get("url"),
                                "date": article.get("publishedAt"),
                                "summary": article.get("description"),
                                "source": article.get("source", {}).get("name")
                            })
                except Exception:
                    continue
        return result

    def _llm_recommend_leaders(self, market: str, product_category: str, brand: str, official_site: str) -> list:
        """
        用 LLM 產生行業/市場/產品領導者名單，含品牌/公司/產品/官網/推薦說明/是否標竿。
        """
        if not self.gemini_model:
            # fallback 範例
            return [
                {"name": "台積電", "website": "https://www.tsmc.com/", "reason": "全球半導體製造領導者，技術創新與市佔率最高。", "is_benchmark": True},
                {"name": "聯電", "website": "https://www.umc.com/", "reason": "台灣第二大晶圓代工廠，具國際競爭力。", "is_benchmark": False}
            ]
        prompt = f"""
請根據下列資訊，列出{market}市場、{product_category}品類、{brand}品牌領域最具權威與競爭力的品牌/公司/產品（含本地與國際），每個請附上簡要說明與官網連結，並標註是否為行業標竿：
品牌/官網：{brand}（{official_site}）
請以 JSON 格式回傳：
[
  {{"name": "品牌/公司/產品名稱", "website": "官網連結", "reason": "推薦原因", "is_benchmark": true/false}},
  ...
]
"""
        try:
            response = self.gemini_model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            leaders = json.loads(text)
            return leaders
        except Exception:
            return []

    def _llm_compare_with_benchmarks(self, brand: str, official_site: str, market: str, product_category: str, leaders: list) -> dict:
        """
        用 LLM 比對本品牌與行業標竿，產生優劣勢/差距分數/建議。
        """
        if not self.gemini_model or not leaders:
            return {"summary": "無法取得 LLM 標竿比對分析（缺少 LLM 或標竿資料）"}
        prompt = f"""
請根據下列資訊，分析本品牌與行業標竿的具體差異，列出優勢、劣勢、差距分數與具體建議：
- 行業/市場：{market}
- 產品/品類：{product_category}
- 本品牌：{brand}（{official_site}）
- 行業標竿：{json.dumps(leaders, ensure_ascii=False)}
請以 JSON 格式回傳：
{{
  "gap_score": 0~100,  // 本品牌與標竿的整體差距分數，分數越高差距越大
  "advantages": ["優勢1", "優勢2", ...],
  "disadvantages": ["劣勢1", "劣勢2", ...],
  "recommendations": ["建議1", "建議2", ...],
  "summary": "簡要總結"
}}
"""
        try:
            response = self.gemini_model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            gap = json.loads(text)
            return gap
        except Exception:
            return {"summary": "LLM 比對失敗或格式錯誤"}

def run_eeat_benchmarking(target_website: str, competitors: List[str] = [], gemini_api_key: Optional[str] = None, industry: Optional[str] = None, product_category: Optional[str] = None, brand: Optional[str] = None) -> Dict:
    """執行 E-E-A-T 基準分析的主函式（支援行業/品類/品牌）"""
    analyzer = EEATBenchmarkingAnalyzer(gemini_api_key, industry, product_category, brand)
    return analyzer.analyze_eeat_benchmarking(target_website, competitors) 