---
title: "How Ansible Configuration Parsing Made Me Pull My Hair Out"
date: 2020-12-21 09:06:00
tags: [ Ansible ]
---
Yesterday I wrote a frustrated tweet after wasting an hour trying to figure out why a combination of OSPF and IS-IS routing worked on Cisco IOS but not on Nexus OS. Having to wait for a minute (after Vagrant told me SSH on Nexus 9300v was ready) for NX-OS to "boot" its Ethernet module did't improve my mood either, and the inconsistencies in NX-OS interface naming (_Ethernet1/1_ is uppercase while _loopback0_ and _mgmt0_ are lowercase) were just the cherry on top of the pile of ****. Anyway, here's what I wrote:

> Can't tell you how much I hate Ansible's lame attempts to do idempotent device configuration changes. Wasted an hour trying to figure out what's wrong with my Nexus OS config... only to find out that "interface X" cannot appear twice in the configuration you want to push.

Not unexpectedly, I got a few (polite and diplomatic) replies from engineers who felt addressed by that tweet, and less enthusiastic response from the product manager (no surprise there), so it's only fair to document exactly what made me so angry.

**Update 2020-12-23**: In the meantime, [Ganesh Nalawade](https://github.com/ganeshrn) already [implemented a fix](https://github.com/ansible-collections/ansible.netcommon/pull/190) that solves my problem. Thanks you, awesome job!
<!--more-->
### Background

Managing parts of network device configuration with a network automation tool is a major PITA. Junos makes it relatively easy as it treats a device configuration as a data model, allows you to modify the candidate data model in any way you wish, and shows you the differences between candidate and actual configuration. Arista EOS is pretty close. Most everything else is a nightmare of carefully orchestrated steps trying to get from here to there without cutting yourself off or bricking the box. No news here, I [wrote about this in 2016](/2016/10/network-automation-rfp-requirements.html) (not that it helped).

Anyway, there are two ways to deal with this crapscape. You could say "_it's a vendor problem, and we recommend you create the whole configuration from scratch and replace it_" (the NAPALM/Nornir way) or you could say "_look, I solved this problem for you_" (the Ansible way)... but if you decide to do the latter, it helps if you do it right.

### The Problem

I wanted to push a configuration snippet configuring OSPF and IS-IS routing to a network device. In this blog post I'm using the Cisco IOS version of the template, but Cisco IOS, Cisco Nexus OS and Arista EOS all exhibit the same behavior (at least it's consistent). 

{{<cc>}}Routing configuration template{{</cc>}}
```
router ospf 1
!
interface loopback0
 ip ospf 1 area 0.0.0.0
!
{% for l in links %}
interface {{ l.ifname }}
 ip ospf 1 area 0.0.0.0
{% endfor %}
!
router isis fabric
 is-type level-2
 net 49.0000.0000.{{ '%04d'|format(id) }}.00
!
interface loopback0
 ip router isis fabric
!
{% for l in links %}
interface {{ l.ifname }}
 ip router isis fabric
{% endfor %}
```

The above Jinja2 template generates these configuration commands that should be pushed to a Cisco IOS device with **ios_config** module (using Jinja2 template as the **src** parameter):

{{<cc>}}Desired Cisco IOS configuration{{</cc>}}
```
router ospf 1
!
interface loopback0
 ip ospf 1 area 0.0.0.0
!
interface GigabitEthernet0/1
 ip ospf 1 area 0.0.0.0
interface GigabitEthernet0/2
 ip ospf 1 area 0.0.0.0
!
router isis fabric
 is-type level-2
 net 49.0000.0000.0003.00
!
interface loopback0
 ip router isis fabric
!
interface GigabitEthernet0/1
 ip router isis fabric
interface GigabitEthernet0/2
 ip router isis fabric
```

And this is what the **ios_config** module really does:

{{<cc>}}Where did it manage to lose all the interface sections{{</cc>}}
```
TASK [cisco.ios.ios_config] *****************************************************
changed: [ios] => changed=true
  ansible_facts:
    discovered_interpreter_python: /usr/bin/python3
  banners: {}
  commands:
  - router ospf 1
  - interface loopback0
  - ip ospf 1 area 0.0.0.0
  - interface GigabitEthernet0/1
  - ip ospf 1 area 0.0.0.0
  - interface GigabitEthernet0/2
  - ip ospf 1 area 0.0.0.0
  - router isis fabric
  - is-type level-2
  - net 49.0000.0000.0003.00
  - interface loopback0
  - ip router isis fabric
  - ip router isis fabric
  - ip router isis fabric
  updates:
  - router ospf 1
  - interface loopback0
  - ip ospf 1 area 0.0.0.0
  - interface GigabitEthernet0/1
  - ip ospf 1 area 0.0.0.0
  - interface GigabitEthernet0/2
  - ip ospf 1 area 0.0.0.0
  - router isis fabric
  - is-type level-2
  - net 49.0000.0000.0003.00
  - interface loopback0
  - ip router isis fabric
  - ip router isis fabric
  - ip router isis fabric
```

You might notice that the commands extracted from my configuration template by Ansible **ios_config** module correctly select various interfaces when I mention them for the first time (OSPF configuration), and then _select the first interface and apply configuration commands for all subsequent interfaces to that one_ when I mention them the second time (IS-IS configuration).

And this is where I went into [Artur Bergman mode](https://www.youtube.com/watch?v=oebqlzblfyo). Seriously, WTF??? The second time I specify I want to configure an interface **the interface selection command is simply dropped**... but not for **loopback0** but for all subsequent interfaces???

Obviously there are tons of ways to work around this behavior ([Jeroen van Bemmel suggested the most appropriate one](https://twitter.com/jbemmel/status/1340890305814556672)), and after I realized what's going on it took me a minute to implement a workaround, but I still think that a network automation platform that claims to do partial configuration updates on a network device should do better than what I experienced.

Dear Ansible team:

* Sections in device configurations are there for a reason. They have to be parsed as sections, not as meaningless text strings. Oh, and while I'm mentioning it, you might also want to focus on the concept of *indentation* instead of taking the easy way out comparing strings (and treating two leading whitespaces as being a different configuration command than the same command having one leading whitespace).
* I understand that you might NOT want to treat device configurations as data models, but in that case PLEASE fail with an appropriate error message instead of doing the worst thing possible: mangling my device configuration.
* It helps if you fail consistently. Configuring something on one interface but not on others *with no warning* is the absolute worst thing you could do.

Finally, am I really the only one unfortunate or stupid enough to stumble upon this? The network device configuration modules were added to Ansible release 2.1 almost half a decade ago, and I'm running release 2.10.3... and nobody ever complained about this?

### How Realistic Is This Example?

Yes, I am snarky and grumpy, but No, I didn't try to break Ansible. The template I created reflects the way I was thinking at the moment (focused on routing protocols)... and we could go into endless debates of whether it's better to group everything related to one protocol (Junos way) or to group everything related to one interface (Cisco IOS way). Some such debates started in [18th century](https://en.wikipedia.org/wiki/Gulliver's_Travels) and still [haven't come to a conclusion](https://en.wikipedia.org/wiki/Endianness).

In this particular case, I find the OSPF-versus-IS-IS way of thinking cleaner than the workaround I had to implement with tons of IF statements inside an interface configuration block.

Regardless, I understand that every tool has limitations and cannot be pushed beyond a breaking point, the real question is *how* it breaks, and Ansible broke in a truly horrible way.

### Why Did It Work in the First Place?

Got so far? You might wonder why I got OSPF and IS-IS running on Cisco IOS, but not on Nexus OS. 

Being lazy, I enabled OSPF with the **network** command on Cisco IOS, so I only configured each interface once in my Cisco IOS template. The same approach cannot be used on Nexus OS where you have to enable OSPF _and_ IS-IS on individual interface. Kaboom...

### Release History

2020-12-21
: Added _How Realistic Is this Example_ section after receiving several _why are you doing things this way_ or _it's not Ansible that's broken but your template_ replies on Twitter.

2020-11-23
: Added a link to a pull request fixing the problem by Ganesh Nalawade