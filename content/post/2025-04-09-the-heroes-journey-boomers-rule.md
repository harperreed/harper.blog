---
date: 2025-04-09 18:00:00-05:00
title: The LLM codegen heroes journey
description: A comprehensive guide detailing the evolution of using AI-assisted software development, from basic code completion to fully autonomous coding agents, with practical steps and insights for maximizing productivity through LLM integration.
draft: false
tags:
    - llm
    - coding
    - artificial-intelligence
    - development-workflow
    - software-engineering
    - developer-productivity
---

I have spent a lot of time since my [last blog post](/2025/02/16/my-llm-codegen-workflow-atm/) talking to folks about codegen and how to get started, get better, and why it is interesting.

There have been an incredible amount of interest in this topic. I have received a lot of emails from people who are working to figure all of this out. I started to notice that many people are struggling to figure out how to start, and how it all fits together. Then I realized that I have been hacking on this process since 2023 and I have seen some shit. Lol.

I was talking about this with friends and I sent this message in response to a thread about AI assisted agents, and editors:

> if i were starting out, i don't know if it is helpful to jump right into the "agent" coders. It is annoying and weird. having walked a few people through this (successfully, and not successfully) i find that the "hero's journey" of starting with the Copilot, moving to the copy and paste from Claude web, to the Cursor/continue, to the fully auto "agents" seems to be a successful way to adopt these things.

This lead me to start thinking a lot about the journey and how to get started using agentic coding:

> The caveat is that this is largely for people with experience. If you don’t have much dev experience then fuck it - jump to the end. **Our brains are often ruined by the rules of the past.**

## A journey of sight and sound

This is my journey. It is largely the path I took. I think you could speed run it if you were compelled. I don’t think you need to follow every step, but I do think every step is additive.

### Get out of bed with wonder and optimism

Lol. Just kidding. Who has time for that. It may help, but the world is falling apart and all we got is codegen to distract us.

It does help to to assume that these type of workflows can work and be additive. If you hate LLMs and don’t think it will work, then you will not be successful here. ¯\\\_(ツ)\_/¯

### Start with AI assisted autocomplete

This is the real step one! You need to spend enough time in the IDE context to know how well you would work with intellisense, zed autocomplete, Copilot, etc. It gives you an idea of how the LLM is working - and prepares you for the stupid shit it will often recommend.

A lot of folks skip this step and just jump to the end. Then they are like “this LLM is a piece of shit and can’t do anything right!” Which is not true, but also can be true. The magic is in the nuance. Or as I like to remember: life is confusing.

### Start using Copilot as more than autocomplete

Once you have a good process in place with the autocomplete and you are not mad _all_ of the time, you can move on to the magic of talking to Copilot.

VS Code has a pane where you can Q&A with Copilot and it will help you with your code, etc. It is pretty cool. You can have a nice convo about your code, and it will be thoughtful and help you solve whatever query you asked.

However, using Copilot is like using a time machine to talk to ChatGPT in 2024. It isn’t _that_ great.

You will be wanting more.

### Move to copying and pasting code into Claude or ChatGPT

You start to satisfy your curiosity by pasting code into the browser based foundational model and asking “WHY CODE BROKE??” And then having LLM respond with a coherent and helpful response.

You will be AMAZED! The results are going to blow your mind. You are going to start to build lots of weird shit, and doing really fun things with code again. Mostly cuz it cut out the entire debugging process.

You can also do wild things like paste in a python script and tell the LLM “make this into go” and it will just _make it into go_. You will start thinking “I wonder if I can one shot this.”

Copilot will start to look like 2004 autocomplete. It is handy, but not really necessary.

This will lead you down a couple sub paths:

#### You will start to prefer one model cuz of vibes

This is the unfortunate first step towards the vibe in vibe coding. You will start to prefer how one of the big models talk to you. It is feelings tho. Kind of weird. You will find yourself thinking “I like how Claude makes me feel.”

Lots of devs like Claude. I use both, but mostly Claude for code related things. The vibe with Claude is just better.

One important note:

You have to pay for them to get the good stuff. So many friends are like “This is a piece of shit” and then you find out they are using a free model that barely works. Lol. This was more of an issue when the free version was ChatGPT 3.5, but make sure you are using a capable model before you throw the entire premise out.

#### You will start thinking about how to make things go faster

After copying and pasting code into Claude for a few weeks you are going to realize that this is annoying. You are going to start working through context packing, and trying to fit more of your code into the LLM context window.

You will experiment with repopack, repo2txt, and other code context tools. Just so that you can slam your entire codebase into the Claude context window. There is a chance that you will even start writing shell scripts (well Claude will write them) to help make this process easier.

This is a turning point.

### Use an AI enabled IDE (Cursor, Windsurf? )

Then a friend will say “why don’t you just use Cursor?”

It will completely blow your mind. All the magic you just experienced by copying and pasting is now available in your IDE. It is faster, it is fun, and it is close to magic.

At this point you are paying for like 5 different LLMs - what is another $20 a month.

It works super well, and you feel way way more productive.

You will start playing with the agentic coding features built directly into the editors. It will _basically_ work. But you can see a destination on the horizon that may be better.

### You start planning before you code

Suddenly you find yourself building out very robust specs, PRDs, and todo docs that you can pipe into the IDEs agent, or into Claude web.

You have never “written” so much documentation. You start to use other LLMs to write more robust documentation. You are transposing docs from one context to another (“Can you make this into prompts”). You start to use the LLM to design your codegen prompts.

You are saying the word “waterfall” with a lot less disdain. If you are old, you may be fondly remembering the late 90s and early 2000s and wonder “is this what Martin Fowler felt like before 2001?”

In the world of codegen: The spec is the godhead.

### You start playing with aider to enable quicker loops

At this point you are ready to start getting into the **good stuff**. The codegen previously required you to be involved, and paying attention. But it is 2025! Who wants to code with their fingers?

> One other path that lots of friends are experimenting with is to code with your voice. To start instruct aider, etc via a whisper client. It is hilarious and fun.

Trying out aider is a wild experience. You start it up, it instantiates itself into your project. You put your query directly into aider, and it just kind of does it. It asks for permission, and gives you a framework to get things done. It completes the task. You no longer are so worried about one shotting tasks. You just have aider do it.

You start building out rulesets for the LLM to follow. You learn about the “Big Daddy” rule, or the “no deceptions” addition. You start be really good at prompting the robot.

It works.

Eventually you don’t even open up an IDE - you are just a terminal jockey now.

You spend your time watching the robot do your job.

### You lean all the way into agentic coding

You are now using an agent to code for you. The results are pretty good. There are a few times when you have no idea what’s going on. But then you remember you can just ask it.

You start to experiment with Claude Code, Cline, Agentis-cli, etc. You are super happy to be able to use a reasoning model (deepseek!) and a coding model (Claude sonnet 3.7) together to start removing planning steps.

You are doing wild stuff like running 3-5 concurrent sessions. Just tabbing through terminals watching robots code.

You will start coding defensively:

- really hardcore test coverage
- thinking about formal verification
- using memory safe languages
- etc

You will think long and hard about how to make sure that the thing you are building just gets built, safely without intervention.

You will spend SO SO much money on tokens. You will also use up all your GitHub action hours running all the wild tests that you are running to make sure that the code is built safely.

It feels good. You are not mad about not coding.

### You let the agent code, and you play video games

Suddenly you are there. You are at the destination. Well, kind of - but you see where we are going. You start to worry about software jobs. Your friends are being laid off, and they can’t get new jobs.

When you talk to your peers they think of you as a religious zealot cuz you are working within a different context than they are. You tell them “omg you have to try out agentic coding!” Maybe you add “I hate the word agentic” just to not show that you have drank 200 gallons of kool-aid. But you have. The world seems brighter cuz you are so productive with your code.

It doesn’t matter.

Nobody can see because they didn’t go through the journey to get here. But those who have are agreeing and sharing their own tips around the journey, and debating the destination.

Now that you are knee deep in letting robots do the work, you can really focus on all those gameboy games you have been wanting to play. There is a lot of downtime. And when the robot is done, it will be like “should I continue” and you type yes and go back to Tetris.

Very strange. Unsettling, even.

## The acceleration

I don’t know what will happen in the future. I am worried that people who are not working through this journey are not going to be attractive to employers. Which is kind of near sighted, because ultimately we are talking about tooling, and automation.

When we were ramping up hiring in the past, we would often spread our queries well past our network, and past our tech stack. We would do python and be interviewing people who didn’t know python, and have never used python. Our thought was with a great engineer, we could work together to get them comfortable with python. They would be additive even if they were not super comfortable with our stack. This worked out well for us. We hired incredible people who had never worked with our stack. Many times they brought such a different perspective that it elevated the entire team.

This seems no different. If you hire a person that is talented, and fits in your team, and they are stoked to join up - then I wouldn’t worry about whether they have been on this journey or not. They don’t have to have drank all the kool-aid. Put them in the passenger seat and bring them along on the journey.

Eventually they will be the driver and will be successfully using these tools.

One other aspect I have been considering: Writing is even more important. We have always over indexed on good communicators. It helps with team dynamics, documentation, and general problem solving. It is even more important today. In prompt land, we need people who can communicate via writing to robots.

## The leadership

I think it is really important for those of you who are leaders and engineering managers to dig all the way into this. Not because you agree - but you are going to be hiring people whose only experience coding is this path. That is the future software engineers. We gotta be ready for that.

Us boomers are not long for this world.
