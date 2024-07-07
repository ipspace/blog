---
date: 2007-11-28 06:54:00+01:00
tags:
- DNS
- PPP
- WAN
title: Configure DNS Servers Through IPCP
url: /2007/11/configure-dns-servers-through-ipcp/
---
After I\'ve fixed the default routing in my home office, I\'ve stumbled across another problem: the two ISPs I\'m using for my primary and backup link have DNS servers that reply solely to the DNS requests sent from their own IP address range:

{{<figure src="/2007/11/homeSetupDNS.jpg">}}

When the traffic is switched from the primary to the backup ISP, I therefore also need to switch the DNS servers. Fortunately, this is quite easy to do on a router; you just need to configure **ppp ipcp dns request** on the dialer interface and the router starts asking for the DNS server address as part of the IPCP negotiation.
<!--more-->
The negotiation process can be debugged with the **debug ppp negotiation** command; it\'s a bit more complex than usual in my case since the access server has no secondary DNS (only the primary DNS is configured):

``` {.code}
Se1/0 IPCP: O CONFREQ [Closed] id 1 len 22
Se1/0 IPCP:    Address 0.0.0.0 (0x030600000000)
Se1/0 IPCP:    PrimaryDNS 0.0.0.0 (0x810600000000)
Se1/0 IPCP:    SecondaryDNS 0.0.0.0 (0x830600000000)
Se1/0 PPP: Process pending ncp packets
Se1/0 IPCP: Redirect packet to Se1/0
Se1/0 IPCP: I CONFREQ [REQsent] id 1 len 10
Se1/0 IPCP:    Address 10.0.0.33 (0x03060A000021)
Se1/0 IPCP: O CONFACK [REQsent] id 1 len 10
Se1/0 IPCP:    Address 10.0.0.33 (0x03060A000021)
Se1/0 IPCP: I CONFREJ [ACKsent] id 1 len 10
Se1/0 IPCP:    SecondaryDNS 0.0.0.0 (0x830600000000)
Se1/0 IPCP: O CONFREQ [ACKsent] id 2 len 16
Se1/0 IPCP:    Address 0.0.0.0 (0x030600000000)
Se1/0 IPCP:    PrimaryDNS 0.0.0.0 (0x810600000000)
Se1/0 IPCP: I CONFNAK [ACKsent] id 2 len 16
Se1/0 IPCP:    Address 10.0.0.34 (0x03060A000022)
Se1/0 IPCP:    PrimaryDNS 10.0.0.10 (0x81060A00000A)
Se1/0 IPCP: O CONFREQ [ACKsent] id 3 len 16
Se1/0 IPCP:    Address 10.0.0.34 (0x03060A000022)
Se1/0 IPCP:    PrimaryDNS 10.0.0.10 (0x81060A00000A)
Se1/0 IPCP: I CONFACK [ACKsent] id 3 len 16
Se1/0 IPCP:    Address 10.0.0.34 (0x03060A000022)
Se1/0 IPCP:    PrimaryDNS 10.0.0.10 (0x81060A00000A)
Se1/0 IPCP: State is Open
```

The results can be inspected only with the show host command:

``` {.code}
GW#show host
Default domain is not set
Name/address lookup uses domain service
Name servers are 10.0.0.10
```

The access server receiving the call requires no special configuration; the first IP address configured with the **ip name-server** command is used as the primary DNS and the second one as the secondary. Alternatively, you can configure a different set of DNS servers to pass to the client with the **ppp ipcp dns *primary-DNS-address secondary-DNS-address*** interface configuration command.

Unfortunately, the integration with LAN clients is not [as seamless as with DHCP](/2007/08/import-dhcp-options-from-upstream-dhcp/); to make the whole solution work, you have to configure the router as a forwarding DNS server and make the LAN clients use the router as the default gateway and DNS server with the DHCP pool configuration:

``` {.code}
ip dns server
!
ip dhcp pool LAN
   import all
   network 192.168.0.0 255.255.255.240
   default-router 192.168.0.1
   dns-server 192.168.0.1
```
