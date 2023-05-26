---
title: "Use Existing Device Configurations in netlab"
date: 2023-04-24 07:39:00
tags: [ netlab, DMVPN ]
---
[Anne Baretta](/kb/NetAutJourney/index.html) decided to use _[netlab](https://netlab.tools/)_ to test a proposed DMVPN topology. As _netlab_ doesn't support DMVPN (and probably never will), he decided to use _netlab_ capabilities to start the lab topology and perform initial configuration, adding DMVPN configuration commands as _custom configurations_. Here's how he described the process:

---

In this case I used _netlab_ as a quick way to get a topology up and running, and then add the DMVPN configuration by hand.
<!--more-->
I built a '3rd party' underlay network in the lab, including the IPsec tunnel to the IoT provider, as well as the redundant hub DMPVPN overlay with two NHRP instances, and it behaves as expected. 

{{<figure src="/2023/04/dmvpn-netlab.png">}}

I (mis)used the **[netlab config](https://netlab.tools/netlab/config/)** command to merge complete configuration files collected with **[netlab collect](https://netlab.tools/netlab/collect/)** to limit the copying and pasting (for instance after changing the topology). For every device I'd execute a command like `netlab config config/hub1.cfg -l hub1`, which I could also optimize with a Bash `for` loop:

``` 
for i in spoke1 spoke2 hub1 hub2 firewall iotprovider; do
  netlab config config/$i.cfg -l $i
done
```

It's a bit hacky, but it works (obviously within limits...). I am looking at a proper Jinja2 template, but while it's fewer lines it is too 'custom' to be of much use 😕

---

An alternate solution would be to use per-node **[config](https://netlab.tools/groups/#custom-config)** parameter, for example:

```
nodes:
  spoke1:
    config: config/spoke1.cfg
  spoke2:
    config: config/spoke2.cfg
  hub1:
    config: config/hub1.cfg
  ...
```

{{<note info>}}An even better solution would be to have _netlab_ [find configuration templates](https://netlab.tools/dev/config/deploy/#finding-custom-configuration-templates) based on node names -- a [feature introduced in release 1.5.2](https://netlab.tools/dev/config/deploy/#finding-custom-configuration-templates).{{</note>}}

Finally, a few gotchas:

* Obviously one wouldn't have the configuration files when starting the lab for the first time, which would crash the final step in the device configuration process. That's not a big deal (the lab would be running and configured), but if it bothers you, skip the _custom configuration_ part of the lab initialization by running `netlab up --no-config` (start the lab but don't configure it) followed by `netlab initial -i -m` (perform initial configuration and configure modules, but don't use the custom configuration templates).
* Changing lab topology might change interface names, link IP prefixes, and interface IP addresses. It might be a good idea to clean up the collected device configurations after running **netlab collect**.

### Revision History

2023-04-27
: Changed a link to _netlab_ 1.5.2 documentation
