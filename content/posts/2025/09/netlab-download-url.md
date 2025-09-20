---
title: "Start a Lab From a GitHub netlab Topology File"
date: 2025-09-24 07:37:00+0200
tags: [ netlab ]
netlab_tag: use
---
Someone approached me after my [NOG.HR](https://nog.hr/en/meetups/meetup5/) _netlab_ presentation and said: "_wouldn't it be great if we could just start the lab from an example topology published on GitHub?_"

It took me [almost a year](https://github.com/ipspace/netlab/issues/1388) to get it done, but the [functionality](https://netlab.tools/netlab/up/#usage) finally made it into the [25.09 release](https://netlab.tools/release/25.09/):
<!--more-->

* You can use a URL instead of a topology file name with **[netlab up](https://netlab.tools/netlab/up)** and **[netlab create](https://netlab.tools/netlab/create)** commands.
* _netlab_ recognizes GitHub URLs and appends `?raw=true` to them to get the YAML file contents instead of the HTML page[^SS].
* _netlab_ prefers to download the topology file into an empty directory. It will complain otherwise and ask for a confirmation, but will keep quiet if you use the `--quiet` flag.
* The topology file is downloaded, parsed (to verify it's valid YAML), and saved into `downloaded.yml`. The filename is fixed, and there's no way to change it at the moment.
* After the downloaded topology has been saved, **netlab up** or **netlab create** commands continue like you'd specify `downloaded.yml` as the topology file.

[^SS]: If you want to have a similar support for other public Git repositories, [open an issue](https://github.com/ipspace/netlab/issues) or (even better) [modify the code](https://github.com/ipspace/netlab/blob/763b00b9b94a2c795f818127f23eea1581e9e5a6/netsim/cli/create.py#L71) and [submit a pull request](https://netlab.tools/dev/guidelines/).

You can use this functionality to quickly check the [graph examples](/2025/09/netlab-graphs-colors-lines/) I wrote about a few days ago:

* Copy the link to a lab topology file (for example, `https://github.com/ipspace/netlab-examples/blob/master/graphs/colors-lines/spine-color.yml`)
* Execute **netlab create URL** to download the topology file and transform it.
* Use **netlab graph** command to create graph description files and **dot** or **d2** commands to generate the graphs.
* If you want to experiment, modify the downloaded topology file (`downloaded.yml`), execute **netlab create downloaded.yml** to transform it, and generate modified graphs.
