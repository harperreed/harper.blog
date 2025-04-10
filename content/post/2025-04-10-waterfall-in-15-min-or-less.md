---
date: 2025-04-10 18:00:00-05:00
title: "Waterfall in 15 Minutes: My Take on AI-Assisted Coding with teams"
description: A practical guide exploring how AI is transforming software development workflows, from basic prompts to automated agents, with tips for maximizing team productivity and code quality.
draft: false
tags:
    - LLM
    - Coding
    - Artificial Intelligence
    - Development Workflow
    - Software Engineering
    - Developer Productivity
---

I recently had a conversation that started out as a casual catch-up and spiraled into a deep exploration of AI-assisted coding and what it's doing to our workflows, teams, and sense of "craft." It spanned everything from rewriting old codebases to how automated test coverage changes the nature of programming.

I took the transcript and popped it into o1-pro and asked it to write this blog post. Not terrible. Representative of my beliefs.

## Here it is:

### The New Normal: "Why Does Code Quality Even Matter?"

For years, we've talked about code as craft—how we get into that precious flow state, sculpt a piece of logic, and emerge victorious, artisanal bug fixes in hand. But there's a new paradigm creeping in where code generation tools (think large language models, or LLMs) can effectively pump out features in minutes.

Some folks are rattled by this pace and how it upends the old standards of "clean code." Suddenly, writing robust test suites, or even test-driven development, is more about letting the bots verify themselves than it is about methodically stepping through each line of code.

Will code quality nosedive? Possibly. On the other hand, we're also seeing a push for hyper-defensive coding—static analysis, formal verification, and test coverage everywhere—so that if an AI-based agent does break something, we catch it quickly. We've never needed top-notch CI/CD pipelines and rigorous checks more than we do now.

---

### Waterfall in 15 Minutes

We used to talk about "Waterfall vs. Agile" as if they were moral opposites, with Agile the only correct path. But ironically, code generation is nudging us toward micro waterfall cycles: we carefully define a spec (because the AI needs clarity), press "go," wait for the code to be generated, and review. It might still feel iterative, but in practice, we do a chunk of planning, then a chunk of execution, then a chunk of review. "Waterfall in 15 minutes."

The real magic? You can spin up multiple "agents" simultaneously. While one AI is building a feature, another is handling your docs, and a third is chewing on your test coverage. That's not exactly the old idea of a single, linear Waterfall—this is concurrency on steroids.

---

### The Coming Shift in Team Culture

If you manage or lead an engineering team, you probably hear from the top: "What about AI to make us more productive?" But you may also sense that your existing team has varying levels of enthusiasm for these tools. Some are all-in—spinning up entire new features purely through prompt-driven coding—while others are protective of that craft identity.

Here's what I think works:

1. **Run Small Pilots**

    Pick an internal project, or maybe a side tool that doesn't carry heavy production risk, and let a few curious engineers run wild with AI coding. Let them break stuff, experiment, see what happens when they trust the model a little too much, then watch how they incorporate best practices to rein it back in.

2. **Rotate People In and Out**

    Having a dedicated "AI-coded" side project means you can rotate team members—let them spend a week or two living in this new environment, learning from each other, and then bring those lessons back to the larger codebase.

3. **Get Serious About Documentation**

    AI "agents" often require extremely clear specs. Code generation is cheap, but guiding an LLM in the right direction costs careful planning. If you want your entire team to benefit, put the best specs and architecture docs you've ever written into a shared repository. You'll thank yourself when people rotate on or off that project.

---

### Why Flow State May Be Overrated

One surprising takeaway: a lot of us got into coding because we love the flow state—the pure, heads-down, "zone" feeling. But AI coding doesn't always foster that same immersion. You might spend an hour setting up prompts, letting the AI build stuff in the background, and occasionally popping over to approve or nudge it.

For some folks, that's jarring. For others—especially those who have kids or who juggle a million tasks—it's liberating. When you can context-switch (check the AI's output, jump back to real life, then come back to a functioning snippet), you realize there's a new way to be productive that doesn't revolve around long blocks of quiet time.

---

### Does This Mean "Peak Programmer?"

There's chatter that once AI can generate code, we've hit "peak programmer"—that soon we won't need as many engineers. That might be partly true if we're talking about straightforward feature work or hooking up an API. But there are new complexities, too, around security, compliance, test coverage, and architecture.

The real difference? "Strategic engineers" will flourish—those who can orchestrate multiple AI tools, keep an eye on code quality, and design new systems that scale. The folks who thrive will be part product manager, part architect, part QA, part developer. They'll shape the prompts, define the tests, maintain quality, and handle all the edge cases an LLM doesn't predict.

---

### Pro Tips from the Front Lines

A few things I've personally learned the hard way:

1. **Start Manually, Then Turn On the AI**

    For iOS apps, initialize the project in Xcode first, so the auto-generated files don't confuse the AI. Then let the AI fill in the rest.

2. **Short, Clear Prompts Sometimes Outperform Long Instructions**

    Oddly, telling an LLM "make code better" can work as well as a super-elaborate prompt. Experiment—some models respond better to fewer constraints.

3. **Use a "Checkpoint" Workflow**

    Commit often, even if it's "Commit –m 'It passed the tests, I guess!'" AI can break everything just as quickly as it can fix it. Frequent commits give you easy rollback points.

4. **Prevent AI from Over-Testing the Basics**

    AI loves to test everything, including whether a `for` loop still loops. Stay vigilant, prune pointless tests, and keep your pipeline lean.

5. **Document Absolutely Everything**

    Let the AI generate big "Implementation Guides." These guides not only help you but help the AI itself on subsequent passes.

---

### Final Thoughts

Our industry is shifting faster than it ever has. Some of our well-worn assumptions—like the centrality of the flow state, or big celebrations around meticulously hand-coded features—are about to look quaint. But that doesn't mean we lose our creativity. Instead, it becomes about strategic orchestration—knowing what to build, how to describe it, and how to keep it from turning into a dumpster fire.

In the end, we might see that what makes your product win isn't brute-forcing code. It's designing an experience users love. Because if we can spin up 10 versions of Instagram in a weekend, the tiebreaker won't be how elegantly the code is written. It'll be which one resonates with people—and that's a design and product problem, not purely an engineering one.

So welcome to the new waterfall—done in 15-minute cycles, with AI as your infinite junior engineer and your code pipeline on hyperdrive. It's weird and wonderful and occasionally terrifying. And odds are, we're all going to have to learn this dance one way or another.

—

_Hope this condensed conversation offers a little insight into how AI-assisted coding is changing the game, and how you might adapt. While there's definitely uncertainty in the air, there's also an opportunity to let humans focus on what humans are really good at—defining, designing, and delivering products that matter._
