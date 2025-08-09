---
title: "iBGP Local-AS Route Propagation"
date: 2025-08-29 07:52:00+0200
tags: [ BGP ]
---
In the [previous blog post on this topic](/2025/04/ibgp-local-as-details/), I described the iBGP local-as functionality and explained why we MUST change the BGP next hop on the routes sent over the fake iBGP session (TL&DR: because we're not running IGP across that link).

That blog post used a simple topology with three routers. Now let's add a few more routers to the mix and see what happens.
<!--more-->
{{<figure src="/2025/08/localas_ibgp_topo.png">}}

The Device Under Test (DUT) in [our lab](https://github.com/ipspace/netlab/blob/dev/tests/integration/bgp/08-ibgp-localas.yml) has three BGP sessions:

* A real IBGP session with X3
* A real EBGP session with X1
* A fake IBGP (local-as IBGP) session with X2

We'll use FRRouting as the DUT router; here's the relevant configuration (including the **next-hop-self** option configured on the *local-as IBGP* session):

{{<cc>}}DUT BGP configuration (FRRouting){{</cc>}}
```
router bgp 65000
 bgp router-id 10.0.0.1
 no bgp default ipv4-unicast
 bgp bestpath as-path multipath-relax
 neighbor 10.0.0.4 remote-as 65000
 neighbor 10.0.0.4 description x3 (IBGP)
 neighbor 10.0.0.4 update-source lo
 neighbor 10.1.0.2 remote-as 65100
 neighbor 10.1.0.2 local-as 65002 no-prepend replace-as
 neighbor 10.1.0.2 description x1 (EBGP)
 neighbor 10.1.0.6 remote-as 65101
 neighbor 10.1.0.6 local-as 65101 no-prepend replace-as
 neighbor 10.1.0.6 description x2 (local-as IBGP)
 !
 address-family ipv4 unicast
  network 10.0.0.1/32
  network 172.42.42.0/24
  neighbor 10.0.0.4 activate
  neighbor 10.0.0.4 next-hop-self
  neighbor 10.1.0.2 activate
  no neighbor 10.1.0.2 send-community extended
  neighbor 10.1.0.6 activate
  neighbor 10.1.0.6 next-hop-self
```

Here's how well route propagation works with our simplistic setup. The rows in the following table [^CT] are the routers advertising a prefix; the columns are the target routers.

[^CT]: To create the table, I executed the **show ip bgp** command on all four routers and checked the prefixes visible in the BGP table.

| Source ⬇️ Target ➡️ | DUT | X1 (EBGP) | X2<br>(Local-AS IBGP) | X3 (IBGP) |
|-----|:-:|:-:|:-:|:-:|
| DUT | ✅| ✅| ✅| ✅|
| X1  | ✅| ✅| ✅| ✅|
| X2  | ✅| ✅| ✅| ❌ |
| X3  | ✅| ✅| ❌ | ✅|
{ .fmtTable style="width: auto" }

* DUT can see all routes, as can X1 (no surprise there)
* X2 and X3 can see routes from DUT and X1 routes propagated by DUT
* DUT is not propagating routes between X2 and X3

What could possibly be wrong? Why wouldn't DUT propagate IBGP routes received from X3 over another (albeit fake) IBGP session to X2?

Of course: the routes between the two IBGP sessions must be **reflected**. Trying to minimize the configuration changes, let's configure X2 as a route-reflector client on DUT.

{{<cc>}}Configure X2 as a route-reflector client on DUT{{</cc>}}
```
router bgp 65000
 neighbor 10.1.0.6 description x2 (local-as IBGP)
 !
 address-family ipv4 unicast
  neighbor 10.1.0.6 next-hop-self
  neighbor 10.1.0.6 route-reflector-client
```

Did anything change? Here are the test results (limited to what's visible on X2 and X3):

| Source ⬇️ Target ➡️ | X2<br>(Local-AS IBGP) | X3 (IBGP) |
|-----|:-:|:-:|
| DUT | ✅| ✅|
| X1  | ✅| ✅|
| X2  | ✅| ❗️|
| X3  | ❗️| ✅|
{ .fmtTable style="width: auto" }

While the X2/X3 routes appear in the BGP tables on X3 and X2, they are not *valid*. Let's look at the X3 prefix on X2:

{{<cc>}}X2 claims the X3 prefix is not valid{{</cc>}}
```
x2# show ip bgp 172.42.3.0
BGP routing table entry for 172.42.3.0/24, version 0
Paths: (1 available, no best path)
  Not advertised to any peer
  Local, (Received from a RR-client)
    10.0.0.4(dut) (inaccessible, import-check enabled) from dut(10.1.0.5) (10.0.0.4)
      Origin IGP, metric 0, localpref 100, invalid, internal
      Originator: 10.0.0.4, Cluster list: 10.0.0.1
      Last update: Sat Aug  9 13:20:29 2025
```

We're back to the **next hop** saga. Not only do we have to change the next hop on the EBGP routes sent to X2, we have to do it on **all** routes sent to X2 (including the reflected routes). Fortunately, numerous network operating systems support that nerd knob. Here's the relevant FRRouting configuration:

```
router bgp 65000
 neighbor 10.1.0.6 description x2 (local-as IBGP)
 neighbor 10.0.0.4 description x3 (IBGP)
!
 address-family ipv4 unicast
  neighbor 10.0.0.4 next-hop-self force
  neighbor 10.1.0.6 next-hop-self force
```

{{<note>}}
We also have to change the next hops of the X2 routes reflected to X3 (the proof is left as an exercise for the reader 😎); we have to configure **neighbor next-hop-self force** on *all* IBGP and local-as IBGP neighbors.
{{</note>}}

[^PLER]: 

To recap. A router with at least one *local-as IBGP* session:

* MUST be a route-reflector for the *local-as IBGP* peer
* MUST set the next-hop to *self* on *all IBGP and local-as IBGP sessions* for *EBGP and reflected IBGP* routes.
* SHOULD NOT be used as a route reflector in its autonomous system (because it would mangle the next hops and redirect all the traffic to itself)

Furthermore, you MUST apply the same rules to the router on the other side of the local-as IBGP session[^AER] (X2 in our topology).

[^PLER]: The proof is left as an exercise for the reader ;)

[^AER]: Another exercise for the reader. Add another router to AS 65101 and observe the propagation of its routes.
