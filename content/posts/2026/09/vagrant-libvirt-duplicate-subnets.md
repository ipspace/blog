---
title: "How vagrant-libvirt Plugin Deals with Duplicate Subnets"
date: 2026-09-16 08:27:00+0200
tags: [ virtualization ]
---
**TL&DR:** Badly. The *vagrant-libvirt* plugin mysteriously crashes when an existing virtual network (with a different libvirt name) uses the same IP subnet as the desired management network.

**Background:** *netlab* is using the *[vagrant-libvirt](https://vagrant-libvirt.github.io/vagrant-libvirt/)* plugin to manage libvirt/KVM virtual machines with [Vagrant](https://developer.hashicorp.com/vagrant). As I already have that infrastructure, I use it to start standalone virtual machines (usually to test various Ubuntu releases) on my Linux server. Things work great... until they don't.

Here's how I managed to waste half a day chasing imaginary gremlins caused by a simple error.
<!--more-->
The *vagrant-libvirt* plugin usually creates all the virtual networks it needs. For example, if you define the management network, the plugin creates it before the VMs start and destroys it once they stop.

The definition of the [management network](/2026/09/network-lab-management-ip/) could be as simple as this:

{{<printout caption="The management network definition in a Vagrantfile">}}
Vagrant.configure("2") do |config|
  config.vm.provider "libvirt" do |lv|
    lv.management_network_address = "192.168.42.0/24"
    lv.management_network_name = "netlab_mgmt"
  end
end
{{</printout>}}

Imagine my surprise when I copied an existing Vagrantfile, modified it a bit[^ABIT], and was faced with a crashing **vagrant up** command claiming the virtual network does not exist.

[^ABIT]: I changed the `management_network_name`, but also a bunch of other things, which made the "what changed" troubleshooting that much more fun.

After trying everything and everything else (apart from fixing my trivial mistake, of course), I finally decided to start Vagrant with the `--debug` option and capture the output in a file. Even that refused to work; for some incomprehensible reason, Vagrant prints *debugging* output to *stderr* (I thought *err* stood for *error*, but what do I know). Well, that was easy to fix, and once I had all the information in one place, the mystery quickly disappeared (as did too many hours of my life):

* The *vagrant-libvirt* plugin collects the management network information from the virtual machine configurations.
* It checks existing virtual networks based on their name *and IP subnet*
* If it finds an existing virtual network *with a subnet matching the* `management_network_address` *parameter*, it decides it does not have to create a new network *but never changes the expected network name or warns you that there's a mismatch in network name*
* When a VM is started attached to the virtual network that should have been created (but wasn't because another network had the same IP subnet), you get a horrendously long crash dump.

Here's the relevant part of the debugging printouts. Notice the difference between the network that should have been created (`ms_mgmt`) and the one that was supposedly created (`netlab_mgmt`):

```
 INFO create_networks: Using ms_mgmt at 192.168.42.0/24 as the management network nat is the mode
DEBUG create_networks: In config found network type forwarded_port options {:guest=>22, :host=>2222, :host_ip=>"127.0.0.1", :id=>"ssh", :auto_correct=>true, :protocol=>"tcp"}
DEBUG create_networks: Searching for network with options {:iface_type=>:private_network, :model_type=>"virtio", :network_name=>"ms_mgmt", :ip=>"192.168.42.0", :netmask=>"255.255.255.0", :dhcp_enabled=>true, :forward_mode=>"nat", :guest_ipv6=>"yes", :autostart=>true, :bus=>nil, :slot=>nil, :driver_iommu=>false, :iface_name=>nil, :mac=>"52:54:00:aa:bb:02"}
DEBUG create_networks: looking up network with ip == 192.168.42.0
DEBUG create_networks: Checking that network name does not clash with ip
 INFO create_networks: Saving information about created network netlab_mgmt, UUID=ad277be9-2b63-4090-9303-d72e0f06a759 to file /home/pipi/vm/multiserver/.vagrant/machines/s2/libvirt/created_networks.
...
 INFO interface: detail: error: failed to get network 'ms_mgmt'
error: Network not found: no network with matching name 'ms_mgmt'

 INFO interface: detail:     s2: error: failed to get network 'ms_mgmt'
    s2: error: Network not found: no network with matching name 'ms_mgmt'
    s2:
```
Modifying the `management_network_address` in the modified Vagrantfile solved the problem.

Finally, you might be wondering where the existing virtual network with the overlapping IP subnet came from. Even though Vagrant deletes virtual networks when you stop the VMs, they can remain defined across server reboots.

**Lesson learned:** whenever you change the *vagrant-libvirt* network names, make sure you also change their IP subnets. It's not like you'll run out of the RFC 1918 address space inside your Linux server.
