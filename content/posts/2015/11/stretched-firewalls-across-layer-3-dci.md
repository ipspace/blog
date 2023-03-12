---
date: 2015-11-02 13:08:00+01:00
ha-cluster_tag: firewall
high-availability_tag: ignore
series:
- ha-cluster
tags:
- firewall
- data center
- WAN
- high availability
title: Stretched Firewalls across Layer-3 DCI? Will the Madness Ever Stop?
url: /2015/11/stretched-firewalls-across-layer-3-dci.html
---
I got this question from one of my readers (and based on [these comments](https://blog.ipspace.net/2015/10/sometimes-you-have-to-decide-how-badly.html?showComment=1444734501354#c3913979959302428031) he's not the only one facing this challenge):

> I was wondering if you can do a blog post on Cisco\'s new ASA 5585-X clustering. My company recently purchased a few of these with the intent to run their cross data center active/active firewalls but found out we cannot do this without OTV or a layer 2 DCI.

A while ago I [expressed my opinion about these ideas](https://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html), but it seems some people still don't get it. However, a picture is worth a thousand words, so maybe this will work:
<!--more-->
![](/2015/11/s500-Triple-facepalm.jpg)

On a more serious note...

Whenever someone proposes a stupidity like "*let's turn our L3 DCI into L2 DCI so we can run stretched firewall cluster on top of it*", politely ask "*and what happens* [*when (not if) the DCI link fails*](https://blog.ipspace.net/2012/10/if-something-can-fail-it-will.html)*?*" because asking "*what were you smoking*" might sound offensive.

Fortunately for everyone who has to work with real-life networks, Cisco engineers (even those working in marketing) tend to be pretty honest when it comes to how things really work, so it was really easy to answer that question by reading the documentation, [design guides](http://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Data_Center/VMDC/ASA_Cluster/ASA_Cluster/ASA_Cluster.html), and [ASA Clustering Deep Dive](https://www.ciscolive.com/online/connect/sessionDetail.ww?SESSION_ID=76601) Cisco Live session:

-   A failure in communication between different members of the cluster will result in ejection of that firewall from the cluster;
-   CCL (Cluster Communication Link) loss forces the member out of the cluster
-   CCL link loss causes unit to shut down all data interfaces and disable clustering. Clustering must be re-enabled manually after such an event

For those who still don't get it: if you lose the communication between cluster members (which would happen after DCI link failure), the firewalls in one data center **shut down** and **cut that data center off the net**.

Do keep in mind that if you have two data centers with L3 DCI between them, they could work independently after DCI link failure (apart from the potential need to synchronize data between them). Building a firewall cluster on top of L3 DCI is thus a huge step back in terms of failure resiliency.

Finally, here's my message to the vendor sales engineers promoting such stupidities:

![](/2015/11/s500-Enough+of+this+shit.jpg)

