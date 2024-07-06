---
title: "Data Center Fabric Designs: Size Matters"
date: 2024-03-14 08:55:00+0100
tags: [ fabric, design ]
---
The "_should we use the same vendor for fabric spines and leaves?_" discussion triggered the expected counterexamples. Here's one:

> I actually have worked with a few orgs that mix vendors at both spine and leaf layer. Can’t take names but they run fairly large streaming services. To me it seems like a play to avoid vendor lock-in, drive price points down and be in front of supply chain issues. 

As always, one has to keep two things in mind:
<!--more-->
* Size matters. Straight out of RFC 3439:

> In particular, the largest networks exhibit, both in theory and in practice, architecture, design, and engineering non-linearities which are not exhibited at smaller scale.

* Complexity matters, and large networks try to avoid it as much as possible because they have plenty of other problems. For example, a large streaming service probably does not run EVPN route reflectors on their spine switches.

If one would try to group data center fabrics based on their size, one might get these categories:

* Hyperscalers. They're doing whatever it is they're doing. Some of them are silent (AWS), and others boast how smart they are (Google), even though whatever they're doing is irrelevant to almost everyone.
* Large IP fabrics (including content providers and non-VMware public clouds). They're running some subset of OSPF/IS-IS/IBGP/EBGP. Of course, you can use that on any mix of vendor boxes; that's how we run the global Internet. 
* Enterprise data centers. Most don't need more than [two switches](https://www.ipspace.net/Optimize_Data_Center_Infrastructure/) per site. Few organizations need more than a single leaf-and-spine fabric with four ([or six or eight](/2023/03/leaf-switches-four-uplinks.html)) spines.

Building a single enterprise data center fabric with switches from multiple vendors is thus primarily an exercise in futility – the operational costs of dealing with multiple operating systems, vendor support centers, and tooling quirks probably outweigh the acquisition savings.

As always, there are exceptions:

* You have no control over your purchasing department; their bonus depends on how far they squeeze the vendors. It's time to polish your resume.
* Your workforce is so underpaid that it's cheaper to deal with perpetual multi-vendor quirks than buying potentially more expensive boxes.
* You must import the boxes and pay them with hard-to-get "hard currency." Unfortunately, I was there decades ago, and it makes you incredibly "creative."
* You're boosting your resume.

However, please keep in mind that most people searching for information on the public Internet belong to the "two switches" or "small fabric" crowds. As Jeff [wrote](/2024/03/multivendor-evpn-revisited.html#2123) in a comment to my [Rant: Multi-Vendor EVPN Fabrics](/2024/03/multivendor-evpn-revisited.html) blog post:

> Average company is blessed beyond their wildest dreams to find an engineer who understands what a BPDU is and that bridging loops are bad. L2oL3, MP-BGP AFIs, ESIs, VTEPs....not supportable by 99% of the wild. All just pushing the needle on sales. 4k VLAN limit isn't a valid argument in the 99% either.

Please don't confuse them with totally irrelevant edge cases and outliers.