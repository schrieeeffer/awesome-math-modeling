# LaTeX 论文工程

一个可独立编译的中文论文起点，包含分章源文件、图表样式、BibTeX 引用和正文页数标记。复制到项目目录后，按本届要求和参考论文调整结构与样式。已有适用的官方模板时，可直接在官方工程中写作。

## 编译

本地建议使用带中文支持的 TeX Live 或 MiKTeX。主要依赖为 XeLaTeX、BibTeX、latexmk、CTeX、Fandol、TeX Gyre、gbt7714、zref 及常见数学和表格宏包；MiKTeX 运行 latexmk 还需要 Perl。

在本目录执行：

```sh
latexmk
```

配置文件 `latexmkrc` 会调用 XeLaTeX，将结果输出到 `build/main.pdf`。也可以使用 `latexmk -xelatex main.tex`。

初始引用库为空。在 `references.bib` 中添加文献、正文中加入 `\cite{文献键}`，再将 `main.tex` 中的 `\usebibliographyfalse` 改为 `\usebibliographytrue`，latexmk 就会自动运行 BibTeX。

没有 latexmk 时，空模板运行两次 XeLaTeX 即可；启用文献后依次执行以下命令，输出为 `main.pdf`：

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

## 在哪里修改

| 文件 | 编辑内容 |
| --- | --- |
| `main.tex` | 题目、章节顺序、声明与文献开关、正文和附录边界 |
| `project-style.tex` | 当前项目的字体、间距、页边距、标题和题注设置 |
| `modeling.sty` | 模板默认样式与公共命令 |
| `sections/abstract.tex` | 摘要及关键词 |
| `sections/problem-analysis.tex` | 题意、方法选择与各问之间的联系 |
| `sections/assumptions-symbols.tex` | 假设、符号和单位 |
| `sections/model-q1.tex` | 一问的模型、求解、结果与验证 |
| `sections/evaluation-conclusion.tex` | 模型评价、局限和结论 |
| `sections/ai-statement.tex` | 按实际使用情况填写的简短声明 |
| `sections/appendix.tex` | 结果明细、支撑文件清单和程序 |
| `references.bib` | 实际查阅并在论文中引用的文献 |
| `examples/` | 单独编译的排版演示 |

模板中的 `\slot{...}` 会显示为 `〔待填：…〕`，用来标记尚未完成的内容。写作时先填模型、结果和验证，再从确定的结论整理摘要。

增加问题二时，复制 `sections/model-q1.tex` 为 `sections/model-q2.tex`，将其中的 `q1` 标签及引用统一改为 `q2`，然后在 `main.tex` 中加入：

```tex
\input{sections/model-q2}
```

章节也可以按任务或主题重新组织。需要英文 Summary Sheet、信函或不同文档类时，直接调整 `main.tex` 和相应章节。

## 调整样式

默认使用 A4 纸、25 mm 页边距、小四正文、黑体标题、宋体正文；摘要首段缩进两个字，关键词加粗。中文字体来自 TeX 发行版的 Fandol，英文使用 TeX Gyre，便于本地与在线编译。

`project-style.tex` 在默认样式之后加载，适合集中存放本项目的覆盖设置。样式依据可记录在 [参考论文画像](../assets/reference-profile.yaml) 中；具体提取方法见 [参考论文适配](../references/reference-adaptation.md)。

这些默认值用于开始写作，正式格式由当前比赛要求决定。

## 插入图表和文献

在工程内新建 `figures/`，放入由实际结果绘制的图。例如：

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\linewidth]{figures/q1-result.pdf}
  \caption{填写图中对象、条件与单位}
  \label{fig:q1-result}
\end{figure}
```

图片路径相对于 `main.tex`。正文用 `\ref{fig:q1-result}` 引用图片，用 `\eqref{eq:q1-model}` 引用公式；各标签保持唯一。

文献条目从期刊、会议或出版社的原始页面核验后写入 `references.bib`，在对应论述处引用。默认采用 [gbt7714 顺序编码样式](https://ctan.org/pkg/gbt7714)，启用后自动生成参考文献标题和列表。

[`examples/`](examples/README.md) 中另有公式与引用演示，主论文不加载该目录，提交源件时可将它留在工作区。

## 正文、附录与页数

模板将摘要单独分页，正文包含模型章节、启用的 AI 声明和参考文献，随后另页进入附录。声明是否保留可通过 `\includeaistatementtrue` 或 `\includeaistatementfalse` 设置，内容按真实用途和本届要求填写。

`.aux` 文件提供以下物理页标记；使用 latexmk 时文件位于 `build/main.aux`。

| 标记 | 含义 |
| --- | --- |
| `skill:body-start` | 正文第一物理页 |
| `skill:body-end` | 正文及其浮动图表的最后物理页 |
| `skill:appendix-start` | 附录第一物理页 |

页数为末页减首页加 1。标记使用 `\zref@newlabel` 中的 `\abspage`，因此不受页脚重新编号影响。`\skillendbody` 会先排完正文浮动图表，再记录末页。计页范围随比赛规则调整，最终核对实际 PDF。

从仓库根目录运行检查示例：

```sh
python scripts/check_delivery.py --root latex-template/build --pdf main.pdf --aux latex-template/build/main.aux --body-limit 30
```

这里的 `30` 换成本届页限；使用与 PDF 同次编译的 `.aux`，其相对路径从运行命令的目录计算。脚本需要 Python 3.10 或更新版本，读取 PDF 需要 `pypdf`。

## 上传到 Overleaf

将本目录的工程文件上传为一个项目，主文档选择 `main.tex`，编译器选择 **XeLaTeX**。参考文献采用 BibTeX。图片、章节和文献文件一并上传，并保留路径与大小写。

在线源件和本地 PDF 使用同一份最终内容。编译后检查中文字体、公式、表格换页、引用及正文页数。

## 定稿检查

- 将待填内容替换为实际论证与结果，清理空表和填写说明。
- 摘要、正文和图表使用一致的数值、单位和比较基准。
- 在正文呈现主要答案与要求的汇总表，明细和程序按规则放入附录及支撑材料。
- 根据当前支撑目录更新附录清单，核对匿名信息与 AI 使用说明。
- 重新编译并查看各页，处理缺字、重复标签、未定义引用和内容溢出。

写作可参考 [论文写作指南](../references/writing-style.md)，模板来源与历史检查记录见 [模板指南](../references/template-guide.md)。
