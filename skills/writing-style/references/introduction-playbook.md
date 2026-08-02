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

## Limitation 措辞

- 从对方覆盖范围切入，不贬低前人："X 存在严重缺陷"改为"X 聚焦于……而未涉及……"
- 引用最接近的工作并指出它具体做不到什么，不写泛泛的"现有方法存在不足"
- gap 句紧跟后果：这个缺口不补，读者或领域损失了什么

## 自查清单

- [ ] 开头具体不泛泛，有 running example
- [ ] 最相关工作被引用并直接比较
- [ ] gap 一句话可指认，紧跟后果
- [ ] limitation→challenge→module→contribution 链条完整可追溯
- [ ] 贡献 2-4 条，每条在实验中有对应验证
- [ ] 无过度声称（"first"必须窄限定）
