---
date: 2023-03-27 07:15:00+00:00
netlab_tag: use
series_title: DHCP Relaying in VXLAN Segments
tags: [ netlab, IP routing, DHCP, VXLAN ]
title: DHCP Relaying in VXLAN Segments
pre_scroll: True
series: [ dhcp-relay ]
---
After I got the testing infrastructure in place ([simple DHCP relay](/2023/03/netlab-dhcp-relay/), [VRF-aware DHCP relay](/2023/03/netlab-vrf-dhcp-relay/)), I was ready for the real fun: DHCP relaying in VXLAN (and later EVPN) segments.

**TL&DR:** It works exactly as expected. Even though I had anycast gateway configured on the VLAN, the Arista vEOS switches  used their unicast IP addresses in the DHCP relaying process. The DHCP server had absolutely no problem dealing with multiple copies of the same DHCP broadcast relayed by different switches attached to the same VLAN. One could only wish things were always as easy in the networking land.
<!--more-->
### Lab Topology

The lab is a bit bigger than the original [DHCP relaying lab](https://github.com/ipspace/netlab-examples/blob/master/DHCP/relay/):

* The network core has three nodes connected in a triangle: two switches and a router running DHCP server.
* Two DHCP clients are connected to the same client VLAN (VLAN 1000)
* Two Arista vEOS switches use VXLAN to extend the client VLAN across the network core.
* Arista switches are doing DHCP relaying toward the DHCP server in the network core.
<!--more-->

{{<figure src="/2023/03/vxlan-dhcp-relay.png" caption="Lab topology diagram">}}

{{<cc>}}Lab IPv4 addressing{{</cc>}}
```
  Interface                  IPv4 address  Description
================================================================================
srv (10.0.0.2/32)
  GigabitEthernet0/1          10.1.0.1/30  srv -> sw1
  GigabitEthernet0/2          10.1.0.5/30  srv -> sw2

sw1 (10.0.0.3/32)
  Ethernet1                   10.1.0.2/30  sw1 -> srv
  Ethernet2                   10.1.0.9/30  sw1 -> sw2
  Vlan1000                  172.16.0.3/24  VLAN client (1000) -> [cl_a,cl_b,sw2]

sw2 (10.0.0.4/32)
  Ethernet1                   10.1.0.6/30  sw2 -> srv
  Ethernet2                  10.1.0.10/30  sw2 -> sw1
  Vlan1000                  172.16.0.4/24  VLAN client (1000) -> [cl_a,sw1,cl_b]

cl_a (10.0.0.5/32)
  GigabitEthernet0/1        172.16.0.5/24  cl_a -> [sw1,cl_b,sw2]

cl_b (10.0.0.6/32)
  GigabitEthernet0/1        172.16.0.6/24  cl_b -> [cl_a,sw1,sw2]
```

You can [view the complete topology file on GitHub](https://github.com/ipspace/netlab-examples/blob/master/DHCP/vxlan-relay/topology.yml).

### Device Configurations

In addition to IP addressing, VLAN, VXLAN, and OSPF configuration I configured anycast gateways and simple DHCP relay on the Arista switches, and a DHCP pool on the Cisco IOSv router. The [final device configurations](https://github.com/ipspace/netlab-examples/tree/master/DHCP/vxlan-relay/config) are available in [netlab-examples GitHub repository](https://github.com/ipspace/netlab-examples).

{{<cc>}}Arista vEOS VLAN/VXLAN DHCP relay configuration{{</cc>}}
```
vlan 1000
   name client
!
interface Vlan1000
   description VLAN client (1000) -> [cl_a,cl_b,sw2]
   ip address 172.16.0.3/24
   ip helper-address 10.0.0.2
   ip virtual-router address 172.16.0.1/24
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vlan 1000 vni 101000
   vxlan vlan 1000 flood vtep 10.0.0.4
!
ip virtual-router mac-address 02:00:ca:fe:00:ff
```

{{<cc>}}Cisco IOS DHCP server configuration{{</cc>}}
```
ip dhcp excluded-address 172.16.0.3
ip dhcp excluded-address 172.16.0.1
ip dhcp excluded-address 172.16.0.4
!
ip dhcp pool p_172.16.0.0
 network 172.16.0.0 255.255.255.0
 default-router 172.16.0.1 
```

### Does It Work?

It does. Here's the DHCP lease on **cl_a**:

{{<cc>}}DHCP lease on cl_a{{</cc>}}
```
Temp IP addr: 172.16.0.2  for peer on Interface: GigabitEthernet0/1
Temp  sub net mask: 255.255.255.0
   DHCP Lease server: 10.1.0.1, state: 5 Bound
   DHCP transaction id: 21A5
   Lease: 86400 secs,  Renewal: 43200 secs,  Rebind: 75600 secs
Temp default-gateway addr: 172.16.0.1
   Next timer fires after: 11:53:03
   Retry count: 0   Client-ID: cisco-5254.0099.2272-Gi0/1
   Client-ID hex dump: 636973636F2D353235342E303039392E
                       323237322D4769302F31
   Hostname: cl_a
```

Getting to that point is a bit more interesting; we'll use debugging on the DHCP client (**debug dhcp detail**) and the DHCP server (**‌debug ip dhcp server packet**) to figure out what's going on:

* DHCP client sends the initial DISCOVER packet

```
00:12:28: DHCP: SDiscover attempt # 1 for entry:
00:12:28: Temp IP addr: 0.0.0.0  for peer on Interface: GigabitEthernet0/1
00:12:28: Temp  sub net mask: 0.0.0.0
00:12:28:    DHCP Lease server: 0.0.0.0, state: 3 Selecting
00:12:28:    DHCP transaction id: 12E3
00:12:28:    Lease: 0 secs,  Renewal: 0 secs,  Rebind: 0 secs
00:12:28:    Next timer fires after: 00:00:04
00:12:28:    Retry count: 1   Client-ID: cisco-5254.0099.2272-Gi0/1
00:12:28:    Client-ID hex dump: 636973636F2D353235342E303039392E
00:12:28:                        323237322D4769302F31
00:12:28:    Hostname: cl_a
00:12:28: DHCP: SDiscover placed class-id option: 636973636F706E70
00:12:28: DHCP: SDiscover: sending 303 byte length DHCP packet
00:12:28: DHCP: SDiscover 303 bytes
00:12:28:             B'cast on GigabitEthernet0/1 interface from 0.0.0.0
```

* The broadcast from the DHCP client is propagated across the whole VLAN1000 and reaches **sw1** and (over VXLAN) **sw2**. Both switches relay the DHCP request to the DHCP server which gets two copies of the DHCP DISCOVER message. The switches use their unicast IP address in VLAN 1000 (172.16.0.3 and 172.16.0.4) as the **giaddr** (gateway IP address). Anycast IP address is not used.

{{<cc>}}DHCP DISCOVER message forwarded by sw1{{</cc>}}
```
00:12:27: DHCPD: Sending notification of DISCOVER:
00:12:27:   DHCPD: htype 1 chaddr 5254.0099.2272
00:12:27:   DHCPD: remote id 020a00000a01000101000000
00:12:27:   DHCPD: circuit id 00000000
00:12:27: DHCPD: DHCPDISCOVER received from client 0063.6973.636f.2d35.3235.342e.3030.3939.2e32.3237.322d.4769.302f.31
            through relay 172.16.0.3.
00:12:27: DHCPD: Option 125 not present in the msg.
00:12:27: DHCPD: Seeing if there is an internally specified pool class:
00:12:27:   DHCPD: htype 1 chaddr 5254.0099.2272
00:12:27:   DHCPD: remote id 020a00000a01000101000000
00:12:27:   DHCPD: circuit id 00000000
00:12:27: DHCPD: Allocate an address without class information (172.16.0.0)
00:12:27: DHCPD: Allocated binding 1013E808
00:12:27: DHCPD: Adding binding to radix tree (172.16.0.6)
00:12:27: DHCPD: Adding binding to hash tree
00:12:27: DHCPD: assigned IP address 172.16.0.6 to client 0063.6973.636f.2d35.3235.342e.3030.3939.2e32.3237.322d.4769.302f.31.
```

{{<cc>}}DHCP DISCOVER message forwarded by sw2{{</cc>}}
```
00:12:27: DHCPD: Sending notification of DISCOVER:
00:12:27:   DHCPD: htype 1 chaddr 5254.0099.2272
00:12:27:   DHCPD: remote id 020a00000a01000502000000
00:12:27:   DHCPD: circuit id 00000000
00:12:27: DHCPD: DHCPDISCOVER received from client 0063.6973.636f.2d35.3235.342e.3030.3939.2e32.3237.322d.4769.302f.31
            through relay 172.16.0.4.
00:12:27: DHCPD: Option 125 not present in the msg.
00:12:27: DHCPD: Seeing if there is an internally specified pool class:
00:12:27:   DHCPD: htype 1 chaddr 5254.0099.2272
00:12:27:   DHCPD: remote id 020a00000a01000502000000
00:12:27:   DHCPD: circuit id 00000000
00:12:27: DHCPD: Found previous server binding
00:12:29: DHCPD: Reprocessing saved workspace (ID=0x10000003)
00:12:29: DHCPD: Option 125 not present in the msg.
00:12:29: DHCPD: Sending notification of DISCOVER:
00:12:29:   DHCPD: htype 1 chaddr 5254.0099.2272
00:12:29:   DHCPD: remote id 020a00000a01000101000000
00:12:29:   DHCPD: circuit id 00000000
```

* DHCP server realizes it got duplicate DHCP DISCOVER messages and sends a single DHCP OFFER to the client:

```
00:12:29: DHCPD: Sending DHCPOFFER to client 0063.6973.636f.2d35.3235.342e.3030.3939.2e32.3237.322d.4769.302f.31 (172.16.0.6).
00:12:29: DHCPD: Option 125 not present in the msg.
00:12:29: DHCPD: no option 125
00:12:29: DHCPD: unicasting BOOTREPLY for client 5254.0099.2272 to relay 172.16.0.3.
00:12:29: DHCPD: client's VPN is .
00:12:29: DHCPD: No option 125
```

* **sw1** (172.16.0.3) relays the DHCP OFFER to the DHCP client. Please note that the DHCP server IP address is set to the IP address of the LAN interface, not the loopback IP address to which the request has been relayed:

```
00:12:30: DHCP: Received a BOOTREP pkt
00:12:30: DHCP: Scan: Message type: DHCP Offer
00:12:30: DHCP: Scan: Server ID Option: 10.1.0.1 = A010001
00:12:30: DHCP: Scan: Lease Time: 86400
00:12:30: DHCP: Scan: Renewal time: 43200
00:12:30: DHCP: Scan: Rebind time: 75600
00:12:30: DHCP: Scan: Subnet Address Option: 255.255.255.0
00:12:30: DHCP: Scan: Router Option: 172.16.0.1
00:12:30: DHCP: rcvd pkt source: 172.16.0.3,  destination:  255.255.255.255
00:12:30:    UDP  sport: 43,  dport: 44,  length: 308
00:12:30:    DHCP op: 2, htype: 1, hlen: 6, hops: 1
00:12:30:    DHCP server identifier: 10.1.0.1
00:12:30:         xid: 12E3, secs: 0, flags: 8000
00:12:30:         client: 0.0.0.0, your: 172.16.0.6
00:12:30:         srvr:   0.0.0.0, gw: 172.16.0.3
00:12:30:         options block length: 60
```

{{<note warn>}}If the DHCP server replied to the DHCP DISCOVER forwarded by **sw2**, the IP address of the DHCP server would be different, so it would look like you have two DHCP servers in your network.{{</note>}}

* The next packet in the process is a DHCP REQUEST packet sent as a broadcast packet (because the client still doesn't have a usable IP address) to the selected DHCP server:

```
00:12:30: DHCP: SRequest- Server ID option: 10.1.0.1
00:12:30: DHCP: SRequest- Requested IP addr option: 172.16.0.6
00:12:30: DHCP: SRequest placed class-id option: 636973636F706E70
00:12:30: DHCP: SRequest: 315 bytes
00:12:30: DHCP: SRequest: 315 bytes
00:12:30:             B'cast on GigabitEthernet0/1 interface from 0.0.0.0
```

* Yet again, the DHCP REQUEST broadcast is relayed by both switches, and the DHCP server receives two copies of the request. This time, the DHCP server replies to both DHCP REQUEST packets with DHCP ACK packets. It's better to send multiple ACKs than to risk not replying to the second request; the first reply could have been lost.

```
00:12:29: DHCPD: DHCPREQUEST received from client 0063.6973.636f.2d35.3235.342e.3030.3939.2e32.3237.322d.4769.302f.31.
...
00:12:29: DHCPD: Sending DHCPACK to client 0063.6973.636f.2d35.3235.342e.3030.3939.2e32.3237.322d.4769.302f.31 (172.16.0.6).
00:12:29: DHCPD: unicasting BOOTREPLY for client 5254.0099.2272 to relay 172.16.0.3.
...
00:12:29: DHCPD: DHCPREQUEST received from client 0063.6973.636f.2d35.3235.342e.3030.3939.2e32.3237.322d.4769.302f.31.
...
00:12:29: DHCPD: Sending DHCPACK to client 0063.6973.636f.2d35.3235.342e.3030.3939.2e32.3237.322d.4769.302f.31 (172.16.0.6)
00:12:29: DHCPD: unicasting BOOTREPLY for client 5254.0099.2272 to relay 172.16.0.4.
```

* Subsequent DHCP messages are exchanged as unicast messages between the DHCP client and the DHCP server.

### Reference: Lab Topology

As in the previous DHCP relaying labs, I had to define DHCP attributes in the lab topology:

```
defaults.attributes:
  link.dhcp:
    client: bool
    server: str
```

Next, I defined groups of devices:

* DHCP server is running on a Cisco IOS router running OSPF. We'll use an additional configuration template (`dhcp-server.j2`) to configure it.

```
groups:
  dhcp_server:
    members: [ srv ]
    module: [ ospf ]
    config: [ dhcp-server ]
    device: iosv
```

* DHCP clients are Cisco IOS routers:

```
groups:
  dhcp_client:
    members: [ cl_a, cl_b ]
    config: [ dhcp-client ]
    device: iosv
```

* VXLAN switches are Arista vEOS devices. They need OSPF, VLAN, VXLAN, and first-hop gateway *netlab* configuration modules. We'll use an additional configuration template (`dhcp-relay.j2`) to configure them.

```
groups:
  switch:
    members: [ sw1, sw2 ]
    module: [ ospf,vlan,vxlan,gateway ]
    config: [ dhcp-relay ]
    device: eos
```

Next, I had to define the client VLAN:

* It uses a shared first-hop gateway (default: anycast gateway). The anycast gateway is the first IP address in the subnet.
* The subnet is advertised into core OSPF process (the lab is not using VRFs) but we're not running OSPF on the VLAN.
* The VLAN is automatically mapped into a VXLAN segment (default *netlab* behavior):

```
vlans:
  client:
    gateway: True
    ospf.passive: True

gateway.id: 1
```

We have to list the nodes:

```
nodes: [ srv, sw1, sw2, cl_a, cl_b ]
```

And finally, it's time to define the links:

* First the three core links:

```
links:
- srv-sw1
- srv-sw2
- sw1-sw2
```

* Last but definitely not least, the client-facing links. The links are in access VLAN *client*, the clients use DHCP to get their IP address, and the switches relay DHCP requests to `srv`:

```
links:
- cl_a:
    dhcp.client: True
  sw1:
    dhcp.server: srv
  vlan.access: client
- cl_b:
    dhcp.client: True
  sw2:
    dhcp.server: srv
  vlan.access: client
```

You can download the [lab topology file](https://github.com/ipspace/netlab-examples/blob/master/DHCP/vxlan-relay/topology.yml) from GitHub.

### Reference: Configuration Templates

I had to make slight modifications to the DHCP server configuration template I used in the [simple DHCP relaying lab](/2023/03/netlab-dhcp-relay/):

* The default gateway IP address is the anycast IP address (if present)
* Anycast IP address has to be excluded from the DHCP pool.

{{<cc>}}DHCP pool configuration template{{</cc>}}
```
{% for h,v in hostvars.items() %}
{%   for intf in v.interfaces if intf.dhcp.server is defined and intf.ipv4 is defined %}
ip dhcp excluded-address {{ intf.ipv4|ipaddr('address') }}
{%     if intf.gateway.ipv4 is defined %}
ip dhcp excluded-address {{ intf.gateway.ipv4|ipaddr('address') }}
{%     endif %}
{%   endfor %}
{% endfor %}
!
{% for h,v in hostvars.items() %}
{%   for intf in v.interfaces if intf.dhcp.server is defined and intf.ipv4 is defined %}
!
ip dhcp pool p_{{ intf.ipv4|ipaddr('network') }}
 network {{ intf.ipv4|ipaddr('network') }} {{ intf.ipv4|ipaddr('netmask') }}
{%     if intf.gateway.ipv4 is defined %}
 default-router {{ intf.gateway.ipv4|ipaddr('address') }}
{%     else %}
 default-router {{ intf.ipv4|ipaddr('address') }}
{%     endif %}
{%   endfor %}
{% endfor %}
```

You can [download the configuration templates from GitHub](https://github.com/ipspace/netlab-examples/tree/master/DHCP/vxlan-relay); 

### Try It Out!

Want to run this lab on your own, or try it out with different devices? No problem:

* Make sure your preferred device supports DHCP relaying
* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [DHCP in VXLAN segment relaying example](https://github.com/ipspace/netlab-examples/tree/master/DHCP/vxlan-relay) into an empty directory
* If you want to use a relaying device that's not Arista EOS, add a configuration template to `dhcp-relay` subdirectory.
* Execute **netlab up**
* Enjoy! 😊

{{<next-in-series page="/posts/2023/04/netlab-evpn-dhcp-relay.md">}}
### Coming Up Next

DHCP relaying works in VXLAN segments with static ingress replication. Will it also work when we add EVPN and EVPN VRFs to the mix? That's the topic of the next blog post in this series.{{</next-in-series>}}
