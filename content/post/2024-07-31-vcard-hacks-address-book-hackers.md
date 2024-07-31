---
title: "Contact management in 2024: Stupid vcard tricks for hackers"
date: 2024-07-31T09:00:00-05:00
description: "Too many contacts, apps crashing. Ditched fancy solutions for old-school vCards and vdir. Wrote scripts, used khard for CLI management, vdirsyncer for syncing. Deduped, sorted, version-controlled my digital Rolodex. Google's still a pain with UIDs. It's messy, it's overkill, but it's mine. Command-line junkies, this one's for you!"
draft: true
---

## How to really fuck up your contacts and also get control back

I have too many contacts. Seriously. Like many thousands. It is uncomfortable.

I do not recommend it. All the apps are like “I want to use your contacts” and then they die cuz too many contacts. Certain apps are slower, some apps crash, and most apps are like “wtf.”

To solve this, I have used all manner of contact management solutions:

- Google Contacts - decent interface, kind of slow, and stupid.
- Contacts Plus - good syncing, kind of annoying, not as slow, good tooling (deduping, etc).
- Sunshine - I like the team, I like the product. A bit too fancy in some regards. I like the interface for their tooling. Very usable

However, I wasn’t satisfied.


{{< image src="/images/posts/vcards-i-should-buy-a-boat.jpg" caption="Buy why shouldn't I? " >}}

## Self Sovereign Contacts

I don’t know what that [means](https://en.wikipedia.org/wiki/Self-sovereign_identity) - but it sounds pretty cool.

In my limited worldview, I am looking for control of my info, autonomy over management, and the ability to remove my info from third parties that use it.

In regards to my contacts, this means I want to be able to see a log of everything that is happening. Control who gets what. And be able to edit, delete, and modify with ease.

You would think I could get most of these requirements from any of the options listed above. And you kind of can. However, it isn’t exactly how I wanted it.

In the 1990s I started using the command line and that is my happy place. I needed command line control over my contacts.

## Enter the vdir

I have always loved vcards. I have written so so many scripts to manipulate vcards over the years. Screen scraping conference apps to get attendees, pulling from friends academic websites to get updated contact info, etc. Cleaning up vcards, backing up cards, etc. Lots and lots of work to make contacts awesome.

I started looking for vcard management tools!

Aside: I miss maildir. Lol

**vdir** is what people seem to be calling a directory that holds vCards or vCalendar. It allows you to dump all your vcards into a `contacts` directory and then manage them as independent vcards. This is really handy!

One of the main tools to manipulate, search and manage your contacts vdir is called `khard.` It is a simple cli app that will interact with your contacts. Works great!

This unlocked one magical thing that I have been wanting for ages: separate contacts.

I wanted to be able to have separate address books:
- Primary: all of the people I normally contact
- Secondary: people who I know but aren’t in normal contact
- Other: all the people who I have interacted with over time

This allows me to have 16k contacts, but not 16k contacts on my phone.

`khard` does this easily. You just create multiple directories and then config khard to use those dirs:

```shell
[addressbooks]
[[main]]
path = ~/.contacts/main/
[[secondary]]
path = ~/.contacts/secondary/
[[Other Contacts]]
path = ~/.contacts/other/
```

This is effectively solved my problem.

I went ahead and downloaded a good backup of all my contacts from google contacts as a vcard file. It was one file with all the mini vcards JAMMED together. Literally. Its hilarious.

I found a great script that I had Claude rewrite that split your vcard file into multiple vcards. You can find it [here](https://github.com/harperreed/vcard-tools/blob/main/vcf-splitter.py). It works super well.

I now have one dir in my `~/.contacts` directory that has 100% of my contacts. I am almost in a good spot!

I then exported my *other* contacts from google, split them, and then put them in the **other** directory.

My favorite part was checking the contacts into git. One of the problems I was trying to solve, was to understand what is changing in my contacts. Now I have version control!

I was basically ready for the next step!

## Mo complexity. Mo problems.

Now that I had my contacts as individual vcards, I had suddenly introduced a bunch of new problems:

 - How do I dedupe my contacts?
 - How do I sort my contacts into priority groups?
 - How do I get the contacts to my phone?
 - How do I sync to multiple address books?
 - How do I get beef rendang in Chicago?
 - How do I stop climate change?
 - Is cardio really the answer?

Whew. This is a lot. Let’s start at the top

### How do I dedupe my contacts

Enter my newish friend [Claude](https://claude.ai)!

I said to Claude: “I have a directory of vcards. I want to dedupe them.” And Claude spit out a python script that was not very good, but was a very good start.

Claude and I negotiated a bit around what I was attempting to do, and finally Claude spit out a script that was decent.

It worked! The final script ends up using some light ML, and does a good job of not destroying all your vcards. It even backs up merged cards!

You can find the dedupe script [here](https://github.com/harperreed/vcard-tools/blob/main/vcf-dupe-checker-ml.py)

### How do I sort my contacts into priority groups?

This is a hilarious problem, and once again Claude is here to save us. I explained the issue to Claude - and Claude whipped up a good solution.

We built hot or not for your contacts. You just run this script and it will help you curate your contacts.

I am using openai, serper and some silliness to try and figure out if the contact is relevant to me. It then allows me to keep, move, or skip. This way I can quickly jump through a bunch of contacts and sort them into **primary** or **secondary**.


{{< image src="/images/posts/vcard-curation.jpg" caption="Chad made the cut!" >}}

It works pretty well, but is kind of slow. I find I will do a few contacts at a time. It is nice.

### How do I get the contacts to my phone?

This was not too hard. But, it introduces the real keystone. I can’t believe I am this far into this post without talking about the real meat of the solution.

#### Vdirsyncer!

Vdirsyncer is an amazing utility that basically does what it says on the tin. It syncs vdirs.

You do a lot of dancing to configure it, and then once it is configured you run `vdirsyncer` and it syncs your directory to another place.

It works natively with carddav (apple, fruit, etc) a few other providers (mainly google using their various contact apis). Vdirsyncer is in the middle of a much needed rewrite/migration to rust - but is working.

I am using it to sync my *main* contacts directory to my main google contacts addressbook.

My google contacts addressbook is my phones address book of record.

This works OK. I tried a handful of carddav providers (apple, fruux) and google was the most reliable strangely. It also had the benefit of having a rational and easy to use interface available on the web.

###  How do I sync to multiple address books?

Vdirsyncer is very good at this. However, the providers are all stupid. And by providers I mean google.

I don’t know who made google contacts api, or why but they have made one of the dumbest decisions I have seen in awhile.

The vcard spec is pretty flexible, annoyingly so. You can kind of do anything you want. And many providers do. This is also why it is awesome.

One of the ways to add sanity is to add a UID to the vcard.

Here is a sample vcard:

```shell
BEGIN:VCARD
VERSION:4.0
FN:Milo Minderbinder
N:Minderbinder;Milo;;;
BDAY:--0203
GENDER:M
EMAIL;TYPE=work:milo@minderbinder.com
END:VCARD
```

This is fine. But what happens if there are two people with the same name, etc. It can get complicated.

One way that `khard` handles this is to assume that every vcard has a UID. This is much better, and makes a lot o sense.

```shell
BEGIN:VCARD
VERSION:4.0
UID:a9ef2d17-7dbf-40c3-83e0-7c60165062a5
FN:Milo Minderbinder
N:Minderbinder;Milo;;;
BDAY:--0203
GENDER:M
EMAIL;TYPE=work:milo@minderbinder.com
END:VCARD
```

Adding a UID is magical and allows for a lot of good things to happen.

Enter google - the destroyer of all that is good.

Google changes the UID whenever you have a write operation. This means that when you sync a contact from your directory to google, google will overwrite your artisanal UID with their AI OVERLORD created UID.

The ramification here is that the next sync you have is 100% changes. You can never have a clean sync if Google is in the equation.

This is [thoroughly](https://gist.github.com/evert/b1cef035890701973fd9) [thoroughly](https://stackoverflow.com/questions/14232604/google-carddav-changes-vcard-uid) [documented](https://evertpot.com/google-carddav-issues/). Google’s carddav is stupid. Lol.

You can build a sync infinity mirror by using vdirsyncer to sync two google contact addressbooks. They will happily change UIDs forever.

So frustrating.

This means that you can’t use the magic of vdirsyncer if you want to sync multiple google accounts. For this, I am still using contacts plus. I use vdirsyncer to sync to my main google account. And then contacts plus pushes those changes to my work, and other address books.

We have:

{{< image src="/images/posts/vcard-reality.svg" caption="Not ideal, but works" >}}

Instead of:

{{< image src="/images/posts/vcard-dream.svg" caption="Why can't we have nice things? " >}}

#### Annoying. Google is bad. Never go full google.



### **A quick aside.**
>
> While debugging this I had to reset my address books dozens of times. It is never an easy task.
>
> **How to delete Google contacts**
>
> Google makes it easy to select all and then “delete.” But if you select more than 3000 contacts the web app will choke.
>
> You could use an address book interface (osx, etc). I had fleeting success with that.
>
> What did work was reloading google contacts, and then selecting 1000-2000 at a time, and then deleting. Rinse repeat until you have no more.
>
> BUT WAIT. That doesn’t actually delete the contacts. It just puts them in the trash. You have to manually go to the trash and then click “delete all contacts.”
>
> This kicks off a job that will take forever, but will eventually delete all contacts.
>
> **How to delete apple contacts**
>
> It is a similar problem. I had fleeting success with the native addressbook. Mostly it didn’t work.
>
> What did work was selecting contacts from each letter via the iCloud web interface, and deleting the contacts there.
>
> Later you will have `vdirsyncer` working and can use it to delete all your contacts. But even that barely worked.
>
> There were multiple days where both google and apple was mad at me and was returning bad data. My iCloud web interface is still broken. Lol. But the native address book works fine.

### OK. So now what.

It works!

I have my contacts in a datastore that I control, that lets me make and see granular changes. I can sync to my phone, different address books, and receive changes from these address books. All via the CLI.

My immediate next step is to automate this via a GitHub action or something of the sort.

I have a lot of [helper scripts](https://github.com/harperreed/vcard-tools/) that will help clean up my contacts. I have a good Claude project that is thoroughly vcard centric.

I can manage my contacts easy and without a lot of pain. My goal of having autonomy with my contacts is complete!

One nice side effect is that i can use tools like sunshine, clay, or contacts+ and see exactly what they are doing to my contacts. I can also declutter my contacts without deleting contacts. It is great!

Thanks for reading. [Email me](mailto:harper@modest.com) and we can chat vcards!
