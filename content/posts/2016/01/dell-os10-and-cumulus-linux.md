---
date: 2016-01-28 09:55:00+01:00
tags:
- switching
- data center
- Cumulus Linux
title: Dell OS10 and Cumulus Linux
url: /2016/01/dell-os10-and-cumulus-linux.html
---
A few days ago Dell [announced their next-generation network OS based on Debian Linux](https://www.dell.com/learn/us/en/uscorp1/press-releases/2016-01-20-dell-raises-the-bar-for-open-networking), and bloggers (like my good friend [Tom Hollingsworth](http://networkingnerd.net/2016/01/20/the-tortoise-and-the-austin-hare/)) started wondering what's going to happen with Cumulus Linux.

Let's get into prognostication mode...

{{<note>}}On a totally unrelated note, I love the picture Dell marketing put on the [OS10 page](https://web.archive.org/web/20160125141829/http://www.dell.com/us/business/p/open-platform-software/pd). Linux distro in a binder? Really? When was the last time they checked the calendar?{{</note>}}
<!--more-->
### Who cares?

Dell OS10 runs on data center switches. The question should thus be *who cares about another network operating system within the data center?*

Most enterprises [don't need more than two 1RU or 2RU switches in their data center](/2014/10/all-you-need-are-two-top-of-rack.html). Some of them might not want to admit it, but once you do the [consolidation homework](/2015/11/presentation-all-you-need-are-two.html), that's what you're left with.

Some larger enterprises might need a bit more, maybe a small leaf-and-spine fabric. For most of those, a single switch is way above the [acceptable unit of loss](http://kontrolissues.net/2015/03/27/sometimes-size-matters-im-sorry-but-youre-just-not-big-enough/). From that perspective it might make more sense to stick to a traditional vendor, preferably one that has full-blown readily-accessible Linux on the box. Some of these customers will try playing with open networking switches, and some of them will get badly burned, but then some people never want to listen to unwanted advice that contradicts their unfounded beliefs.

The big guys (Google, Facebook, Microsoft, Amazon) buy enough gear to have direct relationship with Broadcom (or someone else) and use their SDK on customized network OS.

Who's left? The huge enterprises and cloud services providers (where every cent counts).

### Why does it matter?

If you decided to go for white- or britebox switches, weren't big enough to get Broadcom's attention, and wanted to have something that resembles a network OS (I've heard enough horror stories about crapware shipping with some of those switches), you had no other option than to put one of the vendor operating systems (Cumulus Linux, Big Switch OpenFlow agent or a few others) on the box because there was no other way to get the mapping between Linux kernel forwarding tables and switching silicon.

Dell OS10 is supposed to remove that obstacle (there's a bit of a path between press release and shipping product), but so does [OpenSwitch](/2016/01/openswitch-deep-dive-on-software-gone.html) from HP and a few other options. Effectively, Dell is shipping their hardware with a Linux device driver -- a no-brainer in server world and a novelty obviously worth talking about in networking.

### Who will take what?

If you think you need a single throat to choke, you'd better stay with a traditional vendor.

If you want to be your own system integrator (or you already are a system integrator selling turnkey solutions to your customers) and want vendor support, go for britebox switches (so you'll get decent hardware support) and put Cumulus Linux (if you believe in traditional networking) or Big Switch OS (if you believe in centralized control plane) on them.

If you're big enough to have a team capable of doing their own stuff, Dell OS10 might make sense to you. On a cynical note, and based on what I've seen in the OpenStack world, I know a lot of service providers who think they're in this category and who'll probably waste a year or two trying to get their homebrewed distro up and running (and throw away way more money than Cumulus license would cost them). For more cynical details, see also [this video](https://www.youtube.com/watch?v=ClKEkCRvWTQ).

### Want even more details?

Why don't you [register for the free *Introduction to SDN webinar*](http://www.ipspace.net/Introduction_to_Software_Defined_Networking_(SDN)), where I'll also talk about software/hardware disaggregation, merchant silicon and whitebox switching?

Also, you (RFC 2119) SHOULD read the [fantastic blog post](http://packetpushers.net/industry-needs-open-source-framework-switching-silicon/) by Carlos Cardenas -- it goes in way more details on why truly open-source Linux device driver is a big deal.
