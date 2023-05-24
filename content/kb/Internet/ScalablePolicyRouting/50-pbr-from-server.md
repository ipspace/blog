title: Policy Routing from the Server

The changes to BGP routing that force the traffic flow from the *Legacy* servers to remote sites through the slower links are slightly more complex. Obviously, both core routers (*CoreFR* and *CoreInet*) have to prefer BGP prefixes received from remote sites over the same BGP prefixes received from the other core router. That’s the default BGP behavior (so we need no configuration change on *CoreInet* and *CoreFR*), but this requirement also precludes the usage of tools like BGP Local Preference or Multi-Exit Discriminator as any of these attributes would make routes from one of the core routers preferable on all other routers on the central site.

Even though the *CoreInet* and *CoreFR* routers cannot modify any BGP attributes of the routes received from the remote sites, the *Legacy* router has to prefer BGP routes received from the *CoreFR* router (to ensure the traffic from the legacy servers is sent over the slower link) and the *Web* router has to prefer BGP routes received from the *CoreInet* router (making the traffic from the internal Web servers flow over through the GRE-over-Internet tunnels).

The easiest BGP tool available to do the job is the **weight** mechanism[^WL] that is local to a router and does not change any of the BGP attributes, ensuring that even if the *Web* and *Legacy* routers would propagate their BGP routes, these would not be changed. You could use any other mechanism that influences BGP route selection algorithm, including _local preference_ (set with an inbound route map) or IGP cost (increase IGP cost on the link between *Legacy* and *CoreInet* routers).

To simplify the implementation, we’ll use static weights: all routes received from the *CoreFR* router will have a higher weight on the *Legacy* router. 

[^WL]: Weights are an intra-device tool and are thus not standardized or required by any BGP-related RFC. They are therefore not available in all BGP implementations.

```
router bgp 65000
 neighbor 10.0.1.3 weight 500
```
CAPTION: BGP configuration change on the Legacy router

You have to perform BGP soft reconfiguration with the **clear ip bgp \* soft in** command on the *Legacy* router after changing its BGP configuration to make sure that the BGP prefixes received from the *CoreFR* and *CoreInet* routers are processed using the new set of parameters. After the new updates are processed, the *Legacy* router prefers prefixes received from the *CoreFR* router.

```
Legacy#show ip bgp reg 65100

   Network          Next Hop            Metric LocPrf Weight Path
*>i10.0.1.1/32      10.0.8.2                 0    100    500 65100 i
* i                 10.0.11.2                0    100      0 65100 i
*>i192.168.1.0      10.0.8.2                 0    100    500 65100 i
* i                 10.0.11.2                0    100      0 65100 i 
```
CAPTION: BGP prefixes originated by Site-A on the *Legacy* router

NOTE: Even though the *Legacy* router always prefers routes received from the *CoreFR* router, the traffic flow is always optimal, as the BGP next-hop of an external route does not change within the autonomous system, regardless of the path the route has taken to reach the final BGP router.

Likewise, the weights are set on the *Web* router to prefer BGP prefixes received from the *CoreInet* router:

```
router bgp 65000
 neighbor 10.0.1.2 weight 500
```
CAPTION: BGP configuration change on the *Web* router

The results of this configuration change are shown in the next printout:

```
Web#show ip bgp regexp 65100

   Network          Next Hop            Metric LocPrf Weight Path
*>i10.0.1.1/32      10.0.11.2                0    100    500 65100 i
* i                 10.0.8.2                 0    100      0 65100 i
*>i192.168.1.0      10.0.11.2                0    100    500 65100 i
* i                 10.0.8.2                 0    100      0 65100 i
```
CAPTION: BGP prefixes originated by Site-A on the *Web* router

In a more complex scenario, you could duplicate the setup used in the previous section: the *CoreFR* and the *CoreInet* routers would set BGP communities on BGP routes received from the remote sites and the *Legacy* and the *Web* routers would change BGP local preference or weight for routes marked with specific BGP community, but this would only complicate the design. The implementation would be even more complex if there would be additional routers between the *Legacy* and the *CoreFR* routers.
