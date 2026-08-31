# Introduction 写法（top venue）

Introduction 的核心是六个功能位的逻辑链：

1. **Background + Running Example**：场景重要性 + 一个贯穿全文的具体例子
2. **Existing Limitations**（≤3）：现有工作具体做不到什么
3. **Problem / Goal**：本文要解决什么（一句话）
4. **Key Challenges**（≤3）：为什么不能直接做，难在哪
5. **Solution Overview**：我们怎么做的（一段高层概括）
6. **Contributions**：本文贡献列表

**核心纪律**：limitation→challenge→method module→contribution 每个箭头都要能追溯，任何一个断了就是结构问题。功能位是清单，篇幅和顺序由论文的核心概念动作决定：这篇论文赖以成立的那个动作（新维度、新对象、新能力问题）占最大篇幅，其余功能位可以合并成一两句，逻辑链完整即可。

**Technique vs Benchmark paper 区别**：technique paper 的叙事轴是 Key Idea/Mechanism；benchmark paper 的叙事轴是 Evaluation Gap + Benchmark Design Rationale，problem definition 本身就是贡献，实验目的是"揭示能力边界"不是"证明我最好"。Benchmark intro 的功能位替换为：Background + Running Example → Existing-Benchmark Limitations → Research Questions → Design Considerations → Our Proposal → Contributions。

**Running example**：intro 里引入的例子必须在 Method（作为 walkthrough）和 Experiments（作为 case study）中兑现，不能用完就丢。

## Prior-work 段落形状

根据论文与已有工作的关系选择最自然的展开方式：

1. **Challenge chain**：传统方法处理了早期困难，近期方法继续推进，但目标场景中的具体问题仍未解决。最后一个 limitation 要准确落到本文处理的 challenge。
2. **Insight with history**：经典方法已经包含与本文 insight 相近的思想。先用这条历史线建立学术来源，再说明它在当前任务中的覆盖不足，最后引出本文的技术载体。
3. **Novel task decomposition**：缺少直接 prior work 时，先定义新任务，再把困难拆成几个读者可以分别理解的 challenge，随后引出完整方案。

增量工作也应从真实 technical challenge 起笔。直接摆出一个 naive 方案再逐项改进，会让读者把贡献理解成顺手补丁，并提前消耗本应由问题产生的好奇心。

## Limitation 措辞

- 从对方覆盖范围切入，不贬低前人："X 存在严重缺陷"改为"X 聚焦于……而未涉及……"
- 引用最接近的工作并指出它具体做不到什么，不写泛泛的"现有方法存在不足"
- gap 句紧跟后果：这个缺口不补，读者或领域损失了什么

## 自查清单

- [ ] 开头具体不泛泛，有 running example
- [ ] 最相关工作被引用并直接比较
- [ ] gap 一句话可指认，紧跟后果
- [ ] limitation→challenge→module→contribution 链条完整可追溯
- [ ] 每条贡献都能指认其在实验叙事中的角色或实际结果
- [ ] 无过度声称（"first"必须窄限定）
