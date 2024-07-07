---
date: 2007-03-14 16:39:00+01:00
tags:
- network management
- command line interface
- configuration
title: Display Configuration of a Single Interface
url: /2007/03/display-configuration-of-single/
---
Displaying configuration of a single interface can be a time-consuming task if your router has extremely long configuration (for example, high-end device with hundreds of interfaces, route-maps, access-lists etc.). In this case, the **interface** keyword of the **show running-config** command becomes extremely useful.
<!--more-->
For example, the **show running-config interface serial 0/0.1** command displays only configuration of the specified interface (without building the whole running configuration)

``` {.code}
POP#show running-config interface serial 0/0.1
Building configuration...

Current configuration : 154 bytes
!
interface Serial0/0.1 point-to-point
 description *** Link to Core-1 ***
 ip address 172.16.1.6 255.255.255.252
 frame-relay interface-dlci 101
end
```
