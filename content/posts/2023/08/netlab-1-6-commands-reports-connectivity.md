---
title: "netlab 1.6.0: New Commands, Reports, and External 
Connectivity"
series_title: "New Commands, Reports, and External Connectivity (Release 1.6.0)"
date: 2023-08-01 15:08:00
tags: [ netlab ]
netlab_tag: release
---
*netlab* release 1.6.0 has (probably) [the longest release notes so far](https://netlab.tools/release/1.6/#release-1-6-0) as it contains so many user-visible new features including:

### New Commands

Some users were complaining how complex it was to use **netlab create** command to create graphs, inspect data structures, or create custom reports. They might find the new commands easier to use:
<!--more-->
-   **[netlab report](https://netlab.tools/netlab/report/)** generates built-in or user-defined text- or HTML reports based on transformed lab topology.
-   **[netlab graph](https://netlab.tools/netlab/graph/)** generates [topology graph descriptions](https://netlab.tools/outputs/graph/) in GraphViz or D2 format
-   **[netlab inspect](https://netlab.tools/netlab/inspect/)** displays data structures in transformed lab topology

### Reports

You could store a Jinja2 template into a **defaults.outputs.reports.something** dictionary value in the lab topology to create custom reports with previous *netlab* versions -- probably one of the worst kludges I ever made.

The new **netlab report** command can read Jinja2 templates from user-, system- or package directories and create text or HTML reports. The report templates shipping with *netlab* release 1.6 include:

* Node, interface and link addressing reports
* Lab wiring summary
* Device management IP addresses, usernames, and passwords

If you'd like to have other reports, please [open a Github issue](https://github.com/ipspace/netlab/issues) describing what you'd like to see in them.

### Display Internal Information

**netlab show** command can display [configuration modules](https://netlab.tools/netlab/show/#display-configuration-modules), [devices supported by each configuration module](https://netlab.tools/netlab/show/#display-device-module-support), the state of the [virtualization providers](https://netlab.tools/netlab/show/#display-virtualization-providers), [output formats](https://netlab.tools/netlab/show/#display-output-modules) supported by **netlab create** command, and [report templates](https://netlab.tools/netlab/show/#display-report-templates) included with _netlab_. All reports are available in table-, text-, or YAML format.

### External Connectivity

One of the previous versions added the ability to connect *libvirt*-based virtual machines straight to the external networks (using *macvtap* interfaces). A few days after *containerlab* implemented *macvlan* interfaces I [used that functionality in the `clab` provider](https://netlab.tools/labs/clab/#connecting-to-the-outside-world) -- containers started by *netlab* can now communicate directly with external devices.

Finally, I figured out it's not too hard to implement host-to-VM or host-to-container port forwarding, enabling [direct (management) connectivity to lab devices](https://netlab.tools/example/external/#connecting-to-lab-devices) without connecting the management network to the outside world.

### Upgrading

To get more details and learn about additional features included in release 1.6.0, [read the release notes](https://netlab.tools/release/1.6/#release-1-6-0). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab). There's also a [*netlab* channel](https://networktocode.slack.com/archives/C022DQHK8BH) in networktocode Slack team, but you will get faster response time reporting your challenges in GitHub.




  
