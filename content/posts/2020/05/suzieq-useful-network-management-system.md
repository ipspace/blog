---
title: "What If... There Would Be an Easy Way to Run Your Network"
date: 2020-05-11 06:50:00
tags: [ network management ]
---
Imagine a life where you would be able to...

* Find all interfaces that have VRRP configured but no useful VRRP neighbor;
* Find all OSPF adjacencies that should be up but are not;
* Get an alert every time the default IP route is lost;
* Find all MTU mismatches in your network;
* List all VXLAN-to-VLAN mappings across your data center, and find if two different VLANs map into the same VXLAN VNI;
* Compare IP routes in your data center to those you had yesterday;
* Verify that IP routing tables on all spine switches contain the same prefixes;
* Do the same comparison before and after a software upgrade;
* Identify changes in IP routing tables or ARP tables that happened between yesterday evening and this morning;

... and be able to do all that in a multi-vendor environment without writing tons of Ansible playbooks or Python code.
<!--more-->
We all know that most network management products promise a unicorn-powered nirvana, but always fail to deliver because they were designed to impress the CxO controlling the budget, not help the engineers running the network. The last tool that could answer some of these questions was probably NetMRI (no wonder - it was designed by [Terry Slattery](https://www.ipspace.net/Author:Terry_Slattery) of the [Cisco CLI fame](/2019/04/must-watch-history-of-cisco-ios-cli/)), but after it got acquired by Infoblox, that wonderful product (still fondly remembered by its users) got lost in the corporate morass.

There are other products out there that were designed by people who ran actual networks, for example [pmacct](/2014/08/pmacct-traffic-analysis-tool-with/) or [Kentik](https://techfieldday.com/appearance/kentik-presents-at-presents-at-networking-field-day-16/), and after more than a decade (and after surviving the useless SDN craze) it seems we might be getting something even better than NetMRI.

[Recently-released SuzieQ](https://github.com/netenglabs/suzieq) is an extensible framework that allows you to:

* Collect data you think you need from your network (as opposed to what the Product Manager thinks you need);
* Store changes to collected data into a time-series database to give you a long-term history of how your network behaved;
* Query the data in a variety of ways using either a Python API or CLI.

But wait, there's more... you could use built-in tests (*asserts*), or define your own tests to check that your network is not broken (VRRP or OSPF/BGP adjacencies immediately come to mind), and have them executed continuously, alerting you whenever there's a mismatch between your intent (see, I got another hit on the Buzzword Bingo) and the actual network state.

Oh, and did I mention that (contrary to [some other emerging network management products](/2019/11/ip-fabric-with-gian-paolo-boarina-on/)) this one is open-source, so you can extend it in any way you want, and make it do whatever **you** think your network deserves without begging the vendor.

**Long story short**: Stop dreaming about the ideal network management product. [Download SuzieQ](https://github.com/netenglabs/suzieq), [adapt it to your needs, and contribute your changes](https://forwardingplane.net/2018/02/19/strategy-series-build-vs-buy-sorta/). It's time the networking engineers rally around an open-source network management software instead of spending their time collecting vanity points on vendor forums doing unpaid technical support.

Finally, before someone writes a comment saying "_but our intent-based magic can hide all the network complexity and make it work like a charm_" let me reuse the quote from [Luke Gorrie talking about Snabb Switch](/2014/06/snabb-switch-and-nfv-on-openstack-in/) (and its lack of support for overlay virtual networking): SuzieQ is a solution for people who like their network the way it is, not for those who are so ashamed of it that they want to hide it behind another layer of abstraction.