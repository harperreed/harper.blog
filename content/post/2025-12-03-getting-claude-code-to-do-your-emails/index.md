---
date: 2025-12-03
description: A personal journey using Claude Code with MCP servers to manage overwhelming email during the holidays. From building custom skills to creating drafts, this explores how AI agents can help triage your inbox while maintaining your authentic voice - with lessons learned from accidentally letting an agent say yes to writing a book.

draft: false
tags:
    - ai
    - agents
    - claude
    - mcp
    - email
    - productivity
    - automation
    - tools
    - pipedream
    - personal-assistant
title: Getting Claude Code to do my emails
generateSocialImage: true
translationKey: Claude Code Email Management
slug: claude-code-email-productivity-mcp-agents
---

Over the last week or so, I have been using Claude Code to help me with some email, and scheduling. It started cuz the holidays are overwhelming, and I felt like I was constantly behind. My inbox was overflowing with everything I had deemed important, and I hadn’t been able to make a dent. It was stressful. It still is!

{{% figure src="R0002380.jpeg" caption="Maybe a storm?, Ricoh GRiiix, 11/2025" %}}

I had just seen the [zo.computer](https://zo.computer) launch (neat project!) and it reminded me that [Pipedream](https://pipedream.com) has this wild MCP server that you can use to connect to literally anything Pipedream supports. This means I could use it to do my emails! Problem solved. Problem created. More problems created! WHY ARE WE COUNTING PROBLEMS!

## How? Why? HUMANS ARE DYING AND GOING EXTINCT

I love email. I really do. Typically I am really great at managing my email. However, when the email gets overwhelming - I end up ignoring it. Which means it gets worse. Which means everyone loses.

I just need a way to start doing my email that is pretty low pressure. Using Claude Code has made it MUCH easier.

1. I boot up a Claude Code session hooked to the proper MCP servers.
2. I ask it to check my email
3. It tells me what email is in my inbox that needs addressing (unread, then read email)
4. Either offers to start fixing emails, or just starts writing drafts intelligently (checks my calendar, searches for context, etc).
5. Says “We are done!”
6. I go to my email client, and check the drafts. Edit and send most of them cuz they are great. Reject a few.
7. Rinse Repeat
8. Bacon

Basically, I just have Claude Code check my email, and then pops out a message like “your brother emailed asking about thanksgiving plans” and I say “cool. Tell him we will be there, and will bring turkey juice or whatever you call stuffing” and then Claude Code will write an email that is approximately what I said but in the style it found from your past emails.

I then specifically save it as a draft that I review heavily before sending.

> I trust these agents to write code way way more than I trust them to write an email to a friend, stranger or business partner. It is pretty close, but not quite close enough to go yolo mode and let it send. Maybe soon? Or maybe a different email address? Who knows.

It works remarkably well. However, there are some gotchas

### Funny story that isn’t so funny.

A while back I was prototyping an email triaging agent with some code I had written, and it was working well but not great. A friend connected me to a person who was looking for someone to write a book about AI. The agent was like “this person wants to talk about writing a book about ai, they want a skeptical and academic perspective about AI’s impact” and I was like “I LOVE THIS. But this isn’t for me. I have some friends that would be good.” However, there was a bug, and the agent was drafting replies before getting feedback from me. And it ended up sending the previous draft that said very formally: “I would love to do this.”

The person excitedly replied and was like “let’s do this.”

That is when I found out that I fucked up. So I replied back and was like “well. My agents said yes for me before talking. Here is what I meant to say” and that person rightfully replied “**F U**”

### You cannot trust these things.

This is why I am cautiously doing it again. Haha. This time I am way more careful, and the agent cannot send email only draft it. I am finding that I am editing every email - but only a little, and maybe less and less. Feels like a year ago with codegen.

Thus far it works pretty well. It allows me to get through a lot of email that I normally would ignore, giving me space to focus on the emails I really want to reply to. Basically it cleans up the cruft (vendors, services, etc) and allows me to hang out with my friends. Perfect AI usage.

I recommend it.

## Replicate my setup?? If you dare!

I didn’t want to start fresh every time so I built a super simple Claude Code “directory.”

It has most of the things that you will need to handle triaging your inbox.

```
📁 .
├── 📁 .claude
│   ├── 📄 CLAUDE.md
│   ├── 📄 settings.json
│   └── 📁 skills
│       ├── 📁 crm-management
│       │   └── 📄 SKILL.md
│       └── 📁 email-management
│           └── 📄 SKILL.md
├── 📄 .mcp.json
```

There are a few important parts:

### The CLAUDE.md

This is highly personal (how do you manage YOUR inbox), and very important. The first thing I did was have Claude go through the past couple hundred emails I have sent, and develop a vibe for how I write emails. After a bit of back and forth, we have this:

```
1. **Find the thread**: Search for the original email/thread to get context
2. **Get thread details**: Retrieve the thread ID, message ID, AND recipient email address for proper threading
3. **Check for calendar events**: If the email mentions an event, proactively check calendar and add it
4. **Draft the email**:
    - **CRITICAL**: Always explicitly provide the `To:` email address - the MCP tool does NOT auto-extract it from threads
    - Keep it ultra-concise (but adjust based on context - some emails need warmth)
    - Match Harper's voice (casual, direct, no fluff)
    - No signatures or sign-offs
5. **Always create as DRAFT**: Never send directly - always save as draft
6. **Ensure proper threading**: When replying, use thread ID and in-reply-to message ID so the draft appears in the conversation thread
7. **Iterate on feedback**: Harper will refine the wording - update the draft as needed
```

### The skills

Then I went through and did a bunch of emails via Claude Code. It did ok. But I was able to coach it, and once it was in a good place I had it make a skill based on what we discovered together.

```
## Core Principles

1. **Always draft, never send** - Save emails as drafts so Harper can review before sending
2. **Threading is critical** - Replies must appear in the correct conversation thread
3. **Match Harper's voice** - Ultra-concise, casual, no signatures
4. **Extract structured data** - Pull event details, action items, contact info from emails
```

And

```
## Success Criteria

You've successfully handled email tasks when:
- Drafts appear in correct conversation threads
- Harper says "looks good" without needing changes
- Calendar events are added proactively
- Inbox summaries surface what matters
- Process feels efficient and natural

## Remember

Email is personal communication using Harper's voice. The goal is to save time while maintaining authentic, effective communication that sounds like Harper wrote it.

When in doubt: shorter, more casual, and always draft first.
```

Having Claude build its own skills is clutch. You really need to iterate to make it happen.

### the tools!

I am still mad about MCP as a concept, but not mad enough not to use it.

The goal is to simply give Claude Code a suite of tools that allows it to do its job well.

```
{
  "mcpServers": {
    "pd": {
      "type": "http",
      "url": "https://mcp.pipedream.net/v2"
    },
    "pagen": {
      "type": "stdio",
      "command": "pagen",
      "args": [
        "mcp"
      ],
      "env": {}
    },
    "toki": {
      "type": "stdio",
      "command": "toki",
      "args": [
        "mcp"
      ],
      "env": {}
    },
    "chronicle": {
      "type": "stdio",
      "command": "chronicle",
      "args": [
        "mcp"
      ],
      "env": {}
    }
  }
}
```

### Pipedream

The [Pipedream MCP](https://pipedream.com/docs/connect/mcp/developers) is very straight forward. You essentially add it to your Claude Code (works in other clients too), and then it will pop you through their auth. Once auth’d you add various services. Those services are then exposed as MCP tools. These are clutch. You can then use Claude to wire together some workflows.

I currently use their Gmail, Google Calendar, and Contacts connections.

### The others:

I created 3 simple MCP servers that I wanted to exist:

#### Toki

a super straight forward todo tracker on the CLI. The plan is to build out support for various backends. Currently it is just local.

It works as a cli app or as a mcp server:

You can try it out here:

- [harperreed/toki](https://github.com/harperreed/toki)
- `brew install harperreed/tap/toki`

#### Chronicle

a log for agent actions. I want my agents to log what they have been up to!

You can try it out here:

- [harperreed/chronicle](https://github.com/harperreed/chronicle)
- `brew install harperreed/tap/chronicle`

#### pagen

a misspelled crm that acts as my **p**ersonal **agen**t backend. This allows me to have reasonable understanding of where I am from a comms, etc standpoint

You can try it out here:

- [harperreed/pagen](https://github.com/harperreed/pagen)
- `brew install harperreed/tap/pagen`

### Wrapping it together.

The robust skill, the claude.md and the MCP tools make this a pretty easy and helpful system for triaging email. It is not perfect, but it does work nicely.

I do recommend playing around with this. I would maybe be cautious about blindly trusting it. Lol.

## Wanna try it?!

I made a simple plugin that should do this for you. All you gotta do is install it!

Installation Now:

```
/plugin marketplace add harperreed/office-admin-claude
/plugin install office-admin
/setup-office-admin
```

YMMV

## This is obviously the future.

Whether we like it or not, it appears that agentic email will be a thing. It is early enough that we will start to see people like myself building bespoke and custom experiences that largely do what a product will do. Somehow Google will launch a version directly in gmail, that somehow doesn’t work. My guess is that the best versions will be like Mimestream or superhuman that are primarily agentic. I hope it isn’t primarily chat - but we shall see.

I do recommend playing with this. Especially if you have a lot of email that you need to take care of. I think of it as clearing brush. You don’t want to fuck up the flowers (all of you. you are my flowers), but you don’t mind cutting down the weeds (all of them! You can see the random emails about business loans lurking in the corners..)

### Privacy, what privacy!!

My emails are going through Pipedream, and Anthropic. This is not ideal. it is obviously a privacy concern. I can't wait to run these things locally, and maybe have an MCP server that interacts directly with Google Suite.

### Be cautious

{{% figure src="L1030630.jpeg" caption="Not even once, Leica Q, 11/2017" %}}

Giving your agents access to things that affect other people is scary and should be done with caution. It works pretty well for me, but I did totally fuck up a few situations trying this out.

My inbox is pristine. DO NOT SEND ME EMAILS! IT IS BEAUTIFUL!
