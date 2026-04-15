---
date: 2026-04-14T10:00:00-06:00
description: "What happens when your whole engineering team goes all-in on AI codegen. The bottleneck moves from execution to judgment, collaboration gets weird, and the org chart has to change before the stack does. Lessons from over a year of ~100% AI-generated code."
draft: true
tags:
    - ai
    - coding
    - codegen
    - engineering
    - management
    - workflow
    - agents
    - talks
title: "When code stops being the bottleneck"
generateSocialImage: true
translationKey: When-Code-Stops-Being-The-Bottleneck
slug: when-code-stops-being-the-bottleneck
---

I have been giving a lot of talks about AI codegen lately. Like, a lot. People keep asking me the same questions, and I keep finding myself saying the same things, so I figured I should just write it down in a more durable format.

I've been writing about [my codegen workflow](/2025/02/16/my-llm-codegen-workflow-atm/) and [Claude Code specifically](/2025/05/08/basic-claude-code/) for over a year now. I wrote about how [waterfall is back](/2025/04/10/waterfall-in-15-min-or-less/) and everyone got mad at me (lol). Those posts were about the individual developer workflow. How one person sits down with an agent and ships.

This post is different. This is about what happens when your whole team does it. When the bottleneck moves. When the org chart has to change before the stack does.

Here's the thing that surprised me: we had week-long sprints. Everyone was shipping so fast with AI codegen that we moved to three-day sprints. Output did not change. We could build anything in six weeks. Plus or minus five weeks. That variance should tell you everything.

{{% figure src="slide-that-is-the-transition.png" caption="" %}}

## This is not a tool talk

Everyone asks me what tool to use. Cursor or Copilot? Claude Code or Codex? Gemini?

You already have tools. Too many tools. That *is* the problem.

{{% figure src="slide-that-is-the-problem.png" caption="" %}}

The tool is not the point. The *workflow* is the point. The *operating model* is the point. AI codegen is not a productivity tool change. It is an operating model change, and if you treat it like a better autocomplete, you're going to plateau fast and wonder why everyone else is moving faster.

[Dan Shapiro wrote about five levels of AI-driven code](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/) that I think about constantly. Level 0 is manual labor, you write every line, AI is spicy autocomplete. Level 1, you hand your AI intern bounded tasks. Level 2, you pair with AI in flow state. 90% of "AI-native" devs are here. Level 3, you're not a senior developer anymore, you're a manager. Level 4, you write a spec, you argue about the spec, AI builds it. Level 5 is the dark factory: spec in, software out, humans neither needed nor welcome.

{{% figure src="slide-level-4.png" caption="" %}}

Most orgs plateau at Level 3. We operate between 4 and 5. I have not opened an editor in months. Nobody on my team writes code the old way. None of us touch code, none of us read code, none of us review code. ~100% AI-generated, for over a year. It is a weird weird time.

{{% figure src="slide-workflows-beat-tools.png" caption="" %}}

Stop debating tools. Start designing workflows.

## Conviction collapse

I had a conversation with Tim O'Reilly recently where he said something that stuck: a product used to be a *thing*. Now a product is a *process*.

{{% figure src="slide-product-is-process.png" caption="" %}}

Code got cheap. Choice got expensive.

When you can build anything, *what to build* is the hard part. We experienced this firsthand. The bottleneck moved from "can we build it?" to "should we build it?" and that shift damn near broke us. We'd build an entire product, complete with landing pages, show it to someone, get feedback, and then just build another entire product. The whole thing. Again. [I talked about this with O'Reilly](https://www.oreilly.com/radar/conviction-collapse-and-the-end-of-software-as-we-know-it/) and I called it "conviction collapse." You don't have time to fall in love with your product the same way. You don't have time to enjoy and define and defend your conviction around it. You just build again.

{{% figure src="slide-when-you-can-build-anything.png" caption="" %}}

That much optionality destroyed our ability to make decisions. This is a leadership problem, not a technology problem. No tool fixes it. You have to get better at knowing what to build, and that means getting better at saying no. (Turns out saying no is really hard when building yes costs $0.)

## Collaboration got weird

Here's something nobody warned me about: merging AI code with AI code is a mess.

You ask your agent: "how's the navbar going?"

It says: "I got them all!"

Got all what?

{{% figure src="slide-all-of-them.png" caption="" %}}

*All of them?*

It fixed the navbar. And the footer. And 100 bugs it found along the way. Agents lack discrete focus. They fix everything everywhere all at once. Which sounds great until two engineers' agents are touching the same repo. Everything conflicts. You spend your whole day resolving merge conflicts and untangling code nobody asked for.

Our answer: one engineer per repo. I know that sounds extreme, but it works. Spend tokens on progress, not defense.

{{% figure src="slide-output-went-way-up.png" caption="" %}}

Output went way up. But alignment got harder. The engineer became manager and orchestrator at once. You used to be a musician. Now you're a conductor. This is one of the reasons everyone is tired. You are not used to this cognitive load, and nobody trained you for it. (More on the cognitive load thing later.)

## The workflow that works

Here's what actually works for us: Spec, Plan, Build, Review, Test, Ship. In that order. Every time.

Yes, this is waterfall. Waterfall is not a bad word anymore. LLMs need ultra-clear requirements up front. The difference: this waterfall runs in minutes, not months.

{{% figure src="slide-spec-for-anyone.png" caption="" %}}

### The spec is everything

We do reverse Q&A with an LLM. It asks you questions, one at a time, until you have a spec you could hand to *anyone*. Clear instructions are now the most important engineering skill. Actually, let me restate that: *clear writing* is now the most important engineering skill. Spec quality determines output quality. Garbage spec, garbage output. Every time. I really cannot overstate this. If you take one thing away from this post, it's that the spec is the whole game.

### The cook-off

LLMs converge fast. One path, one answer. That kills exploration.

{{% figure src="slide-kills-exploration.png" caption="" %}}

So we build the same feature 3-5 times in parallel. Different agents, different approaches. A judge picks the best of each, weaves them into the final version. Old way: pick one, hope, pivot. New way: try five, compare, choose with data. Code costs $0. When trying costs tokens instead of weeks, try everything. I am a really big fan of this pattern tbh.

### Scenario testing

This is the big one. Not test coverage theater. Have the LLM *use your software as a user*. Through a browser. Through an emulator. We even have Android phones hooked up through ADB, clicking through the app like a real person. No scripts. The instruction is literally "go buy this product, here's a credit card that is actually a credit card." You can even hook that up to a mailbox API and say it's done when you get the confirmation email. It's the dumbest shit ever. It's bash. And it works.

{{% figure src="slide-finds-what-unit-tests-wont.png" caption="" %}}

When I worked at Threadless back in the day, I would set my test account's address to my brother's address. When we'd do big test runs, he'd get hundreds of t-shirts. I thought it was hilarious.

The fun part about scenario testing: whenever it finds a bug, it's like "this is a huge bug, this is horrible, who did this?" And you're like, well, *you* did it. Fix it. And then it just fixes it, because it's in the same loop. The dev loop isn't finished until it passes the scenario test.

Most legacy tests are theoretical. Staging is a thought experiment. Coverage targets are assumptions. Don't get rid of them, but they miss what a real user finds in thirty seconds.

## The giggling matters

The cognitive load of going from "I write code" to "I manage something that writes code" is real. That's management. Management is exhausting. Especially when you didn't sign up for it.

People who treat agents as *social* outperform people who treat them as *tools*. I know that sounds weird. Give agents personalities. We run review squads with themed perspectives. Squad one: users. Solid review. Squad two: experts. Also solid. Squad three: all Hacker News commenters.

Annoying review. Super annoying. But they find bugs that the serious reviews miss. Every single time.

And every time, you kind of giggle. That giggling matters. It's a coping mechanism for the cognitive load. Make the work fun. You need it.

{{% figure src="slide-best-engineers-best-writers.png" caption="" %}}

The best engineers on my team are the best writers. That's not a coincidence. Docs are currency now. Clear writing = better prompts = better code. If you can't articulate what you want, you can't build it.

### Guardrails stay sacred

CI after every codegen commit. Pre-commit hooks are non-negotiable. If the agent wants to skip a check, that is when you need it most.

{{% figure src="slide-agent-skip-check.png" caption="" %}}

Git is your undo button for runaway agents. Commit early, commit often, roll back freely. Your engineering discipline is not obsolete. It *becomes* the guardrails. I am such a fan of this framing. Your years of engineering practice aren't wasted, they're the thing that keeps the agents from going off the rails.

## The org changes before the stack does

Every person is becoming more team-shaped. Idea, build, code, test, ship, all one person. Everyone becomes a product person. A product person who can now *ship*.

Execution used to be the bottleneck. Not anymore. If you can articulate what you want, you can now build it.

We ran an intern program that proved this out. Paired zero-experience interns with senior coaches. Gave the intern an agent and said go. Run into the wall. When you hit a problem, your coach helps. It worked. The person closest to the problem can be the person who solves the problem, regardless of title. I found this really encouraging tbh.

Staff engineers become workflow designers. Coherence guardians. Less "principal coder," more "principal *thinker*." Product, design, engineering boundaries blur. And that's ok.

{{% figure src="slide-surprised-me-most.png" caption="" %}}

Here's the insight that surprised me most: this is 100% people management. The agent is a capable junior employee. Tireless and fast. No ego. Needs clear direction and oversight. Great engineering manager skills turn out to be great agent operator skills. Wild tbh.

## The choice

Every org has two paths right now. Use this to *cut*. Or use this to *do more*.

Why are we always thinking we can cut half? Why not do twice as much?

{{% figure src="slide-twice-as-much.png" caption="" %}}

Tackle the backlog. Replace the legacy system. Build what never got prioritized. The stuff that was important but never got done, it ships every night now while you sleep. The agents go wild on the stuff that you would never have gotten to otherwise.

This is a leadership decision. Not a technology decision. Same humans. Less time on the wrong layer of the stack.

{{% figure src="slide-strengths.png" caption="" %}}

If you want to start Monday, here's what I'd do:

- Stop debating tools as ideology
- Define 3-5 preferred workflows
- Preserve your sensible defaults as guardrails: ship from main, small tasks, continuous delivery
- Pick one thin-slice legacy replacement. End to end. Prove it works.
- Build what fits *your* context. Do not wait for a vendor. Anthropic does not care about your org. [Every Jedi builds their own lightsaber.](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/)
- Give engineers permission to build the workflow, not just use the tool
- The people who figure this out first should be teaching, not hoarding

The shift is not that engineers type faster. It's that software teams stop organizing around typing.

Design the transition you want. Don't let it happen to you.

If any of this resonates, or you think I'm totally wrong, hit me up. I really like hearing how other teams are handling this. It is a weird weird time and we're all figuring it out together.
