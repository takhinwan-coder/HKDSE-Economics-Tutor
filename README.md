# HKDSE Economics Tutor

一個為一位中四學生逐課累積的 HKDSE 經濟教學 repository。每課按學校進度和概念難度安排內容，不限制概念數目；把學生用的精簡講義與導師備課材料分開，不追求一次整理完整個 syllabus。

## 教學情境

- 學生：中四、中文授課、理解力良好；每週 Zoom 一課，約 90 分鐘。練習可加入較複雜情境和易混淆的題目。
- 目標：理解概念、練習考試應用與結構式作答，並建立信心。
- 材料：繁體中文、HKDSE 程度、篇幅精簡；優先採用香港生活、消費、房屋、商業、銀行與政府政策例子。
- 學校提供的 syllabus、筆記和用語是編寫材料的首要依據；只教當前進度所需內容。

## Repository 導覽

| 路徑 | 用途 |
|---|---|
| [`course-map.md`](./course-map.md) | 學年/學期進度總覽；收到 syllabus 後逐步填寫 |
| [`syllabus/`](./syllabus/) | syllabus、課程參考文件及學生提供的校內筆記；見 [文件索引](./syllabus/index.md) |
| [`lessons/`](./lessons/) | 按課題命名的每課教材；學生檔案與導師檔案分開 |
| [`past-papers/`](./past-papers/) | 歷屆試題原檔及按課題索引 |
| [`question-bank/`](./question-bank/) | 自編、改編或整理後可重用的練習 |
| [`common-mistakes/`](./common-mistakes/) | 學生常見錯誤及補救提示 |
| [`teaching-notes/`](./teaching-notes/) | 跨課堂的教學心得與待跟進事項 |
| [`templates/`](./templates/) | 每課教材範本 |
| [HKDSE 教學 Skill](./.github/skills/hkdse-economics-teaching-assistant/SKILL.md) | Agent 編寫教材時採用的工作流程與品質標準 |

## 每課工作流程

1. 指出今課課題及學生大概進度；按概念難度安排 90 分鐘內的教學內容，不限於 1–2 個概念。學生只記得口頭課題也可以，不必等到取得校內筆記才開始。
2. 如有相關學校教材，可放在 [`syllabus/student-notes/`](./syllabus/student-notes/)；若有合適的歷屆試題，從 [試題索引](./past-papers/index.md) 選取。
3. 只載入本課相關的 syllabus 摘錄和試題參考，按本 repository 的範本製作當課材料。
4. Tutor 檢查內容和題目後，把 `student-pack.md` 匯出成 PDF 給學生；導師使用一頁內的 `tutor-guide.md`，並在其中查看精簡答案提示。
5. 課後提供學生理解情況和實際上課日期；更新 [`course-map.md`](./course-map.md) 的日期、教材狀態及一句話待跟進，並只在有可重用的匿名化錯誤時更新常見錯誤紀錄。欄位定義見 course map。

建議每次只處理**一課**的工作，不要把整份 syllabus 和所有歷屆試題一次載入對話；repository 的索引負責定位相關來源。也建議每課開一個新的對話，沿用這個工作區並按需讀取 course map、本課材料和相關 syllabus/試題即可；不用重貼整套教學規則或上一課的完整對話。新對話可用以下開場：

> 請在目前 HKDSE Economics Tutor repository 準備「課題名稱」。今課課題：……；學生目前進度/先備知識：……；請只查閱相關 syllabus 部分和 `past-papers/index.md` 中對應的試題。建立或更新該課的 student pack、tutor guide 和 metadata。校內進度尚未確認的地方請標示，不要猜測。

## 每課教材

每課建立一個按 HKDSE 課題命名的獨立資料夾，例如 `lessons/topic-04-production-factors-scale/`。若同一課題需要多課，資料夾名稱再加上具體子題，例如 `topic-05-short-run-production/` 和 `topic-05-short-run-costs/`，不要用 Week 01、Week 02 等週次作資料夾名稱。每個資料夾使用以下檔案：

- `student-pack.md` — 學生版課堂摘要及練習，可直接轉成 PDF。不要放答案。
- `tutor-guide.md` — 導師版教學流程、講解重點、延伸例子、提問提示及 Zoom 建議。
- `metadata.md` — 課題、學校進度、先備知識、來源和歷屆試題引用。

每課內容按概念難度和 90 分鐘教學目標安排；不必限制為 1–2 個概念。若同一課題需要不同範例或獨立評估，也可拆成各自清楚命名的課堂資料夾。學生版不附答案；答案提示放在導師筆記。

學生講義要讓學生課後能獨立複習：核心概念需由淺入深說明原因和關係，並用至少一個逐步拆解的例子展示推理；不要只列定義或為了增加頁數加入填充內容。每課製作時請沿用 [`student-pack.md` 範本](./templates/student-pack.md) 和 [HKDSE 教學 Skill](./.github/skills/hkdse-economics-teaching-assistant/SKILL.md) 的深度要求。

## PDF 與版本管理

- Markdown 是可修改、可追蹤的主要來源；PDF 是交給學生的發佈版本。
- 建議在 VS Code 安裝 Markdown PDF 匯出 extension（`yzane.markdown-pdf`）；本 workspace 提供 A4 繁體中文列印樣式 [`teaching-notes.css`](./.vscode/teaching-notes.css)，學生講義與導師筆記共用。
- 開啟 `student-pack.md` 或 `tutor-guide.md`，執行 **Markdown PDF: Export (pdf)**；PDF 會輸出在同一課題資料夾。導師筆記及答案提示不應併入學生版 PDF。
- 輸出前檢查繁體中文字型、圖表標籤、換頁和頁數；若 PDF 排版不理想，先調整 Markdown，再重新輸出。
- 可把發給學生的 PDF 放回同一課題資料夾，檔名例如 `student-pack.pdf`；不要把答案或導師筆記合併進學生 PDF。
- Git 用來記錄 syllabus 摘要、講義和索引的每課修訂。這是本機 repository；定期備份，未決定用途前不要加入學生姓名等個人資料。

## 開始使用

學校 syllabus 和課程參考文件放入 [`syllabus/`](./syllabus/)；學生的校內筆記放在 [`syllabus/student-notes/`](./syllabus/student-notes/)。先在 [`course-map.md`](./course-map.md) 記下學生目前大概進度，再指定當課課題和相關歷屆試題，即可逐課製作材料。
