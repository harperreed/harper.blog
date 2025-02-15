---
date: 2025-02-14 20:59:59-05:00
title: My LLM codegen workflow atm.
description: A detailed walkthrough of my current workflow for using LLms to build software, from brainstorming through planning and execution.
draft: true
tags:
    - llm
    - coding
    - ai
    - workflow
    - software-development
    - productivity
---

_tl:dr; Brainstorm spec, then plan a plan, then execute using llm codegen. Discrete loops. Then magic. ✩₊˚.⋆☾⋆⁺₊✧_

I have been building a lot of small products using LLMs. It has been fun, and useful. However, there are a lot of pitfalls that can waste so much time.

(p.s. if you are a AI hater - scroll to the end)

I talk to a lot of dev friends about this, and we all have a similar approach with various tweaks in either direction.

Here is my workflow. It is built upon a lot of my own work, a lot of conversations with friends (thx Nikete, Kanno, and Erik), and following lots of best practices shared on the

This is working well **NOW**, it will probably not work in 2 weeks. Lol.

Here is my workflow! Enjoy.

## Let’s go

{{< image src="/images/posts/llm-coding-robot.webp" alt="Juggalo Robot" caption="I always find these AI generated images to be suspect. so lean in! Here is my juggalo coding robot angel!" >}}

There are many paths for doing dev, but my case is typically one of two:

- Greenfield code
- Legacy modern code

I will show you my process for both paths

## Greenfield

I find the following process works well for greenfield development. It is a robust on the planning and documentation side.

{{< image src="/images/posts/greenfield.jpg" alt="Green field" caption="Technically there is a green field on the right. Leica Q, 5/14/2016" >}}

### Step 1: Idea honing

Use a conversational LLM to hone in on an idea (I use ChatGPT 4o / o3 for this):

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

At the end of the brainstorm (it will come to a natural conclusion):

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

This will output a pretty solid and straightforward spec that can be handed off to the planning step. I like to save it as `spec.md` in the repo.

### Step 2: Planning

Take the spec and pass it a proper reasoning model (`o1*`, `o3*`, `r1`):

(This is the TDD prompt)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at those chucks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(This is the non-tdd prompt)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at those chucks and then go another round to break it into small steps. review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that thr steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

It should output a prompt plan that you can execute with aider, cursor, etc. I like to save this as `prompt_plan.md` in the repo.

I then have it output a `todo.md` that can be checked off.

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

You can save it as `todo.md` in the repo.

Your codegen tool should be able to check off the `todo.md` while processing. This is good for keeping state across sessions.

---

Now you have a robust plan and documentation that will help you execute and build your project.

This entire process will take maybe **15 minutes**. It is pretty quick. Wild tbh.

### Step 3: Execution

There are so many options available for execution. The success really depends on how well step 2 went.

I have used this workflow with [github workspace](https://githubnext.com/projects/copilot-workspace), [aider](https://aider.chat/), [claude engineer](https://github.com/Doriandarko/claude-engineer), [geppetto](https://chatgpt.com) (lol), [claude.ai](https://claude.ai), etc. It all works pretty well with all of the tools. It should work with any codegen tool.

I, however, prefer raw claude and aider:

### Claude

I either pair program with [claude.ai](https://claude.ai) and just drop each prompt in iteratively. I find that works pretty well. There is a lot of back and forth, but it works.

I am in charge of the initial boilerplate code, and making sure tooling is set up correctly. This allows for some freedom and choice.

I will then use a tool like [repomix](https://github.com/yamadashy/repomix) to iterate when things get stuck (more about that later).

The workflow is like this:

- set up the repo (boilerplate, uv init, cargo init, etc)
- paste in prompt into claude
- copy and paste code from claude.ai into IDE
- run code, run tests, etc
- ...
- if it works, move on to next prompt
- if it doesn’t work, use repomix to pass the codebase to claude to debug
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) is a lot of fun. I find that it slots in well to the output of step 2. I can get really far with very little work.

The workflow is essentially the same as above but instead of pasting into claude, I am pasting the prompts into aider.

Aider will then “just do it” and I get to play [cookie clicker](https://orteil.dashnet.org/cookieclicker/).

> An aside: Aider does really great benchmarking of new models for codegen in their [llm leaderboards](https://aider.chat/docs/leaderboards/). I find it to be a really great resource for seeing how effective new models are.

Testing is nice with aider, because it can be even more hands off as aider will run the test suite and debug things for you.

The workflow is like this:

- set up the repo (boilerplate, uv init, cargo init, etc)
- start aider
- paste prompt into aider
- watch aider dance ♪┏(・o･)┛♪
- aider will run tests, or you can run app to verify
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

### Results

I have built so so many things using this workflow: scripts, expo apps, rust cli tools, etc. It has worked across programming languages, and contexts. I do like it. If you have a small or large project that you are procrastinating on, I would recommend giving it a shot. You will be surprised how far you can get in a short amount of time.

## non-greenfield: Iteration, incrementally

Sometimes you don’t have greenfield, and instead need to iterate or do increment work on an established code base.

{{< image src="/images/posts/brownfield.jpg" alt="a brown field" caption="This is not a green field. A random photo from of grandfather's somewhere in uganda in the 60s" >}}

For this I have a slightly different method. It is similar to above, but a bit less “planning based.” The planning is done per task, not for the entire project.

### Get context

I think everyone who is knee deep in AI dev has a different tool for this, but you need something to grab your source code and efficiently jam it into the LLM.

I currently use a tool called `[repomix](https://github.com/yamadashy/repomix)`. I have a task set system wide in my `.mise.toml` that allows me to do various things with my code base ([mise rules](https://mise.jdx.dev/)).

Here is the llm task list:

```
llm:clean_bundles           Generate LLM bundle output file using repomix
llm:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
llm:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
llm:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
llm:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
llm:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
llm:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

I generate an `output.txt` that has the context from my code base. If I am blowing through tokens, and it is too big - I will edit the generate command to ignore parts of the code base that are not germane to this task.

Once the output.txt is generated, I pass it to the [llm](https://github.com/simonw/llm) command to do various transformations and then save those as a markdown file.

For instance, if I need a quick review of test coverage I would do the following:

#### Claude

- go to the directory where the code lives
- run `mise run llm:generate_missing_tests`
- look at the generated markdown file
- grab the full context for the code: `mise run llm:copy_buffer_bundle`
- paste that into claude along with the first missing test “issue”
- copy the generated code from claude into my ide.
- ...
- run tests
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- go to the directory where the code lives
- run aider (always make sure you are on a new branch for aider work)
- run `mise run llm:generate_missing_tests`
- look at the generated markdown file
- paste the first missing test “issue” into aider
- ...
- run tests
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

This is a pretty good way to incrementally improve a code base. It has been super helpful to do small amounts of work in a big code base. You can pretty much do any sized tasks with this method.

### Prompt magic

These quick hacks work super well to dig into places where we can make a project more robust. It is super quick, and effective.

Here are some of my prompts that I use to dig into established code bases:

#### Code review:

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply  before writing the code review. Review every part, and don't hallucinate.
```

#### GitHub Issue generation

(I need to automate the actual issue posting!)

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Missing tests

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues  will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

These prompts are pretty old and busted. They need some refactoring. If you have ideas to make them better lmk.

## Skiing ᨒ↟ 𖠰ᨒ↟ 𖠰

When I describe this process to people I say “you gotta keep track of what’s going on cuz you can get ahead of yourself quite easily.”

I find that using a planning step (ala the Greenfield process above) can help keep things under control. At least you will have a doc you can double check against. I also do believe that testing is helpful - especially if you are doing wild style aider coding. Helps keep things good, and tight.

Regardless, I do find myself over my skies quite a bit. Sometimes a quick break or short walk will help. In this regard it is a normal problem solving process, but accelerated to a break neck speed.

> One fun things we have been doing is to ask the LLM to do ridiculous things. For instance, we asked it to create a lore file and then reference the lore in the user interface. This is for python cli tools. Suddenly there is lore, glitchy interfaces, etc. All to manage your cloud functions, your todo list or whatever. The sky is the limit.

## I am so lonely (｡•́︿•̀｡)

My main complaint about these workflows is that it is largely a solo endeavor. I have spent years coding by my self, years coding as a pair, and years coding in a team. It is always better with people. These workflows are not easy to use as a team. The bots collide, the merges are horrific, the context complicated.

I really want someone to solve this problem in a way that makes coding with an LLM a multiplayer game. Not a solo hacker experience. GET TO WORK!

## ⴵ Time ⴵ

All this codegen has accelerated the amount of code that I as a single person am able to generate. However, there is a weird side effect. There is a lot of “down time” while you are waiting for the LLM to finish or whatever.

{{< image src="/images/posts/apple-print-shop-printing.png" alt="Printing" caption="I remember this like it was yesterday" >}}

I have changed how I work enough to start incorporating some practice that will try and eat the waiting time:

- I start the “brainstorming” process for another project
- I listen to records
- I play cookie clicker
- I talk shit to friends

It is pretty awesome. Hack Hack Hack. I can't think of another time I have been this productive in code.

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

A lot of my friends are like "fuck LLMs. They are terrible at everything." I don't mind this pov. I don't share it, but I think it is important to be skeptical. There are an awful lot of reasons to hate AI. My main fear is about power consumption and the environmental impact. But.. the code must flow. Right... sigh.

If you are open to understanding more, but don't want to dig in and become a cyborg programmer - my recommendation is not to change your opinion, but to read Ethan Mollick's book about LLMs and how they can be used: [**Co-Intelligence: Living and Working with AI.**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/)

It does a good job of explaining a lot of the benefits without being a tech anarcho capitalist bro type. I found it very helpful, and have had a lot of good and nuanced conversations with friends who have read it. Highly recommend.

If you are skeptical, but a bit curious - feel free to hmu and let's talk through it. I can show you how we use them, and maybe we could build something together.
