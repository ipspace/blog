---
date: 2023-03-13 07:01:00+00:00
netlab_tag: use
series_title: DHCP Relaying Lab
tags: [ netlab, DHCP, IP routing ]
title: Test DHCP Relaying with netlab
pre_scroll: True
series: [ dhcp-relay ]
---
After [figuring out how DHCP relaying works](/2023/03/dhcp-relay-process/), I decided to test it out in a lab. *netlab* has no DHCP configuration module (at the moment); the easiest way forward seemed to be custom configuration templates combined with a few extra attributes.

### Lab Topology

This is how I set up the lab:
<!--more-->
* I created simple lab topology with DHCP server (IOSv), DHCP client (another IOSv), and a relaying node that could be anything that supports DHCP relaying.

{{<figure src="/2023/03/dhcp-relay.png" caption="lab topology">}}

{{<cc>}}Lab IP addressing{{</cc>}}
```
  Interface                  IPv4 address  Description
=========================================================
srv (10.0.0.1/32)
  GigabitEthernet0/1          10.1.0.2/30  srv -> relay

relay (10.0.0.2/32)
  GigabitEthernet0/1          10.1.0.1/30  relay -> srv
  GigabitEthernet0/2        172.16.0.2/24  relay -> user

user (10.0.0.3/32)
  GigabitEthernet0/1        172.16.0.3/24  user -> relay
```

* I used interface attribute **dhcp.client** (boolean) on the client and **dhcp.server** (node name, string) on the relay node. This is how I [defined those attributes](https://netlab.tools/extend-attributes/):

{{<cc>}}Extra DHCP attributes{{</cc>}}
```
defaults.attributes:
  link.dhcp:
    client: bool
    server: str
```

* I could have defined [custom configuration templates](https://netlab.tools/groups/#custom-configuration-templates) on individual nodes but decided to [use groups](https://netlab.tools/groups/) to make the lab topology easy to extend:

{{<cc>}}DHCP client, relay, and server groups{{</cc>}}
```
groups:
  dhcp_server:
    members: [ srv ]
    module: [ ospf ]
    config: [ dhcp-server ]
    device: iosv
  dhcp_client:
    members: [ user ]
    config: [ dhcp-client ]
    device: iosv
  switch:
    members: [ relay ]
    module: [ ospf ]
    config: [ dhcp-relay ]
```

* I'm running OSPF between DHCP relay and DHCP server. While that's not how you'd set up a typical DHCP server, it allows me to relay DHCP requests to the DHCP server loopback interface.
* Finally, I had to define the nodes and the links:

{{<cc>}}Nodes and links{{</cc>}}
```
nodes: [ srv, relay, user ]

links:
- relay-srv
- user:
    dhcp.client: True
  relay:
    dhcp.server: srv
  type: lan
```

{{<note info>}}I set the link **type** on the link between user and relay switch to LAN to ensure it gets a /24 prefix. Doing DHCP on a /30 prefix is boring.{{</note>}}

As always, you can [find the final topology file on GitHub](https://github.com/ipspace/netlab-examples/blob/master/DHCP/relay/topology.yml).

### Configuration Templates

Now for the fun part: custom configuration templates ([also on GitHub](https://github.com/ipspace/netlab-examples/tree/master/DHCP/relay)). The client template was trivial:

* Find interfaces with **dhcp.client** attribute
* Remove static IPv4 address from them
* Enable DHCP client on the interface

{{<cc>}}DHCP client configuration template{{</cc>}}
```
{% for intf in interfaces if intf.dhcp.client is defined and intf.dhcp.client %}
interface {{ intf.ifname }}
 no ip address
 ip address dhcp
{% endfor %}
```

The relaying template was already a bit more convoluted. I had to find the interfaces with **dhcp.server** attribute and then find the loopback IP address of the DHCP server to use in the **helper-address** command. Interestingly, I could use identical template for Cisco IOSv and Arista vEOS.

{{<cc>}}DHCP relay configuration template{{</cc>}}
```
{% for intf in interfaces if intf.dhcp.server is defined %}
interface {{ intf.ifname }}
 ip helper-address {{ hostvars[intf.dhcp.server].loopback.ipv4|ipaddr('address') }}
{% endfor %}
```

Finally the DHCP server template. This one is a beast:

* It iterates over all other nodes in the Ansible inventory and finds interfaces with **dhcp.server** attribute (relaying interfaces)
* For each relaying interface, the template excludes its IPv4 address from the DHCP pool, and creates a corresponding pool with the relaying interface IPv4 address as the default router.
* I also turned on debugging in the configuration template so I could log into the DHCP server and inspect the logs immediately after **netlab up** completes its job.

{{<cc>}}DHCP server configuration template{{</cc>}}
```
logging buffered
no service timestamp debug
!
do debug ip dhcp server packet
do debug ip dhcp server event
!
{% for h,v in hostvars.items() %}
{%   for intf in v.interfaces if intf.dhcp.server is defined and intf.ipv4 is defined %}
ip dhcp excluded-address {{ intf.ipv4|ipaddr('address') }}
{%   endfor %}
{% endfor %}
!
{% for h,v in hostvars.items() %}
{%   for intf in v.interfaces if intf.dhcp.server is defined and intf.ipv4 is defined %}
!
ip dhcp pool p_{{ intf.ipv4|ipaddr('network') }}
 network {{ intf.ipv4|ipaddr('network') }} {{ intf.ipv4|ipaddr('netmask') }} 
 default-router {{ intf.ipv4|ipaddr('address') }}
{%   endfor %}
{% endfor %}
```

Here are the extra configuration commands generated by these templates:

{{<cc>}}Cisco IOS DHCP client configuration{{</cc>}}
```
interface GigabitEthernet0/1
 no ip address
 ip address dhcp
```

{{<cc>}}Cisco IOS DHCP relay configuration{{</cc>}}
```
interface GigabitEthernet0/2
 ip helper-address 10.0.0.1
```

{{<cc>}}Cisco IOS DHCP server configuration (including debugging commands){{</cc>}}
```
logging buffered
no service timestamp debug
!
do debug ip dhcp server packet
do debug ip dhcp server event
!
ip dhcp excluded-address 172.16.0.2
!
!
ip dhcp pool p_172.16.0.0
 network 172.16.0.0 255.255.255.0
 default-router 172.16.0.2
```

You can find the [final device configurations](https://github.com/ipspace/netlab-examples/tree/master/DHCP/relay/config) using Arista EOS on the DHCP relay in the [GitHub netlab-example repository](https://github.com/ipspace/netlab-examples).

### Does It Work?

You bet. Here's the printout from the client router:

```
user#show dhcp lease
...
Temp IP addr: 172.16.0.3  for peer on Interface: GigabitEthernet0/1
Temp  sub net mask: 255.255.255.0
   DHCP Lease server: 10.1.0.2, state: 5 Bound
   DHCP transaction id: EAB
   Lease: 86400 secs,  Renewal: 43200 secs,  Rebind: 75600 secs
Temp default-gateway addr: 172.16.0.2
   Next timer fires after: 11:59:35
   Retry count: 0   Client-ID: cisco-5254.002c.2b7b-Gi0/1
   Client-ID hex dump: 636973636F2D353235342E303032632E
                       326237622D4769302F31
   Hostname: user
```

There seems to be a tiny glitch in the printout: the DHCP relay is forwarding DHCP requests to 10.0.0.1, but the DHCP client claims it's talking with DHCP server with IP address 10.1.0.2 -- the LAN interface IPv4 address of the DHCP server. The change of IP address is a perfect implementation of RFC 2131 which [says](https://www.rfc-editor.org/rfc/rfc2131#section-4.1):

> If the server has received a message through a DHCP relay agent, the server SHOULD choose an address from the interface on which the message was recieved [sic] as the 'server identifier' (unless the server has other, better information on which to make its choice).

It's nice to see things working exactly the way they should ;)

### Fighting Repeatability Crisis One Lab at a Time

Want to run this lab on your own, or try it out with different devices? No problem:

* Make sure your preferred device supports DHCP relaying
* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [DHCP relaying example](https://github.com/ipspace/netlab-examples/tree/master/DHCP/relay) into an empty directory
* If you want to use a relaying device that's not Cisco IOS or Arista EOS, add a configuration template to `dhcp-relay` subdirectory.
* Execute **netlab up**
* Enjoy! 😊

{{<next-in-series page="/posts/2023/03/netlab-vrf-dhcp-relay.md">}}
### Coming Up Next

Simple DHCP relaying works, but what about inter-VRF DHCP relaying? That's the topic of the next blog post in this series.{{</next-in-series>}}
