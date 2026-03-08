---
title: "Automating netlab-Based Cisco SD-WAN Deployment"
date: 2026-03-09 08:29:00+0100
tags: [ SD-WAN, netlab ]
netlab_tag: use
sd-wan_tag: cisco
---
We haven't implemented support for Cisco SD-WAN in _[netlab](https://netlab.tools/)_ yet, and we might never do so; after all, _netlab_ isn't meant to be a kitchen sink of vendor-specific features. However, having an open-source tool that uses [input](https://netlab.tools/topology-reference/) and [output](https://netlab.tools/outputs/ansible/) files with standardized encoding (JSON or YAML) makes it easy to develop an independent solution that adds functionality.

That's exactly what [Sebastien d'Argoeuves](https://www.linkedin.com/in/seb-dargoeuves/) did: he developed a [solution](https://github.com/sdargoeuves/automate_cisco_sdwan_lab) that automates Cisco SD-WAN deployment after the corresponding _netlab_ lab is started, and published it in a [GitHub repo](https://github.com/sdargoeuves/automate_cisco_sdwan_lab). If you're an SD-WAN fan, you must give it a try ;)
