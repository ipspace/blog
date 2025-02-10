---
title: "Point-to-Point Links in Virtual Labs"
date: 2025-02-12 07:55:00+0100
tags: [ virtualization, netlab ]
netlab_tag: use
---
In the [previous blog post](/2025/02/virtual-lab-links/), I described the usual mechanisms used to connect virtual machines or containers in a virtual lab, and the drawbacks of using Linux bridges to connect virtual network devices.

In this blog post, we'll see how KVM/QEMU/libvirt/Vagrant use UDP tunnels to connect virtual machines, and how containerlab creates point-to-point vEth links between Linux containers.
<!--more-->
### QEMU UDP Tunnels

I [already mentioned](/2025/02/virtual-lab-links/#qemu) that [QEMU](https://en.wikipedia.org/wiki/QEMU) (the program that does all the real work when you run KVM virtual machines on a Linux server) emulates a virtual NIC for its VM guest and shuffles packets between the input/output queues of the virtual NIC and a Linux tap interface connected to a Linux bridge.

{{<figure src="/2025/02/qemu-tap.png" caption="QEMU forwarding packets between VM NIC and Linux tap interface">}}

However, exchanging packets between VM NICs and Linux interfaces is not required. QEMU could use any other infrastructure to transport VM packets, including TCP and UDP sockets. It can even use multicast destination addresses on UDP sockets to emulate a multi-access Ethernet subnet[^AQD].

{{<figure src="/2025/02/qemu-udp.png" caption="QEMU forwarding packets between VM NIC and UDP socket">}}

[^AQD]: According to cryptic QEMU documentation. Not tested.

Figuring out how to get from Vagrant to QEMU UDP tunnels requires a recursive application of RFC Rule 6a:

* Vagrant passes whatever is specified in Vagrantfile **network** parameter to vagrant-libvirt plugin.
* vagrant-libvirt plugin creates [libvirt XML definition](https://libvirt.org/formatdomain.html#udp-unicast-tunnel) for the VM NIC[^DIP]
* libvirt uses the interface XML definition to create CLI arguments for the **qemu** command.
* The ultimate source of truth is found in the arcane [QEMU invocation document](https://www.qemu.org/docs/master/system/invocation.html) hidden deep in the bowels of the [Network Options](https://www.qemu.org/docs/master/system/invocation.html#hxtool-5) section.

[^DIP]: Libvirt developers further try to confuse you by calling the parameter specifying the destination IP address **source** and the parameter specifying the source IP address **local**.

The Vagrantfile definitions specifying a UDP tunnel between two virtual machines are also a masterpiece of obfuscation:

{{<cc>}}Creating a Vagrantfile point-to-point link between two virtual machines{{</cc>}}
```
    x1.vm.network :private_network,
                  :libvirt__tunnel_type => "udp",
                  :libvirt__tunnel_local_ip => "127.1.1.3",
                  :libvirt__tunnel_local_port => "10001",
                  :libvirt__tunnel_ip => "127.1.1.1",
                  :libvirt__tunnel_port => "10002",
                  :libvirt__iface_name => "vgif_x1_1",
                  auto_config: false
...
    s1.vm.network :private_network,
                  :libvirt__tunnel_type => "udp",
                  :libvirt__tunnel_local_ip => "127.1.1.1",
                  :libvirt__tunnel_local_port => "10002",
                  :libvirt__tunnel_ip => "127.1.1.3",
                  :libvirt__tunnel_port => "10001",
                  :libvirt__iface_name => "vgif_s1_2",
                  auto_config: false
```

Fortunately, we have several tools (including [netlab](https://netlab.tools/)) to create Vagrantfile from a higher-level specification (the [original netlab use case](/2020/12/build-labs-netsim-tools/)).

Finally, it's worth mentioning an unpleasant quirk of the UDP tunnels. They don't use Linux interfaces, making it impossible to do simple packet capture on VM-to-VM links. QEMU does provide a traffic capture CLI command[^CCC] that saves packets into a file, and there might be a Wireshark plugin out there that strips the UDP header automatically (or you could create custom decoding rules). _netlab_ uses a workaround: it politely tells you how to [replace a UDP tunnel with a Linux bridge](https://netlab.tools/labs/libvirt/#libvirt-capture).

[^CCC]: Good luck enabling it through a half-dozen layers of abstraction ;)

### Point-to-Point Container Links

Docker [implements container networking](/2025/02/virtual-lab-links/#docker) with vEth pairs, connecting one end of the virtual cable to a Linux bridge and placing the other end of the cable into a container network namespace.

{{<figure src="/2025/02/veth-bridge.png" caption="Containers connected to a Linux bridge">}}

When you ask containerlab to create a point-to-point link between two containers, it bypasses Docker networking, creates the vEth pair, and places the ends of the virtual cable *directly into two container network namespaces*.

{{<figure src="/2025/02/containerlab-p2p.png" caption="Direct point-to-point link between two containers">}}

That's a perfect solution from the device connectivity perspective. The containers receive whatever their peer sends them, allowing you to implement whatever networking constructs, including custom STP or MLAG solutions. Even better, the configuration is trivial. This is all you have to specify in a containerlab topology file to create a link between two containers:

```
  links:
  - endpoints:
    - "s1:eth1"
    - "s2:eth1"
```

There's just a minor inconvenience: Docker knows nothing about those point-to-point links. If a container crashes, the vEth pair is lost and cannot be recreated when Docker restarts the container. You can recreate the links with the **[containerlab tools veth create](https://containerlab.dev/cmd/tools/veth/create/)**, but it's cumbersome, and you never know how well network devices respond to suddenly-disappearing interfaces.

Finally, as I mentioned packet capture woes of UDP tunnels: **tcpdump** works on point-to-point vEth pairs *if you start it within the container network namespace* with the **ip netns exec** command. [*netlab* provides a convenient wrapper around that command](https://netlab.tools/netlab/capture/), and the [containerlab packet capture documentation](https://containerlab.dev/manual/wireshark/) is excellent [^RD].

[^RD]: Roman Dodin knows how necessary good documentation is. One could only wish that other open-source developers would share that mindset.

### Worth the Effort?

Point-to-point UDP tunnels or vEth pairs are a much better option than Linux bridges if you want to build a realistic network in a virtual lab. They transparently pass traffic between network devices, allowing you to test layer-2 control-plane protocols like STP or LACP and evading the stupidities like the [default dropping of bridged IPv6 traffic](https://github.com/ipspace/netlab/issues/1669#issuecomment-2585778785).

{{<next-in-series page="/posts/2025/02/no-such-post">}}**Coming up next:** stub interfaces in virtual labs{{</next-in-series>}}