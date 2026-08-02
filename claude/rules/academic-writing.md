# Academic Writing Rules

> 审稿 / 编辑 / 写作论文时生效。Codex 侧经 `~/.codex/AGENTS.md` §4 指针读本文件；本文件是唯一权威。

## 审稿与编辑
- 审稿 / 编辑前完整读所有相关文件，段落级批判带 file:line 引用，不做浅审；不做未验证 claim，不确定就明说
- 论文结论 = 作者声称，非既定事实；质疑优于转述，证据强度 > 引用量；区分"广泛采用"与"被证明正确"；结论矛盾时主动指出分歧并分析
- "润色 / polish / 改一下" = 微调措辞；"重构 / restructure" = 从头按新结构重写，不许退化成修修剪剪。批判分析 / limitations 要简洁可操作，不写 meta-commentary、不列显而易见的局限
- 润色未指定批次时默认一次一段 diff 等确认；删减不超用户指定范围，大删（>30%）先列清单确认（精简 ≠ 砍半）；用户给字数限制时显式写进方案并报告实际字数
- qualifier 保护：`几乎 / 大多数 / 约 / 部分 / 可能 / 倾向 / suggests / likely / partially / mostly / nearly` 等 claim-calibration 词删除前必须询问，超字数也不自作主张。引导句（Notably / 值得注意的是）另判：后接具体新发现 / 数据保留，空泛则删
- 反绝对化：obvious → straightforward，always → generally / usually，never → rare，avoid / eliminate → alleviate / relieve

## 引用硬规则
- BibTeX 条目只从 DOI / arXiv ID / ai4scholar / CrossRef 程序化获取，禁凭记忆构造 author/title/year/venue；验证不了用 `[CITATION NEEDED]` / `\cite{PLACEHOLDER_*}` 占位交用户，不伪装真引用
- citation count 等数字必须程序化验证（ai4scholar 等），失败写 "not verified" 不猜
- Grounding：引用密集段优先引已实读验证的论文；仅凭记忆的标 `[CLAIM_UNVERIFIED]`
- 本地优先：学术 skill 启动先 Glob/Grep 本地 paper notes / `references.bib` / `evidence/`，本地缺失才调外部搜索

## 写作
- 动笔前先接地（铁律 3 的学术落地）：实读项目 story / 口径文档与同行真实范文，用用户已定口径复述叙事骨架等确认再写；禁止用自带学术模板、规律罗列、增量补丁替代用户的体系
- 面向真实读者（审稿人 / 选手）写，不面向内部术语体系（铁律 5）；保留作者原有措辞风格，不统一为"AI 标准英语"
- 流程：先完整稿再优化（内容优先 → de-AI + claim 校准）；Intro 写两遍（早期当思维工具，evaluation 后从 evidence 重写），四层叙事（大领域 → 本领域 → 缺失 → 贡献）；Related Work 按主题分组、每组结尾回扣本文差异；结论每个 claim 有数据支撑，用 suggests 不用 proves，scope 明确
- 学术英文禁用词（风险扫描非无条件禁令；偶现 MINOR，同词 3+ 次 MAJOR）：adaptive, leverage, robust, delve, utilize, facilitate, streamline, comprehensive, cutting-edge, novel, notably, furthermore, pivotal, paradigm, holistic, underscore, underpin, realm, embark, unveil, encompass, differentiate, pave the way, remarkable, breakthrough, transformative（学术 claim / 统计术语除外）
- 可读性五透镜自查：逻辑连贯靠内容不靠连接词；每句经得住"凭什么"；概念就近解释不让读者翻页；正文不堆常识与实验细节（放 appendix）；每组实验后有 takeaway 段回扣 claim
- 终检：引用交叉验证（DBLP + ai4scholar，必要时 CrossRef / arXiv，核对作者 / 年份 / 会议）+ 数据合理性；多源报告正文末附来源台账（看过哪些源 / 采纳 / 丢弃 / 验证状态）
- 探索性文档（research seed / brief）：未调研内容用 hedge 语言（"可能 / 暂时想到"），核心是问题清单不是贡献列表；完整工作流见 `research-idea` skill
