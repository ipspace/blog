---
title: "IBGP Source Interface Selection Still Requires Configuration"
date: 2024-12-10 08:32:00+0100
tags: [ BGP ]
---
A fellow networking engineer recently remarked, "_FRRouting automatically selects the correct [IBGP] source interface even when not configured explicitly._"

**TL&DR:** No, it does not. You were just lucky.

Basics first[^OBP]. BGP runs over TCP sessions. One of the first things a router does when establishing a BGP session with a configured neighbor is to open a TCP session with the configured neighbor's IP address.

[^OBP]: FWIW, I wrote a [blog post about this topic in 2008](/2008/01/bgp-essentials-configuring-internal-bgp/). It looks like I can write a "this is how it works" blog post on any topic once a decade or so, and it still wouldn't help.
<!--more-->
That works really well for EBGP sessions, usually established between directly connected IP addresses. Let's assume that R1 (from the following diagram) tries to open a TCP session with R2:

{{<ascii>}}
                   10.0.0.2        
┌──────┐                 ┌──────┐  
│  R1  ├─────────────────┤  R2  │  
└──────┘                 └──────┘  
      10.0.0.1                     
{{</ascii>}}

The BGP daemon on R1 asks the TCP/IP stack to open a TCP session with 10.0.0.2. If it does not specify the desired source IP address, the TCP/IP stack takes the IP address of the outgoing interface as the source IP address. Thus, the TCP SYN request is sent from 10.0.0.1 to 10.0.0.2. Assuming you configured a BGP neighbor with IP address 10.0.0.1 on R2, R2 continues the 3-way handshake. Eventually, we have a TCP session between 10.0.0.1 and 10.0.0.2. Mission accomplished.

Not so fast. In the IBGP world, we prefer having TCP sessions between loopback addresses to ensure the BGP sessions are not affected by changes within the network[^EVPN]. In our scenario, the IP subnet on the link between the two routers is 172.16.0.0/24, while we use the loopback IP addresses from the 10.0.0.0/24 range.

[^EVPN]: EVPN uses the same approach, resulting in [ridiculous designs](/2024/11/evpn-designs-ibgp-ebgp/) when a vendor with a decent IBGP EVPN implementation desperately wants to look cool.

{{<ascii>}}
10.0.0.1                 10.0.0.2
┌──────┐                 ┌──────┐
│  R1  ├─────────────────┤  R2  │
└──────┘                 └──────┘
   172.16.0.1       172.16.0.2
{{</ascii>}}

What happens when the BGP daemon on R1 asks the TCP/IP stack to open a TCP session with 10.0.0.2? Assuming a path to 10.0.0.2 is in the forwarding table, a TCP SYN packet is sent toward 172.16.0.2 (the next hop toward 10.0.0.2) *with the source IP address set to 172.16.0.1*. R2 takes a quick look at that packet, decides it's a spoofing attempt (it has no BGP neighbor with IP address 172.16.0.1), and [drops the packet](https://blog.ipspace.net/2023/10/reject-unknown-bgp-session/) (or [opens a TCP session and politely tells the intruder to go away](https://blog.ipspace.net/2023/11/open-bgp-daemons/)).

To establish an IBGP session between R1 and R2, the routers MUST send the TCP SYN packet with the source IP address set to the loopback interface IP address. In a [blatant violation of layering principles](https://blog.ipspace.net/2009/08/what-went-wrong-socket-api/), TCP/IP stacks allow applications to specify the source IP address of the TCP sessions, which BGP daemons do to make IBGP work.

However, figuring out what source IP address to use is a Mission Impossible. Some people believe in running IBGP sessions between directly connected interfaces, and others love to have more than one loopback interface or more than one IP address on the loopback interface. That's why we must specify the **neighbor update-source** parameter in most BGP implementations.

Back to our network engineer. When told that the FRRouting BGP daemon does not provide the magic[^MAGIC] source address auto-selection functionality, he claimed that "*it accidentally selected the correct interface.*"

[^MAGIC]: Vendor marketers would claim it's AI. AI can get you better funding than PFM these days.

**TL&DR:** No, it did not. One of the neighbors was configured correctly.

Here's what happened. **neighbor update-source** was configured on R2 but not on R1. R1 would try to establish a TCP session between 172.16.0.1 and 10.0.0.2. As we already know, R2 rejects that session. In the meantime, R2 tries establishing a TCP session between 10.0.0.2 and 10.0.0.1, and R1 accepts the incoming TCP SYN request. We have a working IBGP session between R1 and R2, even though the **neighbor update-source** is configured only on one end of the TCP session.

You are probably already considering the implications if you have a devious mind. For example, you could configure the source IP address of the BGP session only on route reflectors, and the network would still work. Even better[^FJJS], you could run route reflectors on hosts without a loopback interface[^RD] (for example, [in virtual machines](https://blog.ipspace.net/2021/10/circular-dependencies-considered-harmful/)[^CD]). In that design, you would never have an issue with the source IP addresses of the TCP sessions (the proof is left as an exercise for the reader) unless another creative engineer decides to "optimize" the CPU utilization on the route reflectors and configures *[dynamic BGP peers](https://bgplabs.net/session/9-dynamic/)* or *[passive BGP peers](https://bgplabs.net/session/8-passive/)*.

**Long story short:** Don't be a MacGyver. Whenever you use BGP between loopback interfaces, specify the source IP address to use when opening the TCP sessions.

[^RD]: You run two or more route reflectors anyway. You can ignore link failures, right?

[^FJJS]: For your job security

[^CD]: If you love circular dependencies
