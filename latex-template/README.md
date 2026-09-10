# 数学建模 LaTeX 标准工作模板

复制本目录即可编译；默认已启用 `.tex` 分章、`.bib` 文献和自动交叉引用，无需手工取消注释。本模板延续仓库提炼的“分问、依据、模型、求解、答案、验证”写作结构。这里的“标准”指完整可复用的工程结构；页面、字号和附录安排仍须按适用竞赛通知调整。

## 一条命令编译

建议安装含中文支持的完整 TeX Live 或 MiKTeX。必需组件包括 XeLaTeX、BibTeX、latexmk、CTeX、Fandol、TeX Gyre、gbt7714，以及常见数学与表格宏包；MiKTeX 的 latexmk 还需要可用的 Perl。

进入本目录后运行：

```sh
latexmk
```

`latexmkrc` 会自动执行 XeLaTeX、BibTeX 和必要的重复编译，输出 **`build/main.pdf`**。也可以显式执行 `latexmk -xelatex main.tex`。目录和文件名大小写应保持不变。

没有 latexmk 时，在本目录依次运行以下命令；此方式输出 `main.pdf`：

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

在线编辑器中将本目录内容作为独立项目上传，主文档选择 `main.tex`，编译器选择 **XeLaTeX**。参考文献使用 **BibTeX**，不使用 Biber。

## 文件与编辑位置

| 文件 | 用途 |
| --- | --- |
| `main.tex` | 题目、章节顺序、文献表入口 |
| `modeling.sty` | A4、25 mm 页边距、小四正文、字体、标题与图表样式 |
| `sections/abstract.tex` | 先从已核验结果取数，再按问题填写摘要 |
| `sections/problem-analysis.tex` | 题意、交付物、方法选择与分问依赖 |
| `sections/assumptions-symbols.tex` | 有依据的假设与带单位的符号表 |
| `sections/model-q1.tex` | 一问的依据、推导、实现、结果和验证 |
| `sections/evaluation-conclusion.tex` | 有证据的评价、局限、改进和逐问结论 |
| `sections/appendix.tex` | 复现入口、AI 记录与可删除的排版示例 |
| `references.bib` | 正文和附录实际引用的文献 |
| `latexmkrc` | 编译链与输出目录 |

使用 TeX 发行版自带的 Fandol 和 TeX Gyre 字体，不需要复制商业字体或旧模板的类文件。摘要后另起一页，正文自然分页；这些是可修改的工作默认值，并非已核验的官方规则。

## 分问、图表和文献

增加问题二时，复制 `sections/model-q1.tex` 为 `sections/model-q2.tex`，修改标题，将文件中 **全部 `q1` 标签和引用改为 `q2`**，并在 `main.tex` 添加 `\input{sections/model-q2}`。公式、图、表、章节标签都必须唯一；正文使用 `\eqref{eq:q2-model}`、`\ref{tab:q2-results}` 等自动引用。

真实图像可以放入新建的 `figures/` 目录，以如下内容替换附录中的占位示例。路径是相对于 `main.tex` 的，首次使用前须确保文件存在：

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\linewidth]{figures/q1-result.pdf}
  \caption{填写真实对象、条件与单位}
  \label{fig:q1-result}
\end{figure}
```

在 `references.bib` 添加核验过的条目，并在相关句子后写 `\cite{文献键}`。默认采用 [gbt7714 的顺序编码 BibTeX 样式](https://ctan.org/pkg/gbt7714)，文献表自动生成一次，不要再手写“参考文献”标题或使用 `\nocite{*}` 填满清单。

附录默认引用一条真实的 [amsmath 官方用户指南](https://www.latex-project.org/help/documentation/amsldoc.pdf)，仅演示引用链和公式排版。元数据按该 PDF 首页的版本 2.1、2020-02-18 修订信息核验，访问日期为 2026-09-10。该条不是赛题文献；删除“排版示例”整节时同时删除示例条目，并加入实际查阅、实际引用的文献。若当前草稿确实没有引用，可暂时注释 `main.tex` 的两条 bibliography 命令，避免空文献表警告。

## 成稿前检查

- 替换全部 `\slot{...}` / `〔待填：…〕`，删除填写说明、空表和“排版示例”整节。
- 摘要、正文、图表与结果台账使用同一组真实数字；未执行的计算、验证和人工核验保持未完成状态。
- 按适用要求调整匿名信息、页数、摘要、参考文献和 AI 披露安排。
- 重新编译并逐页查看 PDF，检查缺字、图表位置、公式与文献引用、重复标签和溢出。模板可编译不代表填入内容后无需检查。

写作细则见仓库的 [优秀论文风格指南](../references/writing-style.md) 和 [模板提炼依据](../references/template-guide.md)。本目录不依赖本地资料库，可单独复制使用。

验证记录：2026-09-10，在 Windows + TeX Live 2025 中从独立复制目录运行 `latexmk`，自动完成 XeLaTeX、BibTeX 和后续重编译，生成 4 页 PDF。最终日志无未定义文献、未定义交叉引用、重复标签、缺字、Overfull 或 Underfull 提示；全部页面已渲染检查。页数仅反映当前空模板，不是成稿限制。
