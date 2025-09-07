---
title: "netlab 25.09: IPv6 RA, Link Impairments, and Performance Gains"
series_title: "IPv6 RA, Link Impairments, and Performance Gains (Release 25.09)"
date: 2025-09-08 08:14:00+01:00
tags: [ netlab ]
netlab_tag: release
---
[*netlab* release 25.09](https://netlab.tools/release/25.09/) includes:

- Link impairment (implemented with Linux *netem* queuing discipline) defined in [lab topology](https://netlab.tools/links/#links-netem) or configured/controlled with the **[netlab tc](https://netlab.tools/netlab/tc/)** command
- Configurable [IPv6 Router Advertisement](https://netlab.tools/links/#links-ra) parameters
- The [**files** plugin](https://netlab.tools/plugins/files/#plugin-files) to store the content of short files (including custom configuration templates) directly in the lab topology
- Support for Nokia SR-OS container (SR-SIM)
- Support for very large topologies (tested so far: [approximately 3000 lab devices](/2025/09/netlab-lab-size/))

But wait, there's more (as always):
<!--more-->
- Stefano Sasso implemented EVPN VLAN bundle service on Junos and Aruba CX
- You can enable debugging on Cisco IOS and FRR devices when starting the lab
- `isis-nodes` report (available as text, Markdown, or HTML) describes IS-IS nodes, areas, system IDs, and IS-types
- `ssh_config` report [creates an SSH configuration file](https://netlab.tools/example/external/#external-ssh-forwarding) you can use to establish SSH sessions with the lab devices using the *netlab* server as a proxy host.

We also added the `isis` graph type that creates a graph of IS-IS routing (including areas, color-coded circuit types, and stub networks) as well as a half-dozen other graphing goodies:

- Graph titles can be defined with the **graph.title** topology parameter
- BGP graphs can display a subset of address families. They can also display local-as IBGP and confederation EBGP sessions, or style VRF BGP sessions as dashed lines.
- You can set `color`, `width`, and `fill` attributes on nodes and links.

Finally, the performance improvements (most notable in large topologies with hundreds of nodes):

- Shared container files (for example, /etc/hosts shared across all Linux and FRR containers) reduce the lab creation time by a factor of three
- The `pickle` snapshot file (replacing a YAML file) reduces the  start time of various **netlab** commands by a factor of almost ten
- Cached Jinja2 templates also don't hurt (they drastically sped up the integration test reports).

Want even more goodies? Explore the [release notes](https://netlab.tools/release/25.09/).

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
