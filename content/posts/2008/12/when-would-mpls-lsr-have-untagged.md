---
date: 2008-12-01 06:40:00.002000+01:00
tags:
- MPLS
title: When Would an MPLS LSR Have Untagged Output Label?
url: /2008/12/when-would-mpls-lsr-have-untagged/
---
This is a nice MPLS question I've received from one of the readers:

> I have understood the Penultimate Hop Popping (PHP) process, but I don't understand when a router would use UNTAGGED instead of POP TAG?

Instead of answering the question directly, let\'s walk through a series of simple Q&A pairs that will help you understand the whole process (remember: [knowledge, not recipes](/2008/09/knowledge-or-recipes/)!).

{{<note>}}It\'s highly recommended you read the first few chapters of the *[MPLS and VPN Architectures](http://www.amazon.com/gp/product/1587050021?ie=UTF8&tag=cisioshinandt-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=1587050021)* book before the rest of this post.
{{</note>}}
<!--more-->
**Where does the _Untagged_ keyword appear?** It only appears as the *output* label in the LFIB (Label Forwarding Information Base) that you can inspect with the **show mpls forwarding-table**.

**What does the _Untagged_ keyword mean?** This keyword means that the router has no output label associated with the *forwarding equivalence class* (FEC \... usually an IP prefix). Since there is no output label, the router cannot perform a label swap (or pop) but has to remove the whole MPLS shim header.

**Where would a router get the output label?** It\'s received from the next-hop router.

**When would a router have no output label?** When there is no next-hop router or when the next-hop router did not advertise a label for the IP prefix.

**When would there be no next-hop router?** If the IP prefix is a directly connected subnet (including a loopback interface) or a summary route advertised by the router itself.

**When would the next-hop router not advertise a label?** The reasons a next-hop router would not advertise a label for an IP prefix include:

-   It\'s not running MPLS.
-   It\'s running MPLS but not CEF (MPLS labels are assigned to IP prefixes in CEF table).
-   It\'s not reachable across an MPLS-enabled interface (both routers could be running MPLS, but the transit interface does not have the **mpls ip** configuration).
-   The LDP session has not been established yet.
-   There is a mismatch in LDP protocol (one router is running Cisco\'s proprietary TDP, the other one standard LDP).
-   The next-hop router uses an access-list to filter the IP prefixes for which the MPLS labels are advertised.

**Summary:** you would see the *Untagged* label in the LFIB when the IP prefix is a directly connected interface, a summary route or the next-hop router has not advertised the label.
