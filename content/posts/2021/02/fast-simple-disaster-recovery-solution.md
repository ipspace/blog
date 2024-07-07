---
date: 2021-02-04 07:11:00+00:00
dr_tag: other
high-availability_tag: dr
series:
- dr
series_title: Fast and Simple Disaster Recovery Solution
tags:
- high availability
- design
title: 'MUST READ: Fast and Simple Disaster Recovery Solution'
---
More than a year ago I was enjoying a cool beer with my friend [Nicola Modena](https://www.ipspace.net/Expert:Nicola_Modena) who started explaining how he solved the "_[you don't need IP address renumbering for disaster recovery](/2019/12/you-dont-need-ip-renumbering-for/)_" conundrum with _production_ and _standby_ VRFs. All it takes to flip the two is a few changes in import/export route targets.

I asked Nicola to write about his design, but he's too busy doing useful stuff. Fortunately he's not the only one using common sense approach to disaster recovery designs (as opposed to [flat earth](/2011/09/large-scale-bridging-nuked-earth/) [vendor marketectures](/2020/09/disaster-recovery-vendor-marketing/)). Adrian Giacometti used a very similar design with one of his customers and [documented it in a blog post](/2020/09/vendor-marketectures-in-real-life/).
<!--more-->
**TL&DR Summary:**

* Layer-3 DCI
* No stretched VLANs
* Simple storage replication between sites
* Recovery site is in ready-to-go hot standby. Storage is ready, networking is ready, all it needs are the virtual machines
* Production and Recovery VRFs use the same IP addressing internally. They are never connected directly.
* He complicated the design a bit with NAT and probing-based DNS. I'm positive it would be possible to get rid of these requirements following Nicola's approach.

He concluded his blog post with three rhetorical questions that I couldn't resist answering:

> Is technology evolving or is just a pile of old stuff rebranded by new developers?

It's just a pile of old stuff (see also RFC 1925 rule 11). Unfortunately most developers don't care about history and thus repeat its mistakes ad nauseam.

> Why haven’t I seen these scenarios before? I know it might sound weird, but it is completely viable as a basic case of study.

Because these scenarios don't fulfill two requirements:

* You can't [fake disaster recovery testing](/2019/09/disaster-recovery-test-faking-another/) with them, because it's impossible to move a single VM to the other site, claim "[mission accomplished](https://en.wikipedia.org/wiki/Mission_Accomplished_speech)", and go home.
* These designs don't make any money for the networking or virtualization vendors -- they work well on any gear that supports VRFs, and are not complex enough to justify selling new gear.

> How far away were we from having an active-active scenario?

Very very far. More in an upcoming blog post.

{{<jump>}}[Keep reading](https://adriangiacometti.net/index.php/2020/12/18/fast-and-basic-drp-solution/){{</jump>}}