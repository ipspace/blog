---
date: 2011-02-21 07:04:00.002000+01:00
tags:
- IPv6
title: DHCPv6+SLAAC+RA = DHCPv4
url: /2011/02/dhcpv6slaacra-dhcpv4.html
---
We all know that [IPv6 handles host network parameter initialization a bit different than IPv4](/2010/06/ipv6-autoconfiguration-too-many-cooks.html) (where we usually use DHCP), but the details could still confuse you if you're just entering the IPv6 world.

A typical LAN-attached hosts needs its own address as well as the addresses of the default router and DNS server. DHCPv4 provides all three; in the IPv6 world you need two or three protocols as summarized in the following table
<!--more-->

| Parameter      | DHCPv4 | DHCPv6[^A] | SLAAC[^1] | RA[^2] |
| -------------- | :----: | :----: | :-------: | :----: |
| Host address   | ✅     | ✅ [^3]| ✅        | ❌      |
| Default router | ✅     | ❌      |           | ✅     |
| DNS server     | ✅     | ✅     |           | ✅ [^4]|
| DNS search list| ✅     | ✅     |           | ✅ [^4]| 
{.fmtTable}

[^A]: As of January 2023, DHCPv6 is still not supported on Android due to [obstinate opinions of a few individuals](/2021/10/dhcpv6-matters.html).
[^1]: SLAAC (RFC 2462) uses RA to get IPv6 prefix information for the local subnet.
[^2]: Router Advertisements (RA) are part of ICMPv6 (RFC 4443).
[^3]: While it might be desirable to retain control over IPv6 address allocation with IPv6, it's better to use SLAAC with privacy extensions (RFC 4941), otherwise the web servers throughout the Internet can track your end-users based on their IPv6 addresses.
[^4]: You might want to check whether [*IPv6 RA options for DNS configuration*](https://tools.ietf.org/html/rfc6106) (RFC 6106) is [implemented in your operating system(s)](https://en.wikipedia.org/wiki/Comparison_of_IPv6_support_in_operating_systems).

This is how I would set up a typical IPv6 subnet:

-   Unless you want to have tight control over host IPv6 addresses, **deploy DHCPv6 servers on the routers** without associated IPv6 address pools. DHCPv6 should be used just to pass the DNS information to the hosts;
-   **Enable RA on all LAN interfaces**. If your LAN switches support RA guard, you should enable it to prevent RA spoofing and MITM attacks. RA is enabled by default on most LAN interfaces (but check BVI, SVI and wireless interfaces).
-   **Use RA RDNSS option** whenever possible, making sure even broken operating systems without DHCPv6 support get IPv6 DNS information.
-   **Use SLAAC with privacy extensions**. RA is enabled, so SLAAC works; use of privacy extensions has to be configured on the host (it's enabled by default on most modern operating systems).
-   **Use DNS server that supports dynamic host registration**. Dynamically-assigned (and frequently changing) IPv6 addresses can turn your troubleshooting efforts into a nightmare. If the IPv6 hosts register their addresses with your DNS server, you'll have at least a fighting change.
