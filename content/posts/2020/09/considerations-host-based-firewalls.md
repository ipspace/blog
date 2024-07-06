---
date: 2020-09-03 06:57:00+00:00
series:
- host-firewalls
tags:
- security
- firewall
title: Considerations for Host-based Firewalls (Part 1)
---
*This is a guest blog post by [Matthias Luft](https://www.linkedin.com/in/matthias-luft-b50b7219/), Principal Platform Security Engineer @ Salesforce, and a regular [ipSpace.net guest speaker](https://www.ipspace.net/Author:Matthias_Luft).*

Having spent my career in various roles in IT security, Ivan and I always bounced thoughts on the overlap between networking and security (and, more recently, Cloud/Container) around. One of the hot challenges on that boundary that regularly comes up in network/security discussions is the topic of this blog post: microsegmentation and host-based firewalls (HBFs). 
<!--more-->
New technologies like NSX-T, Tetration, or security group-functionality in public clouds make this topic come up even more often recently. This post will not discuss the details of individual products (for more information watch the [NSX](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive), [AWS](https://www.ipspace.net/Amazon_Web_Services_Networking) and [Azure](https://www.ipspace.net/Microsoft_Azure_Networking) webinars), but different aspects of firewall rule design based on your chosen firewall technology (centralized vs. microsegmentation). As always, your mileage/requirements/risk appetite will vary, and I hope this post provides relevant input for your evaluation. 

[RFC7288](https://tools.ietf.org/html/rfc7288) provides reflections on host firewalls and describes the security benefits of using firewalls in general. When it comes to security benefit from technology, I usually like to introduce my view on security benefit and its implications:
Security Benefit = Security Posture + Security Functionality.

## Security Posture

The security posture of any technology is a prerequisite to gaining security benefits from it. There are plenty of examples where security technology, which was supposed to provide security benefits, actually resulted in a net reduction of the overall security posture. OpenSSL (providing transport encryption) with [Heartbleed](https://en.wikipedia.org/wiki/Heartbleed) or the various [RCE](https://en.wikipedia.org/wiki/Arbitrary_code_execution) vulnerabilities in endpoint protection solutions ([1](https://googleprojectzero.blogspot.com/2016/06/how-to-compromise-enterprise-endpoint.html),[2](https://googleprojectzero.blogspot.com/2015/09/kaspersky-mo-unpackers-mo-problems.html),[3](https://bugs.chromium.org/p/project-zero/issues/detail?id=1252&desc=5)) come to mind as some of many examples. 

The analysis of the security posture of a product/technology is a topic beyond this post (we covered some aspects in [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions)). Still, make sure to look at the security posture of the products on your evaluation shortlist. Even in recent years, security researchers found vulnerabilities in all types of networking products - from [firewalls](https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-20161019-asa-idfw) to Host [TCP stacks](https://securitylab.github.com/research/apple-xnu-exploit-icmp-poc). 

## Security Functionality

The security benefit from network filtering solutions (and we are purely talking filtering on Layer 3/4) is based on restricting access to and from systems. There is comprehensive guidance on which specific types of traffic your firewall (or packet filter) should be filtering (e.g. [RFC4890](https://tools.ietf.org/html/rfc4890) or [NIST SP 800-41](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf))... but in my opinion, [RFC1825](https://tools.ietf.org/html/rfc1825) contains the most relevant quote for firewall rules: "[...] many dislike their presence because they restrict connectivity". The fact that systems need to communicate and that it is tough to distinguish legitimate from malicious communication results in several fundamental truths which result in intrinsically hard challenges:

- An allowlist approach, only allowing defined communication relationships, provides the most security benefit.
- Numerous systems need to communicate with many external services.
- Various modern software engineering/deployment/operation approaches require broad Internet access.
- IP addresses, the building blocks of network filtering, are more ephemeral than ever.
- Network filtering is implemented by network/firewall engineers, while the knowledge about required communication relationships lies with application engineers.
    
Those truths apply to host-based and central firewalls with only slightly different extents. They also account for the fact that I have barely ever performed/participated in/heard of a firewall rule audit that did not result (quickly) in (a high number of) findings of outdated rules that nobody knew anymore what they were supposed to do. 

Based on those truths, I find these guiding principles for firewall ruleset design very helpful:

- Start with little filtering granularity.
- Design the rule change process with a high degree of automation in mind. Modern approaches to automated firewall management can bring network engineering and application engineering closer together while improving documentation and traceability of rules (examples [here](/2019/01/firewall-ruleset-automation-with-ci.html) and [here](https://www.ipspace.net/PubCloud/))
- Automation can drive self-service, expiration, and automated approval processes for rule changes.
- Automation and increasing granularity require a high degree of overall IT engineering maturity. Often firewalls are thought of as a way to bring structure and order to an environment. That will not work when the existing business processes are not in order and require unknown communication relationships. 

To bring it all together:

- Start with little filtering granularity
- Implement automated processes around that
- Improve overall process and engineering maturity to support automation and filtering granularity. 

These considerations result in an essential requirement for your filtering technology of choice: administrative interfaces that allow a proper level of automation and central management - whether it is vendor-provided or [home-grown](https://www.slideshare.net/cmdln/building-a-host-based-firewall-on-top-of-cfengine).

And finally, circling back to the host-based focus of this post: While host-based firewalls inherently allow for a greater level of filtering granularity, the more relevant question is whether the management of your HBF solution and your operational maturity will allow you to leverage/reach this greater granularity. 

## Conclusion

I have seen successful large-scale deployments of host-based firewalls on client/endpoint systems. The rules there are often quite simple and rarely change:

- Block any inbound access
- Allow outbound access
- Allow inbound access from your endpoint administration segments (which will most likely be necessary and at least should be well known and not change often).

Server environments usually don't conform to this communication pattern, making firewall rule design more difficult. With the fundamentals covered in this post, we will dive into more details in the future, such as common network security patterns for servers or the challenge that an attacker can disable a host-based firewall on a compromised system.  

We would be very excited to hear your comments, disagreements, get links to other sources, and receive more questions! Finally, you might want to [watch this presentation](https://www.youtube.com/watch?v=Kb_dU6t56mo) that provides a more network engineering-focused perspective large-scale firewall operation. 