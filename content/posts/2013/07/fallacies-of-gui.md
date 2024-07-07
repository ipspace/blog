---
cdate: 2022-07-09
comment: 'One of the major talking points of the SDN Hype Crusade was the CLI bashing.
  That''s total nonsense (ask anyone who had the privilege to [suffer through a GUI-based
  deployment](/2011/01/vmware-cluster-up-and-running-in-three/)),
  but the myth refuses to die. I wrote more than a dozen follow-up posts [focusing
  on REST API versus CLI](/kb/tag/cli-or-api/).

  '
date: 2013-07-03 07:08:00+02:00
sdn_hype_tag: clueless
series:
- sdn_hype
tags:
- SDN
- network management
title: Fallacies of GUI
url: /2013/07/fallacies-of-gui/
---
I love [Greg Ferro's characterization of CLI](http://etherealmind.com/thoughts-on-choosing-node-js-for-automation/):

> We need to realise that the CLI is a "power tools" for specialist tradespeople and not a "knife and fork" for everyday use.

However, you do know that most devices' GUI offers nothing more than what CLI does, don't you? Where's the catch?
<!--more-->
For whatever reason, people find colorful screens full of clickable items less intimidating than a blinking cursor on black background. Makes sense -- after all, you can see all the options you have; you can try pulling down things to explore possible values, and commit the changes once you think you enabled the right set of options. Does that make a product easier to use? Probably. Will it result in better-performing product? Hardly.

Have you ever tried to configure OSPF through GUI? How about trying to configure usernames and passwords for individual wireless users? In both cases you're left with the same options as you'd have in CLI (because most vendors implement GUI as eye candy in front of the CLI or API). If you know how to configure OSPF or RADIUS server, GUI helps you break the language barrier (example: moving from Cisco IOS to Junos), if you don't know what OSPF is, GUI still won't save the day \... or it might, if you try clicking all the possible options until you get one that seems to work (expect a few meltdowns on the way if you're practicing your clicking skills on a live network).

What the casual network admins need are *GUI wizards* -- a tool that helps you achieve a goal while keeping your involvement to a minimum. For example: "I need IP routing between these three boxes. Go do it!" should translate into "Configure OSPF in area 0 on all transit interfaces." When you see a GUI offering this level of abstraction please let me know. In the meantime, I'm positive that the engineers who have to get a job done quickly [prefer using CLI](/2008/12/im-too-old-i-prefer-cli-over-gui/) over [clickety-click GUI](http://packetpushers.net/wp-content/uploads/2011/06/Clickity-Click-Click.mp3) (and I'm [not the only one](http://www.wired.com/wiredenterprise/2012/07/command-line/)), regardless of whether they have to configure a network device, Linux server, Apache, MySQL, MongoDB or a zillion other products. Why do you think Microsoft invested so heavily in PowerShell?
