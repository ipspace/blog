---
title: "BGP Labeled Unicast on Cisco IOS"
date: 2022-03-23 07:50:00
tags: [ BGP, MPLS ]
pre_scroll: True
---
While researching the BGP RFCs for the *[Three Dimensions of BGP Address Family Nerd Knobs](/2022/01/bgp-af-nerd-knobs.html)*, I figured out that the BGP Labeled Unicast (BGP-LU, advertising MPLS labels together with BGP prefixes) uses a different address family. So far so good.

Now for the intricate bit: a BGP router might negotiate IPv4 and IPv4-LU address families with a neighbor. Does that mean that it's advertising every IPv4 prefix twice, once without a label, and once with a label? Should that be the case, how are those prefixes originated and how are they stored in the BGP table?

As always, the correct answer is "_it depends_", this time on the network operating system implementation. This blog post describes Cisco IOS behavior, a follow-up one will focus on Arista EOS.
<!--more-->
### The Lab

Whenever I get a question along the lines "_what would happen if..._" I always ask the sender "_... and did you consider testing that in a lab?_"[^STOP]. We'll test BGP-LU behavior in a simple lab with three autonomous systems and a route reflector in the central autonomous system. 

[^STOP]: ... often followed by no reply whatsoever. Some people think they can use bloggers as Free Encyclopedia of Useless Trivia and walk away when asked to do a bit of homework first.

{{<figure src="/2022/03/bgp-lu-topology.bgp.png" caption="BGP sessions in the BGP-LU lab">}}

Labeled Unicast IPv4 address family (IPv4-LU) will be enabled on all BGP sessions apart from the PE1-CE1 session, so we'll be able to observe BGP-LU behavior on IBGP and EBGP sessions, as well as propagation of information (or lack thereof) between unlabeled and labeled address families. The lab topology file is [available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/MPLS/ldp-bgp-lu).

### Cisco IOS Behavior

Cisco IOS configuration treats labeled unicast as an add-on to IPv4 or IPv6 address family -- instead of activating a neighbor in a new address family, you add **send-label** parameter to a neighbor within IPv4 or IPv6 address family.

{{<cc>}}BGP-LU configuration on Cisco IOS{{</cc>}}
```
router bgp 65000
 bgp router-id 10.0.0.1
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 neighbor 10.0.0.4 remote-as 65000
 neighbor 10.0.0.4 description rr
 neighbor 10.0.0.4 update-source Loopback0
 neighbor 10.1.0.1 remote-as 65101
 neighbor 10.1.0.1 description ce1
 !
 address-family ipv4
  network 10.0.0.1 mask 255.255.255.255
  neighbor 10.0.0.4 activate
  neighbor 10.0.0.4 send-community both
  neighbor 10.0.0.4 next-hop-self
  neighbor 10.0.0.4 send-label explicit-null
  neighbor 10.1.0.1 activate
  neighbor 10.1.0.1 send-community
```

When you configure **neighbor send-label**, Cisco IOS tries to negotiate two address families (IP and IP-LU) on the BGP session:

{{<cc>}}BGP address families negotiated between PE1 and RR{{</cc>}}
```
pe1#show ip bgp nei 10.0.0.4 | section capabilities
  Neighbor capabilities:
    Route refresh: advertised and received(new)
    Four-octets ASN Capability: advertised and received
    Address family IPv4 Unicast: advertised and received
    ipv4 MPLS Label capability: advertised and received
    Enhanced Refresh Capability: advertised and received
    Multisession Capability:
    Stateful switchover support enabled: NO for session 1
```

Even though the routers negotiated IPv4 and IPv4-LU address families on the BGP session, the IPv4 BGP updates are sent only within the IPv4-LU address family. IPv4 address family is not used at all.

{{<cc>}}BGP updates between PE1 and CE1 (both running Cisco IOS){{</cc>}}
```
pe1#debug ip bgp all updates 10.0.0.4 in
BGP updates debugging is on for neighbor 10.0.0.4 (inbound) for all address families
pe1#clear ip bgp 10.0.0.4
pe1#
%BGP-5-ADJCHANGE: neighbor 10.0.0.4 Up
BGP(0): 10.0.0.4 rcvd UPDATE w/ attr: nexthop 10.0.0.2, origin i, localpref 100, metric 0, originator 10.0.0.2, clusterlist 10.0.0.4, merged path 65102, AS_PATH
BGP(0): 10.0.0.4 rcvd 10.0.0.6/32, label 22
BGP(0): 10.0.0.4 rcvd UPDATE w/ attr: nexthop 10.0.0.2, origin i, localpref 100, metric 0, originator 10.0.0.2, clusterlist 10.0.0.4
BGP(0): 10.0.0.4 rcvd 10.0.0.2/32, label 0
BGP(0): 10.0.0.4 rcvd UPDATE w/ attr: nexthop 10.0.0.4, origin i, localpref 100, metric 0
BGP(0): 10.0.0.4 rcvd 10.0.0.4/32, label 0
```

The unlabeled and labeled BGP prefixes are stored in the same BGP RIB. Labels are automatically assigned to all prefixes that are advertised over Labeled Unicast address families. 

Consider the labels assigned to BGP prefixes on PE1 (the *In Label* column contains labels assigned by the local router):

{{<cc>}}BGP labels on PE1{{</cc>}}
```
pe1#show ip bgp labels
   Network          Next Hop      In label/Out label
   10.0.0.1/32      0.0.0.0         imp-null/nolabel
   10.0.0.2/32      10.0.0.2        nolabel/exp-null
   10.0.0.4/32      10.0.0.4        nolabel/exp-null
   10.0.0.5/32      10.1.0.1        21/nolabel
   10.0.0.6/32      10.0.0.2        nolabel/22
```

* No label is assigned to 10.0.0.2/32, 10.0.0.4/32 and 10.0.0.6/32 because these prefixes aren't advertised over any BGP-LU sessions -- they were received over IBGP session from the route reflector and are advertised over EBGP session to CE1 (which has not activated the IPv4-LU AF).
* A label is assigned to 10.0.0.5/32 even though that prefix was not received over IPv4-LU address family.

The situation is slightly different on PE2 that has BGP-LU sessions with RR and CE2:

{{<cc>}}BGP labels on PE2{{</cc>}}
```
pe2#show ip bgp labels
   Network          Next Hop      In label/Out label
   10.0.0.1/32      10.0.0.1        18/exp-null
   10.0.0.2/32      0.0.0.0         imp-null/nolabel
   10.0.0.4/32      10.0.0.4        16/exp-null
   10.0.0.5/32      10.0.0.1        23/21
   10.0.0.6/32      10.1.0.5        22/exp-null
```

Going from BGP RIB to IP routing and forwarding tables, there's no difference between labeled and unlabeled prefixes apart from the label stack associated with the prefix advertised over IPv4-LU address family.

For example, the BGP-LU label for 10.0.0.6/32 (22) is combined with an LDP label for PE2 (16) on PE1 to get a label stack in the forwarding table:

{{<cc>}}MPLS label stack for CE2 loopback on PE1{{</cc>}}
```
pe1#show mpls forwarding-table 10.0.0.6 detail
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop
Label      Label      or Tunnel Id     Switched      interface
None       22         10.0.0.6/32      0             Gi0/2      10.1.0.9
	MAC/Encaps=14/22, MRU=1496, Label Stack{16 22}
	5254004057F9525400D3B3948847 0001000000016000
	No output feature configured
```

### Summary: Cisco IOS

* Labeled unicast is configured as yet another parameter on a BGP neighbor.
* The routers negotiate two address families, but use only the labeled address family to send the updates -- a nice optimization and a fallback mechanism in case the remote router does not support labeled unicast.
* There's a single BGP RIB for labeled and unlabeled prefixes. 
* Labeled and unlabeled prefixes are inserted into IP routing- and forwarding tables.
