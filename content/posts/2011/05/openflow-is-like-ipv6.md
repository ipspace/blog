---
url: /2011/05/openflow-is-like-ipv6.html
title: "OpenFlow is like IPv6"
date: "2011-05-10T06:45:00.000+02:00"
tags: [ SDN,OpenFlow ]
---

<p>Frequent eruptions of OpenFlow-related hype (a <a href="http://community.brocade.com/community/brocadeblogs/wingspan/blog/2011/05/03/being-open-about-virtualization-and-cloud-interoperability">recent one</a> caused by <a href="http://newsroom.brocade.com/easyir/customrel.do?easyirid=74A6E71C169DEDA9&amp;version=live&amp;prid=750964&amp;releasejsp=custom_184">Brocade Technology Day Summit</a>; I’m positive Interop will not lag behind) call for a continuous myth-busting efforts. Let’s start with a <a href="http://bit.ly/iQW55Y">widely-quoted</a> (and immediately glossed-over) fact from <a href="http://www.eecs.berkeley.edu/Faculty/Homepages/shenker.html">Professor Scott Shenker</a>, a <a href="http://www.networkworld.com/news/2011/041411-open-flow.html">founding board member</a> of the <a href="http://www.opennetworkingfoundation.org/">ONF</a>: “[OpenFlow] doesn't let you do anything you couldn't do on a network before.”<!--more--></p>
<p>To understand his statement, remember that OpenFlow is nothing more than a standardized version of communication protocol between <a href="http://wiki.nil.com/Control_and_Data_plane">control and data plane</a>. It does not define a radically new architecture, it does not solve distributed or virtualized networking challenges and it does not create new APIs that the applications could use. The only thing it provides is the <a href="https://blog.ipspace.net/2011/04/what-is-openflow.html">exchange of TCAM (flow) data between a controller and one or more switches</a>.</p>
<p>Cold fusion-like claims are nothing new in the IT industry. More than a decade ago another group of people tried to persuade us that changing the network layer address length from 32 bits to 128 bits and writing it in hex instead of decimal solves <a href="https://blog.ipspace.net/2010/02/ipv6-myths.html">global routing and multihoming and improves QoS, security and mobility</a>. After the reality distortion field collapsed, we were left with the <a href="https://blog.ipspace.net/2009/05/lack-of-ipv6-multihoming-elephant-in.html">same set of problems</a> <a href="https://blog.ipspace.net/2011/02/ipv6-provider-independent-addresses.html">exacerbated</a> by the <a href="https://blog.ipspace.net/2010/12/small-site-multihoming-in-ipv6-mission.html">purist approach</a> of the original IPv6 architects.</p>
<p>Learn from the past bubble bursts. Whenever someone makes an extraordinary claim about OpenFlow, remember the “it can’t do anything you couldn’t do before” fact and ask yourself:</p>
<ul class="ListParagraph"><li>Did we have a similar functionality in the past? If not, why not? Was there no need or were the vendors too lazy to implement it (don't forget they usually follow the money)?</li>
<li>Did it work? If not, why not?</li>
<li>If it did - do we really need a new technology to replace a working solution?</li>
<li>Did it get used? If not, why not? What were the roadblocks? Why would OpenFlow remove them?</li>
</ul>
<p>Repeat this exercise regularly and you’ll probably discover the new emperor’s clothes aren’t nearly as shiny as some people would make you believe.</p>

