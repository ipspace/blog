---
date: 2022-05-05 06:57:00+00:00
netlab_tag: guidelines
tags:
- netlab
title: Configure Hardware Labs with netlab
---
*[netlab](https://netlab.tools/)* started as a [simple tool to create virtual lab topologies](https://blog.ipspace.net/2020/12/build-labs-netsim-tools.html) (I hated creating *Vagrantfiles* describing complex topologies), but when it morphed into an ever-growing "_configure all the boring stuff in your lab from a high-level description_"  thingie, it gave creative networking engineers an interesting idea: could we use this tool to do all the stuff we always hated doing in our physical labs?

My answer was always "_of course, please feel free to submit a PR_", and [Stefano Sasso](http://stefano.dscnet.org/) did just that: he implemented [_external_  orchestration provider](https://netlab.tools/providers/) that allows you to use *netlab* to configure IPv4, IPv6, VLANs, VRFs, VXLAN, LLDP, BFD, OSPFv2, OSPFv3, EIGRP, IS-IS, BGP, MPLS, BGP-LU, L3VPN (VPNv4 + VPNv6), EVPN, SR-MPLS, or SRv6 on [supported hardware devices](https://netlab.tools/platforms/).
<!--more-->
All you need to do to get that giant bag of goodies is to [install netlab](https://netlab.tools/install/) and Ansible, and describe the topology (devices and links) of your hardware lab.

Start with the devices:

* For every device in your lab, add a [node](https://netlab.tools/nodes/) to the **nodes** dictionary in your [lab topology file](https://netlab.tools/topology-overview/).
* Use **device** attribute to set the [device type](https://netlab.tools/platforms/).
* Set **mgmt.ipv4** or **mgmt.ipv6** to the management IP address. *netlab* assumes you're using out-of-band management interfaces, preferably in a separate VRF.
* To make your life easier, use the *netlab* default login credentials[^CRED] on your hardware devices. If you can't do that, set corresponding Ansible inventory variables (**ansible_user**, **ansible_ssh_pass** and **ansible_become_password**) in the node definition.

Example:

```
nodes:
  leaf_1:
    device: eos
    mgmt.ipv4: 10.42.42.1
    ansible_ssh_pass: SomethingElse
```

[^CRED]: Username *vagrant*, password *vagrant* on most devices.  Junos is a bit picky, so we had to use *Vagrant* as the password. Use *admin*/*admin* on Fortinet, Nokia SR Linux, Nokia SR OS, and Mikrotik RouterOS.

Next, describe the links between your hardware devices. For every link, add an entry to the **links** list. Use the **ifname** parameter on individual node-to-link connections to specify the actual interface name, for example:

```
links:
- leaf_1:
    ifname: Ethernet1/3
  spine_1:
    ifname: Ethernet2/1
```

Finally, don't forget to specify you're using the *external* provider:

```
provider: external
```

And that's it. Execute **netlab up** and you'll get default IP addressing configured in your hardware lab.

Next step(s): explore a dozen [configuration modules](https://netlab.tools/module-reference/) to prepare your lab for whatever tests you'd like to perform.

Experiencing problems? We have a [channel](https://networktocode.slack.com/archives/C022DQHK8BH) in [NetworkToCode Slack team](https://networktocode.herokuapp.com/), and if you're pretty sure you're dealing with a bug, please [open a GitHub issue](https://github.com/ipspace/netlab/issues).

Last but not least: wouldn't it be great to have a tool that would collect operational device data (software version, LLDP neighbors, interface state) from your hardware lab and create the lab topology for you? Why don't you create something along these lines and submit a PR?
