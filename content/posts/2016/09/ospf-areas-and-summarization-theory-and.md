---
date: 2016-09-09 13:59:00+02:00
ospf_tag: areas
tags:
- design
- OSPF
title: 'OSPF Areas and Summarization: Theory and Reality'
url: /2016/09/ospf-areas-and-summarization-theory-and/
---
While most readers, commenters, and Twitterati agreed with my take on the uselessness of OSPF areas and inter-area summarization in the 21st century, a few of them pointed out that [in practice, the theory and practice are not the same](http://c2.com/cgi/wiki?DifferenceBetweenTheoryAndPractice). Unfortunately, most counterexamples failed due to broken implementations or vendor "optimizations."
<!--more-->
### Broken OSPF Implementation

Someone (name and other details withheld for an apparent reason) described the problem they faced in their data center network: while switches from most vendors worked like a charm without route summarization (they had to use OSPF areas due to the network size), a particular vendor's switches needed seconds to recompute the topology and install the new routes in the forwarding table.

They tried using BGP, and the problem disappeared, proving it must have been a broken OSPF implementation.

Potential workarounds:

-   Use BGP;
-   Use stub areas, either with aggressive summarization or as totally stubby areas (no inter-area routes inserted into an area).

{{<note warn>}}The second workaround requires inter-spine links to avoid black holes after leaf-to-spine link failures. The proof is left as an exercise to the reader, or you could cheat and watch the [Leaf-and-Spine Fabric Designs](http://www.ipspace.net/Leaf-and-Spine_Fabric_Designs) webinar (more specifically, the *Route Summarization and Link Aggregation* video in the [*Layer-3 Fabrics with Non-redundant Server Connectivity*](http://content.ipspace.net/get/Clos#Layer-3%20Fabrics%20with%20Non-Redundant%20Server%20Connectivity) section).{{</note>}}

### Vendor Licensing

[Jochen Bartl](https://www.linkedin.com/in/jochenbartl) sent me this message:

> Another sad but valid reason to use summarization could also be due to licensing. There are still vendors out there who put artificial limitations on their data center gear. Nexus 5600, for example, supports only 256 dynamic routes in the [LAN_BASE_SERVICES_PKG license](http://www.cisco.com/c/en/us/td/docs/switches/datacenter/sw/nx-os/licensing/guide/b_Cisco_NX-OS_Licensing_Guide/b_Cisco_NX-OS_Licensing_Guide_chapter_01.html). Ordering and getting budget for a license upgrade can become quite a challenge on its own in some organizations ;-)

Well done, Cisco! Seeing you guys supporting clean and straightforward network designs is so lovely.

### Old Gear

Finally, there's always a dinosaur hiding in a dusty closet. As an [anonymous commenter wrote](/2016/09/do-we-still-need-ospf-areas-and/#c2289999859109206256):

> Got some customers still using very old routers managing critical services with 7+ yrs uptime that can't process a large DB and cannot be touched whatever is the issue/project.

Deal with these as you would with a broken OSPF implementation: isolate them in a stub area and hope they fail soon. It's even better if they're so old you can't replace them anymore.
