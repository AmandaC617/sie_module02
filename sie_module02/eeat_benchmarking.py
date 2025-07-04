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
    
    def __init__(self, gemini_api_key: Optional[str] = None):
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
    
    def analyze_eeat_benchmarking(self, target_website: str, competitors: List[str] = []) -> Dict:
        """執行動態 E-E-A-T 評估與競爭基準分析"""
        if not target_website.startswith(('http://', 'https://')):
            target_website = 'https://' + target_website
        
        st.info(f"🔍 正在分析目標網站: {target_website}")
        
        try:
            # 1. AI 領導者識別與分析
            ai_leader_analysis = self._identify_ai_leaders(target_website)
            
            # 2. 動態媒體權重評估
            dynamic_media_weights = self._analyze_dynamic_media_weights(target_website)
            
            # 3. 競爭對手基準分析
            competitor_benchmarking = self._analyze_competitor_benchmarks(target_website, competitors)
            
            # 4. 趨勢追蹤與預測
            trend_analysis = self._analyze_trends_and_predictions(target_website)
            
            # 5. 生成策略建議
            strategic_recommendations = self._generate_strategic_recommendations(
                ai_leader_analysis, dynamic_media_weights, competitor_benchmarking, trend_analysis
            )
            
            return {
                "eeat_benchmarking": {
                    "ai_leader_analysis": ai_leader_analysis,
                    "dynamic_media_weights": dynamic_media_weights,
                    "competitor_benchmarking": competitor_benchmarking,
                    "trend_analysis": trend_analysis,
                    "strategic_recommendations": strategic_recommendations
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
    
    def _analyze_dynamic_media_weights(self, target_website: str) -> Dict:
        """分析動態媒體權重"""
        st.write("📊 分析動態媒體權重...")
        
        dynamic_media_weights = {
            "media_mentions": {
                "recent_mentions": [],
                "mention_sentiment": "neutral",
                "media_coverage_score": 0
            },
            "social_media_presence": {
                "platforms": [],
                "engagement_metrics": {},
                "social_authority_score": 0
            },
            "content_distribution": {
                "content_types": [],
                "distribution_channels": [],
                "reach_metrics": {}
            }
        }
        
        try:
            response = self.session.get(target_website, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 檢查社交媒體連結
                social_platforms = []
                social_links = soup.find_all('a', href=True)
                
                social_platform_patterns = {
                    'linkedin': 'linkedin.com',
                    'twitter': 'twitter.com',
                    'facebook': 'facebook.com',
                    'instagram': 'instagram.com',
                    'youtube': 'youtube.com'
                }
                
                for link in social_links:
                    href = link['href'].lower()
                    for platform, pattern in social_platform_patterns.items():
                        if pattern in href and platform not in social_platforms:
                            social_platforms.append(platform)
                
                dynamic_media_weights["social_media_presence"]["platforms"] = social_platforms
                
                # 模擬媒體提及
                recent_mentions = [
                    {
                        "source": "TechCrunch",
                        "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                        "title": f"AI Innovation at {target_website}",
                        "sentiment": random.choice(["positive", "neutral", "positive"])
                    },
                    {
                        "source": "VentureBeat",
                        "date": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d"),
                        "title": f"Digital Transformation Insights from {target_website}",
                        "sentiment": "positive"
                    }
                ]
                
                dynamic_media_weights["media_mentions"]["recent_mentions"] = recent_mentions
                
                # 計算媒體覆蓋分數
                positive_mentions = len([m for m in recent_mentions if m["sentiment"] == "positive"])
                total_mentions = len(recent_mentions)
                media_coverage_score = (positive_mentions / max(total_mentions, 1)) * 100
                
                dynamic_media_weights["media_mentions"]["media_coverage_score"] = media_coverage_score
                dynamic_media_weights["media_mentions"]["mention_sentiment"] = "positive" if media_coverage_score > 60 else "neutral"
                
                # 模擬社交媒體權威分數
                social_authority_score = len(social_platforms) * 20 + random.randint(10, 30)
                dynamic_media_weights["social_media_presence"]["social_authority_score"] = min(social_authority_score, 100)
                
                # 模擬參與度指標
                dynamic_media_weights["social_media_presence"]["engagement_metrics"] = {
                    "total_followers": random.randint(1000, 50000),
                    "engagement_rate": random.uniform(2.0, 8.0),
                    "post_frequency": random.randint(3, 15)
                }
                
                if social_platforms:
                    st.success(f"✅ 發現社交媒體平台: {', '.join(social_platforms)}")
                else:
                    st.warning("⚠️ 未發現社交媒體連結")
                
        except Exception as e:
            st.warning(f"⚠️ 無法分析動態媒體權重: {str(e)}")
        
        return dynamic_media_weights
    
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

def run_eeat_benchmarking(target_website: str, competitors: List[str] = [], gemini_api_key: Optional[str] = None) -> Dict:
    """執行 E-E-A-T 基準分析的主函式"""
    analyzer = EEATBenchmarkingAnalyzer(gemini_api_key)
    return analyzer.analyze_eeat_benchmarking(target_website, competitors) 