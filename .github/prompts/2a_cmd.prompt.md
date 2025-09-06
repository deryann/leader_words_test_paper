任務: 讀取一張教材 JPG 圖片，執行 OCR，整理成指定 JSON 單字資料檔。

輸入:
1. 圖片檔: {jpg_filename}.jpg
2. 已存在之格式參考: AL-p1.json
3. 目錄: cfg-202509

步驟要求:
1. 對圖片做 OCR，擷取每個詞彙卡片上的
   - 單字(保留原括號或複數/過去式標示: 例 weigh(ed), collar(s))
   - 英文解釋 (保持簡潔)
   - 例句 (若圖片已有則忠實擷取並修正常見拼寫錯誤: dodgebal→dodgeball)
2. 圖片最下方四個僅列單字而無英文解釋與例句者，需補：
   - 國小程度英英解釋 (避免使用生字本身)
   - 高不可替換性例句：讓該單字在句中語意無法被另一常見同義字自然替換
3. 統整為 JSON：
{
  "explain": [
    ["定義1", "word1"],
    ["定義2", "word2"],
    ...
  ],
  "statement": [
    ["例句1", "word1"],
    ["例句2", "word2"],
    ...
  ]
}
4. 順序：依圖片自上而下、由左到右。
5. 命名輸出檔：
   cfg-202509/2A-p{base_jpg_filename}.json
   例: 圖片 01.jpg → 2A-p01.json
6. 風格與範例 (參考已成功案例):
{
  "explain": [
    ["to measure how heavy something is", "weigh(ed)"],
    ["to stand tall on your feet", "stood"],
    ...
  ],
  "statement": [
    ["A dog can be weighed on the scale so the vet knows how heavy the dog is.", "weigh(ed)"],
    ["The children measured the dog and he stood one foot tall.", "stood"],
    ...
  ]
}
7. 品質規則:
   - 定義開頭用小寫 (專有名詞除外)。
   - 不含多餘標點或空格。
   - 例句首字母大寫，句末句點。
   - 不添加未在圖片出現的額外單字。
   - 若圖片原文字出現明顯錯字則糾正於輸出 (記錄正確形式)。
   - 不輸出解釋或例句之外的說明文字。

輸出: 僅輸出 JSON 內容 (不加入多餘敘述、標題或程式碼語言標示)。