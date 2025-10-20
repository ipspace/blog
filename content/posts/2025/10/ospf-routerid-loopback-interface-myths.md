---
title: "OSPF Router ID and Loopback Interface Myths"
date: 2025-10-21 08:14:00+0200
tags: [ OSPF ]
ospf_tag: details
---
Daniel Dib wrote a [nice article describing the history of the loopback interface](https://www.linkedin.com/feed/update/urn:li:activity:7381217822187708416/)[^PHB], triggering an inevitable [mention](https://www.linkedin.com/feed/update/urn:li:activity:7381217822187708416?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7381217822187708416%2C7381277236454395904%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287381277236454395904%2Curn%3Ali%3Aactivity%3A7381217822187708416%29) of the role of a loopback interface in OSPF and related flood of ancient memories on my end.

[^PHB]: If only he would also publish it on his blog for posterity 🤷‍♂️

Before going into the details, let's get one fact straight: an OSPF router ID was always (at least from the days of OSPFv1 described in [RFC 1133](https://www.rfc-editor.org/rfc/rfc1131.pdf)) just a 32-bit identifier, not an IPv4 address[^SM]. Straight from the RFC 1133:
<!--more-->
> Router ID a 32-bit number that uniquely identifies this router in the AS. One possible implementation strategy would be to use the smallest IP interface address belonging to the router.

[^SM]: I was too ~~stupid~~ focused on Cisco's documentation to realize it at the time when I was creating the Advanced OSPF course. It took me years to figure out it pays to read the RFCs.

Someone within Cisco focused too much on the latter part of the above paragraph, resulting in decades-long insistence on OSPF router ID being an interface IPv4 address[^IFADDR]. That slant persisted as the informal OSPF lore spread across other vendors[^OSV]. 

[^IFADDR]: If I remember correctly, there are modern implementations that expect you to configure explicit router IDs.

[^OSV]: It looks like none of the vendors mentioned in the first [Experience with the OSPF protocol](https://www.rfc-editor.org/rfc/rfc1246) from 1991 are still around. Also, I didn't know that Dino Farinacci of the EIGRP and LISP fame worked on OSPF at 3com at that time.

However, compared to what we have to deal with today, the initial implementation attempts were particularly "interesting"[^WWYT]. Here's how I remember Cisco's slow realization of the gap between theory and practice[^SPH]:

[^WWYT]: Some of them falling into the "what were you thinking" category.

[^SPH]: Yeah, I know that snark is easy with perfect hindsight, but hey, I had to live with all that. Give me some slack ;)

1. Initially, Cisco would pick the highest IP address of any interface configured on the box as the router ID.
2. Even worse, they would change the router ID if that interface went down, resulting in a temporary loss of a router node for no good reason.
3. Losing a transit router just because an interface flapped eventually bothered enough customers to trigger a change in behavior. They figured out that using a loopback interface IPv4 address as a router ID makes for more stable networks, so the above rule #1 was changed into 'the highest loopback IPv4 address, or the highest IPv4 address if the device has no loopbacks'
4. Years later[^120T], we got the **router-id** command.

[^120T]: [In release 12.0T](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-i1.html#wp4220238026) according to Cisco IOS OSPF command reference.

{{<note>}}
Fun fact: according to Cisco IOS IPv6 command reference, the **ipv6 router ospf** command was [added](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6/command/ipv6-cr-book/ipv6-i4.html#wp1790661162) in IOS release 12.2(15)T and it took until [IOS release 15.2T](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6/command/ipv6-cr-book/ipv6-r1.html#wp4240068693) to get the **router-id** OSPFv3 configuration command.
{{</note>}}

5. Sometime during that journey, they got to a point where a loss of an interface no longer triggered a change in the router ID. Even changing the interface IP address that was used as the router ID no longer changes the router ID (you have to clear the OSPF process to change it). Mission Accomplished.

However, based on the my experience writing OSPF-in-VRFs _netlab_ configuration templates for numerous devices, Cisco IOS is the only device that still treats OSPF router ID as something special[^DQ].

All other devices are perfectly happy to start multiple OSPF processes with the same router ID[^PF]; Cisco IOS (and IOS/XE) refuses to do that, rejects duplicate statically-configured **router-id**[^AFF], and uses the above algorithm to pick a different OSPF router ID for every VRF OSPF process. Even worse, if you configure two OSPFv3 routing processes (without static router IDs) but have a single IPv4 address on the device, one of them won't start.

[^DQ]: To make Cisco IOS pass OSPF-in-VRF integration tests (we use router ID to verify whether the expected OSPF adjacencies are up), we had to add a device quirk that generates different OSPF router IDs for every VRF OSPF instance. No other device we [implemented OSPFv2/OSPFv3](https://netlab.tools/module/ospf/#platform-support) for required that quirk.

[^PF]: Which is perfectly fine unless you connect multiple OSPF processes running on the same box to the same OSPF network.

[^AFF]: Another fun fact: while refusing the configured OSPF router ID, Cisco IOS generates an error message that Ansible **ios_config** module does not recognize as an error. The Ansible playbook configuring OSPF succeeds, but the device is not working the way you'd expect it to work.
