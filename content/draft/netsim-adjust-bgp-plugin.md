---
title: "Building a Multi-Platform netsim-tools Plugin"
#date: 2022-05-04 07:11:00
draft: True
tags: [ BGP ]
series: netsim
netsim_tag: extend
---
In January I described how you can [use *netsim-tools* plugins to modify the lab topology transformation behavior](https://blog.ipspace.net/2022/01/netsim-plugins.html) and remove unnecessary IBGP sessions from the [BGP anycast lab](https://blog.ipspace.net/2021/12/bgp-anycast-lab.html). Last week I added multi-platform configuration templates to that same lab. Could we combine the two features and use plugins in a multi-platform lab? 

Of course... and as I spent way too much time working with Perl, there are at least two ways of doing it ;)

## Quick-and-Dirty Solution

