---
title: "Names, Addresses and Routes"
comment: |
  In early 2020 I created the _[Network Address Introduction](https://my.ipspace.net/bin/get/Net101/NA1.1%20-%20Network%20Addressing%20Introduction.mp4?doccode=Net101)_ video as part of the _[How Networks Really Work webinar](https://www.ipspace.net/How_Networks_Really_Work)_. This blog post is an edited transcript of the first part of that video.
date: 2023-09-19 05:56:00
tags: [ networking fundamentals ]
---
It always helps to figure out the challenges of a problem you're planning to solve, and to have a well-defined terminology. This blog post will mention a few challenges we might encounter while addressing various layers of the [networking stack](https://blog.ipspace.net/2019/09/on-usability-of-osi-layered-networking.html), from data-link layer and all the way up to the application layer, and introduce the concepts of *names*, *addresses* and *routes*.

[According to Martin Fowler](https://martinfowler.com/bliki/TwoHardThings.html), one of the best quotes I found on the topic originally came from Phil Karlton:
<!--more-->
> There are only two hard things in Computer Science: cache invalidation and naming things.

Jeff Atwood added a slight programming slant to that quote:

{{<figure src="/2023/09/hard-things.png">}}

{{<note>}}I am positive anyone who ever had to deal with C or any other programming language in which array indexes start at zero knows where off by one errors come from.{{</note>}}

In computer networks we have to deal with both of these hard things, starting with _naming things_, which is the core topic of the [Network Addressing](https://my.ipspace.net/bin/list?id=Net101#ADDR) section of the webinar, but we'll also touch on caching. You'd usually encounter cached mappings between names and addresses (DNS cache) or caching mappings between addresses in different networking layers. For example, mappings of layer-3 addresses into layer-2 addresses would be stored in ARP/ND cache.

Terminology first. John F. Shoch nailed it in **[IEN 19](https://www.rfc-editor.org/ien/ien19.txt)[^IEN]** (published in January 1978):

[^IEN]: IEN stands for Internet Experiment Note -- the documents that were written before RFC documents started to be written, from times when internet was still considered an experiment.

* A name of a resource indicates what we seek
* An address where it is
* A route tells us how to get there.

For example, your first and last name would be the name of the resource. I want to talk to you, so you are the one I'm seeking. Assuming I want to drive over and have a chat with you, I need your address -- the usual street address, town, and country. That's where you are. Finally, I enter those details into Google Maps (or whatever your preferred mapping app might be) and I get a route -- it tells me how to get from where I'm sitting to where I can meet you

The sad part: more than 45 years ago, someone precisely summarized what we've been struggling with forever[^AN], we all ignored what he wrote, and we're still struggling with it. We are still not willing to admit that we have to have three different concepts[^LISP].

[^AN]: Including using IP addresses as names

[^LISP]: Technologies like LISP try to work around the problem by having two layers of IP addresses, one layer serving as names, the other one as transport endpoints.

Back to what John F. Shoch wrote. A name (he wrote) is usually human readable string -- today we'd call it a host name or URL -- identifying a resource or a set of resources. If you want to make any use of that name, like connecting to that resource, it must be mapped into an address. Interestingly, as early as 1978, mr. Shoch identified a very important point: an address associated with a name may change over time. A resource can be moved from one host to another or the host might get a different network layer address.

Address, on the other hand, is just some data structure. It's supposed to be machine readable -- after all, the packets sent from me to you have to be parsed by the machines called routers sitting in the middle. Obviously, if we want the packet to get from here to there, then everyone in the whole domain has to recognize what that data structure is and has to be able to understand the data structure. The global Internet would be such a domain.

If on the other hand, we're talking about MPLS transport networks, then an MPLS network would be such a domain, and everyone would have to recognize the format of an MPLS label. Similarly, a Wi-Fi network would be a layer-2 domain and everyone within that layer-2 domain would have to agree on how to parse the Wi-Fi MAC addresses. 

An address therefore defines an addressable object (we'll go into what they are in the next blog post). Most importantly, it must be meaningful throughout a domain -- everyone has to agree what addresses mean -- and must be drawn from uniform address space[^MAD]. Every node within a domain must agree on the address space and everyone has to use the same address space if we want to get somewhere.

[^MAD]: Ignoring for the moment locally-significant MPLS labels ;), or you could argue that the addressing domain of the traditional MPLS is a single link between adjacent nodes.

Finally some food for thought: if your network is using private (RFC 1918) IPv4 addresses, is it in the same domain as the global Internet? They must be different domains as the address space is not uniform[^MPA], and the private IP addresses are not meaningful on the global internet. We'll cover the implications of this fact when we get to Network Address Translation (NAT) section where we'll discuss the interesting question of connecting the two domains.

[^MPA]: Multiple networks can use the same RFC 1918 addresses.

{{<next-in-series page="/posts/2023/09/addresses-in-network-stack.md">}}**Coming up next:** What addresses do we need?{{</next-in-series>}}
