---
title: "Goodbye, Cumulus Community Vagrant Boxes"
date: 2025-02-19 08:01:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
Last Monday, I decided to review and merge the "[VXLAN on Cumulus Linux 5.x with NVUE](https://github.com/ipspace/netlab/pull/1832)" pull request. I usually run integration tests on the modified code to catch any remaining gremlins, but this time, all the integration tests started failing during the VM creation phase. I was completely weirded out, considering everything worked a week ago.

Fortunately, Vagrant debugging is pretty good[^VD] and I was quickly able to pinpoint the issue ([full printout](https://github.com/ipspace/netlab/issues/1781#issuecomment-2663343672)):
<!--more-->
[^VD]: Even though it's not configurable and thus suffers from severe verbal diarrhea.

* The VM would start and get an IP address
* Vagrant would try to SSH to the VM using the default Vagrant SSH key
* The SSH negotiation would succeed, but then the authentication would fail with:

```
You are required to change your password immediately (password expired).
```

* To add insult to injury, Cumulus VM would add:

```
WARNING: Your password has expired.
Password change required but no TTY available.
```

Let me recap:

* You're trying to log into a device using an SSH key
* The device rejects the log-in attempt because *the password* (that you're not using) *has expired*.

I can't possibly fathom how one could recover from that situation if one had never used the password to log into the device, but maybe that's just my lack of Linux skills.

Anyway, that shouldn't be a big deal. Download a newer version of the Vagrant box (one published within 6 months) and move on. Well, that no longer works. The latest release of the public [CumulusCommunity/cumulus-vx](https://portal.cloud.hashicorp.com/vagrant/discover/CumulusCommunity/cumulus-vx/versions) box is almost exactly 6 months old, and the newest box is only 12 days younger (hooray, we got another week to go).

{{<note info>}}Jeroen van Bemmel [found a workaround](https://github.com/ipspace/netlab/issues/1938#issuecomment-2663860073) that fixes the VM disk extracted from Vagrant box.{{</note>}}

Like any other vendor that doesn't want to alienate their potential customers[^CSCO], NVIDIA offers software download options, carefully protected with an email-collecting regwall. OK, that's par for the course. However, the Vagrant boxes you can download have no version information (will they never learn?) and have the same password expiration policy[^IT]. It looks like we'll have to go through the hassle of downloading and installing a new box every few months.

[^CSCO]: As opposed to Cisco making it impossible to download even a crippled version of its ancient operating system without a support contract.

[^IT]: Trust me, I checked that. I moved the VM clock 6 months into the future with [**vagrant-libvirt** `clock_adjustment` parameter](https://vagrant-libvirt.github.io/vagrant-libvirt/configuration.html#clock) and got the same behavior.

To recap:

* Newer Cumulus Community boxes are useless.
* The ancient boxes (Cumulus Linux 4.4) still work, but I'd prefer using FRR on Debian over three-year-old software. The only real difference between the two is MLAG support.
* Cumulus containers were a [personal pet project](https://github.com/networkop/cx) of an engineer who moved on years ago and are no longer maintained or updated. The latest release was 5.3.0, created [approximately two years ago](https://hub.docker.com/r/networkop/cx/tags).

It looks like the Cumulus Linux fairy tale is over for good, and we're dealing with yet another vendor-as-usual. I knew it was too good to last.
