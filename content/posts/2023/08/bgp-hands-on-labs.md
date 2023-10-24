---
title: "New Project: BGP Hands-On Labs"
date: 2023-08-03 09:04:00
tags: [ BGP ]
---
Approximately 30 years ago I managed to persuade the powers-that-be within Cisco's European training organization that they needed a deep-dive BGP course, resulting in a 3 (later 5) day Advanced BGP Configuration and Troubleshooting (ABCT) course[^CD]. I was delivering that course for close to a decade, and gradually built a decent story explaining the reasoning and use cases behind most of (then available) BGP features, from simple EBGP sessions to BGP route reflectors and communities[^EC].

Now imagine having more than a dozen hands-on labs that go with the "_BGP from rookie to hero_" story available for any platform of your choice[^NL]. I plan to make that work (eventually) as an open-source project that you'll be able to download and run free-of-charge.
<!--more-->
The project will be based on _netlab_[^HT] and use Cumulus Linux (or FRR if NVIDIA strays too far away from being useful) as external BGP routers. You'll be able to use whatever networking devices you wish to work on[^XP], and if they happen to be supported by _netlab_ you'll get lab topology and basic device configuration for each lab set up in seconds[^XR]. I will also provide device configurations for the external BGP routers for people who love wasting time with GUI.

[^XP]: Including physical hardware if you happen to have a few extra Cumulus switches or are willing to do some crazy stuff to set things up.

I set up a [GitHub repository](https://github.com/ipspace/bgplab) and created the [first labs](https://bgplab.github.io/bgplab/). I also put together a long list of [labs that would be nice to have](https://bgplab.github.io/bgplab/3-upcoming/). I might add newer BGP features and BGP security to the list, but it's already long enough that it will take me months[^AL] to create all the planned labs. I probably missed something important, or you might have better ideas how to structure them -- leave a comment or (even better) become a contributor and submit a PR.

### Revision History

2023-08-21
: The list of lab ideas has been heavily restructured based on your feedback (thank you!). I also added links to the first labs.

[^EC]: The echoes of those ideas are still visible (if you know where to look) in the Configuring BGP on Cisco Routers course --  ABCT eventually morphed into CBCR and became part of the original CCIP curriculum in early 2000s, but that's another story.

[^CD]: If you happen to have the original ABCT course description please send it over. I tried to find it in Web Archive but it's been way too long...

[^NL]: As long as it's supported by _netlab_.

[^HT]: When you happen to have a Hammer of Thor handy everything looks like a nail waiting to be hit ;)

[^XR]: Unless you love using resource hogs like Nexus OS, IOS XR, or some Junos variants.

[^AL]: At least... look at how quickly my [How Networks Really Work project](https://blog.ipspace.net/2019/05/its-time-for-another-pet-project.html) is progressing; it's been over four years since I started it.