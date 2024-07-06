---
date: 2019-01-17 08:52:00+01:00
tags:
- automation
title: Five Stages of Automation Grief
url: /2019/01/five-stages-of-automation-grief.html
---
As I'm doing occasional consulting for large enterprises redesigning their data centers, I encounter a wide range of network automation readiness, from *"we don't need that"* to *"how could we automate as much as possible"*.

Based on the pervasiveness of "*we don't need that"* responses it looks like many enterprise network engineers still have to go through the five stages of automation grief.
<!--more-->
**Denial**. I don't need automation. Our network doesn't change that much, and it's perfectly OK to configure devices by hand. We've always been doing it this way, and it was fine.

**Anger**. Why is everyone talking about this new stuff? Why should I learn something new after studying networking for a decade?

**Bargaining**. Maybe I don't need automation. Maybe I can buy an [intent-based](/2018/06/what-is-intent-based-networking.html) or software-defined product from my $vendor and [continue using GUI](/2018/05/layers-of-single-pane-of-glass.html)... or maybe I could do [a bit of Google-and-paste and get something done](/2018/03/dunning-kruger-in-it-infrastructure.html).

Needless to say, $vendors love engineers being stuck in this phase... and [well-meaning evangelists explaining how easy it is to automate stuff](/2023/01/network-automation-expert-beginners.html) (without ever telling you about the hard parts like [source-of-truth or data models](https://my.ipspace.net/bin/list?id=NetAutSol&module=3)) inadvertently help creating either [Expert Beginners](https://daedtech.com/how-developers-stop-learning-rise-of-the-expert-beginner/) that stay stuck at this phase forever (while thinking they really nailed it) or [death by a thousand scripts](https://aldrinisaac.blogspot.com/2018/12/death-by-thousand-scripts.html).

**Depression**. It's so complex. I have to learn all this new stuff. [I hate YAML](https://www.reddit.com/r/ProgrammerHumor/comments/9fhvyl/writing_yaml/). Jinja2 is really a pile of crap. Network devices suck... [even SSH doesn't work reliably](/2017/04/lets-drop-some-random-commands-shall-we.html). Why couldn't my $vendor give me a clean API returning the data I need (hint: [because you chose the wrong vendor](/2016/10/network-automation-rfp-requirements.html) ;).

**Acceptance**. Damn it, I'm an engineer. I can make it work. I'll work hard, master new stuff, and get it done. After all, if I managed to get to the point where I can design and deploy complex networks, I might be able to team with a programmer (or an automation expert) and slowly build something useful.

Hundreds of networking engineers found out that they could get great results once they get to the acceptance phase by following a structured program instead of trying to figure things out on their own. [Here are a few success stories](https://my.ipspace.net/bin/list?id=NetAutUC) from those that enrolled in [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.