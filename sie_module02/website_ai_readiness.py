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
    
    def analyze_website(self, website_url: str, product_category: str = None) -> Dict:
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
            
            # 4. 檢查產品品類權威性 (新增)
            product_authority = self._check_product_category_authority(website_url, product_category)
            
            # 5. 檢查 FAQ 與消費者問題解答 (新增)
            faq_analysis = self._check_faq_and_consumer_qa(website_url, product_category)
            
            # 6. 生成 AI 改善建議
            actionable_recommendations = self._generate_recommendations(
                root_files, architecture_signals, llm_friendliness, product_authority, faq_analysis
            )
            
            # 7. 生成 SEO 與 LLM 友善度改善建議 (新增)
            seo_llm_recommendations = self._generate_seo_llm_recommendations(
                website_url, root_files, architecture_signals, llm_friendliness, product_authority, faq_analysis
            )
            
            return {
                "technical_seo_ai_readiness": {
                    "root_files": root_files,
                    "architecture_signals": architecture_signals,
                    "llm_friendliness": llm_friendliness,
                    "product_authority": product_authority,
                    "faq_analysis": faq_analysis,
                    "actionable_recommendations": actionable_recommendations,
                    "seo_llm_recommendations": seo_llm_recommendations
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
            "structured_data_score": 0,
            "semantic_html": False,
            "content_hierarchy": "unknown"
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
                
                # 檢查語義化 HTML
                semantic_elements = soup.find_all(['article', 'section', 'nav', 'header', 'footer', 'main', 'aside'])
                llm_friendliness["semantic_html"] = len(semantic_elements) > 0
                
                if llm_friendliness["semantic_html"]:
                    st.success("✅ 使用語義化 HTML 標籤")
                else:
                    st.warning("⚠️ 未使用語義化 HTML 標籤")
                
                # 檢查內容層級結構
                h1_count = len(soup.find_all('h1'))
                h2_count = len(soup.find_all('h2'))
                h3_count = len(soup.find_all('h3'))
                
                if h1_count == 1 and h2_count > 0:
                    llm_friendliness["content_hierarchy"] = "good"
                    st.success("✅ 內容層級結構良好")
                elif h1_count > 0:
                    llm_friendliness["content_hierarchy"] = "fair"
                    st.info("ℹ️ 內容層級結構一般")
                else:
                    llm_friendliness["content_hierarchy"] = "poor"
                    st.warning("⚠️ 內容層級結構較差")
                
                # 模擬 PageSpeed 分數 (實際應用中應使用 Google PageSpeed Insights API)
                llm_friendliness["pagespeed_scores"] = {
                    "mobile": {"performance": 75, "lcp": 2.1, "cls": 0.05},
                    "desktop": {"performance": 92, "lcp": 1.5, "cls": 0.01}
                }
                
        except Exception as e:
            st.warning(f"⚠️ 無法分析 LLM 友善度: {str(e)}")
        
        return llm_friendliness
    
    def _check_product_category_authority(self, website_url: str, product_category: str = None) -> Dict:
        """檢查產品品類權威性"""
        st.write("🏆 檢查產品品類權威性...")
        
        product_authority = {
            "product_pages_found": 0,
            "product_info_completeness": "unknown",
            "technical_specs_available": False,
            "comparison_features": False,
            "expert_content": False,
            "authority_score": 0
        }
        
        if not product_category:
            st.info("ℹ️ 未指定產品品類，跳過產品權威性檢查")
            return product_authority
        
        try:
            response = self.session.get(website_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 搜尋產品相關頁面
                product_keywords = [product_category.lower()]
                
                # 根據產品品類添加相關關鍵字
                if product_category == "除濕機":
                    product_keywords.extend(["dehumidifier", "除濕", "乾燥", "濕度"])
                elif product_category == "冷氣":
                    product_keywords.extend(["air conditioner", "冷氣", "空調", "製冷"])
                elif product_category == "洗衣機":
                    product_keywords.extend(["washing machine", "洗衣", "洗滌"])
                elif product_category == "冰箱":
                    product_keywords.extend(["refrigerator", "冰箱", "冷藏", "冷凍"])
                elif product_category == "電視":
                    product_keywords.extend(["tv", "television", "電視", "顯示器"])
                elif product_category == "手機":
                    product_keywords.extend(["mobile", "phone", "smartphone", "手機", "智慧型手機"])
                elif product_category == "筆電":
                    product_keywords.extend(["laptop", "notebook", "筆電", "筆記型電腦"])
                elif product_category == "平板":
                    product_keywords.extend(["tablet", "ipad", "平板", "平板電腦"])
                elif product_category == "相機":
                    product_keywords.extend(["camera", "相機", "攝影", "拍照"])
                elif product_category == "音響":
                    product_keywords.extend(["speaker", "audio", "音響", "喇叭"])
                else:
                    # 對於其他產品，添加一些通用的產品相關關鍵字
                    product_keywords.extend(["產品", "product", "規格", "specification", "功能", "feature"])
                
                # 檢查產品頁面
                product_links = []
                for link in soup.find_all('a', href=True):
                    link_text = link.get_text().lower()
                    href = link['href'].lower()
                    
                    for keyword in product_keywords:
                        if keyword in link_text or keyword in href:
                            product_links.append(link)
                            break
                
                product_authority["product_pages_found"] = len(product_links)
                
                if product_links:
                    st.success(f"✅ 發現 {len(product_links)} 個產品相關頁面")
                    
                    # 檢查產品資訊完整性
                    page_text = soup.get_text().lower()
                    
                    # 檢查技術規格
                    tech_specs_keywords = ["規格", "specification", "技術", "technical", "參數", "parameter"]
                    if any(keyword in page_text for keyword in tech_specs_keywords):
                        product_authority["technical_specs_available"] = True
                        st.success("✅ 發現技術規格資訊")
                    
                    # 檢查比較功能
                    comparison_keywords = ["比較", "compare", "對比", "vs", "versus"]
                    if any(keyword in page_text for keyword in comparison_keywords):
                        product_authority["comparison_features"] = True
                        st.success("✅ 發現產品比較功能")
                    
                    # 檢查專家內容
                    expert_keywords = ["專家", "expert", "專業", "professional", "評測", "review"]
                    if any(keyword in page_text for keyword in expert_keywords):
                        product_authority["expert_content"] = True
                        st.success("✅ 發現專家內容")
                    
                    # 計算權威分數
                    score = 0
                    score += len(product_links) * 10
                    if product_authority["technical_specs_available"]:
                        score += 20
                    if product_authority["comparison_features"]:
                        score += 15
                    if product_authority["expert_content"]:
                        score += 15
                    
                    product_authority["authority_score"] = min(score, 100)
                    
                    if score >= 60:
                        product_authority["product_info_completeness"] = "excellent"
                    elif score >= 40:
                        product_authority["product_info_completeness"] = "good"
                    elif score >= 20:
                        product_authority["product_info_completeness"] = "fair"
                    else:
                        product_authority["product_info_completeness"] = "poor"
                        
                else:
                    st.warning(f"⚠️ 未發現 {product_category} 相關產品頁面")
                    
        except Exception as e:
            st.warning(f"⚠️ 無法分析產品權威性: {str(e)}")
        
        return product_authority
    
    def _check_faq_and_consumer_qa(self, website_url: str, product_category: str = None) -> Dict:
        """檢查 FAQ 與消費者問題解答"""
        st.write("❓ 檢查 FAQ 與消費者問題解答...")
        
        faq_analysis = {
            "faq_section_found": False,
            "faq_count": 0,
            "product_specific_qa": False,
            "common_questions_covered": False,
            "qa_content_quality": "unknown",
            "qa_score": 0
        }
        
        try:
            response = self.session.get(website_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 搜尋 FAQ 相關元素
                faq_keywords = ["faq", "常見問題", "frequently asked", "q&a", "問答"]
                faq_elements = []
                
                # 檢查標題中的 FAQ
                for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                    heading_text = heading.get_text().lower()
                    if any(keyword in heading_text for keyword in faq_keywords):
                        faq_elements.append(heading)
                
                # 檢查 FAQ 區塊
                faq_sections = soup.find_all(['div', 'section'], class_=re.compile(r'faq|question|answer', re.I))
                faq_elements.extend(faq_sections)
                
                if faq_elements:
                    faq_analysis["faq_section_found"] = True
                    faq_analysis["faq_count"] = len(faq_elements)
                    st.success(f"✅ 發現 FAQ 區塊，包含 {len(faq_elements)} 個問題")
                    
                    # 檢查產品特定問題
                    if product_category:
                        page_text = soup.get_text().lower()
                        product_keywords = [product_category.lower()]
                        
                        # 根據產品品類添加相關關鍵字
                        if product_category == "除濕機":
                            product_keywords.extend(["除濕", "濕度", "乾燥", "冷凝"])
                        elif product_category == "冷氣":
                            product_keywords.extend(["冷氣", "空調", "製冷", "溫度"])
                        elif product_category == "洗衣機":
                            product_keywords.extend(["洗衣", "洗滌", "清潔"])
                        elif product_category == "冰箱":
                            product_keywords.extend(["冰箱", "冷藏", "冷凍", "保鮮"])
                        elif product_category == "電視":
                            product_keywords.extend(["電視", "顯示器", "螢幕"])
                        elif product_category == "手機":
                            product_keywords.extend(["手機", "智慧型手機", "通話", "app"])
                        elif product_category == "筆電":
                            product_keywords.extend(["筆電", "筆記型電腦", "電腦", "處理器"])
                        elif product_category == "平板":
                            product_keywords.extend(["平板", "平板電腦", "觸控"])
                        elif product_category == "相機":
                            product_keywords.extend(["相機", "攝影", "拍照", "鏡頭"])
                        elif product_category == "音響":
                            product_keywords.extend(["音響", "喇叭", "音樂", "音質"])
                        else:
                            # 對於其他產品，添加一些通用的產品相關關鍵字
                            product_keywords.extend(["產品", "使用", "功能", "問題"])
                        
                        if any(keyword in page_text for keyword in product_keywords):
                            faq_analysis["product_specific_qa"] = True
                            st.success("✅ 發現產品特定問題解答")
                    
                    # 檢查常見問題覆蓋度
                    common_questions = [
                        "如何", "怎麼", "為什麼", "什麼時候", "哪裡", "多少錢",
                        "how", "why", "when", "where", "what", "price", "cost"
                    ]
                    
                    question_count = 0
                    for element in faq_elements:
                        element_text = element.get_text().lower()
                        for question in common_questions:
                            if question in element_text:
                                question_count += 1
                                break
                    
                    if question_count >= 3:
                        faq_analysis["common_questions_covered"] = True
                        st.success("✅ 覆蓋多個常見問題類型")
                    
                    # 評估 QA 內容品質
                    score = 0
                    score += len(faq_elements) * 5
                    if faq_analysis["product_specific_qa"]:
                        score += 20
                    if faq_analysis["common_questions_covered"]:
                        score += 15
                    
                    faq_analysis["qa_score"] = min(score, 100)
                    
                    if score >= 50:
                        faq_analysis["qa_content_quality"] = "excellent"
                    elif score >= 30:
                        faq_analysis["qa_content_quality"] = "good"
                    elif score >= 15:
                        faq_analysis["qa_content_quality"] = "fair"
                    else:
                        faq_analysis["qa_content_quality"] = "poor"
                        
                else:
                    st.warning("⚠️ 未發現 FAQ 區塊")
                    
        except Exception as e:
            st.warning(f"⚠️ 無法分析 FAQ: {str(e)}")
        
        return faq_analysis
    
    def _generate_recommendations(self, root_files: Dict, architecture_signals: Dict, 
                                llm_friendliness: Dict, product_authority: Dict, faq_analysis: Dict) -> List[Dict]:
        """使用 Gemini API 生成改善建議"""
        if not self.gemini_model:
            return self._generate_fallback_recommendations(
                root_files, architecture_signals, llm_friendliness, product_authority, faq_analysis
            )
        
        st.write("🤖 生成 AI 改善建議...")
        
        try:
            # 準備分析數據
            analysis_data = {
                "root_files": root_files,
                "architecture_signals": architecture_signals,
                "llm_friendliness": llm_friendliness,
                "product_authority": product_authority,
                "faq_analysis": faq_analysis
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
      "category": "Root Files/Architecture/LLM Friendliness/Product Authority/FAQ"
    }}
  ]
}}

請確保建議具體、可執行，並針對 AI 就緒度優化。
請只回傳 JSON 格式，不要包含其他文字。
"""
            
            response = self.gemini_model.generate_content(prompt)
            
            # 嘗試解析 JSON 回應
            try:
                # 清理回應文字，移除可能的 markdown 格式
                response_text = response.text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                
                recommendations_data = json.loads(response_text)
                return recommendations_data.get("recommendations", [])
                
            except json.JSONDecodeError as json_error:
                st.warning(f"⚠️ Gemini API 回應格式錯誤: {str(json_error)}")
                st.info("使用備用建議生成...")
                return self._generate_fallback_recommendations(
                    root_files, architecture_signals, llm_friendliness, product_authority, faq_analysis
                )
            
        except Exception as e:
            st.warning(f"⚠️ Gemini API 生成建議失敗: {str(e)}")
            st.info("使用備用建議生成...")
            return self._generate_fallback_recommendations(
                root_files, architecture_signals, llm_friendliness, product_authority, faq_analysis
            )
    
    def _generate_fallback_recommendations(self, root_files: Dict, architecture_signals: Dict, 
                                         llm_friendliness: Dict, product_authority: Dict, faq_analysis: Dict) -> List[Dict]:
        """生成備用改善建議（當 Gemini API 不可用時）"""
        recommendations = []
        
        # Root Files 建議
        if not root_files["has_robots_txt"]:
            recommendations.append({
                "issue": "缺少 robots.txt 檔案",
                "recommendation": "請在網站根目錄建立 robots.txt 檔案，這是網站與搜尋引擎和 AI 機器人溝通的重要檔案。\n\n建議內容：\n```\nUser-agent: *\nAllow: /\nUser-agent: Google-Extended\nAllow: /\nUser-agent: GPTBot\nAllow: /\nUser-agent: anthropic-ai\nAllow: /\n\nSitemap: https://yourdomain.com/sitemap.xml\n```\n\n這將確保所有搜尋引擎和 AI 機器人都能正確存取您的網站內容。",
                "priority": "High",
                "category": "Root Files"
            })
        
        if not root_files["robots_allows_ai_bots"]:
            recommendations.append({
                "issue": "robots.txt 封鎖 AI 機器人",
                "recommendation": "請修改 robots.txt，確保允許 Google-Extended 與 GPTBot 等 AI User-Agent 進行存取。建議添加：User-agent: Google-Extended 和 Allow: /。",
                "priority": "High",
                "category": "Root Files"
            })
        
        if not root_files["has_sitemap_xml"]:
            recommendations.append({
                "issue": "缺少 sitemap.xml 檔案",
                "recommendation": "請建立 sitemap.xml 檔案，這是幫助搜尋引擎和 AI 理解網站結構的重要檔案。\n\n建議內容結構：\n```xml\n<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n  <url>\n    <loc>https://yourdomain.com/</loc>\n    <lastmod>2024-01-01</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>\n  <url>\n    <loc>https://yourdomain.com/products</loc>\n    <lastmod>2024-01-01</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>\n```\n\n包含所有重要頁面，並定期更新以反映最新內容。",
                "priority": "Medium",
                "category": "Root Files"
            })
        
        if not root_files["sitemap_is_valid"]:
            recommendations.append({
                "issue": "sitemap.xml 格式錯誤",
                "recommendation": "請檢查 sitemap.xml 檔案格式，確保符合 XML 標準，包含正確的 URL 結構。",
                "priority": "Medium",
                "category": "Root Files"
            })
        
        # Architecture 建議
        if not architecture_signals["uses_https"]:
            recommendations.append({
                "issue": "未使用 HTTPS 加密",
                "recommendation": "請啟用 HTTPS 加密連線，這對網站安全性和搜尋引擎排名都很重要。可以透過 SSL 憑證提供商或 CDN 服務實現。",
                "priority": "High",
                "category": "Architecture"
            })
        
        if architecture_signals["internal_link_structure"] == "poor":
            recommendations.append({
                "issue": "內部連結結構較差",
                "recommendation": "請改善網站內部連結結構，確保主要頁面都有清晰的導航連結，這有助於 AI 理解網站內容關聯性。",
                "priority": "Medium",
                "category": "Architecture"
            })
        
        # LLM Friendliness 建議
        if not llm_friendliness["schema_detected"]:
            recommendations.append({
                "issue": "缺少結構化資料",
                "recommendation": "請為網站添加 Schema.org 結構化資料，這對 AI 理解內容語義至關重要。建議實施以下標記：\n\n1. **組織標記 (Organization)**：包含公司名稱、logo、聯絡資訊\n2. **產品標記 (Product)**：包含產品名稱、描述、價格、規格\n3. **文章標記 (Article)**：包含標題、作者、發布日期\n4. **FAQ 標記 (FAQPage)**：包含問題和答案\n5. **麵包屑標記 (BreadcrumbList)**：顯示頁面層級結構\n\n實施方式：在 HTML 的 <head> 區塊中添加 <script type=\"application/ld+json\"> 標籤，包含結構化資料 JSON。這將大幅提升 AI 對網站內容的理解能力。",
                "priority": "Medium",
                "category": "LLM Friendliness"
            })
        
        if llm_friendliness["content_readability"] == "poor":
            recommendations.append({
                "issue": "內容結構較差",
                "recommendation": "請改善內容結構，使用清晰的標題層級（H1, H2, H3）組織內容，確保內容邏輯清晰，便於 AI 理解。",
                "priority": "Medium",
                "category": "LLM Friendliness"
            })
        
        if not llm_friendliness["semantic_html"]:
            recommendations.append({
                "issue": "未使用語義化 HTML",
                "recommendation": "請使用語義化 HTML 標籤，這對 AI 理解內容結構至關重要。\n\n建議使用的標籤：\n- **<header>**：頁面或區塊的標題區域\n- **<nav>**：導航選單\n- **<main>**：主要內容區域\n- **<article>**：獨立的文章或產品內容\n- **<section>**：內容區塊\n- **<aside>**：側邊欄或相關內容\n- **<footer>**：頁面底部\n\n範例結構：\n```html\n<header>\n  <nav>導航選單</nav>\n</header>\n<main>\n  <article>\n    <section>產品介紹</section>\n    <section>技術規格</section>\n  </article>\n  <aside>相關產品</aside>\n</main>\n<footer>聯絡資訊</footer>\n```\n\n這將大幅提升 AI 對網站結構的理解能力。",
                "priority": "Medium",
                "category": "LLM Friendliness"
            })
        
        if llm_friendliness["content_hierarchy"] == "poor":
            recommendations.append({
                "issue": "內容層級結構較差",
                "recommendation": "請改善內容層級結構，確保每個頁面有且僅有一個 H1 標題，並使用 H2、H3 等建立清晰的內容層級。",
                "priority": "Medium",
                "category": "LLM Friendliness"
            })
        
        # Product Authority 建議
        if product_authority["product_info_completeness"] in ["poor", "fair"]:
            recommendations.append({
                "issue": "產品資訊不完整",
                "recommendation": "請完善產品資訊，包含詳細的技術規格、產品比較功能、專家評測、使用指南等內容，提升產品權威性。",
                "priority": "Medium",
                "category": "Product Authority"
            })
        
        if product_authority["product_pages_found"] == 0:
            recommendations.append({
                "issue": "未發現產品相關頁面",
                "recommendation": "請建立專門的產品頁面，包含產品介紹、規格、功能說明等內容，幫助消費者了解產品特性。",
                "priority": "High",
                "category": "Product Authority"
            })
        
        if not product_authority["technical_specs_available"]:
            recommendations.append({
                "issue": "缺少技術規格資訊",
                "recommendation": "請為產品提供詳細的技術規格和參數，包括尺寸、重量、功率、功能特點等，提升產品資訊的專業性。",
                "priority": "Medium",
                "category": "Product Authority"
            })
        
        # FAQ 建議
        if not faq_analysis["faq_section_found"]:
            recommendations.append({
                "issue": "缺少 FAQ 區塊",
                "recommendation": "請建立 FAQ 區塊，回答消費者常見問題，這不僅能提升用戶體驗，也能增加網站內容的權威性。",
                "priority": "Medium",
                "category": "FAQ"
            })
        
        if faq_analysis["qa_content_quality"] in ["poor", "fair"]:
            recommendations.append({
                "issue": "FAQ 內容品質較差",
                "recommendation": "請改善 FAQ 內容品質，包含產品特定問題、使用問題、常見問題等，確保回答詳細且實用。",
                "priority": "Medium",
                "category": "FAQ"
            })
        
        if not faq_analysis["product_specific_qa"]:
            recommendations.append({
                "issue": "缺少產品特定問題解答",
                "recommendation": "請在 FAQ 中包含產品特定的問題和解答，幫助消費者更好地了解產品使用方法和注意事項。",
                "priority": "Medium",
                "category": "FAQ"
            })
        
        # 如果沒有發現任何問題，提供一般性建議
        if not recommendations:
            recommendations.append({
                "issue": "網站基礎良好",
                "recommendation": "您的網站基礎架構良好！建議持續監控 AI 就緒度指標，並考慮建立 llms.txt 檔案以適應未來 AI 搜尋需求。",
                "priority": "Low",
                "category": "General"
            })
        
        return recommendations
    
    def _generate_seo_llm_recommendations(self, website_url: str, root_files: Dict, architecture_signals: Dict,
                                        llm_friendliness: Dict, product_authority: Dict, faq_analysis: Dict) -> List[Dict]:
        """生成 SEO 與 LLM 友善度改善建議"""
        st.write("🎯 生成 SEO 與 LLM 友善度建議...")
        
        seo_llm_recommendations = []
        
        # SEO 基礎建議
        seo_llm_recommendations.append({
            "category": "SEO 基礎優化",
            "recommendations": [
                "建立完整的 XML Sitemap，包含所有重要頁面",
                "優化 robots.txt，確保搜尋引擎和 AI 機器人正確存取",
                "實施 HTTPS 加密，提升安全性和信任度",
                "改善網站載入速度，優化 Core Web Vitals 指標"
            ]
        })
        
        # 內容結構建議
        content_recommendations = []
        if llm_friendliness["content_readability"] != "good":
            content_recommendations.append("使用清晰的標題層級結構（H1 > H2 > H3）")
        if not llm_friendliness["semantic_html"]:
            content_recommendations.append("實施語義化 HTML 標籤")
        if not llm_friendliness["schema_detected"]:
            content_recommendations.append("添加 Schema.org 結構化資料")
        
        if content_recommendations:
            seo_llm_recommendations.append({
                "category": "內容結構優化",
                "recommendations": content_recommendations
            })
        
        # LLM 友善度建議
        llm_recommendations = [
            "建立 llms.txt 檔案，明確告知 AI 模型如何處理網站內容",
            "使用自然語言撰寫內容，避免過度優化關鍵字",
            "提供完整的產品資訊和技術規格",
            "建立 FAQ 區塊，回答消費者常見問題",
            "使用內部連結建立內容關聯性",
            "確保內容的可讀性和可理解性"
        ]
        
        seo_llm_recommendations.append({
            "category": "LLM 友善度優化",
            "recommendations": llm_recommendations
        })
        
        # 產品權威性建議
        if product_authority["product_info_completeness"] in ["poor", "fair"]:
            seo_llm_recommendations.append({
                "category": "產品權威性建立",
                "recommendations": [
                    "提供詳細的產品技術規格和參數",
                    "建立產品比較功能，幫助消費者選擇",
                    "發布專家評測和使用指南",
                    "建立產品使用教學和維護指南",
                    "提供產品相關的專業知識內容"
                ]
            })
        
        # 未來 LLM 收錄建議
        seo_llm_recommendations.append({
            "category": "未來 LLM 收錄準備",
            "recommendations": [
                "建立完整的產品知識庫",
                "提供結構化的產品資訊",
                "使用標準化的內容格式",
                "建立內容更新機制",
                "監控 AI 模型對內容的存取和使用情況",
                "準備適應未來 AI 搜尋演算法的內容策略"
            ]
        })
        
        return seo_llm_recommendations

def run_website_analysis(website_url: str, product_category: Optional[str] = None, gemini_api_key: Optional[str] = None) -> Dict:
    """執行網站 AI 就緒度分析的主函式"""
    analyzer = WebsiteAIReadinessAnalyzer(gemini_api_key)
    return analyzer.analyze_website(website_url, product_category) 