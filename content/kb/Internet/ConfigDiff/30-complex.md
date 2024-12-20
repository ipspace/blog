---
kb_section: ConfigDiff
minimal_sidebar: true
pre_scroll: true
title: Order-Sensitive Configurations
date: 2025-03-12 07:51:00+0100
---
Based on the first tests, it was obvious that the Contextual Configuration Diff feature correctly identifies most of the changes made to the Cisco IOS configuration. It was time to stress-test this feature with configuration structures that are order-sensitive. I’ve started with traditional IP access lists:

{{<cc>}}Startup configuration{{</cc>}}
```
access-list 101 permit tcp any any eq www
access-list 101 permit icmp any any
```

{{<cc>}}Running configuration{{</cc>}}
```
access-list 101 deny tcp host 10.0.0.2 host 192.168.0.2 eq www
access-list 101 permit tcp any any eq www
access-list 101 permit icmp any any echo
```

Even such a basic example exposes an inherent weakness in the contextual differences. While the removals and additions in configuration files are correctly identified (but then any *diff* program would be able to do the same), you are not warned that the meaning of the **access-list** has changed drastically, as access list rules were inserted and/or reordered:

{{<cc>}}Reported changes in a traditional access list{{</cc>}}
```
fw#whatsnew
Contextual Config Diffs:
+access-list 101 deny tcp host 10.0.0.2 host 192.168.0.2 eq www
+access-list 101 permit icmp any any echo
-access-list 101 permit icmp any any
```

{{<note>}}By this time, I was tired of typing the same long command over and over again, so I decided to make an alias for it with the **alias exec whatsnew show archive config differences nvram:startup-config system:running-config** configuration command.{{</note>}}

Recent Cisco IOS XE releases don't have the same limitation as the parser automatically migrates traditional ACLs into sequenced named access lists format. These are the results you would get on Cisco IOS XE release 17.12:

{{<cc>}}Reported changes in a traditional access list on a recent Cisco IOS XE release{{</cc>}}
```
fw#whatsnew
!Contextual Config Diffs:
ip access-list extended 101
 +10 deny tcp host 10.0.0.2 host 192.168.0.2 eq www
 +20 permit tcp any any eq www
 +30 permit icmp any any echo
ip access-list extended 101
 -10 permit tcp any any eq www
 -20 permit icmp any any```
```

One would think that the named **ip access-lists**, with their ability to have sequenced rules, would offer much better input to the contextual differences process. After all, it would not be too hard to generate numbered rules that would be nicely inserted into their proper place in the access list. However, this is not how the process works; on Cisco IOS, the results are the same as for traditional access lists:

{{<cc>}}Named access lists: startup configuration{{</cc>}}
```
ip access-list extended Test
 deny   tcp host 10.0.0.2 host 192.168.0.2 eq www
 permit tcp any any eq www
 permit udp any host 192.168.0.2 eq domain
 permit icmp any any
```

{{<cc>}}Named access lists: running configuration{{</cc>}}
```
ip access-list extended Test
 deny   tcp host 10.0.0.3 host 192.168.0.2 eq www
 permit tcp any any eq www
 permit tcp any any eq ftp
 permit udp any host 192.168.0.2 eq domain
 permit icmp any any echo
 deny icmp any any
```

{{<cc>}}Cisco IOS change report after the reconfiguration of a named access list{{</cc>}}
```
fw#whatsnew
Contextual Config Diffs:
ip access-list extended Test
 +deny tcp host 10.0.0.3 host 192.168.0.2 eq www
 +permit tcp any any eq ftp
 +permit icmp any any echo
 +deny icmp any any
ip access-list extended Test
 -deny tcp host 10.0.0.2 host 192.168.0.2 eq www
 -permit icmp any any
```

Yet again, recent Cisco IOS XE releases perform much better as they automatically sequence the entries in the extended ACLs:

{{<cc>}}Cisco IOS XE change report after the reconfiguration of a named access list{{</cc>}}
```
fw#whatsnew
!Contextual Config Diffs:
ip access-list extended Test
 +10 deny tcp host 10.0.0.3 host 192.168.0.2 eq www
 +30 permit tcp any any eq ftp
 +40 permit udp any host 192.168.0.2 eq domain
 +50 permit icmp any any echo
 +60 deny icmp any any
ip access-list extended Test
 -10 deny tcp host 10.0.0.2 host 192.168.0.2 eq www
 -30 permit udp any host 192.168.0.2 eq domain
 -40 permit icmp any any
```

My last access-lists test involved a simple reordering of rules in a named access list:

{{<cc>}}Startup configuration{{</cc>}}
```
ip access-list extended Test
 deny   tcp host 10.0.0.3 host 192.168.0.2 eq www
 permit tcp any any eq www
 permit tcp any any eq ftp
 permit udp any host 192.168.0.2 eq domain
 permit icmp any any echo
 deny icmp any any
```

{{<cc>}}Running configuration{{</cc>}}
```
ip access-list extended Test
 permit tcp any any eq ftp
 deny   tcp host 10.0.0.3 host 192.168.0.2 eq www
 permit tcp any any eq www
 permit udp any host 192.168.0.2 eq domain
 permit icmp any any echo
 deny icmp any any
```

The results produced by a Cisco IOS router were a bit surprising – it did correctly identify that the rules were reordered but also claimed that:

* Two new rules were added to the access list
* No rules were removed (which is obviously incorrect).

{{<cc>}}Incomplete change report after a named access list line reordering{{</cc>}}
```
fw#whatsnew
Contextual Config Diffs:
ip access-list extended Test
 +deny tcp host 10.0.0.3 host 192.168.0.2 eq www
 +permit tcp any any eq www
!
!The following order-dependent line(s) were re-ordered
!ip access-list extended Test
! permit tcp any any eq ftp
```

Yet again, Cisco IOS XE did much better. It did not identify the reordered lines, but the differences it displayed (based on rule numbering) covered all the changes:

{{<cc>}}Cisco IOS XE reporting reordered ACL rules{{</cc>}}
```
fw#whatsnew
!Contextual Config Diffs:
ip access-list extended Test
 +10 permit tcp any any eq ftp
 +20 deny tcp host 10.0.0.3 host 192.168.0.2 eq www
 +30 permit tcp any any eq www
ip access-list extended Test
 -10 deny tcp host 10.0.0.3 host 192.168.0.2 eq www
 -20 permit tcp any any eq www
 -30 permit tcp any any eq ftp
```
