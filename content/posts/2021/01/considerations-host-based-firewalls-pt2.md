---
date: 2021-01-07 07:19:00+00:00
series:
- host-firewalls
tags:
- security
- firewall
title: Considerations for Host-based Firewalls (Part 2)
---
*This is a guest blog post by [Matthias Luft](https://www.linkedin.com/in/matthias-luft-b50b7219/), Principal Platform Security Engineer @ Salesforce, and a regular [ipSpace.net guest speaker](https://www.ipspace.net/Author:Matthias_Luft).*

A couple of months ago I had the pleasure to publish my [first guest post here](/2020/09/considerations-host-based-firewalls.html) and, as to be expected from ipspace.net, it triggered some great discussion.

With this input and some open thoughts from the last post, I want to dive into a few more topics. 
<!--more-->
## Application Engineering vs. (?) Network Engineering

One trigger for the initial post was the question whether host-based firewalls (HBFs), potentially combined with solutions to learn rulesets based on flows, are intrinsically better than central firewalls. While we discussed the mileage around that already, comments and questions emphasized how often we have to handle a "software engineering vs. network engineering" mentality -- which should not involve any blame in either direction as this mindset is usually enforced by organizational structures. 

For whatever it is worth, I can only stress the point that a strong collaboration between software and network engineering will resolve way more issues than any technology. I award myself a "*Thanks, Captain Obvious*" here, but I still want to make the point to try and embed it into daily thinking. While I obviously come from a software engineering organization, such a collaboration is typically harder to achieve in typical corporate environments where software is operated and less often developed. In any case, I highly recommend this [publication](https://www.blackhat.com/us-20/briefings/schedule/#engineering-empathy-adapting-software-engineering-principles-and-process-to-security-19659) for additional insights. 

## Admins or Malware will turn off HBF

While the scenario of admins disabling HBFs should be covered in my previous point, we still have to take a look at the scenario that Malware can disable HBFs. If a malicious actor can disable the HBF, the envisioned benefits are gone. However, keep the  following things in mind:

- HBFs were used as an umbrella term for the overall concept of microsegmentation. When looking at this particular line of thought, we have to differentiate between HBFs and virtualization-based microsegmentation. While they may differ only a little with regard to complexity, virtualization-based microsegmentation can only be disabled in weird cases from a compromised host.
- While you should filter in- and outbound flows, this can be achieved for your own environment exclusively by inbound rules. This makes the rulesets more resilient against the turn-off scenario and, from my experience, also greatly reduces complexity. Outbound filtering towards the Internet or other big sites are unfortunately another very big topic too comprehensive for this post (See [here for some discussion](https://twitter.com/search?q=(from%3A%40cyb3rops)%20proxy&src=typed_query)).
- The focus on inbound filtering works particularly well for central infrastructure services like DNS and NTP with a clear communication pattern as was also pointed out in several comments on the last blog post.

## Focus on inbound filtering or what to filter in general

Looking at both previous discussion points, there is the "Total Ownership" model that I want to describe a bit:

- Many modern IT environments operate under a total ownership model. This means that teams completely own the components they develop and operate, thus (inbound) filtering is also owned by them.
- These teams will have the required domain knowledge to properly define filtering rules. In addition, it also helps in moving towards a zero trust network model where every component has very clearly defined ingress paths with clear security mechanisms attached to those. I specifically use the term security mechanisms here instead of filtering -- but discussing zero trust networks would again be an entire other series of blogposts.
- Such a model often results in simplified network requirements. Of course, there are old RPC monsters out there, but try to collaborate with your software engineers on simplified network protocols and flows. Also, modern hosting platforms should make it easy to provide small local instances of all supporting services (such as caches, reverse proxies, or databases) per component instead of centralizing those, which results in complex network flows.

## Is a paradigm shift coming?

Some comments mentioned the need for a paradigm shift in firewalling -- and I fully agree. The concept of long, central, IP- and port-based list of rules does not work with modern software engineering patterns. I already see the integration of security mechanisms (including filtering) into application and infrastructure manifests, which is a great direction for you to develop your networking engineering approach. There are also a lot of resources on ipspace.net to help you with that, especially on modern cloud and container environments which also provide microsegmentation functionality. 

While I emphasized the need for collaboration between software and network engineering, the same holds true for security. Security engineering must also strive for close collaboration with the other engineering departments, which realistically is not the case in most organizations yet. However, when starting your unified engineering journey, make sure to also include them on it because they will love to be able to review early drafts of your infrastructure-as-code manifests!
