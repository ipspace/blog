---
kb_section: PMTUD
minimal_sidebar: true
title: Summary
url: /kb/Internet/PMTUD/50-summary.html
---
After decades years of struggles, the IP fragmentation remains one of the persistent challenges in IP networks, particularly if you have to implement extra layers in the protocol stack (like MPLS or PPP over Ethernet) without changing the layer-2 MTU size, or if you use tunneling or IP encryption techniques. The generic solution to the IP fragmentation issues should be the *Path MTU Discovery* that was issued as an RFC in November 1990 and remained a draft standard ever since. However, misconfigured firewalls still prevent us from using this solution reliably.

Fortunately, TCP implementations don't have to rely exclusively on Path MTU Discovery - [RFC 4821](https://tools.ietf.org/html/rfc4821) describes an alternate probe-based mechanism.

If you cannot get PMTUD to work reliably in your network, you can at least fix the TCP sessions by setting the TCP Maximum Segment Size on the intermediate routers with the **ip tcp adjust-mss** interface configuration command. Broken UDP-over-IPv4 applications that pretend to use the PMTUD but ignore its results can be fixed with policy-based routing that clears the DF bit in UDP packets. There's no equivalent hack for UDP-over-IPv6.

The worst impact of IP fragmentation is in the router-to-router communication (GRE tunnels or IPSec encryption). If a router-to-router IP packet is fragmented somewhere in the path, the receiving router has to reassemble the original packet, resulting in significantly reduced switching performance. In these cases, it’s best to enable the router’s support for PMTUD with the **tunnel path-mtu-discovery** interface configuration command (assuming the end hosts support PMTUD as well). Worst case, you can still lower the tunnel MTU size as well as TCP MSS value, resulting in slightly higher switching overhead but ensuring that the GRE or IPSec packets will not be fragmented.

## More to explore:

**Related webinars:**

- [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)

**Related blog posts:**

- [The relationship between interface MTU, IP MTU and MPLS MTU](http://blog.ipspace.net/2007/10/tale-of-three-mtus.html)
- [All MTUs Are not the Same](https://blog.ipspace.net/2011/07/all-mtus-are-not-same.html)
- [TCP MSS Clamping Explained](https://blog.ipspace.net/2013/01/tcp-mss-clamping-what-is-it-and-why-do.html)
- [MTU issues (and TCP MSS clamping) in residential IPv6 deployments](https://blog.ipspace.net/2013/01/mtu-issues-and-tcp-mss-clamping-in.html)
- [The MPLS MTU challenges](https://blog.ipspace.net/2011/07/mpls-mtu-challenges.html)
- [Asymmetric MPLS MTU Problem](https://blog.ipspace.net/2011/07/asymmetric-mpls-mtu-problem.html)
- [The impact of MTU mismatch on OSPF](http://blog.ipspace.net/2007/10/ospf-neighbors-stuck-in-exstart.html)
- [EIGRP MTU metric](https://blog.ipspace.net/2010/06/eigrp-mtu-metric.html)

**Useful tools:**

- [tracepath](https://linux.die.net/man/8/tracepath) on Linux
- [mturoute utility](https://elifulkerson.com/projects/mturoute.php) on Windows. See also [related blog post](https://blog.ipspace.net/2007/09/mturoute-utility-that-measures-hop-by.html)

**Related RFCs:**

- [TCP Problems with Path MTU Discovery](https://tools.ietf.org/html/rfc2923), RFC 2923
- [Path MTU Discovery](https://tools.ietf.org/html/rfc1191), RFC 1191
- [IPv6 Path MTU Discovery](https://tools.ietf.org/html/rfc8201), RFC 8201

**Other articles:**

- [IP Fragmentation in Detail](https://packetpushers.net/ip-fragmentation-in-detail/)
- [Path MTU Discovery in Practice](https://blog.cloudflare.com/path-mtu-discovery-in-practice/), Cloudflare, February 2015
- [Why Can't I Browse the Internet when Using a GRE Tunnel?](http://www.cisco.com/warp/public/105/56.html)
- [Resolve IP Fragmentation, MTU, MSS, and PMTUD Issues with GRE and IPSEC](http://www.cisco.com/en/US/tech/tk827/tk369/technologies_white_paper09186a00800d6979.shtml)
