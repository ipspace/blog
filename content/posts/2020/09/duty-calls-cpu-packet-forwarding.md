---
title: "Duty Calls: CPU Is Not Designed for Packet Forwarding"
date: 2020-09-13 10:38:00
tags: [ switching ]
---
Junhui Liu added [this comment](/2020/09/need-smart-nic.html#124) to my _[Where Do We Need Smart NICs?](/2020/09/need-smart-nic.html)_ blog post:

> CPU is not designed for the purpose of packet forwarding. One example is packet order retaining. It is impossible for a multicore CPU to retain the packet order as is received after parallel processing by multiple cores. Another example is scheduling. Yes CPU can do scheduling, but at a very high tax of CPU cycles.

[Duty calls](https://xkcd.com/386/).
<!--more-->
Nobody can argue with the "_CPU is not designed for packet forwarding_" argument. It can, however, be good enough in many cases, and the optimal solution for complex packet forwarding like TCP session termination (including retransmissions), defragmentation, or out-of-order packet processing. All these functions can be hard-coded in an ASIC or NPU, but once the packet forwarding functionality requires a complex algorithm, CPUs tend to be cheaper than the alternatives due to economies of scale.

Also, do keep in mind that most low-speed packet forwarding (up to a few gigabits these days) is done in the CPU. Using a reasonable CPU is cheaper than the alternatives.

How about "_it's impossible to retain packet order in multi-core packet processing_". Doing a bit of research (it took me about 10 minutes, but then I knew where to look) before making broad claims usually helps.

Let's define the problem first. Retaining strict source-to-destination packet ordering across a generic IP network is usually a Mission Impossible, and if [your application requires that, you might be using the wrong transport technology](/2020/05/ip-packet-reordering.html). What we're usually looking for is in-session packet order: packets of a single TCP or UDP session are not reordered while traversing a network.

Now for a tiny dose of reality. I downloaded the [Intel Ethernet Controller I350 Datasheet](https://www.intel.com/content/www/us/en/design/products-and-solutions/networking-and-io/ethernet-controller-i350/technical-library.html?grouping=EMT_Content%20Type&sort=title:asc) (because I couldn't be bothered going through the 1700 pages of XL710 data sheet), browsed through it to find Receive Side Scaling (the functionality that assigns incoming packets to multiple queues which can then be assigned to multiple cores) and found this in the section 7.1.2 of the data sheet:

* Multiple hashing functions are used on incoming packets based on the packet type (TCP, UDP, other IPv4, other IPv6, others). As expected, those hashing functions use the usual 5-tuple for TCP and UDP, and source- and destination IP addresses for other IPv4 and IPv6. Even more, individual hashing functions can be enabled or disabled. For example, you could disable UDP or TCP hash functions if you want to retain strict source-to-destination packet ordering.
* Low-order 7 bits of the 32-bit hash result are used to select an index in the RSS queue indirection table.
* RSS queue indirection table maps hash results into eight queues (RSS Output Index) that can then be assigned to multiple CPU cores.

**Lesson learned**: Intel I350 NIC preserves in-session packet order by storing all packets received from a single session in a single receive queue. If the packet forwarding code in the CPU does not cause packet reordering (and why should it do so if retaining in-session packet order is your goal), you will NOT get in-session packet reordering in a multi-core packet forwarding environment.

![](/2018/10/s500-MythBusted.gif)

What about "_very high tax for scheduling_"? Even my sense of duty is time-limited (and I have a lunch to make), but if you want to know how people with long-time experience in fast CPU-based packet forwarding solve this problem, listen to these Software Gone Wild podcasts:

* [Snabb Switch and NFV on OpenStack](/2014/06/snabb-switch-and-nfv-on-openstack-in.html)
* [Snabb Switch Deep Dive](/2014/09/snabb-switch-deep-dive-on-software-gone.html)
* [PF_RING Deep Dive with Luca Deri](/2015/04/pfring-deep-dive-with-luca-deri-on.html)
* [x86-Based Switching at Ludicrous Speed](/2016/03/x86-based-switching-at-ludicrous-speed.html)
* [Fast Linux Packet Forwarding with Thomas Graf](/2016/10/fast-linux-packet-forwarding-with.html)

**TL&DL**: CPU cores dedicated to poll-based packet processing