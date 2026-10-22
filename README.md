# HKDSE Economics Tutor

一個為一位中四學生逐課累積的 HKDSE 經濟教學 repository。每課按學校進度準備 **1–2 個相關課題**，把學生用的精簡講義與導師備課材料分開；不追求一次整理完整個 syllabus。

## 教學情境

- 學生：中四、中文授課、程度中等；每週 Zoom 一課，約 60–75 分鐘。
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

1. 指出今課要教的 1–2 個課題及學生大概進度；學生只記得口頭課題也可以，不必等到取得校內筆記才開始。
2. 如有相關學校教材，可放在 [`syllabus/student-notes/`](./syllabus/student-notes/)；若有合適的歷屆試題，從 [試題索引](./past-papers/index.md) 選取。
3. 只載入本課相關的 syllabus 摘錄和試題參考，按本 repository 的範本製作當課材料。
4. Tutor 檢查內容和題目後，學生 PDF 由工作區自動生成；導師使用同時包含教案、答案及評分提示的 `tutor-guide.md`。
5. 課後提供學生理解情況和實際上課日期；更新 [`course-map.md`](./course-map.md) 的日期、教材狀態及一句話待跟進，並只在有可重用的匿名化錯誤時更新常見錯誤紀錄。欄位定義見 course map。

建議每次只處理**一課**的工作，不要把整份 syllabus 和所有歷屆試題一次載入對話；repository 的索引負責定位相關來源。也建議每課開一個新的對話，沿用這個工作區並按需讀取 course map、本課材料和相關 syllabus/試題即可；不用重貼整套教學規則或上一課的完整對話。新對話可用以下開場：

> 請在目前 HKDSE Economics Tutor repository 準備「課題名稱」。今課課題：……；學生目前進度/先備知識：……；請只查閱相關 syllabus 部分和 `past-papers/index.md` 中對應的試題。建立或更新該課的 student pack、tutor guide（包括答案及評分提示）和 metadata。校內進度尚未確認的地方請標示，不要猜測。

## 每課教材

每課建立一個按 HKDSE 課題命名的獨立資料夾，例如 `lessons/topic-04-production-factors-scale/`。若同一課題需要多課，資料夾名稱再加上具體子題，例如 `topic-05-short-run-production/` 和 `topic-05-short-run-costs/`，不要用 Week 01、Week 02 等週次作資料夾名稱。每個資料夾使用以下檔案：

- `student-pack.md` — 學生版課堂摘要及練習，可直接轉成 PDF。不要放答案。
- `tutor-guide.md` — 導師版教學流程、講解重點、Zoom 建議，以及所有練習答案和評分提示。
- `metadata.md` — 課題、學校進度、先備知識、來源和歷屆試題引用。

一課可以有 1–2 個相連課題；若同一課題需要不同範例或獨立評估，也可拆成各自清楚命名的課堂資料夾。檔名及結構可按需要調整，但應保持學生版與答案分離。

學生講義要讓學生課後能獨立複習：核心概念需由淺入深說明原因和關係，並用至少一個逐步拆解的例子展示推理；不要只列定義或為了增加頁數加入填充內容。每課製作時請沿用 [`student-pack.md` 範本](./templates/student-pack.md) 和 [HKDSE 教學 Skill](./.github/skills/hkdse-economics-teaching-assistant/SKILL.md) 的深度要求。

## 自動生成學生 PDF

- Markdown 是可修改的來源；學生 PDF 僅由 `student-pack.md` 生成，導師答案不會放入學生版。
- macOS 首次設定先安裝系統字型排版元件及 Python PDF 工具：`brew install pango`，然後執行 `python3 -m pip install -r requirements-pdf.txt`。
- 在 VS Code 開啟 repository 後，允許「Keep lesson PDFs up to date」自動工作。它會先生成每課 PDF，之後每次儲存 `student-pack.md` 即更新同一資料夾的 `student-pack.pdf`。
- 若 VS Code 詢問是否允許資料夾開啟時執行自動工作，選擇允許。下次開啟工作區便會自動監看，毋須手動匯出。
- 手動一次生成或補做 PDF：`python3 scripts/build_student_pdfs.py`；也可指定某課資料夾或講義檔案。
- PDF 使用 [`student-pack.css`](./scripts/student-pack.css) 的 A4 樣式，並支援同資料夾內的 SVG 圖表。分享前仍請快速檢查繁體中文字型、圖表和換頁。
- Git 用來記錄 syllabus 摘要、講義和索引的每課修訂。這是本機 repository；定期備份，未決定用途前不要加入學生姓名等個人資料。

## 開始使用

學校 syllabus 和課程參考文件放入 [`syllabus/`](./syllabus/)；學生的校內筆記放在 [`syllabus/student-notes/`](./syllabus/student-notes/)。先在 [`course-map.md`](./course-map.md) 記下學生目前大概進度，再指定當課課題和相關歷屆試題，即可逐課製作材料。
