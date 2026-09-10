# Awesome Math Modeling

面向中文数学建模竞赛的 **AI Skill、论文写作指南与可编译 LaTeX 模板**。把赛题分析、模型选择、计算验证和论文表达连接起来，并从历年论文中提炼摘要、分问论证、公式组织、图表说明与局限写法。

核心技能名为 `math-modeling-competition`。你可以在 Codex 中调用，也可以直接阅读指南、复制模板使用。

## 内容与特色

- **建模流程**：从各问交付物和约束出发，选择基线与模型，保留可复算结果，安排适合问题类型的验证。
- **历年论文写法**：整理 32 个历史论文及讲评案例，提供来源 ID、实际选读页码、可借鉴结构及适用边界；见[写作风格](references/writing-style.md)、[论文结构类型](references/paper-archetypes.md)和[案例证据](references/case-evidence.md)。
- **多格式资产**：独立的 [LaTeX 工程模板](latex-template/README.md)，以及 [Word 论文模板](assets/manuscript.docx)、[Markdown 骨架](assets/manuscript.md)、摘要、分问章节、结果台账、假设表和 AI 使用记录。
- **可追溯检索**：用 Python 标准库检索来源目录，可按关键词、年份、扩展名或精确 ID 筛选；接入自己的抽取文本后可搜索正文与物理页码。

本仓库包含蒸馏后的指南、模板和来源元数据，**不包含原始论文、题目附件、数据集、视频和抽取全文**。资料清点覆盖 1,504 个原始文件、4,531 个压缩包成员；这些是索引数量，包含重复路径，不表示逐篇全文审读。32 个案例的阅读深度也不同，完整统计与限制见[覆盖说明](references/corpus-guide.md)。

## 快速开始

### 在 Codex 中安装

将仓库复制到 Codex 的个人技能目录，并把技能文件夹命名为 `math-modeling-competition`：

```powershell
# Windows PowerShell；已设置 CODEX_HOME 时使用该目录
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex/skills' }
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
git clone https://github.com/schrieeeffer/awesome-math-modeling.git (Join-Path $skillRoot 'math-modeling-competition')
```

macOS / Linux：

```bash
git clone https://github.com/schrieeeffer/awesome-math-modeling.git "${CODEX_HOME:-$HOME/.codex}/skills/math-modeling-competition"
```

也可下载仓库 ZIP，将解压后的完整目录复制到上述位置。目标目录已存在时，先保留自己的修改，再合并更新。重新打开 Codex 后，在任务中提供赛题、数据或草稿并调用：

```text
使用 $math-modeling-competition 分析附件赛题，先列出每问交付物、变量、约束和可验证的基线方案。
```

```text
使用 $math-modeling-competition 改进这份论文摘要。参考历史论文的分问表达，保留已有数字，标出没有结果支持的判断。
```

如果只需模板或写作指南，直接使用下述文件即可。其他支持 `SKILL.md` 的工具可按其技能导入方式加载本目录。

### 编译 LaTeX 论文

复制整个 [`latex-template/`](latex-template/) 到你的赛题工作目录，编辑 `main.tex`、`sections/*.tex` 和 `references.bib`。安装包含 CTeX、Fandol、BibTeX 与 latexmk 的 TeX Live 或等效环境后，在模板目录运行：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

默认编译链使用 **XeLaTeX 与 BibTeX**，由 latexmk 自动完成必要轮次，生成 `build/main.pdf`。依赖、手动编译步骤和各文件用途见[模板说明](latex-template/README.md)。

这是可编辑的通用论文工程，页面设置不代表某届竞赛的官方要求。按题目增删章节，只写入实际计算结果和核验过的引用；填充后重新检查图表、公式、交叉引用和分页。`assets/latex/` 保留原有最小骨架；新论文建议从顶层 `latex-template/` 开始。

### 检索资料索引

Python 3.9 或更新版本，无第三方依赖。在仓库根目录运行：

```bash
python scripts/search_corpus.py "种植" --year 2024 --ext pdf --limit 8
python scripts/search_corpus.py --id S4190f2ed8e7b
```

这些命令只搜索随仓库提供的路径与元数据，无需本机配置或原资料。若拥有对应的抽取正文目录（内含 `text/来源ID.txt`），可显式指定根目录：

```bash
python scripts/search_corpus.py "供应商" --content --text-root "../my-corpus/_distillation" --limit 6
```

也可复制 [`references/local-corpus.example.json`](references/local-corpus.example.json) 为 `references/local-corpus.json`，修改路径，或通过 `--config` 指定自己的 JSON 文件。配置中的相对路径按**配置文件所在目录**解释；`--text-root` 优先于配置。`local-corpus.json` 是被 Git 忽略的本机文件，不应提交个人资料路径。详见[语料检索说明](references/corpus-guide.md#定向检索原件)。

## 目录结构

```text
.
├── SKILL.md                    技能入口、任务路由与核心约束
├── agents/openai.yaml          Codex 展示与调用元数据
├── latex-template/             可独立复制编译的 LaTeX 工程
│   ├── main.tex
│   ├── sections/
│   └── references.bib
├── assets/                     Word、Markdown、CSV 与最小 LaTeX 骨架
├── references/                 建模、写作、案例、审查与来源索引
└── scripts/search_corpus.py     路径检索与可选本地全文检索
```

## 使用边界与贡献

历史材料中的“优秀”“一等奖”“官方”等文件名标签未独立核验。案例用于学习论证方法，不保证模型正确、获奖结果或当前比赛合规；页面限制、匿名要求、AI 使用与提交格式须依据适用赛事的当届通知。

写作指南强调用真实结果支撑摘要与结论、解释假设影响、核对引用和复现过程。不要复制往年长段正文、沿用示例数值，或把尚未验证的结果写成已完成。

欢迎通过 Issue 或 Pull Request 补充可复现的模板修复、写作案例分析与模型验证经验。新增案例请说明来源、选读范围和结论边界；不要提交无再分发授权的论文全文、资料包、数据、字体或个人本机配置。
