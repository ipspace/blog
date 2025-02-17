---
title: "Cisco VRRPv3 IPv6 Configuration Sucks"
date: 2025-01-27 08:20:00+0100
tags: [ IP routing, netlab ]
netlab_tag: quirks
---
_I spent way too much time ironing out the VRRPv3 quirks on the [dozen (or so) platforms](https://netlab.tools/module/gateway/) supported by [netlab](https://netlab.tools/). This is the second blog post describing some of the ridiculous stuff I had to deal with._

This is how you configure the basic VRRPv3 parameters for IPv4 on a Cisco IOS/XE device:

{{<cc>}}VRRPv3 IPv4 configuration on Cisco IOS{{</cc>}}
```
interface GigabitEthernet0/1
  vrrp 217 address-family ipv4
    address 172.16.33.42
```

You would expect something similar for IPv6, right? You'd be right if you were working with Arista EOS:
<!--more-->
{{<cc>}}VRRPv3 IPv4 and IPv6 configuration on Arista EOS{{</cc>}}
```
interface Ethernet1
  vrrp 217 ipv4 version 3
  vrrp 217 ipv4 172.16.33.42
  vrrp 217 ipv6 2001:db8:cafe:33::2a
```

However, this is how Cisco IOS expects you to configure VRRPv3 for IPv6 (IOS XE and Nexus OS are no better):

{{<cc>}}VRRPv3 IPv6 configuration on Cisco IOS{{</cc>}}
```
interface GigabitEthernet0/1
  vrrp 217 address-family ipv6
    address fe80::200:5eff:fe00:02d9 primary
    address 2001:db8:cafe:33::2a/64
```

What's going on? Let's look into [RFC 9568](https://datatracker.ietf.org/doc/html/rfc9568):

* The *[definitions](https://datatracker.ietf.org/doc/html/rfc9568#name-definitions)* section defines *primary IP address* as "_the link-local address of the interface over which the packet is transmitted._"
* The [description of IP addresses in the VRRP packet](https://datatracker.ietf.org/doc/html/rfc9568#name-ipvx-addresses) is very explicit: "_For IPv6, the first address MUST be the IPv6 link-local address associated with the Virtual Router._"

To recap:

* An IPv6 VRRPv3 group **must** have a link-local address (LLA) and **might** have one or more global IPv6 addresses.
* The LLA **must** be the primary (first) IPv6 address.

This is how sane implementations deal with these requirements:

* The VRRP MAC address is derived from the VRRP group.
* The VRRP LLA is derived from the VRRP MAC address.
* The router allows you to configure *additional* IPv6 addresses. The prefix lengths attached to those IPv6 addresses are useless; they are not advertised in VRRPv3 (and should be /64 anyway).

And this is how the Cisco IOS or Nexus OS VRRPv3-for-IPv6 configuration works:

* You MUST configure the LLA manually and use the **primary** keyword. You cannot configure a global IPv6 address as the primary VRRPv3 address (they got this bit right).
* Don't try to cheat; VRRPv3 won't start without the **primary** LLA.
* You could configure any LLA as the primary VRRPv3 IPv6 address, but if you want to interoperate with non-Cisco devices, you SHOULD use the MAC-derived LLA.
* If you dream in hex, you'll have no problem figuring out the LLA.
* Everyone else should configure the global IPv6 address first, then do **show vrrp** to get the MAC address used with your VRRPv3 group. Finally, copy the last MAC address octet into the LLA from the above example.
* You can configure additional IPv6 addresses, but you have to specify the prefix length.

Other implementations I had to deal with are not much better; you have to specify the primary LLA manually on almost all of them. Junos and VyOS are exceptions, but Junos CLI police[^NX] managed to muddy the (templating) waters with AF-dependent keywords[^BP]:

[^BP]: Placing VRRP configuration within the IPv4/IPv6 address configuration is also pretty high on my list of *The Most Bizarre Things I've Seen*.

[^NX]: I made this up 😜, but they would need one. There were rumors Cisco had it in its early years, but it probably got disbanded way before the **class maps** and **policy maps** were implemented.

{{<cc>}}VRRPv3 IPv4 and IPv6 configuration on Junos{{</cc>}}
```
interfaces {
  et-0/0/0.0 {
    family inet {
      address 172.16.33.1/24 {
        vrrp-group 217 {
          virtual-address 172.16.33.42;
          priority 30;
        }
      }
    }
    family inet6 {
      address 2001:db8:cafe:33::1/64 {
        vrrp-inet6-group 217 {
          virtual-inet6-address 2001:db8:cafe:33::2a;
          priority 30;
        }
      }
    }
  }
}
```

Finally, an honorable mention for Dell OS10 happily ignoring the RFC 9568 requirements and starting VRRPv3 with a global IPv6 address as the primary VRRP address:

{{<cc>}}Invalid VRRPv3 configuration is accepted by Dell OS10{{</cc>}}
```
interface ethernet1/1/1
 vrrp-ipv6-group 217
  priority 30
  virtual-address 2001:db8:cafe:33::2a
```

{{<cc>}}VRRPv3 status on a misconfigured Dell OS10 device{{</cc>}}
```
dut# show vrrp ipv6 217

Interface       : ethernet1/1/1                           IPv6 VRID            : 217
Version         : 3                                       State                : active-state
Primary IP      : 2001:db8:cafe:33::2a                    Active IP            : fe80::a4f:a9ff:fe00:56
Virtual MAC     : 00:00:5e:00:02:d9                       Accept Mode          : true
Admin Priority  : 30                                      Operational Priority : 30
Advertise Interval(in centi secs) : 100
Preempt Status  : true                                    Hold Time            : 0
Virtual IP address :
2001:db8:cafe:33::2a
active-transitions        : 2                             advertise-rcvd            : 0
advertise-interval-errors : 0                             ip-ttl-errors             : 0
priority-zero-pkts-rcvd   : 0                             priority-zero-pkts-sent   : 1
invalid-type-pkts-rcvd    : 0                             address-list-errors       : 2
pkt-length-errors         : 0
omit-skew-time : no
```

Want more details? Jeff McLaughlin published an [interesting behind-the-scenes view of how the CLI sausage is made](https://subnetzero.info/2025/02/07/vrrp-why/)[^MN]

[^MN]: While also misspelling my name, but who's counting ;)

### Revision History

2025-02-12
: Added a link to Jeff McLaughlin's blog post
