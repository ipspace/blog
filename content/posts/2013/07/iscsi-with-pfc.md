---
date: 2013-07-08 07:31:00+02:00
tags:
- data center
- SAN
- workshop
- QoS
title: iSCSI with PFC?
url: /2013/07/iscsi-with-pfc/
lastmod: 2020-11-19 12:17:00
---
[Nicolas Vermandé](http://uk.linkedin.com/in/vnicolas) sent me a really interesting question: "*I\'ve been looking for answers to a simple question that even different people at Cisco don\'t seem to agree on: Is it a good idea to class IP traffic (iSCSI or NFS over TCP) in pause no-drop class? What is the impact of having both pauses and TCP sliding windows at the same time?*"
<!--more-->
{{<note update>}}2020-11-19: Seems like there's no good answer to this question; see below{{</note>}}

Let's rephrase the question using the terminology Fred Baker used in his [Bufferbloat Masterclass](http://staff.science.uva.nl/~delaat/news/2012-09-27/Bufferbloat_Masterclass.pdf): does it make sense to use lossless transport for elephant flows or is it better to drop packets and let TCP cope with packet loss?

It's definitely not bad to randomly drop an occasional TCP packet of a mouse session -- if you have thousands of TCP sessions on the same link and drop a single packet of one or two sessions to slow them down, the overall throughput won't be affected too much \... and if you randomly hit different sessions at different times, you're pretty close to effective management of a mice aggregate.

Elephants are different because they are rare and important (see also [Storage Networking is Different](/2010/08/storage-networking-is-different/) and [Does Dedicated iSCSI Infrastructure Make Sense?](/2013/03/does-dedicated-iscsi-infrastructure/)) -- dropping a single packet of an elephant iSCSI session could affect thousands of end-user sessions (because the overall disk throughput would go down), more so if you're using iSCSI to access VMware VMFS volumes (where a single iSCSI session carries the data of all VMs running on the vSphere host). 

Classifying iSCSI as lossless traffic class thus seems to make a lot of sense (but see below), and comparing the results of QoS policing (= dropping) versus shaping (= delaying) on a small number of TCP sessions supports the same conclusions.

{{<note info>}}Going back to Fred Baker's Bufferbloat presentation: he claims delay-based TCP congestion control (that you get with PFC) is the most stable approach (assuming the host TCP stack has a reasonable implementation that responds to delays).{{</note>}}

### After Almost a Decade

I never found an authoritative answer to this question, and if you ask a dozen experts you'll get two dozen answers, in particular if you add the _does that mean we need large buffers in data center switches_ question to the mix. In any case, you might find these resources helpful:

* J Metz published fantastic [napkin dialogues](https://blogs.cisco.com/datacenter/the-napkin-dialogues-lossless-iscsi) diving deep into iSCSI details;
* I discussed the "_should we delay or drop_" question with [Thomas Graf](/2017/03/tcp-in-data-center-and-beyond-on/) and [Juho Snellman](/2017/01/to-drop-or-to-delay-thats-question-on/), and the conclusions were that drops are not bad assuming you have a decent TCP stack implementation;
* Google introduced a [totally new TCP congestion control (BBR)](https://blog.acolyer.org/2017/03/31/bbr-congestion-based-congestion-control/) in 2016
* JR Rivers addressed the question of data center buffering in an excellent (and free) *[Networks, Buffers and Drops](https://www.ipspace.net/Networks,_Buffers,_and_Drops)* webinar.

#### More information

Storage networks, iSCSI, FCoE and Data Center Bridging (including PFC) are described in the [Data Center 3.0 for Networking Engineers](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers) webinar.
