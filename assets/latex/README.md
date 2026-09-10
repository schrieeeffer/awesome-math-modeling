# 可移植论文骨架

该模板从本地 Word 与 LaTeX 资料提炼结构，不依赖其中定制的 `cumcmthesis.cls`、大字体文件、演示图片和示例代码。它不是官方赛题或提交格式。

在已安装 CTeX、Fandol 字体与常见宏包的 TeX Live 中编译：

```text
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

默认 A4、四边 25 mm、正文小四、两字符缩进，来自本地写作模板的共同页面特征。字体使用 TeX Live 提供的 Fandol 宋/黑体以减少机器依赖；英文字体优先 Times New Roman，不存在时用 TeX Gyre Termes。章节数量、摘要和页码安排均为可编辑选择。提交前按适用官方通知调整。

先复制整个 `latex` 目录到赛题工作目录，再编辑。复制模型章节时同时修改所有标签及其引用，采用每问唯一的名称，如 `tab:q1-results`、`tab:q2-results`、`eq:q1-model`，避免重复 `\label`。保留中文的 `〔待填：…〕` 或 `\slot{…}` 意味着仍是草稿。模板没有真实研究结果，不要通过删除占位标记假装已完成研究。数字需能回溯项目的 `result-ledger.csv`。

参考文献库初始为空。只有核验且在正文实际引用的来源才写入 `references.bib`，并取消 `main.tex` 底部 BibTeX 命令的注释，同时删除手写的 `\section*{参考文献}` 和临时占位段，避免自动文献表生成重复标题。按源中说明启用 `gbt7714-numerical` 格式时，还需安装该样式。不要使用 `\nocite{*}` 填满文献列表。

本次验证环境为 Windows + TeX Live 2025；只证明空骨架可编译、页面可读。填入真实内容后必须重新编译并逐页检查溢出、表格、图注、公式和交叉引用。原 `latex.zip` 的完整文件保留在项目资料中，未改动。
