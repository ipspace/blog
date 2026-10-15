---
title: "Crappy Configuration Errors: Cisco Nexus OS Edition"
date: 2026-10-20 07:33:00+0200
tags: [ automation ]
---
**TL&DR:** Programmers writing Cisco Nexus OS code should have known better. They didn't (care?).

One can understand that an operating system written in the late 1980s generates ~~crappy~~ [suboptimal error messages](/2026/10/crappy-cisco-ios-cli-error-reporting/), even though it was known even in those days how to do things right.

Is it too much to hope that the programmers writing newer operating systems (like Cisco Nexus OS) would be better? Obviously, it is 🤦‍♂️
<!--more-->
I decided to implement Netmiko-based configuration for Cisco Nexus OS and tried to figure out the minimum regular expression needed to detect configuration errors. It looked like 'anything starting with a percentage sign' was a good starting point:

```
Enter configuration commands, one per line. End with CNTL/Z.
sw(config)# wrong
              ^
% Invalid command at '^' marker.
```

I did a few other spot checks, and the error messages all followed the same pattern. Cool, we're done (I thought). I ran the integration tests and *all IS-IS tests* failed with a configuration error. Here's the culprit (which appears only the first time you mention IS-IS on a loopback interface):

```
sw# conf t
Enter configuration commands, one per line. End with CNTL/Z.
sw(config)# feature isis
sw(config)# router isis Gandalf
sw(config-router)# !
sw(config-router)# interface loopback0
sw(config-if)# ip router isis Gandalf
%INFO: Command "no isis mtu-check level-2" has no effect on loopback0
```

OK, so I need to match a percentage sign that is *not followed by INFO*. Sure, I can do that. The next thing I know, [@snuffy22](https://github.com/snuffy22) reported [an exception](https://github.com/ipspace/netlab/pull/3936#discussion_r4229236170). It turns out that *some* error messages do not start with the percentage sign:

```
sw(config)# interface ethernet 1/6
sw(config-if)# mtu 5000
ERROR: MTU can only be default or system jumbo MTU
```

The crazy part: that error message appears only if the Nexus OS port has no underlying VM NIC. You can set the MTU on "connected" interfaces, which is why the integration tests never caught this exception:

```
sw(config-if)# interface ethernet 1/1
sw(config-if)# mtu 5000
```

No big deal, I extended the regular expression to match on 'error' regardless of where it appears, and then I stumbled upon a truly disgusting exception:

```
sw(config-if)# interface etherhet 0/0
                         ^
Invalid interface format at '^' marker.
```

The error message looks like any other "invalid something" error message, but whoever wrote it obviously forgot the percentage sign, and whatever tests Cisco runs on Nexus OS never caught this particular blunder.

Based on that, here's the final error-detecting regular expression netlab uses when configuring Nexus OS switches with Netmiko, and I'm even more disappointed in the consistency of Cisco's network operating systems than I was a week ago.

```
error_regexp: [ "^%(?!INFO).*", "(?i:invalid|error).*" ]
```
