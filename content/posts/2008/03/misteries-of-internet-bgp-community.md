---
date: 2008-03-13 07:11:00.001000+01:00
tags:
- BGP
title: The Mysteries of the “Internet” BGP Community
url: /2008/03/misteries-of-internet-bgp-community/
---
[Cisco documentation has always claimed there were four well-known communities](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/command/irg-cr-book/bgp-n1.html#wp2607806244) (the *Internet* community being one of them), while the [RFC 1997 lists three well-known values](http://tools.ietf.org/html/rfc1997). Unfortunately, many people blindly copy the IOS documentation without asking themselves "what the heck is the *Internet* community".

{{<note update>}}**Update 2020-12-27**: While cleaning up this 12 year old blog post I searched for the latest *Cisco IOS IP Routing: BGP Command Reference* document and it still contains the same error.{{</note>}}
<!--more-->
It was time to revisit the mystery. I've tried applying the *Internet* community to a network originated by the BGP routing process to see what its value is:

``` {.code}
router bgp 65000
 network 192.168.1.0 route-map SetInternet
!
route-map SetInternet
 set community internet additive
```

While the router obediently attached the *Internet* community to the IP prefix, I was no wiser ... all show outputs converted the community value into its symbolic name. I had to use Wireshark and analyze the actual routing updates between BGP neighbors to figure out that the *Internet* community has an illegal value 0:0. Obviously it's not a well-known community.

Digging through old materials finally gave me the answer I was looking for: sometimes you need a *permit all* at the end of the **ip community-list** (like access-lists, the community-lists have an implicit *deny all* at the end) and someone decided that **permit internet** makes more sense than the familiar **permit any** (yes, that's correct ... you use the keyword **internet** to match *any community* in the **ip community-list**).\
\
And just for the sake of completeness, let me conclude with a slide from late 1990s explaining this phenomenon:

{{<figure src="/2008/03/bgpCommunity.jpg">}}