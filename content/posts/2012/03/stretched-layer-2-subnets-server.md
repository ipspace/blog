---
date: 2012-03-27 15:05:00+02:00
dr_tag: stretch
high-availability_tag: dr
series:
- dr
tags:
- data center
- workshop
- fabric
- virtualization
- high availability
title: Stretched Layer-2 Subnets – The Server Engineer Perspective
url: /2012/03/stretched-layer-2-subnets-server.html
---
A long while ago I got a very interesting e-mail from [Dmitriy Samovskiy](http://www.somic.org/), the author of [VPN-Cubed](http://www.cohesiveft.com/vpncubed), in which he politely asked me why the networking engineers find the stretched layer-2 subnets so important. As we might get lucky and spot a few unicorns merrily dancing over stretched layer-2 rainbows while attending the [Networking Tech Field Day](http://techfieldday.com/2012/nfd3/), I decided share the e-mail contents with you (obviously after getting an OK from Dmitriy).
<!--more-->
> I was wondering if you could spare a couple of minutes to explain something to me. You see, when I was designing VPN-Cubed, I specifically targeted an L3 interconnect. It is my understanding this is how it\'s been done forever. Be it a case of connecting to a vendor, partner or big customer - didn\'t people by default use IPsec forever for this? I worked at an \[bigco\] where we had a link to \[big supplier\]. It was used occasionally so didn\'t make sense to waste money on a dedicated circuit. So we did a VPN - regular IPsec, layer 3. Everyone was happy.

That's exactly what most networking engineers are trying to do every time they have an opportunity to get asked about sensible design options before the project is less than a week away from its completion deadline. However, quite often the need for stretched layer-2 segments comes to us in form of a "mandatory requirement" from apps/server teams.

::: separator
![](http://www.ancientlight.info/products/images_robes/unicorn_rainbow_fabric.jpg){width="500"}\
[Unicorn and rainbow fabric](http://www.ancientlight.info/products/robes-children.html) - an ideal material to use in your stretched fabric designs
:::

Interestingly, Dmitriy (being a server/application engineer and a programmer) thinks along exactly the same lines as I do:

> My thinking was that fooling hosts to think that they are on the same eth segment or VLAN when they are milliseconds of latency (+ jitter) apart was pointless - apps written to rely on the fact that hosts are on the same eth segment for speed won\'t work anyway; apps written without such assumptions usually operate on top of IP, not L2.

Exactly. SNA circuit between two IBM mainframes might be an exception.

> VPN-Cubed does L3 only, doesn\'t touch or attempt to virtualize L2 at all - but then I see folks focusing on L2 and I don\'t get it. What\'s the point of focusing on an L2 segment spread over WAN (in general case) - what kind of an app needs that sort of setup?

Apart from [stretched clusters](/2011/06/stretched-clusters-almost-as-good-as.html) and [other mythical beasts](/2011/11/busting-layer-2-data-center.html) I have yet to find an application where stretched L2 segment would add value beyond being a design-failure-avoidance kludge.

> Is it Ethernet broadcasts for DHCP? Is it the fact that when geo-distributed hosts are under the same administrative domain (my hosts in dc and my hosts in cloud, vs my hosts in dc and my partner\'s hosts in the cloud) that\'s driving this?

The only sensible explanation I got so far is the [inability to change IP addresses while moving cold virtual machines](/2012/01/ip-renumbering-in-disaster-avoidance.html) from one data center to another (example: disaster recovery). While we might be able to solve that problem with routing protocols (and that's how [it's been done forever](http://www-03.ibm.com/support/techdocs/atsmastr.nsf/WebIndex/PRS1708) \... but those skills got lost in the mists of times), it's easier to request a stretched layer-2 segment and push the problem into another team's lap.

> Also I am wondering why geo-distributed L2 segments are so important to network engineers, which is a conclusion I made from your posts.

The only reason they're important to us is that we get asked to implement them, even though we know they will eventually fail \... [badly](/2011/12/large-scale-l2-dci-true-story.html).
