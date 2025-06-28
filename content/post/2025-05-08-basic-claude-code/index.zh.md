---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description:
    详细讲解如何使用 Claude Code AI 助手进行软件开发，包括工作流程提示、测试实践以及来自真实项目的实际示例。内容涵盖防御式编码策略、TDD
    和团队实施。
draft: false
generateSocialImage: true
tags:
    - ai
    - coding
    - claude
    - development
    - automation
    - testing
    - tdd
    - programming
title: Claude Code 基础
slug: basic-claude-code
translationKey: Basic Claude Code
---

我真心迷上了这种 agentic（自主体式）编码方式，它处处都让人上头。

自从我写下[那篇原始博客](/2025/02/16/my-llm-codegen-workflow-atm/)后，Claude 世界发生了不少事：

- Claude Code
- MCP
- 等等

我已经收到了数百封邮件（wat），大家聊自己的工作流，以及如何用我的流程抢占先机。我在几场大会上做了分享，还教过几门代码生成课。后来我发现电脑拼写检查总想把 “codegen” 改成 “codeine”，谁能想到！

{{< image src="codegen.png" >}}

前几天我和一位[朋友](https://www.elidedbranches.com/)聊天，讨论 **咱们都要完蛋**、**AI 会把我们的饭碗抢光**（之后再写）。她说：“你该写篇文章聊聊 Claude Code。”

那就开搞吧。

Claude Code 在我发那篇工作流文章八天后就上线，正如我预料，它让文中不少内容瞬间失效。我随即从 Aider 迁到 Claude Code，从此没回头。Aider 仍然好用，也有独特场景，但眼下 Claude Code 更香——虽然贵得离谱。

我的工作流和以前几乎一样：

- 先跟 `gpt-4o` 聊聊，打磨点子
- 用能找到的最强推理模型生成规格文档 (spec.md)。现在多用 o1-pro 或 o3（o1-pro 真比 o3 强吗？还是因为它跑得更久我就觉得更强？）
- 继续用同一个模型去写提示词。让 LLM 自己产出 prompt 是个神操作，还能把老一辈程序员（boomers）气得直跺脚
- 把 spec.md 和提示计划文件（prompt_plan.md）放到项目根目录
- 然后在 Claude Code 里输入下面这段提示：

```prompt
1. Open **@prompt_plan.md** and identify any prompts not marked as completed.
2. For each incomplete prompt:
    - Double-check if it's truly unfinished (if uncertain, ask for clarification).
    - If you confirm it's already done, skip it.
    - Otherwise, implement it as described.
    - Make sure the tests pass, and the program builds/runs
    - Commit the changes to your repository with a clear commit message.
    - Update **@prompt_plan.md** to mark this prompt as completed.
3. After you finish each prompt, pause and wait for user review or feedback.
4. Repeat with the next unfinished prompt as directed by the user.
```

- 这段提示的魔法在于：它先检查提示计划文件，找到未标 “completed” 的条目，完成下一件事；搞定后提交到 Git，并把 prompt_plan 标记为已完成；然后停下来等你审核。🤌
- 我直接往椅背一靠，对 Claude 说 `yes`，它就自己干活。它会跳出来要你给反馈，魔法就此展开。
- 随后就是不停点 “yes”，一遍遍输入 “continue”，活成真人版 Cookie Clicker。

这一套非常管用。如果在流程里再嵌入几项“小超能力”，效果更猛。

## 防御式编码！

### Testing

测试，以及测试驱动开发（Test-Driven Development，TDD），必须有。我强烈建议下狠功夫培养起稳固的 TDD 习惯。

我以前讨厌 TDD，写得烂，觉得浪费时间。事实证明我错得离谱，LOL。过去几十年里，我们在公司和项目里加了不少测试，但大多是功能完成后才补——这对人类还行，**对机器人可太糟糕了。**

机器人对 TDD 简直上瘾：先让机器人写测试和 mock，下一条 prompt 再把 mock 实现成真代码，机器人爽翻天。TDD 是我见过最有效的“防幻觉、防跑题”利器。

### Linting

我是真爱 lint。Ruff 巨香，Biome 很酷，Clippy 名字帅又好用。奇怪的是，机器人也特别爱跑 linter。

让 linter 持续运行能挡掉一堆 bug，让代码更易维护、更好读；再加个 formatter，一切就 A+++，下次执行也能一次通过。

### pre-commit 钩子

真正的魔法是把这些检查写进 pre-commit 钩子。我推荐 Python 包 `pre-commit`：一句 `uv tools install pre-commit`，再配好 `.pre-commit-config.yaml`，搞定。每次提交都会自动跑测试、类型检查、lint 等，确保代码 A+++。

这招配上 Claude Code 更嗨。机器人特别特别想 commit。你让它“写完就提交”，它可能大幅改动、提交，把一切搞崩后再修。

好处是不会把 GitHub Actions 堵成一锅粥：格式化、lint、类型检查全红，只因为机器人当时不在状态。

> 有意思的是，Claude 死活学不会正确用 `uv`。稍不留神就到处 `pip install`；就算你让它用 `uv`，它也会写成 `uv pip install`。看来六月诞生 AGI 是悬了，so sad。

### CLAUDE.md 与 commands

这两个简单小工具能榨出巨大收益。

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

我从朋友 [Jesse Vincent](https://fsck.com/) 那里“偷”来一份 [CLAUDE.md](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md)，他[下了大功夫把它做得超完善](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md)。里面包括：

- 精简版 Big Daddy Rule
- 如何做 TDD 的说明
- 我偏好的代码风格

> [@clint](https://instagram.com/clintecker) 把他的 CLAUDE.md 配成必须管他叫 MR BEEF，于是文档里全是 “If you're stuck, stop and ask for help—MR BEEF may know best.” 写这段时我也决定把自己的 CLAUDE.md 设成叫我 “Harp Dog”。这是特性，不是 bug。

commands 也很带劲。我的 dotfiles 里有一些示例：[看这里](https://github.com/harperreed/dotfiles/tree/master/.claude/commands)。

{{< image src="commands.png" >}}

以前我更频繁地用 commands，它依旧是复用常用 prompt 的神技。还能传参，比如 GitHub issue 命令要传 issue 号：`/user:gh-issue #45`

Claude 会按 `gh-issue.md` 里定义的 prompt script 跑。

你也可以把这些 commands 放到项目目录，再放一份项目专属的 CLAUDE.md。我常这么干，为 Hugo、Rust、Go、JavaScript 项目各配一套。

## “Continue”

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

有时我就像《辛普森》里那只不停敲 “Y” 的小鸟——只管打 “continue”，或者按上键把同一条 prompt 再发一次。

大多数计划大概 8–12 步。不管项目看着多庞杂、用哪个语言，我通常能在 30–45 分钟内完成一个从零开始的开发计划。

我把这事跟朋友 Bob 讲，他不信。我说：“随便说个要做的东西，再指定语言，咱走起！”

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

他来一句：“那就用 C 写个 BASIC 解释器。”

这并不理想。我不会 C，也没写过解释器，更懒得写。但——管他呢，干就完了。

按照上述流程走，Claude Code 表现很给力。现在我们有了[能跑的 BASIC 解释器](https://github.com/harperreed/basic)。首版一小时搞定，我又折腾几小时，现在已经相当像样。要是放在 1982 年能直接发布吗？大概还不行。完整的 [prompt_plan 在此](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md)。

## 团队

我们整个团队都在用 Claude Code，大体遵循上述流程，各自再加点 tweak。

我们的测试覆盖率比历史任何时期都高；代码质量也更好，而效率看起来和过去那堆糟糕代码差不多。偶尔抬头，就能看到 Claude Code 在 ghostty、VS Code 终端、Zed 终端里运行，甚至在 Jupyter Notebook 里乱舞。

{{< image src="dril.jpg" >}}

哪位 token 富豪帮我算算预算吧，我全家都快饿死了。

## 致谢

感谢所有给我发邮件的人。听你们聊各自的工作流和项目又酷又有趣。我真的很感激——来信别停！
