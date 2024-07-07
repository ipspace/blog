---
date: 2012-01-21 13:52:00.001000+01:00
tags:
- DHCP
- IPv6
- PPP
title: DHCPv6 Prefix Delegation with Radius Works in IOS Release 15.1
url: /2012/01/dhcpv6-prefix-delegation-with-radius/
---
A while ago I described the [pre-standard way Cisco IOS used to get delegated IPv6 prefixes from a RADIUS server](/2011/03/dhcpv6-radius-integration-cisco-way/). Cisco's documentation [always claimed](http://www.cisco.com/en/US/prod/collateral/iosswrel/ps8802/ps6968/ps6350/prod_bulletin0900aecd802eaa4f.html) that Cisco IOS implements [RFC 4818](http://tools.ietf.org/html/rfc4818), but you simply couldn't get it to work in IOS releases 12.4T or 15.0M. In December I wrote about the [progress Cisco is making on the DHCPv6 front](/2011/12/dhcpv6-server-on-cisco-ios-making/) and *iord\@intracom.com* commented that IOS 15.1S does support RFC 4818. You know I absolutely had to test that claim \... and it's true!
<!--more-->
This is the configuration you can use on the PE-router:

``` {.code}
aaa authorization configuration IA_PD group radius
!
ipv6 dhcp pool PPP-Radius
 prefix-delegation aaa method-list IA_PD lifetime 7200 300
 dns-server FEC0::CCCC:4
 domain-name example.com
!
interface Virtual-Template10
 mtu 1480
 no ip address
 ipv6 enable
 ipv6 nd other-config-flag
 no ipv6 nd ra suppress
 ipv6 dhcp server PPP-Radius
```

And this is the FreeRADIUS user definition:

``` {.code}
Site-A  Cleartext-Password := "Site-A"
        Service-Type = Framed-User,
        Framed-Protocol = PPP,
        Framed-IPv6-Prefix = "fec0:1:2400:1::/64",
        Delegated-IPv6-Prefix = "fec0:1:2400:1100::/56"
```

Cisco IOS release 15.1(3)S that I used in the tests also supports a fallback mechanism:

-   The value of the *Delegated-IPv6-Prefix* from the RADIUS reply is saved in a per-interface DHCPv6 block;
-   When the PPPoE client uses DHCPv6 to get a delegated prefix, PE-router checks the pre-populated DHCPv6 reply associated with the incoming interface. If the delegated prefix is already in there, it returns the reply without querying the RADIUS server;
-   If the delegated IPv6 prefix is not yet available, the PE-router uses the pre-standard method and sends [another RADIUS request for the *user-*dhcpv6 username](/2011/03/dhcpv6-radius-integration-cisco-way/).

According to Cisco's documentation, you get the same functionality (RFC 4818 support) in IOS XE release 3S.

## More information

You'll get more IPv6 access network design and configuration guidelines in [*Building Large IPv6 Service Provider Networks*](http://www.ipspace.net/IPv6SPCore) webinar.
