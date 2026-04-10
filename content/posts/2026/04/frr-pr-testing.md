---
title: "Testing FRRouting Pull Requests with netlab"
date: 2026-04-16 07:50:00+0200
tags: [ netlab ]
netlab_tag: use
---
Every other blue moon, I discover a bug in FRRouting ([example](/2026/04/frr-evpn-ipv6-pmsi/)). Because the FRRouting developers care about their work, it usually gets fixed within a few days, often resulting in a "can you test this PR?" question.

It turns out that's surprisingly easy to do with _netlab_ -- here's the step-by-step procedure (assuming you already have the topology file that reproduced the bug):
<!--more-->
* Clone the FRRouting GitHub repository:

```
git clone https://github.com/FRRouting/frr
```

* Go into the newly-created directory (usually **frr**) and switch to the correct branch. That's easiest to do if you use [GitHub CLI](https://cli.github.com/):

```
gh pr checkout 21488
```

* Build the FRRouting container from the sources. The build script is included in the FRRouting repository and takes surprisingly little time[^LT].

[^LT]: For old-timers like myself, used to operating systems taking half a day to compile and build.

```
./docker/alpine/build.sh
```

* The build process results in a FRRouting container named something like `frr:alpine-blah-blah`. Make that container the default _netlab_ FRRouting image. You could either change the [user defaults](https://netlab.tools/defaults/#changing-defaults-in-user-defaults-files) or [use an environment variable](https://netlab.tools/defaults/#changing-defaults-with-environment-variables) (choose one of the following commands):

```
netlab defaults devices.frr.clab.image=frr:alpine-6bb1602358
export NETLAB_DEVICES_FRR_CLAB_IMAGE=frr:alpine-6bb1602358
```

* Start the lab using your bug-reproducing lab topology and check that it uses the correct FRRouting image. You could look at the *containerlab* printout generated during **netlab up**,  or use **docker ps**, **containerlab inspect**, or the new **[netlab report devices](https://netlab.tools/netlab/report/)**.

| Node | Node ID | Device | Image |
|------|--------:|--------|-------|
| h1 | 3 | linux | python:3.13-alpine |
| h2 | 4 | linux | python:3.13-alpine |
| h3 | 5 | linux | python:3.13-alpine |
| h4 | 6 | linux | python:3.13-alpine |
| s1 | 1 | frr | frr:alpine-6bb1602358 |
| s2 | 2 | eos | ceos:4.35.2F |
{ .fmtTable }

* When you're done testing, don't forget to delete the changed default image (if you used the **[netlab defaults](https://netlab.tools/netlab/defaults/)** command):

```
netlab defaults --delete --user devices.frr.clab.image
```

Have fun!
