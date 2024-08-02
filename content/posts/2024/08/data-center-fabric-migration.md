---
title: "Migrating a Data Center Fabric to VXLAN"
date: 2024-08-06 07:34:00+0200
tags: [ data center, VXLAN, design ]
---
Darko Petrovic made an [excellent remark on one of my LinkedIn posts](https://www.linkedin.com/feed/update/urn:li:activity:7222145210732949504?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7222145210732949504%2C7222261031140524036%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287222261031140524036%2Curn%3Ali%3Aactivity%3A7222145210732949504%29):

> The majority of the networks running now in the Enterprise are on traditional VLANs, and the migration paths are limited. Really limited. How will a business transition from traditional to whatever is next?

The only sane choice I found so far in the data center environment (and I know it has been embraced by many organizations facing that conundrum) is to build a parallel fabric (preferably when the organization is doing a server refresh) and connect the new fabric with the old one with a layer-3 link (in the ideal world) or an MLAG link bundle.
<!--more-->
Trying to migrate an existing fabric to a new technology is usually pointless; old hardware either doesn't support the technology you're interested in or has so many limitations[^VXR] that it's simply not worth the effort[^ROS].

[^VXR]: For example, routing in and out of VXLAN tunnels (RIOT)

[^ROS]: The same rule applies to "_Gee, we have this old server. I'm pretty sure I could run $whatever on it_" I made that mistake more than once and wasted way too much time trying to make new software work on unreliable old hardware.

Not everyone agrees that it makes sense to build a new fabric; you might decide that upgrading the existing data center fabric by layers makes more sense. For example, you could rip out the spine switches (or whatever they were called when you bought them), replace them with new hardware, enable VXLAN on that new hardware, and then gradually replace leaf switches with VXLAN-enabled ones, effectively slowly expanding the VXLAN boundaries. That could work (in theory), but you'd be facing many migration events and a particularly nasty caveat: link speeds. 

If your existing switches are a few years old, they might have 40GE uplinks (or, even worse, 10GE uplinks). Will you buy low-end spine switches to cope with that, or will you purchase modern switches and waste most of their performance to deal with the low-speed links? Also, most businesses' IT needs grow slower than Moore's law or Ethernet speeds, so most fabrics tend to shrink over time. Buying enough spine switches to connect the existing leaf switches is a waste when you know you won't need nearly as many leaf switches in the future.

The same reasoning applies to a hardware migration strategy that starts with the leaf switches: how will you connect the high-speed new leaf switches to the ancient spines?

Finally, Darko mentioned customers who wanted to use shiny new stuff without investing anything into the hardware or migration services ([the whole thread](https://www.linkedin.com/feed/update/urn:li:activity:7222145210732949504?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7222145210732949504%2C7222261031140524036%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287222261031140524036%2Curn%3Ali%3Aactivity%3A7222145210732949504%29) is well worth reading). The only (sane) way to deal with them is to explain that there is no free lunch and walk away if they fail to grasp that message. Sometimes you can't win.


