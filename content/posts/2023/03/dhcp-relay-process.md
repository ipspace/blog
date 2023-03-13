---
title: "DHCP Relaying Details"
date: 2023-03-09 07:54:00
tags: [ DHCP, IP routing ]
series: [ dhcp-relay ]
---
Chinar Trivedi asked an [interesting question](https://twitter.com/cloudnetworkguy/status/1631891785478971392) about DHCP relaying in VXLAN/EVPN world on Twitter and my first thought was "_that shouldn't be hard_" but when I [read the first answer](https://twitter.com/aninchat/status/1631952450189131776) that turned into "_wait a minute, how exactly does DHCP relaying works?_"

I'm positive there's a tutorial out there somewhere, but I decided to go back to the sources of wisdom: the RFCs. It turned out to be a long walk down the IETF history lane.
<!--more-->

### Simple DHCP Relaying

Interestingly, [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131) (DHCP) does not define relaying at all but refers to [Clarifications and Extensions for the BOOTP](https://www.rfc-editor.org/rfc/rfc1542) (RFC 1542)[^ANC]. Here's [how it works](https://www.rfc-editor.org/rfc/rfc1542#section-4):

* The DHCP client[^BP] sends a DHCPDISCOVER message as a layer-2 broadcast. It SHOULD set the **chaddr** field[^MM] in the request message to its MAC address.
* A relaying agent receives that broadcast, turns it into an IP unicast[^RB] and sends that toward the DHCP server.
* The relaying agent sets the **giaddr** (gateway IP address) field in the forwarded DHCP message _if it hasn't been set already_. When you're using a series of DHCP relays[^JS], only the first relay sets the **giaddr**[^HC].
* DHCP server COULD use the **giaddr** IP address to select the IP subnet to use for client address allocation if the relaying agent hasn't added the [IPv4 Subnet Selection Option](https://www.rfc-editor.org/rfc/rfc3011) to the forwarded message.
* DHCP server creates a reply message, copies **chaddr** field from the request into it, and sends the reply message straight to **giaddr** -- the first relay.
* A relaying agent receiving a response from a DHCP server selects the outbound interface based on the **giaddr**, and sends the response to the client as a unicast (assuming the **chaddr** field is set) or a local broadcast (if the **chaddr** field is not set, or if the **broadcast** flag was set by the client).

[^ANC]: I hope you realized that the only reason your phone gets an IP address when it's turned on is an ancient bit of technology developed in early 1980s.

[^BP]: OK, technically it's a BOOTP client, but who's counting ;)

[^MM]: There's another RFC describing how to deal with brain-dead clients that can't figure out what their MAC address is. No, I'm not going there ;)

[^RB]: Or another (subnet-level) broadcast or a batch of packets with different destinations, but let's try to keep things simple.

[^JS]: Hopefully to increase your job security, I see no other good reason ;)

[^HC]: There's also a "forwarded hop count", but as I said, let's try not to explore every crazy rabbit trail there is.

### Relay Options

So far so good, but life is never as easy as that. [RFC 3046](https://www.rfc-editor.org/rfc/rfc3046.html) (DHCP Relay Agent Information Option) defines the famous Option 82 that initially contained *Circuit ID* (incoming interface) and *Remote ID* (end user). DHCP server COULD use that information to:

* "Authenticate" the end-user (has the user connected to port X paid last month's bill?)
* Assign a fixed IP address to an end-user based on the access interface to which the end-user is attached.

It's also worth noting that the DHCP server copies option 82 into DHCP reply messages[^VSX]. A DHCP relay could use option 82 from the reply message instead of **giaddr** to select the outgoing interface for the forwarded reply.

With the generic *relay information option* infrastructure in place, vendor creativity soared. Cisco SDA [uses *remote ID* sub-option to encode VNI and RLOC](https://www.theasciiconstruct.com/post/sda_8/), and DMVPN uses it to [store the transport IP address of the DMVPN spoke](https://blog.ipspace.net/2023/03/dhcp-relay-process.html#1696).

[^VSX]: Apart from one of the Virtual Subnet Selection sub-options. Read [RFC 6607](https://www.rfc-editor.org/rfc/rfc6607.html) if you crave those details.

But wait, that's not all. [IANA DHCP registry](https://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xhtml#relay-agent-sub-options) defines over 20 sub-options of option 82, including [DOCSIS device class](https://www.rfc-editor.org/rfc/rfc3256.html), [Subscriber ID](https://www.rfc-editor.org/rfc/rfc3993.html)[^SID], [RADIUS attributes](https://www.rfc-editor.org/rfc/rfc4014.html)[^RD], [Authentication](https://www.rfc-editor.org/rfc/rfc4030.html)[^RI]...

[^SID]: Because *Circuit ID* and *Remote ID* are obviously not good enough ;)

[^RD]: What could be better than using RADIUS _and_ DHCP and passing information between the two in a DHCP option?

[^RI]: Let's reinvent CHAP or 802.1X

### Inter-VRF DHCP Relaying

Let's add another layer of complexity: we want to have DHCP client and DHCP server in different VRFs[^GT]. One could solve this requirement with inter-VRF route leaking (effectively implementing _common services_ VRF), but then you couldn't have overlapping IP address space in the client VRFs. Time for more DHCP Relay Agent sub-options.

[^GT]: Or have one of them in a VRF and the other one in the global routing table.

Ignoring the endless creativity IETF always demonstrates when it comes to exploring every corner case in the solution space, here are the sub-options we need to implement inter-VRF DHCP relaying:

* [Link selection](https://www.rfc-editor.org/rfc/rfc3527.html) (RFC 3527) replaces the **giaddr**-based subnet selection functionality when the DHCP relay decides it makes sense to use a different IP address to communicate with the DHCP server.
* [Server Identifier](https://www.rfc-editor.org/rfc/rfc5107.html) (RFC 5107) allows the relaying agent to tell the DHCP server to masquerade as something else.
* [Virtual Subnet Selection](https://www.rfc-editor.org/rfc/rfc6607.html) (RFC 6607) specifies the VRF/VPN from which the DHCP request came from.

In a typical inter-VRF DHCP relaying setup, the DHCP relay would:

* Copy IP address configured on its incoming interface (in customer VRF) into *link selection* and *server identifier* sub-options
* Add VPN identifier (VRF name or ID) as *virtual subnet selection* sub-option
* Set **giaddr** to the IP address of the outgoing interface (in global IP routing table or management VRF).

DHCP server would do its work and send the reply to **giaddr**, which is reachable from the DHCP server. DHCP relay would figure out which VRF and outgoing interface to use from the sub-options received in the DHCP reply (note that it inserted those same options into the DHCP request when relaying it[^SAV]) and forward the reply to the client.

Now for the magic bit: because the DHCP relay asked the server to lie to the client about its real IP address (using *server identifier* sub-option), all subsequent unicast packets are sent  from the client to the DHCP relay which then forwards (relays) them into the DHCP server VRF -- there's no need for inter-VRF route leaking if you have properly-implemented VRF-aware DHCP relay.

Now that we know the relevant DHCP relaying details, it's easy(er) to figure out how to make it work in EVPN/VXLAN environment (or you'll have to wait for the follow-up blog post).

[^SAV]: Ignoring yet another detour: the client VPN/VRF membership could be determined by the DHCP server ;)

{{<next-in-series page="/posts/2023/03/netlab-dhcp-relay.md">}}
### Coming Up Next

Now that we know how DHCP relaying works, it's time to test it in a lab.{{</next-in-series>}}

### Revision History

2023-03-10
: Added option-82 examples
