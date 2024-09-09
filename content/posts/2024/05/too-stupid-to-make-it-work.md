---
title: "Famous Last Words: I'm Too Stupid for That"
date: 2024-05-06 08:25:00+0200
lastmod: 2024-09-09 16:26:00+02:00
tags: [ virtualization ]
---
Some networking vendors realized that one way to gain mindshare is to make their network operating systems available as free-to-download containers or virtual machines. That's the right way to go; I love their efforts and point out who went down that path whenever possible[^AOT] (as well as others like Cisco who try to make our lives miserable).

[^AOT]: As of today: Cumulus Linux, Dell OS10, Dell Sonic, FRR, Juniper vPTX, Mikrotik RouterOS7, Nokia SR Linux, and Vyos. Registration (but nothing more) is required for Arista vEOS/cEOS, Aruba CX, and Cisco Nexus OS. The virtual machines might not support all control- or data-plane features you're interested in. As always, YMMV.

However, those virtual machines better work out of the box, or you'll get frustrated engineers who will give up and never touch your warez again, or as someone said in a LinkedIn comment to my blog post describing how [Junos vPTX consistently rejects its DHCP-assigned IP address](/2023/10/vjunos-declines-dhcp-address/): "_If I had encountered an issue like this before seeing Ivan’s post, I would have definitely concluded that I am doing it wrong._"[^CB]
<!--more-->
[^CB]: Paraphrased as the *I'm too stupid for that* clickbait.

The Junos vPTX DHCP FUBAR was a [simple mistake](/2023/10/vjunos-declines-dhcp-address/#1974) fixed in the next software release (vPTX works flawlessly with _netlab_ now), but it was impossible to diagnose or fix from the outside[^MT3M]. Also, it proved (to me) that the vPTX target audience is not people who run virtual machines in environments where the management IP address allocation is done via DHCP. I can't imagine a scenario where someone doing the most rudimentary tests with something like *vagrant-libvirt* (or any other cloud environment) would miss that problem.

[^MT3M]: Taking more than three months to release a fix is a different story. Einstein was right; time really is relative.

Unfortunately, it's not just Juniper[^NWTBP]. I built a Dell OS10 Vagrant box a few days ago, and its SSH server fails to start in approximately 30% of the cases, making it totally useless in any sort of CI/CD pipeline or any environment more complex than a virtual console cable attached to the virtual serial port. Here are sample _netlab_ integration test results for Dell OS10; the **crashed** entries are caused by a failed SSH server (Vagrant couldn't connect to the VM)[^MTU].

{{<figure src="/2024/05/dell-os10-results.jpg">}}

[^MTU]: Most of the *validation failed* results were caused by OSPF failing to start due to MTU mismatches. You can find the latest test results [here](https://tests.netlab.tools/_html/dellos10-libvirt).

Based on what's packed with the Dell OS10 image[^TAT], their target audience seems to be GNS3 users point-and-clicking their way around. Who am I to question their business decisions? However, it might be worth pointing out that an unreliable SSH server might scare away people believing in programmability and automation. Do they really want to compete with Cisco and Arista on who has a better lab GUI?

To make matters worse, someone [mentioned the exact same problem](https://www.dell.com/community/en/conversations/networking-general/s6010-gns3-ssh-not-listening-on-management-port/647f9fa5f4ccf8a8de4839c0) on Dell community forum *in 2022*, and all he got back was effectively "_we can't help you as you're not a paying customer_" Seriously? Is that the way to gain mindshare?

[^NWTBP]: Or I wouldn't be writing this blog post. Let bygones be bygones. It did make for a good intro, though.

[^TAT]: I appreciate Dell releasing the OS10 image with no strings attached. If only it would work reliably.

But wait, it gets better. I also tried out the Dell Enterprise Sonic image. Its SSH server works (no surprise; it runs on mostly unmodified Linux), but the data plane doesn't[^SMD]. I don't think that anyone trying to connect that VM to two Linux endpoints within a GNS3 system[^GA] would get it to work without fixing the underlying problem, which (from my limited perspective) might indicate that nobody involved in the Dell Sonic release process ever tried to do that[^PFB].

[^SMD]: Sonic uses a weird mapping between physical ports (Linux Ethernet interfaces in the VM scenario) and Sonic data plane interfaces. That mapping is defined in a platform-specific configuration file, and the configuration file for a KVM VM is missing from the Dell Enterprise Sonic image. There's no way that thing could forward packets between Ethernet interfaces when running in a VM.

[^GA]: Yes, the Sonic image is targeting GNS3 users. I will refrain from commenting.

[^PFB]: I'm perfectly OK with Dell not releasing a Sonic VM that could be used in a virtual lab, but if they do, it should work at least some of the time (see, I'm lowering my bar as I'm ranting).

Finally, there's Nokia. People like Roman Dodin and Jeroen van Bemmel are doing a great job, only to have their hard work tarnished by stupidities like [this one](https://github.com/nokia/ansible-networking-collections/issues/23), which we had to "fix" with [downgrading Ansible to release 4.10](https://github.com/ipspace/netlab/blob/2177d6cb797bd26340ebd594218fca194bc9b1fd/netsim/install/grpc.sh#L36) and downloading `nokia.grpc` collection from GitHub (instead of Ansible Galaxy) when using Nokia devices in _netlab_. Nobody updated the `nokia.grpc` Ansible Galaxy collection in years (or [merged a simple PR](https://github.com/nokia/ansible-networking-collections/pull/27) that would get rid of `nokia.grpc` collection crashing Ansible), and it took the Ansible team [a year and a half](https://github.com/ansible/ansible/pull/79372) to [merge the fix on the Ansible side into release 9.5.1](https://github.com/ansible/ansible/pull/82956).

{{<note update>}}**September 9th 2024:** In the meantime, Nokia released `nokia.srlinux` Ansible Galaxy collection, and Jeroen van Bemmel made it work with *netlab* and fixed most of the configuration templates. In August 2024, I added the polishing touches and made his work part of [*netlab* release 1.9.0-post1](https://netlab.tools/release/1.9/#release-1-9-0-post1). The convoluted software installation needed to use Nokia SR Linux is gone (and it works like a charm).

However (you knew this was coming, right?), _netlab_ still uses `nokia.grpc` collection to configure Nokia SR OS, and (as of September 2024) that collection hasn't been changed since [January 2022](https://github.com/nokia/ansible-networking-collections/commit/f7b6aa79d87c509cd297c122b24018530250288e). We also have no idea what's on Ansible Galaxy; the last time the version number was changed on the `nokia.grpc` collection was in [February 2020](https://github.com/nokia/ansible-networking-collections/commit/6b572c3591256745cf7a555cce97cd0b0142addb), so even if someone published the fixes, we have no way of knowing that. I honestly didn't expect to see Nokia-branded abandonware.
{{</note>}}

To wrap up:

* Making your software widely available has worked for numerous companies and might work for niche networking vendors. 
* Regardless of the underlying motivation, we should loudly praise and support anyone releasing a no-strings-attached networking device VM or container image, and I will continue to do that.
* However, whatever you release in the wild should work in no-brainer scenarios, like running a DHCP client and accepting an address from a DHCP server on the management interface, having a working SSH server, or having a working data plane.
* You might want to attract people who think beyond GUI and console cables; they might appreciate a VM they can connect to via SSH.
* People you want to attract might be someone other than your paying customers, and the VM image you gave them will make a lasting impression. Have a support mechanism in place, or at least fix the glaring problems they point out (or even diagnose in some cases) *in a timely manner*.
* Finally, we all ship buggy code (I'm no exception), but what matters is the time it takes to fix it. It is unacceptable to take months to fix a broken DHCP client or years to merge one-line PRs.

Without all of the above, please don't waste everyone's time releasing images you claim could be used in virtual labs. A broken image does more harm than good.

Also, it's not such a stretch goal. Arista vEOS/cEOS, Aruba CX, Cumulus, Cisco (ASAv, IOSv, IOS-XE, IOS-XR, NexusOS), Juniper vSRX, Mikrotik RouterOS7, Nokia SR Linux, and Vyos worked for me out of the box on the first try.

### Revision History

2024-09-09
: Added information about `nokia.srlinux` Ansible collection
