# 资料覆盖、证据索引与维护

## 本次蒸馏做到了哪一层

资料根目录的原始五个资料文件夹均纳入递归清点，原件未修改。这里把“全量文件覆盖”和“逐页内容审阅”分别记录；不能把可提取文字或目录中的奖项标签当成内容已经验证。

| 层级 | 本次范围 | 能支持什么 |
|---|---|---|
| 原始文件全量索引 | 1,504个文件，2,663,413,228字节；SHA-256去重后1,397份，107个重复文件 | 查找来源、原路径、大小、重复关系和处理状态 |
| PDF原生文本提取 | 535份PDF，共11,409个物理页；185份通过基本文本量/汉字覆盖检查，252份低文本量，98份文本层可疑 | 检索可读文字；可疑和扫描文件需进一步看图/OCR，不能根据字符数宣称全文可读 |
| 旧Word转换 | 原始及压缩包共262个DOC路径，240个不同内容；237份转换成功，覆盖259个路径，另3份失败 | 成功文件可搜索正文；转换不等于所有公式、图形都已准确解析或逐页审读 |
| 压缩包递归索引 | 原始64个ZIP/RAR；计入嵌套后索引4,531个成员，总目录6,035行；相同嵌套档案通过同内容ID关联 | 发现压缩包内论文、题目、数据、代码；成员数包含不同路径下重复副本，不是独立论文数 |
| 历史论文/讲评选读 | 32个案例：10个文本选读、14个视觉选读、8个仅摘要视觉；覆盖1993–2025之间13个年份，含2022图片论文 | 风格、分问结构、公式组织、图表论证和反例；每条卡片标实际页码与适用边界 |
| 模板与提示词 | Word/LaTeX/AI记录模板结构和代表页；两套提示词目录21份DOCX，按正文去重13组 | 可编辑模板、可执行流程及需要剔除的固定数据/营销要求 |
| 代码静态抽查 | 8份MATLAB附件，跨6个原目录年份 | 变量、单位、路径、索引、随机性和复制错误的复现检查经验；未执行源代码 |

统计以 [corpus-summary.json](corpus-summary.json) 为准。完整原始及档案成员索引在 [corpus-catalog.jsonl](corpus-catalog.jsonl)，不要默认把整个大文件加载到上下文。

原始图片共504个文件，其中499为JPG；36个原始MP4以及档案内视频没有逐一转写，二进制数据与旧PPT没有逐一内容解析。2022两份图片论文只选读卡片所列页，其他图像大多仅记录尺寸和路径。一个约490MB的CSV只抽取表头及前5条记录确认格式，没有据此总结全量数据。

三份旧Word的失败已保留错误原因：`Saa43531091d0`（2004临时迷你超市）、`S09db6e13af62`（2009 A题）、`A14cb07c98479`（2012档案中的20121784.doc）。Word报告损坏或文件问题；未通过关闭保护绕过，也不将其当作已读内容。

## 哪些规则来自哪里

- 历史论文案例使用 **P01–P32**；卡片中 **S…** 表示原文件索引ID。图片论文一页对应一个S编号，按数字页号排序。
- 培训提示词使用 **W01–W22**；其 `P014` 等定位是提取时的段落编号，**不是PDF页码，也不是历史论文P14**。复核时用 prompt-distillation.md 的源文件与段落提取记录。
- 压缩包内成员使用 **A…**；`path` 以 `!/` 分隔档案边界，`archive_id` 指到父档案，`member` 保留实际成员名。
- 建模决策表、结果台账、数据泄漏防护和验证框架中标为综合设计/纠偏的内容，是蒸馏后的工作规则，不声称每篇历史论文都遵守。
- 没有以目录标题验证奖项，也没有联网认定本地所谓“2026官方规则”。需要当届规则时回到主办方原文。

## 定向检索原件

在技能目录运行以下命令；也可把脚本写成绝对路径从任意目录调用。脚本仅用Python标准库，不运行资料中的代码。

```powershell
python scripts/search_corpus.py "种植" --year 2024 --ext pdf --limit 8
python scripts/search_corpus.py "供应商" --content --limit 6
python scripts/search_corpus.py --id S4190f2ed8e7b
python scripts/search_corpus.py "logistic" --ext m
```

检索词以空格分隔时要求全部命中。默认检索原路径；`--content` 才扫描本地抽取正文。结果默认隐藏重复内容，也可用 `--include-duplicates` 查看副本。`--year` 使用原文件近层目录/文件名推断的 `year_hint`，不把“1992-2017合集”当成每篇的年份；它仍是检索提示，需要原件核实。

`--id` 可直接定位具体案例；内容命中返回短片段及可确定的PDF物理页号。结果的 `status` 表示自动处理状态，`review_depth` 表示是否有另外的实际审阅；片段不证明全文正确。扫描、疑似缺字和公式必须打开原页查看。页号来自PDF分页符，Word正文没有强行生成伪页码。

公开仓库只包含索引和蒸馏成果，不包含原件、抽取全文、转换副本或原项目的 `_distillation/` 中间资料。默认路径检索无需本机配置。进一步搜索正文时，需要自行准备与索引 `text_path` 对应的抽取文本，并通过 `--text-root` 指向抽取根目录（其下通常有 `text/来源ID.txt`）：

```powershell
python scripts/search_corpus.py "供应商" --content --text-root "../my-corpus/_distillation" --limit 6
```

可选配置的公开示例为 [local-corpus.example.json](local-corpus.example.json)。复制为同目录的 `local-corpus.json` 并修改路径，或用 `--config` 指定另一份 JSON。配置中的相对路径按配置文件所在目录解释；显式 `--text-root` 优先，命令行相对路径按当前工作目录解释。`source_root` 记录原件位置，`extraction_root` 用于正文搜索；抽取根目录可同时保留 `legacy_docx/`、`archive_members/` 等本机副本。`local-corpus.json` 仅供本机使用，应保持被 Git 忽略。

```powershell
python scripts/search_corpus.py "供应商" --content --config "../my-corpus/settings.json"
```

配置、原件或抽取目录不可用时，蒸馏后的规则、案例总结、模板和路径索引仍可独立使用。正文搜索会明确提示缺少哪项本地依赖，不应据此阻塞普通建模或写作任务。

## 处理状态的准确含义

| 状态 | 含义和下一步 |
|---|---|
| text_extracted | 已抽取原生文本，基本启发式通过；公式、表格和版式仍需原页核对 |
| legacy_text_extracted | DOC经Word另存为DOCX后提取了文本；不保证嵌入对象完整 |
| needs_ocr | 原生文本很少；按具体任务渲染/OCR并核对公式、表格、页序 |
| text_layer_suspect | 中文资料中文字形覆盖很少；也可能是英文或公式材料，须看图判断，不能自动判为坏文件 |
| image_not_ocr / video_not_transcribed | 文件已登记，内容没有全量OCR/转写；选读图片另有review_depth记录 |
| binary_indexed / archive_member_indexed | 已登记路径和元数据，未完成语义解析 |
| large_csv_header_sampled | 仅表头和少量样本核对；不代表全量数据质量已检查 |
| legacy_conversion_failed | 保存实际失败原因；不引用尚未成功读取的内容 |
| nested_archive_listed / nested_archive_duplicate | 已列成员，或成员集合由相同内容的另一档案代表 |
| raw_markup_extracted | 保留原始标记文本，非已还原的排版/正文 |

## 维护与质量验证

新增资料时先做来源和内容去重，再按新题型或已有结论缺口选读，不把资料堆进SKILL.md。只有新的证据改变选型、写作或检查动作时才扩充参考；具体案例放case-evidence.md，并记录物理页号和阅读深度。某篇的偏好不升级为所有论文的硬要求。

本次生成和抽取过程保留于原项目 `_distillation/`，包括build_corpus.py、augment_corpus.py、extract_legacy.ps1、finalize_catalog.py及三个分工的观察记录。这些是维护审计资料，不是常规使用依赖；重新运行抽取会更新中间记录，应先保留已有人工标注。

本次交付检查包括技能frontmatter与链接、模板编译/原生分页视觉检查、检索脚本和独立摘要试用。试用仅修改摘要，正确使用现有结果、限制最优性措辞并标记未做验证；这证明该场景可用，不代表在所有竞赛题上已经验证建模能力。具体运行记录保存在项目 `_distillation/validation/` 与 `_distillation/forward_test/`。
