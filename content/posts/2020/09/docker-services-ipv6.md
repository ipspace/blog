---
title: "Accessing Docker Container Services over IPv6"
date: 2020-09-22 05:49:00
tags: [ Docker, IPv6 ]
---
Getting Docker to work with IPv6 is an interesting and under-documented (trying to stay diplomatic) adventure, but there's a shortcut to the promised land: even if your Docker environment is pure IPv4 morass, you can still [reach published container ports over IPv6](/kb/DockerSvc/50-ipv6.html) thanks to the [userland proxy](/kb/DockerSvc/40-userland-proxy.html) I described last week. The performance is obviously commensurate with traversing kernel-user boundary too many times.

New to this rabbit hole? [Start here](/kb/DockerSvc/index.html).

Finally, you don't have to tell me (again) that Docker is dead and we should all use K8s. It's as useful as telling me CloudStack is dead and we should all use OpenStack. Different challenges deserve different tools.

