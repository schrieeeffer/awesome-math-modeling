# 单文件 LaTeX 论文骨架

适合从一个 `main.tex` 开始写作的项目。需要分章编辑、自动编译或 Overleaf 使用说明时，可以选择 [完整 LaTeX 工程](../../latex-template/README.md)。

## 编译与填写

复制整个目录到项目中，在带有 CTeX、Fandol、TeX Gyre、zref 及常见宏包的 TeX Live 环境执行：

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

生成文件为 `main.pdf`。默认使用 A4、25 mm 页边距、小四宋体正文、黑体标题和两字符缩进，摘要关键词加粗。按当前要求及参考论文调整这些设置和章节顺序。

`\slot{...}` 显示为 `〔待填：…〕`。填入本题的推导、结果和验证，数字来源记录在项目结果台账中。复制模型章节时，为公式、表格和图片使用不同的标签前缀，例如 `tab:q1-results`、`tab:q2-results`，并同步修改引用。

## 启用文献

在 `references.bib` 中加入已核验的文献，并在正文写入 `\cite{文献键}`。删除文末手写的 `\section*{参考文献}` 及占位段落，然后取消以下两行的注释：

```tex
\bibliographystyle{gbt7714-numerical}
\bibliography{references}
```

该样式需要安装 `gbt7714`。随后依次运行 XeLaTeX、`bibtex main`、两次 XeLaTeX，由 BibTeX 生成文献表。

## 声明、附录与页数

按实际使用情况和本届要求填写 AI 简短声明；不需要该节时设为 `\includeaistatementfalse`。详情与支撑材料的位置也按当前规则安排。

正文结束后另页进入附录，标题显示“附录 A …”。主要结论和要求的汇总表放在正文，结果明细和程序按规则安排；采用选录时注明范围及完整文件位置。

编译生成的 `.aux` 包含 `skill:body-start`、`skill:body-end`、`skill:appendix-start`。它们记录物理页，正文计数包含末尾浮动图表。不同比赛的计页范围可能不同，调整标记后核对实际 PDF。检查工具和标记解释见 [完整工程说明](../../latex-template/README.md#正文附录与页数)。

定稿后重新编译，检查缺字、图表换页、公式和交叉引用，并根据当前支撑目录更新附录清单。
