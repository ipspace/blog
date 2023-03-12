---
cli_tag: cli-api
date: 2015-03-16 09:27:00+01:00
series:
- cli
tags:
- SDN
title: We Have to Get Away from the Box-Focused Mentality
url: /2015/03/we-have-to-get-away-from-box-focused.html
---
I had a great SDN-focused conversation with Terry Slattery during last Interop New York, ago and of course we came to the argument that the CLI is the root of all evil, which started my [usual rant](https://blog.ipspace.net/2014/02/is-cli-in-my-way-or-is-it-just-symptom.html). Guess what: not surprisingly that wasn't what Terry had in mind. He was using the "CLI mentality is bad" as a synonym for "we're used to configuring our networks one box at a time" (so we should really be talking about box-focused mentality).
<!--more-->
### How Did We Ever Get to this Point?

What we're doing is not so much different from the way server people were configuring servers 10 years ago, and we know that today they use totally different tools that allow them to configure hundreds or [thousands of servers simultaneously](https://twitter.com/devops_borat/status/41587168870797312). What has changed in the server world that we're failing to reproduce in the networking world?

There are a few usual reasons why you'd go outside of your comfort zone:

-   You have to start from scratch (read: startups), in which case you'd do anything to make you different (and hopefully more efficient) so you could compete with the incumbents, which is why the [Netflixes](https://blog.ipspace.net/2014/08/toolsmith-netflix-on-software-gone-wild.html) and [Spotifys](http://blog.ipspace.net/2014/07/network-automation-spotify-on-software.html) of the world are heavy users of network automation;
-   You grow so big and have so many problems that you simply snap, have a mental breakdown, and start doing things some other way, which is why people like [Google](https://blog.ipspace.net/2012/05/openflow-google-brilliant-but-not.html) and [Amazon](http://blog.ipspace.net/2013/12/packet-forwarding-in-amazon-vpc.html) started doing things the sensible way;
-   You slowly get lured into this new world by [stories of other people](http://www.ipspace.net/Podcast/Software_Gone_Wild) who successfully made the transition that made their life easier, and this is probably how most enterprise networking engineers will slowly get more comfortable with the SDN concepts -- this was also how many server admins started embracing Chef, Puppet and other tools, and figured out that those tools actually solve their problems.

Of course there's another path: a new technology is dumped into your lap by an over-naive CxO who likes to read industry press or analyst reports and believes that vendors or analysts know more about his business and his network (without ever seeing it) than his own engineers.

### The First Steps

Assuming you're a typical enterprise (or small service provider) networking engineer who wants to become more comfortable with the brave new world of SDN, you'll find tons of resources on my [SDN pages](https://www.ipspace.net/SDN):

-   An [SDN focused podcast](http://www.ipspace.net/Podcast/Software_Gone_Wild);
-   Plenty of [free SDN webinars](http://content.ipspace.net/bin/publicWebinars) (including a fantastic high-level step-by-step guide to [network programmability](http://content.ipspace.net/get/NetProg101) by Matt Oswalt);
-   [In-depth webinars](https://www.ipspace.net/Roadmap/SDN_and_OpenFlow_webinars) covering SDN basics, [OpenFlow](http://www.ipspace.net/OpenFlow_Deep_Dive), [NETCONF and YANG](https://www.ipspace.net/NETCONF_and_YANG), [deployment guidelines](http://www.ipspace.net/SDN_Architectures_and_Deployment_Considerations), and [management aspects](http://www.ipspace.net/Monitoring_Software_Defined_Networks).
