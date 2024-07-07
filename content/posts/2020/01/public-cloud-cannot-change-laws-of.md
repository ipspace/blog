---
date: 2020-01-21 08:33:00+01:00
ha-cloud_tag: stretch
series_weight: 1000
high-availability_tag: cloud
series:
- ha-cloud
tags:
- design
- cloud
- WAN
- high availability
title: Public Cloud Cannot Change the Laws of Physics
url: /2020/01/public-cloud-cannot-change-laws-of/
---
Listening to public cloud evangelists and marketing departments of vendors selling over-the-cloud networking solutions or multi-cloud orchestration systems, you could start to believe that migrating your workload to a public cloud would solve all your problems... and if you're gullible enough to listen to them, you'll get the results you deserve.

Unfortunately, nothing can change the fundamental laws of physics, networking, or application architectures:
<!--more-->
-   **Latency** remains a performance killer, and if you replace sub-millisecond latency you get within your data center with several milliseconds typical of hybrid cloud deployments, the performance of your applications will inevitably plummet;
-   **Bandwidth** is still limited and [more expensive than you think](http://blog.thestateofme.com/2019/12/12/the-great-bandwidth-swindle/);
-   [**Data has mass and gravity**](/2013/05/data-has-mass-and-gravity/), and the location of data usually dictates the location of compute infrastructure. In other words, you can't move to the cloud and leave your data behind.

Then there are so-called soft skills. You can either master a new environment, or try to use it the way you handled the old one (example: using a screwdriver as a hammer). Organizations believing they can simply migrate their existing workloads into public clouds are usually rewarded with outlandish bills.

Even worse, you might be fighting reckless or negligent application developers who keep cutting corners to get their job done as soon as possible (no matter the consequences) on a daily basis. Why would anyone in this world think that giving them access to an on-demand orchestration system, and all the tools they need to create another [memcrashed perfect storm](https://www.cloudflare.com/learning/ddos/memcached-ddos-attack/) would make the situation any better is beyond my comprehension.

In the end, your organization will need someone who understands the laws of physics, fallacies of [distributed computing](https://my.ipspace.net/bin/list?id=Net101#FALLACIES) and [network security](https://my.ipspace.net/bin/list?id=Net101#NETSEC), and the [realities of public clouds](https://my.ipspace.net/bin/list?id=Cloud101#NET); it's just the question of whether it needs a major disaster to wake up first. A public cloud expert would be invaluable once the hard lessons have been digested, and it could be you assuming you'll be ready for the challenge. We're trying to do our best to help you get prepared with our [public cloud webinars](https://www.ipspace.net/Cloud) and [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course.