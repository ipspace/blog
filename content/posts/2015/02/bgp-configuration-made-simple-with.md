---
date: 2015-02-23 09:02:00+01:00
tags:
- SDN
- BGP
- Cumulus Linux
title: BGP Configuration Made Simple with Cumulus Linux
url: /2015/02/bgp-configuration-made-simple-with/
dcbgp_tag: cl
series:
- dcbgp
---
BGP is without doubt the most scalable routing protocol, which made it a popular choice for large-scale deployments from service provider networks to [enterprise WAN/VPN](/2014/03/scaling-bgp-based-dmvpn-networks/) networks and even [data centers](/2013/10/exception-routing-with-bgp-sdn-done/). Its only significant drawback is the tedious configuration process (which almost reminds me of writing COBOL programs decades ago).
<!--more-->
The Cumulus Networks routing team decided to change that and added numerous BGP configuration enhancements to Quagga (now FRR), the routing daemon used by Cumulus Linux. You might want to watch the [Data Center Architectures](https://vimeo.com/119403106) video from [Cumulus' Network Field Day 9 presentation](http://techfieldday.com/appearance/cumulus-networks-presents-at-networking-field-day-9/) for the introduction to the topic before delving into the details.

### Configure BGP neighbor on an interface

Here's how you'd usually configure a BGP neighbor:

``` {.code}
router bgp <as-number>
  neighbor <address> remote-as <as-number>
```

This is how you can do it with Quagga in Cumulus Linux:

``` {.code}
router bgp <as-number>
  neighbor <interface> remote-as <as-number>
```

{{<note info>}}Do I have to mention how easy it is to create a template configuration for a ToR switch running BGP on four uplinks? Now try doing that with traditional BGP configuration.{{</note>}}

After configuring an interface neighbor, the router tries to figure out the neighbor's IP address. That's easy to do for IPv6 (use link-local addresses), and for interfaces with /30 or /31 IPv4 subnets... but Cumulus Linux allows you to run BGP (IBGP or EBGP) over [unnumbered interfaces](/2014/06/unnumbered-ospf-interfaces-in-quagga/).

{{<note info>}}You still need a numbered interface on every box -- preferably a loopback interface -- to access the box and to give the box an IPv\[46\] address to use in ICMP replies and other switch-generated traffic (syslog, SNMP...).{{</note>}}

It was always possible to run IBGP over unnumbered interfaces: configure an IGP, run IBGP between loopback interfaces, and let IGP sort out how to exchange traffic between the BGP speakers. But how do you get EBGP to run over unnumbered interfaces without using IGP?

Cumulus routing team used one of the more obscure BGP-related RFCs to get the job done. [RFC 5549](https://tools.ietf.org/html/rfc5549) documents how you exchange IPv4 BGP prefixes with IPv6 next hops (for more details see the [RIPE presentation by AMS-IX](https://ripe65.ripe.net/presentations/101-RIPE65.pdf)), and when you combine that with the ability to run EBGP across link-local IPv6 addresses, you get a one-line BGP neighbor configuration that is totally independent from the IPv4/IPv6 addressing in your network and thus easy to turn into a template and automate.

Final question: how do you get the LLA of your neighbor? Easy: listen to its ND or RA messages.

**Notes and caveats:**

-   You can use the interface-based BGP neighbors with devices from other vendors if you use /30 or /31 subnet mask on the interface (in that case Cumulus Linux uses standard BGP);
-   You don't have to run IPv6 in your network to get this feature to work on unnumbered interfaces -- just make sure you haven't disabled IPv6 on the interfaces you want to use in BGP configuration;
-   You can use this feature for IPv6 BGP sessions with any third-party box that supports BGP over LLA (Cisco's IPv6/security guru Eric Vyncke [published an RFC describing this idea](https://tools.ietf.org/html/rfc7404)... but unfortunately that had no impact on messy configuration you have to use in Cisco IOS to get it to work);
-   If you want to use interface-based BGP neighbors over unnumbered IPv4 interfaces, the BGP neighbor has to support RFC 5549, and I'm not aware of any major vendor doing that;
-   Obviously this feature works only over point-to-point interface. You'd need something like [dynamic BGP neighbors from Cisco IOS](/2014/03/scaling-bgp-based-dmvpn-networks/) for multi-access (example: mGRE) scenarios.

### Getting rid of AS numbers

The other major pain of BGP configuration syntax (particularly when you're trying to generate standard configuration templates) is the requirement to specify neighbor AS number in the **neighbor** statement. Here's how Cumulus routing team solved that problem:

``` {.code}
router bgp <as-number>
  neighbor <interface> remote-as internal
  neighbor <interface> remote-as external
```

The **remote-as internal** part of the **neighbor** statement is obvious -- use my own BGP AS number. One has to wonder why nobody else is using this syntax; maybe they're too busy copying industry-standard CLI.

The **remote-as external** feature is where Cumulus engineers got slightly creative. BGP speakers advertise their AS number in the BGP OPEN message, and the usual behavior is to close the session if the AS number in the incoming OPEN message doesn't match the number configured on the BGP **neighbor** statement. Instead of that, the new code they wrote for Quagga ignores the strict AS check, accepts the AS number advertised by the neighbor, and uses it later on in the same way as if it would have been configured in the router configuration.

{{<note warn>}}
Do I have to tell you not to use this feature with untrusted neighbors? It's OK to trust an adjacent switch in your data center (or use [Prescriptive Topology Manager](http://docs.cumulusnetworks.com/display/CL25/Prescriptive+Topology+Manager+-+PTM) if you want to be sure your data center is wired correctly), but definitely *NOT* OK to trust your customers or peering partners. See [RFC 7454](/2015/02/rfc-7454-bgp-operations-and-security/) for more details on what not to do with BGP.
{{</note>}}

### Summary

Regardless of what I think about the whole concept of whitebox switching, I love creative solutions;) It's refreshing to see how startups with no legacy codebase to protect solve annoyances that have been bothering us for decades. Great job!

**Disclosure**: Cumulus Networks was indirectly covering some of the costs of my attendance at the Network Field Day 9 event. [More...](/p/networking-tech-field-day-disclaimer/)
