---
title: "Rant: Cisco ACI Complexity"
date: 2021-03-01 07:05:00
tags: [ SDN, data center ]
---
A while ago [Antti Leimio](https://twitter.com/AnttiLeimio) wrote a long twitter thread describing his frustrations with Cisco ACI object model. I asked him for permission to repost the whole thread as those things tend to get lost, and he graciously allowed me to do it, so here we go.

---

I took a 5 days Cisco DCACI course. This is all new to me. I'm confused. Who is ACI for? Capabilities and completeness of features is fantastic but how to manage this complex system?
<!--more-->
Everything is based on objects. I thought Junos is policy heavy but this is ultimate. There's no proper tools to create and manage all these objects and policies. Manually through GUI it seems impossible even at small scale. So you'd need external automation tools and inventory. 

Object names can't be changed after creation. Do things right for the first time or do it several times by trial and error. Logical structure and consistency is hard. 

APIC GUI is overwhelming. Config hierarchy is very deep and hard to navigate. You can't list or find all objects at once but you have to pick every one in different config hierarchy. 
 
Leaf access interface configuration blocks for example. Interface policy has 20 drop down menus to define used policies. Simple access port configuration takes about 10 different policy definitions and glueing them together.

L3 interfaces are also complex to manage. Like OSPF configuration which is distributed to multiple config hierarchies.

Every GUI config page has tens of config options. You have to check what is it and do I need to set it. Very complex and time consuming to operate. Most options are best to just ignore in the first round. 

That's just basic connectivity at switchport level. Along the vlan pools, physical domains, attachable entity profiles, bridgedomains, VRFs, L3outs you need contracts between endpoints to let traffic flow. You can skip this and allow all traffic but then you lose lot of ACI. 

Verification and troubleshooting is still relying on CLI. GUI has lot of visibility but finding simple things like what is configured and what is the protocol status is frustrating via GUI. Lower level network verification ends up to logging device CLI and running show commands. 

I hate NX-OS syntax. It's combination of Linux and IOS but worse combination than each one alone. Even industry standard "sh" command is not working without writing it completely. Argh... 
 
Overall ACI was impressive with its comprehensive features and capabilities. But operations using GUI are frustrating and almost impossible to handle. You need huge amount of config structure and feature understanding and planning. Hard to see it going right first time. 

That's why you want to use external single source of truth where you can create and manipulate objects and push new configuration to APIC. 

Also you may want to standardize and simplify your connectivity and services before putting it all in ACI. Which is only a good thing. 
