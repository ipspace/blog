title: Path MTU Discovery
publish: 2019-09-02

The early IPv4 host implementations were extremely simple: if the destination IPv4 address was directly connected, the interface MTU size was used; otherwise the MTU was fixed at 576 bytes. This algorithm proved impractical in both low-speed networks due to extra overhead introduced by small packet sizes as well as in high-speed networks due to extra CPU utilization required to process the same amount of data. Furthermore, as the routers started being used to connect LAN segments (for example, in collapsed backbone scenarios), the usage of small packet sizes between LAN segments was bordering on ridiculous.

INFO: The overhead of the 40 bytes of IPv4 and TCP headers in a 576-byte packet is 7.5% (<sup>40</sup>/<sub>532</sub>), the same overhead in a 1500-byte packet is 2,7%.

The imperfect solution that was proposed almost 30 years ago is still present in modern TCP implementations: IP end-hosts detect the end-to-end MTU size with *Path MTU discovery*, defined in [RFC 1191](https://tools.ietf.org/html/rfc1191). The Path MTU Discovery (PMTUD) relies on the following properties of the IP and ICMP protocols:

- The sending host can indicate that its IP datagrams shall not be fragmented by setting the *Don’t Fragment (DF)* bit in each outgoing datagram.
- The intermediate routers that have to drop oversized IP datagrams they cannot fragment (due to DF bit or protocol version) inform the sending host that the datagram has been dropped with an ICMP Destination Unreachable message with the status code *Fragmentation needed and DF set*.
- An extra field in the ICMP response indicates the maximum MTU the sending router could support on the outgoing link.

An IP host using PMTUD performs the following steps:

- Whenever the first PMTUD-aware session with a new destination host is started, the MTU of the outgoing interface is assumed to be the MTU of the overall path.
- All outgoing IP datagrams are sent with the DF bit set.
- Whenever the layer-4 session happens to send an oversized datagram, a router in the path will drop the packet, report that the local egress MTU was exceeded and suggest the new MTU size in the ICMP reply.
- The MTU size reported by an intermediate router is cached as the new MTU for the destination host and all future outgoing datagrams will not exceed that MTU.
- The TCP stack in the originating host or a PMTUD-aware UDP application has to retransmit the data in smaller datagrams.

NOTE: As you can see from the description, the PMTUD is usually a reactive procedure, not an active process by which an IP host would measure the end-to-end MTU. The computed end-to-end MTU is a by-product of sending large datagrams and might not be correct if all the sessions between a pair of end-hosts send only small datagrams. There were, however, IP implementations that continuously pinged the remote host to measure path MTU.

The IP hosts (as well as most of the routers) don’t have the detailed visibility into the structure of the global Internet and the subnet masks associated with the destination IP hosts, therefore the PMTUD has to be performed on a per-destination-host basis. Since the end-to-end paths through the network might change with time, the hosts eventually age out the computed end-to-end MTU values (the timeout recommended in the RFC 1191 is ten minutes), resulting in renewed PMTUD process. Obviously, the decrease in the path MTU due to a routing table change is discovered as soon as the first datagram exceeds the new path MTU.

The effects of the computed path MTU on host applications depends on the transport protocol they are using. TCP sessions use PMTUD transparently, as the TCP protocol models a continuous stream that is not sensitive to packet boundaries. PMTUD is usually built into the TCP stack and can be disabled. For example, you can disable PMTUD a [socket-by-socket basis in Linux](http://linux.die.net/man/7/ip) by setting the IP\_MTU\_DISCOVER option. The end-to-end MTU for TCP sessions can also be influenced with the TCP Maximum Segment Size (MSS) option that indicates the maximum segment size (not considering IP or TCP options) that the sender of the TCP MSS option is able to receive; outbound datagrams use the smaller remote MSS value and path MTU value.

UDP-based applications control their own datagram size and can only be assisted by the operating system:

- If an UDP application sends IPv4 datagrams without the DF bit set, they are propagated as required and fragmented within the network as needed.
- An UDP application can decide to rely on PMTUD by indicating that its outgoing datagrams shall have the DF bit set. This is usually done with a *setsockopt* call setting the IP\_DONTFRAGMENT option (Windows) or IP\_MTU\_DISCOVER option (Linux).
- As soon as the UDP application has indicated it wants to use the PMTUD, all the outgoing datagrams are sent with the DF bit set, potentially resulting in dropped UDP packets.

NOTE: If the UDP application tries to exceed the locally computed path MTU, the outgoing message will be rejected immediately. If an intermediate router drops the UDP packet and reports the local MTU with ICMP Destination Unreachable message, no indication is sent to the UDP application (even though the local path MTU is updated); it has to perform its own retransmission.

## Notes

* Path MTU discovery does not work for IP multicast - routers do not generate ICMP messages in response to dropped IP multicast packets.
* Windows has two [socket options](https://docs.microsoft.com/en-us/windows/win32/winsock/ipproto-ip-socket-options): IP_DONTFRAGMENT sets DF bit and works only for UDP and ICMP sockets, IP_MTU_DISCOVER controls the path MTU discovery (according to Windows documentation enabled by default).

## TCP MSS Example

Imagine a simple network with two LAN segments with mismatched MTU sizes - Segment A (with host A) has MTU set to 9000, Segment B (with host B) has MTU sent to 1500.


    +------+      +------+      +------+
    |Host A|      |Router|      |Host B|
    +--+---+      ++----++      +---+--+
       |    9000   |    |   1500    |
    +--+-----------++  ++-----------+--+


When a TCP session is established between Host A and Host B, Host A sets MSS to 8960 (MTU - 40 bytes) while Host B sets MSS to 1460. Host A sends 1460-byte long TCP segments to Host B due to MSS setting, Host B sends 1460-byte long TCP segments to Host A due to interface MTU setting.