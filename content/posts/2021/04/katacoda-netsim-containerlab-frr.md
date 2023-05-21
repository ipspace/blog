---
date: 2021-04-30 07:59:00+00:00
netlab_tag: use
tags:
- netlab
title: 'Katacoda Scenario: netlab with Containerlab and FRRouting'
---
**TL&DR**: If you'd like to see how easy it is to deploy a full-blown OSPF+BGP network with [netlab](https://netlab.tools/) together with [Containerlab](https://blog.ipspace.net/2021/04/netsim-containerlab.html) and FRRouting, check out [this Katacoda scenario](https://katacoda.com/ipspace/scenarios/netsim-containerlab-101).

**What is Katacoda?** An [awesome environment](https://katacoda.com/) that allows content authors to create scenarios running on Linux VMs accessible through a web browser. I can only hope they'll fix the quirks and keep going -- I have so many ideas what could be done with it.

**Why FRR?** Not too long ago [Jeroen van Bemmel](https://www.linkedin.com/in/jeroenvbemmel/) sent me a link to a simple Katacoda scenario he created to demonstrate how to set up **netlab** and **containerlab**. His scenario got the tools installed and set up, but couldn't create a running network as there are almost no usable Network OS images on Docker Hub (that is accessible from within Katacoda) -- the only image I could find was FRR.
<!--more-->
{{<note>}}I totally understand that companies like Cisco,  Arista, or Juniper want people to click _I agree to your licensing terms_ before downloading containers. Unfortunately, that makes their products unusable for online on-demand scenarios. No problem, we'll work on getting people hooked on Linux networking. Speaking of which, I can't grasp why Cumulus releases a Vagrant box, but not a Docker container.{{</note>}}

**Why did it take me more than a day?** The latest FRR Docker image crashed when run in containerlab. [Roman Dodin](https://www.linkedin.com/in/rdodin/) was quick to point out I have to use 7.5.0 image, and I got the whole thing up and running in no time. Next challenge: configuring FRR.

Linux and FRR are great when you grasp the *configurations are files waiting to be replaced* approach, but when you start from the traditional network OS perspective (let's send this bunch of commands to the device to modify what it's doing), and try to implement FRR configuration with the minimum amount of work, you might experience interesting challenges.

In the end, I decided to create **bash** scripts that would be executed within the FRR container, allowing me to use Linux **ip** configuration commands as well as FRR CLI accessible via **vtysh**. It's a dirty hack, but it works. Implementing it in **netlab** was a matter of a few hours, most of the time spent tweaking OSPF, BGP and IS-IS templates.

With FRR being integrated into **netlab**, I had all the components I needed to create a [full-blown OSPF+BGP scenario in Katacoda](https://katacoda.com/ipspace/scenarios/netsim-containerlab-101). Hope you'll enjoy it, and if you have an interesting idea for another similar scenario, just write a comment.

### Useful netlab Links

* [Github repository](https://github.com/ipspace/netlab)
* [Documentation](https://netlab.tools/)
* [Installation guide](https://netlab.tools/install/)
* [Platform support](https://netlab.tools/platforms/)
* [Release notes](https://netlab.tools/release/)

