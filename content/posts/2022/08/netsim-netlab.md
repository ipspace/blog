---
title: "netsim-tools Renamed to netlab"
date: 2022-08-27 11:35:00
tags: [ automation ]
series: [ netlab, netsim ]
netlab_tag: release
---
**TL&DR**: we renamed *netsim-tools* to *netlab* as the project evolved from a bag of tools into a full-blown intent-based lab-as-code system (how's that for a Bullshit Bingo winner?).

There is no change to the functionality, user interface (CLI commands), or documentation. Upgrading the existing Python package should install the new one.

Now for more details:
<!--more-->
* The bulk of the change was renaming the Python package to *networklab*[^NLP] and fixing documentation (replacing all *netsim-tools* references with *netlab*). We also bumped the version to 1.3 ([release notes](https://netsim-tools.readthedocs.io/en/latest/release/1.3.html))
* GitHub repositories have been renamed: **ipspace/netsim-tools** to **ipspace/netlab** and **ipspace/netsim-examples** to **ipspace/netlab-examples**. GitHub creates automatic redirects -- git remotes and forks still work -- but it might be a good idea to update your remote repositories with `git remote set-url`. @Loren: thanks a million for the [tip](https://blog.ipspace.net/2022/08/netsim-netlab.html#1346)!
* The Python modules have not been renamed
* The readthedocs documentation URL has not changed yet. We might change it sometime in the future.
* netlab-related blog posts were updated to use the new project name and repository URL. The blog post URLs will not change.

[^NLP]: ... because someone squatted on *netlab* package a few days before I planned to make the change. Bummer.
 
What's the impact:

* If you haven't used netlab before: none. Follow the [updated installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html).
* A happy user? Remove *netsim-tools* package with `pip3 uninstall netsim-tools` and install *networklab* package with `pip3 install networklab` (or [whatever else you're doing to manage your Python packages](https://xkcd.com/1987/)).
* You can also upgrade the *netsim-tools* package with `pip3 install --upgrade netsim-tools`. That command will remove the old *netsim-tools* package, replace it with an empty stub, and install the *networklab* package (now a dependency of *netsim-tools*).

### Revision History

2022-08-28
: Renamed GitHub repositories based on feedback by Loren.