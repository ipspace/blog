---
title: "BGP AS Numbers for a Private MPLS/VPN Backbone"
date: 2024-03-13 08:30:00+0100
tags: [ MPLS VPN, BGP, design ]
---
One of my readers was building a private MPLS/VPN backbone and wondered whether they should use their public AS number or a private AS number for the backbone. Usually, it doesn't matter; the deciding point was the way they want to connect to the public Internet:

> We also plan to peer with multiple external ISPs to advertise our public IP space not directly from our PE routers but from dedicated Internet Routers, adding a firewall between our PEs and external Internet routers.

They could either run BGP between the PE routers, firewall, and WAN routers (see [BGP as High-Availability Protocol](https://blog.ipspace.net/kb/BGPHighAvailability/) for more details) or run BGP *across* a bump-in-the-wire firewall:
<!--more-->
{{<ascii>}}
┌─────────┐   ┌────────┐   ┌──────────┐
│PE-router├───┤Firewall├───┤WAN router│
└─────────┘   └────────┘   └──────────┘
                                       
     ◄─────────── BGP ──────────►      
{{</ascii>}}

In either case, it's easier to run EBGP sessions at the edge of the MPLS/VPN backbone to avoid the BGP-next-hop mess. If you do that, using a private ASN for the MPLS backbone is simpler—you can remove it from the public AS path with the **remove-private-as** functionality.

Now for a more interesting challenge. They wanted to "*‌use a dedicated 4-byte private ASN for each VPN.*" Using a private ASN for a VPN (assuming each connected site belongs to a single VPN) is not the best way to set up a private MPLS/VPN backbone. You have to use *route targets* to indicate VPN membership anyway, and I'd use the BGP AS numbers to indicate *sites* – each site would get a unique private ASN.

Finally, I'd prefer the traditional 2-byte private AS numbers, assuming the network doesn't have more than 1000 sites. While it's perfectly OK to use 4-byte private AS numbers (most network devices have supported 4-octet ASNs for ages), they're at the end of the 32-bit address space (4200000000-4294967294), and I'm not sure I'd want to use such an excellent opportunity for a typing mistake in my device configurations.