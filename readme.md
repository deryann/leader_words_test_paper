# 產生 spelling word test paper


## 操作方式
1. 可從 PDF copy paste 出來的資料 存成 txt 後
2. 透過 from-text-to-cfg-spec.md 與 github copilot 產生的 json 檔案
3. 可透過 run.py 來產生 word test paper
```shell
python run.py -i ALP16.json
```

## Web 介面

可透過瀏覽器操作，下載測驗題目及答案（DOCX 或 PDF）：

```bash
# 安裝 FastAPI 與 Uvicorn
pip install fastapi uvicorn
# 確保已安裝 pandoc 以進行 PDF 轉換: https://pandoc.org/installing.html
uvicorn app:app --reload
```

開啟瀏覽器並前往 http://127.0.0.1:8000