---
title: "Breaking APIs or Data Models Is a Cardinal Sin"
date: 2025-04-29 08:15:00+0200
tags: [ automation ]
series: cli
cli_tag: api-challenge
---
Imagine you decide to believe the marketing story of your preferred networking vendor and start using the REST API to configure their devices. That probably involves some investment in automation or orchestration tools, as nobody in their right mind wants to use **curl** or **Postman** to configure network devices.

A few months later, after your toolchain has been thoroughly tested, you decide to upgrade the operating system on the network devices, and everything breaks. The root cause: the vendor changed their API or the data model between software releases.
<!--more-->
### Why Does It Hurt So Much?

There's nothing more annoying than having to change your working code just because an API (or a data model) your code is using has changed. You waste a lot of time just to keep things running while gaining absolutely no extra functionality. In the worst case (in networking), you are forced to keep working with two (or more) versions of the data model in parallel (and keeping track of which version to use with which device) because you can't upgrade all devices in one shot.

Most providers of API-based services are well aware of that and do their best to keep their APIs stable[^X]. Even Google (the [notorious deprecator](https://killedbygoogle.com/)) changed their analytics API only once in more than a decade I was using their product. While doing that, they had about a year-long grace period during which both versions of the API worked.

[^X]: People [killing their APIs](https://platformonomics.com/2025/04/never-take-a-dependency-on-elon-musk-grok-api-edition) because they find them inconvenient are an entirely different category.

### But Networking Is Different, Right?

As always, some people think that networking has to be different. You might be lucky and work with a vendor that learned the hard way that customers prefer stability, or you might be using a vendor that changes their data model every year, like Nokia does with SR Linux.

{{<long-quote>}}
You might claim that I'm picking on Nokia, and I might be. While I love their work on containerlab and appreciate that they make SR Linux available in a fast-starting, free-to-download container format, there are certain things no vendor should be doing, and breaking promises they made to their customers (a published API or data model is somewhere between a promise and a contract) is pretty high on my list of things to avoid.
{{</long-quote>}}

Of the [two dozen platforms _netlab_ supports](https://netlab.tools/platforms/), only Nokia SR Linux requires configuration template changes with every other software release (_netlab_ configuration templates were impacted by software releases [25.3](https://github.com/ipspace/netlab/pull/2179), [24.7](https://github.com/ipspace/netlab/commit/d9265646a9e281d79814efe7018869f0e5e71d5a), and [23.3](https://github.com/ipspace/netlab/pull/803)). While FRRouting loves changing the data structures of JSON printouts (which totally breaks our validation scripts), I don't remember ever having to change a configuration template to accommodate a newer software release from a major networking vendor ([VyOS](https://github.com/ipspace/netlab/pull/2161) is another unfortunate exception). On the other side of the spectrum, Cisco IOS introduced address families in BGP decades ago, but still recognizes the old IPv4-only configuration syntax.

### What's Changing?

One would understand that you have to break some eggs to make a better omelet, but some SR Linux changes we had to deal with are so banal that they're driving me crazy. For example, in SR Linux release 25.3:

* They changed the way you set BGP MED in a routing policy. Previously, the attribute was set with `/routing-policy/policy/entry/action/bgp/med/set`, now you have to set the `/routing-policy/policy/entry/action/bgp/med/operation` to **set**. Why couldn't they retain both options?
* Prefix matching in a routing policy was specified with `/routing-policy/policy/entry/match/prefix-set`, now it's `/routing-policy/policy/entry/match/prefix/prefix-set`. WTA*?
* BGP community propagation was specified per BGP neighbor; now it's set per address family. Many vendors [belatedly realized](https://blog.ipspace.net/2024/08/bgp-session-af-parameters/) (or not at all) that some BGP attribute handling should be configurable on the AF-level, but most of them retained backward-compatible syntax when they changed their mind. For example, configuring a parameter per neighbor would still be allowed and impact all address families.

I would have hoped the customer's well-being would be valued higher than a puristic view of the data model, but I'm clearly misguided. On the other hand, even Ansible, with its "_[we cut it three times and it's still too short](/2019/09/measure-twice-cut-once-ansible/)_" stunts, mastered the art of deprecating functionality. I really can't grasp why someone would feel the urge to abruptly break the data model instead of slowly deprecating old attributes.

Then there are more fundamental changes to the data model. What was a single value could become a list. For example, SR Linux 24.7 introduced multiple routing policies per BGP neighbor, changing the `import-policy` and `export-policy` parameters from strings to lists. Even that's trivial to solve -- _netlab_ silently converts scalar values to lists because we don't want to force the customers to enclose stuff in square brackets for no good reason. Typical CLI configuration commands that previously accepted a single value could start accepting a list of values. XML also had no problems with the one-or-many dilemma[^XJ], which might explain why Junos happily takes a single value or a list of values for many configuration parameters.

[^XJ]: Resulting in [hilarious XML-to-JSON translation SNAFUs](https://blog.ipspace.net/2021/01/fixing-xml-json-challenges/)

However, you can't see those solutions if you drank too much YANG Kool-Aid. YANG is a strongly typed schema language and does not allow multiple data types for a single parameter. But even the YANG world has a solution: you can specify mutually exclusive parameters with the **choice** construct. In the above example, we could have `import-policy` taking a single value and `import-policy-list` taking a list of values.

But like breaking changes to the configuration data model wouldn't be enough, there's more. If you save the configuration of a device running SR Linux release 24.10, and that configuration uses one of the changed data model parameters, you cannot load it on a device running SR Linux release 25.3. I've never seen a network device without that baseline level of backward compatibility[^DG].

[^DG]: Trying to downgrade the software after saving the device configuration with the new software release is an entirely different ballgame.

Even assuming one cannot avoid breaking changes, there's a clean solution to all of the above: [API](https://www.postman.com/api-platform/api-versioning/) or data model versioning. The simplest solution would be to ask the customers to include the target software version in every configuration request and do the necessary translations behind the scenes. Why do you think Cisco IOS configuration starts with the **version** command?

### What Could We Do?

Is there something you can do about vendors breaking APIs and data models (it probably isn't just Nokia -- please leave a comment with your horror story)? Make yourself heard. Maybe you'll hit a pain point somewhere (it worked for me [at least once](https://blog.ipspace.net/2017/04/lets-drop-some-random-commands-shall-we/)), or maybe there's someone within the vendor organization who knows what needs to be done but cannot make the changes without [external pressure](https://blog.ipspace.net/2010/09/hiding-documentation-will-they-never/).

Finally, I always told people yammering about vendor behavior to vote with their wallets, but that doesn't seem to work in this case. Nokia must have a particularly loyal set of customers[^PD] to be able to break customer provisioning tools just to retain a clean configuration data model.

[^PD]: Or maybe they're so big that the decisions are made solely at the golf course/PowerPoint level, and the developer complaints are completely ignored.

