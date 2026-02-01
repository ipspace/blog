---
title: "Interface MAC Address in IOS Layer-2 Images"
date: 2026-02-03 08:08:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
Here's another "You can't make this up, but it sounds too crazy to be true" story: Cisco IOS layer-2 images change the interface MAC address when you change the interface **switchport** status.

Let me start with a bit of background:

* IOL Layer 2 image starts with interfaces enabled and in bridged (**switchport**) mode ([details](/2025/03/stupid-bridges-strike-again/))
* _netlab_ has to run a *normalize* script (applicable to IOLL2, IOSv L2, and Arista EOS) before configuring anything else to ensure all interfaces are shut down.
* The IOLL2 `normalize` Jinja template had a bug -- when setting the interface MAC address, it checked `l.mac_address` instead of `intf.mac_address`. Nevertheless, everything worked because the MAC addresses were also set during the initial device configuration.
<!--more-->
Having a bit of a tidiness OCD, I decided to fix the code (changing `l.mac_address` into `intf.mac_address`), and all of a sudden, the MAC addresses were no longer in the device configuration.

The root cause turned out to be a quirk in how Cisco IOS layer-2 images handle interface MAC addresses:

* A MAC address is tied to the interface **switchport** status
* When the **switchport** status changes, the interface MAC address changes.
* Which **mac-address** command appears in the device configuration depends on the **switchport** status.

Sounds crazy? Let me show you. Here's a printout from a freshly-booted IOL layer-2 container:

```
r#show run int eth 0/1
Building configuration...

Current configuration : 29 bytes
!
interface Ethernet0/1
end
```

Let's change the interface MAC address and verify that it's there:

```
r#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
r(config)#interface ethernet 0/1
r(config-if)#mac-address cafe.0bad.0001
r(config-if)#do show run interface ethernet 0/1
Building configuration...

Current configuration : 57 bytes
!
interface Ethernet0/1
 mac-address cafe.0bad.0001
end
```

So far, so good. Now, let's change the interface **switchport** status:

```
r(config-if)#no switchport
r(config-if)#do show run interface ethernet 0/1
Building configuration...

Current configuration : 59 bytes
!
interface Ethernet0/1
 no switchport
 no ip address
end
```

MAGIC!!! The **mac-address** command is gone. Let's set it to something else:

```
r(config-if)#mac-address 00bd.cafe.0042
r(config-if)#do show run interface ethernet 0/1
Building configuration...

Current configuration : 87 bytes
!
interface Ethernet0/1
 no switchport
 mac-address 00bd.cafe.0042
 no ip address
end
```

Looks good, the **mac-address** is there, but what happens if we go back to a **switchport** interface?

```
r(config-if)#switchport
r(config-if)#do show run interface ethernet 0/1
Building configuration...

Current configuration : 57 bytes
!
interface Ethernet0/1
 mac-address cafe.0bad.0001
end
```

🤦‍♂️ 🤦‍♂️ 🤦‍♂️ (we need an emoji for those moments when a single facepalm wouldn't be enough) You get the point, right? 

Finally, let me explain how Cisco IOS and Ansible conspired to "make my day 🤦‍♂️". This was the interface configuration in the fixed `normalize` configlet (applied first):

```
interface Ethernet0/1
 mac-address caf0.0084.0001
```

This is what the initial device configuration looked like (applied next):

```
interface Ethernet0/1
 no switchport
 mac-address caf0.0084.0001
```

And this is the final device configuration:

```
interface Ethernet0/1
 no switchport
```

Can you guess how that happened (before glancing at the following paragraph)?

OK, here's the spoiler:

* Ansible compares the existing device configuration to the changes you want to make
* It applies only the "real" changes (and sets the "changed" flag if needed)
* In our scenario, Ansible decided to apply **no switchport** interface configuration command, but not the **mac-address** one (because it was already configured).
* Cisco IOS switches the MAC addresses, and because the MAC address of the L3 interface was never defined, the **mac-address** command is not in the device configuration (the interface uses the default MAC address)
* Ansible has no chance of realizing that, and so does not apply the new (old) MAC address.

Fun times working with devices that are so "consistent", right?
