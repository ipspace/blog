---
title: "Amazing Speed of Bug Fixes in Nokia SR Linux"
date: 2025-05-21 08:25:00+0200
tags: [  ]
---
A few weeks ago, I was [criticising Nokia's unnecessary changes to the SR Linux configuration data model](/2025/04/api-data-model-contract/), so it's only fair that I also publish a counterexample:

* On April 12th, SR Linux failed one of the [_netlab_ integration tests](https://tests.netlab.tools/). We keep adding functionality to these tests as we discover edge cases we didn't test before, so sometimes a device that passed the test before might fail the modified version.
* I [opened a netlab issue](https://github.com/ipspace/netlab/issues/2142), believing it might be a configuration error on our part.
* It quickly became evident that we're dealing with an SR Linux bug, as the failure to apply routing policies was random.

I thought that was the end of the story and closed the issue, but then something truly amazing happened:
<!--more-->
* [Jeroen](https://github.com/jbemmel) reached out to his Nokia contacts, and on May 1st, [Roman Dodin](https://www.linkedin.com/in/rdodin/) from Nokia left a [comment acknowledging the bug and telling us it has been fixed](https://github.com/ipspace/netlab/issues/2142#issuecomment-2844620921). I never experienced something similar from another networking vendor.
* On May 14th (a month after I accidentally stumbled upon the bug), I got an automated email announcing the SR Linux release 25.3.2.
* I reran the integration tests, and they all passed. **The bug was gone** 😳

I don't think I've ever seen a major networking vendor fixing a bug and shipping a fixed release within a month of the bug being *mentioned* (not even reported through proper channels, let alone by a paying customer). Kudos to the Nokia SR Linux team for a phenomenal job!
