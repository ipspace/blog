---
date: 2008-08-20 07:25:00+02:00
ospf_tag: config
tags:
- OSPF
title: Reverse Lookup of OSPF Router IDs
url: /2008/08/reverse-lookup-of-ospf-router-ids/
---
If you store the reverse mapping for the routers' loopback interfaces in DNS or configure the name-to-address mappings with the **ip host** commands, you can use the **ip ospf name-lookup** global configuration command to display the OSPF router IDs as router names.
<!--more-->
For example, I've configured the names of all provider routers' loopback interfaces in one of my MPLS VPN labs:

``` code
P#show run | inc host
ip host PE-A 10.0.1.1
ip host PE-B 10.0.1.2
ip host PE-C 10.0.1.5
ip host P 10.0.1.6
```

After that, I configured the **ip ospf name-lookup** command, and the OSPF show commands started printing names instead of IP addresses:

``` code
P#show ip ospf database

            OSPF Router with ID (10.0.1.6) (Process ID 1)

                Router Link States (Area 0)

Link ID    ADV Router   Age   Seq#       Checksum Link count
10.0.1.1   PE-A         56    0x80000002 0x000C1F 3
10.0.1.2   PE-B         57    0x80000002 0x003FD8 3
10.0.1.5   PE-C         59    0x80000002 0x0027CF 3
10.0.1.6   P            53    0x80000003 0x00B675 7
```

Unfortunately, this functionality does not implement its full potential. For example, when examining router link states, the router ID is displayed as a name, but the adjacent router IDs are not. Too bad, you still have to know the router IDs by heart.

``` code
P#show ip ospf database router 10.0.1.6

            OSPF Router with ID (10.0.1.6) (Process ID 1)

                Router Link States (Area 0)

  LS Type: Router Links
  Link State ID: 10.0.1.6
  Advertising Router: P
  LS Seq Number: 80000003

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.5
     (Link Data) Router Interface address: 10.0.7.30
      Number of MTID metrics: 0
       TOS 0 Metrics: 64

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.2
     (Link Data) Router Interface address: 10.0.7.18
      Number of MTID metrics: 0
       TOS 0 Metrics: 64

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.1
     (Link Data) Router Interface address: 10.0.7.10
      Number of MTID metrics: 0
       TOS 0 Metrics: 64 
```
