---
date: 2018-06-04 08:35:00+02:00
dcbgp_tag: newrp
series:
- dcbgp
tags:
- design
- fabric
- BGP
- IP routing
title: Is EBGP Really Better than OSPF in Leaf-and-Spine Fabrics?
url: /2018/06/is-ebgp-really-better-than-ospf-in-leaf.html
---
Using EBGP instead of an IGP (OSPF or IS-IS) in leaf-and-spine data center fabrics is becoming a best practice (read: thing to do when you have no clue what you're doing).

The usual argument defending this design choice is "*BGP scales better than OSPF or IS-IS*". That's usually true (see also: Internet), and so far, EBGP is the only reasonable choice in very large leaf-and-spine fabrics... but does it really scale better than a link-state IGP in smaller fabrics?
<!--more-->
There are operators running single-level IS-IS networks with thousands of devices, and yet most everyone claims you [cannot use OSPF or IS-IS in a leaf-and-spine fabric with more than a few hundred nodes](https://blog.ipspace.net/2018/05/is-ospf-or-is-is-good-enough-for-my.html) due to [inordinate amount of flooding traffic caused by the fabric topology](http://blog.ipspace.net/2018/03/data-center-routing-with-rift-on.html).

This is the moment when a skeptic should say "*are you sure BGP works any better?*" and the answer is (not surprisingly) "*not exactly*", at least if you get your design wrong.

### EBGP or IBGP?

Most everyone understanding how BGP really works agrees that it makes more sense to use EBGP between leaf and spine switches than trying to get IBGP to work without underlying IGP, so we'll ignore IBGP as a viable design option for the rest of this blog post.

{{<note info>}}You can run IBGP without IGP, and we had to make it work a long while ago because customers, but it's somewhat counter-intuitive and requires additional configuration tweaks.{{</note>}}

### Let's Make It Simple...

Not knowing any better, let's assume a simplistic design where every switch has a different AS number:

{{<note>}}If your first thought was "*didn't you tell us we shouldn't do it this way in the* [*Leaf-and-Spine Fabric Architectures*](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) *webinar,*" you're absolutely right. There's a reason why this is a bad idea. Keep reading...{{</note>}}

Now imagine a leaf switch advertising a prefix:

-   It advertises the prefix to all spine switches;
-   Spine switches advertise the prefix to all other leaf switches;
-   Properly-configured leaf switches use all equal-cost BGP prefixes for traffic forwarding, but still select one of the as the best BGP path (that's how BGP works when you don't configure *add-path* functionality);

{{<note warn>}}It's worth mentioning that by default some common BGP implementations don't do ECMP across EBGP paths, and don't accept paths coming from different autonomous systems as equal-cost paths. You need two nerd knobs to get it working.{{</note>}}

-   Leaf switches advertise their best BGP path **to all spine switches** apart from the one that advertised the best path to them. Some BGP implementations might actually advertise the best path to the router they got the best path from.
-   Every single spine switch installs all the alternate BGP paths received from all leaf switches in BGP table... just in case it might be needed.

{{<figure src="/2018/06/s600-Paper.EVPN+diagrams.3.png" caption="Data center fabric with different AS numbers on spine switches">}}

To recap: on most spine switches you'll see N entries for every single prefix in the BGP table (where N is the number of leaf switches) -- one from the leaf switch with the prefix, and one from every other leaf switch that didn't select the path through the current spine switch as the best BGP path.

{{<note>}}Figuring out what happens when a leaf switch revokes one of its prefixes and how many unnecessary BGP updates are sent is left as an exercise for the reader.{{</note>}}

Compare that to how OSPF flooding works and you'll see that there's not much difference between the two. In fact, BGP probably uses even more resources in this setup than OSPF because it has to run BGP path selection algorithm whenever BGP table changes, whereas OSPF separates flooding and path computation processes.

### Fixing the Mess We Made...

Obviously, we need to do something to reduce the unnecessary flooding. There's not much one could do in OSPF or IS-IS (don't get me started on IS-IS mesh groups), which is the real reason why you can't use them in larger fabrics, and why smart engineers work on RIFT and OpenFabric.

What about BGP? There are two simple ways to filter the unnecessary announcements:

-   Configure outbound update filtering on leaf switches (or inbound update filtering on spine switches) to discard paths that traverse more than one leaf switch;
-   Use the same AS number on all spine switches and let BGP's default AS-path-based filtering do its job.

{{<figure src="/2018/06/s600-Paper.EVPN+diagrams.4.png" caption="Data center fabric with spine switches as a single AS">}}

Now you know why smart network architects use the same AS number on all spine switches and why [RFC 7938 recommends it](https://tools.ietf.org/html/rfc7938#section-5.2).

### The Dirty Details...

The effectiveness of default AS-path-based filtering depends on the BGP implementation:

-   Some implementations (example: Cisco IOS) send BGP updates to all EBGP neighbors regardless of whether the neighbor AS is already in the AS path. The neighbor has to process the update and drop it;
-   Other implementations (example: Junos) filter BGP updates on the sender side and don't send BGP updates that would be dropped by the receiver (as always, there's a nerd knob to twiddle if you want those updates sent).

Finally, it's interesting to note that using IBGP without IGP, with spine switches being BGP route reflectors tweaking BGP next hops in outbound updates, results in exactly the same behavior -- another exercise for the reader if you happen to be so inclined.

### Want to know more?

-   Start with [Using BGP in Data Center Leaf-and-Spine Fabrics](http://www.ipspace.net/Data_Center_BGP) document;
-   Watch [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar;
-   [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
