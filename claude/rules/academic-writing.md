# Academic Writing Rules

> 下游消费点：`~/.codex/AGENTS.md` §9 Domain Overrides（指针，Codex 审稿/编辑论文前读本文件全文）。本文件是唯一权威。

- When reviewing or editing academic papers, ALWAYS read ALL relevant files completely before providing feedback. Never give shallow reviews based on partial reading.
- When asked to rewrite or restructure content, do a genuine structural rewrite — do NOT fall back to trimming, simplifying, or making cosmetic edits. If the user says "restructure" or "重构", that means rebuild from scratch following the new structure.
- When reviewing, provide paragraph-level critique with specific file and line citations. Never give surface-level comments.
- Never make unverified claims during review. If uncertain, explicitly state so.
- **学术态度**：论文结论 = 作者声称（非既定事实）。评估综合考虑期刊声誉、实验条件、可重复性。质疑优于转述；证据强度 > 引用量。区分"广泛采用"与"被证明正确"。结论矛盾时主动指出分歧并分析原因。
- 写批判分析、future directions、limitations 时：简洁、可操作、有新意。避免 meta-commentary（如"可以发展为完整工作"）、避免强行关联原文、避免列举显而易见的局限性。
- **编辑纪律**：按 CLAUDE.md §2 改前确认、§4 最简方案执行；"润色 / 改一下 / polish" = 微调措辞不是重写。
- **迭代节奏**：用户说"润色 / polish / 改一下 / 优化"且**未指定批次**时，默认**一次只输出一段 diff**，等确认再进入下一段。不适用于用户明确要求的"全文重写"。
- **删减守恒**：编辑学术文本时，删减的内容不超过用户指定范围。大幅删减（>30%）先列出删减清单并等确认。"精简/缩写" ≠ "砍掉一半"。
- **字数约束传递**：用户指定字数/字符限制时，将限制显式写入编辑方案，编辑后报告实际字数。
- 接地原则（Grounding）：写 Related Work、文献综述等引用密集段落时，优先引用内容已被实际验证过的论文（通过 paper-note-generator 阅读、PDF 文本提取、或 ai4scholar 摘要检索）。对于仅凭记忆引用但未实际阅读的论文，标注 `[CLAIM_UNVERIFIED]`。
- **本地优先检索**：学术 skill（`paper-note-generator`、`validate-bib`、`writing-style` 等）启动时，**先用 Glob/Grep 扫本地已有的** paper notes 归档、`paper/references.bib`、`evidence/` 目录。本地已覆盖 → 直接复用引用；**仅在**本地缺失或需补充最新文献时才调用外部搜索（ai4scholar / arXiv / firecrawl）。
- **BibTeX 来源硬规则**：BibTeX 条目**只**从 DOI / arXiv ID / ai4scholar / CrossRef **程序化**获取，禁止凭记忆构造 author/title/year/venue/pages。无法验证时用 `[CITATION NEEDED]` 或 `\cite{PLACEHOLDER_*}` 占位，明确交用户补，不得混入正文伪装成真引用。
- 引用具体数字（citation count、h-index、下载量等）或填写 survey / 论文模板中的引用数据时，**必须通过 ai4scholar 或其他程序化来源验证**，禁止凭记忆；"paper X 有多少引用"视为搜索任务。验证失败写"citation count not verified"，不要猜。

## Writing Tone

> 通用 de-AI 写作纪律（词汇/句式/段落三层）见 `rules/writing-tone.md § 通用 De-AI 写作纪律`，适用于所有文字产出。以下为学术写作特有补充。

- **学术英文禁用词**：adaptive, leverage, robust, delve, utilize, facilitate, streamline, comprehensive, cutting-edge, novel, notably, furthermore, pivotal, paradigm, holistic, underscore, underpin, realm, embark, unveil, encompass, differentiate, pave the way, remarkable, breakthrough, transformative（学术 claim 或统计术语除外）。**频率敏感**：偶尔一次 = MINOR（标注但不强删），同一术语全文 3+ 次 = MAJOR（必须替换或给充分理由）。这是风险扫描，不是无条件禁令。
- 编辑时保留作者原有措辞风格，不统一为"AI 标准英语"。详见 `writing-style` skill。
- **qualifier 保护**：以下 claim-calibration 词删除前必须显式询问 —— `几乎 / 几乎完全 / 大多数 / 绝大部分 / 约 / 大约 / 部分 / 可能 / 倾向 / 似乎 / suggests / likely / partially / mostly / nearly`。即使超字数也要询问，不自作主张删。
- **Confidence-calibration cue 区分**：引导句（如 `Notably / Interestingly / It is worth noting / 值得注意的是 / 一个有趣的现象是`）≠ 上一条的 scientific qualifier。前者按学术功能判断：后接具体新发现/对比/数据时保留（合法 calibration），后接空泛叙述或堆 hedge 时删。后者（嵌入 claim 的 qualifier）不可删。
- **反绝对化用词**：写作和编辑时避免绝对化表述，遇到时主动建议替换。obvious → straightforward, always → generally/usually/often, never → rare, avoid/eliminate → alleviate/relieve。此规则与上方 qualifier 保护互补——一个是"别删弱化词"，一个是"别用绝对词"。

## 论文写作最佳实践

- **流程**：先完整稿再优化（Phase 1 内容优先不纠结措辞，Phase 2 de-AI + claim 校准 + 漏洞检查）。Introduction 写两遍：早期版本是思维工具（约束后续实验设计），evaluation 完成后从 evidence 出发重写。
- **摘要/Intro**：立重要性不朴素（反例"没人做就做"）；Intro 采用"大领域 → 本领域 → 缺失问题 → 我们贡献"四层叙事
- **Related Work**：按主题分组，不逐篇堆砌，每组结尾回扣本文差异（"Unlike these works..."）
- **结论**：每个 claim 必有实验/数据支撑，用 "suggests" 不用 "proves"，scope 明确界定
- **可读性五透镜**（审稿和自查时用）：(1) Logical Strength——逻辑连贯性来自逻辑本身，不是连接词堆砌 (2) Defensibility——每句话要经得住"凭什么这么说？"的追问，claim 要有 reference 或 evidence 紧跟 (3) Confusion Time——读者从"这是什么"到"我懂了"的总耗时要短；概念提出后就近解释，不要让读者翻页才知道什么意思 (4) Information Density——正文不写人人都知道的背景、不堆实验细节（放 appendix）、图表自解释 (5) Takeaway Discipline——每组相关实验后必须有解释段陈述 pattern 并回扣 claim，不能只摆数字让读者猜
- **终检**：引用交叉验证（DBLP + ai4scholar，必要时 CrossRef / arXiv，核对作者/年份/会议/页号）+ 数据合理性（数学可能性、内部一致性）
- **多源报告的来源账本**：综述 / 调研报告这类多源产出，正文末尾附一小段台账：看过哪些源（数量或列表）、采纳了哪些、丢了哪些（死链 / 存疑 / 被推翻）、整体验证状态（已验证 / 有保留 / 受阻）。

## 探索性 / 提议性文档

研究探索阶段的种子文档（research seed / proposal draft / 调研 brief）写作纪律：未经调研的方法、实验、贡献不以确定性表达呈现，必须用 hedge 语言（"可能 / 觉得 / 暂时想到"），避免"必然 / 已被证明可行 / isomorphic / motivating precedent"这类强确定性词；文档核心是待回答的问题清单，不是 contribution 列表 + 预期实验 + 结论段；能用中文说清的不堆英文 jargon。完整工作流和 anti-pattern 检查见 `research-idea` skill（seed-brief mode）。
