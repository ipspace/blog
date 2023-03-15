---
date: 2023-03-20 07:15:00+00:00
netlab_tag: use
series_title: VRF-Aware DHCP Relaying Lab
tags: [ DHCP, netlab, IP routing ]
title: Test VRF-Aware DHCP Relaying with netlab
pre_scroll: True
series: [ dhcp-relay ]
---
After [figuring out how DHCP relaying works](/2023/03/dhcp-relay-process.html) and [testing it in a simple lab](/2023/03/netlab-dhcp-relay.html), I went a step further and tested VRF-aware DHCP relaying.

### Lab Topology

I had to make just a few changes to the [DHCP relaying lab topology](https://github.com/ipspace/netlab-examples/blob/master/DHCP/relay/topology.yml):

* DHCP server is running on CSR 1000v. IOSv DHCP server does not support subnet selection DHCP option and thus doesn't work with relays that do inter-VRF DHCP relaying.
* I put the link between the DHCP client and DHCP relay into a VRF. 
<!--more-->
{{<cc>}}Changes in lab topology{{</cc>}}
```
groups:
  switch:
    members: [ relay ]
    module: [ ospf,vrf ]

vrfs:
  client:

links:
- user:
    dhcp.client: True
  relay:
    dhcp.server: srv
  type: lan
  vrf: client
```

{{<figure src="/2023/03/vrf-dhcp-relay.png" caption="Lab topology diagram">}}

{{<cc>}}Lab IPv4 addressing{{</cc>}}
```
  Interface                  IPv4 address  Description
================================================================================
srv (10.0.0.1/32)
  GigabitEthernet2            10.1.0.2/30  srv -> relay

relay (10.0.0.2/32)
  GigabitEthernet0/1          10.1.0.1/30  relay -> srv
  GigabitEthernet0/2        172.16.0.2/24  relay -> user (VRF: client)

user (10.0.0.3/32)
  GigabitEthernet0/1        172.16.0.3/24  user -> relay
```

You can [view the complete topology file on GitHub](https://github.com/ipspace/netlab-examples/blob/master/DHCP/vrf-relay/topology.yml).

### Device Configurations

I configured VRF-aware DHCP relay (**ip dhcp relay information option vpn**) and VRF-aware DHCP pools (use **vrf** option in **ip dhcp pool**). The [final device configurations](https://github.com/ipspace/netlab-examples/tree/master/DHCP/vrf-relay/config) (with Cisco IOSv as DHCP relay) are available in [netlab-examples GitHub repository](https://github.com/ipspace/netlab-examples).

{{<cc>}}Cisco IOS VRF-aware DHCP relay configuration{{</cc>}}
```
ip dhcp relay information option vpn
!
interface GigabitEthernet0/2
 ip helper-address global 10.0.0.1
```

{{<cc>}}Cisco IOS VRF-aware DHCP server configuration{{</cc>}}
```
ip dhcp excluded-address vrf client 172.16.0.2
!
ip dhcp pool p_172.16.0.0
 vrf client
 network 172.16.0.0 255.255.255.0
 default-router 172.16.0.2
```

### Does It Work?

It does... once I figured out IOSv DHCP server doesn't work well with inter-VRF DHCP relaying and switched to CSR 1000v[^ST]. Let's go into some of the interesting (cleaned up) debugging printouts on the DHCP server. Full [client](https://github.com/ipspace/netlab-examples/blob/master/DHCP/vrf-relay/config/user.log) and [server](https://github.com/ipspace/netlab-examples/blob/master/DHCP/vrf-relay/config/srv.log) logs are [available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/DHCP/vrf-relay).

[^ST]: My stubbornness wasted a few hours of my life :(

{{<cc>}}Debugging printout of DHCP server discovery{{</cc>}}
```
DHCPD: tableid for 10.1.0.2 on GigabitEthernet2 is 0
DHCPD: found subnet_info_addr 172.16.0.0
DHCPD: Giaddr from server-id-override suboption 172.16.0.2
DHCPD: client's VPN is client.
DHCPD: DHCPDISCOVER received from client 0063.6973.636f.2d35.3235.342e.3030.3539.2e64.6664.352d.4769.302f.31 through relay 10.1.0.1.
DHCPD: using server-id-override 172.16.0.2
DHCPD: Option 125 not present in the msg.
DHCPD: egress Interfce GigabitEthernet2
DHCPD: unicasting BOOTREPLY for client 5254.0059.dfd5 to relay 10.1.0.1.
```

Here's what's going on behind the scenes.

DHCP relay:

* Specified its global IPv4 address (10.1.0.1) as the relay IPv4 address (**giaddr**)
* Used link selection sub-option (option 82 sub-option 5, defined in [RFC 3527](https://www.rfc-editor.org/rfc/rfc3527.html)) to pass the information about the VRF IP subnet in which the client resides.
* Included client VPN information (option 82 sub-option 150, defined in [RFC 6607](https://www.rfc-editor.org/rfc/rfc6607.html))
* Set the desired server ID to its VRF IP address (option 82 sub-option 11, defined in [RFC 5107](https://www.rfc-editor.org/rfc/rfc5107.html))

DHCP server therefore assigned an IP address from 172.16.0.0 pool to the client, set the server ID to 172.16.0.2, and sent the reply to 10.1.0.1. Similar processing happens for all subsequent packets.

Let's also check the client lease:

{{<cc>}}DHCP lease on the DHCP client{{</cc>}}
```
user#show dhcp lease
...
Temp IP addr: 172.16.0.4  for peer on Interface: GigabitEthernet0/1
Temp  sub net mask: 255.255.255.0
   DHCP Lease server: 172.16.0.2, state: 5 Bound
   DHCP transaction id: 2030
   Lease: 86400 secs,  Renewal: 43200 secs,  Rebind: 75600 secs
   Next timer fires after: 11:36:39
   Retry count: 0   Client-ID: cisco-5254.0059.dfd5-Gi0/1
   Client-ID hex dump: 636973636F2D353235342E303035392E
                       646664352D4769302F31
   Hostname: user
```

As expected, the DHCP server IP address is the VRF IP address of the DHCP relay. All subsequent DHCP packets are thus sent to the DHCP relay and not directly to the DHCP server.

### Vendor Interoperability Is Fun

I tried to test a combination of Arista vEOS DHCP relay (4.28.3M) and Cisco CSR DHCP server.

{{<cc>}}Arista vEOS VRF-aware DHCP relay configuration{{</cc>}}
```
ip dhcp relay information option
!
interface Ethernet2
 ip helper-address 10.0.0.1 vrf default
```

It didn't work until I removed the **vrf** definition from the DHCP pool -- here's the relevant part of Cisco IOS XE debugging printout:

```
DHCPD: Bad VPN information type: 99.
DHCPD: client's VPN is .
```

According to RFC 6607, the VPN selection sub-option (sub-option 151) starts with [Virtual Subnet Selection Type](https://www.rfc-editor.org/rfc/rfc6607.html#section-3.5) (a binary zero for VRF name), and that's what Cisco IOS XE expects.

Arista EOS 4.29.1F documentation (section 13.1.9 -- DHCP Relay Across VRF) claims that the value of sub-option 151 created by EOS contains just the VPN name (without the intervening binary zero meaning "what follows is the VPN name"). Faced with `client` as the value of sub-option 151, Cisco IOS understands the VSS Type to be 99 (ASCII value of `c`), which is invalid. The DHCP server on CSR 1000v thus ignores sub-option 151.

### Takeaways

* Inter-VRF DHCP relaying is complex -- it's trying to make a simple protocol do things it was never designed to do. We'll get back to the fun implications of this Rube Goldberg stack of kludges when we get to redundant designs.
* Two or three sub-options of option-82 are involved in inter-VRF DHCP relaying, and DHCP relays and servers have to support them perfectly for the whole thing to work.
* In particular, the DHCP relay and DHCP server MUST support *server identifier override* sub-options of option 82 and MUST  support the same way of identifying the client subnet.
* There are at least two ways of specifying the client subnet in DHCP -- *link selection* sub-option of option 82 and *subnet selection option* (option 118). In the ideal world, all relay agents and servers would use *link selection* sub-option -- after all, it was designed to be used in DHCP relaying scenarios. I wouldn't be surprised if the networking vendors fail to reach that level of consistency.
* *Virtual Subnet Selection Suboption* (option 151) it not needed for inter-VRF DHCP relaying, but is required to implement multi-tenant DHCP with overlapping address pools. At least one vendor implemented it incorrectly.

I'm positive that you've experienced your share of horror stories on other platforms. Please share them in the comments!

### Reference: Configuration Templates

I had to make the DHCP relay and DHCP server configuration templates VRF-aware to make this lab work.

DHCP relay has to use the **global** parameter of the **ip helper-address**. It also has to be configured to insert VPN sub-option into Relay Agent DHCP option (**ip dhcp relay information option vpn**):

{{<cc>}}DHCP relay configuration template{{</cc>}}
```
{% for intf in interfaces if intf.dhcp.server is defined and intf.vrf is defined %}
{%   if loop.first %}
ip dhcp relay information option vpn
{%   endif %}
{% endfor %}
!
{% for intf in interfaces if intf.dhcp.server is defined %}
{%   set helper = hostvars[intf.dhcp.server].loopback.ipv4|ipaddr('address') %}
interface {{ intf.ifname }}
{%   if intf.vrf is defined %}
 ip helper-address global {{ helper }}
{%   else %}
 ip helper-address {{ helper }}
{%   endif %}
{% endfor %}
```

All I had to do in the DHCP server template was to add the **vrf** option to **ip dhcp excluded-address** and **ip dhcp pool** configuration commands:

{{<cc>}}DHCP relay server template{{</cc>}}
```
logging buffered
no service timestamp debug
!
do debug ip dhcp server packet
do debug ip dhcp server event
!
{% for h,v in hostvars.items() %}
{%   for intf in v.interfaces if intf.dhcp.server is defined and intf.ipv4 is defined %}
ip dhcp excluded-address {% if intf.vrf is defined %}vrf {{ intf.vrf }} {% endif %}{{ intf.ipv4|ipaddr('address') }}
{%   endfor %}
{% endfor %}
!
{% for h,v in hostvars.items() %}
{%   for intf in v.interfaces if intf.dhcp.server is defined and intf.ipv4 is defined %}
!
ip dhcp pool p_{{ intf.ipv4|ipaddr('network') }}
{%     if intf.vrf is defined %}
 vrf {{ intf.vrf }}
{%     endif %}
 network {{ intf.ipv4|ipaddr('network') }} {{ intf.ipv4|ipaddr('netmask') }} 
 default-router {{ intf.ipv4|ipaddr('address') }}
{%   endfor %}
{% endfor %}
```

You can [download the configuration templates from GitHub](https://github.com/ipspace/netlab-examples/tree/master/DHCP/vrf-relay); 

### Try It Out!

Want to run this lab on your own, or try it out with different devices? No problem:

* Make sure your preferred device supports DHCP relaying
* [Install netlab](https://netsim-tools.readthedocs.io/en/latest/install.html)
* [Download the relevant containers](https://netsim-tools.readthedocs.io/en/latest/labs/clab.html) or [create Vagrant boxes](https://netsim-tools.readthedocs.io/en/latest/labs/libvirt.html)
* Download the [VRF-aware DHCP relaying example](https://github.com/ipspace/netlab-examples/tree/master/DHCP/vrf-relay) into an empty directory
* If you want to use a relaying device that's not Cisco IOS or Arista EOS, add a configuration template to `dhcp-relay` subdirectory.
* Execute **netlab up**
* Enjoy! 😊

{{<next-in-series page="/posts/2023/03/netlab-vxlan-dhcp-relay.md">}}
### Coming Up Next

So far so good: simple DHCP relaying works, as does (with a few quirks) inter-VRF DHCP relaying. Will they still work in VXLAN segments? That's the topic of the next blog post in this series.{{</next-in-series>}}
