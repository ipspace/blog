---
cli_tag: fail
date: 2020-04-27 06:01:00+00:00
series:
- cli
series_weight: 900
tags:
- automation
title: Network Automation and Hammer of Thor
---
Imagine that you just stumbled upon the hammer Thor carelessly dropped, and you’re so proud of your new tool that everything looks like a nail even though it might be a lightbulb or an orange.

That happens to some people when they get the network automation epiphany: all of a sudden CLI and manual configuration should be banned, and everything can be solved by proper incantation of Git and Ansible commands or whatever other workflow you might have set up... even though the particular problem might have nothing to do with what you have just automated.

{{<note info>}}I'm not saying we should keep using box-by-box CLI for daily operations or mundane configuration tasks. I'm just saying that the world is not as binary as some people want it to be.{{</note>}}
<!--more-->
Here's an example: I’ve seen a hilarious "discussion" (if you can call 280-character back-and-forth a discussion) between a seasoned networking architect and an automation evangelist claiming that even if your network is down (you're facing a P1 case in TAC lingo), you can just roll back to previous configuration and be done with it. See mum, no CLI needed.

{{<figure src=/images/patience-you-must-have-my-young-padawan.jpg >}}

The myth of "**fail fast and roll back**" comes from the new-age software world, and even there some people discovered that sometimes it's hard to roll back, so they changed their mantra to "**fix fast and roll forward**"... unless of course your failed rollout clobbered the database, in which case you're toast anyway. Translated into networking terminology: [you might not be able to roll back](/2019/04/recovering-from-network-automation.html) because you either bricked your devices, or can't access them.

Next, **it might not be the configuration**. Sometimes increased load, or weird packets, or increased number of prefixes, or some [weird attribute attached to a BGP update](/2009/02/root-cause-analysis-oversized-as-paths.html) trigger a software- or even a hardware bug that brings down your network. In those cases, rolling back to the previous config is as useful as "_did you reload or power cycle the device_" question we all love to get from clueless first-level support.

### Aside

Some of my favorite weird bugs:

* File transfer triggering remote loopback on a modem;
* ARP request consistently crashing a router;
* Xbox update crashing my Internet modem (nothing more than a bridge between fiber- and copper Ethernet) most of the time;
* Catalyst 7600 dropping into software switching (and losing 95% of its stated performance);
* Catalyst 7600 randomly copying incoming packets into wrong VRF.

### Back to Automation

While you can automate tons of troubleshooting tasks (and you should), the only way to solve unexpected hard problems is still to:

* log into the devices
* explore what's going on
* collect data that you never thought about before (and thus haven't ever collected)
* sit down and think hard
* shut down something or find a workaround.

Guess what, automation won't help you there - you can't automate unknown one-off events. The only thing that might save the day is a decent CLI, and someone who can use it... or you could [bring your network to a local mechanic](/2018/02/how-self-sufficient-do-you-want-to-be.html) (vendor TAC), and drink awful coffee while they're trying to figure out why on Earth you'd have the weird configs you have (hint: because your automation tool made them ;).

In the end, someone will find a solution to your _network down_ situation, and it might involve a device configuration change. Will you file a change request, wait for someone to add that to your automation system, run all integration and pre-deployment tests, and deploy the new configurations... or will you [temporarily disable the automation system](/2018/02/big-red-button-for-network-automation.html) (so it won't overwrite the fix you're about to make) and fix the network? I know what I'd do, but that's just a biased perspective from an old-school network guru sitting in his ivory tower.
