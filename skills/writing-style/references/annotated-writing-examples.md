# Annotated Writing Examples

Worked examples with `% role` annotations showing the function of each sentence in context. Use these as templates when drafting Abstract, Introduction, and Method sections.

**See also**:
- `references/abstract-playbook.md` — Abstract templates and pre-writing questions
- `references/introduction-playbook.md` — Introduction templates and backward-first protocol
- `references/method-playbook.md` — Method three-element decomposition

---

## Abstract Examples

### Example 1: Version 1 (Challenge → Contribution)

```
% context: Code efficiency evaluation for LLMs
% template: Version 1 — Challenge → Contribution

Large language models (LLMs) have demonstrated strong capabilities    % role: context
in code generation, yet evaluating the efficiency of generated code   % role: context (narrowing)
remains limited to execution time.                                    % role: gap (what is missing)
We introduce BEST, a benchmark for evaluating both time and space     % role: contribution + advantage in one sentence
efficiency of LLM-generated code across 400 expert-curated C++ tasks. % role: scale
BEST employs a subtask-based evaluation scheme that provides          % role: what is new (mechanism)
fine-grained efficiency profiling beyond pass/fail metrics.           % role: advantage
Experiments across 31 LLMs reveal that space-efficient code           % role: results
generation lags significantly behind time efficiency.                 % role: takeaway
```

### Example 2: Version 2 (Challenge → Insight → Contribution, recommended)

```
% context: Multimodal retrieval
% template: Version 2 — Challenge → Insight → Contribution

Cross-modal retrieval aims to match queries and documents across      % role: context (task definition)
different modalities such as text, images, and audio.                 % role: context (scope)
Existing methods align modalities in a shared embedding space,        % role: prior work
but they struggle with fine-grained semantic correspondence           % role: gap
when modalities have fundamentally different information densities.   % role: gap (why it matters)
We observe that aligning at the token level rather than the           % role: insight (key finding)
sequence level preserves modality-specific details that global        % role: insight (mechanism)
pooling discards.                                                     % role: insight (why)
Based on this, we propose TokenAlign, which performs cross-modal      % role: implementation
matching through learned token-to-token correspondences,              % role: implementation (mechanism)
enabling fine-grained alignment without dense cross-attention.        % role: benefits
On three standard benchmarks, TokenAlign reduces retrieval error      % role: results (numbers)
by 23% while requiring 40% fewer parameters than fusion baselines.   % role: results (comparison)
These results suggest that token-level alignment is a more            % role: takeaway
effective paradigm than sequence-level fusion for cross-modal tasks.  % role: takeaway (bounded conclusion)
```

### Example 3: Version 3 (Multiple Contributions)

```
% context: Efficient planning for embodied agents
% template: Version 3 — Multiple Contributions

Embodied agents require real-time planning under computational        % role: context
constraints that preclude exhaustive search.                          % role: context (constraint)
Current planners either sacrifice optimality for speed or require     % role: contrast (existing trade-off)
offline computation that limits adaptability to new environments.     % role: contrast (limitation)
We introduce SparsePlan, a locality-sensitive hashing scheme for      % role: contrib₁ + advantage
plan tokens that reduces planning complexity from O(n²) to            % role: contrib₁ advantage (quantified)
O(n log n) without sacrificing solution quality.                      % role: contrib₁ advantage (trade-off)
We further propose AdaptTree, an online tree-expansion strategy       % role: contrib₂
that dynamically prunes low-reward branches using learned value       % role: contrib₂ (mechanism)
estimates, enabling zero-shot transfer to unseen environments.        % role: contrib₂ advantage
Together, SparsePlan and AdaptTree achieve state-of-the-art success   % role: results (combined)
rates on ALFRED and TEACh while running 5× faster than prior methods. % role: results (numbers)
Our results demonstrate that decoupling search efficiency from        % role: takeaway
plan quality is achievable through structured token sparsification.   % role: takeaway (bounded conclusion)
```

---

## Introduction Examples

### Example A1: Part A — Version 3 (General → Specific setting)

```
% Part A: Task/Application Opening
% Version 3: General task → narrow to specific setting
% Note: Part A ONLY covers the task opening. The gap/challenge belongs in Part B.

Neural architecture search (NAS) has produced competitive models      % role: broad area
across vision, language, and speech tasks.                            % role: breadth
While most NAS research focuses on finding a single optimal           % role: narrowing (what community does)
architecture for a fixed hardware target, real-world deployment       % role: narrowing (specific setting)
often requires a family of architectures spanning the Pareto          % role: what is needed
frontier for devices with varying compute budgets.                    % role: why this setting matters
In this work, we focus on multi-objective NAS under heterogeneous     % role: precise scope
hardware constraints, where the goal is to discover a diverse         % role: goal definition
set of efficient architectures in a single search run.                % role: deliverable
```

### Example A2: Part A — Version 4 (Open with challenge)

```
% Part A: Task/Application Opening
% Version 4: Familiar task → open with challenge directly

A central challenge in open-domain question answering is              % role: challenge upfront
faithfully attributing generated answers to retrieved evidence,       % role: challenge (specific)
without hallucinating unsupported claims.                             % role: consequence of failure
Despite significant progress in retrieval-augmented generation,       % role: acknowledge progress
attribution errors persist even in state-of-the-art systems,          % role: remaining gap
undermining user trust in high-stakes applications such as            % role: impact
medical and legal question answering.                                 % role: application domains
```

### Example B1: Part B — Version 1 (Challenge chain)

```
% Part B: Technical Challenge
% Version 1: Challenge chain (general → traditional → recent → remaining)

Generating diverse yet coherent long-form text remains                % role: general challenge
a fundamental difficulty for autoregressive language models.           % role: task scope
Early decoding strategies such as beam search produce fluent but      % role: traditional approach
repetitive outputs, sacrificing diversity for likelihood.              % role: traditional limitation
More recently, nucleus sampling and typical decoding improve           % role: recent approach
diversity by truncating the token distribution, yet they introduce    % role: recent progress
incoherence at the discourse level: paragraphs may individually       % role: remaining gap
read well but fail to build a sustained argument.                     % role: gap consequence
We identify the root cause as a mismatch between token-level          % role: root issue (insight)
stochasticity and discourse-level planning: diversity is injected     % role: root cause (mechanism)
at the wrong granularity.                                             % role: root cause (diagnosis)
```

### Example C1: Part C — Version 2 (Two contributions bridged by remaining challenge)

```
% Part C: Pipeline Introduction
% Version 2: Two contributions bridged by remaining challenge

Our first contribution is StructDecode, a discourse-aware decoding    % role: contrib₁ (name + category)
strategy that maintains a latent outline during generation,           % role: contrib₁ (mechanism)
selecting tokens that are both locally fluent and globally coherent.  % role: contrib₁ (advantage)
While StructDecode ensures coherence, a remaining challenge is        % role: bridge (remaining challenge)
evaluating discourse-level diversity beyond surface n-gram metrics.   % role: bridge (what is missing)
To address this, we further introduce DiscoDiv, an evaluation         % role: contrib₂ (name)
framework that measures structural diversity through topic-flow       % role: contrib₂ (mechanism)
entropy and argument-arc similarity.                                  % role: contrib₂ (what it measures)
Together, StructDecode and DiscoDiv enable both generation and        % role: combined benefit
evaluation of diverse, coherent long-form text.                       % role: combined benefit (summary)
```

### Example C2: Part C — Version 3 (Adding module to existing pipeline)

```
% Part C: Pipeline Introduction
% Version 3: Adding a new module to an existing pipeline (observation-driven)

We observe that standard retrieval-augmented generation pipelines     % role: observation
pass retrieved passages to the generator without verifying their      % role: observation (specific behavior)
relevance, leading to hallucinated answers when retrieval fails.      % role: observation (consequence)
Motivated by this observation, we propose RetrievalGuard, a           % role: contribution (name)
lightweight verification module that scores passage-question          % role: contribution (mechanism)
alignment before generation and abstains when confidence is low.      % role: contribution (behavior)
When integrated into existing RAG pipelines, RetrievalGuard           % role: advantage (integration)
reduces hallucination rates by 34% on Natural Questions while         % role: advantage (numbers)
adding less than 5% latency overhead.                                 % role: advantage (cost)
```

---

## Method Example

### Three-Element Module Decomposition (complete worked example)

```
% Module: Adaptive Token Merging for Vision Transformers
% Structure: Motivation → Design → Advantage

% === MOTIVATION (why this module exists) ===

A key computational bottleneck in vision transformers is the          % role: motivation (problem)
quadratic self-attention cost over all spatial tokens.                % role: motivation (root cause)
While prior token pruning methods reduce token count, they            % role: motivation (prior approach)
discard potentially useful spatial information irreversibly,          % role: motivation (prior limitation)
degrading performance on tasks requiring fine-grained spatial         % role: motivation (consequence)
reasoning such as object detection and segmentation.                  % role: motivation (affected tasks)

% === DESIGN (how the module works) ===

We represent each token as a tuple (feature, position, importance),   % role: design (representation)
where importance is estimated by a lightweight linear head.           % role: design (implementation detail)
Given N input tokens, we first cluster them into N/r groups           % role: design (step 1: cluster)
using their position embeddings, then merge each group into           % role: design (step 2: merge)
a single token by importance-weighted averaging of features.          % role: design (step 2: mechanism)
Formally, the merged token for group g is computed as:                % role: design (formal definition)

  t_g = sum_{i in g} w_i * f_i / sum_{i in g} w_i                   % role: design (equation)

where w_i is the importance weight and f_i is the feature vector.     % role: design (variable definitions)
This produces N/r tokens that are passed to the next transformer      % role: design (output)
block, reducing the self-attention cost by a factor of r^2.           % role: design (complexity reduction)

% === ADVANTAGE (why this design is better) ===

Compared to token pruning, our merging approach preserves all         % role: advantage (vs. alternative)
spatial information in compressed form rather than discarding it.     % role: advantage (key difference)
This enables a 3× speedup at r=4 while maintaining 98.5% of the     % role: advantage (quantified)
baseline accuracy on COCO detection, whereas pruning at the same      % role: advantage (comparison)
reduction ratio drops accuracy by 4.2 points.                        % role: advantage (comparison number)
```

---

## Anti-Pattern Examples

### Anti-pattern: Pipeline-only Abstract (no insight, no advantage)

```
% BAD EXAMPLE — DO NOT IMITATE
% Problem: Only describes what the method does, not why it works or what advantage it brings

We propose a framework for multimodal learning.                       % role: vague contribution
Our framework consists of three modules: a feature extractor,         % role: pipeline description
a fusion module, and a prediction head.                               % role: pipeline description
The feature extractor uses a pretrained backbone.                     % role: implementation detail
The fusion module combines features from different modalities.        % role: obvious statement
The prediction head outputs the final result.                         % role: obvious statement
Experiments show that our framework achieves good performance.        % role: no numbers, no comparison

% WHY THIS FAILS:
% - No gap or challenge stated
% - No insight explaining why this design works
% - "Good performance" without numbers or baselines
% - Every sentence describes WHAT, none explains WHY
```

### Anti-pattern: Incremental-Patch Introduction

```
% BAD EXAMPLE — DO NOT IMITATE
% Problem: Presents work as iterative debugging rather than principled design

A natural approach to cross-modal retrieval is to project both        % role: naive solution
modalities into a shared embedding space using contrastive loss.      % role: naive solution (detail)
However, this leads to modality collapse where all representations    % role: problem with naive
converge to a narrow subspace.                                        % role: problem detail
To fix this, we add a diversity regularizer to the loss function.     % role: patch 1
But this introduces training instability at large batch sizes.        % role: new problem from patch 1
We further address this by using a two-stage training procedure       % role: patch 2
where diversity is only enforced after warmup.                        % role: patch 2 detail

% WHY THIS FAILS:
% - Reads like incremental debugging, not principled research
% - Makes the work seem like a patchwork of fixes
% - No core insight that unifies the design choices
% - BETTER: Present the final design as a principled solution
%   motivated by the identified challenge (modality collapse),
%   with diversity regularization and staged training as
%   components of a coherent solution, not sequential patches
```
