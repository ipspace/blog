---
cli_tag: api-challenge
date: 2019-04-16 08:38:00+02:00
niac_tag: rest
series:
- niac
- cli
tags:
- automation
title: REST API Is Not Transactional
url: /2019/04/rest-api-is-not-transactional/
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

I was walking down the infinite hallways of Cisco Live Europe chatting with the fellow Tech Field Day Extra delegates when I probably blanked out for a minute as the weirdest of thoughts hit me: "*REST API is not transactional*"

**TL&DR**: Apart from using structured data and having error codes REST API is functionally equivalent to Cisco IOS CLI from 1995
<!--more-->
### Let's Start with an Example

Imagine you're configuring a complex application environment on a single switch (to make it simple). You might have to configure:

-   Several routing domains (VRFs) to enable inline load balancing between them
-   A dozen segments (VLANs)
-   Subnets on those segments
-   Routing with external world
-   Microsegmentation (the unicorn previously known as reflexive ACLs)

Any one of those configuration commands could fail. You could fail to check input data and use a word as IP address, or use an impossible prefix length, or hit some configuration limits (like the number of entries in an ACL), or use duplicate names or...

If you [bought the switch from the right vendor](/2016/10/network-automation-rfp-requirements/) (Juniper, Arista or Cisco IOS XR) then you'd just shrug, abort the whole thing, have it automagically removed, and retry. On those same boxes you'd also be able to say **now I'm done** (aka **commit**) and have all the changes implemented at once.

On a few other boxes you could shrug and **rollback** to previous state (assuming you were smart enough to save it when you started).

Both options are well known to programmers dealing with transactional databases for the last 40 years... and are completely missing in [REST API](/2014/07/what-is-this-api-thingy/) world (unless the API provider took great pains to implement them).

### Now for REST API

Now imagine you'd deploy the same application environment in (almost) any private or public cloud, be it AWS, Azure, GCP, VMware NSX, Cisco ACI... For every object you'd have to configure (VPC, subnet, security group, routing table if you're deploying on AWS, or tenant, bridge group, EPG, contract... if you're working with Cisco ACI) you'd execute a REST API call. Any one of those calls might fail. Now what?

Well, you're on your own. Hopefully you remember what you were doing and what you already created because [*you'll have to clean up your own mess*](/2018/09/infrastructure-as-code-netconf-and-rest/) and you'll have absolutely no help from the orchestration system *because REST API is not transactional* so there's no rollback.

**Long story short**: people who claim how bad network device configuration methods are and how they'd be so [much better if only the network devices would have REST API](/2018/04/dont-get-obsessed-with-rest-api/) (A) might not know what they're talking about and (B) will get exactly what they ask for. Do we really have to repeat every mistake anyone else ever made?
