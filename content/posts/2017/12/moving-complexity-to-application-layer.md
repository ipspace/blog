---
date: 2017-12-12 08:53:00+01:00
high-availability_tag: app
tags:
- DNS
- Internet
- load balancing
- high availability
title: Moving Complexity to Application Layer?
url: /2017/12/moving-complexity-to-application-layer/
---
One of my readers sent me this question:

> One thing that I notice is you mentioned moving the complexity to the upper layer. I was wondering why browsers don\'t support multiple IP addresses for a single site -- when a browser receives more than one IP address in a DNS response, it could try to perform TCP SYN to the first address, and if it fails it will move to the other address. This way we don\'t need an anycast solution for DR site.

Of course I pointed out an [old blog post](/2009/08/what-went-wrong-socket-api/) ;), and we all know that [Happy Eyeballs](/2013/03/happy-eyeballs-happiness-defined-by/) work this way.
<!--more-->
You might wonder why this idea wasn't implemented from the very beginning. I can only guess (although I should know -- after all, I was running an ISP in those days) that the idea of sending a TCP SYN request to all addresses returned in the DNS query and using the first one never became popular because of the resource consumption it would place on the servers. Before server operating systems got decent implementation of [TCP SYN cookies](https://en.wikipedia.org/wiki/SYN_cookies), SYN floods were one of the easiest ways of bringing down a web site.

The rest is history: everyone solved the problem with load balancers, anycast, DNS-based load balancing, moving VMs and whatever other kludge... until the whole thing got unacceptably bad in IPv6-land and a few smart people rediscovered common sense (aka Happy Eyeballs).

{{<note info>}}Want to know more about various application-layer load balancing methods? I covered most of them in [Data Center 3.0 webinar](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers), and we spend a whole section of the [Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course on [high-availability topics](http://nextgendc.ipspace.net/Public:5-High-Availability_Concerns).{{</note>}}

Back to web browsers... in that particular case, there used to be so many attacks based on DNS spoofing that the browser vendors were forced to implement [DNS pinning](https://en.wikipedia.org/wiki/DNS_rebinding). For more details read [this whitepaper](https://www.blackhat.com/presentations/bh-usa-07/Byrne/Whitepaper/bh-usa-07-byrne-WP.pdf).

We continued our discussion with...

> I think there need to be a way to let the service owner choose if the client connects to all addresses at the same time or something else (maybe something in the DNS response?)

Well, once the big players figured out how to use load balancing at scale, and how they can use it to simplify their operations (rolling upgrades, [canary releases](https://martinfowler.com/bliki/CanaryRelease.html), [mitigating thundering herd](https://www.nginx.com/blog/mitigating-thundering-herd-problem-pbs-nginx/)...), it became part of their toolset, and they all rely heavily on a layer of load balancers and application-layer proxies sitting in front of the web servers.

Also, we got way beyond simple DNS-based load balancing with solutions like NS1 that can collect browser-side metrics to influence DNS responses to other users from the same autonomous system (listen to [Software Gone Wild Episode 29](/2015/04/nsone-data-driven-dns-on-software-gone/) for more details), while simplistic methods like Happy Eyeballs select the first server that responds to a SYN request, not the fastest server to deliver the desired response.

Long story short: I don't think anyone big enough to influence browser vendors is interested in reinventing this particular wheel.
