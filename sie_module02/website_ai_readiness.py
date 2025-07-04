import requests
import json
import time
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import os
from typing import Dict, List, Optional, Tuple
import streamlit as st

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("警告: google-generativeai 未安裝，Gemini API 功能將無法使用")

class WebsiteAIReadinessAnalyzer:
    """網站 AI 就緒度與技術健康度分析器"""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SIE-Diagnostic-Tool/1.0 (contact@example.com)'
        })
        
        # 初始化 Gemini API
        if gemini_api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.gemini_model = None
    
    def analyze_website(self, website_url: str) -> Dict:
        """分析網站的 AI 就緒度與技術健康度"""
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        st.info(f"🔍 正在分析網站: {website_url}")
        
        try:
            # 1. 檢查根檔案與 LLM 遵從性
            root_files = self._check_root_files(website_url)
            
            # 2. 檢查網站架構與權威信號
            architecture_signals = self._check_architecture_signals(website_url)
            
            # 3. 檢查 LLM 友善度指標
            llm_friendliness = self._check_llm_friendliness(website_url)
            
            # 4. 生成 AI 改善建議
            actionable_recommendations = self._generate_recommendations(
                root_files, architecture_signals, llm_friendliness
            )
            
            return {
                "technical_seo_ai_readiness": {
                    "root_files": root_files,
                    "architecture_signals": architecture_signals,
                    "llm_friendliness": llm_friendliness,
                    "actionable_recommendations": actionable_recommendations
                }
            }
            
        except Exception as e:
            st.error(f"分析過程中發生錯誤: {str(e)}")
            return {"error": str(e)}
    
    def _check_root_files(self, website_url: str) -> Dict:
        """檢查根檔案與 LLM 遵從性"""
        st.write("📁 檢查根檔案...")
        
        root_files = {
            "has_robots_txt": False,
            "robots_allows_ai_bots": False,
            "has_sitemap_xml": False,
            "sitemap_is_valid": False,
            "has_llms_txt": False,
            "llms_txt_content": None
        }
        
        # 檢查 robots.txt
        try:
            robots_url = urljoin(website_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200:
                root_files["has_robots_txt"] = True
                robots_content = response.text.lower()
                
                # 檢查是否允許 AI bots
                ai_bots = ['google-extended', 'gptbot', 'anthropic-ai', 'claude-ai']
                blocked_ai_bots = []
                for bot in ai_bots:
                    if f'user-agent: {bot}' in robots_content and 'disallow: /' in robots_content:
                        blocked_ai_bots.append(bot)
                
                root_files["robots_allows_ai_bots"] = len(blocked_ai_bots) == 0
                if blocked_ai_bots:
                    st.warning(f"⚠️ robots.txt 封鎖了 AI bots: {', '.join(blocked_ai_bots)}")
                else:
                    st.success("✅ robots.txt 允許 AI bots 存取")
        except Exception as e:
            st.warning(f"⚠️ 無法讀取 robots.txt: {str(e)}")
        
        # 檢查 sitemap.xml
        try:
            sitemap_url = urljoin(website_url, '/sitemap.xml')
            response = self.session.get(sitemap_url, timeout=10)
            if response.status_code == 200:
                root_files["has_sitemap_xml"] = True
                # 簡單驗證 XML 格式
                if '<?xml' in response.text and '<urlset' in response.text:
                    root_files["sitemap_is_valid"] = True
                    st.success("✅ sitemap.xml 存在且格式正確")
                else:
                    st.warning("⚠️ sitemap.xml 格式可能有問題")
        except Exception as e:
            st.warning(f"⚠️ 無法讀取 sitemap.xml: {str(e)}")
        
        # 檢查 llms.txt (前瞻性指標)
        try:
            llms_url = urljoin(website_url, '/llms.txt')
            response = self.session.get(llms_url, timeout=10)
            if response.status_code == 200:
                root_files["has_llms_txt"] = True
                root_files["llms_txt_content"] = response.text
                st.success("✅ llms.txt 存在 (前瞻性指標)")
        except Exception as e:
            st.info("ℹ️ llms.txt 不存在 (這是正常的，目前仍是新興標準)")
        
        return root_files
    
    def _check_architecture_signals(self, website_url: str) -> Dict:
        """檢查網站架構與權威信號"""
        st.write("🏗️ 檢查網站架構...")
        
        architecture_signals = {
            "uses_https": False,
            "estimated_authority_links": 0,
            "internal_link_structure": "unknown",
            "external_links_count": 0
        }
        
        # 檢查 HTTPS
        if website_url.startswith('https://'):
            architecture_signals["uses_https"] = True
            st.success("✅ 網站使用 HTTPS")
        else:
            st.warning("⚠️ 網站未使用 HTTPS")
        
        # 檢查內部連結結構
        try:
            response = self.session.get(website_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 檢查導航連結
                nav_links = soup.find_all('a', href=True)
                internal_links = [link for link in nav_links if link['href'].startswith('/') or website_url in link['href']]
                
                if len(internal_links) >= 5:
                    architecture_signals["internal_link_structure"] = "good"
                    st.success("✅ 內部連結結構良好")
                elif len(internal_links) >= 2:
                    architecture_signals["internal_link_structure"] = "fair"
                    st.info("ℹ️ 內部連結結構一般")
                else:
                    architecture_signals["internal_link_structure"] = "poor"
                    st.warning("⚠️ 內部連結結構較差")
                
                # 估算外部權威連結 (模擬)
                architecture_signals["estimated_authority_links"] = len(nav_links) // 10
                architecture_signals["external_links_count"] = len([link for link in nav_links if not link['href'].startswith('/') and website_url not in link['href']])
                
        except Exception as e:
            st.warning(f"⚠️ 無法分析網站架構: {str(e)}")
        
        return architecture_signals
    
    def _check_llm_friendliness(self, website_url: str) -> Dict:
        """檢查 LLM 友善度指標"""
        st.write("🤖 檢查 LLM 友善度...")
        
        llm_friendliness = {
            "schema_detected": [],
            "pagespeed_scores": {
                "mobile": {"performance": 0, "lcp": 0, "cls": 0},
                "desktop": {"performance": 0, "lcp": 0, "cls": 0}
            },
            "content_readability": "unknown",
            "structured_data_score": 0
        }
        
        try:
            response = self.session.get(website_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 檢查 Schema.org 結構化資料
                schema_scripts = soup.find_all('script', type='application/ld+json')
                schema_types = []
                for script in schema_scripts:
                    try:
                        schema_data = json.loads(script.string)
                        if isinstance(schema_data, dict):
                            schema_type = schema_data.get('@type', 'Unknown')
                            schema_types.append(schema_type)
                    except:
                        continue
                
                llm_friendliness["schema_detected"] = list(set(schema_types))
                llm_friendliness["structured_data_score"] = len(schema_types)
                
                if schema_types:
                    st.success(f"✅ 發現結構化資料: {', '.join(schema_types)}")
                else:
                    st.warning("⚠️ 未發現結構化資料")
                
                # 檢查內容可讀性
                headings = soup.find_all(['h1', 'h2', 'h3'])
                paragraphs = soup.find_all('p')
                
                if len(headings) >= 3 and len(paragraphs) >= 5:
                    llm_friendliness["content_readability"] = "good"
                    st.success("✅ 內容結構良好，有清晰的標題層級")
                elif len(headings) >= 1 and len(paragraphs) >= 2:
                    llm_friendliness["content_readability"] = "fair"
                    st.info("ℹ️ 內容結構一般")
                else:
                    llm_friendliness["content_readability"] = "poor"
                    st.warning("⚠️ 內容結構較差，缺乏清晰的標題層級")
                
                # 模擬 PageSpeed 分數 (實際應用中應使用 Google PageSpeed Insights API)
                llm_friendliness["pagespeed_scores"] = {
                    "mobile": {"performance": 75, "lcp": 2.1, "cls": 0.05},
                    "desktop": {"performance": 92, "lcp": 1.5, "cls": 0.01}
                }
                
        except Exception as e:
            st.warning(f"⚠️ 無法分析 LLM 友善度: {str(e)}")
        
        return llm_friendliness
    
    def _generate_recommendations(self, root_files: Dict, architecture_signals: Dict, llm_friendliness: Dict) -> List[Dict]:
        """使用 Gemini API 生成改善建議"""
        if not self.gemini_model:
            return self._generate_fallback_recommendations(root_files, architecture_signals, llm_friendliness)
        
        st.write("🤖 生成 AI 改善建議...")
        
        try:
            # 準備分析數據
            analysis_data = {
                "root_files": root_files,
                "architecture_signals": architecture_signals,
                "llm_friendliness": llm_friendliness
            }
            
            prompt = f"""
你是一位專業的 SIE 技術顧問，專門協助企業優化網站以提升 AI 就緒度。

請根據以下網站分析結果，提供具體、可執行的改善建議：

分析數據：
{json.dumps(analysis_data, indent=2, ensure_ascii=False)}

請以 JSON 格式回傳改善建議，格式如下：
{{
  "recommendations": [
    {{
      "issue": "問題描述",
      "recommendation": "具體改善建議",
      "priority": "High/Medium/Low",
      "category": "Root Files/Architecture/LLM Friendliness"
    }}
  ]
}}

請確保建議具體、可執行，並針對 AI 就緒度優化。
"""
            
            response = self.gemini_model.generate_content(prompt)
            recommendations_data = json.loads(response.text)
            return recommendations_data.get("recommendations", [])
            
        except Exception as e:
            st.warning(f"⚠️ Gemini API 生成建議失敗: {str(e)}")
            return self._generate_fallback_recommendations(root_files, architecture_signals, llm_friendliness)
    
    def _generate_fallback_recommendations(self, root_files: Dict, architecture_signals: Dict, llm_friendliness: Dict) -> List[Dict]:
        """生成備用改善建議（當 Gemini API 不可用時）"""
        recommendations = []
        
        # Root Files 建議
        if not root_files["has_robots_txt"]:
            recommendations.append({
                "issue": "Missing robots.txt",
                "recommendation": "請在網站根目錄建立 robots.txt 檔案，以正確引導搜尋引擎和 AI 機器人。",
                "priority": "High",
                "category": "Root Files"
            })
        
        if not root_files["robots_allows_ai_bots"]:
            recommendations.append({
                "issue": "AI Bot Crawling Blocked",
                "recommendation": "請修改 robots.txt，確保允許 Google-Extended 與 GPTBot 等 AI User-Agent 進行存取。",
                "priority": "High",
                "category": "Root Files"
            })
        
        if not root_files["has_sitemap_xml"]:
            recommendations.append({
                "issue": "Missing sitemap.xml",
                "recommendation": "請建立 sitemap.xml 檔案，幫助搜尋引擎和 AI 更好地理解網站結構。",
                "priority": "Medium",
                "category": "Root Files"
            })
        
        # Architecture 建議
        if not architecture_signals["uses_https"]:
            recommendations.append({
                "issue": "No HTTPS",
                "recommendation": "請啟用 HTTPS 加密連線，提升網站安全性和信任度。",
                "priority": "High",
                "category": "Architecture"
            })
        
        if architecture_signals["internal_link_structure"] == "poor":
            recommendations.append({
                "issue": "Poor Internal Link Structure",
                "recommendation": "請改善網站內部連結結構，確保主要頁面都有清晰的導航連結。",
                "priority": "Medium",
                "category": "Architecture"
            })
        
        # LLM Friendliness 建議
        if not llm_friendliness["schema_detected"]:
            recommendations.append({
                "issue": "Missing Structured Data",
                "recommendation": "請為網站添加 Schema.org 結構化資料，幫助 AI 更好地理解內容。",
                "priority": "Medium",
                "category": "LLM Friendliness"
            })
        
        if llm_friendliness["content_readability"] == "poor":
            recommendations.append({
                "issue": "Poor Content Structure",
                "recommendation": "請改善內容結構，使用清晰的標題層級（H1, H2, H3）組織內容。",
                "priority": "Medium",
                "category": "LLM Friendliness"
            })
        
        return recommendations

def run_website_analysis(website_url: str, gemini_api_key: Optional[str] = None) -> Dict:
    """執行網站 AI 就緒度分析的主函式"""
    analyzer = WebsiteAIReadinessAnalyzer(gemini_api_key)
    return analyzer.analyze_website(website_url) 