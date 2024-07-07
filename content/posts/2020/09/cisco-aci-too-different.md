---
title: "Is Cisco ACI Too Different?"
date: 2020-09-14 06:34:00
tags: [ ACI, design ]
---
A friend of mine involved in multiple Cisco ACI installations sent me this comment on their tenant connectivity model:

> I'm a bit allergic to ACI. The abstraction is mis-aligned with familiar configurations, in particular contracts being independent of and over-riding routing, tenants, etc. You can really make a mess with that, and I've seen some! One needs to impose some structure, naming conventions..., and most people don't seem to get that done.

As I noticed in the [NSX-or-ACI webinar](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN), it's interesting how NSX decided to stay with the familiar VLAN/routing/filtering paradigm ([more details](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)), whereas the designers of Cisco ACI decided to go down a totally different path.
<!--more-->
{{<note>}}Even public cloud providers decided to stay close to the familiar forwarding/routing concepts, even though they had to bend the laws a bit ([AWS](/2020/05/aws-networking-101/), [Azure](/2020/05/azure-networking-101/)) to make things scale better.{{</note>}}

There's nothing wrong with being different, and Cisco ACI connectivity model might be an ideal abstraction, and just what's needed if you've never seen IP networking before... but it's hard to change the mindset of everyone who ever heard about TCP/IP, or support the [gazillion of broken enterprise applications](/2013/09/sooner-or-later-someone-will-pay-for/) that rely on dirty [VLAN-based tricks](/2017/11/lets-pretend-we-run-distributed-storage/) like [shared MAC](/2009/08/turn-switch-into-hub-microsoft-way/)- or IP addresses. Not surprisingly, many Cisco ACI installations turn into glorified (and overly complex) VLAN managers.

But of course it gets worse... enterprise environments expect GUI-based configuration, and while that encourages the continued creation of bespoke snowflake environments, it has another drawback:

> Documentation would help. But people think the GUI *is* the documentation.

Sometimes it gets as ridiculous as a networking engineer [writing an automation script to collect Cisco ACI tenant configurations](/2018/06/automation-win-document-cisco-aci/) to help identify configuration parameter creep in supposedly-identical tenant deployments.

Is there a way out of this morass? [Infrastructure-as-code and automation obviously help](/2019/02/operating-cisco-aci-right-way/), and you can find several [Cisco ACI deployment automation examples](/2019/03/automating-cisco-aci-environment-with/) in our [Network Automation Solutions showcase](https://www.ipspace.net/NetAutSol/Solutions)... but it turns out that the moment you start automating your deployments, you might not need Cisco ACI anymore. Back to my friend:

> I just did a manual 2-spine/10-leaf VXLAN deployment with multi-site connectivity, and clearly automation is the better way to go, primarily for accuracy of configs. Customer likes Ansible for automation, and now that the fabric is built, adding VLANs is pretty easy templating.

But even if you decide to go down this path, you'll quickly face another challenge: should you build your own solution (aka "invest in premium people"), in which case you might find our [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions) useful, or buy a premium product from an [umbrella orchestration vendor](/2015/01/lock-in-is-inevitable-get-used-to-it/) and [spend the rest of your life fine-tuning it](/2018/05/why-is-network-automation-so-hard/) to meet your ["unique" needs](/2013/04/this-is-what-makes-networking-so-complex/). As always, once you start looking into the details, [there is no easy answer](https://www.goodreads.com/quotes/8639959-for-every-complex-problem-there-is-an-answer-that-is).