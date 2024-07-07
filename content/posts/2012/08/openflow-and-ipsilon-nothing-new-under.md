---
cdate: 2022-07-18
comment: 'OpenFlow did not introduce any new (or revolutionary) ideas. FORCeS has
  been around for a while (with almost zero traction), and concepts similar to reactive
  flow setup were floated in 1990’s and failed miserably. For more details, read [Flow-Based
  Packet Forwarding](/2022/03/flow-based-forwarding/).


  Not surprisingly, the flow-based forwarding ideas floundered (yet again) in the
  decade since I wrote this blog post. There are few hardware implementations, and
  even virtual switches [experienced severe performance penalty](/2014/02/flow-based-forwarding-doesnt-work-well/)
  when trying to use so-called microflows.

  '
date: 2012-08-13 06:31:00+02:00
openflow_101_tag: ugly
series:
- openflow_101
series_weight: 170
tags:
- MPLS
- SDN
- OpenFlow
title: 'OpenFlow and Ipsilon: Nothing New Under the Sun'
url: /2012/08/openflow-and-ipsilon-nothing-new-under/
---
I'd promised to record another MPLS-related podcast and wanted to refresh my failing memory and revisit the beginnings of Tag Switching (Cisco's proprietary technology that was used as the basis for MPLS). Several companies were [trying to solve the IP+ATM integration problem in mid-nineties](/2011/01/campfire-true-story-of-mpls/), most of them using IP-based architectures (Cisco, IBM, 3Com), while Ipsilon tried its luck with a flow-based solutions.
<!--more-->
I found a [great overview of IP+ATM solutions in an article](http://www.cs.washington.edu/education/courses/csep561/97sp/paper1/paper11.txt) published on the University of Washington web site. This is what the article has to say about Ipsilon's approach (and if you really want to know the details, read [GSMP (RFC 1987)](http://tools.ietf.org/html/rfc1987) and [Ipsilon Flow Management Protocol (RFC 1953)](http://tools.ietf.org/html/rfc1953)):

> An IP switch controller routes like an ordinary router, forwarding packets on a default VC. However, it also performs flow classification for traffic optimization.

Replace *IP switch controller* with OpenFlow controller and *default VC* with switch-to-controller OpenFlow session.

> Once a flow is identified, the IP switch sets up a cut-through connection by first establishing a VC for subsequent flow traffic, and then by asking the upstream node to use this VC.

Likewise, some people propose [downloading 5-tuples or 12-tuples in all the switches along the flow path](/2012/08/openstackquantum-sdn-based-virtual/). The only difference is that 15 years ago engineers understood virtual circuit labels use fewer resources than 5-to-12-tuple policy-based routing.

As expected, Ipsilon's approach had a few scaling issues. From the same article:

> The bulk of the criticism, however, relates to Ipsilon\'s use of virtual circuits. Flows are associated with application-to-application conversations and each flow gets its very own VC. Large environments like the Internet with millions of individual flows would exhaust VC tables.

Not surprisingly, a number of people ([myself included](http://highscalability.com/blog/2012/6/4/openflowsdn-is-not-a-silver-bullet-for-network-scalability.html)) that still remember a bit of the networking history are making the exact same argument about [usage of microflows in OpenFlow environments](/2011/10/openflow-and-state-explosion/), but it seems [RFC 1925](http://tools.ietf.org/html/rfc1925) (section 2.11) will yet again carry the day.
