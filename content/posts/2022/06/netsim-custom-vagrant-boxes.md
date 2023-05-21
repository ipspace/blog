---
date: 2022-06-09 06:10:00+00:00
netlab_tag: extend
pre_scroll: true
tags:
- netlab
title: Using Custom Vagrant Boxes with netlab
---
A friend of mine started using Vagrant with libvirt years ago (it was his enthusiasm that piqued my interest in this particular setup, eventually resulting in *netlab*). Not surprisingly, he's built Vagrant boxes for any device he ever encountered, created quite a collection that way, and would like to use them with *netlab*.

While I didn't think about this particular use case when programming the *netlab* virtualization provider interface, I decided very early on that:

* Everything worth changing will be specified in the system defaults
* You will be able to change system defaults in topology file or user defaults.
<!--more-->
### Changing Vagrant Box or Container Name

Parameters describing individual devices are grouped under **devices** dictionary in [system parameters](https://github.com/ipspace/netlab/blob/dev/netsim/topology-defaults.yml). Each device is described as another dictionary, and that dictionary contains image names (box- or container names) for every virtualization provider supported by that device, for example:

```
devices:
  eos:
    virtualbox:
      image: arista/veos
    clab:
      image: ceos:4.26.4M
    libvirt:
      image: arista/veos
```

To change a Vagrant box used by a device type, you have to change one (or all) of these settings.

### Changing System Defaults in Lab Topology

You can change system defaults in your lab topology. Because you're changing a default, you have to make that change within the **defaults** dictionary, for example:

{{<cc>}}Changing Arista cEOS container image in lab topology{{</cc>}}
```
defaults:
  devices:
    eos:
      clab:
        image: ceos:4.27.0F
```

You probably hate using a ruler to figure out proper YAML indentation as much as I do, so I added a neat trick to *netlab* YAML files -- you can use dotted name syntax (similar to how sane programming languages deal with objects):

{{<cc>}}Changing Arista cEOS container image in lab topology -- dotted syntax{{</cc>}}
```
defaults.devices.eos.clab.image: ceos:4.27.0F
```

Each dotted name is expanded into a dictionary, and that dictionary is [merged](https://netlab.tools/defaults/#defaults-deep-merging) with the lab topology ([Box package](https://github.com/cdgriffith/Box) does a wonderful job doing that), allowing you do use the same path in multiple settings:

{{<cc>}}Changing multiple Arista images{{</cc>}}
```
defaults.devices.eos.clab.image: ceos:4.27.0F
defaults.devices.eos.libvirt.image: arista/veos:4.27.0F
```

You can also make your future life miserable and do something like this:

{{<cc>}}Just because you could doesn't mean that you should{{</cc>}}
```
defaults.devices.eos:
  clab.image: ceos:4.27.0F
  libvirt.image: arista/veos:4.27.0F
```

### Changing System Defaults in User Defaults File(s)

If you want to use the same changed defaults for multiple lab topologies (which is what my friend would want to do), you can store the changed defaults in `topology-defaults.yml` (applies to all topologies in the same directory) or `~/.netlab.yml` (applies to everything the current user does).

As you're changing settings within a *defaults* file, you MUST NOT use the **defaults** prefix. For example: to change Arista images for the current user, use the following settings in `~/.netlab.yml`:

{{<cc>}}Changing Arista images in user defaults{{</cc>}}
```
devices.eos.clab.image: ceos:4.27.0F
devices.eos.libvirt.image: arista/veos:4.27.0F
```

### Changing Usernames and Passwords

I try to use *vagrant/vagrant* as username/password combination in all Vagrant boxes I'm building (Junos is the only exception as it enforces password complexity rules we all love so much). Your boxes might have different usernames.

Not a problem: you have to change the **group_vars** device settings -- a dictionary containing Ansible variables for that device type, including authentication variables `ansible_user` and `ansible_ssh_pass`. These are the default settings for Arista EOS:

{{<cc>}}Ansible variables for Arista devices{{</cc>}}
```
devices:
  eos:
    group_vars:
      ansible_user: vagrant
      ansible_ssh_pass: vagrant
      ansible_network_os: eos
      ansible_connection: network_cli
```

Arista is a particularly tough nut: cEOS uses different default username than vEOS, so we had to add support for provider-specific group variables. Even worse, vEOS boxes I build use privileged user *vagrant*, cEOS uses non-privileged user *admin*, so we have to set `ansible_become` as well.

{{<cc>}}Usernames and passwords for Arista Vagrant boxes and containers{{</cc>}}
```
devices:
  eos:
    group_vars:
      ansible_user: vagrant
      ansible_ssh_pass: vagrant
    clab:
      group_vars:
        ansible_user: admin
        ansible_ssh_pass: admin
        ansible_become: yes
        ansible_become_method: enable    
```

Now that you know how to change system defaults, it shouldn't be too hard to change username for *libvirt* Arista vEOS box to *foobar*:

{{<cc>}}Changing default username for Arista vEOS *libvirt* box{{</cc>}}
```
devices.eos.libvirt.group_vars.ansible_user: foobar
```

### Changing Vagrantfile

The final hurdle my friend was facing: he didn't like the way *netlab* sets up NX-OS boxes in generated Vagrantfile:

{{<cc>}}*libvirt* Vagrantfile template for NX-OS boxes{{</cc>}}
```
    {{ name }}.vm.synced_folder ".", "/vagrant", disabled: true
    {{ name }}.ssh.insert_key = false
    {{ name }}.ssh.shell = "run bash"
    {{ name }}.vm.boot_timeout = 360
    {{ name }}.vm.guest = :freebsd

    {{ name }}.vm.provider :libvirt do |domain|
      domain.cpus = 2
      domain.features = ['acpi']
      domain.loader = "/usr/share/OVMF/OVMF_CODE.fd"
      domain.memory = 6144
      domain.disk_bus = "sata"
      domain.disk_device = "sda"
      domain.disk_driver :cache => "none"
      domain.nic_model_type = "e1000"
      domain.graphics_type = "none"
      domain.driver = "kvm"
      {% if "amd" in defaults.processor|lower %}
      domain.cpu_mode = "custom"
      {% endif %}
    end
```

*netlab* release 1.2.4 adds support for user Jinja2 templates -- all *netlab* code using Jinja2 templates[^NOANS] looks for templates in current directory, `~/.netlab` directory, and Python package[^SPD]. Templates used to create Vagrantfile are within the provider-specific subdirectory (`libvirt` or `virtualbox`).

[^NOANS]: But not the Ansible playbooks used by **netlab up** or **netlab initial**

To change the template used to create Vagrantfile configuration for a Nexus OS *libvirt* box:

* If you want to use the changed template for a specific topology, create `libvirt` directory within the directory the with lab topology.
* If you want to use the changed template for all labs, create `libvirt` directory within the `~/.netlab` directory.
* Find the original template in [*netlab* sources](https://github.com/ipspace/netlab/tree/dev/netsim/templates/provider) (example: [*libvirt* Nexus OS template](https://github.com/ipspace/netlab/blob/dev/netsim/templates/provider/libvirt/nxos-domain.j2)).
* Copy that template **with the same file name** into `libvirt` directory and modify it as needed.
* Enjoy using *netlab* with your custom Vagrant boxes.

[^SPD]: To see the template search path, run `netlab create --debug` and look for `TEMPLATE PATH` messages.