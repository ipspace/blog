---
title: "Leaf-and-Spine Fabrics Between Theory and Reality"
date: 2023-03-09 07:01:00
tags: [ fabric, design ]
---
I'm always envious of how easy networking challenges seem when you're solving them in PowerPoint, for example, when an *innovation specialist* explains how scalability works in leaf-and-spine fabrics in a *LinkedIn* comment:

> One of the main benefits of a CLOS folded spine topology is the scale out spine where you can scale out the number of spine nodes increasing your leaf-spine n-way ECMP as well as minimizing the blast radius with the more spine nodes the more redundancy and resiliency.

Isn't that wonderful? If you need more bandwidth, sprinkle the magic spine powder on your fabric, add water, and voila! Problem solved. Also, it looks like adding spine switches reduces the blast radius. Who would have known?
<!--more-->
In reality:

- It doesn't matter whether you have two or sixteen spines -- the blast radius is the same. It is true that you're pretty low on redundancy if you have just two spines and of them exploded, so make that three.
- Adding a spine switch often results in the rewiring of the physical fabric; the only exception would be going from three to four spines when you're using leaf switches with four uplinks. Next step: an exciting configuration exercise unless you've decided to use unnumbered leaf-to-spine links when deploying the fabric. 
- The number of uplink ports on the leaf switches limits the maximum number of spine switches. Most leaf switches have four uplinks (some Cisco switches have six) -- the only realistic options you have are thus two, three, or four spine switches.
- You could build much larger fabrics if you split leaf switch uplinks into individual lanes (100GE ports into four 25GE lanes), but you don't want to know how messy the cabling gets with the octopus cables or complex behind-the-scenes wiring between patch panels.

{{<note info>}}Brad Hedlund [explained that idea](https://my.ipspace.net/bin/list?id=Clos#PHY_TOPOLOGY) in the [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.{{</note>}}

Another dose of reality: most of the above doesn't matter. It's easy to get a spine switch with 32 100GE or 400GE ports; some vendors are shipping spine switches with 64 ports. Sixty-four leaf switches connected to those ports give you over 3000 server-facing ports -- probably good enough for 95% of the data centers out there.

Considering all that, what should we do with generic opinions like the one above? Charity Majors answered this thorny question in a [recent tweet](https://twitter.com/mipsytipsy/status/1628295844251435013)[^LC]:

> I can opine all I want on your architecture or ours, but if I'm not carrying a pager for you, you should probably just smile politely and move along. People with skin in the game are the people you should listen to.

[^LC]: Maybe I should do the same with LinkedIn comments, but sometimes they're just too juicy to pass.

And [also](https://twitter.com/mipsytipsy/status/1628299299867226113):

> The antipattern I see in so many places with devs and architects is the same fucking problem they have with devs and ops. "No time to be on call, too busy writing important software" ~turns into~ "No time to write code, too busy telling other people how to write code."

FWIW, you should read the whole thread (assuming Twitter still works when you're reading this).
