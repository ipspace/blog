---
title: "Adding a Syslog Server to a netlab Lab Topology"
date: 2025-10-27 07:23:00+0100
tags: [ netlab ]
netlab_tag: use
---
_netlab_ does not support a Syslog server (yet), but it's really easy to add one to your lab topology, primarily thanks to the Rsyslog team publishing a ready-to-run container. Let's do it ;)

### Adding a Syslog Server

Rsyslog is an open-source implementation of a Syslog server (with many bells and whistles, most of which we won't use) that can (among other things) log incoming messages to a file. Even better (for our use case), the Rsyslog team regularly publishes [Rsyslog containers](https://www.rsyslog.com/doc/containers/index.html); we'll use the [`rsyslog/rsyslog-collector` container ](https://www.rsyslog.com/doc/containers/collector.html) because it can "_receive logs via UDP, TCP, and optionally RELP, and can send them to storage backends or files_."
<!--more-->
Let's start our lab topology with a single node -- the collector -- using the recipe from the [Custom Containers or Virtual Machines](https://netlab.tools/example/linux/#custom-containers-or-virtual-machines) documentation:

```
nodes:
  syslog:
    device: linux
    provider: clab
    image: rsyslog/rsyslog-collector
```

After starting the lab, we can log into the collector container and examine its default configuration in the `/etc/rsyslog.d` directory. It's exactly what we need:

* The Syslog server listens on TCP and UDP port 514
* All incoming messages are stored in `/var/log/all.log` (text file) and `/var/log/all-json.log` (JSON file).

### Adding Router Nodes

Next, let's add routers to our [lab topology](https://github.com/ipspace/netlab-examples/blob/master/services/syslog/topology.yml). We'll use Arista cEOS and define a group of routers so we'll be able to apply a custom configuration template (configuring the Syslog server) to all of them:

```
provider: clab
defaults.device: eos

groups:
  routers:
    members: [ r1, r2 ]
    module: [ ospf ]

nodes:
  r1:
  r2:
```

We also need a few links to connect the three nodes:

```
links: [ r1-r2, r2-syslog ]
```

### Using the Syslog Server

Finally, we have to tell the routers to use the Syslog server. We'll use a [custom configuration template](https://netlab.tools/custom-config-templates/) (defined with *[configlets](https://blog.ipspace.net/2025/10/netlab-configlets/)*) and apply it to all routers:

```
plugin: [ files ]

configlets:
  syslog:
    eos: |
     logging host syslog protocol tcp

groups:
  routers:
    config: [ syslog ]
```

There's just a tiny glitch in the above idea :( _netlab_ configures all lab devices with hostnames mapping other nodes to their IP addresses, so one would think that the above Arista EOS command tells the switch to look up the IP address of the host named *syslog* and use it. Alas, that does not work; we have to configure an IP address in the **logging host** command[^MBL].

[^MBL]: Or maybe it's just my bad luck, and using **syslog** as a host name confuses Arista EOS?

Fortunately, _netlab_ also defines **hosts** dictionary as an Ansible group variable, making it accessible to all device configuration templates[^HD]. All we have to do is to use `{{ hosts.syslog.ipv4[0] }}` as the host address of the **syslog** server:

[^HD]: Inspect the `group_vars/all/topology.yml` file to see all Ansible group variables available to all device configuration templates. Alternatively, use `ansible-inventory --host r1` to see everything you can use in a Jinja2 template on R1.

```
configlets:
  syslog:
    eos: |
     logging host {{ hosts.syslog.ipv4[0] }} protocol tcp
```

### Kicking the Tires

Our [lab topology](https://github.com/ipspace/netlab-examples/blob/master/services/syslog/topology.yml) is complete; let's start the lab, log into the syslog server, and examine the `/var/log/all.log` file. Here are the last few lines after the OSPF adjacency has been established between R1 and R2:

```
2025-10-26T13:01:50+00:00 r2 Ospf: Instance 1: %OSPF-4-OSPF_ADJACENCY_ESTABLISHED: NGB 10.0.0.1, interface 10.1.0.2 adjacency established
2025-10-26T13:01:59+00:00 r1 Stp: %SPANTREE-6-STABLE_CHANGE: Stp state is now stable
2025-10-26T13:02:00+00:00 r2 Stp: %SPANTREE-6-STABLE_CHANGE: Stp state is now stable
2025-10-26T13:02:15+00:00 r1 SystemInitMonitor: %SYS-5-SYSTEM_INITIALIZED: System is initialized
```

You can easily replicate the results in GitHub Codespaces:

* [Start a new codespace](/2024/07/netlab-examples-codespaces/) off the **netlab-examples** repository
* [Import an Arista cEOS image](/2024/07/arista-eos-codespaces/)
* Change directory to `services/syslog` and execute **netlab up**
* Connect to the syslog server with **netlab connect syslog**, change directory to `/var/log`, and inspect the `all.log` file.

### Multi-Vendor Solution

Want to be able to use a Syslog daemon from Arista EOS and Cisco IOS devices? No biggie, we'll just add a new device to **configlets.syslog**:

```
configlets:
  syslog:
    eos: |
      logging host {{ hosts.syslog.ipv4[0] }} protocol tcp
    ios:
      logging host syslog transport tcp port 514
```

{{<note info>}}
* Due to the way _netlab_ tries to find a matching custom configuration template, you can specify **ios** as the target device, and that definition covers all IOS/IOS-XE devices because it matches their **ansible_network_os** setting.
* You probably won't see the initial OSPF adjacency messages because Cisco IOS finds its neighbors before the _netlab_ Ansible playbook manages to configure Syslog logging (custom configuration templates are processed as the last step in the device configuration).
{{</note>}}
