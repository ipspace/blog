---
date: 2024-07-26 09:14:00+02:00
netlab_tag: guidelines
tags: [ netlab ]
title: "Using netlab Reports"
---
Did you know you can use _netlab_ to generate reports describing your lab topology, IP addressing, BGP details, or OSPF areas? The magic command (`netlab report`) was introduced in August 2023, followed by `netlab show reports` to display the available reports a few months later.

You can generate the reports in text, Markdown, or HTML format. The desired format is selected with the report name suffix. For example, the `bgp-asn.md` report will create Markdown text.

Let's see how that works.
<!--more-->
You'll need a working _netlab_ installation if you want to follow along. If you don't have that:

* Open the [BGP labs](https://bgplabs.net/) in [GitHub codespaces](https://bgplabs.net/4-codespaces/)
* Switch to the `basic/1-session` directory
* Execute `netlab up`

OK, now everyone's on the same page, right? Let's go:

* `netlab report` creates reports from the transformed lab topology data, usually stored in `netlab.snapshot.yml`
* The snapshot file is created when a lab is started; thus, you can always create a report based on a running lab.
* If you don't want to start a lab, execute `netlab create` to create the files you get during the `netlab up` process, including the `netlab.snapshot.yml` file.

Next step: what report do you want to create?

* Use `netlab show reports` to display all available reports.
* That list might be a bit overwhelming, so you can limit the reports to a single markup type by adding the desired suffix as a command argument. For example, if you're interested in HTML reports, use `netlab show reports .html`
* If you're interested in a specific technology, use that technology as a command line argument. For example, use `netlab show reports bgp` to display all BGP-related reports.

Finally, create a report:

* Use `netlab report _report_name_` to create a report. Add an output file name if you want to store a report in a file.
* You might want to create a report on a subset of lab devices. For example, when writing the BGP labs instructions, I often needed a report listing the BGP neighbors of a single router. Use the `--node X` argument to select one or more nodes; in the simple BGP lab, I would use (for example) `netlab report bgp-neighbor.md --node x1`
* You can use wildcards or list several nodes (separated by commas) in the list of nodes.

Last but not least, squeeze the most out of the operating system CLI. For example, I would use `netlab report bgp-asn.md|pbcopy` to get the markdown table describing the BGP autonomous systems into the MacOS pasteboard (and copy it directly into the lab instructions document).

### Getting Started

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

You can also run *netlab* within your browser using (free) GitHub codespaces. To do that, you need a GitHub repository referencing the *netlab* devcontainer, for example, the [BGP labs](https://blog.ipspace.net/2024/06/bgp-labs-github-codespaces/) or [*netlab* examples](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/).
