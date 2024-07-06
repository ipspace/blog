---
date: 2019-10-01 09:01:00+02:00
tags:
- BGP
- SLA
- SD-WAN
title: Changing Cisco IOS BGP Policies Based on IP SLA Measurements
url: /2019/10/changing-cisco-ios-bgp-policies-based.html
sd-wan_tag: weird
---
This is a guest blog post by [Philippe Jounin](https://www.linkedin.com/in/phjounin/), Senior Network Architect at Orange Business Services.

---

You could use **track** objects in Cisco IOS to track route reachability or metric, the status of an interface, or IP SLA compliance for a long time. Initially you could use them to implement [reliable static routing](/2007/02/reliable-static-routing.html) (or even [shut down a BGP session](/2011/09/shut-down-bgp-session-based-on-tracked.html)) or trigger EEM scripts. With a bit more work (and a few more EEM scripts) you could use object tracking to create [time-dependent static routes](/2010/11/time-based-static-routes.html).

Cisco IOS 15 has introduced [Enhanced Object Tracking](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp/configuration/xe-2/iap-xe-2-book/iap-eot.html) that allows first-hop router protocols like VRRP or HSRP to use tracking state to modify their behavior.
<!--more-->
Although it is not documented, I was curious to test if object tracking may be used inside a BGP **route-map**. This would provide a nice alternative to BGP knobs like **inject-maps** or **advertise-maps**, but also make BGP react to ip SLA measurements, just like a brand new SD-WAN network!

My lab consists of 2 routers connected with 2 links (replace direct links with IPSec tunnels if you are thinking about SD-WAN). The traffic between the two endpoints should go through Link1 if the link's delay is below 10 ms, and go through Link2 otherwise (obviously only if Link2 is available).

Collecting the delay between the routers is quite easy with the IP SLA Monitoring feature:

    ip sla 65000
     udp-echo 10.0.1.2 3456
     threshold 10
     timeout 100
     frequency 3
    ip sla schedule 65000 life forever start-time now
    ip sla responder

The IP SLA measurement is linked with an object in order to monitor the SLA compliance. The tracking object will be *up* if the delay is below 10 msec and *down* otherwise. I'm also using dampening timers (15 seconds on delay increase, 30 seconds on decrease).

    track 65 ip sla 65000
     delay down 15 up 30
     match track 65

Using the tracking object inside a route-map allows BGP to change some attributes after a the tracking object changes state. In this lab, we change Link1 local preference in order to reflect the IP SLA status.

    router bgp 65000
     bgp log-neighbor-changes
     network 192.168.7.0
     neighbor 10.0.1.2 remote-as 65000
     neighbor 10.0.1.2 description -- Link 1 --
     neighbor 10.0.1.2 route-map DynamicLP out
     neighbor 10.0.2.2 remote-as 65000
     neighbor 10.0.2.2 description -- Link 2 –

    route-map DynamicLP permit 10
     description -- SLA in profile: primary path --
     match track 65
     set local-preference 200
    !
    route-map DynamicLP permit 20
     description -- SLA out of profile: backup path --
     set local-preference 50

As expected, the local preference is correctly set by the **route-map** depending on the link SLA.

At t=10s, we set a jitter of 50ms, randomly increasing the delay on the Link1. The tracking object status changes after about 20 seconds and BGP advertises the new local preference after another 30 seconds, moving the traffic to Link2.

Of course, if we remove the jitter, the traffic returns to Link1

{{<figure src="/2019/10/s1600-tracked+object.png">}}