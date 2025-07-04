# SIE Module 02 - E-E-A-T 評分模組

## 介紹
本模組用於評估品牌網站的 E-E-A-T（經驗、專業、權威、信任）分數，並可模擬 Google、Gemini API 及維基百科查詢。

## 功能特色
- 🔍 **E-E-A-T 評分分析**：計算經驗、專業、權威、信任四大維度分數
- 📰 **媒體提及分析**：模擬 Google 搜尋各類媒體報導
- 🌐 **維基百科檢查**：驗證品牌與相關實體在維基百科的收錄狀況
- 🔒 **HTTPS 安全檢查**：評估網站安全性
- 🎯 **互動式網頁介面**：提供 Streamlit 網頁版，方便使用

## 安裝
```bash
pip install -r requirements.txt
```

## 使用方式

### 1. 命令列版本
```bash
python eeat_module.py example_config.json example_module1_output.json
```

### 2. Streamlit 網頁版（推薦）
```bash
streamlit run app.py
```
然後在瀏覽器中開啟顯示的網址即可使用互動式介面。

### 3. 雲端部署
本專案已準備好部署到 [Streamlit Cloud](https://streamlit.io/cloud)：
- 主程式路徑：`app.py`
- 依賴套件：`requirements.txt`

## 參數說明
- `example_config.json`：品牌與媒體權重等設定
- `example_module1_output.json`：模組1的 HTTPS 分析結果

## 範例輸出
程式會輸出 E-E-A-T 分數與詳細分析結果。

## 專案結構
```
sie_module02/
├── app.py                    # Streamlit 網頁版主程式
├── requirements.txt          # Python 依賴套件
├── README.md                # 專案說明
├── example_config.json      # 範例設定檔
├── example_module1_output.json  # 範例模組1輸出
└── sie_module02/            # 原始模組檔案
    ├── eeat_module.py       # 核心分析邏輯
    ├── eeat_web.py          # 原始 Streamlit 版本
    └── __init__.py          # Python 套件初始化
``` 