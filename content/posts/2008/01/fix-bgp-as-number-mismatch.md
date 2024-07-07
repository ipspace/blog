---
date: 2008-01-09 06:52:00+01:00
tags:
- BGP
title: Fix a BGP AS Number Mismatch
url: /2008/01/fix-bgp-as-number-mismatch/
---
Sometimes you end up having wrong BGP AS number throughout your network. It could be a result of an unexpected merger or split or you could have started using a private BGP AS number and realized you have to connect to the Internet using a real AS number. The proper solution would be a total reconfiguration of the whole network, but of course not many engineers have the time and courage to do it ;), so it\'s time to introduce another kludge: the **neighbor local-as** configuration command.
<!--more-->
For example, let\'s assume your AS number should be 20, but you\'re using a private AS 65001, as shown in the following figure:

{{<figure src="/2008/01/bgp_1.jpg">}}

To retain the AS 65001 internally but appear as AS 20 to the outside world, you could use the following configuration on R1:

``` {.code}
router bgp 65001
 neighbor 10.0.0.18 remote-as 65001
 neighbor 10.0.0.18 description IBGP to R2
 neighbor 10.1.0.2 remote-as 10
 neighbor 10.1.0.2 local-as 20
 neighbor 10.1.0.2 description EBGP to AS 10
```

This configuration would ensure that the EBGP session with AS 10 is established (R1 pretends that it belongs to AS 20 on this session), but the AS path propagated to AS 30 is somewhat odd ...

``` {.code}
AS30#show ip bgp | include 20
*> 172.16.0.0     10.1.0.5      0 20 65001 20 10 i
```

... making your network appear as a set of nested autonomous systems:

{{<figure src="/2008/01/bgp_2.jpg">}}

There are two reasons for the weird AS path:

-   R1 inserts **local-as** into inbound EBGP updates
-   R2 (configured like R1) inserts **local-as** as well as its real AS (65001) in outbound EBGP update

To fix the AS path, you need the [BGP Support for Dual AS Configuration](http://www.cisco.com/univercd/cc/td/doc/product/software/ios124/124cg/hirp_c/ch05/hbgpdas.htm) introduced in IOS release 12.3T. This feature adds two options to the **local-as** configuration command:

-   **no-prepend** disables **local-as** prepending on incoming EBGP updates;
-   **replace-as** replaces router\'s own AS with **local-as** on outgoing EBGP updates.

When the configuration on R1 and R2 includes these two keywords ...:

``` {.code}
router bgp 65001
 neighbor 10.1.0.2 remote-as 10
 neighbor 10.1.0.2 local-as 20 no-prepend replace-as
 neighbor 10.1.0.2 description EBGP to AS 10
```

... the path propagated through AS 65001/AS 20 looks as expected:

``` {.code}
AS30#show ip bgp | include 20
*> 172.16.0.0     10.1.0.5     0 20 10 i
```
