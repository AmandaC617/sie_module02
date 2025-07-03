# SIE Module 02 - E-E-A-T 評分模組

## 介紹
本模組用於評估品牌網站的 E-E-A-T（經驗、專業、權威、信任）分數，並可模擬 Google、Gemini API 及維基百科查詢。

## 安裝
```bash
pip install -r requirements.txt
```

## 執行方式
```bash
python eeat_module.py example_config.json example_module1_output.json
```

## 參數說明
- `example_config.json`：品牌與媒體權重等設定
- `example_module1_output.json`：模組1的 HTTPS 分析結果

## 範例輸出
程式會輸出 E-E-A-T 分數與詳細分析結果。 