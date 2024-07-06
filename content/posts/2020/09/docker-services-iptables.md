---
title: "How Docker Uses iptables to Implement Published Ports"
date: 2020-09-15 06:04:00
tags: [ Docker ]
---
In [early September](/2020/09/docker-services-basics.html) I explained the difference between [exposed](/kb/DockerSvc/10-Exposed.html) and [published](/kb/DockerSvc/20-Published.html) Docker container ports. 

Now let's peek behind the curtain and explore [how Docker uses iptables to publish container ports](/kb/DockerSvc/30-nat-iptables.html), and why it [runs a userland proxy process for every published port](/kb/DockerSvc/40-userland-proxy.html).

For even more details, explore the [Docker Networking Deep Dive](https://www.ipspace.net/Docker_Networking_Deep_Dive) webinar.

{{<jump>}}[Keep reading](/kb/DockerSvc/30-nat-iptables.html){{</jump>}}