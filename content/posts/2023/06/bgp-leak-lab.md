---
title: "Exercise: Fix BGP Route Leaks"
date: 2023-06-14 06:33:00
tags: [ netlab, BGP ]
netlab_tag: use
---
I created a [*netlab* topology](https://github.com/ipspace/netlab-examples/tree/master/BGP/Route-Leaks) you can use to practice BGP security tools I described in the [Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security) webinar:

* The lab topology mirrors the sample topology I described in the [Classification of BGP Route Leaks (RFC 7908)](/2023/06/bgp-route-leak-classification.html) blog post with one router per autonomous system
* BGP is configured on all devices, and EBGP sessions are set up between all directly-connected devices.
<!--more-->
{{<figure src="/2023/06/leak-practice-lab.png" caption="Lab topology (unfortunately turned around)">}}

Autonomous systems advertise prefixes from three address ranges:

| AS type           | Address range |
| ----------------- | ------------- |
| Transit providers | 172.16.0.0/16 |
| Regional ISPs     | 172.17.0.0/16 |
| Customers         | 172.18.0.0/16 |
{.fmtTable}

I also created a custom configuration template that reflects a typical ISP setup:

* Customer routes have BGP local preference 200. It's always best to send traffic over links someone else is paying for.
* Peer routes have BGP local preference 150. It's better to send traffic over zero-settlement links than over links where we have to pay for transit.
* Routes received from transit providers have default local preference. They are used only when we have no customer- or peer routes to a destination.

While you can use the lab with any [supported device](https://netlab.tools/platforms/), I created the custom configuration template for FRR containers, Cumulus Linux, and Arista EOS.

I did not configure any BGP route filters, so you'll get tons of "simple" route leaks from customers and peers, giving you plenty of opportunity to figure out how to stop them. On top of that:

* One of the customers announces way too many prefixes (a customer shall not advertise more than two prefixes)
* An ISP is advertising a /25 prefix that should not be propagated in the global Internet
* Another ISP is advertising an internal prefix from the 10.0.0.0/8 block
* One of the customers is advertising a prefix that belongs to an ISP (you'll notice the same prefix is advertised as belonging to two different autonomous systems).

The optimal way to run the lab is with Linux containers:

* [Create a Ubuntu VM](https://netlab.tools/install/ubuntu-vm/) and use netlab installation scripts to install all the software you need. Please note that you don't need nested virtualization if you run network devices as containers.
* Optional: [download and install Arista cEOS container](https://netlab.tools/labs/ceos/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/BGP/Route-Leaks/topology.yml) from GitHub into an empty directory.
* Start the lab with **netlab up**
* Enjoy!
