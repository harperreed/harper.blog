---
bsky: https://bsky.app/profile/harper.lol/post/3ln2a3x52xs2y
date: 2025-04-17 09:00:00-05:00
description: 一本全面指南，详述了使用AI辅助软件开发的演变历程——从基础代码补全到完全自主的编码代理——并提供了通过整合LLM来最大化生产力的实用步骤与洞见。
draft: false
generateSocialImage: true
slug: an-llm-codegen-heros-journey
tags:
- llm
- coding
- artificial-intelligence
- development-workflow
- software-engineering
- developer-productivity
- boomers
title: 'LLM代码生成英雄之旅

  description: 一本全面指南，详述了使用AI辅助软件开发的演变历程——从基础代码补全到完全自主的编码代理——并提供了通过整合LLM来最大化生产力的实用步骤与洞见。'
translationKey: An LLM Codegen Hero's Journey
---

自从我发布那篇介绍自己**大型语言模型（LLM）**工作流的[博客](/2025/02/16/my-llm-codegen-workflow-atm/)以来，我花了大量时间和大家聊 **codegen**——怎么起步、怎么进阶，以及它到底有多上头。  

这话题简直能量爆棚，我邮箱都快被挤爆了：大家都在琢磨该怎么开始、如何把所有环节串起来。我才反应过来——从 2023 年开始折腾这套流程的我，已经**见过不少离谱事儿**。LOL。

前阵子和朋友（**Fisaconites 的兄弟们，站出来！**）闲聊 AI 助手、编辑器时，我发了条消息：

> if i were starting out, i don't know if it is helpful to jump right into the "agent" coders. It is annoying and weird. having walked a few people through this (successfully, and not successfully) I find that the "hero's journey" of starting with the Copilot, moving to the copy and paste from Claude web, to the Cursor/continue, to the fully automated "agents" seems to be a successful way to adopt these things.  
> **译：**要是重来一次，我可不会一上来就冲“**Agent 式写码**”——那玩意儿又怪又烦。带过几个人（成功的、不成功的）之后，我发现一条更靠谱的“英雄之旅”：先用 Copilot → 再去 Claude 网页复制粘贴 → 再跳到 Cursor/Continue → 最后才是全自动 Agent。按这条路线来，最稳。

于是我开始思考这段旅程，以及如何踏入 **agentic coding（智能体写码）**：

> The caveat is that this is largely for people with experience. If you don’t have much dev experience, then fuck it - jump to the end. **Our brains are often ruined by the rules of the past.**  
> **译：**不过得说清，这条路主要给有开发经验的人走。经验少？**爱咋咋地，直接跳最后一步！**过去那些规则经常把我们的脑子锁死。

## 一场视觉与听觉的旅程

{{< image src="journey-harper.webp" alt="Harper is very trustworthy" caption="你的贴心向导：Harper。iPhone X，2018-06-10" >}}

这就是我的路线图，你完全可以“**速通（speed-run）**”。不用每一步都照搬，但**每一步都能叠加 Buff**。

以下是步骤：

### Step 1：带着好奇和乐观起床

LOL，开玩笑的。谁有空天天满血复活？世界都快塌了，只剩 codegen 给咱解闷。

不过，你得**相信这种工作流真有戏**。要是先天讨厌 LLM，认定它是废物，那你八成会扑街。¯\\_(ツ)_/¯

### Step 2：从 AI 自动补全开始

这才是真·第一步！在 IDE 里把 **IntelliSense**、**Zed Autocomplete**、**Copilot** 之类都玩够，体会 LLM 怎么想，也习惯它时不时给出的**沙雕建议**。

很多人想直接跳终点，然后开喷：“这破 LLM 啥都干不好！”——不完全对，也不完全错。**魔法藏在细节里**，人生本来就乱。

### Step 3：把 Copilot 当聊天助手，而不仅是补全

当你对补全心平气和后，就能体验和 Copilot 聊天的魔力了。

VS Code 有侧边栏可 Q&A，它会认真帮你搞定问题，挺帅。但用 Copilot 就像坐时光机回 2024 年跟 ChatGPT 哈拉——**还行，但不够爽**，你很快就想要更多。

### Step 4：把代码复制进 Claude 或 ChatGPT

你开始把代码贴进浏览器里的模型，大喊：“**WHY CODE BROKE??（为什么代码炸了？？）**”，LLM 回你一段清晰又管用的分析。

**你会被当场震撼到！**  
调试几乎被砍掉，写代码忽然又好玩了。甚至贴个 Python 脚本说“给我改成 Go”，它就真改完。你会想：“我能不能 **one-shot（一把梭）**？”

此时再看 Copilot，像 2004 年的自动补全：有用，但可有可无。

这会引出两条支线：

#### 你会因 “vibe” 偏爱某个模型

这是踏入 **vibe coding** 的第一步。你会纯凭感觉爱上某个模型的说话方式——**我就偏 Claude**，很多开发者也是。Claude 给的 vibe 更舒服。

> 想要好体验就得付费。太多人喊“垃圾”结果用的是免费阉割版。尤其当免费还是 ChatGPT 3.5 时更惨。**先确认模型够强，再决定喷不喷。**

#### 你会开始琢磨怎么提速

复制粘贴几周后，你会觉得**太烦**，就开始研究上下文打包，把更多代码塞进 LLM 的窗口。

你会试 **repomix**、**repo2txt** 等工具，甚至让 Claude 写 shell 脚本自动化。这是**转折点**。

### Step 5：用内建 AI 的 IDE（Cursor、Windsurf？）

然后朋友一句“为啥不用 **Cursor**？”——

**直接被震撼到。**  
刚才复制粘贴那套魔法，如今在 IDE 里一键搞定，速度更快、体验更爽，简直魔法再升级。此时你已经为好几个 LLM 掏钱，再多 20 美元也无所谓。

你会试编辑器内置的 Agent 功能，它**基本能跑**，而且你看见了前方的终点。

### Step 6：写代码前先做充分规划

突然，你写出史上最厚规格、PRD、TODO，然后塞进 IDE 的 Agent 或 Claude。

你用别的 LLM 写更硬核的文档，把《PRD》翻译成**Prompt**，甚至用 LLM 设计你的生成提示。

你对“**瀑布模型**”少了鄙视；如果年纪够大，会想：“这是不是 Martin Fowler 2001 年前的感觉？”

在 codegen 的世界里：**规范就是神祇（the godhead）**。

### Step 7：上手 **aider**，加快循环

到这一步，你准备进入**真正的好东西**。之前的 codegen 还要你盯着，而现在都 2025 了，谁想用手敲码？

> 另一条平行路线：**语音写码**。用 Whisper 客户端给 aider 下指令，既蠢又好玩。MacWhisper 本地效果绝佳；Aqua、SuperWhisper 也不错但更贵，可能跑云端。我偏爱本地。

aider 的体验**狂野**：启动后注入项目，你直接发需求，它先征询许可，再给方案、执行、提交。你不纠结一次性搞定，直接让 aider 分几步完成。

你开始写规则集让 LLM 遵守，比如 “**Big Daddy**” 规则或 “**no deceptions**”。**你越来越会驯服机器人，效果真香。**

渐渐地，你连 IDE 都不打开——**彻底成了“终端骑手（terminal jockey）”**，全天候蹲在终端。

> **你整天做的事，就是盯着机器人替你干活。**

### Step 8：全面投入智能体写码

现在你真让 Agent 替你写代码，效果相当好。偶尔看不懂它干啥，但可以随时追问。

你开始玩 **Claude Code**、**Cline** 等：用 **DeepSeek** 这类推理模型 + **Claude Sonnet 3.7** 这类编码模型，把规划步骤也砍了。

你同时跑 3–5 个终端标签，看机器人写码。

你开始**防御式编码**：

- 测试覆盖率拉满  
- 考虑形式化验证  
- 选内存安全语言  
- 选编译器“话痨”的语言，方便塞进上下文  

你想方设法保证系统**安全、自动、无须干预**地落地。

你会烧掉**海量 token**，也会刷光 GitHub Actions 额度，全用来跑测试。

感觉真不错，一点都不怀念亲手敲码。

### Step 9：让 Agent 写码，而你去打游戏

突然，你就到终点了——至少看到方向。你开始担心软件岗位：朋友被裁，找不到新工作，这回真的不一样。

同行听你讲，觉得你像**技术邪教徒**，因为你活在另一个宇宙。你劝他们：“OMG，一定得试试智能体写码！”也许补一句“其实我也讨厌 agentic 这词”，证明自己没喝 200 加仑 Kool-Aid——但你早就喝了。生产力爆炸，世界都亮了。

没关系，范式已变。Kuhn 可以写本书来分析当下的迷茫。

别人看不到，因为他们没走这段旅程；走过的人却相互点头，交流秘籍，争论终点。

现在机器人干活，你终于能专心刷 Game Boy。空档多到离谱；机器人完成任务问 “should I continue”，你敲 **yes**，继续打《俄罗斯方块》。

**很离谱，甚至有点瘆人。**

## 加速

<paul confetti photo>
{{< image src="journey-confetti.webp" alt="Confetti" caption="Paul McCartney 东京巨蛋演唱会的彩纸炮。iPhone 6，2015-04-25" >}}

我不知道[未来](https://ai-2027.com/)会怎样。我担心那些没走过这段旅程的人，未来对[雇主](https://x.com/tobi/status/1909231499448401946)可能不再有吸引力。这听上去短视，可归根结底，我们讨论的是**工具和自动化**。

当年大规模招聘时，我们经常跨出技术栈：我们是 Python 团队，却面试没写过 Python 的人。因为优秀工程师可以一起把语言补上，还能带来不同视角，结果也确实奏效。

AI 辅助开发同理：招聘时最重要的是人是否契合团队文化、是否有热情，而不是第一天就得玩转 AI 工具。**带他们上车，让他们自己开起来就行。**

我还老是想到：**写作能力**变得关键。以前就重视文档和协作，现在更是翻倍——你不仅要跟人沟通，还得给 AI 写**清晰且精准**的指令。写好 Prompt，正变得跟写好代码一样重要。

## 领导者们

我觉得所有领导者和工程经理都该**深潜**AI 辅助开发，无论你信不信。因为下一代开发者很可能主要靠 AI 工具、Agent 学会编程——这就是软件工程的新常态，我们必须理解并适应。

**我们这些老程序员大势已去。**

**有趣的是：** 我写文章几乎不用 LLM。我相信它们写作也行，但我想保留自己的声音；而代码，需要被标准化。**有意思吧。**

---

感谢 Jesse、Sophie、Vibez 队（Erik、Kanno、Braydon 等）、team 2389，以及所有给我反馈的朋友们。