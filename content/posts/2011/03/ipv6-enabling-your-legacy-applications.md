---
date: 2011-03-23 06:39:00.004000+01:00
tags:
- IPv6
- load balancing
title: IPv6-Enabling Your Legacy Applications with F5 BIG-IP LTM
url: /2011/03/ipv6-enabling-your-legacy-applications.html
---
In every enterprise-focused IPv6 presentation, including my [Enterprise IPv6 -- the first steps](https://www.ipspace.net/IPv6E101) webinar, I'm telling the attendees that they can easily make their legacy applications reachable over IPv6 with a little help from F5 load balancers. After all, Facebook is doing exactly that, so it should work (in theory)... but as we all know, in practice, the theory and practice are wildly different.
<!--more-->
Last week I decided to get my hands dirty: I downloaded the evaluation version of F5 BIG-IP Local Traffic Manager Virtual Edition (LTM VE), installed it within my VMware workstation and tried to configure IPv6-to-IPv4 load balancing. I've never touched (or seen) F5 products before, but after less than an hour I had the basic IPv4 functionality up and running and thirty minutes later my web browser happily opened an IPv4 web site using an IPv6 address. The only glitch I've encountered is F5's interpretation of IPv6 addresses in its GUI -- double colons don't work, you have to write the whole address chunk-by-chunk -- and I only realized that after configuring everything through the Traffic Manager Shell (**tmsh**).

Here are the steps I took to clone an existing IPv4 load-balancing virtual server into an IPv6-to-IPv4 virtual server:

**Assign an IPv6 address to the external interface**. Not sure whether this is mandatory, but it definitely helped me. Edit the existing **net self** definition from the *external* VLAN and change its IPv4 address into an IPv6 address:

``` code
create net self fd00:dead:beef:1::1/64 {
    vlan external
}
```

**Enable RADVD on the external interface**. If the BIG-IP is the only router on the external interface, you have to use RADVD to enable stateless autoconfiguration of external hosts (this is probably only needed in a test environment). Modify the /etc/radvd.conf file to look like this (the important part is the IPv6 prefix advertised on the interface; obviously it has to match the **net self** definition from above).

``` code
interface external
{
        AdvSendAdvert on;
        IgnoreIfMissing on;
        MinRtrAdvInterval 3;
        MaxRtrAdvInterval 10;
        AdvDefaultPreference low;
        AdvHomeAgentFlag off;
        prefix fd00:dead:beef:1::/64
        {
                AdvOnLink on;
                AdvAutonomous on;
                AdvRouterAddr off;
        };
};
```

**Create new virtual server**. Yet again, I've used **edit** command in **tmsh** to get the definition of an existing virtual server, changed **modify virtual-server** into **create virtual-server**, changed virtual server's name and replaced its IPv4 address with an IPv6 address:

``` code
create ltm virtual webServerV6 {
    destination fd00:dead:beef:1::1.http
    ip-protocol tcp
    pool webPool
    profiles {
        oneconnect { }
        tcp { }
    }
    snat automap
}
```

{{<note info>}}You have to use **snat** or **snatpool** parameter when doing IPv6-to-IPv4 load balancing. If the expected number of client sessions is small, use **snat automap**. If you expect more than a few thousand concurrent sessions, use a SNAT pool.{{</note>}}

**Test the new virtual server**. If you're too lazy to modify your DNS server (like I was), point your browser to [http://\[fd00:dead:beef:1::1\]/](http://%5Bfd00:dead:beef:1::1%5D/). The *external* interface of my virtual BIG-IP is bridged to the Ethernet interface of my Linux host, so I was immediately able to connect to the IPv6 version of my web server from other hosts within my LAN (yeah, I'm still waiting for an IPv6 prefix from my DSL provider \... are you listening, [\@RagnarBelial?]{.screen-name}).
