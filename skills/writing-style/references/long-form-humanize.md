# Long-Form Humanize（长文本去 AI 味工作流）

**This file is a companion to the language layers (`SKILL.md`).** 长文本（>~8000 中文字符 / >~12000 英文字符）、多节目录文档或跨会话续写场景加载本文件。短 snippet（<2000 字符）继续走所在语言层的常规工作流。

本文件提供三样东西：
1. **跨会话轮次状态持久化**（state manifest）
2. **硬分块 + 段落结构还原**（chunking + reassembly）
3. **扩展评分维度**（5×10 core + 2×10 long-form add-on）

---

## §1 Purpose & Scope

语言层的常规工作流按"一次对话改完"设计，对长稿会遇到三类问题：
- 单次 context 不足以装下整篇，导致截断或中途漂移
- 无法跨会话续写（新开一个对话就要从头读）
- 段落结构/编号/引用在大范围改写中容易错位

---

## §2 When to Use

**加载本文件的触发条件**（任一满足）：

- 文档总字符 > 8000（中文）或 > 12000（英文）
- 文档含多节目录（≥3 个 `#` / `##` / `1.1` 这类编号层级）
- 用户明确要求跨会话续写（如"继续上次的 humanize"/"按记录接着改"）
- 输入提及"长稿"/"全文"/"整篇"/"long-form"/"multi-session"

**不加载**（应直接用所在语言层的常规工作流）：

- 单段或短 snippet（< 2000 字符）
- 用户只要风格指导，不要改写产物
- 一次对话内可完成且无须落盘的场景

---

## §3 State Manifest

跨会话恢复依赖一份 JSON 状态文件。默认路径：目标文件同级的 `.humanize/humanize_record.json`。目录不存在时先创建。

### Schema

```json
{
  "doc_id": "/absolute/or/relative/path/to/target.md",
  "manifest_path": ".humanize/humanize_record.json",
  "chunk_limit": 850,
  "lang": "zh",
  "rounds": [
    {
      "round": 1,
      "focus": "surface-patterns",
      "input_path": "/.../原文.md",
      "output_path": ".humanize/round1.md",
      "chunk_manifest_path": ".humanize/round1_chunks.json",
      "chunk_count": 14,
      "scores": {
        "directness": 7,
        "rhythm": 8,
        "trust": 7,
        "authenticity": 7,
        "density": 6,
        "semantic_fidelity": 10,
        "pure_output": 10,
        "core_50": 35,
        "addon_20": 20,
        "total_70": 55
      },
      "timestamp": "2026-04-19T10:00:00Z"
    }
  ]
}
```

### 字段说明

| 字段 | 含义 |
|------|------|
| `doc_id` | 目标文件路径，作为跨会话恢复的 key；建议用绝对路径 |
| `manifest_path` | 当前 manifest 自引用路径，便于外部工具直接读取 |
| `chunk_limit` | 本次处理的单块字符上限（见 §4 默认值） |
| `lang` | `"zh"` / `"en"`，决定 chunk_limit 默认值与句末标点集 |
| `rounds[]` | 顺序追加数组，不覆盖历史 round |
| `rounds[].round` | 轮次编号，从 1 开始 |
| `rounds[].focus` | `"surface-patterns"` 或 `"voice-contract"`（见 §5） |
| `rounds[].input_path` | 本轮输入（R1 为原文，R2+ 为上轮 output） |
| `rounds[].output_path` | 本轮改写后文本落盘位置 |
| `rounds[].chunk_manifest_path` | 本轮切块索引文件（见下） |
| `rounds[].chunk_count` | 子块数量 |
| `rounds[].scores` | 本轮评分（见 §7） |
| `rounds[].timestamp` | ISO 8601 |

### Chunk Manifest（辅助 JSON）

每轮另存一份切块索引，按原段落还原时需要：

```json
[
  {"chunk_id": 1, "parent_paragraph_idx": 0, "char_start": 0, "char_end": 820, "char_count": 820, "flags": []},
  {"chunk_id": 2, "parent_paragraph_idx": 0, "char_start": 820, "char_end": 1340, "char_count": 520, "flags": []},
  {"chunk_id": 3, "parent_paragraph_idx": 1, "char_start": 0, "char_end": 780, "char_count": 780, "flags": ["unsplittable-citation"]}
]
```

`flags` 用于标记"整段保留不切"等特殊情况（见 §4）。

### 读写时机

- **开始本轮前**：读 `manifest_path` → 根据 `rounds[]` 确定下一轮编号 → 读对应 `input_path`
- **结束本轮后**：append 本轮记录到 `rounds[]`，更新 `timestamp`
- **不 rewrite** 既有 round 条目，只追加
- 若 manifest 不存在：视为第 1 轮，新建

---

## §4 Chunking Algorithm

### 默认参数

| 语言 | `chunk_limit` 默认 | 句末标点集 |
|------|-------------------|-----------|
| zh | 850 | `。！？；…` + `.!?;` |
| en | 1200 | `.!?;` |

### 伪代码

```
INPUT: text, chunk_limit, lang
OUTPUT: chunks[], chunk_manifest[]

1. 按空行切段落，每段记 original_index
2. For each paragraph p:
   a. len(p) <= chunk_limit → 整段作为单块
   b. else → 按句末标点贪心装填子块：
      cursor ← 0
      while cursor < len(p):
          next_boundary ← 最后一个 ≤ cursor+chunk_limit 的句末位置
          IF no such boundary OR HARD_GUARD_VIOLATED(boundary):
              调用 §4.2 的 fallback
          emit chunk [cursor, next_boundary]
          cursor ← next_boundary
3. 返回 chunks[] + chunk_manifest[]

REASSEMBLE(改写后的 chunks[]):
   按 parent_paragraph_idx 分组 → 组内按 chunk_id 升序拼接
   组间按 parent_paragraph_idx 升序 → 原空行分隔符插回
```

### §4.1 Hard Guards（任一命中则拒绝该边界）

- **术语/编号内部**：前后 ±3 字符含 CJK 字符+连字符组合，或数字+字母+下划线的 token
- **数字字面量/公式内部**：两侧均为 digit / `.` / `%` / `+-*/` 等
- **引用标记内部**：
  - `\cite{...}` / `\citep{...}` / `\citet{...}`
  - `[1]`, `[1,2]`, `[1-3]`
  - `（张, 2024）` / `（王等, 2023）` / `(Smith, 2020)` / `(Smith et al., 2020)`
- **代码 fence 内部**：三反引号块（```…```）或 inline code（单反引号对）
- **LaTeX 环境内部**：`\begin{…}` … `\end{…}` 之间（equation/figure/table/algorithm 等）
- **Markdown 链接/图片括号内部**：`[text](url)` 或 `![alt](url)` 括号对之间

### §4.2 Fallback 策略

1. 若当前段落找不到安全句界：`chunk_limit ← chunk_limit × 1.2`，重试一次
2. 重试仍失败：整段保留不切，在该 chunk 的 `flags` 中记录 `"unsplittable-<reason>"`（如 `"unsplittable-citation"`、`"unsplittable-codefence"`）
3. 如此产生的超长 chunk 在改写时提示用户："本段因 [原因] 无法安全切分，保持整段处理，可能占用较多 context"

### §4.3 Reassembly 验证

还原后必须满足：
- 段落数 = 原文段落数（通过 `parent_paragraph_idx` 去重计数）
- 标题/编号/引用位置与原文一致
- `\cite{}` 数量、`[N]` 数量、`（作者, 年）` 数量均不变

还原不一致时，拒绝写入 `output_path`，报告差异。

---

## §5 Pass Ordering

默认**两轮 focused pass**。两轮都以清除 AI 痕迹为目标，都受信息守恒守卫约束（见 `SKILL.md` 全局守卫）：删除只针对零信息模式，不以字数减少为目标。

### Round 1 — Surface Pass（词句级）

- **依据**：`patterns-english.md` 全目录（英文）/ `patterns-chinese.md` 全目录 + `chinese-writing.md` 总判据（中文）
- **处理目标**：模板开头、hedge stacking、list addiction、rhythm monotony、破折号滥用、AI 高频词、三段式列举、刻意换词等**词句级**机械化
- **不处理**：篇章级 voice（R2 的事）

### Round 2 — Voice-Contract Pass（篇章级，按语言选材料）

- **英文依据**：`paper-voice-contract.md` Categories 1-7。处理目标：R1 未清除的篇章级机器味：Planner Talk、Template Stems 残留、Hedge Stacking 深层堆叠、Symmetry Addiction、Citation Contamination、Grandiose Framing、Syntactic Over-Elaboration（分词解读尾、抽象名词主语）
- **中文依据**：`chinese-writing.md` 总判据 + `~/.claude/rules/writing-tone.md` 句式/段落级。处理目标：结构性重复、评价性收束残留、幽灵信息、假逻辑连接词、段落主题混杂。中文长文不加载英文 voice contract

### Override

| 参数 | 行为 |
|------|------|
| `rounds=1` | 仅执行 R1（快速粗打磨） |
| `rounds=N`（N ≥ 2） | 执行 N 轮，第 1 轮为 R1，后续轮均为 R2 focus |
| `rounds=iterate` | R1 → 重复 R2 直到 `total_70 ≥ 63` 且 `pure_output ≥ 9`，上限 4 次 |

用户可用自然语言指定，例如"按单轮处理"/"走 iterate 模式"/"跑 3 轮"。

---

## §6 Pure-Output Clauses（5 条铁律）

改写后的正文交付必须满足：

1. 禁止出现「修改后」「改写后」「可以改成」「如果你愿意」「以下是…」「候选版本」「润色建议」等元话语
2. 禁止呈现聊天式答疑、解释性前后缀、注解、备注、reviewer-style 评语
3. **段落角色保真**：原文是正文段就输出正文段，不得转成条目 / 摘要 / 候选标题
4. **编号与层级保真**：`1.` / `1.1` / `（一）` / `①` / `\section` / `\subsection` 等全部保留，顺序不变
5. 输出只含"已经改写完成的正文"，不附总结、不附评分（评分走单独通道，见 §7-§8）

基于文件的处理（非聊天直接粘贴）：正文只写入 `output_path`，对话中不重复贴出。

---

## §7 Scoring Extension

### 5+2 独立计分

短文本按 Core 5×10=50 计分；本文件加载时（长文本）追加 Add-on，总分记 /70。

**Core**（定义在本文件，唯一权威）：

| 维度 | 问题 | 范围 |
|------|------|------|
| Directness | 直接陈述还是绕圈宣告？ | /10 |
| Rhythm | 节奏变化还是机械重复？ | /10 |
| Trust | 尊重读者智慧吗？ | /10 |
| Authenticity | 听起来像真人吗？ | /10 |
| Density | 零信息套话是否清除？（不以字数减少计分，信息守恒由"语义保真"把关） | /10 |

**Long-form Add-on**（本文件新增）：

| 维度 | 问题 | 范围 |
|------|------|------|
| 语义保真 | 原文事实、论点、结论、因果关系是否完整保留？ | /10 |
| 纯净输出 | 输出是否含元话语/候选/聊天腔/解释性前后缀？ | /10 |

### 输出格式

```
Core: Directness /10 · Rhythm /10 · Trust /10 · Authenticity /10 · Density /10 → X/50
Add-on: 语义保真 /10 · 纯净输出 /10 → Y/20
Round total: (X+Y) / 70
```

### Gate 机制

- **`pure_output < 9`**：不推进到下一轮；报告问题位置，由用户决定是否手工修订或要求重跑当前轮
- **`semantic_fidelity < 9`**：同样作为硬门槛；这是比风格更重要的底线

### 评分标准

- 63-70：优秀，AI 痕迹清除且语义稳定
- 49-62：良好，仍有改进空间
- < 49：需重新修订

---

## §8 Per-Round Checklist Template

每轮结束后粘贴一份以下表格到对话或落盘：

```markdown
### Round <N> 评分（focus: <surface-patterns | voice-contract>）

| 维度 | 得分 | 备注 |
|------|------|------|
| Directness | /10 | |
| Rhythm | /10 | |
| Trust | /10 | |
| Authenticity | /10 | |
| Density | /10 | |
| **Core 小计** | **/50** | |
| 语义保真 | /10 | |
| 纯净输出 | /10 | |
| **Add-on 小计** | **/20** | |
| **Round total** | **/70** | |

高频问题块（chunk_id）：
- chunk <id>: <一句话问题描述>
```

落盘时同步写入 manifest `rounds[<N>].scores`。

---

## §9 Cross-References

本文件**只**管 workflow/state/scoring。具体改写规则查以下文件：

| 查找内容 | 去哪里 |
|---------|-------|
| 英文 de-AI 模式清单 | `patterns-english.md` |
| 中文 de-AI 模式清单 | `patterns-chinese.md` |
| 中文总判据与工作流 | `chinese-writing.md` |
| Voice 反模式 7 类 | `paper-voice-contract.md` |
| LaTeX 学术安全规则 | `style-apply.md` § De-AI in academic LaTeX |
| Core 5×10 评分定义 | 本文件 §7 |
