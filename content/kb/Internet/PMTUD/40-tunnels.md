title: IP Fragmentation and Tunnels
publish: 2019-09-09

The impact of IP fragmentation can be devastating if you use high-speed GRE tunnels or IPSec encryption between routers. By default, routers assume a 1500-byte end-to-end MTU between the tunnel endpoints, resulting in 1476 byte IP MTU on a GRE tunnel interface. The GRE packets generated by the router are usually sent without the DF bit and can be fragmented if an intermediate hop between the tunnel endpoints does not support 1500-byte MTU (for example, a PPPoE DSL connection). The situation becomes even more interesting when you're combining GRE tunnels with IPSec encryption, particularly if the two operations are not performed by the same device.

NOTE: This section of the document describes Cisco IOS behavior. Most other router-based IPsec/GRE implementations are reasonably similar, but may vary in performance impact of IP fragment reassembly.

The GRE or IPsec fragments have to be reassembled on the tunnel tail-end router or IPsec peer, resulting in process switching of all tunneled or encrypted traffic. The process switching is several times slower than CEF switching on software-only platforms, resulting in unexpectedly high CPU load on the tail-end router. The situation is worse on platforms that rely on hardware-based or hardware-assisted packet switching; the switching bandwidth of a high-end router can drop by a factor of hundred or more.

You can solve the GRE-related problems by manually lowering the **ip mtu** on the tunnel interface (ideally in combination with the **ip tcp adjust-mss** configuration command), or you could enable PMTUD for GRE tunnels with the **tunnel path-mtu-discovery** interface configuration command. When you enable the PMTUD on a GRE tunnel, the GRE packets are sent with the DF bit set and the router responds to the incoming ICMP destination unreachable messages with the reduction of the tunnel MTU size. The decreased MTU can only be inspected with the **show interface** command as shown below.

    Rtr#show interface tunnel 0 | include protocol|Path

    Tunnel0 is up, line protocol is up
      Tunnel protocol/transport GRE/IP
      Path MTU Discovery, ager 10 mins, min MTU 92, MTU 776, expires 00:01:57

The Cisco IOS implementation of the tunnel PMTUD is suboptimal (to be polite):

- DF bit is copied from the source IP packet into the GRE envelope. If the source IP packet doesn’t have the DF bit set, it won’t be set in the outgoing GRE packet, potentially resulting in fragmentation of the GRE packet and expensive reassembly on the tail-end router.
- The tunnel PMTUD process is thus triggered only by incoming packets with DF bit set.
- After the end-to-end tunnel MTU has been computed, it’s only applied to the incoming packets with the DF bit set.
- Even if the router knows the correct end-to-end MTU, the incoming packets without the DF bit *are not fragmented*, resulting in GRE packet fragmentation further down the path.

NOTE: Regardless of the tunnel PMTUD algorithm, the router fragments or rejects the
tunneled packets if their size exceeds the IP MTU size configured on the tunnel interface
with the **ip mtu** configuration command.
