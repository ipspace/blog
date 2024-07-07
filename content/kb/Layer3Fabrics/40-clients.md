---
kb_section: Layer3Fabrics
minimal_sidebar: true
title: Challenges of Multi-Subnet Clients
url: /kb/Layer3Fabrics/40-clients/
---
Ignoring the [application-level challenges of multi-subnet clients](20-apps.html), the networking setup used on a client faces the same challenges as the [server-side setup](30-servers.html). Most importantly, it should ensure symmetrical traffic flow: outgoing traffic should always be sent through the interface having the IP address used in the outgoing packet.

Traffic flow symmetry is desirable property in most deployments, but becomes crucial when:

* Using multipath TCP on devices connected to multiple service providers (some ISPs implement strict checks of source IP addresses to prevent spoofing attacks from their clients);
* Using strict separation of transport networks like SAN-A/SAN-B separation in MPIO iSCSI deployments.

You could use policy-based routing, VRFs, or routing trick to implement consistent outbound interface selection. The first two approaches have been described in the [previous section](30-servers.html), we'll use multi-path iSCSI example to describe the typical routing tricks used in iSCSI clients (for example, VMware ESXi). 

### Example: Multi-Path iSCSI

Imagine the following scenario:

* Servers (iSCSI initiators — clients) and storage arrays (iSCSI targets — servers) are connected to two isolated transport networks (SAN-A, SAN-B);
* SAN-A and SAN-B fabrics are not connected. Servers should use IP addresses in SAN-A to connect to storage array’s interface connected to SAN-A (and likewise for SAN-B).

{{<note note>}}We'll use the SAN-A/SAN-B terminology commonly used in Fibre Channel networks even though we’re describing the behavior of IP fabrics supporting iSCSI connectivity.{{</note>}}

{{<figure src="../Redundant-App-Sessions.png" caption="Air-gapped SAN-A/SAN-B iSCSI networks">}}

Assuming you don't want to deal with policy routing or VRFs, you could enforce the desired traffic flow with a set of static routes:

* Static route for storage array IP address (or IP prefix) in SAN-A (subnet X or X.1) points to server interface connected to SAN-A (A.1);
* A similar static route is configured for SAN-B.

With the default behavior of TCP stacks in most operating systems:

* Traffic for storage array IP address in SAN-A (or SAN-B) is sent through the server interface connected to the same SAN fabric;
* New TCP sessions established with iSCSI targets in SAN-A therefore use source IP address assigned to server interface connected to SAN-A;
* Assuming a similar setup on the storage array the return traffic uses the same path, resulting in working iSCSI solution and perfect SAN-A/SAN-B isolation.

{{<note info>}}TCP servers (iSCSI targets) with VRF-aware TCP/IP stacks don’t even need static routes. Correctly implemented VRF-aware TCP/IP stacks bind an incoming TCP session to a VRF and use the same VRF for return traffic.{{</note>}}

Unfortunately, most storage vendors don’t want to burden their users (or their internal support teams[^1]) with the host requirements needed to implement a well-designed isolated IP fabrics. It’s much easier to shift the burden to the networking team and mandate a use of a single VLAN[^2] between iSCSI initiators (servers) and targets (storage arrays), resulting in more complex and more brittle transport fabrics.

[^1]: [Revisited: The Need for Stretched VLANs](https://blog.ipspace.net/2018/01/revisited-need-for-stretched-vlans.html)

[^2]: [Let’s Pretend We Run Distributed Storage over a Thick Yellow Cable](https://blog.ipspace.net/2017/11/lets-pretend-we-run-distributed-storage.html)
