---
date: 2023-05-02 06:43:00+00:00
netlab_tag: archive
series_title: Aruba CX, External Tools, Tunnel Interfaces (Release 1.5.2)
tags:
- netlab
title: 'netlab Release 1.5.2: Aruba CX, External Tools, Tunnel Interfaces'
---
_netlab_ [release 1.5.2](https://netlab.tools/release/1.5/#release-1-5-2) brings another bunch of cool features, including:

- [Aruba AOS-CX Support](https://netlab.tools/platforms/) by Stefano Sasso
- [External network management tools](https://netlab.tools/extools/) that you can start together with your lab
- [Tunnel interfaces](https://netlab.tools/links/#links-tunnel)
- [Reusable topology components](https://netlab.tools/components/)

I'll cover these features in separate blog posts; today I wanted to highlight a few minor additions:
<!--more-->
* **Add `--force` flag to [`netlab down`](https://netlab.tools/netlab/down/) command**. It was impossible to clean up the lab directory if you managed to create a lab topology that upset the orchestration tool[^CL]. The new `--force` flag allows you to force a directory cleanup with `netlab down --cleanup --force`.

[^CL]: Most common scenario: creating *containerlab* file binds pointing to invalid file names.

* *netlab* can create configuration files for lab containers (primarily Linux hosts). These files are created before the lab is started and are executed within *netlab*, making it impossible to use anything but the standard Jinja2 filters. Release 1.5.2 allows you to **[use some Ansible filters when creating container configuration files](https://netlab.tools/labs/clab/#jinja2-filters-available-in-custom-configuration-files)**

* The *find custom configuration template* logic was extended to include node name in the search list. This allows you to deploy **[per-node custom configuration templates](https://netlab.tools/dev/config/deploy/#finding-custom-configuration-templates)**, for example to [include saved device configurations when starting a new lab](/2023/04/netlab-merge-config/).

* `netlab up` and `netlab down` commands support **dry run mode** (`--dry-run` option) that prints the commands that would be executed instead of executing them -- that might come handy when you're trying to troubleshoot bizarre failures.

### Upgrading

To get more details and learn about additional features included in release 1.5.2, [read the release notes](https://netlab.tools/release/1.5/#release-1-5-2). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
