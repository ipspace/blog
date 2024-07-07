---
title: "LISP vs EVPN: Mobility in Campus Networks"
date: 2024-04-11 08:29:00+0200
tags: [ EVPN, LISP ]
---
I decided not to get involved in the EVPN-versus-LISP debates anymore; I'd [written everything I had to say about LISP](/tag/lisp/). However, I still get annoyed when experienced networking engineers fall for marketing gimmicks disguised as technical arguments. Here's a recent one:

{{<figure src="/2024/04/juniper-campus-lisp-tweet.png">}}
<!--more-->
**TL&DR:** The discussion on whether "*LISP scales better than EVPN*" became irrelevant when the bus between the switch CPU and the adjacent ASIC became the bottleneck. Modern switches can process more prefixes than they can install in the ASIC forwarding tables (or we wouldn't be using [prefix-independent convergence](/2012/01/prefix-independent-convergence-pic/)).

Now, let's focus on the dynamics of campus mobility. There's almost no endpoint mobility if a campus network uses wired infrastructure. If a campus is primarily wireless, we have two options:

* The wireless access points use tunnels to a wireless controller (or an aggregation switch), and all the end-user traffic enters the network through that point. The rest of the campus network does not observe any endpoint mobility.
* The wireless access points send user traffic straight into the campus network, and the endpoints (end user IP/MAC addresses) move as the users roam across access points.

Therefore, the argument seems to be that LISP is better than EVPN at handling a high churn rate. Let's see how much churn BGP (the protocol used by EVPN) can handle using data from a large-scale experiment called The Internet. According to [Geoff Huston's statistics](https://blog.apnic.net/2024/01/10/bgp-in-2023-bgp-updates/) ([relevant graph](https://blog.apnic.net/wp-content/uploads/2024/01/bgpupd2023-fig2.png)), we've experienced up to 400.000 daily updates in 2021, with the *smoothed long-term average* being above 250.000. That's around *four updates per second on average.* I have no corresponding graph from an extensive campus network (but I would love to see one), but as we usually don't see users running around the campus, the roaming rate might not be much higher.

However, there seems to be another problem: latency spikes following a roaming event.

{{<figure src="/2024/04/wifi-roaming-latency-tweet.png">}}

I have no idea how someone could attribute *latency* spikes equivalent to [ping times between Boston and Chicago](https://wondernetwork.com/pings/Boston) to a MAC move event. Unless there's some magic going on behind the scenes:

* The end-user NIC disappears from point A, and the switch is unaware of that (not likely with WiFi).
* The rest of the network remains clueless; traffic to the NIC MAC address is still sent to the original switch and dropped.
* The EVPN MAC move procedure starts when the end-user NIC reappears at point B.
* Once the network figures out the MAC address has moved, the traffic gets forwarded to the new attachment point.

Where's latency in that? The only way to introduce latency in that process is to have traffic buffered at some point, but that's not a problem you can solve with EVPN or LISP. All you can get with EVPN or LISP is the notification that the MAC address is now reachable via another egress switch.

OK, maybe the engineer writing about latency misspoke and meant *the traffic is disrupted for 20 msec.* In other words, the MAC move event takes 20 msec. Could LISP be better than EVPN in handling that? Of course, but it all comes down to the *quality of implementation.* In both cases:

* A switch control plane [has to notice](/2023/04/evpn-dynamic-mac-learning/) its hardware discovered a new MAC address (forty years after the STP was invented, we're still doing dynamic MAC learning at the fabric edge).
* The new MAC address is announced to some central entity (route reflector), which propagates the update to all other edge devices.
* The edge devices install the new MAC-to-next-hop mapping into the forwarding tables.

Barring implementation differences, there's no fundamental reason why one control-plane protocol would do the above process better than another one.

But wait, there's another gotcha: at least in [some implementations](/2023/05/silent-hosts-evpn/#1814), the control plane takes "forever" to notice a new MAC address. However, that's a hardware-related quirk, and no control-plane protocol will fix that one. No wonder some people talk about [dynamic MAC learning with EVPN](/2023/09/dynamic-mac-learning-evpn/).

**Aside:** If you care about fast MAC mobility, you might be better off doing dynamic MAC learning across the fabric. You don't need EVPN or LISP to do that; VXLAN fabric with ingress replication or SPB will work just fine.

Before doing a summary, let me throw in a few more numbers:

* We don't know how fast modern switches can update their ASIC tables (thank you, [ASIC vendors](/2016/05/what-are-problems-with-broadcom/)), but the rumors talk about 1000+ entries per second.
* The behavior of [open-source routing daemons](https://elegantnetwork.github.io/posts/comparing-open-source-bgp-internet-routes/) and even [commercial BGP stacks](https://elegantnetwork.github.io/posts/BGP-commercial-stacks/) is well-documented thanks to the [excellent work by Justin Pietch](https://elegantnetwork.github.io/posts/comparing-open-source-bgp-internet-routes/). Unfortunately, he didn't publish the raw data, but looking at his graphs, it seems that good open-source daemons have no problems processing 10K prefixes in a second or two.

It seems like we're at a point where (assuming optimal implementations) the BGP update processing rate on a decent CPU[^MT] exceeds the FIB installation rate.

[^MT]: Bonus points for [using multiple threads](/2021/11/multi-threaded-routing-daemons/) on a multi-core CPU.

Back to LISP versus EVPN. It should be evident by now that:

* A campus network is probably not more dynamic than the global Internet;
* BGP handles the churn in the global Internet just fine, and there's no technological reason why it couldn't do the same in an EVPN-based campus.
* BGP implementations can handle at least as many updates as can be installed in the hardware FIB.
* Regardless of the actual numbers, decent control-plane implementations and modern ASICs are fast enough to deal with *highly dynamic* environments.
* Implementing control-plane-based MAC mobility with a minimum traffic loss interval is a complex undertaking that depends on more than just a control-plane protocol.

There might be a reason only a single business unit of a single vendor uses LISP in their fabric solution (hint: regardless of what the whitepapers say, it has little to do with technology).

