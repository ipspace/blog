---
title: "Running BGP Labs in GitHub Codespaces"
date: 2024-06-25 07:45:00+02:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
I love open-source tools (and their GitHub repositories). Someone launches a cool idea, and you can dig through their source code to figure out how it works. It beats reading documentation or fixing AI hallucinations every day of the week ;)

Not too long ago, the containerlab team [launched the ability](https://containerlab.dev/manual/codespaces/) to run containerlab within a free[^GHF] container[^DID] running on GitHub, and that seemed like a perfect solution to run the BGP labs (Jeroen van Bemmel pointing me in the right direction was another significant step forward).

<!--more-->
[^GHF]: [Within limits](https://github.com/features/codespaces#pricing)

[^DID]: Yes, Docker-in-Docker is a thing. Maybe it's time we start watching how tops spin around us ;)

Alas, nothing is as simple as it looks. Building a *dev container* is a bit more complex than **docker build**, so I decided to reuse GitHub's work and do it in a GitHub action. I also had to tweak the **netlab** installation scripts a bit (they have to install *containerlab* but not Docker/Moby), but after a few hours, I had a running proof-of-concept. Unfortunately, the initial configuration crashed every time I started the lab due to [yet another Ansible glitch](https://github.com/ipspace/netlab/issues/1219).

Anyway, after a lengthy [yak-shaving exercise](https://www.hanselman.com/blog/yak-shaving-defined-ill-get-that-done-as-soon-as-i-shave-this-yak), I [pushed out *netlab* release 1.8.4](/2024/06/netlab-1-8-4-vrnetlab-cat8000.html), a GitHub action built the container and pushed it to [GitHub container registry](https://github.com/ipspace/netlab/pkgs/container/netlab%2Fdevcontainer), and I could use it in BGP labs.

The results were well worth the effort. Running BGP labs in a GitHub codespaces container is as easy as it gets:

* Open the [Run BGP with GitHub Codespaces](https://bgplabs.net/4-codespaces/) document in your browser
* Click the "*create a new codespace*" link and create a codespace.
* Follow the rest of the instructions and enjoy the free labs ;)

{{<jump>}}[Start with GitHub Codespaces](https://bgplabs.net/4-codespaces/){{</jump>}}
