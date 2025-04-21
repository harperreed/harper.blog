---
date: 2025-01-12 20:59:59-05:00
title: New Media
description: Adding a media section to my website to track and display what I'm reading, listening to, and bookmarking online through automated data collection.
draft: false
generateSocialImage: true
tags:
    - personal-data
    - hugo
    - rss
    - media-tracking
    - automation
    - web-development
---

_tl;dr: I added a media section to my website to track and display what I'm reading, listening to, and bookmarking online through automated data collection. visit it [here](/media)_

Recently I spent a few hours hanging out with my friends Claude, Aider, and ChatGPT and added a [media section](/media) to this site. I really enjoy AI-aided development (maybe a post for later).

The media section has a log of all my books [read](/media/books) (tracked from Goodreads), my recently saved [tracks](/media/music) (tracked from Spotify), and my [links](/media/links) (tracked from feedbin/netnewsreader).

I started posting my links a month or so ago. I wanted to see how the workflow felt. I think it is important for these types of things to just work, without a lot of BS or additional interactions from me. After a month or so, it was fun to see the links that I was saving show up on the site. Like magic.

{{< image src="new-media-sufjan.jpeg" alt="New Media" caption="Sufjan Stevens, Leica Q, 7/17/2016" >}}

## Why Track?

I did this partially cuz I miss my websites of the past where I manically tracked everything. It was so much fun to see a daily log of everything I consumed and participated in. However, time passed and everything kind of fell apart (mostly my crons).

The other reason I did this was inspired by my friend Simon and his project [dog sheep beta](https://github.com/dogsheep/dogsheep-beta). I wanted a robust way to track a bunch of data and save it. I thought about just putting it in sqlite and stuffing it away in a corner of my GitHub to forget about. That is boring tho. I want to force all y'all to see it all in its glory.

Instead of SQLite, I ended up making just a handful of scripts that grab the entities, drop them as YAML files and generate entries for my Hugo blog. The result is ultimately the same - but now I get both the data and the posts.

I love this cuz I can see my media consumption, force you to see it, and store this for later!

### RSS Feeds

You can check out the feeds for the individual sections quite easily:

- [Full Media RSS](/media/index.xml)
- [Books RSS](/media/books/index.xml)
- [Music RSS](/media/music/index.xml)
- [Links RSS](/media/links/index.xml)

I use [NetNewsWire](https://netnewswire.com/), and [feedbin](https://feedbin.com) and it works great. Highly Recommended them.

I will post most about RSS at a later date!

## Simple Tools Are Better Tools

I love hacking on Hugo. It's fun and super limited. I find the best things are those with fewer options. I don't want to have to deal with unlimited optionality and magic - just a bit of magic.

With Hugo, I can just jam a bunch of markdown into a folder with proper front matter, and then it kind of just works.

Beautiful.

### YOU IN THE CORNER!

If you want to do something like this yourself, I would recommend checking out [micro.blog](https://micro.blog). It's awesome and can do similar things. The new [micro.one](https://micro.one) service is a good, cheap way to get started.

## New Media

{{< image src="harper-politics.jpeg" alt="New Media" caption="My very serious office, unknown camera, 11/8/2012" >}}

Unrelated to anything: When I worked in politics years and years ago, the generalized term for tech folks, etc., was "new media." I always found it funny because from my perspective it wasn't new, it was media.
