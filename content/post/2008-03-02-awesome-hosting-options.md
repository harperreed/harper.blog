---
date: 2008-03-02T02:32:39Z
tags: ["technology","hosting","rackspace","mosso","servers","mediatemple","webfaction","fdcservers"]
title: Awesome hosting options
wordpress_id: 1510
wordpress_url: http://www.nata2.org/2008/03/02/awesome-hosting-options/
---

I spend WAY WAY too much time trying to figure out where and how to host my websites. I guess you could it a hobby. A really horrible and expensive hobby. It isn't a great way to meet friends, enjoy life or honestly save money. However - it prepares me for the awesome ability to bitch about hosting and to write this blog entry.

A couple weeks ago, Mosso changed some stuff and got my buddy <a href="http://broox.com">Derek</a> and I got to talking about hosting options if Mosso doesn't pan out. I decided that since I have this perverse hobby, I should document my journey.

So here is my list of hosting providers I recommend and enjoy!

<b><a href="http://mosso.com">Mosso</a></b>: This is currently my friends blog and generic client hosting favorite. It is easy to use, has amazing service and hilarious growing pains. I have been using them for about a year - and have been VERY happy with pretty much everything. They currently have <a href="http://www.nata2.org/2008/02/29/the-mosso-cloud-how-requests-are-not-a-good-metric/">some crazy billing issues</a> to work out - but when they figure that out, I would certainly recommend using them.  One thing to keep in mind: if you have clients, you can't do any better than Mosso - they can white label EVERYTHING (including phone support). It is awesome.

<b><a href="http://www.mediatemple.net/">MediaTemple</a></b>: These guys are cool. Seriously. I didn't really like MediaTemple until I hung out with the dudes. They are doing cool stuff with virtualization and easy scaling. For instance, you could get one of their horribly named <i>(dv) servers</i> for around 50 bucks a month and then if you ever have a problem with the resources or "scaling"" abilities with the virtualized server, you can just go ahead and "seamlessly" upgrade to a dedicated box. This is because their dedicated boxes are just virtualized instances as well as the (dv) servers. So upgrading the box is as simple as copying your server image from the shared box to the dedicated box. You don't have to change IPs, copy your content or really any of the stupid shit that makes scaling annoying. Now this is of course in theory (and told to me while i was drunk). I have never actually don't this. BUT - it seems like it should and would work.  (if you can shed some light on this - let me know).

<b><a href="http://www.fdcservers.net/">FDCservers</a></b>: FDC servers is interesting. I can't imagine that they are solid or have good support in times of need. Or that their servers aren't made from ants and cheese. But seriously. They are cheap, support is good and they are FAST. They have some of the cheapest, fastest servers i have ever seen. Its out of control (and fast and cheap (what a good documentary)).  I don't hesitate to use them whenever I need a  fast, cheap server with a FAT pipe. But - I am worried that someday their servers will turn to dust without a warning. But until them - they are my secret dedicated server host.

<b><a href="http://www.webfaction.com?affiliate=harper">Webfaction</a></b>: Webfaction is my new best friend. Seriously. If I wasn't already married to an beautiful, awesome woman, I would marry webfaction. They have blown my mind. You are able to use ANY web technology you want to use. They have decent resource allotments and they are rather inexpensive. Especially considering they are expecting you to use long running processes like Ruby or Python frameworks or apps. Pretty sweet. If you want a host that allows you to host a wordpress blog, experiment with web.py, run a rails app and allow you to rock out with django - all under the same domain root - webfaction is your host. The secret is that its all proxied. So when you set up a rails app, it tells you the port number to run that app on. Then it maps that port number on the localhost of the box to /railsapp on the public IP. I currently host my blog and homepage at webfaction. I trust them more than any of these others (I am furiously knocking on wood you read this).

<b><a href="http://www.rackspace.com">Rackspace</a></b>: Rackspace is obviously not your general needs host. It is probably the best host you can get. But don't just grab a Rackspace server and think your good. You gotta get the intensive support. Its like having a concierge service for your hosting. Its incredible. If you are a small organization, and don't want to have to worry about all the nonsense that goes with managing servers, infrastructures, data centers - then give Rackspace a call. They have really helped us (threadless) grow and scale. They are solid.

These are the hosts I use on a daily basis. All of them i recommend. Obviously you wouldn't use Rackspace to host your not often read blog, and you wouldn't use webfaction to host your $100MM social network. However, all of these options have one thing in common. They all have decent support and they all seem to LOVE what they are doing. I can't deal with vendors who offer products that they themselves wouldn't use. You can't trust those guys. You can trust all these guys (except FDC - with their prices, they have to be doing something tricky. heh. ).