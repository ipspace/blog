---
title: "Lab: Protect IS-IS Routing Data with MD5 Authentication"
series_title: "Protect IS-IS Routing Data with MD5 Authentication"
date: 2025-09-26 07:40:00+02:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/feature/3-md5/
---
Like OSPF and BGP, IS-IS contains a simple mechanism to authenticate routing traffic – IS-IS packets can include a cleartext password or an [MD5](https://datatracker.ietf.org/doc/html/rfc5304)- or [SHA hash](https://datatracker.ietf.org/doc/html/rfc5310). Unlike OSPF, IS-IS can also authenticate:

-   The hello packets exchanged between routers
-   The contents of Link State PDUs flooded across an area or a domain.

Want to know more? Check out the [Protect IS-IS Routing Data with MD5 Authentication](https://isis.bgplabs.net/feature/3-md5/) lab exercise.

{{<figure src="https://isis.bgplabs.net/feature/topology-md5.png" width="300">}}

[Click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://isis.bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `feature/3-md5` and execute **netlab up**.
