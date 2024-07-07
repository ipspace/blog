---
date: 2015-07-14 14:29:00+02:00
tags:
- design
- data center
- WAN
- high availability
title: Can You Avoid Networking Software Bugs?
url: /2015/07/can-you-avoid-networking-software-bugs/
---
One of my readers sent me an interesting reliability design question. It all started with a catastrophic WAN failure:

> Once a particular volume of encrypted traffic was reached the data center WAN edge router crashed, and then the backup router took over, which also crashed. The traffic then failed over to the second DC, and you can guess what happened then\...

Obviously they're now trying to redesign the network to avoid such failures.
<!--more-->
> All kind of random things are being suggested such as deliberately maintaining different software revisions, having a different vendor in the second DC, etc.

I don't see what one could do to avoid this type of failures apart from using different equipment in parallel, be it equipment from different vendors or different enough boxes from the same vendor.

{{<note info>}}Obviously you can only do that if you do simple IP routing and not something more creative like DMVPN, OTV or VPLS.{{</note>}}

The multi-vendor approach avoids box-specific catastrophes, but brings its own set of complexities and inter-vendor interoperability challenges... unless you split the network in multiple independent availability zones linked with simple IP transport, and use different set of vendors in each availability zone.

However, I'm not sure whether it would make more sense to deal with the ongoing complexity or once-in-a-blue-moon crash (assuming it does happen once in a blue moon).

{{<note>}}I know that the traditional DMZ design guidelines suggested using equipment from different vendors, but I always had a problem with that approach.{{</note>}}

Did you ever have to solve such a challenge? What did you do? What would you suggest? Oh, and keep in mind that [SDN controllers might not be the right answer](/2014/09/controller-cluster-is-single-failure/) (see also [this blog post](/2015/04/on-sdn-controllers-interconnectedness/)).
