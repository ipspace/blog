---
title: "Weird: vJunos Evolved 23.2R1.5 Declines DHCP Address"
date: 2023-10-30 06:44:00
tags: [ DHCP ]
pre_scroll: True
---
It's time for a Halloween story: imagine the scary scenario in which a DHCP client asks for an address, gets it, and then immediately declines it. That's what I've been experiencing with vJunos Evolved release 23.2R1.15.

{{<long-quote>}}
Before someone gets the wrong message: I'm not criticizing Juniper or vJunos.

* Juniper did a great job releasing a no-hassles-to-download virtual appliance.
* DHCP assignment of management IPv4 address worked with vJunos Evolved release 23.1R1.8
* There were reports that the DHCP assignment process in vJunos Evolved 23.1R1.8 was not reliable, but it worked for me so far, so I'm good to go as long as I can run the older release.
* I might get to love vJunos Evolved. Boot- and configuration times are very reasonable.

However, it looks like something broke in vJunos release 23.2, and it would be nice to figure out what the workaround might be.
{{</long-quote>}}
<!--more-->
{{<note update>}}
### Updates (2023-12-05)

* The behavior was caused by a DHCP client bug in vJunos release 23.2R1.5
* That bug is fixed in release 23.2R1-S1. It took 3.5 months to get a fixed version, but that's a different story.
* Release 23.2R1-S1 totally changed VM connectivity requirements (the VM no longer needs external PFE and RPIO links), making the new VM connectivity settings incompatible with the old ones.
* [_netlab_ release 1.7](https://netlab.tools/release/1.7/) supports [vJunos release 23.2R1-S1](https://netlab.tools/release/1.7/#release-1-7-0-breaking). If you want to use older vJunos releases, use _netlab_ release 1.6.4.
{{</note>}}
It started innocently enough: someone complained that they cannot [build vPTX Vagrant box](https://netlab.tools/labs/vptx/) with **[netlab](https://netlab.tools/)**. It quickly turned out to be a case of *thou shalt be root*, and the fix was trivial: add a `sudo` command in the right place. Obviously I wanted to check whether the fix worked, so I:

* Downloaded the latest [vJunos Evolved QCOW image](https://support.juniper.net/support/downloads/?p=vjunos-evolved). Major kudos to Juniper -- downloading a virtual appliance has never been easier. They even provide a direct URL I could use to download the QCOW image straight to my remote server.
* Built the vPTX box. No errors, apart from the VM not getting an IP address on the management interface (`re0:mgmt-0.0`). Well, I decided to ignore that, shut down the VM, and **netlab** completed the box creation process and installed the box. I should have stopped right there and declared victory, but I made a fatal mistake and took the last step...
* I tried to start the vJunos box with **netlab** and started feeling like Alice in wonderland (and not in the good sense).

Whatever I tried, the vJunos VM did not get an IP address from the *libvirt* DHCP server. Finally I gave up and started **tcpdump** and that's when the things took an exquisitely weird turn. This is the DHCP exchange between the VM and the *libvirt* DHCP server:

```
13:52:19.155730 IP (tos 0x10, ttl 128, id 0, offset 0, flags [none], proto UDP (17), length 328)
    0.0.0.0.68 > 255.255.255.255.67: [udp sum ok] BOOTP/DHCP, Request from 08:4f:a9:00:00:01, length 300, xid 0x369f0b0f, Flags [Broadcast] (0x8000)
	  Client-Ethernet-Address 08:4f:a9:00:00:01
	  Vendor-rfc1048 Extensions
	    Magic Cookie 0x63825363
	    DHCP-Message (53), length 1: Discover
	    Hostname (12), length 4: "vptx"
	    Parameter-Request (55), length 9:
	      Subnet-Mask (1), BR (28), Time-Zone (2), Default-Gateway (3)
	      Domain-Name (15), Domain-Name-Server (6), Unknown (119), Hostname (12)
	      MTU (26)
13:52:19.156075 IP (tos 0xc0, ttl 64, id 49731, offset 0, flags [none], proto UDP (17), length 328)
    192.168.42.1.67 > 255.255.255.255.68: [udp sum ok] BOOTP/DHCP, Reply, length 300, xid 0x369f0b0f, Flags [Broadcast] (0x8000)
	  Your-IP 192.168.42.101
	  Server-IP 192.168.42.1
	  Client-Ethernet-Address 08:4f:a9:00:00:01
	  Vendor-rfc1048 Extensions
	    Magic Cookie 0x63825363
	    DHCP-Message (53), length 1: Offer
	    Server-ID (54), length 4: 192.168.42.1
	    Lease-Time (51), length 4: 3600
	    RN (58), length 4: 1800
	    RB (59), length 4: 3150
	    Subnet-Mask (1), length 4: 255.255.255.0
	    BR (28), length 4: 192.168.42.255
	    Default-Gateway (3), length 4: 192.168.42.1
	    Domain-Name-Server (6), length 4: 192.168.42.1
13:52:19.156336 IP (tos 0x10, ttl 128, id 0, offset 0, flags [none], proto UDP (17), length 328)
    0.0.0.0.68 > 255.255.255.255.67: [udp sum ok] BOOTP/DHCP, Request from 08:4f:a9:00:00:01, length 300, xid 0x369f0b0f, Flags [Broadcast] (0x8000)
	  Client-Ethernet-Address 08:4f:a9:00:00:01
	  Vendor-rfc1048 Extensions
	    Magic Cookie 0x63825363
	    DHCP-Message (53), length 1: Request
	    Server-ID (54), length 4: 192.168.42.1
	    Requested-IP (50), length 4: 192.168.42.101
	    Hostname (12), length 4: "vptx"
	    Parameter-Request (55), length 9:
	      Subnet-Mask (1), BR (28), Time-Zone (2), Default-Gateway (3)
	      Domain-Name (15), Domain-Name-Server (6), Unknown (119), Hostname (12)
	      MTU (26)
13:52:19.156563 IP (tos 0xc0, ttl 64, id 49732, offset 0, flags [none], proto UDP (17), length 328)
    192.168.42.1.67 > 255.255.255.255.68: [udp sum ok] BOOTP/DHCP, Reply, length 300, xid 0x369f0b0f, Flags [Broadcast] (0x8000)
	  Your-IP 192.168.42.101
	  Server-IP 192.168.42.1
	  Client-Ethernet-Address 08:4f:a9:00:00:01
	  Vendor-rfc1048 Extensions
	    Magic Cookie 0x63825363
	    DHCP-Message (53), length 1: ACK
	    Server-ID (54), length 4: 192.168.42.1
	    Lease-Time (51), length 4: 3600
	    RN (58), length 4: 1800
	    RB (59), length 4: 3150
	    Subnet-Mask (1), length 4: 255.255.255.0
	    BR (28), length 4: 192.168.42.255
	    Default-Gateway (3), length 4: 192.168.42.1
	    Domain-Name-Server (6), length 4: 192.168.42.1
	    Hostname (12), length 4: "vptx"
13:52:19.175004 IP (tos 0x10, ttl 128, id 0, offset 0, flags [none], proto UDP (17), length 328)
    0.0.0.0.68 > 255.255.255.255.67: [udp sum ok] BOOTP/DHCP, Request from 08:4f:a9:00:00:01, length 300, xid 0x369f0b0f, Flags [Broadcast] (0x8000)
	  Client-Ethernet-Address 08:4f:a9:00:00:01
	  Vendor-rfc1048 Extensions
	    Magic Cookie 0x63825363
	    DHCP-Message (53), length 1: Decline
	    Server-ID (54), length 4: 192.168.42.1
	    Requested-IP (50), length 4: 192.168.42.101
	    Hostname (12), length 4: "vptx"
```

As you can see:

* The VM asks where the DHCP server might be (DISCOVER)
* The DHCP server responds offering a bunch of parameters including the VM IP address
* The VM accepts the offer and wants to confirm the assigned IP address with the REQUEST message
* The DHCP server acknowledges the VM IP address assignment and sends a bunch of other parameters
* After ~20 msec the vJunos VM declines the IP address.
* There were no other packets exchanged on the Linux bridge between the DHCP ACK and DHCP DECLINE message, so it's not like the VM would detect someone else using its IP address.

DHCP client logging on vJunos wasn't exactly helpful (the DHCP client logs nothing else but one line per DHCP packet), and the **show dhcp client bindings** Junos command displayed nothing at all.

I got no usable information with Google search (I felt almost like [this guy](https://xkcd.com/979/)). It could be that:

* the vJunos DHCP client doesn't like a parameter the DHCP server supplies (**dnsmasq** does supply a few parameters vJunos did not ask for), or
* the vJunos DHCP client hates that the DHCP server does not supply all parameters it asked for, or
* something completely different.

I could try tweaking the **dnsmasq** configuration (*libvirt* release 5.6.0 can pass network parameters to **dnsmasq**), but it would be awesome to know where to start.

Useful hints I could use to unravel this mystery and hopefully get the latest release of vJunos to work with netlab are thus highly appreciated:

* the initial device configuration is [here](https://github.com/ipspace/netlab/blob/e0691dcbb75a5cd890707bff4d8893094a35caad/netsim/install/libvirt/vptx/juniper.conf)
* the DHCP packet trace is [here](/2023/10/vptx-dhcp.pcap)
* the following printout is the Vagrantfile **netlab** generates[^DGS] -- it's out best attempt to translate the KVM XML domain definition Juniper provides into a Vagrant VM definition, and it works with vJunos Evolved 23.1R1.8.

[^DGS]: Don't get me started on the need to have four VM interfaces just so the VM could talk to itself, or the need to have very specific hardware manufacturer hardcoded in VM BIOS.

```
VAGRANT_COMMAND = ARGV[0]

Vagrant.configure("2") do |config|
  config.vm.provider :libvirt do |libvirt|
    libvirt.management_network_address = "192.168.42.0/24"
    libvirt.default_prefix = "vPTX_"
  end
  config.vm.define "r" do |r|
    r.vm.provider :libvirt do |domain|
      domain.management_network_mac = "08:4f:a9:00:00:01"
      domain.qemu_use_session = false
    end
    r.vm.box = "juniper/vptx"
    guest_name = "r"
    r.vm.guest = :tinycore
    r.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    r.ssh.insert_key = false

    r.vm.boot_timeout = 6000

    r.vm.provider :libvirt do |domain|
      domain.cpus = 4
      domain.memory = 8192
      domain.disk_bus = "virtio"
      domain.driver = "kvm"
      domain.nic_model_type = "virtio"
      domain.graphics_type = "none"
      domain.nested = true
      domain.cpu_mode = "custom"
      domain.cpu_model = "qemu64"
      domain.cpu_feature :name => 'vmx', :policy => 'require'
      domain.sysinfo = {
        "bios": {
          "vendor": "Bochs",
          "version": "Bochs"
        },
        "system": {
            "manufacturer": "Bochs",
            "product": "Bochs",
            "serial": "chassis_no=0:slot=0:type=1:assembly_id=0x0D20:platform=251:master=0:channelized=no"
        },
        "chassis": {
          "manufacturer": "Bochs"
        }
      }

    end

    ## add 4 network interfaces required for internal communication:
    ## - vptx_PFE_LINK
    ## - vptx_RPIO_LINK
    ## - vptx_RPIO_LINK
    ## - vptx_PFE_LINK

    r.vm.network :private_network,
                  :libvirt__network_name => "r_pfe",
                  :libvirt__forward_mode => "veryisolated",
                  :libvirt__dhcp_enabled => false,
                  :libvirt__iface_name => "r_pfe_1",
                  :libvirt__mtu => 9600,
                  :auto_config => false
    r.vm.network :private_network,
                  :libvirt__network_name => "r_rpio",
                  :libvirt__forward_mode => "veryisolated",
                  :libvirt__dhcp_enabled => false,
                  :libvirt__iface_name => "r_rpio_1",
                  :libvirt__mtu => 9600,
                  :auto_config => false
    r.vm.network :private_network,
                  :libvirt__network_name => "r_rpio",
                  :libvirt__forward_mode => "veryisolated",
                  :libvirt__dhcp_enabled => false,
                  :libvirt__iface_name => "r_rpio_2",
                  :libvirt__mtu => 9600,
                  :auto_config => false
    r.vm.network :private_network,
                  :libvirt__network_name => "r_pfe",
                  :libvirt__forward_mode => "veryisolated",
                  :libvirt__dhcp_enabled => false,
                  :libvirt__iface_name => "r_pfe_2",
                  :libvirt__mtu => 9600,
                  :auto_config => false
    r.vm.provider :libvirt do |domain|
    end

    r.vm.network :private_network,

                  :libvirt__network_name => "vPTX_1",
                  :libvirt__forward_mode => "veryisolated",
                  :libvirt__dhcp_enabled => false,
                  :libvirt__iface_name => "vgif_r_0",
                  :autostart => true,
                  :auto_config => false


  end
end
```