# CIE Physics 章节页面生成指南

本指南用于把新章节（例如 Deformation of solids、Waves、Electricity 等）生成成与现有章节一致的学习页面。按顺序执行即可。

## 1. 目标结构

每个章节生成一个页面，包含：

- 完整英文知识点（对应 syllabus 内容）
- 20 道 Multiple Choice + 10 道 Structured Questions（SQ 不足 10 道时用该专题全部 SQ）
- 每道题紧跟答案：选择题给官方答案 + 解析，大题按 PDF 评分点逐条
- 章末「Original question PDFs」提供全部原始专题 PDF 的在线链接

文件命名（以第 5 章为例）：

```text
as-level/05-work-energy-power.qmd              # 主页面
as-level/05-work-energy-power-mc.qmd           # 选择题
as-level/05-work-energy-power-structured.qmd   # 大题
assets/questions/work-energy-power/*.webp      # 题目图
resources/original-papers/work-energy-power/*.pdf  # 原始专题 PDF
```

## 2. 定位资料

1. `Note/` 下找对应章节 Note PDF（例如 `Note/5.1 Energy Conservation.pdf.pdf`）。
2. `PastPaper/Topical Past Papers/` 下找该专题的题包：
   - `C` 结尾 = Multiple Choice，`SQ` 结尾 = Structured Questions
   - 通常有 Easy / Medium / Hard 三档
3. 用 `pdftotext -layout` 提取可读文本；题目页渲染成 PNG 后用 tesseract OCR：

```bash
pdftoppm -f 1 -l <题目页数> -r 180 -png <pdf> tmp/pdfs/<topic>/render/<key>/page
```

## 3. 题目选择规则（最重要）

严格按以下优先级选择题目，不要凭感觉换题：

1. **先提取题目页的独立 image 对象**：用 `pdfimages -png` 导出对象。只要对象是 PDF 里的独立 image（不要求有 smask 掩码），都可以使用：
   - 有匹配 smask（相邻对象尺寸一致）→ 合成白底图；
   - 无 smask 且本身是白底图 → 直接转成 WEBP 使用。
2. **只加入两类题**：
   - 原题带图，且图可以独立提取的题；
   - 原题就是纯文字、不需要图的题。
3. **原题带图但图无法独立提取的题：跳过，不加入页面**。不要把它改写成纯文字题，也不要拿其它纯文字题顶替。
   - 注意：很多 PDF 的题目图就是「无 smask 的独立 image 对象」，不要因为缺 smask 就误判为不可提取。用 `pdfimages -list` 列出的对象页号 + 尺寸即可确认。
4. **不要使用答案页的图**。判断方法：pdfimages 的对象页号必须落在题目页范围内（PDF 前半部分是题目页，后半部分是 Model Answers）。
5. 带图题优先；目标状态下 20 道 MC 和 10 道 SQ 尽量全部带图（第 6 章已做到 MC 20/20 带图）。数量不足时用纯文字题补齐。

## 4. 图像处理细节

```bash
# 列出每页对象，确认题目页范围与独立图
pdfimages -list <pdf> | awk 'NR>2 && $1<=<题目页数> && $3=="image"'

# 导出对象
pdfimages -png <pdf> tmp/pdfs/<topic>/objects/<key>
```

处理分两种情况（用 Python + Pillow）：

**情况一：对象带匹配 smask（相邻编号、尺寸一致）**

```python
im = Image.open(img).convert("RGB")
m  = Image.open(mask).convert("L")
assert im.size == m.size
white = Image.new("RGB", im.size, "white")
white.paste(im, mask=m)
white.save(out, "WEBP", lossless=True, method=6)
```

**情况二：对象无 smask（独立完整图）**

```python
im = Image.open(img).convert("RGB")
# 先检查四角是否为白色，确认没有黑底
im.save(out, "WEBP", lossless=True, method=6)
```

无 smask 的对象通常是题目页直接嵌入的白底图，直接保存即可。若四角出现黑底，说明该对象本身是黑底图，放弃使用或改用有 mask 的对象。

完成后必须抽查：

- 图片内容与该题一致（必要时用 view_image 逐张核对）；
- 四角为白色（无黑底）；
- 没有把题干文字或答案示意图一起截进去；
- 没有引用答案页对象。

## 5. 页面内容规范

### 主页面

```yaml
---
title: "5 Work, energy and power"
subtitle: "..."
---
```

知识点用英文 `::: {.study-card}`（概念）与 `::: {.formula-panel}`（公式）组织，覆盖 syllabus 全部条目；公式用 LaTeX。

在页面中 include 两个文件：

```markdown
## Multiple Choice Questions

{{< include 05-work-energy-power-mc.qmd >}}

## Structured Questions

{{< include 05-work-energy-power-structured.qmd >}}
```

章末放 `### Original question PDFs` 链接（见第 6 节）。

### 题目标题格式

统一使用：

```text
#### Example N · 5.1 MC Easy Q1
#### Example N · 5.2 SQ Medium Q3
```

其中 N 是该章节内从 1 开始的连续编号；MC 与 SQ 分别编号。不要使用自创的标题格式。

### 答案格式

- 选择题：

```markdown
<details class="answer-panel"><summary>Show answer and explanation</summary>

**Answer: C.** 解析……
</details>
```

- 大题：按 (a)(i)(ii)… 分点，每点末尾标注分值 `[1]`，数值过程写完整：

```markdown
- **(a)(i)** 计算过程 `[2]`
- **(a)(ii)** 结论 `[1]`
```

答案以 PDF 后半部分 Model Answers 为准，不要自己另造答案；如原答案明显有误，在答案下方加「Source check」说明。

## 6. 原始 PDF 链接

1. 把题包 PDF 复制到：

```text
Physics_Study/resources/original-papers/<topic>/
```

2. 页面中链接统一用 raw 地址（不要用相对路径，否则会进 Pages 包导致部署超时）：

```markdown
- [5.1 Energy - MC Easy](https://raw.githubusercontent.com/nanoxsj/CIE-Physics-Study/main/resources/original-papers/work-energy-power/5.1-energy-conservation-work-power-efficiency-c-easy.pdf)
```

3. PDF 只保留在 `main` 分支，**不要**进入 `gh-pages` / `_site`。

## 7. 接线与渲染

1. `_quarto.yml`：
   - `project.render` 增加 `as-level/05-work-energy-power.qmd`
   - `website.sidebar` 的 AS Level 部分增加 href 与 text
2. `index.qmd`：加一章 `::: {.topic-card}` 卡片，列出知识点与题量。
3. 渲染全站：

```bash
quarto render --no-cache
```

（Quarto 需要写 `~/Library/Caches/quarto`，沙箱下用 require_escalated；若报 `unable to open database file`，基本就是缓存目录权限问题，重跑即可。）

4. 检查生成的 HTML：

```bash
rg -c 'class="level[0-9] question-card"' _site/as-level/05-work-energy-power.html
rg -c 'class="answer-panel"' _site/as-level/05-work-energy-power.html
rg -n 'assets/questions/work-energy-power/' _site/as-level/05-work-energy-power.html
```

确认：题卡数 = 题目数、每个答案区都在、所有图引用存在、没有 "See the original PDF" 之类的占位文本。

## 8. 发布

1. 提交并推送 main：

```bash
git add -A
git commit -m 'Add ... chapter N'
git push --progress origin main
```

（PDF 较多时上传较慢，网络失败就重试；不要 Ctrl-C 中断正在进行的上传。）

2. 发布 gh-pages。优先用 Quarto：

```bash
quarto publish gh-pages --no-render --no-prompt --no-browser
```

若 GitHub 连接不稳定导致失败，改用手动发布：

```bash
pages_dir=$(mktemp -d /tmp/cie-pages.XXXXXX)
git worktree add "$pages_dir" gh-pages
rm -rf "$pages_dir"/*
cp -R _site/. "$pages_dir"/
git -C "$pages_dir" add -A
git -C "$pages_dir" commit -m 'Built site for gh-pages'
git -C "$pages_dir" push --progress origin HEAD:gh-pages
git worktree remove "$pages_dir"
```

3. 验证：查询最新 deployment 状态为 `success`，线上页面返回 200。

## 9. 常见坑

- **答案页图混入**：pdfimages 对象页号超出题目页范围 = 答案页图，禁止使用。
- **误判「无 smask = 不可提取」**：很多题目图是无 smask 的独立对象，检查四角是否为白底后直接使用即可；只有页面内嵌的矢量图或截图才需要放弃。
- **图与题不对应**：对象编号不等于题目编号；必须用 pdfimages 的页号 + 对象尺寸与 OCR 题干对应，合成后逐张核对内容。
- **Quarto 缓存报错**：`unable to open database file` 时用升权限重跑，不要改项目文件。
- **gh-pages 混入 PDF / .DS_Store**：Pages 只应包含 HTML/CSS/WEBP；发布前检查 `git ls-tree` 确认没有 `.pdf` 和 `.DS_Store`。
- **标题格式不统一**：始终用 `Example N · X.Y MC/SQ 难度 Q#`。
- **题量**：MC 20 道、SQ 10 道（SQ 不足时用全部可用题），不要多不要少。
