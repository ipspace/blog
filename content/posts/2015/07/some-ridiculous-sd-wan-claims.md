---
date: 2015-07-09 09:30:00+02:00
tags:
- SD-WAN
title: Some Ridiculous SD-WAN Claims
url: /2015/07/some-ridiculous-sd-wan-claims/
sd-wan_tag: rant
---
[SDx Central](https://www.sdxcentral.com/) is usually a pretty good web site that I love to read, but even they occasionally manage to publish a [gem](https://www.sdxcentral.com/articles/contributed/sd-wan-disrupt-enterprise-networking-jeff-vance/2015/07/) like this one:

> The problem with MPLS and similar technologies is that they weren't designed with today's business challenges in mind. Today, a company may need to launch an overseas R&D office overnight, or it may acquire a startup and want to immediately network with offices in distant regions and countries. Older technologies just don't have the flexibility to do this on the fly.

Not surprisingly, the above paragraph triggered a severe case of Deja-Moo.
<!--more-->
![Deja-Moo](/2021/01/deja-moo.jpg)

**Technology has nothing to do with it**. It's reasonably easy to deploy auto-configuring DMVPN network if you spend a few days studying how DMVPN work and thinking about configuration templates and auto-configuration mechanisms:

-   Use DNS-based NHRP on DMVPN spoke routers;
-   Use DHCP prefix delegation to assign IP addresses to DMVPN spokes;
-   Use dynamic BGP neighbors to build a scalable network;
-   Use shared keys (if you don't care that much about security) or certificates.

{{<note info>}}You might want to consider watching [DMVPN](http://www.ipspace.net/DMVPN_trilogy) and [Ansible](http://www.ipspace.net/Using_Ansible,_YAML_and_Jinja2) webinars if you don't know what I'm talking about ;){{</note>}}

**It's all about the processes and procedures**. The real reason service deployment in typical enterprise network is slow are [broken processes](/2014/09/youve-been-doing-same-thing-for-last-20/):

-   [Organic growth](#/media/File:Chabolas_a_plomo.jpg) coupled with lack of good network design (because managers think anyone can do it and thus don't want to pay for it);
-   Lack of configuration templates (aka the death by thousand kludges);
-   Lack of automated deployment processes (because the software to do it is supposedly too expensive).

The end result: every network (and sometimes even every site) is a unique snowflake. No wonder it takes forever to carefully craft and deploy another unique snowflake instance.

Also, when we're talking about *new offices in distant regions*, there might be this small problem of physical connectivity (in some countries it's [neigh impossible to get a free copper pair](http://farm4.static.flickr.com/3549/3409369082_4fcfbbbe8b_o.jpg), particularly in old cities) which is equally bad for MPLS and Internet services.

Finally, *immediately connecting a startup* might involve a nasty case of dual NAT, which will probably trip most SD-WAN products (which is what the author of that article is promoting), but of course the software-defined evangelists love to gloss over dirty details like this one.

### The Advantages of SD-WAN

Things are usually not totally black-and-white. Most SD-WAN products do have advantages (particularly in enterprise networks) over more traditional solutions:

-   They are new, so they haven't accumulated so many configuration knobs (but I'm positive they eventually will -- no vendor can resist the lure of implementing a few per-customer knobs if a big order looms on the horizon);
-   Their architecture uses a central controller (behind the scenes it's usually a combination of configuration management tool and route reflector), so it's impossible to create truly unique snowflakes.

However, I'm still waiting to see how well the SD-WAN products survive the clash with enterprise reality (you might want to read [Tom Hollingsworth's take on Meraki](http://networkingnerd.net/2015/07/07/meraki-will-never-be-a-large-enterprise-solution/), which is facing a similar problem).

### But Wait, There's More

As you might expect, the rest of that article fares no better than it's beginning. Here's another Deja-Moo claim:

> This is the promise of the SD-WAN: intelligence built into the network; the ability to deploy in minutes; the elimination of vendor lock-in; and the ability for anyone, anywhere to quickly access all enterprise resources, no matter where they are located.

**Intelligence built into the network** -- and how are the existing networks operating? Using a central control plane?

**Ability to deploy in minutes** -- assuming you already got physical connectivity, but then I can as easily deploy another DMVPN spoke router at that same location.

**The elimination of vendor lock-in** -- ah, that's why Greg Ferro [wrote](http://etherealmind.com/concerns-about-sd-wan-standards-and-interoperability/) "*\[While standards are important\], I don't believe they are practical in the current situation around the WAN*"

While [some lock-in is usually inevitable](/2015/01/lock-in-is-inevitable-get-used-to-it/), at the moment, [every single SD-WAN solution is a total lock-in](/2015/06/software-defined-wanwell-orchestrated/), and anyone who claims otherwise is either clueless or trying to mislead you.

### A Note to Marketers

I think I wrote this before -- I understand you have to do what you have to do, but you don't have to make yourself looking totally ridiculous in the process.
