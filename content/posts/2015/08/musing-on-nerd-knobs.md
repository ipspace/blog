---
cli_tag: fail
date: 2015-08-27 09:58:00+02:00
series:
- cli
series_weight: 500
tags:
- SDN
- configuration
title: Musing on Nerd Knobs
url: /2015/08/musing-on-nerd-knobs/
---
Henk left a [wonderful comment](/2015/08/sdn-will-not-solve-real-life-enterprise/#c5725880629730586323) on my [*SDN will not solve real-life enterprise problems*](/2015/08/sdn-will-not-solve-real-life-enterprise/) blog post. He started with a bit of sarcasm:

> SDN will give more control and flexibility over the network to the customer/user/network-admin. They will be able to program their equipment themselves, they will be able to tweak routing algorithms in the central controller. They get APIs to hook into the heart of the intelligence. They get more config-knobs. It\'s gonna be awesome.

However, he thinks (and I agree) that this [vision](https://today.duke.edu/2015/05/kragie) doesn't make sense:
<!--more-->
> If you truly want to prevent what happened at United, the exact opposite is needed. Less config. Less knobs. Less tweaks. Less \"smart stuff\" invented by individuals or individual customers.

Unfortunately I don't believe we'll ever see a world with fewer tweaks and nerd knobs, and here are at least a few reasons why:

-   **Machoism inherent in networking** -- aka [I Can Get the Job Done no Matter What](/2013/08/temper-your-macgyver-streak/). I can fix whatever problem is caused by broken applications by adding another layer of indirection and duct tape -- be it NAT, PBR, GRE, VXLAN, OTV, LISP, SDN... because if I do that, I'm the hero (actually not -- you just [created massive technical debt](/2013/09/sooner-or-later-someone-will-pay-for/)) whereas if I tell the application people to fix their applications, I'm a *department on NO.*
-   **I know I can stretch this thing** (or maybe it's growing organically). Running a country-wide bridged network? Why not (yeah, one of them crashed badly in mid-90s). Running a 300-router IS-IS area? Sure (it actually works). Running a 5000-router network on OSPF instead of using BGP as the core protocol? Sure, why should we consider the proper tools for the job at hand if we hold a hammer?

{{<note>}}I always suspected we got stub areas in OSPF after an idiot with oversized network decided to dump the whole Internet BGP table into OSPF as external routes. Please tell me I'm wrong.{{</note>}}

-   **Network designs based on whitepapers** instead of understanding of technologies used in the design. I can't tell you how many [broken designs I've seen](/2014/04/why-exactly-would-you-want-nexus-7000/) -- and most of them were broken because [architects creating them didn't understand](/2015/08/the-biggest-problem-of-sdn/) how the underlying technologies really work. The truly sad part is that most of these designs work in PoC labs, and break only when faced with large-scale deployment, when the easiest way to fix them is to yell at your vendor to (A) fix their bugs and (B) give you yet another nerd knob to make your broken thing work.
-   **Unique snowflakes**. Instead of using cookie-cutter designs, we prefer to carefully craft unique snowflakes that magically integrate the legacy stuff that should have been dead years ago with the next-generation technologies... and every unique snowflake needs at least a nerd knob or two to make it work.

{{<note>}}Years ago every new Cisco IOS release included at least ten VoIP features that appeared totally useless to my untrained eyes, but were probably caused by yet another snowflake designer willing to raise a large PO.{{</note>}}

Henk concluded his comment with another perfectly valid observation:

> I bet half the configuration commands in today\'s routers could be removed.

And that will never happen for a simple reason: it would break too many existing networks... and as long as the nerd knobs are available, an overzealous engineer will inevitably use them and create an almost-permanent vendor lock-in.

**Homework:** Don't be like that. Resist the siren song of nerd knobs. Make your designs and configurations as simple as possible. Your network (and people running it) will thank you.

**Taking the next step:** Once you clean up and simplify your configurations, it's easy to automate them. The [Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers) webinar includes a case study that gives you a step-by-step description of the whole process.
