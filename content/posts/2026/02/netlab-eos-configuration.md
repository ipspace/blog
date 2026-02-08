---
title: "Fast Arista cEOS Container Configuration"
date: 2026-02-09 07:23:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
After the enormous speedup I achieved with the [FRR containers](/2026/02/netlab-frr-configuration/), I tried to do something similar with the Arista cEOS ones. After all, Arista's pretty open about running its software on standard Linux, so it should be possible to map host-side configuration files into container-side scripts and execute them, right?

There was just one tiny gotcha: all _netlab_-generated EOS configuration files are device configuration snippets that are intended to be submitted via EOS CLI, and I didn't feel like cracking open the [*netmiko* documentation](https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md) (that's another backburner project).

However, Arista cEOS includes this magic command called **FastCli** ;)
<!--more-->
The **FastCli** command can execute any Arista EOS command from **bash**. It can also accept a filename as an argument and pretend there's a user typing commands in that file[^pty]. That looked like a perfect solution:

[^pty]: I never checked whether it creates another PTY to do so.

* Take any Arista EOS configuration snippet
* Prepend it with a **shebang** (`#!/usr/bin/FastCli`)
* [Profit](https://en.wikipedia.org/wiki/Gnomes_(South_Park))

Alas, that failed miserably. Remember the "pretend there's a user typing commands" part? It turns out you have to start from scratch and enter the **configure** mode first. The wrapper I needed to make this idea work[^xbit] turned out to be:

[^xbit]: Along with setting the eXecutable bit on the resulting configuration snippet

```
#!/usr/bin/FastCli
configure terminal
{{ netlab_config_text }}
end
```

After that initial hurdle, it worked. Sort of. Sometimes. The first glitch I uncovered when running the integration tests was the incredible sloppiness Ansible lets through. For example, I had a line in a Jinja2 template that had an extra closing curly bracket:

```
{% if something %}}
```

That line produced a curly bracket on a new line. While that made **FastCli** totally bonkers (no surprise there), it worked with the Ansible **eos.eos_config** module. I observed the same behavior with incorrect comments (starting with "#" instead of "!") and unrecognized commands, such as **ip virtual-router mac-address mlag-peer**.

FWIW, that command generates the following error message *which is [not recognized as an error](https://github.com/ansible-collections/arista.eos/blob/972440cce3e0a120652e730d28bd796513b4e1b0/plugins/terminal/eos.py#L39) by the Arista EOS Ansible module*[^WNP]:

[^WNP]: I'm always wondering why they don't (also) check for the percent sign as the first character in the response, but that's a campfire story for another day.

```
% Unavailable command (not supported on this hardware platform)
```

Cleaning up the configuration templates removed all such quirks[^ESG], but another mystery remained: the configuration process sometimes failed when executing perfectly valid commands.

[^ESG]: I'm ever so grateful I invested so much time into creating integration tests

That mystery turned out to be another timing issue. Try to configure Arista cEOS too soon after the container has started, and you'll experience bizarre errors. Waiting for the SSH server to become available[^SSH] solved that.

[^SSH]: Isn't it weird that we have to wait for the SSH server when we want to use Linux scripts to configure a device? Oh, the wonderful world of networking devices 🤷‍♂️

The solution is part of the _netlab_ release 26.02, but has to be enabled with the **netlab_config_mode** device group variable or node parameter set to **sh**, for example:

```
netlab defaults devices.eos.clab.group_vars.netlab_config_mode=sh
```

Believing in the *eat your own dogfood* BS, I enabled it a few weeks ago, and happily used it ever after. I hope it will work equally well for you.

### Was It Worth It?

**TL&DR:** You bet!

The best I could do on my server was a 20-node Arista cEOS fabric[^BUSY] (four spines, 16 leaves) running OSPF, BGP, and EVPN with VLAN/VXLAN configured on the leaves. This is the gist of the lab topology:

[^BUSY]: That fabric already resulted in a peak 5-second *load average* above 130 when the containers were starting. Not exactly a comfy place to be.

```
module: [ vlan, vxlan, ospf, bgp, evpn ]
bgp.as: 65000

vlans:
  V1:

fabric:
  spines: 4
  leafs: 16
  leaf:
    vlans:
      V1:
  spine:
    bgp.rr: True
```

The lab start times[^PBP] were pretty long[^RTO]:

[^PBP]: See [a previous blog post](/2026/01/netlab-faster-without-ansible#results) for a detailed description of what individual commands do.

[^RTO]: The measured times are not statistically significant. In less-baroque language: I only ran the tests once. The first digit and the order of magnitude are probably not too far off.

| Step | Elapsed time | CPU time |
|------|-------------:|---------:|
| **netlab create** | 2 seconds | 2 seconds |
| **containerlab deploy**[^CD] | ~2 minutes | 1 second |
{ .fmtTable }

[^CD]: Part of **netlab up --no-config**

Now for the fun part: configuring the lab with Linux scripts or Ansible:

| Step | Elapsed time | CPU time |
|------|-------------:|---------:|
| Linux scripts (netlab release 26.02) | 11 seconds | 3 seconds |
| Ansible playbook (netlab release 25.12) | 1 minute 40 seconds | 2 minutes 30 seconds |
{ .fmtTable }

The comparison is light-years away from being fair. While the Linux scripts hammer Arista EOS with configuration commands, the Ansible **eos.eos_config** module executes **show running** followed by a diff and minimal configuration every step of the way (normalize, initial config, VLAN, OSPF, BGP, VXLAN, EVPN).

Nonetheless, it's nice to see how much time you can save when using the best tool for the job ;)
