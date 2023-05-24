title: Network Implications of PMTUD
publish: 2019-09-02

The Path MTU Discovery (PMTUD) is enabled by default in almost all modern TCP/IP implementations; it’s thus mandatory that your packet filters and firewalls don’t block the PMTUD-related ICMP messages. For example, you should include the following two lines into your IP access lists (the second line blocks ICMP fragments that could be used to change the meaning of the ICMP response):

    permit icmp any any packet-too-big
    deny icmp any any fragments

Likewise, you should enable ICMP inspection (available from IOS release 12.3) with the **ip inspect name** ***inspection-name*** **icmp** if you use IOS firewall feature set.

Sometimes, the PMTUD will be broken due to circumstances way beyond your control; for example, the path toward the destination host might include a non-compliant router or the firewall at the other end (protecting the destination server) blocks ICMP messages. In such cases, you can usually get at least the TCP applications working by lowering the TCP MSS value on the router with the **ip tcp adjust-mss** ***maximum-size*** configuration command. The *maximum-size* parameter specifies the maximum TCP payload and has to be at least 40 bytes smaller than the end-to-end MTU. The Cisco IOS documentation is not very specific on where you should apply this command. As it turns out, you can apply it on inbound or outbound interface; MSS value in TCP packets with SYN bit set is modified in the ingress as well as in the egress part of the packet switching path, resulting in the minimum of the two values if the **ip tcp adjust-mss** is specified on both interfaces.

Fixing broken UDP applications is way harder; some of them might set the DF bit but remain oblivious of its implications (sometimes happily assuming 1500-byte end-to-end MTU). If you cannot increase the MTU size, the only reasonable solution in the IPv4 world is to clear the DF bit on the first router with the policy-based routing (there's no equivalent IPv6 hack).

For example, the following configuration clears the DF bit on all UDP traffic entering the router through the Fast Ethernet interface.

    ip access-list extended BrokenUDP
     remark The UDP filter should be more specific
     permit udp any any
    !
    route-map ClearDF permit 10
     match ip address BrokenUDP
     set ip df 0
    !
    interface FastEthernet0/0
     ip address 10.0.0.1 255.255.255.240
     ip policy route-map ClearDF
