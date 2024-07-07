---
date: 2012-01-19 10:44:00+01:00
tags:
- IPv6
title: IPv6 ND Managed-Config-Flag Is Just a Hint
url: /2012/01/ipv6-nd-managed-config-flag-is-just/
---
IPv6 hosts can use *stateless* or *stateful* autoconfiguration. [Stateless address autoconfiguration (SLAAC) uses IPv6 prefixes from Router Advertisement (RA) messages](/2011/10/ipv6-stateless-autoconfiguration-101/); stateful autoconfiguration uses DHCPv6. The routers can use two flags in RA messages to tell the attached end hosts which method to use:

-   Managed-Config-Flag tells the end-host to use DHCPv6 exclusively;
-   Other-Config-Flag tells the end-host to use [SLAAC to get IPv6 address and DHCPv6 to get other parameters](/2011/02/dhcpv6slaacra-dhcpv4/) (DNS server address, for example).
-   Absence of both flags tells the end-host to use only SLAAC.

One might assume that setting *managed-config-flag* in RA messages forces IPv6 hosts to use DHCPv6. Wrong, the two flags are just a polite suggestion.
<!--more-->
Let's start with the [IPv6 Node Requirements](http://tools.ietf.org/html/rfc4294) (RFC 4294). [Section 4.5](http://tools.ietf.org/html/rfc4294#section-4.5) is very explicit: SLAAC *must* be supported, DHCPv6 *may* be supported.

[RFC 4861](http://tools.ietf.org/html/rfc4861) (IPv6 Neighbor Discovery) uses similarly non-committal language in [Section 4.2](http://tools.ietf.org/html/rfc4861#section-4.2): M flag indicates *addresses are available DHCPv6*, nothing more.

Can you enforce the use of DHCPv6 in case you want to track end-user IPv6 addresses for security/accountability reasons? Sure you can (there's a workaround for every networking challenge caused by bad design or misguided expectations) -- if you don't advertise on-link prefixes in router advertisement messages, the hosts cannot auto-generate IPv6 addresses and are forced to use DHCPv6, or stay forever isolated from the beauties of IPv6-only Internet.

To do that on Cisco IOS, configure IPv6 prefix on the LAN interface and disable its propagation with the **ipv6 nd prefix no-advertise** interface configuration command. You need the IPv6 prefix configured on the LAN interface because Cisco IOS DHCPv6 server does not create host routes toward its clients and thus cannot reach the directly-attached hosts without an explicitly configured IPv6 prefix.

{{<cc>}}Enforce DHCPv6-only address configuration in Cisco IOS{{</cc>}}
```
interface FastEthernet0/0.100
 description Host Access LAN (VLAN 100)
 encapsulation dot1Q 100
 ipv6 address FEC0:1:2300:1::1/64
 ipv6 nd prefix FEC0:1:2300:1::/64 no-advertise
 ipv6 nd managed-config-flag
 ipv6 nd router-preference High
 ipv6 dhcp server VLAN_100
```

## More information

Many more IPv6 access network hints are described in the [*Building Large IPv6 Service Provider Networks*](https://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks) webinar.