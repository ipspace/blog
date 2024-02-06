---
title: "Removing FRRouting Configuration Is Not Idempotent"
date: 2024-02-07 08:22:00+0100
tags: [ BGP ]
---
One of the few beauties of most "industry standard CLI" implementations[^ISC] is that they're idempotent: nothing changes (apart from ACLs) if you configure the same stuff a dozen times. Most of these implementations allow you to deconfigure the same stuff multiple times; FRRouting is one of the unfortunate exceptions.

{{<note>}}I'm not saying what FRRouting does is wrong. It's just different and a bit unexpected once you get into the mindset of "Wow, it looks almost like Cisco IOS."{{</note>}}

[^ISC]: An industry-wide euphemism for "_our box looks like Cisco IOS, but we're not allowed to say so_."

### What Am I Talking About?

Imagine you have a bunch of IP prefixes you want to advertise with BGP. You could use **network** statements within the **router bgp** configuration to get that done:
<!--more-->
```
router bgp 65100
 !
 address-family ipv4 unicast
  network 10.42.1.0/24
  network 10.42.2.0/24
  network 10.42.3.0/24
  network 10.42.4.0/24
  network 10.42.5.0/24
```

You can execute the same configuration commands as often as you wish, and the results won't change.

Now, let's imagine you want to remove those prefixes. No problem; prepend **no** to the **network** commands.

```
router bgp 65100
 !
 address-family ipv4 unicast
  no network 10.42.1.0/24
  no network 10.42.2.0/24
  no network 10.42.3.0/24
  no network 10.42.4.0/24
  no network 10.42.5.0/24
```

Cisco IOS/IOS-XE or Arista EOS accept those commands regardless of how many times you execute them, but here's what you might get if you try to execute them twice on a Linux box running FRRouting:

```
customer(bash)#vtysh -f /tmp/nonet.cfg
[555|mgmtd] sending configuration
[556|zebra] sending configuration
[562|bgpd] sending configuration
[570|watchfrr] sending configuration
[572|staticd] sending configuration
Waiting for children to finish applying config...
% Can't find static route specified
line 4: Failure to communicate[13] to bgpd, line:   no network 10.42.1.0/24

% Can't find static route specified
line 5: Failure to communicate[13] to bgpd, line:   no network 10.42.2.0/24

% Can't find static route specified
line 6: Failure to communicate[13] to bgpd, line:   no network 10.42.3.0/24

% Can't find static route specified
line 7: Failure to communicate[13] to bgpd, line:   no network 10.42.4.0/24

% Can't find static route specified
line 8: Failure to communicate[13] to bgpd, line:   no network 10.42.5.0/24

[562|bgpd] Configuration file[/etc/frr/frr.conf] processing failure: 13
[555|mgmtd] done
[556|zebra] done
[570|watchfrr] done
[572|staticd] done
```

{{<note>}}I was sending configuration files to `vtysh` to see which daemon generated the error message. You would get the same results (with less clutter) when executing the **no network** commands interactively.{{</note>}}

**Long story short:** removing **network** commands from BGP configuration is not idempotent on FRRouting.

But wait, that's not all. Those **network** commands relied on **ip address** commands configured on an interface. Maybe the removal of those commands would be idempotent? Let's execute the following sequence twice:

```
interface eth2
 description customer -> stub
 no ip address 10.42.1.1/24
 no ip address 10.42.2.1/24
 no ip address 10.42.3.1/24
 no ip address 10.42.4.1/24
 no ip address 10.42.5.1/24
```

{{<note info>}}Another FRRouting quirk: you can configure multiple IP addresses on an interface without using the **secondary** keyword.{{</note>}}

This is what happens the second time you try to remove the configuration:

```
customer(bash)#vtysh -f /tmp/nonet.cfg
[608|mgmtd] sending configuration
[609|zebra] sending configuration
[615|bgpd] sending configuration
[623|watchfrr] sending configuration
[625|staticd] sending configuration
Waiting for children to finish applying config...
% Can't find address
line 3: Failure to communicate[13] to zebra, line:  no ip address 10.42.1.1/24

% Can't find address
line 4: Failure to communicate[13] to zebra, line:  no ip address 10.42.2.1/24

[608|mgmtd] done
% Can't find address
line 5: Failure to communicate[13] to zebra, line:  no ip address 10.42.3.1/24

% Can't find address
line 6: Failure to communicate[13] to zebra, line:  no ip address 10.42.4.1/24

% Can't find address
line 7: Failure to communicate[13] to zebra, line:  no ip address 10.42.5.1/24

[623|watchfrr] done
[609|zebra] Configuration file[/etc/frr/frr.conf] processing failure: 13
[625|staticd] done
[615|bgpd] done
```

**Another conclusion**: removal of IP addresses is not idempotent either.

What about other configuration bits and pieces? Can I deconfigure the BGP process twice? Nope.

```
customer(bash)#vtysh

Hello, this is FRRouting (version 9.1_git).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

customer# conf t
customer(config)# no router bgp 65100
customer(config)# no router bgp 65100
% Can't find BGP instance
```

### Lesson Learned

While the FRRouting configuration process is idempotent, removing configurations isn't. Don't try to automate FRRouting configuration using the same bag of tricks you'd use on traditional network devices. The only sane workaround seems to be:

* Generate complete configuration files in your automation script;
* Use the FRRouting **reload** functionality to re-read the configuration file(s) and apply changes.

One could make that approach wonderfully modular if only FRRouting supported *include* files like *ifupdown2* does. Alas, that doesn't seem to be the case.

### What Am I Missing?

I hope I missed something. Are you using FRRouting? How do you handle configuration generation/automation? Please leave a comment!