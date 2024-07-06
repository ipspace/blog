---
cdate: 2023-03-10
comment: 'It seems the engineers who have to deal with this kind of scenarios reached
  a reluctant consensus since I wrote this blog post more than a decade ago: NAT66
  or NPT66 is the way to go. For obvious reasons, that conclusion will never make
  it past IETF IPv6 True Believers.

  '
date: 2011-12-13 06:29:00+01:00
high-availability_tag: multihoming
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
- NAT
- Internet
- high availability
title: 'IPv6 Multihoming Without NAT: the Problem'
url: /2011/12/ipv6-multihoming-without-nat-problem.html
---
Every time I write about [IPv6 multihoming issues](/2010/12/small-site-multihoming-in-ipv6-mission.html) and the [need for NPT66](/2011/12/we-just-might-need-nat66.html), I get a comment or two saying:

> But I thought this is already part of IPv6 stack -- can't you have two or more IPv6 addresses on the same interface?

The commentators are right, you can have multiple IPv6 addresses on the same interface; the problem is: which one do you choose for outgoing sessions.

The source address selection rules are specified in [RFC 3484](http://tools.ietf.org/html/rfc3484) (Greg translated that RFC into an [easy-to-consume format](http://etherealmind.com/ipv6-which-address-multiple-ipv6-address-default-address-selection/) a while ago), but they are not very helpful as they cannot be influenced by the CPE router. Let's look at the details.
<!--more-->
### Phase 1 -- Single ISP Connection

We have a simple SMB network: a single CPE router connected to one ISP and a host sitting behind the router (ignore the PE-B part for the moment). CPE router asks ISPA for a delegated prefix (using IA_PD option in DHCPv6) and uses part of that prefix to address its LAN interface.

{{<figure src="/2011/12/s1600-IPv6MH_PD1.png" caption="CPE router with a single active IPv6 connection">}}

This is how you configure the CPE router if you're using Cisco IOS:

{{<cc>}}Simple CPE router configuration{{</cc>}}
```
ipv6 unicast-routing
!
interface FastEthernet0/0
 description Inside interface
 ipv6 address ISPA ::1/64
 ipv6 nd router-preference High
 ipv6 nd ra interval 10
!
interface FastEthernet1/0
 description ISP A uplink
 ipv6 address autoconfig default
 ipv6 dhcp client pd ISPA
```

The CPE router configuration is not complete; you would also need DHCPv6 server on the inside interface to pass DNS server IPv6 address to the clients. A complete (and tested) configuration is included in the materials you get with the [Building IPv6 Service Provider Core](http://www.ipspace.net/Building_IPv6_Service_Provider_Core) webinar.

The IPv6 client receives RA messages sent by the CPE and creates an IPv6 address from the advertised /64 prefix on its LAN interface:

{{<figure src="/2011/12/s1600-IPv6MH_RA1.png" caption="Delegated IPv6 prefix is propagated to the clients">}}

The client is now able to communicate with the IPv6 Internet. Problem solved \... until someone figures out a single upstream connection is a single point of failure and orders a second Internet service.

### Phase 2 -- Two ISP Uplinks

The second ISP uplink is configured almost identically to the first. Since you cannot have two RA-generated default routes in Cisco IOS release 15.1M, I had to use a floating static default route and hard-code the next-hop router's IPv6 address in it.

{{<cc>}}Simple CPE router configuration -- two uplinks{{</cc>}}
```
ipv6 unicast-routing
!
interface FastEthernet0/0
 description Inside interface
 ipv6 address ISPA ::1/64
 ipv6 address ISPB ::1/64
 ipv6 nd router-preference High
 ipv6 nd ra interval 10
!
interface FastEthernet1/0
 description ISP A uplink
 ipv6 address autoconfig default
 ipv6 dhcp client pd ISPA
!
interface FastEthernet1/1
 description ISP B uplink
 ipv6 address autoconfig
 ipv6 dhcp client pd ISPB
!
ipv6 route ::/0 FastEthernet1/1 FE80::2 30
```

After the CPE router receives a delegated prefix from PE-B, it adds a /64 prefix from that address range to its LAN interface and starts advertising two /64 prefixes (one from each ISP) in its RA messages. The IPv6 client creates a second IPv6 address from the second advertised prefix -- it now has two IPv6 addresses on its LAN interface.

{{<figure src="/2011/12/s1600-IPv6MH_2.png" caption="Two prefixes are advertised to LAN clients">}}

### The Problem

There are numerous problems associated with this setup, some of them architectural, many more due to suboptimal implementations, omissions, or strict adherence to RFCs in host and router stacks.

The easy one first: when an IPv6 client with multiple IPv6 addresses starts a new session, it chooses a source address that best matches the destination address (ULA address for ULA destination, global address for global destination \...) without any knowledge of the network topology.

_Distributing Address Selection Policy using DHCPv6_ ([RFC 7078](https://tools.ietf.org/html/rfc7078)) describes a potential solution \... but it has to be implemented in both routers and hosts, and I'm not aware of a production implementation at this moment.

For example, when the IPv6 client in our small network connects to the outside world, it might choose a source IPv6 address assigned by the wrong ISP.

You can see the source address used by the client with the **netstat -n -p tcpv6** (Windows) or **netstat -n -f inet6 -p tcp** (Linux/OSX) command. It seems that Windows picks the lowest IPv6 address while OSX picks the oldest IPv6 address when all interface IPv6 addresses are equivalent according to RFC 3484 rules.

The best that could happen is asymmetrical routing:

{{<figure src="/2011/12/s1600-IPv6MH_Asym.png" caption="Asymmetrical routing">}}

In some rare cases, the ISP actually performs RPF check and drops the packet with an unexpected source IPv6 address.

{{<figure src="/2011/12/s1600-IPv6MH_RPF.png" caption="RPF check on PE-router drops client traffic">}}

The whole situation might have been survivable were this the only problem to solve (and the lack of RPF checks on the ISP side causes people to claim that IPv6 multihoming works). Unfortunately, there are many others, for example:

-   When the CPE router (Cisco IOS router running 15.1(4)M) loses an uplink, it does not stop advertising the delegated prefix it received through that uplink (implementation issue). One of the client IPv6 addresses is thus completely invalid without client being aware of it.
-   If you clear the delegated prefix manually (or with an EEM applet) on the CPE router, it stops advertising the prefix in its RA messages \... but the prefix remains valid on the IPv6 hosts until it expires (architectural issue). Prefix expiration is based on its *preferred lifetime*, which is derived straight from DHCPv6 prefix delegation and is usually measured in weeks.
-   It might be possible to reduce the *preferred lifetime* in the RA messages to a very low number, but the lifetime of an interface prefix based on a delegated prefix is not configurable (implementation issue).

Please don't try to tell me that the whole thing works if you use two CPE routers. It might work once the [host stacks implement RFC 3484 bis](http://tools.ietf.org/html/draft-ietf-6man-rfc3484-revise-03#section-2.3), but we're not there yet (and I'll describe that scenario in an upcoming blog post).

### More Information and Tested Router Configurations

Various IPv6 access- and core network designs and numerous sample configurations are included in the [Building Large IPv6 Service Provider Networks](http://www.ipspace.net/Building_IPv6_Service_Provider_Core) webinar.

### Do Your Own Tests

If you want to test how your hosts behave in this scenario or try to fix my router configurations, use these configurations as a starting point:

{{<cc>}}CPE router configuration (cleaned up){{</cc>}}
```
version 15.1
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname CPE
!
ipv6 unicast-routing
ipv6 cef
!
interface FastEthernet0/0
 description Inside interface
 ipv6 address ISPA ::1/64
 ipv6 address ISPB ::1/64
 ipv6 nd router-preference High
 ipv6 nd ra interval 10
!
interface FastEthernet1/0
 description ISP A uplink
 ipv6 address autoconfig default
 ipv6 dhcp client pd ISPA
!
interface FastEthernet1/1
 description ISP B uplink
 ipv6 address autoconfig
 ipv6 dhcp client pd ISPB
!
ipv6 route ::/0 FastEthernet1/1 FE80::2 30
!
line con 0
 exec-timeout 0 0
 privilege level 15
line vty 0 4
 exec-timeout 0 0
 privilege level 15
 no login
!
ntp logging
end
```

{{<cc>}}PE-router configuration (cleaned up){{</cc>}}
```
hostname PE
!
ipv6 unicast-routing
ipv6 cef
ipv6 dhcp pool ISPA
 prefix-delegation pool ISPA
!
ipv6 dhcp pool ISPB
 prefix-delegation pool ISPB
!
interface Loopback0
 ipv6 address 2001:DB8:CAFE::1/64
!
interface FastEthernet0/0
 description ISP A interface
 ipv6 address FE80::1 link-local
 ipv6 address 2001:DB8:1:FF01::1/64
 ipv6 dhcp server ISPA
!
interface FastEthernet0/1
 description ISP B interface
 ipv6 address FE80::2 link-local
 ipv6 address 2001:DB8:7:FF01::1/64
 ipv6 dhcp server ISPB
!
ipv6 local pool ISPA 2001:DB8:1::/49 60
ipv6 local pool ISPB 2001:DB8:7::/49 60
!
line con 0
 exec-timeout 0 0
 privilege level 15
line vty 0 4
 exec-timeout 0 0
 privilege level 15
 no login
!
ntp logging
end
```
