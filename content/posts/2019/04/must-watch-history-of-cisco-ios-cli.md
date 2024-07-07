---
cli_tag: finally
date: 2019-04-26 08:43:00+02:00
series:
- cli
tags:
- automation
- configuration
title: 'Must Watch: History of Cisco IOS CLI'
series_title: 'History of Cisco IOS CLI'
url: /2019/04/must-watch-history-of-cisco-ios-cli/
---
My first Cisco router was a blade for a Cabletron modular hub (anyone remembers what hubs were or a company named Cabletron?). We plugged it in, I read the documentation, figured out I had to type **conf t** and was faced with a blinking cursor staring back at me from an empty line.

A few years later I was invited to beta test Cisco software release 9.21 (it wasn't called IOS yet). The best feature it had was the awesome configuration CLI with context-sensitive prompts and on-demand help.
<!--more-->
Fast-forward a few more years. For one reason or another, I met [Terry Slattery](https://www.ipspace.net/Author:Terry_Slattery) (second CCIE worldwide) and during one of our [always-enlightening chats](/2015/02/we-need-to-move-from-assembling-car/) he told me he was [the guy behind the new Cisco CLI](https://www.netcraftsmen.com/the-history-of-the-cisco-cli/), permanently making him a demigod in my eyes.

It took another two decades or so before I got the whole story, this time listening to a [Network Collective podcast with Terry](https://web.archive.org/web/20191207095631/https://thenetworkcollective.com/2019/03/hon-cisco-cli/).

You SHOULD listen to the whole podcast (if you manage to find it in Internet Archive), I just wanted to share the hilarious pre-9.21 CLI history:

-   They got it right in the first iteration: router configuration should be in a file that the router would read, parse, and execute.
-   Routers had kilobytes of memory at that time. Adding something like vi or emacs into router code was unimaginable, so they expected the routers to read the file from a TFTP server.
-   Best laid plans fail when they meet reality. This time, they had to demonstrate the routers on a trade show, and for whatever stupid reason they couldn't get a TFTP server in place.
-   A brief hacking session later, Cisco software got **configure terminal** that would allow you to enter configuration commands into an in-memory buffer (with no editing, syntax checking, or anything else). When you'd indicate you're done the router would pretend the text came from a TFTP server.
-   Few releases later someone figured out it would be a great idea if they would parse the lines entered from the terminal connection on-the-fly... opening the Pandora box of *let's mess up the ACL that controls my access to the box one line at a time*.
-   Needless to say, it took them another decade to implement **reload in 5**.

Now you know how we got to the horrible mess we have to deal with on a daily basis. While Cisco tried to rewrite Cisco IOS numerous times, they never really got it done, so we still have to deal with concepts from 1980s that were only slightly improved with Terry's miraculous code from early 1990s.

### Need a Rant?

I ranted about the stupidities of having to use an interface designed for human consumption in automation scripts in the *[Network Automation Roadblocks](https://my.ipspace.net/bin/list?id=NetAut101)* part of *[Network Automation 101](https://www.ipspace.net/Network_Automation_101)* webinar.
