# Related-work writing notes（相关工作写作学习笔记）

吸收循环的入口，全 skill 只维护这一个学习笔记，不按领域另建档案。用法：写新论文前，读 3-5 篇同类中稿论文，先提炼每篇赖以成立的核心写作动作（它重新定义了什么对象、提出了什么能力问题、把哪个争论变成了可测问题），以及这个动作成立所需的贡献形态和证据条件；把自己的 running example 放进这个动作里走一遍，走得通才记成条目、写作时模仿，走不通就记下缺的前提，留作判断力。论文完稿后，跨 paper type 稳定成立的 voice、节奏与 claim 分寸蒸馏进 `personal-style-profile.md`；只对某类 story 成立的动作留在本文件，连同它的适用条件，条目适时压缩或清理。

每个条目记三样东西：**故事骨架**（这一子领域怎么讲故事）、**修辞动作**（关键段落怎么写、防什么质疑、成立的前提）、**可借鉴表述**（例句加上它完成的修辞工作）。例句一律自包含，可直接当模板改写，不依赖读过原论文。

## 出题合成（problem synthesis）子领域（2026-07 为交互算法题合成项目调研，四篇同类论文：三篇正面参考，一篇反面教材）

### 故事骨架（五步）

1. **能力-局限开场**：先承认 LLM 在某个 coding regime 已经很强，一个转折词转入局限。"LLMs now excel at well-defined coding tasks ... Yet these settings are mostly closed-ended."
2. **数据瓶颈当反派**：稀缺 / 耗尽 / 污染 / 人工成本，选其组合并用一句话钉死。范本："This gap reflects a data asymmetry: verified closed-ended tasks are abundant, while open-ended tasks remain scarce."
3. **关键洞察或可行性设问**：断言机制（"Our key insight is that closed-ended problems can serve as seeds ..."）或提问（"Can we bypass the reliance on real-world data ... using fully synthetic data?"）。设问版在结尾有更干净的叙事回报。
4. **先解决信任再谈效用**（子领域的定义性动作）：合成物读者的第一反应是"它可信吗"，必须在 claim 效用之前回答。四条腿，越多越强：
   - 下游对齐人工数据："our synthetic problems achieve competitive or superior performance to human-curated training data on both benchmarks"
   - 对照实验排除混淆：闭式种子对照加随机奖励对照，"confirming that open-ended formulations and genuine reward signals are both necessary"
   - 复现真题的已知行为签名："our synthetic problems match these patterns, suggesting they capture the same structure as human-curated ones"
   - 验证器可靠性数字："this voting strategy achieves 94.7% labeling accuracy with 8 sampled solutions"
   赢面句式：合成数据在方法没有直接优化的轴上约等于或超过人工数据。
5. **编号贡献 + 数字预告**收尾 intro。

### 反面教材的教训

信任只靠可靠性百分比加夸大收尾撑（"redefines benchmarking standards and facilitates the creation of safer AI technologies"），没有下游效用可指；结论几乎逐句复述摘要；"paves the way for ..." 是无界承诺。教训：合成-评测类论文没有 training gain 可指时，信任故事最脆，需要对照实验或人类研究补上。

### 工程惯例

正面范本把每个结果数字定义成宏（`\newcommand{\resultA}{10.62}`），差值用 `\FPeval` 自动计算，摘要 / 正文 / 表格数字不会漂移。已收录进 `latex-project-structure.md`。

## 课题组风格（代码审查 benchmark，FSE 中稿），未来合作对齐用

结构：定义式开头（"Code Review (CR) is an indispensable quality assurance practice ..."）接 "However / To bridge this critical gap" 转折，编号贡献，每个 RQ 结尾盒装结论（`\mybox{Conclusion N}{...}`），加粗 `\paragraph{}` 子分析，Threats to Validity 按 Internal/External/Construct 三分，一段式 Conclusion。

习惯：术语自造并当场辩护（"We use the term `change` rather than `fix` or `defect` because ..."）；每个 claim 后面跟 `\cite{}` 或数字；分级 hedge 词汇（strongly suggests / speculatively points to / we hypothesize）；把设计成本写成优点（"This setup is intentionally more challenging, yet more aligned with real-world practices"）；三段式列举和连接词密度偏高，组内接受。

## 英语母语团队可借鉴表述（同域中稿论文）

- "Recent reports claim that ... we revisit this claim"（摘要开头点名要挑战的对手主张，rebuttal framing）
- "Writing competitive programming problems is exacting."（冷开场：一句陈述难度，零铺垫）
- "problem setting encompasses all the challenges of solving a problem, and then more."（干净的不对称句，不搞强行排比）
- "LLMs can generate solvable problems that they themselves are unable to solve."（发现写成一行悖论）
- "the apparent difficulty of a problem drops sharply / collapses / evaporates"（同一概念换用生动动词，不重复 decreases）
- "often generating confidently incorrect justifications"（紧凑可记的失败模式命名）
- "both the human expert and the model produce valid packings, but the human achieves 87% density while the model achieves only 47%."（一个贯穿全文的 running example 用两个数字把 gap 演出来）
- Finding 可以直接做小节标题（"Misleading Micro-Optimization Trap"）；发现命名要陈述结果，别起品牌名（反例："Good-gets-Better Principle"）
