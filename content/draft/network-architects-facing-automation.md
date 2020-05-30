---
title: "How Should Network Architects Deal with Network Automation"
draft: True
##date: 2020-05-28 09:08:00
tags: [ automation ]
---
A network architect friend of mine sent me a series of questions trying to figure out how he should approach network automation, and how deep he should go.

> There is so much focus right now on network automation, but it's difficult for me to know how to apply it, and how it all makes sense from an Architect's PoV. 

A network architect should be the bridge between the customer requirements and the underlying technologies, which (in my opinion) means he has to have a good grasp of both as opposed to fluffy opinions glanced from vendor white papers, or brushed off so-called thought leaders. 

Like a traditional architect has to understand the limitations of materials, tools and processes used to implement his creations, a network architect MUST understand the advantages and limitations of technologies used to implement and operate the network he designs.

The absolute minimum a network architect thus needs to know about network automation is a firm grasp on the fundamentals needed to implement a successful network automation solution, including:

* The need for standard service definitions;
* No one-off stunts;
* Single source of truth[^SST];
* Minimize the amount of business logic[^BL] needed to implement requested services;
* Minimize the in-network state that has to be derived from the source-of-truth through business logic.

A few practical (low-level) examples along these lines:

* Use regular topologies like leaf-and-spine fabrics so the source-of-truth doesn't have to contain the actual network topology (which could be derived through simple business logic);
* Use wiring plan that can be derived from source-of-truth. For example, all leaf- and all spine switches have the same number of interfaces and uplinks.
* Use unnumbered core interfaces (or IPv6 LLA) whenever possible to minimize the amount of device state that needs to be kept (or changed) in the automation process;
* Use BGP AS numbers that can be derived from network topology (as opposed to having them stored in the source-of-truth).

> The focus in the industry, rightly so, is for people mainly in engineering and ops, transitioning people to network automation experts. That's not the best fit with my current role, or my plans going forward.

That focus is understandable. Showing glitzy demoes is sexier than solving hard problems. Talking about tools and hacks is simpler than thinking about concepts and fundamentals. Also, glitzy demoes sell boxes, educating people about fundamentals does not.

In this respect network automation is no different from any other networking technology. For example, vendors love to talk about the intricate features of their EVPN implementations, and hate you when you start pointing out the complexities of their proposed designs.

> As you know, there is only so much time in a day. If I were to say learn Ansible, then that would take time from something else, maybe cloud networking, maybe a soft skill, or maybe just another technology.

Network automation is just one of many technologies (or tools) a network architect should master. It's no different from BGP, MPLS, VXLAN, EVPN, IPsec, cloud networking... You have to get exposed to it, you have to get your hands dirty (if you want to be a good network architect as opposed to PowerPoint creator), and you have to figure out its limitations because nobody else will do it for you, least of all vendors, tool creators (who would ever criticize their own baby), or automation evangelists.

Does that mean you have to learn Ansible? Sure. You have to hit the wall (hard) a few times to realize how limited it is. You have to try to run it on a large-scale deployment to figure out how slow it is. You have to try to implement a complex configuration template to figure out how much Jinja2 sucks without custom Python filters... or you could read IBM's white papers praising its beauties.

NOTE: I'm not saying Ansible sucks (in general). It's just a tool, and every tool sucks when used incorrectly or in environment it's not good for. Just try hacking down a sequoia with a Swiss Army knife which happens to be a great tool... but not for that particular use case.

Unfortunately it's not just Ansible. There's Salt, Nornir, Terraform... and the very minimum a network architect should understand is the difference between Ansible- or Nornir-style step-by-step automation and infrastructure-as-code approach of tools like Terraform.

NOTE: I know Nornir is a Python framework and can be made to do anything you wish it to do... but so can a Turing machine. The crucial difference between Terraform and Ansible or Nornir is that Terraform does the hard work of comparing and adjusting desired and current system state for you.

> How do you think an Architect should approach automation? Should I spend X amount of time there even though my role doesn't touch it currently?

YES. Network automation is slowly becoming one of the crucial components of large-scale networks, and as a network architect you have to understand its implications, benefits, and limitations.

> Even if my main passion is not there? My main passion is in infrastructure, design, mentoring and teaching people.

Unfortunately, network automation will become as ubiquitous as IP or TCP. You might hate IP routing, but can't successfully design or operate networks without understanding how it works... unless you believe in outsourcing all challenges to your favorite vendor who always has your best interest in mind (right?).

Also, being an emerging approach (at least for mainstream enterprise networks) with a potential huge long-term impact, network automation is a shining example of where you could add most value mentoring and teaching people stuck in the old ways ;)

> Is there any courseware more focused on Architect PoV? I know you probably have some offerings in your subscription, such as introduction to different topics.

I'm not aware of any courseware apart from ipSpace.net webinars and courses that I could recommend (but then I'm not exactly looking for it ;). Most alternatives out there that I'm aware of focus on hands-on tasks (example: automating with Python and Netmiko) or tools (most commonly Ansible).

You could start with the introductory [network automation webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars) like [Network Automation 101](https://www.ipspace.net/Network_Automation_101), explore a [high-level overview of network automation tools](https://www.ipspace.net/Network_Automation_Tools), and find some ideas in [network automation use cases](https://www.ipspace.net/Network_Automation_Use_Cases), but once you're serious about mastering network automation concepts (as opposed to becoming proficient with an automation tool), I'd strongly recommend going for the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course as it covers numerous concepts you might need to understand to become a better network architect including:

* [network automation system design](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S3);
* [tool selection](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S4A);
* [security and reliability](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S4B);
* [supply chain security aspects](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S6A);
* [data models and data stores](https://my.ipspace.net/bin/list?id=NetAutSol&module=3#M3S1);
* [intent-based networking and abstract data models](https://my.ipspace.net/bin/list?id=NetAutSol&module=3#M3S4A)
* [network infrastructure as code](https://my.ipspace.net/bin/list?id=NetAutSol&module=7)
* [validation, error handling and unit tests](https://my.ipspace.net/bin/list?id=NetAutSol&module=5#M5S2)
* [continuous integration](https://my.ipspace.net/bin/list?id=NetAutSol&module=5#M5S3), [system testing](https://my.ipspace.net/bin/list?id=NetAutSol&module=5#M5S3C), and [testing pipelines](https://my.ipspace.net/bin/list?id=NetAutSol&module=5#M5S3B)
* [event-driven network automation](https://my.ipspace.net/bin/list?id=NetAutSol&module=8)

[^SST]: Every bit of information needed to provision or operate the network or the services it offers should be stored in a single well-defined place
[^BL]: The rules needed to map user-level information into device-level data models or configurations.