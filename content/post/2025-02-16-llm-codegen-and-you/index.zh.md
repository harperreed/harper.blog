---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: 从头脑风暴到规划再到执行，详细讲解我目前使用 LLM 构建软件的工作流程。
draft: false
generateSocialImage: true
slug: my-llm-codegen-workflow-atm
tags:
    - LLM
    - coding
    - ai
    - workflow
    - software-development
    - productivity
title: "我当前的 LLM 代码生成工作流程"
translationKey: My LLM codegen workflow atm
---

_tl:dr; 先用头脑风暴打磨规范，再“计划如何制定计划”，然后让 LLM 按离散循环一步步写代码——最后见证魔法 ✩₊˚.⋆☾⋆⁺₊✧_

我已经靠 LLM 做了不少小产品，过程既有趣也高效，但也暗藏几个能吞掉大把时间的坑。前阵子朋友问我怎么用 LLM 写软件，我心想：“oh boy，这得聊多久！”于是就有了这篇文章。

（p.s. 如果你是 AI 黑粉——直接跳到最后）

我和许多开发朋友聊过，大家的思路大同小异，只是在细节上各有偏好。

下面的流程融合了我的实践、朋友的经验（感谢 [Nikete](https://www.nikete.com/)、[Kanno](https://nocruft.com/)、[Obra](https://fsck.com/)、[Kris](https://github.com/KristopherKubicki)、[Erik](https://thinks.lol/)），以及来自互联网上那些“糟糕角落”里的最佳实践。

它**此刻**很好使，也许两周后就失效，也可能效率翻倍。¯\\\_(ツ)\_/¯

## Let’s go

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="AI 画的图总让人觉得哪儿怪怪的。和我的 Juggalo 编程机器人天使打个招呼！" >}}

开发场景很多，但我常遇到两类：

- 全新项目（Greenfield code）
- 刚变旧的代码（Legacy modern code）

下面分别说明我的做法。

## Greenfield

对全新项目，这套流程既能产出完备文档，又便于小步迭代。

{{< image src="greenfield.jpg" alt="Green field" caption="严格说右边那片才是绿田。Leica Q，2016-05-14" >}}

### Step 1：打磨想法

用对话式 LLM 把创意细化（我用 ChatGPT 4o / o3）：

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

等头脑风暴自然收束后：

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

模型会生成一份相当扎实的规范文档，我通常保存为 `spec.md`。

> 这份规范不只用来代码生成。我常让推理模型“must go deeper!”——挑毛病、写白皮书、生成商业模型，甚至做深度研究，一口气回你一万字。

### Step 2：规划

把 `spec.md` 交给推理能力更强的模型（`o1*`、`o3*`、`r1`）。

（TDD 版提示词）

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

（非 TDD 版提示词）

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

模型会产出一份可直接执行的提示词清单，我保存为 `prompt_plan.md`。

接着让它生成勾选清单 `todo.md`：

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

> 最好让代码生成工具在执行时自动勾选 `todo.md`，这样跨会话也能保持进度。

#### 计划就绪

到此你就有了稳健的计划和文档，可直接驱动项目落地。

整个流程大概也就 **15 分钟左右**。

### Step 3：执行

执行工具五花八门，成败主要取决于规划质量。

我用过 [GitHub Workspace](https://githubnext.com/projects/copilot-workspace)、[aider](https://aider.chat/)、[cursor](https://www.cursor.com/)、[claude engineer](https://github.com/Doriandarko/claude-engineer)、[sweep.dev](https://sweep.dev/)、[ChatGPT](https://chatgpt.com)、[claude.ai](https://claude.ai) 等，都能跑通——理论上任何代码生成工具都行。

我个人最常用的是直接在 claude.ai 网页端配合 aider。

### Claude

我把 [claude.ai](https://claude.ai) 当结对伙伴，逐条投喂提示词，虽来回沟通略多，但整体可靠。

仓库初始化和工具链由我先搭好，避免 Claude 一股脑吐 React 代码。卡住时，我会用 [repomix](https://github.com/yamadashy/repomix) 打包完整代码库让 Claude 调试。

流程大致如下：

- 初始化仓库（样板代码、`uv init`、`cargo init` 等）
- 把提示词粘给 Claude
- 将 Claude 输出复制到 IDE
- 运行代码或测试
- 如果通过，继续下一个提示词
- 如果未通过，用 repomix 打包代码让 Claude 调试
- 重复 ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) 上手有点奇特，但与第二步产出的提示词配合得天衣无缝，能极省心地推进。

These quick hacks work super well to dig into places where we can make a project more robust. It is super quick, and effective.

Aider 的流程与上面几乎一致，只是把提示词粘到 Aider 而非 Claude，而且 Aider 会自动修改文件、执行命令并汇报结果。

流程如下：

- 初始化仓库（样板代码、`uv init`、`cargo init` 等）
- 启动 aider
- 粘入提示词
- 观看 aider “跳舞” ♪┏(・o･)┛♪
- Aider 会自动运行测试；也可手动验证
- 如果通过，继续下一个提示词
- 如果未通过，与 Aider 问答修复
- 重复 ✩₊˚.⋆☾⋆⁺₊✧

测试环节在 Aider 中尤为省心，因为它会自动跑测试并尝试修补。

### 结果

借此我做出了脚本、Expo App、Rust CLI 等大量项目，跨语言跨场景都能跑。

如果你有项目一直拖着，强烈推荐尝试——会惊讶于自己能多快推进。

## Non-greenfield：增量迭代

有时你面对的不是空白项目，而是仍在服役的代码库，需要持续迭代。

{{< image src="brownfield.jpg" alt="a brown field" caption="这可不是绿田。外公 60 年代在乌干达拍的老照片" >}}

此时按任务逐步规划，而非一次性规划整项目。

### 获取上下文

大家都有不同工具，但本质是把源码高效打包进 LLM。我目前用 [repomix](https://github.com/yamadashy/repomix)，在全局 `~/.config/mise/config.toml` 里配了这组任务：

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

这些命令会生成 `output.txt`，包含代码库上下文。如果 token 超限，就调整忽略规则把无关部分剔掉。

> `mise` 的好处是任务可在项目目录 `.mise.toml` 覆写。只要最终依旧输出 `output.txt`，后续流程就无缝。

生成 `output.txt` 后，用 [LLM](https://github.com/simonw/LLM) 做各种转换并保存为 markdown，例如：

```shell
cat output.txt | LLM -t readme-gen > README.md
cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md
```

This isn’t super complicated；`LLM` 负责调用模型、管理密钥和套用提示词模板。

如果我要补齐测试覆盖率，会这么做：

#### Claude

- 进入代码目录
- `mise run LLM:generate_missing_tests`
- 打开 `missing-tests.md`
- `mise run LLM:copy_buffer_bundle` 把上下文复制到剪贴板
- 将上下文和首条“缺失测试”任务粘给 Claude
- 把 Claude 生成的代码复制进 IDE
- 运行测试
- 重复 ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- 进入代码目录，先建新分支
- 启动 aider
- `mise run LLM:generate_missing_tests`
- 打开 `missing-tests.md`
- 把首条“缺失测试”任务粘给 aider
- 看 aider “跳舞” ♪┏(・o･)┛♪
- 运行测试
- 重复 ✩₊˚.⋆☾⋆⁺₊✧

这套方法可在大型代码库里高效做小步快跑。

### Prompt magic

下面是我常用来深挖遗留代码的几条提示词（prompt）：

#### Code review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply before writing the code review. Review every part, and don't hallucinate.
```

#### GitHub Issue generation

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Missing tests

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

这些提示词有点 **boomer prompts** 的味道，早该重构；如果你有更好点子欢迎砸我。

## Skiing ᨒ↟ 𖠰ᨒ↟ 𖠰

我常说，用 LLM 编程容易 **over my skis**——如果不紧盯进度，很快就失控。可能刚还在顺滑粉雪上飞驰，转眼就 “WHAT THE FUCK IS GOING ON!” 然后掉进悬崖。

在全新项目里插一段**规划**有助于稳住：至少手里有文档可对照。我也强烈建议写测试，尤其当 Aider 自动改代码时，测试能让一切保持健康紧凑。

即便如此，我仍时常 **over my skis**。这时起身走走，换个思路，多半能重新聚焦——本质还是正常问题-解决，只是节奏被倍速。

> 我们经常让 LLM 给并不奇幻的项目加点离谱元素：比如生成 lore 文件再让 UI 引用。结果 Python CLI 工具里突然冒出背景故事、闪烁界面……想象力天花板才是极限。

## I am so lonely (｡•́︿•̀｡)

最大槽点：现有流程几乎都是**单人模式**。

我独码、结对、团队协作都干过，还是觉得跟人一起写代码更爽。但现在的 bot 容易互撞、分支合并惨烈、上下文同步麻烦。

真心希望有人把 LLM 编程变成多人在线协作，而不是孤独黑客的单机游戏。快去做吧！

## ⴵ Time ⴵ

代码生成让个人产码量飙升，但也带来副作用：等模型烧 token 的空挡越来越多。

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="我仿佛昨天才用过它" >}}

我开始用这些方式消磨等待：

- 开一个新项目的头脑风暴
- 听唱片
- 玩 [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/)
- 和朋友、机器人聊天

能如此疯狂 hack 真是爽。我想不出还有哪个时代能让我写这么多代码。

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

不少朋友说：“LLM？啥都干不好。” 这种怀疑我理解。AI 的能耗和环境影响确实值得担忧。但……代码总得流动，对吧，唉。

如果你想了解又不想变成“赛博格程序员”，推荐 Ethan Mollick 的 [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/)。它讲清楚 LLM 的好处，却不流于乌托邦。

如果你半信半疑又有点好奇——随时找我，一起聊聊、折腾点东西。

_感谢 [Derek](https://derek.broox.com)、[Kanno](https://nocruft.com/)、[Obra](https://fsck.com) 和 [Erik](https://thinks.lol/) 审阅并提出修改意见。Thanks, folks!_
