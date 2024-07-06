---
date: 2011-09-09 06:33:00+02:00
tags:
- BGP
- EEM
title: Shut Down BGP Session Based on Tracked Object
url: /2011/09/shut-down-bgp-session-based-on-tracked.html
---
In responses to my [*The Road to Complex Designs is Paved With Great Recipes*](/2011/08/road-to-complex-designs-is-paved-with.html) post Daniel suggested shutting down EBGP session if your BGP router cannot reach the DMZ firewall and Cristoph guessed that it might be done without changing the router configuration with the **neighbor fall-over route-map** BGP configuration command. He was sort-of right, but the solution is slightly more convoluted than he imagined.
<!--more-->
Cristoph's original idea was simple enough: create a fake static route based on a **track** object (that can track anything you want) and match that route with the **fall-over route-map**. Unfortunately, that's not how the fast fall-over functionality works -- it takes the neighbor's IP address, finds all routes that can be used to reach the neighbor, and tests them with the specified **route-map** (more details in my *Designing Fast Converging BGP Networks* article -- search for it somewhere in [this list](/kb/Internet/)).

I used a creative approach to create a static route that fits the requirements of the [*Fast Peering Deactivation*](http://www.cisco.com/en/US/docs/ios/12_0s/feature/guide/cs_bsfda.html): a host route toward the BGP next hop pointing at BGP next hop.

Let's walk through a lab-tested example: The router is running BGP in AS\#65100 and has an EBGP session with 10.0.7.10 in AS\#65000:

``` {.code}
router bgp 65100
 bgp log-neighbor-changes
 network 10.0.1.1 mask 255.255.255.255
 neighbor 10.0.7.10 remote-as 65000
```

First we have to create the track object that will cause the BGP session termination. It can track anything -- you can track interface state, use IP SLA and ping the firewall, or even use EEM to trigger time-based (or other event-based) session shutdown. I decided to track the state of the LAN interface.

There are simpler solutions if you want to originate a BGP route only when the LAN interface is operational. Read [this blog post](/2011/08/road-to-complex-designs-is-paved-with.html) for more information.

``` {.code}
track 10 interface FastEthernet0/0 ip routing
 carrier-delay
```

Next, create a host route for the BGP next hop pointing to the next hop itself.

If you use a PPP interface to connect to the BGP next hop, make sure you disable **peer neighbor-route**, otherwise the router [creates a competing host route](/2008/02/remove-unwanted-ppp-peer-route.html) for the BGP next hop.

``` {.code}
ip route 10.0.7.10 255.255.255.255 Serial1/0 10.0.7.10 track 10
!
interface Serial1/0
 description Link to AS65000
 ip address 10.0.7.9 255.255.255.252
 encapsulation ppp
 no peer neighbor-route
```

We need a **prefix-list** and a **route-map** to match the host route toward the BGP next hop:

``` {.code}
ip prefix-list BGP_OK seq 5 permit 10.0.7.10/32
!
route-map BGP_OK permit 10
 match ip address prefix-list BGP_OK
```

And finally, we can configure the fast BGP session deactivation on the EBGP session:

``` {.code}
router bgp 65100
 neighbor 10.0.7.10 fall-over route-map BGP_OK
```

**Test\#1 -- shut down the LAN interface**. BGP session is shut down almost immediately (you can fine-tune the delay with **track** object parameters).

``` {.code}
A1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
A1(config)#int fa 0/0
A1(config-if)#shut
A1(config-if)#
15:27:55.719: %LINK-5-CHANGED: Interface FastEthernet0/0, changed state to 
  administratively down
15:27:56.383: %TRACKING-5-STATE: 10 interface Fa0/0 ip routing Up->Down
15:27:56.415: %BGP-5-ADJCHANGE: neighbor 10.0.7.10 Down Route to peer lost
15:27:56.415: %BGP_SESSION-5-ADJCHANGE: neighbor 10.0.7.10 IPv4 Unicast 
  topology base removed from session  Route to peer lost
15:27:56.719: %LINEPROTO-5-UPDOWN: Line protocol on Interface 
  FastEthernet0/0, changed state to down
```

**Test\#2 -- re-enable the LAN interface**. BGP session is reestablished in less than a second. Perfect ;)

``` {.code}
A1(config-if)#no shut
A1(config-if)#
15:29:22.211: %LINK-3-UPDOWN: Interface FastEthernet0/0, changed state to up
15:29:22.395: %TRACKING-5-STATE: 10 interface Fa0/0 ip routing Down->Up
15:29:22.511: %BGP-5-ADJCHANGE: neighbor 10.0.7.10 Up
15:29:23.211: %LINEPROTO-5-UPDOWN: Line protocol on Interface
  FastEthernet0/0, changed state to up
```

#### Need help?

BGP is one of those topics that never cease to intrigue me. If you need help getting it up and running, check out our [*ExpertExpress*](http://www.ipspace.net/ExpertExpress) service.
