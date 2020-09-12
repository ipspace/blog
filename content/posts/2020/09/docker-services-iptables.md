---
title: "How Docker Uses iptables to Implement Published Ports"
date: 2020-09-15 06:04:00
tags: [ Docker ]
---
In [early September](https://blog.ipspace.net/2020/09/docker-services-basics.html) I explained the difference between [exposed](https://www.ipspace.net/kb/DockerSvc/10-Exposed.html) and [published](https://www.ipspace.net/kb/DockerSvc/20-Published.html) Docker container ports. 

Now let's peek behind the curtain and explore [how Docker uses iptables to publish container ports](https://www.ipspace.net/kb/DockerSvc/30-nat-iptables.html), and why it [runs a userland proxy process for every published port](https://www.ipspace.net/kb/DockerSvc/40-userland-proxy.html).

For even more details, explore the [Docker Networking Deep Dive](https://www.ipspace.net/Docker_Networking_Deep_Dive) webinar.

{{<jump>}}[Keep reading](https://www.ipspace.net/kb/DockerSvc/30-nat-iptables.html){{</jump>}}