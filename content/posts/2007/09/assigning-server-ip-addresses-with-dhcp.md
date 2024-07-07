---
date: 2007-09-19 07:56:00.001000+02:00
tags:
- DHCP
title: Assigning Server IP addresses with DHCP
url: /2007/09/assigning-server-ip-addresses-with-dhcp/
---
Using DHCP to assign server IP addresses is usually not a wise decision. To start with, you have to define static DHCP mappings, which rely on client-id attribute in the DHCP request (usually the MAC address of the client). For me, the easiest way to find the correct client ID is as follows:

-   Use DHCP to assign the IP address to the server
-   Note the newly assigned IP address
-   Use the **show ip dhcp bindings \| include *ip-address*** command to display the client-id to IP address binding.
-   Create a static DHCP mapping (for example, by configuring a **host** DHCP pool on the router) and release/renew IP address on the server
<!--more-->
Of course, if the Ethernet adapter in the server is replaced, the static mapping stops working. The only reliable workaround I\'ve found so far is to assign a locally-administered MAC address to the server\'s LAN adapter (if anyone has figured out a way to assign ASCII client-ID to a Windows server, let me know). To do it on Windows XP, use the Advanced properties in the adapter configuration window.

{{<figure src="/2007/09/LanAdapter.jpg">}}

**Remember**: locally administered MAC addresses on Ethernet networks start with 02xx. More precisely, second bit in first byte must be set, thus 02 in the previous sentence. AA00-0000-0001 is also a locally administered MAC address.

After you\'ve configured MAC address on the server, prepend 01 to it and insert a dot after every fourth character to get the client-ID you need to enter on the DHCP server. For example, the MAC address 0200.1000.1234 becomes client-id 0102.0010.0012.34, and the static DHCP pool on a router is configured as follows:

``` {.code}
ip dhcp pool Server_static
host 10.0.0.10 255.255.255.0
client-identifier 0102.0010.0012.34
```
