---
title: "Prefix Sets: Simplifying netlab ACLs and Prefix Filters"
date: 2026-09-28 08:16:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
When I implemented [prefix filters](https://netlab.tools/module/routing/#generic-routing-prefixes) in _netlab_ ([release 1.9.0](https://netlab.tools/release/1.9/#release-1-9-0)), I wanted them to match the final device configurations as closely as possible, including the *one prefix per entry* rule to match the device configuration sequence numbers. That worked well, but resulted in YAML bloat, since each matching prefix requires several lines of YAML.

We tried to use the same approach with ACLs but quickly gave up when we realized the *port not in range* operation requires multiple ACL entries on most platforms. With the *matching sequence numbers* paradigm gone with the wind, it made no sense to limit ourselves to one prefix per ACL entry -- the initial [ACL entry implementation](https://netlab.tools/module/routing/#acl-entries) already accepted *lists* of prefixes and expanded them into ACL entries.
<!--more-->
Mistakenly[^DMWL], we also copied the prefix-specification mechanism from prefix filters into ACLs: each entry accepted a number of parameters (**prefix**, **pool**, **ipv4**, **ipv6**, **node**...) that resulted in IP prefix(es) from different netlab objects. However, once we started rolling, the ideas didn't stop there. It would be nice to match on VLAN prefixes and link prefixes based on a link ID or role. It was time for a redesign, resulting in [generic prefix sets](https://netlab.tools/module/routing/#generic-routing-prefix-set) introduced in release 25.09:

[^DMWL]: Following the *do more with less* mantra popularized by the techbros.

* A *prefix* set is a list of prefixes
* Every prefix is either an IPv4/IPv6 address, an IPv4/IPv6 prefix, or an object descriptor
* An object descriptor has a *namespace* (**pool**, **vlan**...) and an object ID, separated by a dot (for example, `vlan.red`). You can find the [complete list of object namespaces](https://netlab.tools/module/routing/#specifying-generic-prefixes) in the netlab documentation.

{{<note>}}
Following the *no topology left behind* mantra, the old ACL attributes still work, and we still have to migrate the **node** attribute to the new format. That will take a bit longer, as I plan to use *node sets*.
{{</note>}}

For example, you can use this simple definition to allow all traffic from LAN subnets and loopbacks (assuming you use automatic address assignments):

```
routing.acl:
  endpoints:
  - protocol: ip
    src.prefix: [ pool.lan, pool.loopback ]
```

It generates this ACL on Arista EOS:

```
ip access-list endpoints_ipv4
   100 permit ip 172.16.0.0/16 any
   110 permit ip 10.0.0.0/24 any
```

After cleaning up the ACL implementation, it was time to implement the same mechanism for *prefix filters*:

* Each prefix-specifying argument can be a list (previously, they only accepted a single value)
* You can use the **prefix** argument to specify a prefix set.

For example, the following topology using [dual-stack loopbacks](https://netlab.tools/addressing/) and a [named prefix](https://netlab.tools/prefix/) specifies a prefix filter containing a pool definition, a named prefix, and a literal IPv6 prefix:

```
module: [ routing ]

addressing.loopback.ipv6: 2001:db8::/48
prefix.alpha.ipv4: 192.168.42.0/24

nodes:
  rtr:
    routing.prefix:
      example:
      - prefix: [ pool.loopback, prefix.alpha, 2001:db8:cafe:2::/64 ]
```

Based on the *example* prefix filter definition, netlab generates two prefix lists on Arista EOS:

{{<printout caption="Prefix lists generated from the example prefix filter for Arista EOS">}}
ip prefix-list example-ipv4 seq 100 permit 10.0.0.0/24
ip prefix-list example-ipv4 seq 110 permit 192.168.42.0/24
!
ipv6 prefix-list example-ipv6
  seq 100 permit 2001:db8::/48
  seq 110 permit 2001:db8:cafe:2::/64
{{</printout>}}

Cisco IOS XR can accept IPv4 and IPv6 prefixes in the same prefix set. netlab thus generates the following prefix set based on the above lab topology:

{{<printout caption="Prefix lists generated from the example prefix filter for Cisco IOS XR">}}
prefix-set example
  10.0.0.0/24,
  192.168.42.0/24,
  2001:db8::/48,
  2001:db8:cafe:2::/64
end-set
{{</printout>}}
