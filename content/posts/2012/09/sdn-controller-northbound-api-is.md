---
cdate: 2022-07-19
comment: 'Open Networking Foundation (ONF) created a ginormous amount of OpenFlow
  hype, declared Mission Accomplished, and never even tried to focus on what interface
  the SDN controllers will offer to the outside world.


  Nor surprisingly, every controller vendor used a different API, creating [another
  layer of lock-in](/2015/01/lock-in-is-inevitable-get-used-to-it.html), but ONF never
  cared about that, because the most influential founding members planned to write
  their own controllers anyway.


  A decade after I wrote this blog post the debate is moot -- there are not enough
  OpenFlow controllers out there to worry about being lock-in -- but we''re experiencing
  the same dilemma  in network automation and intent-based networking space.


  On a totally unrelated note, nothing ever came out of Cisco ONE marketing machinery,
  but we did get REST API on Nexus OS and decent NETCONF on Cisco IOS XE.

  '
date: 2012-09-27 06:48:00+02:00
openflow_101_tag: ugly
series:
- openflow_101
series_weight: 150
tags:
- SDN
- OpenFlow
title: SDN Controller Northbound API Is the Crucial Missing Piece
url: /2012/09/sdn-controller-northbound-api-is.html
---
Imagine you'd like to write a simple Perl (or Python, Ruby, JavaScript -- you get the idea) script to automate a burdensome function on your server (or router/switch from any vendor running Linux/BSD behind the scenes) that the vendor never bothered to implement. The script interpreter relies on numerous APIs being available from the operating system -- from process API (to load and start the interpreter) to file system API, console I/O API, memory management API, and probably a few others.

Now imagine none of those APIs would be standardized (various mutually incompatible dialects of Tcl used by Cisco IOS come to mind) -- that's the situation we're facing in the SDN land today.
<!--more-->
If we accept the analogy of OpenFlow being the x86 instruction set (it's actually more like the [p-code machine](http://en.wikipedia.org/wiki/P-code_machine) from [UCSD Pascal](http://en.wikipedia.org/wiki/UCSD_Pascal) days, but let's not go there today), and all we want to do is to write a simple script that will (for example) redirect the backup-to-tape traffic to secondary path during peak hours, we need a standard API to get the network topology, create a path across the network, and create an ingress Forwarding Equivalence Class (FEC) to map the backup traffic to that path. In short, we need what's called [SDN Controller Northbound API](http://etherealmind.com/northbound-api-southbound-api-eastnorth-lan-navigation-in-an-openflow-world-and-an-sdn-compass/).

### There Is No Standard Northbound API

I have some bad news for you: nobody is working on standardizing such an API (read a [great summary by Brad Casemore](http://nerdtwilight.wordpress.com/2012/09/18/northbound-api-the-standardization-debate/), and make sure to read all the articles he linked to).

Are you old enough to remember the video games for early IBM PC? None of them used MS-DOS. They were embedded software solutions that you had to boot off a floppy disk (remember those?) and then they took over all the hardware you had. That's exactly what we have in the SDN land today.

Don't try to tell me I've missed [Flowvisor](https://openflow.stanford.edu/display/DOCS/Flowvisor) -- an OpenFlow controller that allocates slices of actual hardware to individual OpenFlow controllers. I haven't; but using Flowvisor to solve this problem is like using Xen (or KVM or ESXi) to boot multiple embedded video games in separate VMs. Not highly useful for a regular guy trying to steer some traffic around the network (or [any one of the other small things that bother us](/2011/11/openflow-enterprise-use-cases.html)), is it?

Also, don't tell me each SDN controller has an API. While NEC and startups like Big Switch Networks are creating something akin to a network operating system that we could use to program our network (no, I really don't want to deal with the topology discovery and fast failover myself), and each one of them has an API, no two APIs are even remotely similar.

I still remember the days when there were at least a [dozen operating systems running on top of 8088 processor](http://www.csee.wvu.edu/~jdm/classes/cs258/OScat/micros.html), and it was a mission impossible to write a meaningful application that would run on only a few of them without major porting efforts.

### Let's Speculate

There might be several good reasons for the current state of affairs:

-   The only people truly interested in OpenFlow are the [Googles of the world](/2012/05/openflow-google-brilliant-but-not.html) ([Nicira is using OpenFlow](/2012/02/nicira-bigswitch-nec-openflow-and-sdn.html) purely as an information transfer tool to get MAC-to-IP mappings into their vSwitches);
-   Developers love using standard libraries and APIs other people created, and figure out all sorts of excellent reasons why their dynamic and creative work couldn't possibly be hammered into tight confines of a standard API;
-   Nobody is [interested in creating a Linux-like solution](http://www.forbes.com/sites/ciocentral/2012/04/03/be-wary-of-geeks-bearing-gifts/); everyone is striving to achieve the maximum possible vendor lock-in;
-   We still [don't know what we're looking for](http://en.wikipedia.org/wiki/Blind_men_and_an_elephant).

The reality is probably a random mixture of all four (and a few others), but that doesn't change the basic facts: until there's a somewhat standard and stable API (like SQL-86) that I could use with SDN controllers from multiple vendors, I'm better off using Cisco ONE or Junos XML API, otherwise I'm just [trading lock-ins](http://it20.info/2012/02/the-abc-of-lock-in/) (as ecstatic users of umbrella network management systems would be more than happy to tell you).

On the other hand, if I stick with Cisco or Juniper (and implement a simple abstraction layer in my application to work with both APIs) at least I could be pretty positive they'll still be around in a year or two.
