---
cdate: 2022-07-06
comment: 'Some people never learn and vigorously chase every new hype, be it OpenFlow
  or IPv6 – the evangelists of both technologies promised way more than the technologies
  were ever capable of delivering.


  Not surprisingly, most of the overhyped technologies fail. It took IPv6 decades
  to get real-life adoption, and ([according to Gartner](https://blogs.gartner.com/andrew-lerner/2021/10/11/networking-hype-cycle-2021/))
  OpenFlow/SDN died before ever reaching mainstream deployments.

  '
date: 2011-05-10 06:45:00+02:00
sdn_hype_tag: initial
series:
- sdn_hype
tags:
- SDN
- OpenFlow
title: OpenFlow Is Like IPv6
url: /2011/05/openflow-is-like-ipv6/
---
Frequent eruptions of OpenFlow-related hype (example: [Being Open about Virtualization and Cloud Interoperability](https://web.archive.org/web/20120505055833/http://community.brocade.com/community/brocadeblogs/wingspan/blog/2011/05/03/being-open-about-virtualization-and-cloud-interoperability) published after Brocade Technology Day Summit) call for a continuous myth-busting efforts. Let’s start with a [widely-quoted](http://bit.ly/iQW55Y) (and immediately glossed-over) fact from [Professor Scott Shenker](http://www.eecs.berkeley.edu/Faculty/Homepages/shenker.html), a founding board member of the [Open Networking Foundation](http://www.opennetworkingfoundation.org/): “\[OpenFlow\] doesn't let you do anything you couldn't do on a network before.”

To understand his statement, remember that OpenFlow is nothing more than a standardized version of communication protocol between [control and data plane](/2013/08/management-control-and-data-planes-in/). It does not define a radically new architecture, it does not solve distributed or virtualized networking challenges and it does not create new APIs that the applications could use. The only thing it provides is the [exchange of TCAM (flow) data between a controller and one or more switches](/2011/04/what-is-openflow/).

Cold fusion-like claims are nothing new in the IT industry. More than a decade ago another group of people tried to persuade us that changing the network layer address length from 32 bits to 128 bits and writing it in hex instead of decimal solves [global routing and multihoming and improves QoS, security and mobility](/2010/02/ipv6-myths/). After the reality distortion field collapsed, we were left with the [same set of problems](/2009/05/lack-of-ipv6-multihoming-elephant-in/) [exacerbated](/2011/02/ipv6-provider-independent-addresses/) by the [purist approach](/2010/12/small-site-multihoming-in-ipv6-mission/) of the original IPv6 architects.

Learn from the past bubble bursts. Whenever someone makes an extraordinary claim about OpenFlow, remember the “it can’t do anything you couldn’t do before” fact and ask yourself:

-   Did we have a similar functionality in the past? If not, why not? Was there no need or were the vendors too lazy to implement it (don't forget they usually follow the money)?
-   Did it work? If not, why not?
-   If it did - do we really need a new technology to replace a working solution?
-   Did it get used? If not, why not? What were the roadblocks? Why would OpenFlow remove them?

Repeat this exercise regularly and you’ll probably discover the new emperor’s clothes aren’t nearly as shiny as some people would make you believe.

### More to Explore

Want to hear the real-life [SDN](https://www.ipspace.net/SDN), [OpenFlow](https://ipspace.net/OpenFlow) or [IPv6](https://www.ipspace.net/IPv6) story? Check out the [ipSpace.net webinars](https://www.ipspace.net/Webinar_roadmaps) available with [standard subscription](https://www.ipspace.net/Subscription).

### Revision History

2022-07-06
: Replaced a link to a Brocade blog post with an archived copy