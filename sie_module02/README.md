# 🚀 SIE 平台 - 智能搜尋引擎優化分析系統

SIE (Search Intelligence Engine) 平台是一個全面的智能搜尋引擎優化分析工具，專為現代 AI 驅動的搜尋環境設計。

## 📋 功能特色

### 🔧 模組 1: 網站 AI 就緒度與技術健康度分析
- **根檔案與 LLM 遵從性檢查**
  - robots.txt 存在性與 AI bot 存取權限
  - sitemap.xml 格式驗證
  - llms.txt 前瞻性指標檢查
- **網站架構與權威信號分析**
  - HTTPS 安全性檢查
  - 內部連結結構評估
  - 外部權威連結估算
- **LLM 友善度指標**
  - Schema.org 結構化資料檢測
  - 內容可讀性與標題層級分析
  - PageSpeed 效能指標模擬
- **AI 技術建議生成**
  - 基於 Gemini API 的智能建議
  - 具體可執行的改善方案

### 📊 模組 2: 動態 E-E-A-T 評估與競爭基準分析
- **AI 領導者識別與分析**
  - AI 技術指標檢測
  - AI 內容信號分析
  - AI 領導地位評估
- **動態媒體權重評估**
  - 媒體提及監控與情感分析
  - 社交媒體權威分數計算
  - 內容分發渠道分析
- **競爭對手基準分析**
  - 多維度競爭對手比較
  - 市場地位評估
  - 競爭優勢與改善機會識別
- **趨勢追蹤與預測**
  - 當前趨勢分析
  - 成長預測模型
  - 市場機會與風險識別
- **策略建議生成**
  - 基於 AI 的戰略規劃
  - 實施步驟與時間線
  - 預期影響評估

### 🎯 完整 E-E-A-T 分析
- **Experience (經驗)**: 內容深度與實用性評估
- **Expertise (專業)**: 作者資歷與專業度分析
- **Authoritativeness (權威)**: 行業影響力與認可度
- **Trustworthiness (可信度)**: 透明度與可靠性評估

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 設定 API 金鑰
在 Streamlit 應用程式中輸入您的 Gemini API 金鑰以啟用 AI 建議功能。

### 3. 執行程式
```bash
streamlit run sie_main_app.py
```

## 📁 專案結構

```
sie_module02/
├── sie_main_app.py          # 主要 Streamlit 應用程式
├── website_ai_readiness.py  # 模組 1: 網站 AI 就緒度分析
├── eeat_benchmarking.py     # 模組 2: E-E-A-T 基準分析
├── eeat_module.py           # 完整 E-E-A-T 分析模組
├── requirements.txt         # Python 依賴項
├── README.md               # 專案說明文件
├── config_example.json     # 配置範例檔案
└── .gitignore             # Git 忽略檔案
```

## 🎯 使用指南

### 模組 1: 網站 AI 就緒度分析
1. 選擇「模組 1: 網站 AI 就緒度分析」
2. 輸入要分析的網站 URL
3. 點擊「開始分析」
4. 查看技術健康度報告與改善建議

### 模組 2: E-E-A-T 基準分析
1. 選擇「模組 2: E-E-A-T 基準分析」
2. 輸入目標網站與競爭對手
3. 點擊「開始分析」
4. 查看競爭基準分析與策略建議

### 完整 E-E-A-T 分析
1. 選擇「完整 E-E-A-T 分析」
2. 輸入網站 URL 與公司名稱
3. 點擊「開始分析」
4. 查看詳細的 E-E-A-T 評估報告

## 🔧 技術架構

### 核心技術
- **Streamlit**: 互動式 Web 介面
- **BeautifulSoup**: HTML 解析與內容分析
- **Requests**: HTTP 請求與網站爬取
- **Plotly**: 資料視覺化
- **Google Gemini API**: AI 建議生成

### 分析維度
- **技術 SEO**: 網站技術健康度
- **AI 就緒度**: LLM 友善度與 AI 技術整合
- **競爭分析**: 市場地位與競爭優勢
- **趨勢預測**: 市場趨勢與成長機會

## 📊 分析指標

### 技術健康度指標
- 根檔案完整性 (0-100)
- 架構優化程度 (0-100)
- LLM 友善度 (0-100)

### E-E-A-T 指標
- Experience 分數 (0-100)
- Expertise 分數 (0-100)
- Authoritativeness 分數 (0-100)
- Trustworthiness 分數 (0-100)

### 競爭基準指標
- AI 領導者分數 (0-100)
- 媒體覆蓋分數 (0-100)
- 社交媒體權威分數 (0-100)
- 市場地位評估

## 🎨 視覺化功能

- **互動式圖表**: 使用 Plotly 的動態圖表
- **評分儀表板**: 直觀的分數顯示
- **比較分析**: 競爭對手對比圖表
- **趨勢圖表**: 時間序列分析

## 🔒 隱私與安全

- 所有分析均在本地執行
- 不儲存敏感網站資料
- API 金鑰僅用於 AI 建議生成
- 符合資料保護法規

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request 來改善這個專案！

### 開發環境設定
```bash
git clone <repository-url>
cd sie_module02
pip install -r requirements.txt
streamlit run sie_main_app.py
```

## 📄 授權

本專案採用 MIT 授權條款。

## 📞 支援

如有問題或建議，請透過以下方式聯繫：
- 提交 GitHub Issue
- 發送郵件至支援團隊

---

**SIE 平台** - 讓您的網站在 AI 時代脫穎而出！ 🚀 