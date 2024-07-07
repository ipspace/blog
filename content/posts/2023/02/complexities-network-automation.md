---
title: "Response: Complexities of Network Automation"
date: 2023-02-01 07:00:00
tags: [ automation ]
---
_David Gee couldn't resist making a few choice comments after I asked for his opinion of an early draft of the [Network Automation Expert Beginners](/2023/01/network-automation-expert-beginners/) blog post, and allowed me to share them with you. Enjoy_&nbsp;😉

---

Network automation offers promises of reliability and efficiency, but it came without a warning label and health warnings. We seem to be perpetually stuck in a window display with sexily dressed mannequins.
<!--more-->
Instead of simple demonstrations with warnings like “don’t do this in production”, the art of network automation is to regulate the state between a topological desirable state and the current topological state. To word it differently, this means we have to manage how things are currently related with what data, present how we want it to look, then close the gaps through testable transactions made to the infrastructure.

Imagine if some of that data is incorrect, or our understanding of a dependency trees is inaccurate. Configuration might get delivered, but it could be entirely meaningless, or even worse, it might be meaningful in a destructive way because we didn’t consider anything else beyond a data set we thought was ok. 

Automation is a manifested software process and like all software problems, we must start with a process and a variable set. Network automation is nothing more than an algorithm with a set of inputs and outputs. Unfortunately for network automation, it has graph effects and any algorithm coded into existence can have deep ramifications, like affecting how routes appear several hops away.

I’ve always aired away from network engineers reading a Python book and being let loose. It’s not being a snob or gate keeper, but having real world experience of what can go wrong when a newcomer is let loose on production infrastructure. Automation needs to be treated with the seriousness it deserves and end-to-end effects must always be considered. In great systems, complexity and self-fulfilling graph conditions are hidden by simple user experiences. Because one configures OSPF on a device and routes magically appear (in area 0 of course), it does not mean one knows OSPF any more than turning it on. Automation is shaping up the same way in my eyes; just because one can run an Ansible playbook against a local device, it doesn’t mean anything beyond stuffing templated configuration onto a device. That times a thousand is pure chaos.

Great automation projects follow software development patterns, because it’s software. I’m not talking about GitOps here either. Software engineers, especially back-end ones, understand the world of dependencies deeply and intimately. When manipulating a system with explicit dependencies, one must be able to model the inputs and reserve the input variables, generate a desired state that can be reached via a set of mutations on a state-machine, execute it and then test for desired outcomes. Data sets like input variables can then be assigned properly after reservation and reports can be generated. Good systems deal with deletions as well as creations so when a service is shut down, as easily as state was added, it can be removed. Lastly, in multi-vendor environments, services that are to be automated present additional requirements in so much as multi-output schemas, where an operator can generate configuration for Junos just as easily as EOS. 

Complexity and complications are everywhere you look in network automation and simply declaring it job done or a failure sits very wrong with me. The real question in more recent times for me is who needs the simple UX and who owns the complexity? Is it time for network engineers to have a nice UX now and stop dreaming about more nerd knobs? Software engineering and network engineering are two different things. And to throw my two cents in, scripting is not software engineering!