---
title: "Projects to Work On – the AI Recommendations"
date: 2025-02-13 07:49:00+0100
tags: [ worth reading ]
---
Vini Motta decided to use AI on ipSpace.net content to find what it would recommend as the projects to work on in order to become employable in 2025. Here are the results he sent me; my comments are inline on a gray background.

Network Automation with Python
: Project: Automate basic network tasks like device configuration, backup, or monitoring using Python scripts.
<!--more-->
{{<long-quote>}}
Depending on your programming background, Ansible might be a [better starting point](https://blog.ipspace.net/2017/02/network-automation-and-undifferentiated/). Also: [potential Python tools/libraries to use](https://blog.ipspace.net/2019/09/paramiko-netmiko-napalm-or-nornir/).
{{</long-quote>}}

BGP Fundamentals and Route Manipulation
: Project: Build a small BGP lab to demonstrate routing policies, route filtering, and BGP path selection. You can showcase both internal and external BGP scenarios.

{{<long-quote>}}
Before someone starts the "we don't need no routing in SD-WAN world" mantra, have you ever looked at how you connect to any reasonably-sized public cloud ;)

Also, there's a great tool that allows you to [run free BGP labs in GitHub Codespaces](https://blog.ipspace.net/2024/06/bgp-labs-github-codespaces/), or master BGP using a [long sequence of structured lab exercises](https://bgplabs.net/)?
{{</long-quote>}}

Docker Networking
: Project: Set up a Docker environment where you manage networking between containers, perhaps integrating with an overlay network or using Docker's built-in networking capabilities.

{{<long-quote>}}
Docker is obsolete according to the gospel of K8S evangelists, but we keep using it everywhere, so this probably makes sense as well. You could use [this Vagrantfile](https://github.com/ipspace/docker-examples/blob/master/Vagrantfile) and [other examples from the same repository](https://github.com/ipspace/docker-examples/tree/master) to get you started.

Also: containerlab.
{{</long-quote>}}

Kubernetes Networking
: Project: Create a Kubernetes cluster and demonstrate network policy enforcement, service discovery, and load balancing within the cluster.

{{<long-quote>}}
I have this one on my to-do list for ages (current excuse: waiting for [clabernetes](https://containerlab.dev/manual/clabernetes/) to come out of beta).

There are several good tutorials describing how to build a K8S cluster between Vagrant-controlled virtual machines, and a [lovely (free) webinar to get you started](https://my.ipspace.net/bin/list?id=Kubernetes).
{{</long-quote>}}

### Anything Else?

I would add *networking in public clouds* to the list. The public cloud to work on depends on your geography and environment. I would start with AWS, but Azure tends to be more popular in some enterprise environments.

When you open that can of worms (and decide it's time to move beyond ClickOps), you'll quickly get into *infrastructure-as-code* waters and start working with tools like Terraform or Pulumi. Also, check out my [AWS and Azure examples](https://github.com/ipspace/pubcloud) if you get stuck.