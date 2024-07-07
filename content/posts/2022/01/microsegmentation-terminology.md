---
title: "Microsegmentation Terminology"
date: 2022-01-04 08:43:00
tags: [ security, firewalls ]
---
While I liked reading the *[Where to Stick the Firewall](https://netcraftsmen.com/where-to-stick-the-firewall-part-1/)* blog post by Peter Welcher, it bothered me a bit that he used *microsegmentation* to mean *security groups*.

I know that *microsegmentation* became approximately as well-defined as *cloud* or *SDN*[^MSG], but let's aim our shiny lance [^SL] at the nearest windmill and gallop away...
<!--more-->
[^SL]: It's been neatly polished during the New Year break

[^MSG]: Gartner [claims to have](https://blogs.gartner.com/andrew-lerner/2017/03/21/microsegmentation/) *an official definition*, but it's behind a paywall so whatever.

The way it was initially defined[^VMD], **microsegmentation** is the ability to protect **every individual endpoint**, which means a packet filter in front of every VM, container, or end-user device. You get that level of protection in most cloud environments, with VMware NSX Distributed Firewall, or with Cisco ACI (to some extent[^ACIV]).

[^VMD]: IIRC: by VMware at the NSX launch

[^ACIV]: Cisco ACI has a problem with virtual endpoints on VMware ESXi as they cannot control the VMware virtual switch. I have no idea how the [Application Virtual Switch](/2017/03/running-vsphere-on-cisco-aci-think-twice/) SNAFU ended; the usual workarounds are _run virtual switch in a VM_ or _run private VLANs_. Oh, the beauties of [fixing suboptimal architecture](/2013/06/network-virtualization-and-spaghetti/) with complex kludges.

The packet filters in front of the endpoints could be stateless (Cisco ACI[^SESS]), stateful (AWS or Azure security groups), or have some deep packet inspection capabilities (VMware NSX).

[^SESS]: Per-session 5-tuples needed to implement stateful packet filters cannot fit into any reasonably sized TCAM -- another wonderful side effect of insisting on using the wrong hammer for the job.

Then we have *Security groups* or *security tags*. They could be just a convenient configuration mechanisms (in most cases) or data-plane markers (Cisco ACI) that simplify packet filters[^SCALE]... but they are nothing more than another application of RFC 1925 Rule 6. Regardless of PowerPoint-promised magic and dancing unicorns, the traffic filtering rules using *object tags* or *sets of objects* have to be transformed into the usual 5-tuple packet filters (modulo optimizations like object groups). There’s no other way to do it at reasonable speed.

[^SCALE]: See [Scaling the Cloud Security Groups](/2014/11/scaling-cloud-security-groups/) for more details.

Finally, while [Matthias Luft somewhat disagrees with me](/series/host-firewalls/), I think the microsegmentation packet filter should be outside of the protected endpoint to prevent root exploits from disabling it.

### More Details

* I mentioned microsegmentation in _[Virtual Firewalls](https://www.ipspace.net/Virtual_Firewalls)_ webinar and dived deep into IPv6-related details in _[IPv6 Microsegmentation](https://www.ipspace.net/IPv6_Microsegmentation)_
* I compared VMware's and Cisco's implementation of microsegmentation in _[VMware NSX, Cisco ACI or Standard-Based EVPN](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN)_ webinar.
* You'll find Cisco ACI implementation details in _[Cisco ACI Deep Dive](https://www.ipspace.net/Cisco_ACI_Deep_Dive)_ and NSX implementation details in _[VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)_
* AWS Security Groups and Azure Network Security Groups are described in _[Amazon Web Services Networking](https://www.ipspace.net/Amazon_Web_Services_Networking)_ and _[Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking)_ webinars.
