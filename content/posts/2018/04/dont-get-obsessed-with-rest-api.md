---
cli_tag: cli-api
date: 2018-04-05 09:56:00+02:00
series:
- cli
tags:
- automation
title: Don't Get Obsessed with REST API
url: /2018/04/dont-get-obsessed-with-rest-api.html
---
REST API is the way of the world and all network devices should support it, right? Well, Ken Duda (Arista) [disagreed with this idea during his Networking Field Day presentation](http://techfieldday.com/video/arista-eos-programmability-with-ken-duda/), but unfortunately there wasn't enough time to go into the details that would totally derail the presentation anyway.

Fixing that omission: should we have REST API on network devices or not?
<!--more-->
Before going into the details:

-   Well-defined and well-behaved API is obviously the best way to implement an interface to a system, and a great foundation for a robust automation solution... but you might not need a REST API.
-   REST is so loosely defined that it could mean anything (it doesn't even have to run over HTTP). For the purpose of this discussion we'll assume that we're talking about the common understanding of REST as an API providing CRUD functionality: you can *Create, Read, Update* or *Delete* individual objects known by the system you're interfacing with.

Now consider how you'd like to manage a network device. Would you like to create/update/delete individual objects (interfaces, neighbors, ACL entries, static routes) the way we're doing today with the CLI, or would it be better to treat the network device as a single-purpose system with a configuration that can be replaced and reloaded as needed?

If you think we need REST API to manage network devices, then you're effectively trying to replicate existing workflow where we spend inordinate amount of time considering the right sequence of steps to get from here to there, and replace it with a faster version of the same choreography. See also: [CRUD hell](/2018/09/infrastructure-as-code-netconf-and-rest.html).

Wouldn't it be better to tell the device how it should work (intent, anyone?), and tell it to reload the "how it should work" document as needed?

Looking for analogies beyond networking: do you want your network device to look like an orchestration system with a REST API (OpenStack comes to mind) or like a web server (configured with text configuration and no API)? What do you think?

For a more in-depth discussion of this topic, watch the [*Intent-Based Networking*](https://my.ipspace.net/bin/list?id=AutConcepts#INTENT) section of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.

*This blog post was initially sent to the subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*
