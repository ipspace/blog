---
kb_section: RouterConfigManagement
minimal_sidebar: true
pre_scroll: true
title: Modular Objects
date: 2025-01-15 08:01:00+0100
---
The final group of tests focused on Modular CLI commands (**class-maps** and **policy-maps**). As these structures are used to configure more and more Cisco IOS features (starting with Quality of Service, they are now used for access control, firewall configuration, and a variety of other IOS features), it’s very important that their changes are correctly identified. I’ve started with an easy task – a few classes were added to a policy-map.

{{<cc>}}Startup configuration{{</cc>}}
```
class-map match-all mail
 match protocol smtp
class-map match-all web
 match protocol http
!
policy-map WAN
 class mail
  police rate percent 20
    conform-action transmit
    exceed-action set-prec-transmit 0
    exceed-action set-frde-transmit
 class web
  bandwidth percent 30
```

{{<cc>}}Running configuration{{</cc>}}
```
class-map match-all mail
 match protocol smtp
class-map match-all ServerMail
 match protocol smtp
 match access-group 101
class-map match-all web
 match protocol http
class-map match-all ServerWeb
 match protocol http
 match access-group 101
!
policy-map WAN
 class ServerMail
  priority 64
 class ServerWeb
  bandwidth percent 30
  set precedence 3
 class mail
  police rate percent 20
    conform-action transmit
    exceed-action set-prec-transmit 0
    exceed-action set-frde-transmit
 class web
  bandwidth percent 30
!
access-list 101 permit ip host 10.0.0.2 host 192.168.0.2
access-list 101 permit ip host 192.168.0.2 host 10.0.0.2
```

Not surprisingly, Cisco IOS correctly identified the additions to the running configuration but did not warn me that the new classes were inserted in front of the already-configured ones. Cisco IOS XE release 17.12 did no better; its Contextual Config Difference utility is still unaware that the entries in a policy map are order-dependent.

{{<cc>}}Changes in QoS policy map identified by Cisco IOS{{</cc>}}
```
fw#whatsnew
Contextual Config Diffs:
+class-map match-all ServerMail
 +match protocol smtp
 +match access-group 101
+class-map match-all ServerWeb
 +match protocol http
 +match access-group 101
policy-map WAN
 +class ServerMail
  +priority 64
 +class ServerWeb
  +bandwidth percent 30
  +set precedence 3
+access-list 101 permit ip host 10.0.0.2 host 192.168.0.2
+access-list 101 permit ip host 192.168.0.2 host 10.0.0.2
```

Similar to **access-lists** and **route-maps**, the **policy-maps** are order-dependent; the first **class** in the **policy-map** that matches the packet under inspection specifies the actions performed on the packet. My next test thus involved a misconfigured **policy-map** in **startup-config** that was fixed in the running configuration:

{{<cc>}}Startup configuration{{</cc>}}
```
policy-map WAN
 class mail
  police rate percent 20
    conform-action transmit
    exceed-action set-prec-transmit 0
    exceed-action set-frde-transmit
 class web
  bandwidth percent 30
 class ServerMail
  priority 64
 class ServerWeb
  bandwidth percent 30
  set precedence 3
```

{{<cc>}}Running configuration{{</cc>}}
```
policy-map WAN
 class ServerMail
  priority 64
 class ServerWeb
  bandwidth percent 30
  set precedence 3
 class mail
  police rate percent 20
    conform-action transmit
    exceed-action set-prec-transmit 0
    exceed-action set-frde-transmit
 class web
  bandwidth percent 30
```

The *ServerMail* **class** is a subset of *Mail* **class**. If it’s placed after the *Mail* class in the **policy-map** it will match no traffic at all. The running configuration fixes that mistake, but Cisco IOS release 12.4 failed to identify the change:

{{<cc>}}Cisco IOS release 12.4 fails to identify reordered classes{{</cc>}}
```
fw#whatsnew
Contextual Config Diffs:
!No changes were found
```

Cisco IOS release 15.9 and Cisco IOS XE did a bit better and identified that some reordering took place. However, their reports were highly misleading:

* The **mail** or **web** classes were not added to the policy-map.
* The actions in the **mail** class have not changed.
* Nothing was removed from the **ServerMail** class.

{{<cc>}}Changes reported by Cisco IOS release 15.9 and Cisco IOS XE release 17.12{{</cc>}}
```
fw#whatsnew
!Contextual Config Diffs:
policy-map WAN
 +class mail
  +police rate percent 20
   +conform-action transmit
   +exceed-action set-prec-transmit 0
   +exceed-action set-frde-transmit
 +class web
  +bandwidth percent 30
!
!The following order-dependent line(s) were re-ordered
!policy-map WAN
! class ServerMail
!End of reordered section
!
  -priority 64
!
!The following order-dependent line(s) were re-ordered
!policy-map WAN
! class ServerWeb
!End of reordered section
!
  -bandwidth percent 30
  -set precedence 3
```
