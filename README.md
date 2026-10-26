# 数学建模与论文写作

从赛题分析、实验验证到论文定稿的一套工作方法，适用于国赛、美赛及其他数学建模比赛。

你可以把它作为 `math-modeling-competition` 技能交给 AI 使用，也可以直接阅读指南、运行辅助脚本，或复制 LaTeX 工程写论文。提供一篇往年论文后，技能会分析它的结构、文风和版式，再结合本届题目与规则组织你的论文。

[快速开始](#快速开始) · [使用示例](#使用示例) · [文档导航](#文档导航) · [LaTeX 模板](latex-template/README.md)

## 可以用它做什么

- 读懂赛题和附件，整理每问需要回答的问题、可用数据和约束。
- 从简单基线出发选择模型，完成求解、对比实验和结果核验。
- 学习往年论文的论证方式，形成适合本题的提纲、段落和图表。
- 改进已有初稿，保留成熟方案，补足说明、引用和验证。
- 整理论文、代码与结果文件，检查页数、图表和提交材料。

开始完整任务时，技能会先读取已有文件，再补问缺少的参赛要求、参考论文和输出位置。需要填写封面或登记表时，再按规则确认队伍信息；匿名论文和实名材料分开处理。

## 快速开始

### 安装技能

将仓库放入 Codex 的个人技能目录，文件夹名使用 `math-modeling-competition`。

Windows PowerShell：

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex/skills' }
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null

git clone https://github.com/schrieeeffer/awesome-math-modeling.git (Join-Path $skillRoot 'math-modeling-competition')
```

macOS / Linux：

```bash
git clone https://github.com/schrieeeffer/awesome-math-modeling.git "${CODEX_HOME:-$HOME/.codex}/skills/math-modeling-competition"
```

也可以下载 ZIP，解压到同一位置。已有安装时，保留自己的修改后再合并更新。重新打开 Codex，在对话中输入 `$math-modeling-competition` 即可调用。其他支持 `SKILL.md` 的工具可按各自方式导入本目录。

### 准备材料

通常需要赛题、附件、当届要求，以及你已有的代码或论文。往年参考论文提供链接或本地路径都可以；一篇完整案例就能开始。暂时没有参考时，也可以先分析题目，再从已有资料中选择合适案例。

个人信息由本届提交要求决定，也可以留给队员最后填写。

## 使用示例

### 从题目开始

```text
使用 $math-modeling-competition 分析附件赛题。
先梳理每问的目标、数据、约束和基线方案，再完成求解与验证。
题目和参赛要求在〔项目目录〕，输出保存到〔结果目录〕。
```

### 参考往年论文写作

```text
使用 $math-modeling-competition。
参考〔论文链接或文件路径〕，分析它的章节结构、文风和排版。
结合〔项目目录〕里的题目、数据和比赛要求，完成本题的原创论文。
缺少材料时请集中询问，最终文件保存到〔提交目录〕。
```

### 改进已有论文

```text
使用 $math-modeling-competition 审改这份论文。
保留已确认的模型和结果，重点改善解释、图表和章节衔接。
先检查现有实验能否支持结论，再决定是否补充计算。
```

完整任务会沿着“读题 → 建模与验证 → 写作与排版 → 检查与交付”继续推进。你也可以只处理其中一问、一段摘要或几张图。

## 文档导航

| 想做什么 | 从这里开始 |
| --- | --- |
| 了解技能如何工作 | [技能入口](SKILL.md) |
| 从往年案例提取结构、文风与版式 | [参考论文适配](references/reference-adaptation.md) |
| 完成建模到提交的整个流程 | [终稿流程](references/one-pass-delivery.md) |
| 拆解题目、选择模型和验证结果 | [建模流程](references/modeling-workflow.md) · [模型选择](references/model-selection.md) |
| 写摘要、模型解释与结果分析 | [论文写作](references/writing-style.md) · [结构参考](references/paper-archetypes.md) |
| 改进图表、引用和提交材料 | [终稿检查](references/submission-quality.md) · [论文审改](references/paper-review.md) |
| 处理预测驱动的动态决策 | [动态决策](references/dynamic-decisions.md) · [微网案例复盘](references/case-lessons-microgrid.md) |
| 查阅往年案例与来源 | [32个论文及讲评案例](references/case-evidence.md) · [资料索引](references/corpus-guide.md) |

## 模板与辅助工具

### LaTeX 工程

[`latex-template/`](latex-template/) 提供可独立编译的中文工程。已有官方模板时可以直接使用官方文件；从案例重建样式时，也可以把这个工程作为起点。

在模板目录运行：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

结果位于 `build/main.pdf`。章节在 `sections/` 中编辑，项目样式在 `project-style.tex` 中调整，文献放入 `references.bib`。添加引用后，在 `main.tex` 开启文献开关。安装依赖、Overleaf 用法和编译说明见 [模板文档](latex-template/README.md)。

[`assets/`](assets/README.md) 还提供 Markdown 论文骨架、摘要提示、结果台账、假设表、进度记录和参考论文画像。Word 文件保留为历史样式参考。

### 提交检查

需要 Python 3.10 或更新版本；读取 PDF 时安装 `pypdf`。

```bash
python scripts/check_delivery.py --root ./submit --expect paper.pdf --expect support/result.xlsx
python scripts/check_delivery.py --root ./submit --pdf paper.pdf --aux ./build/main.aux --body-limit 30
```

第一条检查所列文件是否齐全。第二条读取模板的物理页标记并计算正文页数；这里的 `30` 请换成本届页限，`.aux` 使用对应 PDF 的最新编译文件，路径相对于运行命令的目录。也可以通过 `--body-first` 和 `--body-last` 指定已确认的物理页范围。

脚本还会列出疑似占位和过程文件，供逐项检查。数学结果和实际版面仍需结合原始输出、PDF 页面核对。完整参数见 `python scripts/check_delivery.py --help`。

### 资料检索

索引检索使用 Python 3.9 或更新版本，仅依赖标准库：

```bash
python scripts/search_corpus.py "种植" --year 2024 --ext pdf --limit 8
python scripts/search_corpus.py --id S4190f2ed8e7b
```

拥有抽取全文时，可以指定文本目录：

```bash
python scripts/search_corpus.py "供应商" --content --text-root "../my-corpus/_distillation" --limit 6
```

本机路径配置见 [资料索引说明](references/corpus-guide.md#定向检索原件)。

## 资料来源

仓库收录的是整理后的指南、模板和来源索引，原始论文、题目附件及数据由使用者自行提供。索引包含1,504个原始文件记录和4,531个压缩包成员，其中有重复路径；32个案例附有实际选读范围，详见[覆盖说明](references/corpus-guide.md)。

历史案例用于学习写法和比较思路，当前比赛的格式、页数和披露安排以当届要求为准。论文中的数值来自当前计算，引用回到原始来源核验。

## 参与完善

欢迎通过 [Issue](https://github.com/schrieeeffer/awesome-math-modeling/issues) 或 Pull Request 分享使用反馈、模板修复和案例分析。报告问题时附上复现步骤、运行环境和必要的脱敏示例；新增案例请注明来源及阅读范围。
