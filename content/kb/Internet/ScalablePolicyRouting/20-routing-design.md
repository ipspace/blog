---
kb_section: ScalablePolicyRouting
minimal_sidebar: true
pre_scroll: true
title: Basic Routing Design
url: /kb/Internet/ScalablePolicyRouting/20-routing-design/
---
The whole network uses BGP as its core routing protocol, giving us a highly-scalable solution with the inherent capability to implement policy-based routing (most of the BGP’s complexity is a direct result of its abilities to perform policy-based routing decisions). Each site is a separate autonomous system (AS); remote sites have one or two routers in their AS and the central site can have as many routers as needed, using the two core routers as BGP route reflectors. OSPF is also deployed in the core site to ensure fast convergence and solve the BGP next-hop problems. The overall routing design is displayed in the next diagram:

{{<figure src="/kb/Internet/ScalablePolicyRouting/routing-design.jpg" caption="Basic Routing Design">}}

You could decide to simplify the router configuration by redistributing directly connected routes into the BGP on each router, but this would just pollute the BGP tables with the point-to-point WAN subnets that are usually not needed for proper network operation. It’s thus better to manually list the networks you want to announce in the BGP routing process. The sample configuration from one of the remote sites is included in the next listing:

{{<cc>}}BGP configuration on Site-A{{</cc>}}
```
router bgp 65100
 network 10.0.1.1 mask 255.255.255.255
 network 192.168.1.0
```

{{<note note>}}Only the most relevant parts of the router configurations are included in the article.{{</note>}}

To make the core router configurations as scalable as possible, we’re using BGP peer policy and peer session templates. These template mechanisms might look verbose if you have only a few neighbors, but the ease-of-management they give you quickly pays off – if you have to make a change in your BGP configuration, you change the settings in one place and they get propagated to all BGP neighbors automatically. For example, the core BGP routers use several templates:

*	The *LocalAS* session template is used to create all peers in the same AS;
*	The *Global* policy template defines rules that apply to all neighbors (community propagation is configured in this template);
*	The *RRClient* template covers all the other routers in the central site;
*	The *RemoteSite* template specifies parameters for the BGP neighbors on remote sites.

Here are the BGP templates used on the *CoreInet* router:

{{<cc>}}BGP templates on the *CoreInet* router{{</cc>}}
```
router bgp 65000
 template peer-policy Global
  send-community both
!
 template peer-policy LocalAS
  inherit peer-policy Global 1
!
 template peer-policy RRClient
  route-reflector-client
  inherit peer-policy Global 1
!
 template peer-policy RemoteSite
  inherit peer-policy Global 1
!
 template peer-session LocalAS
  remote-as 65000
  update-source Loopback0
```

And this is how those templates are used to configure BGP neighbors:

{{<cc>}}BGP neighbors of the *CoreInet* router{{</cc>}}
```
router bgp 65000
 neighbor 10.0.1.3 description CoreFR
 neighbor 10.0.1.3 inherit peer-session LocalAS
 neighbor 10.0.1.3 inherit peer-policy LocalAS
 !
 neighbor 10.0.1.4 description Legacy
 neighbor 10.0.1.4 inherit peer-session LocalAS
 neighbor 10.0.1.4 inherit peer-policy RRClient
 !
 neighbor 10.0.1.20 description Web
 neighbor 10.0.1.20 inherit peer-session LocalAS
 neighbor 10.0.1.20 inherit peer-policy RRClient
 !
 neighbor 10.0.11.2 description Site-A
 neighbor 10.0.11.2 remote-as 65100
 neighbor 10.0.11.2 inherit peer-policy RemoteSite
 !
 neighbor 10.0.11.6 description Site-B
 neighbor 10.0.11.6 remote-as 65101
 neighbor 10.0.11.6 inherit peer-policy RemoteSite
 !
 neighbor 10.0.11.10 description Site-C
 neighbor 10.0.11.10 remote-as 65102
 neighbor 10.0.11.10 inherit peer-policy RemoteSite
```

On the other hand, the routers on the remote sites have just two BGP neighbors. Implementing peer templates is thus overkill, the traditional BGP configuration is used on remote sites:

{{<cc>}}BGP configuration on a remote site{{</cc>}}
```
router bgp 65100
 neighbor 10.0.8.1 remote-as 65000
 neighbor 10.0.8.1 description CoreInet
 !
 neighbor 10.0.11.1 description CoreFR
 neighbor 10.0.11.1 remote-as 65000
```

<!-- end -->
