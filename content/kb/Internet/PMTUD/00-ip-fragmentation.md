title: Never-Ending Story of IP Fragmentation
index: yes
toc_title: MTU Basics

I first encountered IP fragmentation issues in mid-1990s when people started deploying carelessly designed firewalls that blocked all Internet Control Messages Protocol (ICMP) traffic. One would hope that the situation would get better as network designers and operations engineers gained experience, but it’s constantly getting worse with the introduction of encapsulation techniques like PPP-over-Ethernet (PPPoE) used in DSL connections, IPSec-based encryption, IP-over-IP tunnels used to fix IP routing problems or implement topologies that some “service providers” cannot support, or a dozen IPv6-over-IPv4 or IPv4-over-IPv6 tunneling schemes. In this article, you’ll find the reasons behind IP fragmentation, the detailed description of how *Path MTU discovery* works and the various mechanisms you can use on Cisco routers to alleviate the IP fragmentation-related problems.

INFO: This article was written in 2007, and has been updated and republished on ipSpace.net in 2019. IPv4 and IPv6-specific behavior is pointed out; whenever the article uses IP it means "IPv4 or IPv6".

## MTU Basics

The basic fact in networking is that not all networking technologies were created equal. One of the differences between various layer-2 technologies is the maximum payload (commonly called *Maximum Transmission Unit* – MTU) a layer-2 frame can transport. For example, regular Ethernet packets can be up to 1518 bytes long (including the CRC bytes), but they can transport only a 1500-byte payload if you’re using the default [Ethernet-II encapsulation](https://en.wikipedia.org/wiki/Ethernet_frame#Ethernet_II); the payload size is reduced to 1492 bytes if you use [SNAP encapsulation](https://en.wikipedia.org/wiki/Ethernet_frame#IEEE_802.2_SNAP). Token Ring and FDDI were able to transport much larger packets and the larger packet sizes are sometimes used to reduce the overhead in high-speed or high-volume data transfers.

NOTE: Frames longer than 1518 bytes (called *jumbo* *frames*) are commonly supported in Ethernet environments, but usually not enabled by default.

On the other hand, slow-speed serial links used lower MTU sizes to reduce the serialization delay (transmitting a single 1500-byte packet on a 64 kbps link takes almost 200 milliseconds). Higher link speeds made these tricks and technologies like link fragmentation and interleaving (LFI) over PPP links obsolete.

Encapsulation and tunneling techniques add their own limitations: for example, if you’re using PPP-over-Ethernet, the PPPoE header takes eight bytes from the Ethernet payload, leaving 1492 bytes for the layer-3 packet. Similarly, Generic Route Encapsulation (GRE) uses 24 bytes headers, reducing the MTU on GRE tunnels to 1476 bytes. Obviously, the combination of various encapsulation techniques further reduces the MTU size; the MTU of a GRE tunnel running over an ADSL is 1468 bytes.

INFO: While the GRE header is only four bytes long (unless you use the GRE key, which extends the GRE header to eight bytes), the IPv4-in-IPv4 encapsulation requires an extra IPv4 header (20 bytes), resulting in 24-byte overhead (the overhead is 20 bytes larger when using IPv6 transport). A pure IPv4-over-IPv4 tunnel configured with **tunnel mode ipip** on Cisco IOS has a 20-byte overhead.

IPSec further complicates the MTU calculations, as the size of the IPSec header that is inserted in the IP packet depends on the parameters of the IPsec transform sets (combinations of tunneling mode, encryption, NAT-T usage and variable padding to 8- or 16-byte blocks). The original Cisco IOS paradigm where the encrypted packets are routed through the same interface as non-encrypted traffic does not help either, as there is no longer an interface-wide MTU; the MTU size varies based on whether a packet is encrypted or not.

INFO: We covered the effects of various IPsec transform sets in combination with GRE tunnels
in [DMVPN webinars](https://www.ipspace.net/DMVPN_Technology_and_Configuration).

