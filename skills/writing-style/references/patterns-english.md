# English AI Writing Patterns - Complete Reference

英文 AI 写作模式的唯一完整目录（英文层的 de-AI 目录；中文层用 `patterns-chinese.md`）。

## Usage criteria (read first)

This catalog descends from Wikipedia's AI-cleanup guide, whose native genre is encyclopedia prose. Every "After" below is shorter than its "Before", but brevity is a side effect, not the goal: these rewrites delete zero-information filler and replace vague wording with concrete facts. Three guards:

- Information conservation precedes pattern matching: if deleting a sentence would leave the reader knowing less, it is not filler. Rewriting direction is "swap in the specific" or "delete the zero-information", never "make it shorter".
- The "swap vague for specific" moves in these examples are legal only when the concrete fact already exists in the source or context. Never invent facts; with nothing to swap in, keep the information and only adjust the wording.
- In technical and academic prose, explanatory sentences carry causal reasoning. A sentence that matches a pattern's surface form but carries real information gets re-shaped, not removed.

## CONTENT PATTERNS (内容模式)

### 1. Undue Emphasis on Significance (过度强调意义)

**Words to watch**: stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Before**:
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After**:
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

---

### 2. Undue Emphasis on Notability (过度强调知名度)

**Words to watch**: independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Before**:
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After**:
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

---

### 3. Superficial Analyses with -ing Endings (-ing 结尾的肤浅分析)

**Words to watch**: highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Academic camouflage variants**（躲过吹捧词过滤器，因为长得像正经 hedge）: ", indicating that...", ", suggesting that...", ", demonstrating that...", ", revealing...", ", enabling...", ", supporting...", ", showing that...". 每节出现一次是正常学术 hedge，扎堆出现才是 AI 信号。修法不是删解读，是改句形：在数字或具体实例处断句，另起一个平实短句作解读（"This may be because...", "It demonstrates that..."），不挂在数据句后面当分词尾巴。详见 `paper-voice-contract.md` Category 7。

**Before**:
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After**:
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

---

### 4. Promotional Language (宣传性语言)

**Words to watch**: boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Before**:
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After**:
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

### 5. Vague Attributions (模糊归因)

**Words to watch**: Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Before**:
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After**:
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

---

### 6. Formulaic "Challenges" Sections (公式化的"挑战"部分)

**Words to watch**: Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Before**:
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After**:
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

---

## LANGUAGE PATTERNS (语言模式)

### 7. AI Vocabulary (AI 词汇表)

**High-frequency AI words**: Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Before**:
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After**:
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

---

### 8. Copula Avoidance (回避系动词)

**Words to watch**: serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Before**:
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After**:
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

---

### 9. Negative Parallelisms (否定式排比)

**Before**:
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After**:
> The heavy beat adds to the aggressive tone.

---

### 10. Rule of Three (三段式法则)

**Before**:
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After**:
> The event includes talks and panels. There's also time for informal networking between sessions.

---

### 11. Elegant Variation (刻意换词)

**Before**:
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After**:
> The protagonist faces many challenges but eventually triumphs and returns home.

---

### 12. False Ranges (虚假范围)

**Before**:
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After**:
> The book covers the Big Bang, star formation, and current theories about dark matter.

---

## STYLE PATTERNS (风格模式)

### 13. Em Dash Overuse (破折号过度使用)

**Before**:
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**After**:
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

---

### 14. Overuse of Boldface (粗体过度使用)

**Before**:
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After**:
> It blends OKRs, KPIs, and visual strategy tools like Business Model Canvas and Balanced Scorecard.

---

### 15. Inline-Header Vertical Lists (内联标题垂直列表)

**Before**:
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After**:
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

---

### 16. Title Case in Headings (标题大小写)

**Before**:
> ## Strategic Negotiations And Global Partnerships

**After**:
> ## Strategic negotiations and global partnerships

---

### 17. Emojis (表情符号)

**Before**:
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After**:
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

---

### 18. Curly Quotation Marks (弯引号)

**Before**:
> He said “the project is on track” but others disagreed.

**After**:
> He said "the project is on track" but others disagreed.

---

## COMMUNICATION PATTERNS (交流模式)

### 19. Collaborative Communication Artifacts (协作交流痕迹)

**Words to watch**: I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Before**:
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After**:
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

---

### 20. Knowledge-Cutoff Disclaimers (知识截止免责声明)

**Words to watch**: as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Before**:
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After**:
> The company was founded in 1994, according to its registration documents.

---

### 21. Sycophantic/Servile Tone (谄媚语气)

**Before**:
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After**:
> The economic factors you mentioned are relevant here.

---

## FILLER PATTERNS (填充模式)

### 22. Filler Phrases (填充短语)

| Before | After |
|--------|-------|
| "In order to achieve this goal" | "To achieve this" |
| "Due to the fact that it was raining" | "Because it was raining" |
| "At this point in time" | "Now" |
| "In the event that you need help" | "If you need help" |
| "The system has the ability to process" | "The system can process" |
| "It is important to note that the data shows" | "The data shows" |

---

### 23. Excessive Hedging (过度限定)

**Before**:
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After**:
> The policy may affect outcomes.

---

### 24. Generic Positive Conclusions (通用积极结论)

**Before**:
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After**:
> The company plans to open two more locations next year.

---

## SUPPLEMENTARY PATTERNS (非维基补充)

### 25. Reflexive Analogies (条件反射式比喻)

**Words to watch**: comparing concepts to engines, bridges, maps, journeys, recipes, ecosystems, flywheels, layers, compasses, mirrors, toolboxes when the analogy adds nothing.

**Before**:
> Think of the API gateway as a traffic cop directing requests, a bridge between services, the beating heart of the architecture.

**After**:
> The API gateway routes each request to the matching service and rejects ones that fail authentication.

---

### 26. Staccato Drama Sentences (连续短句制造戏剧感)

**Watch for**: three or more consecutive clipped sentences, often an elliptical run like "No symmetry. No priors. No mercy."

**Problem**: one short sentence emphasizes a point; a run of them turns ordinary information into trailer narration without adding content.

**Before**:
> Then AlphaEvolve arrived. No symmetry preference. No aesthetic priors. The old rules stopped working.

**After**:
> AlphaEvolve has no preference for symmetry or human aesthetics, so the old rules no longer fully apply.

---

### 27. Aphorism Formulas (格言金句公式)

**Watch for**: "X is the language/currency of Y", "X is not a tool but a mirror", "the real substrate of X is Y", "X becomes a trap".

**Problem**: dresses an ordinary claim as a quotable maxim; the posture rises while precision does not.

**Before**:
> Symmetry is the language of trust. Optimize processes too hard and efficiency becomes a trap.

**After**:
> Symmetric layouts usually feel more predictable to users. Teams that over-optimize processes tend to overlook how people actually work.

---

### 28. Fake-Candor Openers (假装坦率开场)

**Watch for**: "Honestly?", "Let me be real", "Here's the thing", "To be blunt" used as a beat of manufactured candor before an ordinary answer.

**Problem**: the opener promises a revelation, then delivers a mundane claim. Natural conversational use is fine; the fixed opener-then-shrug formula is the tell.

**Before**:
> Is it worth the price? Honestly? It depends on how often you use it.

**After**:
> Whether it is worth the price depends on how often you use it.

---

## AI High-Frequency Vocabulary Reference（高频词表）

> 以下单词 AI 味较浓，命中不等于必删。判断时考虑：(a) 该词在当前上下文是否有合法替代功能（"ecosystem" 在描述具体技术栈时合法，描述抽象领域时是 AI 词；"robust" 在统计/系统论文里是术语）；(b) 同类 AI 词在文中的密度（孤立 1 个可能是无心，≥3 个聚集是强信号）；(c) 学科约定。词表是触发器不是判决书。

Accentuate, Ador, Amass, Ameliorate, Amplify, Alleviate, Ascertain, Advocate, Articulate,
Bear, Bolster, Bustling, Cherish, Conceptualize, Conjecture, Consolidate, Convey, Culminate,
Decipher, Demonstrate, Depict, Devise, Delineate, Delve, Delve Into, Diverge, Disseminate,
Elucidate, Endeavor, Engage, Enumerate, Envision, Enduring, Exacerbate, Expedite,
Foster, Galvanize, Harmonize, Hone, Innovate, Inscription, Integrate, Interpolate, Intricate,
Lasting, Leverage, Manifest, Mediate, Nurture, Nuance, Nuanced, Obscure,
Opt, Originates, Perceive, Perpetuate, Permeate, Pivotal, Ponder, Prescribe, Prevailing, Profound,
Recapitulate, Reconcile, Rectify, Rekindle, Reimagine, Scrutinize, Substantiate,
Tailor, Testament, Transcend, Traverse,
Underscore, Unveil, Vibrant

---

## Source

[Based on Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. Key insight: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
