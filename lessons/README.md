# 按課題整理的課堂材料

每課一個以 syllabus 課題命名的獨立資料夾，例如 `topic-04-production-factors-scale/`。同一課題分多課時，在課題名稱後加上子題焦點，例如 `topic-05-short-run-production/` 和 `topic-05-short-run-costs/`。每課集中處理 1–2 個相連課題，並建立：

- `student-pack.md` — 繁體中文、學生可讀的課堂摘要與練習，適合匯出 PDF。
- `tutor-guide.md` — 60–75 分鐘導師教案、講解提示，以及學生講義每題的完整答案與評分點。
- `metadata.md` — 進度、來源和題庫/歷屆試題參照。

每課只製作學生版和導師版兩份教學筆記；導師版須逐題對應學生版，包含 MC 錯誤選項的概念解釋。舊課堂或存檔材料可能保留獨立 `solutions.md`，新課不再另外產生。從 [`templates/`](../templates/) 複製範本。不要用週次命名資料夾；不要為未提供的 syllabus 或課題預先編造內容。

學生 PDF 由 workspace 自動工作監看 `student-pack.md` 並更新為同資料夾的 `student-pack.pdf`。首次設定及使用方式見 repository 的 [`README.md`](../README.md)。
