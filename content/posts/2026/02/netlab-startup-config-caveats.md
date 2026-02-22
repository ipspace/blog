---
title: "netlab: The Caveats of Using Startup Configurations"
series_title: "The Caveats of Using Startup Configurations"
date: 2026-02-23 07:23:00+0100
tags: [ netlab ]
netlab_tag: details
---
[Petr Ankudinov](https://www.linkedin.com/in/petr-ankudinov/) wrote an excellent comment about _netlab_ [Fast cEOS Configuration](/2026/02/netlab-eos-configuration/) implementation. Paraphrasing the [original comment](https://www.linkedin.com/feed/update/urn:li:activity:7426526191903293440?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7426526191903293440%2C7426553915321757697%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287426553915321757697%2Curn%3Ali%3Aactivity%3A7426526191903293440%29):

>  If the use case is the initial lab deployment, why don't you use *containerlab* **startup-config** option to change the device's startup configuration?

I have to admit, I'm too old to boldly go with the *just use the startup configuration* approach. In ancient times, Cisco IOS did crazy stuff if you rearranged the commands in the startup configuration. But ignoring that historical trivia (Cisco IOS/XE seems to be doing just fine), there are several reasons why I decided to use the startup configurations (and you [can use them](https://netlab.tools/platforms/#platform-config-mode) with some containers) as the last resort:
<!--more-->
* While you can use *partial startup configurations* for most devices for which _containerlab_ supports **startup-config** parameter, _containerlab_ can give Arista cEOS only *complete startup configuration*. That would require _netlab_ to reimplement the initial device configuration that is now managed by _containerlab_.
* None of the devices I tested produce easily-observable error messages when there are errors in startup configurations; they usually generate messages that appear in container logs along with all other boot-related chaff. The outputs (including error messages) of FastCLI-based Linux scripts are easy to capture in the calling process (**netlab initial**) that displays them to the user.
* **netlab initial** uses **docker exec** to execute Linux scripts within the containers, and automatically receives the exit status of the executed Linux scripts, making it trivial to detect configuration errors. I found no similar mechanism for startup configurations.
* _netlab_ configures individual device features with independent configuration snippets. You might get [unexpected side effects](https://github.com/ipspace/netlab/pull/3097) when combining multiple snippets into a single configuration file if the same command happens to be valid in multiple configuration contexts, and the configuration snippets are arranged in just the right way to make the two conflicting parts adjacent.

Finally, we need a mechanism to deploy ad-hoc configurations anyway (using the **netlab config** command), and it's simpler to use a single fast configuration mechanism (when available) than a combination of several mechanisms.
