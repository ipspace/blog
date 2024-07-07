---
title: "Worth Exploring: Pluginized Protocols"
date: 2020-11-30 07:47:00
tags: [ BGP, intent-based networking ]
intent-based-networking_tag: related
---
Remember my _[BGP route selection rules are a clear failure of intent-based networking paradigm](/2018/01/bgp-route-selection-failure-of-intent/)_ blog post? I wrote it almost three years ago, so maybe you want to start by rereading it...

Making long story short: every large network is a unique snowflake, and every sufficiently convoluted network architect has unique ideas of how BGP route selection should work, resulting in all sorts of crazy extended BGP communities, dozens if not hundreds of nerd knobs, and 2000+ pages of BGP documentation for a recent network operating system (no, unfortunately I'm not joking).
<!--more-->
What if we'd admit that [intent-based networking looks better in PowerPoint than in real life](/2019/05/how-hard-is-it-to-manage-your-intent/), and give people the tools to influence the BGP route selection process through a callback API that would be invoked at various points during the BGP update processing and route selection process.

Welcome to [Pluginized Protocols](https://pluginized-protocols.org/xbgp/), an academic project exploring the viability of this approach.  Coming from the same team that worked on [Prefix Independent Convergence](/2012/01/prefix-independent-convergence-pic/), [Loop-Free Alternate](/2012/01/loop-free-alternate-ospf-meets-eigrp/), MP-TCP, [Flowbender](https://conferences2.sigcomm.org/co-next/2014/CoNEXT_papers/p149.pdf), [Software-Defined IXP](/2015/10/software-defined-ixp-with-laurent/), [Fibbing with OSPF](/2015/11/fibbing-ospf-based-traffic-engineering/), or [natural-language interface to network operations](/2019/09/net2text-natural-language-interface-to/)... and having been implemented in FRRouting and BIRD, it's definitely worth looking at.