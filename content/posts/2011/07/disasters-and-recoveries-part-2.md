---
date: 2011-07-20 06:56:00.002000+02:00
dr_tag: life
high-availability_tag: dr
series:
- dr
tags:
- high availability
title: "Disaster Recovery: Lessons Learned"
url: /2011/07/disasters-and-recoveries-part-2.html
---
After the [bumpy start of our holidays](https://blog.ipspace.net/2011/07/disasters-happen-its-recovery-that.html), we thoroughly enjoyed the crystal-clear waters, hot sunny weather and the hospitality of inhabitants of [Croatian island Brač](http://en.wikipedia.org/wiki/Bra%C4%8D) \... until my daughter came to me quietly asking "hey, I don't want to raise panic, but my friend saw a weird cloud \... would you mind checking if it's a forest fire" A short walk to a vantage point confirmed the initial observation -- we were facing what turned out to be the worst forest fire in more than a decade. Obviously I was bound to receive another hefty dose of disaster recovery lessons.
<!--more-->
**Lesson#1 -- Watch for early signs**. According to the informal chats I had with the locals, it seems that the fire was reported after someone had seen the cloud from several miles away. By then, the fire has been well under way. Likewise, CRC errors or RAM leaks might get ignored until they result in a catastrophe. Monitoring the health of your network, establishing a baseline behavior and watching the deviations and trends are crucial if you want to fix minor problems before they escalate in major disasters.

**Lesson#2 -- Fast reaction is critical**. We've been observing the huge smoke cloud for around half an hour before we've heard the sirens and spotted the [first airplane](http://en.wikipedia.org/wiki/Air_Tractor_AT-802). This was probably the only mistake the firefighters made; by the time they reacted, the strong wind has blown the fire way out of control. Drawing a parallel with your network -- a significant deviation from the baseline (for example, fast increase in the number of CRC errors) requires an immediate response. Usually the problems don't disappear on their own.

Fortunately we were able to pull out of the house we were living in (the flames came to within a quarter mile of it) and moved further west to a hotel that was well away from the hot spots. The fire continued during the night (the [airplanes](http://en.wikipedia.org/wiki/Canadair_CL-415) need good visual conditions, so they became useless) and the local firefighters were quickly overwhelmed. In the meantime, crews from all over Dalmatia were ferried to the island to help them.

**Lesson#3 -- Know when to ask for help**. Many networking engineers like the I-can-fix-it macho approach to troubleshooting. Sometimes it works, sometimes you become overwhelmed, but it's important to realize early on when you might need help and ask for it. You could alert someone and ask him to be on standby, you could ask for a second set of eyes or you could actually pull in more people to help you work on the problem.

**Lesson#4 -- Take a break**. Some of the firefighting crews brought to the island were used to relieve the exhausted early responders. You should do the same; you can't work on a problem for hours without getting totally exhausted, sloppy and eventually useless. Ask for help, let them take over, take a break and relax -- you might actually find a creative solution while relaxing or talking the problem over with someone else.

When we woke up the next day we were surrounded by a wasteland. More than 10% of the island burned down, but they managed to save all the houses and nobody was seriously hurt. Obviously the firefighters knew exactly what they were doing.

**Lesson#5 -- Plan**. Asking "what shall we do now" when the disaster strikes is a bit too late. Plan for all major contingencies. Develop as many automated procedures as feasible (VMware's Site Recovery Manager is one of the tools that can help you).

**Lesson#6 -- Practice**. Croatian firefighters get tens of forest fires each year (most of them caused by human factor like careless tourists or even arsonists) and thus lots of practice. You don't (or at least I'm hoping you don't). Fire drills are thus essential. Whenever you change your disaster recovery process, you have to test it. If you haven't tested it in a few months, you have to test it (because something you're not aware of has changed in the meantime). Netflix went a step further and created a [Chaos Monkey](http://techblog.netflix.com/2010/12/5-lessons-weve-learned-using-aws.html) to introduce [random failures in their server infrastructure](http://www.codinghorror.com/blog/2011/04/working-with-the-chaos-monkey.html). No wonder they survived the Amazon EC2 failure.

**Lesson#7 -- Avoid disasters with rock-solid design**. There are numerous reasons the forest fires so often turn into infernos; one of them is the accumulation of dead wood in untended forests, the other one is the choice of fast-growing (but highly flammable) pine trees over local oaks or hornbeams during reforestation efforts.

In a parallel universe, engineers stretch layer-2 VLANs across data centers because it's easier and faster to implement than proper scale-out application architecture.
