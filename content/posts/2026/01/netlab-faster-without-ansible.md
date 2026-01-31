---
title: "How Moving Away from Ansible Made netlab Faster"
date: 2026-01-19 07:36:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
**TL&DR:** Of course, the title is clickbait. While the differences are amazing, you won't notice them in small topologies or when using [bloatware that takes minutes to boot](/2023/02/virtual-device-boot-times/).

Let's start with the background story: due to the (now fixed) [suboptimal behavior of bleeding-edge Ansible releases](/2025/12/ansible-abandoned-network-automation/), I decided to [generate the device configuration files within _netlab_](https://netlab.tools/release/26.01/#configuration-deployment-changes) (previously, _netlab_ prepared the device data, and the configuration files were rendered in an Ansible playbook).

As we use **bash** scripts to configure Linux containers, it makes little sense (once the **bash** scripts are created) to use an Ansible playbook to execute **docker exec _script_** or **ip netns _container_ exec _script_**. _netlab_ release 26.01 runs the **bash** scripts to configure Linux, Bird, and dnsmasq containers directly within the **netlab initial** process.

Now for the juicy part.
<!--more-->
I used a [very large topology](https://github.com/ipspace/netlab/blob/e2c169a097ceb4c3e2b44b110bb234f2844f7808/tests/platform-integration/large/01-large-topo.yml) with 300 Linux containers and 6 switches (FRRouting containers) to measure the time it takes to start the lab. Here's how long it takes to start it with _netlab_ release 25.10 (using Ansible to create and deploy configurations):

| Step | Elapsed time | CPU time |
|------|-------------:|---------:|
| **netlab create** | 18 seconds | 18 seconds |
| **containerlab deploy** | 39 seconds | < 1 second |
| **netlab initial** | 2 minutes 20 seconds | ~ 12 minutes |
| **containerlab destroy** | 37 seconds | < 1 second |
{ .fmtTable #results }

**Notes:**

* The measured times are not statistically significant[^RTO]
* I have a server with a 16-core AMD Ryzen CPU, SSD disks, and 64GB of memory; the elapsed times might be a bit on the low end.
* Reducing the printouts with the `--quiet` option did not change the execution times significantly[^CES].
* **netlab create** does the data transformation, stores transformed data in YAML and pickled format, and creates Ansible and containerlab configuration files
* **containerlab deploy** starts the containers. The process takes as long as it takes (Docker is doing all the work); the time spent in **containerlab** itself is minimal.
* **netlab initial** runs the Ansible playbook that deploys the device configurations. It looks like that playbook burns ~5 CPU cores (the number of parallel threads Ansible is using) for well over two minutes.

[^RTO]: A fancy way of saying "I only ran the tests once". The first digit and the order of magnitude are probably not too far off.

[^CES]: Sometimes, the quiet version of the command would be slower than the chatty one, but the difference is probably well within the non-existent error bars (see the previous footnote).

It's worth noting that the Ansible playbook is a bit convoluted:

* It has to find the template file
* It has to find the task list that is used for the particular device
* It runs the task list, which does the actual configuration deployment
* The Linux container task list creates a temporary file, renders the template into that file, executes **ip netns exec**, and deletes the temporary file -- plenty of Ansible module calls for what's effectively a very straightforward operation.

Next, I tested _netlab_ release 26.01 that:

* Generates configuration files within **netlab create**
* No longer stores the transformed data in YAML format
* Runs Linux configuration scripts directly.
* Executes several Linux configuration scripts in parallel[^CF]

[^CF]: It's using **concurrent.futures.ThreadPoolExecutor** with the default number of threads.

Here are the relevant results (the containerlab configuration file did not change, so there were no changes in containerlab times):

| Step | Elapsed time | CPU time |
|------|-------------:|---------:|
| **netlab create** | 10 seconds | 10 seconds |
| **netlab initial** | 11 seconds | ~ 40 seconds |
{ .fmtTable }

Amazingly, using Jinja2 templates to generate configuration files for 300+ devices is much faster than simply storing the transformed data in YAML format[^YS].

Even better, the configuration deployment time went from 140 seconds (2 minutes 20 seconds) to 11 seconds. Most of that time was spent configuring the six FRRouting containers with the Ansible playbook.

[^YS]: In case you didn't know: YAML performance sucks.

Finally, I have experimental[^XC] (as of mid-January 2026) code that configures FRRouting containers with Linux scripts executed directly from **netlab initial**. Here's how fast that code configures 300 hosts and 6 switches:

[^XC]: It's experimental because FRRouting gets twitchy if you try to configure it too early. 

| Step | Elapsed time | CPU time |
|------|-------------:|---------:|
| **netlab create** | 10 seconds | 10 seconds |
| **netlab initial** | 4 seconds | ~ 21 seconds |
{ .fmtTable }

The only thing left: a huge THANK YOU to (you know how you are) for a pretty hard kick in the direction that reduced configuration deployment time by a factor of 30+.

