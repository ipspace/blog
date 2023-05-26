---
date: 2012-02-15 06:28:00+01:00
tags:
- data center
- workshop
- load balancing
title: Microsoft Network Load Balancing Behind the Scenes
url: /2012/02/microsoft-network-load-balancing-behind.html
---
I figured out I [wrote a lot about Microsoft Network Load Balancing (NLB)](http://www.google.com/search?q=nlb+site:ipspace.net) without ever explaining how that marvel of engineering works. To fix that omission, here's a [short video](http://demo.ipspace.net/bin/watch?id=8050da3e-5655-11e1-96be-005056880254) taken from the [Data Center 3.0 webinar](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers).

[![](/2012/02/s400-MSNLB.png)](https://my.ipspace.net/bin/get/DC30/D1%20-%20Microsoft%20Network%20Load%20Balancing.mp4?doccode=DC30)
<!--more-->
**Notes and links**

-   Microsoft NLB can use IGMP, which can be used with IGMP snooping configured on the switches to limit the inbound traffic flooding to the servers that are actually interested in the traffic.
-   [Network Load Balancing Technical Overview](http://technet.microsoft.com/en-us/library/bb742455.aspx), which includes this gem: "Experience has shown that Cisco routers currently do not accept an ARP response from the cluster that resolves unicast IP addresses to multicast MAC addresses." (because Cisco's engineers actually read RFCs before writing the code).
-   [Catalyst Switches for Microsoft NLB Configuration Example](http://www.cisco.com/en/US/products/hw/switches/ps708/products_configuration_example09186a0080a07203.shtml) (including the famous static ARP hack).
-   If you want to use NLB unicast mode within vSphere, you have to [disable RARP packets that are automatically sent after the vMotion events](http://www.vmware.com/files/pdf/implmenting_ms_network_load_balancing.pdf) \... because even vSwitch hates being a hub.

### More Information

Several webinars available on ipSpace.net cover [data center-specific topics](http://www.ipspace.net/Roadmap/Data_center_webinars):

-   Generic data center technologies and designs (including load balancing solutions that make sense) are described in [Data Center 3.0 for Networking Engineer](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers).
-   You'll find large-scale network designs (including leaf & spine and Clos network architectures) in the [Data Center Fabric Architectures](http://www.ipspace.net/Data_Center_Fabrics) webinar.
-   Learn everything there is to know about VMware's vSwitch and other VMware-related networking solutions in [VMware Networking Deep Dive](http://www.ipspace.net/VMware_Networking_Deep_Dive).
-   Cloud networking-specific topics are the focus of [Cloud Computing Networking -- Under the Hood](http://www.ipspace.net/Cloud_Computing_Networking:_Under_the_Hood) webinar.

And don't forget: you get access to all these webinars (and numerous others) if you buy the [yearly subscription](http://www.ipspace.net/Subscription).
