---
date: 2022-06-23 06:12:00+00:00
netlab_tag: archive
series_title: VLAN Module Is Complete (Release 1.2.4)
tags:
- netlab
title: netlab VLAN Module Is Complete
---
One of the last things I did before starting the 2022 summer break was to push out the [next netlab release](https://netlab.tools/release/). 

It includes support for routed VLAN subinterfaces (needed to implement router-on-a-stick) and routed VLANs (needed to implement multi-hop VRF lite), completing the lengthy (and painful) development of the [VLAN configuration module](https://netlab.tools/module/vlan/). Stefano Sasso added VLAN support for Mikrotik RouterOS and VyOS, and Jeroen van Bemmel completed VLAN implementation for Nokia SR Linux. Want to see VLANs on other platforms? Read the [contributor guidelines](https://netlab.tools/dev/guidelines/) and [VLAN developer docs](https://netlab.tools/dev/config/vlan/), and submit a PR.

I'll be back in September with more blog posts, webinars, and cool netlab features. In the meantime, automate everything, get away from work, turn off the Internet, and enjoy a few days in your favorite spot with your loved ones!
