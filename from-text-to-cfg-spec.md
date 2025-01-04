# 文檔到設定檔

## 文檔輸入路徑 
- 文檔輸入路徑: `./data/`
- 文檔輸入格式: `*.txt`

## 輸出路徑
- 輸出的 basename 與 對應的文檔輸入 相同，附檔名為 *.json 
- 設定檔輸出路徑: `./cfg-output/`


## 格式轉換摘要

- 文檔內容為 英文生字、英文解釋、中文解釋、詞性、英文例句，不規則換行的資料

- 請協助將文檔格式化為 cfg 格式可仿照以下

```json
{
    "explain": [
        ["perhaps, possibly, but not certainly", "maybe"],
        ...
    ],
    "statement": [
        ["Maybe we can go out to play if the rain stops.", "Maybe"],
        ....
}
```

- 產出json 完畢後，請更改，後方的生字，必須依照前面例句的大小寫、時態，單複數有無加s，來決定是否要大寫、小寫、原型、或者其單複數的變型等等

- 請協助將文檔轉換為 cfg 格式，並輸出到 `./cfg-output/` 資料夾中