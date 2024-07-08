---
title: "BGP Labs: Session Templates"
series_title: "Session Templates"
date: 2024-02-14 07:35:00+01:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/session/6-templates/
---
Configuring an IBGP session on a route reflector takes a half-dozen parameters, starting with the remote BGP AS number (equal to the local one), remote IP address, and the source IP address or interface. You might have to specify the propagation of BGP communities and an MD5 password, and you will definitely have to specify that the BGP neighbor is a route reflector client.

Wouldn't it be nice if you could group those parameters into a template and apply the template to a neighbor? Most BGP implementations have something along those lines. That feature could be called a *session template* or a *peer group*, and you can practice it in the [next BGP lab exercise](https://bgplabs.net/session/6-templates/).

{{<figure src="https://bgplabs.net/session/topology-session-templates.png">}}
