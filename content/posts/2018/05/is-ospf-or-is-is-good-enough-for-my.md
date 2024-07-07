---
date: 2018-05-15 11:45:00+02:00
dcbgp_tag: newrp
series:
- dcbgp
tags:
- design
- data center
- IP routing
title: Is OSPF or IS-IS Good Enough for My Data Center?
url: /2018/05/is-ospf-or-is-is-good-enough-for-my/
---
Our good friend mr. Anonymous has too many buzzwords and opinions in his repertoire, at least based on this comment he left on my [Using 4-byte AS Numbers with EVPN](/2018/05/using-4-byte-bgp-as-numbers-with-evpn/) blog post:

> But IGPs don\'t scale well (as you might have heard) except for RIFT and Openfabric. The others are trying to do ECMP based on BGP.

Should you be worried about OSPF or IS-IS scalability when building your data center fabric? Short answer: most probably not. Before diving into a lengthy explanation let\'s give our dear friend some homework.
<!--more-->
![](/2018/05/s1600-Bart+-+My+Network+Is+Not+FANG.gif)

**TL&DR summary**: OSPF or IS-IS is most probably good enough for your data center... and if it isn't, I sincerely hope you have an architecture/design team in place and don't design your data center fabrics based on free information floating around the 'net.

### What Are the Real Limits of IGPs?

Now that our Anonymous friend is (hopefully) busy, let's try to put the *IGPs don't scale well* claim in perspective:

-   There are service providers having several thousand routers in a single IS-IS area. IS-IS traditionally scaled a bit better than OSPF because it was exposed to more abuse, but it shouldn't be hard to push OSPF (should you prefer it) to several hundred devices in a single area. I've heard of networks having 300+ routers in an OSPF area in times when CPUs were an order of magnitude slower than they are today;
-   We tried to scope the problem with [Dr. Tony Przygienda](https://www.linkedin.com/in/dr-tony-przygienda-018501) during our [Data Center Routing with RIFT](/2018/03/data-center-routing-with-rift-on/) discussion, and while he pointed out that the real challenge OSPF and IS-IS are facing in leaf-and-spine fabric is not topology database size but the amount of redundant flooding, he put a comfortable limit of what OSPF or IS-IS could handle today at \~100 switches.

RIFT and OpenFabric were designed to perform better in larger environments where you might hit the scaling limitations of traditional OSPF and IS-IS flooding, but we don't know whether that's true yet -- as of mid-May 2018, you could get RIFT as experimental code running on Junos, and OpenFabric was still in very early stages the last time I chatted with Russ White

### What Can We Build with 100 Switches?

Let's assume for a moment that we'd like to stick with an IGP and are therefore limited to \~100 switches in a single data center fabric. Is that good enough?

Assuming you're building your leaf-and-spine fabric with most common switch models, you'd have:

-   48-port switches (10/25GE) with four uplinks (40/100GE) at the leaf layer;
-   32-port higher-speed (40GE or 100GE) switches at the spine layer.

The largest fabric you can build with these devices without going into breakout cables or superspines is a 32-leaf fabric with a total of 1536 ports.

If you use larger spine switches with 64 ports like Arista's 7260CX3-64 or Cisco's 9364C, you could get to 3072 ports with 68 switches (64 leaves, 4 spines).

### Quick Detour into Even Larger Fabrics

Finally, if you need an even larger fabric, you could use modular switches at the spine layer, or build a superspine layer (we covered both options in [Physical Fabric Design](https://my.ipspace.net/bin/list?id=Clos#PHY_TOPOLOGY) section of [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar).

A superspine architecture with 176 switches (using 32-port switches at the spine layer) gives you 6144 ports, so it might be cheaper to go with breakout cables in a leaf-and-spine fabric (144 switches). Both of them are at the high end of what you might consider comfortable, but still somewhat within reasonable bounds for a single-area IGP.

The detailed designs are left as an exercise for the reader. You'll find all the information you need to make them work in [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.

### Back to Reality

The largest data center fabric we could build without investing anything into understanding how things really work has around 70 switches and around 3000 edge-facing ports, and there's no reason to feel limited by IGP scalability at this size.

Assuming you want redundant server connectivity that's 1500 bare-metal servers. Assuming you didn't buy them in a junkyard sale, you could easily put 30-50 reasonably-sized VMs on each one of them, for a total of around 50.000 (application) servers.

Is that good enough? It definitely is for [most enterprises](/2017/11/bgp-as-better-igp-when-and-where/) as well as for [smaller cloud providers](/2014/07/how-big-will-your-cloud-be/)... and if your data center network is larger than that, please don't listen to whatever is being said (overly generalized) on the Internet -- you need a proper design done by someone who understands *why* he's doing what he's doing. Buzzwords and opinions won't cut it.

### Why Is Everyone So Focused on BGP Then?

Dinesh Dutt outlined a few technical reasons why you might consider replacing OSPF or IS-IS with BGP in his part of the [Layer-3 Fabrics](https://my.ipspace.net/bin/list?id=Clos#L3_SINGLE) section of leaf-and-spine fabrics webinar (you need at least [free ipSpace.net subscription](http://www.ipspace.net/Subscription/Free) to watch those videos).

Here are a few more cynical ones:

-   We're telling you BGP is good for you because Petr (and [RFC 7938](https://tools.ietf.org/html/rfc7938)) said so. I've seen vendor SEs doing exactly that;
-   I always wanted to play with BGP and now I have an excuse to do so;
-   I want my network to be as cool as Microsoft's (that's where Petr started using BGP as better IGP);
-   I need to pad my resume.

While you might decide to replace OSPF or IS-IS with BGP for any one of these reasons, IGP scalability limitations are most probably not on the very top of the list of potential challenges you might be facing in your data center fabric design.

### Master Data Center Fabric Designs

-   Want to learn the basics of data center fabrics and figure out what individual vendors are doing? Check out the [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) webinar.
-   Want to learn how to design leaf-and-spine fabrics? Go for [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.
-   Looking for a guided and mentored tour with plenty of peer- and instructor support? You probably need [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
-   Want to know more about EVPN technology? Watch the [EVPN Technical Deep Dive](http://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar.
