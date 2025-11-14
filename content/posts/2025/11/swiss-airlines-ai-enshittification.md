---
title: "AI Enshittification: Swiss Airlines Edition"
date: 2025-11-17 08:00:00+0100
tags: [ AI ]
ai_tag: rant
---
Remember the [vendor consultants](https://blog.ipspace.net/2020/09/disaster-recovery-vendor-marketing/) who persuasively told you how to use their gear to build a disaster recovery solution with stretched VLANs, even though the only disaster recovery they ever experienced was the frantic attempt to restart their PowerPoint slide deck? Fortunately, I was only involved in the aftermath of their activity when the laws of physics reasserted themselves, and I [helped the poor victims](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha/) rearchitect their network into a somewhat saner state.

There's another batch of ~~snake-oil salesmen~~ consultants peddling their warez to the gullible incompetent managers: the AI preachers promising reduction in support costs. Like the other group of consultants, they have never worked in support and have never implemented a working AI solution in their lives, but that never bothered them or their audience.

Unfortunately, this time I had the unfortunate "privilege" of having the painful front-row seat.
<!--more-->
### Before You Start Telling Me I'm a Luddite

I'm pretty sure a judicious application of AI technologies could solve many of the stupid problems we encounter every day and streamline support operations. I also believe that:

1. A better solution would be not to create those problems in the first place.
3. Instead of trying to save on paperclips, you might consider giving customers a working support channel (even if you have to charge for it).
3. The support people should be empowered to get the job done.

Finally, if you decide to *replace* your support channel with AI (and I'm not saying that's a wrong idea to have), you'd better:

4. Make damn sure it works[^BPLT].
5. Update your online information to reflect the new reality. Having web pages point to 800-numbers that don't work is worse than nothing.

[^BPLT]: Otherwise, you just created a huge dumpster fire that will eventually stink to the heavens and result in blog posts like this one. Hint to the readers: it will hurt more if you make it go viral.

### Back to the Campfire Story

I was at the other end of Europe, and a cold front with high winds and rainstorms was rolling in, so I decided to return home a day earlier. I had a ticket with free rebooking, and it was always easy to change my flight in the past: I would go to the airline website, find an alternate flight, confirm it, pay the inevitable difference[^FRB], and be on my merry way.

[^FRB]: We all know "free rebooking" is a myth. They always find ways to claim the fare or taxes have changed.

This time, the website politely told me that I could not rebook online and would have to contact the airline's support center.

{{<long-quote>}}
I wouldn't be writing this blog post if the airline's software department (or whatever consulting firm they outsourced this to) spent a bit more time dealing with the potential rebooking scenarios.
{{</long-quote>}}

Unfortunately (for me), someone within Swiss Airlines bought the "reduce support costs with AI" fairy tale. The *only* way to rebook a flight (according to their website) is through an online chat, and that online chat is AI-powered... and that's where the nightmare started.

{{<long-quote>}}
At this point, it's worth mentioning that I paid a premium for a ticket with free rebooking, and probably wouldn't mind a small support center processing fee. Alas, that doesn't matter to the true believers in AI efficiencies.
{{</long-quote>}}

I explained to the AI thingy what I needed, and it correctly identified that I'd need to chat with a support rep (wow, what a discovery), patched me into the chat support queue, and went on its merry way.

{{<long-quote>}}
Collecting the prerequisite information (booking ID), verifying the customer identity (name/phone number), and figuring out what they want to achieve is a perfect use for a lightweight AI-based system... as long as it works. The one I encountered did not.
{{</long-quote>}}

The "only" problem: the whole chat thingy collapsed and disconnected me from the operator (more than once) before we could even start working on my challenge. After several retries, all I could get from the AI was "sorry, we're experiencing technical turbulences".

A few more failed retries resulted in this tweet:

{{<figure src="/2025/11/swiss-rant.png">}}

I was pleasantly surprised to see the Swiss social media team (one of the really good guys in this story) react to my rant and offer their help. In the meantime, the chat system recovered to the point where I was finally connected to someone frantically dealing with multiple customers (apart from "frantically", that's the warning I got from the chat system). At that moment, I thought I dodged the bullet:

* We found the flight I was looking for
* He rebooked me and told me what the fare difference was
* I told him to use my credit card for the fare difference
* He acknowledged that and told me he'd pass the information to the ticketing team, who would send me an updated ticket.

{{<long-quote>}}
Do I have to mention that people aren't naturally good at multitasking, and that errors inevitably occur when you force someone to context-switch between multiple parallel conversations? That's obvious to anyone with a shred of common sense, but it doesn't align well with the glitzy *reduced human resources costs* in the AI consultant slide decks.
{{</long-quote>}}

### Stuck in Limbo

Little did I know that I stumbled upon at least four broken processes:

1. I used PayPal to buy my ticket, so Swiss Airlines did not have my credit card information on file. They could have warned me that using PayPal to pay for a rebookable ticket is not the best idea, but it seems that collecting money in any way possible is more important.
2. The person rebooking me obviously did not know that Swiss had no credit card information on file. Letting a support person fly blind is sometimes not a good idea.
3. I was therefore left in a state of a rebooked flight with no valid ticket, but apart from confusing information (some pages would show the old departure date, some the new one), I had no indication that there was a problem
4. My flight was in limbo for a few days, but nobody felt the need to contact me and tell me I had a problem.

{{<long-quote>}}
When I was still running my own business, I had a cron job that would scan the outstanding items, like upcoming webinars, and send me a warning if they were in an unexpected state. Obviously, such a convoluted solution never occurred to whoever is writing airline software.
{{</long-quote>}}

### What, No Boarding Pass?

But wait, there's more. The check-in time came around, and the boarding pass didn't arrive (no surprise there). The online checking process was completely useless; it either complained that it couldn't find my ticket or reported that *an error has occurred* (extremely helpful). The only support mechanism available: AI-powered online chat.

This time, the "AI" turned out to be a multiple-choice decision tree[^TIP] (someone had replaced voice prompts and a phone keypad with a web form) that told me not to worry and that I could resolve the problem at the airport.

[^TIP]: So maybe my previous encounter with Swiss Airlines AI was a failed attempt to *test in production*.

I was well beyond trusting an AI recommendation, so I took advantage of the very generous offer from the @FlySWISS social media team. The lady on the other end tried her best to help me; she even called me to obtain my credit card number, and would have solved my problem if we had gotten that part right (we failed).

I absolutely admire her dedication and wouldn't want to be in her shoes -- our simple "conversation" took over two hours with extensive delays as she must have been handling dozens of similar complaints, doing her best to restore the tarnished image of her company because someone got drunk on AI Kool Aid.

### Call Center to the Rescue

The next morning, I decided to dig out a Swiss Airlines call center number and call them no matter what. But wait, that's not as easy as it looks. They're hiding that number better than snakes hide their feet. I finally found a contact page specific to the country I was in, and it listed a broken 800 number (thanks a million, exactly what I needed at that point) and a Switzerland-based support number (do I have to mention how cheap it is to call from the EU to Switzerland?).

The Switzerland support number turned out to be *web support* (what else might one need when dealing with a flight ticket stuck in limbo?), but the person answering the call quickly identified what I needed and gave me the (secret?) reservation center number. I was almost there...

The next five-minute phone call was what I would have needed three days earlier: the operator found my booking, told me what the fare difference was, took my credit card number, processed it (I heard the comforting *ping* on my phone), and told me he'd send me an email confirmation (I got it) and pass the information to the ticketing department that would (finally!!!) send me a new ticket.

That last bit never happened. While I was able to check in and get my boarding pass, I still don't have the updated ticket.

### Adding Insult to Injury

Like the three-day saga wouldn't be bad enough, a check-in crew from hell was waiting for me at the airport[^NSP]. There was an elderly gentleman handling like 80% of the passengers while the rest of the crew kept wasting oxygen and blowing hot air. I even saw an agent leaving her desk *with a customer standing in front of her* to go flirt with an airline captain and disappear for good, leaving the stranded customer in front of an empty counter.

Fortunately, I got processed by the said elderly gentleman. He very efficiently handled my luggage and produced the boarding pass in no time, and the never-ending saga was finally over.

[^NSP]: If I remember the airline colors correctly, they wore Lufthansa uniforms, so not a Swiss problem.

### The Enshittification Results

To recap:

* Due to the inability of Swiss Airlines' online services to process a simple rebooking request, I needed a 5-minute phone call with an operator to rebook my flight, take credit card information, and generate a new ticket.
* Instead of being able to make that phone call, I was fighting with a broken online chat system. I interacted with three people (two of whom were clearly multitasking and overloaded) without ever reaching the expected end-state (a new ticket), and wasted hours trying to complete a simple task.

Another clear win for the AI consultants.