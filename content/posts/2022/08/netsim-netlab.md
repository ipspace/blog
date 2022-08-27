---
title: "netsim-tools Renamed to netlab"
date: 2022-08-27 11:35:00
tags: [ automation ]
series: [ netlab, netsim ]
netsim_tag: release
---
**TL&DR**: we renamed *netsim-tools* to *netlab* as the project evolved from a bag of tools into a full-blown intent-based lab-as-code system (how's that for a Bullshit Bingo winner?).

There is no change to the functionality, user interface (CLI commands), or documentation. Upgrading the existing Python package should install the new one.

Now for more details:
<!--more-->
* The bulk of the change was renaming the Python package to *networklab*[^NLP] and fixing documentation (replacing all *netsim-tools* references with *netlab*). We also bumped the version to 1.3 ([release notes](https://netsim-tools.readthedocs.io/en/latest/release/1.3.html))
* The Python modules have not been renamed
* The readthedocs documentation URL has not changed yet. We might change it sometime in the future.
* I will update the netlab-related blog posts to use the new project name. The blog post URLs will not change.

[^NLP]: ... because someone squatted on *netlab* package a few days before I planned to make the change. Bummer.
 
What's the impact:

* If you haven't used netlab before: none. Follow the [updated installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html).
* A happy user? Remove *netsim-tools* package with `pip3 uninstall netsim-tools` and install *networklab* package with `pip3 install networklab` (or [whatever else you're doing to manage your Python packages](https://xkcd.com/1987/)).
* You can also upgrade the *netsim-tools* package with `pip3 install --upgrade netsim-tools`. That command will remove the old *netsim-tools* package, replace it with an empty stub, and install the *networklab* package (now a dependency of netsim-tools).

Finally: we haven't renamed GitHub repository yet. Renaming it would break Git remotes for everyone who forked or cloned netsim-tools source code or associated examples. Not renaming it might lead to confusion down the line. Would love to hear your thoughts on this topic.
