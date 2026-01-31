---
title: "Fast FRR Container Configuration"
date: 2026-02-02 07:47:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
After creating the infrastructure that [generates the device configuration files within _netlab_](/2026/01/netlab-faster-without-ansible) (not in an Ansible playbook), it was time to try to apply it to something else, not just Linux containers. FRR containers were the obvious next target.

_netlab_ uses two different mechanisms to configure FRR containers:

* Data-plane features are configured with **bash** scripts using **ip** commands and friends.
* Control-plane features are configured with FRR's **vtysh**

I wanted to replace both with Linux scripts that could be started with the **docker exec** command.
<!--more-->
### Shebang To The Rescue

We used an [Ansible task list](https://github.com/ipspace/netlab/blob/0f6c98ba9cff8585b42469bbe947f2a8f5b11eb2/netsim/ansible/tasks/deploy-config/frr.yml) to solve the script-or-config challenge. The task list:

* Renders a configuration template into a file within the container (or VM) and a local variable
* Checks the contents of the rendered template and executes the remote file if the contents start with a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))
* Otherwise, **vtysh -f _filename_** is invoked within the container or VM

Interestingly, one can use [anything as the interpreter in a script](/2017/10/turn-your-ansible-playbook-into-bash/). If a script starts with `#!/usr/bin/vtysh -f`, **vtysh** is invoked as the program to process the script, `-f` is passed as the first argument to **vtysh**, and the script filename as the second argument -- precisely what we need to turn FRRouting configuration into an executable Linux script.

The new _netlab_ release (coming out as 26.02 sometime in February, already [available](https://netlab.tools/install/clone/) as the *dev* branch) can prepend a device-specific shebang to configuration files that lack one, resulting in executable Linux scripts. We could already [execute configuration scripts on containers](/2026/01/netlab-faster-without-ansible), so I declared Mission Accomplished and started the integration tests.

### The Glitches

While the integration tests finished way faster than before, I got unexpected failures. Some of them were easy to fix:

* Some of the integration tests were too aggressive; it turns out that Ansible's leisurely configuration pace gave FRR devices just enough time to get the job done behind the scenes. Increasing the wait timers resolved this issue.
* I found an interesting race condition when deploying a large number of containers -- without significant CPU load, the **bash** script configured the VLAN interface addresses before the *zebra* daemon did. When running dozens of scripts in parallel, *zebra* sometimes woke up before the **ip addr** command could do its job, and **ip addr** complained about an existing IP address. The fix was trivial: [don't step on *zebra*'s toes](https://github.com/ipspace/netlab/pull/3041).

Unfortunately, I also experienced bizarre behavior. For example, RIPv2 would accept the **redistribute** configuration commands (they were in the device configuration) but wouldn't redistribute routes. Even worse, SRv6 configuration consistently failed with *vtysh* claiming it cannot talk with the BGP daemon *even though it successfully configured BGP milliseconds before*.

The root cause turned out to be the amazing speed of the configuration scripts. *containerlab* just starts the FRRouting containers and moves on, and in the old days, it took Ansible long enough to warm up its muscles for the FRRouting daemons to get ready. I found no mechanism to determine when the FRRouting gaggle of daemons is ready to do business (if you have an idea, please leave a comment), so I gave up and implemented a QDS[^QDS] -- *containerlab* executes **sleep 1** after starting the FRR containers -- and everything worked smoothly ever after.

[^QDS]: Quick and Dirty Solution

### The Results Are In

Here's how fast the new approach configures a [~200-node leaf/spine/superspine fabric](https://github.com/ipspace/netlab/blob/dev/tests/platform-integration/large/x-large-fabric.yml) ([diagram](/2026/02/large-fabric.png)) built with FRR containers:

| Step | Elapsed time | CPU time |
|------|-------------:|---------:|
| **netlab create -o none**[^ON] | 13 seconds | 13 seconds |
| **netlab create** | 24 seconds | 24 seconds |
| **netlab up --no-config** | 1 minute 20 seconds | 1 second |
| **netlab initial** (Linux scripts) | 10 seconds | 22 seconds |
| **netlab initial** (Ansible) | 4 minutes 50 seconds | ~ 15 minutes |
| **containerlab destroy** | 37 seconds | < 1 second |
{ .fmtTable }

Ten seconds to configure 200 nodes? Not too shabby, if I say so myself ;)

[^ON]: This command performs the lab topology transformation, but does not create output files.

**Notes:**

* See the [previous blog post](/2026/01/netlab-faster-without-ansible#results) for a detailed description of what individual commands do.
* The measured times are not statistically significant[^RTO]
* I have a server with a 16-core AMD Ryzen CPU, SSD disks, and 64GB of memory; the elapsed times might be a bit on the low end.
* **netlab create** spends almost half of its runtime writing output files. Most of that time is spent writing YAML files[^DWF] (containerlab configuration and Ansible inventory). Some of that overhead is already gone; in the next release, we'll [use JSON files for Ansible group/host vars](https://github.com/ipspace/netlab/pull/3046).
* **netlab up** spends almost all of its time waiting for **containerlab**, which spends most of its time waiting for Docker.

[^RTO]: A fancy way of saying "I only ran the tests once". The first digit and the order of magnitude are probably not too far off.

[^DWF]: The timing difference between writing the inventory data for an edge switch (with four BGP neighbors) and a spine switch (with 68 BGP neighbors) is clearly noticeable in the printout.

