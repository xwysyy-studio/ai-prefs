# Dev Core（开发高频纪律）

> 自动适用于所有代码改动。下游消费点：`~/.codex/AGENTS.md` §3 / §4 / §6（精简版 + 指针）。本文件是唯一权威，仅当核心条目增删时更新那边。

## 动手前
- 相关文件 / 现有模式 / 项目惯例先读；同类问题先 Grep 有没有已解决的；有基线测试 / 构建命令先跑一遍确认现状
- repo-state 协议仓库（存在 `scripts/docctl.py`）：开工先 `python3 scripts/docctl.py context <路径/关键词>`；state 文档是现状权威，process 记录只当历史快照。涉及既有项目的设计 / 写作，动笔前先回查决策台账与已否决项（铁律 4）
- 测试姿态：用户要求（含 spec / AC 点名）或修 bug 时才写测试，不主动铺测试套件；修 bug 的回归测试先跑红再修（从未红过的测试不可信）；测试断言行为、只走 public interface（深度见 `tdd` skill）
- 新建 API / service / utility 前停靠，到第一层成立就停：本仓库已有 → 语言标准库 / 工具原生 → 已装依赖 → 都没有才新写；新建要写清旧的为什么不够用
- 修改被多处依赖的代码前 grep 调用方；破坏性改动（改签名 / 返回值 / 删方法）列受影响调用方等确认；修 bug 护栏加在共享函数一处，不逐调用点贴补丁
- ≥3 文件或 >15 分钟工作量 → 先出方案（2-3 句）等确认；有回滚风险先记 baseline sha
- 不熟的 CLI / API 先读 `--help` 或 doc，不猜命令和 flag。HuggingFace CLI 前缀是 `hf`（不是 `huggingface-cli`）

## 编码克制
> 触发词：try / except / fallback / default / interface / adapter / factory / strategy / 泛型 / config 开关 / validate / guard / lock / 防御性分支——看到自己要写，先过判据再写。

- 不预先抽象：不到两个语义相同的真实调用点，不抽函数 / 类 / 接口；不为想象中的未来加扩展点、可选模式、没用上的参数
- 不静默兜底：错误优先抛到能处理的层；不 try/except 吞掉返回默认值 / 静默续跑；请求失败不偷偷换模型 / provider / URL / 解析器，除非有界重试的已知瞬时故障
- 不层层设防：校验只在信任边界（外部输入 / 网络 / 持久化 / 安全 / 并发）做一次；内部函数假设调用方守约，不重复 null 检查和"不可能发生"分支
- 理由词红旗："更安全 / 更健壮 / 更灵活 / 未来可能 / 防御性 / 为兼容"若指不出当前在失败的例子、外部边界或用户需求 → 删
- 判据：让程序**停下 / 验证 / 报告 / 大声失败**的护栏，留；让程序**静默续跑 / 多接受一种模式 / 多暴露一个开关 / 伺候想象中调用方**的护栏，砍

## 写完后
- 相关脚本 / 构建 / 测试跑过、退出码确认；对外交付物按 `rules/verification.md` 验收
- debug 残留（print / console.log / debugger）清掉；走弯路产生的冗余代码 / 文件 / 死路径自查清理，不留给用户点名
- 过度工程扫描：diff 新增行里的 try / fallback / 新抽象 / config 开关 / 防御分支，每处指不出真实失败场景 → 撤回。外部审查返回的加固建议按同一判据过滤，不采纳记一句理由；自己当审查者时同一判据管输出侧：审查 = 找有真实失败场景的 bug，不产出加固建议清单
- 涉及安全 / 权限 / 支付 / 并发：输入校验、权限层级、异常路径、边界条件（空值 / 溢出 / 竞争）过一遍
- commit message 用 Conventional Commits：`<type>[scope]: <描述>`，破坏性改动 type 后加 `!`；repo-state `[doc-ack:]` 等标记放 footer

## 进程与搜索
- 停 dev server / 预览进程禁宽匹配 `pkill` / `killall`：先 `pgrep -f` 列出确认，再 kill 精确 PID（宽匹配曾误杀 MCP server 和自身）
- Bash 搜索优先 `rg` 并限定路径 / 文件类型；禁止大目录树宽通配 `grep` / `ugrep`（曾 OOM 弄崩 WSL2）；能用原生 Grep 工具就不开 shell 搜索

## 并发执行
批量同构 + 单元无依赖 + 外部等待主导，三条同时满足 → 默认并发，禁止逐个串行。先按速率约束定并发度 + 退避；命中限流降并发加退避，不退回串行。真实依赖 / 写同一资源 / 纯本地计算 → 串行合理。

## API 脚本与失败阶梯
- 脚本默认：认证预检（key 缺失 / 格式错明确报错退出）；429 / 5xx 指数退避最多 3 次，401 / 403 立即报错不重试；HTTP 超时默认 30s
- 失败阶梯：先按 `rules/verification.md` 归因；第 1 次失败重试 1 次；第 2 次换**根本不同**的路径（不是调参）并告知用户；第 3 次停，给已验证事实 + 已排除假设 + 选项 + 推荐。`bug-detective` L3/L4 压力档仅在用户对停点回复"继续 / try harder"后解锁
- 瓶颈同走阶梯：连续 2-3 轮迭代无实质提升（没报错不等于在前进）= 非通过。两问要有证据的"能"（当前思路还正确吗？还能继续提升吗？），答不出就主动转向根本不同的路径 / 角度 / 拆法，不磨也不停摆；在无法提升的方案上继续开发是愚蠢错误的决定

## Subagent 分发
- 每个 prompt 自含全部上下文：任务、输出路径、命名、格式、约束、参考文件；不假设子 agent 知道主 agent 的约束。必带四件：git 安全（"Do NOT commit, push, or run destructive git commands"）+ 自主权边界（默认可修有证据的 bug 并记录，不得扩 scope；只读任务声明 READ_ONLY）+ 既有裁定与已否决黑名单（铁律 4）+ 先接地再产出与受众假设（铁律 3 / 5）
- 同时 dispatch ≤3；限定只读指定文件、只返回摘要，不把源文件全量拉回；401 / 403 / 503 等 30s 重试 1 次仍失败报告等指示；大仓库调查类超 2 分钟主动中止分段
- 交回契约：会写文件的子任务在 prompt 里指定宿主已有验证器（没有就指定最小检查命令），验证不过不得报 DONE；交回摘要必带 `STATUS:`（DONE / DONE_WITH_CONCERNS / PARTIAL / BLOCKED / NEEDS_INPUT）+ `EVIDENCE:`（词汇同 `references/codex-task-template.md` §9），已验证事实与未验证假设分开列。父会话按 EVIDENCE 复核，不采信 PASS 自评；无 EVIDENCE 按未验证处理

## Codex 调用底线
任何 Codex 调用前先读 `references/codex-delegation.md`（模型路由 / 写模式门槛 / 审查隔离 / 失败处理的唯一权威）。底线：只用插件命令，禁止直接 `codex exec`；显式 `--model gpt-5.6-sol`（rescue 加 `--effort max`），禁止降级；前台执行，禁止 background；失败不静默 fallback。
