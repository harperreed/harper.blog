
---
title: "Digital Contact Tracing and Alerting vs Exposure Alerting"
date: 2020-04-22T22:34:27-05:00
draft: false
---

> There are only two hard things in Computer Science: cache invalidation and naming things.
>
> -- Phil Karlton

TL;DR: 

  * Digital contact tracing should be called Exposure Alerting
  * That is what it does. It doesn't "trace contacts" from an epidemiological perspective. 
  * Exposure Alerting could tie in with contact tracing, but we should not conflate these separate technologies. 
  * Manual Contact Tracing is essential and is very different than Exposure Alerting
  * Exposure Alerting should be decentralized. Manual contact tracing is centralized. 
  * Exposure Alerting has very specific [privacy concerns][1] that are very different than Manual Contact Tracing 

   [1]: https://contacttracingrights.org

* * *


Over the past 6 weeks, I have been working with some fantastic people to help figure out what tech is appropriate to address the Covid19 crisis. I am skeptical of technology being the hammer that matches all these nails - but there are appropriate uses.  

It is a unique experience. Everyone I have worked with is laser-focused on the same goal:

  * to end the crisis
  * to save lives
  * to get out of lockdowns
  * to restart our economy

In my past, I have been part of tech movements that have had a similar property: a pure focus. It is exhilarating and inspiring. More importantly, it makes the job easier when we all have the same motivations.

There are two objectives getting a lot of buzz: one is to alert people if/when they come in close enough proximity to someone who's infected and the other is more aligned with what epidemiologists traditionally call contact tracing. These two scenarios have popped up a bunch over the last 6 weeks, as dozens of companies are working to build solutions for them. 

The idea is simple:

Using the device in your pocket, you can make sure that if you are exposed to someone who currently has Covid19, you can be alerted. This is done with some fancy cryptography, some fun bluetooth communications and an improbable amount of buy-in by the consumer. It also requires people who have tested positive for Covid19 to also participate and trigger exposure to the network.

I found this idea compelling, but had a few concerns: 

  * Privacy
  * Interoperability

I got to work to try and solve some of these issues. 

  * A group of us launched [contacttracingrights.org][2] - a framework for digital contact tracing individual data rights. We noticed that there wasn't a solid foundation for building these solutions in a privacy-preserving way. Luckily we had a lot of folks who had thought about this before, and we could learn from them. We just collated and massaged the words until we felt it allowed for that foundation. 
  * I was a minor player in helping organize the [TCN coalition][3] - a coalition of app developers, protocol designers, and organizations that are building solutions to enable alerting of exposure. The goal was to get everyone working on the same ideas. Interoperability is critical, and working together is vital. TCN Coalition is helping make that happen. 

   [2]: https://contacttracingrights.org/
   [3]: https://tcn-coalition.org

After we pushed out this stuff, the public started to notice. The concept of digital contact tracing was in the press more. People were clearly thinking about these solutions as a tool to "get out of lockdown."

I found myself in conversations with lots of folks about these technologies and was helping many companies, states, foundations, etc. understand how they could recommend or use this tech. 

One thing that became clear was that a lot of the people who were trying to understand digital contact tracing were conflating these two ideas[a][b][c]. This included government people, epidemiologists and others who were deeply familiar with contact tracing and public health. processes. This leads to these officials expecting contact tracing results, or data from the digital contact tracing technology. 

It seems that we have a problem with vocabulary. We were talking about two things, but using the same words, vocab, etc. and it was confusing. 

Some background: 

Contact Tracing is an essential tool for understanding and stopping disease transmission. It is a bread and butter function of public health, and has been used to successfully eradicate smallpox; to limit the spread of Ebola during outbreaks; and, most often, to handle outbreaks of diseases such as TB and HIV in our own cities. All of our excellent public health departments have people who are focused on contact tracing. 

One of my favorite organizations, [Partners in Health][4], is currently doing a lot of work to get manual contact tracing out in our world to stop this virus. It is very much one of the best tools to stop Covid19. You can find out more about contact tracing on the [very helpful Wikipedia page][5]. 

   [4]: https://www.pih.org/
   [5]: https://en.wikipedia.org/wiki/Contact_tracing

As my friend [Alli Black](https://bedford.io/team/allison-black/) explained, Manual Contact Tracing typically involves interviewing a person who is confirmed to have whatever disease you're investigating. The epidemiologist wants to provide resources to support and educate the confirmed case, and also collect information about who the case interacted with while they were infectious. The goal of this second part is to find people who could be infected early enough on that you can prevent them from spreading the disease on to other people. Traditionally, these interviews are conducted via phone or in person. Given the number of people who could become infected with Covid, and the need to perform contact tracing quickly, there are some new technologies that are doing Manual Contact Tracing via web-based or mobile surveys. But these technologies still fundamentally follow the principle that the confirmed case will tell the epidemiologist who they had contact with. This is very different from exposure alerting apps or technologies. 

Once we started describing digital contact tracing tools, it was only a matter of time before someone would say, "Is this contact tracing?"

And we would spend a lot of time explaining that although the name is the same, the results are quite different

**Digital contact tracing and alerting as defined by these apps, Apple and Google, and many of the protocols don't actually do "contact tracing" as expected by epidemiologists and public health officials. What these apps, protocols, etc. do is alert a consumer to potential exposure.**

Alerting to exposure is very important. It fits nicely into the traditional world of contact tracing (at the very very beginning). However, it is not synonymous. To use the same words to describe these two concepts isn't helpful. 

This is why I have started calling this type of tool, "Exposure Alerting." I originally called it Digital Contact Tracing. Then for our privacy framework, we changed it to Digital Contact tracing and Alerting (DCTA). That last bit - alerting - wasn't clear enough. Let's start calling it what it does:

## Exposure Alerting

I hope this is helpful. 

* * *

A couple other thoughts: 

  1. Originally I had suggested calling this technology Exposure Proximity Alerting - with proximity is a redundant. In a lot of the conversations we ended up explaining that the alerting was done via a very specific method of determining proximity. I received some really helpful feedback from Tina White of [Covid Watch][6] that we should call it just Exposure Alerting. Originally, I thought that the redundancy helps clarify another question: how do you track the exposure? Going forward, I think calling these solutions Exposure Alerting as Covid Watch does is sufficient. I will continue to use Exposure Proximity Alerting when verbally describing this tech when helpful. FWIW the WHO seems to call this "Exposure Notification." It is unclear if they are also talking about these apps or just general exposure notification.  

   [6]: https://www.covid-watch.org/

  2. There are two aspects of Exposure Alerting that I think are really important:  Privacy and Decentralization. Many of the better solutions take advantage of these aspects (CovidWatch, CoEpi, Apple/Google protocol, TCN protocol, DP^3T protocol, PACT protocols and others). There are a few, however, that do alerting without following the best privacy practices or being decentralized. I think that privacy and decentralization should be required. It was one of the main reasons we launched the [contacttracingrights.org][7] framework (now we need a new domain hah). 

   [7]: https://contacttracingrights.org/

* * * 

Thanks to a bunch of folks who read and commented on this post. Especially: Adam Conner, Andreas Gebhard, Andy Moss, Chris Messina, Dylan Richard, Jenny Wanger, Tina White

I am sure a few I am missing others who helped out. It is more clear than ever that I am standing on the shoulders of giants. Thanks for all your help 
