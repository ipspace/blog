---
title: "Using netlab to Argue with Vendor TAC"
date: 2026-06-04 07:42:00+0200
tags: [ netlab ]
netlab_tag: use
---
A happy [_netlab_](https://netlab.tools) user sent me an unexpected use case: they successfully used its multi-vendor capabilities to argue with a vendor TAC. Here's the gist of the story (edited/anonymized for obvious reasons):

{{<long-quote>}}
They deployed a configuration change that resulted in an unexpected outage. The outage partially disrupted the data center network, so they didn't have the luxury of collecting data and reproducing the issue, as they had to roll back the change as expeditiously as possible.
{{</long-quote>}}
<!--more-->
So far so good. These things happen. Unfortunately, the next step turned out to be a TAC hell loop.
 
{{<long-quote>}}
A TAC-loop ensued where they kept sending the vendor TAC drawings, **show** command outputs illustrating the problem, configs, and explanations, but the TAC engineers kept asking for more data. Of course, tech support dumps being amongst that. One of them even persisted in calling the situation 'works as expected.'
{{</long-quote>}}

They were probably also asked to upgrade the software and reload the boxes 🤦‍♂️. I've been in similar situations several times, but in those days, we didn't have virtual network devices. Now we do ;)

{{<long-quote>}}
They subsequently recreated the physical topology in a _netlab_ lab with the minimum of devices. Their setup was simple enough that they could use the standard _netlab_ functionality to recreate the bug, and as expected, Arista cEOS and FRR didn't cause an outage. Grumpily (so the user), they jumped through the hoops to netlab-up with vendor devices. Lo and behold, the outage could be reproduced.

Instead of continuing the never-ending TAC discussions, they sent the vendor TAC team the _netlab_ topology file and asked them to reproduce the issue on their own.
{{</long-quote>}}

**Note:** *jumping through the hoops* was caused by _netlab_ failing to install libvirt on a Ubuntu 25.04 VM with nested virtualization. The root cause might have been the *netlab* installation script (now fixed) that was never tested on Ubuntu versions newer than 24.04.

Anyway, two weeks later, I received a wonderful follow-up message:

{{<long-quote>}}
After sending vendor TAC the _netlab_ topology.yml, they had to admit the issue, and they have escalated it to the engineers working on the software :-) There is some talk about an esoteric/hidden nerd knob 🤢, but the main point is that _netlab_ helped to return the TAC ping-pong conversation to something productive!
{{</long-quote>}}

Have you used _netlab_ in an interesting or unexpected way? Please let me know.