---
title: "Using netlab to Configure Live Devices"
date: 2026-06-08 08:02:00+0200
tags: [ netlab ]
netlab_tag: use
---
Leo Fleskes sent me an interesting question after reading my [Generate Partial Device Configurations with netlab](/2026/04/netlab-generate-device-configs/) blog post:

> What is stopping us from eventually, given enough usage and coverage, using _[netlab](https://netlab.tools)_ to configure devices in the live network?

In theory, nothing. In practice, you might hit a few hurdles:
<!--more-->
* You might discover you need numerous features **_netlab_ does not support** (yet). ACLs immediately come to mind. While you could solve that with custom device configurations, the whole setup would quickly get clunky. But hey, if you're OK with the functionality we implemented so far, keep reading.
* **_netlab_ does not integrate with IPAM systems** like _netbox_. While doing some simple integration would be trivial, maintaining consistent subnet assignments[^CSA] would be way harder. You could pull data from an IPAM system and augment the _netlab_ topology file[^PEV], but it's an extra DIY step.
* **_netlab_ does not generate full device configurations**. It creates per-technology configuration snippets that are deployed in a predefined sequence, and multiple configuration snippets might configure the same objects (interfaces or routing protocols). A naive merge of the configuration snippets (copy them into the final configuration file in the correct seqneuce) might result in a working device configuration[^CLSC], but I wouldn't use the merged contents to try to replace the running configuration[^PWS]. Yet again, you could write your own script that would do an intelligent merge of configuration commands for individual configuration objects.
* **_netlab_ assumes the devices are not configured**. It generates the device configurations needed to deploy the features requested in the topology file, but cannot bring an already-configured device to the new state. You could try to use configuration replacement to do that, but see above.
* **_netlab_ describes the whole network as a single YAML file**. While that's not too far from the simple Ansible+YAML automation solutions some [hipsters were so vocal about](/2022/11/public-cloud-snowflakes/) in the past, it's not what I would hope to have as an automation solution for a production network. YMMV.

[^PWS]: It would most likely work on Junos, probably on Arista EOS, but maybe not on Cisco IOS.

[^CSA]: Assigning the same subnet to a link regardless of whether the number of links changed.

[^PEV]: Potentially using environment variables instead of modifying the topology file

[^CLSC]: You can use that approach to generate startup configurations for _containerlab_ devices. It works because the container managing the device VM uses an expect-like script to type the startup configuration into the console session.

Alternatively, you can always use the [_netlab_ configuration templates](https://github.com/ipspace/netlab/tree/dev/netsim/ansible/templates) -- create the device data structures used in our templates from whatever source, and use the templates to generate tested device configurations. Numerous data structures are described in the [netlab implementation notes](https://netlab.tools/dev/config/); if you feel like improving that documentation, you're most welcome.
