---
date: 2026-01-05T18:10:00-06:00
description: ""
bsky: false
draft: false
tags:
    - productivity
    - tools
    - travel
    - agent
    - llm
    - prompts
title: "How to find magical travel experiences using an AI travel buddy"
generateSocialImage: true
translationKey: llm-travel-agent-friend
slug: llm-travel-agent-friend
---


I have been traveling and using ChatGPT for the last few years. Super helpful. I started doing this in 2024, and it was a bit rough - but it surfaced some amazing gems. It has gotten really good over the last year or so. Especially in places where I don’t speak the language. 

I primarily use this to hang out in the more rural areas of Japan when I am on family vacations. It is very effective, and has found us some really wonderful spots. The process is effectively extracting your travel vibe, and using it to prompt the models. This allows the experience to lean really far into your personal vibe, and maybe allows for a bit more serendipity and magic than your usual guide book or YouTube video.

TLDR: build taste profile, add to prompt, make project in ChatGPT. Use this as project instructions ... profit. 

> You can add this to openclaw, etc. it works for the most part. I find that ChatGPT/Claude is what most people are using and the apps work really well while traveling. 
> 
> here is a skill that you can drop into your agent harness and make magic: [harperreed/travel-agent](https://github.com/harperreed/travel-agent). You shoudl be able to install it in most places with `npx skills add harperreed/travel-agent`
>
> Ostensibly this also works in chatgpt, claude but i haven't really tested it. I have only tested the non-skill process in those contexts. 


## Your tastes

Do this before your trip 

The first thing is to figure out your taste profile. Spend 30 min doing this and you will have a very nice taste profile to use when prompting ChatGPT. It is important to remember that we are all different and you do yourself no favors by lying to the interview. Nobody is watching but you, the feds, and Openai. 

Here is the prompt:

```prompt
Help me build a taste profile for travel, restaurants, shopping, hotels, things to do, and cultural experiences.

Ask me one question at a time.

Keep questions very easy to answer. Prefer yes/no, multiple choice, or short forced comparisons. Avoid open-ended questions that require me to explain or write more than a few words.

Occasionally ask me to name a specific restaurant, store, neighborhood, hotel, city, movie, object, or experience I loved or hated when a concrete example would tell you more. If needed, use simple follow-up questions to figure out why I liked or disliked it.

Focus only on **taste**, not medical, dietary, accessibility, family, or other logistical constraints.

Capture:

* strong preferences
* strong dislikes
* meaningful trade-offs and tolerances
* several concrete “taste anchors” that can be used to compare unfamiliar things

Adapt your questions based on what you learn. Do not follow a rigid questionnaire or repeat the same idea in different ways.

Stop when you have enough information to reasonably predict what I would probably like.

At the end, output **only one compact taste profile of no more than 250 words**, suitable for pasting into another AI’s instructions.

Compress aggressively. Include only information that would materially affect recommendations. Include the strongest taste anchors, but do not summarize the interview or explain your reasoning.
```

Go through and answer questions. Once you are done with the Q&A and it outputs the summary, change to a higher reasoning mode (highest is best) and ask it to generate the taste profile. 

The taste profile should look something like this:

```prompt
The user is exploring Tokyo with a strong preference for hidden, local, and atmospheric experiences. Prioritize places with a modern, but retro or nostalgic feel (昭和-era aesthetics), subtle wabi-sabi textures, and nature quietly integrated into the city — such as overgrown alleys, mossy shrines, or ivy-covered rooftops. 
```

It shouldn’t be perfect, cuz you are not a perfect person! 

# The System (Prompt)

This is my prompt for Japan. ChatGPT helped me write it. But it should work for any locale. A couple notes: 

- It uses web search in the native language of the locale.
- It will tell you how to pronounce things
- It tries to summarize, and not just do word for word computer translation
- Various bits are custom to me

```prompt
* When conducting web searches, search primarily in the local language(s) of the destination, using the terms a local person would use. Use English or other languages as a secondary search when useful.
* Always respond in English unless the user explicitly asks for another language.
* When names use a non-Latin script, include the original name plus a common transliteration.
* Summarize local-language sources naturally rather than translating them word-for-word.
* Assume the user has high digital and cultural fluency. Be concise, but preserve texture and charm when describing places.
* Prioritize recommendations that strongly match the user's taste profile and party constraints. Do not default to major tourist destinations or generic "top 10" recommendations unless they are genuinely a strong match.
* Feel free to suggest nearby or related discoveries when they are unusually good fits.
* Prefer local and first-party sources over English-language travel sites, SEO lists, or generic aggregators.

For restaurants, shops, venues, events, and other places that can change frequently:

* Verify important details using a first-party source when possible: official website, official social account, ticketing system, reservation system, etc.
* Also check a respected local review, directory, or discovery platform when one exists.
* Include useful links such as the official site, social account, local listing, reservation/ticket link, and address when available.
* Because places close and hours change, perform a separate current-status check before recommending something.

Distinguish between:

1. **OPERATING** — there is current evidence the place still exists and is active.
2. **OPEN** — there is evidence it should be open at the requested date/time.
3. **AVAILABLE** — there is evidence the user can actually visit, reserve, buy a ticket, or otherwise use it at that time.

Do not infer one from another. Never claim something is available unless you can verify it. If you cannot verify hours or availability, say so plainly.

If sources conflict, tell the user and prefer the most recent first-party information.

For immediate requests like "I need food right now," prioritize:

1. hard constraints;
2. actually open;
3. realistically reachable;
4. likely availability;
5. taste match.

Prefer a few excellent, well-researched recommendations over a long generic list.

Think through the request, the user's taste profile, party constraints, location, timing, and what information needs current verification before answering.
```

I then have a section that I call **Party Details**

```prompt
PARTY DETAILS

Harper Reed - late forties male. Harper has tattoos. Eats everything but Uni. 
Person 2 - ....
Person 3 - ....


Interests: 
- ....
- ....
```


Then comes the taste profile:

```prompt
The user is exploring Tokyo with a strong preference for hidden, local, and atmospheric experiences. Prioritize places with a modern, but retro or nostalgic feel (昭和-era aesthetics), subtle wabi-sabi textures, and nature quietly integrated into the city — such as overgrown alleys, mossy shrines, or ivy-covered rooftops.
```

Add it all together like this: 

```
<INSTRUCTIONS>

---

<PARTY DETAILS>

---

<TASTE PROFILE>

```


## Now what? 

Go to ChatGPT and create a "project." This has two unique properties that are really nice:

1. All of your trip chats are in one place, and easy to find. 
2. You can make "instructions" for this project (the above system prompt)

Once you create the project, go into it and add the above created project instructions to the  "**instructions**" of the project. 

Now you are ready to go!

## Let's do it

Now you can ask: 

"I am hungry RIGHT NOW, and I need a place to eat. I am in Setagaya near Meguro.“

And it will output some really good options that fit your party requirements, your taste profile, and *typically* be open, and available for you. 

### Drugs are bad. 

This thing still gets things wrong, and you really have to double check. But mostly it is stuff that humans also get wrong: 

- is a thing open? 
- what about availability
- was it closed in 2023? 
- etc

Typically you can ask, and it will find out. I have found that you can get it to act correctly, but you may have to do the final leg of verification.  

## The results

This has been a real fun addition to my lil tool set. I have spent a lot of time in Japan, and know mostly what we are doing. This has found some spots that we adored, and would not have found otherwise. Kind of wild. 

My pro tip is that you can do comparisons that are irrational. Like: 

"I really like Handlebar (chicago vegetarian punk restaurant) and I want something similar in Shinjuku that is open tomorrow"

And chatgpt will respond with something like: 


> NEO 新宿アツシ – Cyberpunk Vegan Bar.  
> A hidden gem on the 4th floor of a tight side‑street building near Shinjuku‑sanchōme—this place is all neon, exposed wiring, retro‑futuristic cinema vibes, and loud electronic beats. The menu is 100% plant‑based, with vibe‑fit items like vegan “calbi BBQ burger” and “vegan cheeseburger,” plus wild drinks like “electric lemon sour” and “blue neon soda” .
> 
> Address: 新宿区新宿3‑3‑7 三慶ビル 4F (1 min from Shinjuku‑sanchōme C3 exit)~~‌~~
> 
> Tabelog: active and open — expect a punk‑futuristic, neon‑lit interior with a small counter and intimate tables.
> 
> Why it hits the mark:
> This isn't polite Muji minimalism—it’s raw, neon‑lit, full of wired ambience, and unapologetically future‑punk. 

This obviously isn't handlebar, but it is vegan, and has a VIBE. I also wouldn't have found it otherwise! 

# Transference

This works for locales outside of Japan. It works for your hometown, etc. 

The examples are all restaurants and travel - but it also works for shopping, and really anything. 

it kind of rules. 

# The magic

The magic that we just went through is capturing in a rather efficient taste profile that you can carry with you and jam into pretty much anything: chatgpt, claude, google, etc.

If you followed this exactly, you have created a handy and effective travel workspace that will know you scarily well. You will find magic spaces that you wouldn’t have found by reading reddit, or other English focused spaces. 

Hope this is helpful! 
 
