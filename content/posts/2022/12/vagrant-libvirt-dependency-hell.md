---
title: "vagrant-libvirt Dependency Hell"
date: 2022-12-12 08:30:00
tags: [ netlab ]
netlab_tag: quirks
pre_scroll: True
---
One of the tiny details Open Networking preachers conveniently forget to mention is the tendency of open-source software to use a [gazillion small packages from numerous independent sources](https://xkcd.com/2347/) to get the job done. Vendors selling commercial products (for example, Cumulus Linux) try their best to select the correct version of every package involved in their product; open-source projects could [quickly end in dependency hell](https://xkcd.com/1579/).

*netlab* tries to solve the dependency conundrum with [well-defined installation scripts](https://netlab.tools/netlab/install/). We recommend you start with a brand new Ubuntu server (or VM) and **[follow the four lines of instructions](https://netlab.tools/install/ubuntu-vm/#manual-virtual-machine-provisioning)**[^FI]. In that case, you usually get a working system unless something unexpected breaks behind the scenes, like what we experienced a few days ago.

[^FI]: It's amazing how hard that is for some people ;)
<!--more-->
{{<note>}}Before moving on: I'm not blaming anyone for the SNAFU, and [Darragh Bailey](https://github.com/electrofelix)'s response time has been amazing. These things happen; it's important to be aware of the hidden tax of using open-source software.{{</note>}}

A user strictly following the instructions got a working lab but couldn't bring it down. **[netlab down](https://netlab.tools/netlab/down/)** command consistently crashed somewhere deep in the *vagrant-libvirt* plugin. It was pretty easy to reproduce the behavior[^CS], but ridiculously hard to find a workaround.

[^CS]: That's the beauty of starting with a clean slate and following the instructions

*netlab* was using an ancient version of the *vagrant-libvirt* plugin. I tried a newer version a long while ago, but it didn't work as expected, so I pinned the plugin version in the installation script and moved on. Upgrading the plugin seemed like the obvious first step, only to discover that the newest version of the plugin (0.11.1) didn't work with any VM network adapter but virtio. Not a big deal if you're using Arista or Cumulus VMs, but a total showstopper for Cisco IOS or Nexus OS[^e1k]. The [*vagrant-libvirt* developer](https://github.com/electrofelix) fixed the bug literally hours after I [chimed in on an already-open issue](https://github.com/vagrant-libvirt/vagrant-libvirt/issues/1688), and the fix works. He was also quick to push out a new version of *vagrant-libvirt* plugin (0.11.2); we [plan to use it](https://github.com/ipspace/netlab/issues/667) in the next _netlab_ release.

[^e1k]: They both require emulated ancient Intel Ethernet adapter lovingly known as e1000.

In the meantime, we needed a workaround. After wasting too much time, I discovered that a change in the parameters of a function in the *fog-libvirt* library (used by the *vagrant-libvirt* plugin) caused the crash. That library was dormant for about a year; release 0.10.0 (with a slightly changed API) came out a few days before the *netlab* user tried to build a new VM (explaining why he was the first one reporting the problem). 

To make matters worse:

* The *fog-libvirt* release 0.10.0 does not work with any released version of the *vagrant-libvirt* plugin that handles the e1000 adapter correctly.
* I could find no way to influence the version of a Ruby library used by a Vagrant plugin[^RD] -- `vagrant plugin install` always installs the latest version of the library[^SG].
* Vagrant installs Ruby gems used by its plugins in a weird place.

[^SG]: Another workaround might have been to install the *‌ruby-fog-libvirt* Ubuntu package. Too late for that, I'm not changing a working installation script until the new version of the *vagrant-libvirt* plugin comes out.

Anyway, after a serious wrestling match with `gem`, I found the magic commands (and added them to the installation script):

```
vagrant plugin install vagrant-libvirt --plugin-version=0.4.1
#
# Temporary fix: replace fog-libvirt 0.10.1 with fog-libvirt 0.9.0 until we can upgrade to the latest vagrant-libvirt plugin
#
echo ".. replacing fog-libvirt gem with an older version"
GEMS_DIR=`echo ~/.vagrant.d/gems/*`
GEM_HOME=$GEMS_DIR gem uninstall -aIx fog-libvirt
GEM_HOME=$GEMS_DIR gem install 'fog-libvirt:0.9.0'
```

The modified installation script is included in the latest *networklab* PyPi package (1.4.1.post2), and the installation process yet again results in a working environment.

**Moral of the story:** nothing is as easy as it looks, and if someone claims some IT solution is wonderful, they probably have zero operational experience with it (see also RFC 1925 Rule 4).

[^RD]: Ruby gem has a dependency system similar to pip3, but for whatever reason I always got the latest version of fog-libvirt installed even if I already had a version that satisfied the dependencies listed in the vagrant-libvirt plugin.