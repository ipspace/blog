---
cli_tag: cli-api
date: 2014-02-27 06:47:00+01:00
series:
- cli
tags:
- SDN
- network management
title: CLI or API? Wait … Do You Really Have to Ask?
url: /2014/02/cli-or-api-wait-do-you-really-have-to/
---
The "*[Is CLI In My Way ... or a Symptom of a Bigger Problem](/2014/02/is-cli-in-my-way-or-is-it-just-symptom/)*" post generated some interesting discussions on Twitter, including this one:

{{<figure src="/2014/02/s400-API_First.png">}}

One would hope that we wouldn't have to bring up this point in 2014 ... but unfortunately some \$vendors still don't get it.
<!--more-->
### Why Is the CLI or API a Silly Dilemma?

A reasonably sound management plane implementation would have an object model (think SNMP MIB on steroids) that you could manipulate with CLI or API, and that the control-plane protocols would use to adjust their behavior. A simplistic object model would be just a tree of variables, a more thought-out one would use object-oriented programming with [getter and setter functions](http://en.wikipedia.org/wiki/Mutator_method).

Similarly, the state of the control-plane protocols (example: OSPF adjacencies, STP root bridge ...) would be stored in a similar structure that any other process could access through a well-defined interface.

Once you have such an object model, it becomes trivial to implement CLI, REST API with JSON or XML, NETCONF API with XML, or any other data manipulation protocol (like OVSDB or even SNMP) -- you just need a generic translation layer that maps external requests into GET or SET calls on internal objects.

### The State of Networking Reality

How many vendors have an API call for every CLI command (or vice versa)? How many vendors can give you the same control-plane state or data-plane counters that you can inspect with CLI commands in an XML- or JSON-formatted response?

Junos definitely meets these requirements. Nexus OS NX-API and Arista EOS eAPI might be decent, but I never checked the feature parity between API and CLI.

On the other hand, Cisco IOS implementation of NETCONF fell far short of these goals the last time I checked (it was mostly screen scraping on steroids), IOS XR is better, but I'm not sure how far it goes (comments welcome). What about other vendors? Share your experience in the comments!

### But Isn't That Extra Work?

Of course it is if you have "suboptimal" software architecture ... but if you did it right from the very beginning, every single CLI command should be accessible as an API call and vice versa. Also, adding the full-blown functionality isn't hard -- you get most of what you need with [Tail-f's ConfD](http://www.tail-f.com/on-device-configuration-management/) (but of course that doesn't work if you're infected with the Not Invented Here plague).

Oh, and before anyone mentions increased testing requirements -- if you don't have an automated testing mechanism that would test CLI and API access to every object exposed by your software, you have a much bigger problem on your hands.

### Does This Matter?

You might think that I'm discussing [the maximum number of angels that can dance on a pinhead](http://en.wikipedia.org/wiki/How_many_angels_can_dance_on_the_head_of_a_pin%3F), but do consider that you *might* have to implement programmatic access to the devices you're buying today in a few years (and roadmaps aren't exactly helpful when you have to roll out something tomorrow).

Also, lack of CLI-API parity (particularly in the case of CLI being richer than API) might be an indication of vendor's focus or the product's software architecture. Whenever you encounter a recently-designed product with poor API be vary, proceed carefully, and vote with your budget.
