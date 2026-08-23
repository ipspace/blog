---
title: "Yak-Shaving netlab Podman Support"
date: 2026-08-27 07:30:00+0200
tags: [ netlab ]
netlab_tag: details
---
Long, long time ago, in a [long-forgotten PR](https://github.com/ipspace/netlab/pull/587) adding support for Cumulus VX Ignite runtime, an [off-the-cuff remark was made](https://github.com/ipspace/netlab/pull/587/changes#diff-08e871da6c853eda9062b91cab02f26978e08acb645d46ebb77f4295e461eb8aR62) saying, "*and this is how you use netlab with Podman*". That remark was quietly sitting in the documentation for years until someone (A) tried to use Podman and (B) found enough time to [report](https://github.com/ipspace/netlab/issues/3690) that it doesn't work with *netlab*.

I don't know what that tells us: either very few people use Podman, or nobody (apart from a notable exception) cares enough to spend a few minutes telling us stuff doesn't work[^NUN].

[^NUN]: There's the third option that I'm sure my lovely anonymous troll will eventually figure out: nobody is using *netlab*. However, I have approximately a dozen data points saying otherwise 🤷🏻‍♂️

Anyway, based on [Joey Buiteweg](https://github.com/joebb97)'s wonderful research, I was able to put together a working solution pretty quickly, but it did involve a lot of [yak shaving](https://en.wiktionary.org/wiki/yak_shaving) ([more bovine details](https://seths.blog/2005/03/dont_shave_that/)).
<!--more-->
The original _netlab_ implementation tried to do things the easy way (which rarely works) -- when the default *clab* runtime is set to *podman*, add the *podman* runtime to all nodes. That might have worked at the time the off-the-cuff remark was made[^IDI]; recent *containerlab* versions check the Docker socket (and thus fail miserably when Docker is not installed) *unless* you use the `-r` CLI argument (which didn't fit nicely into how _netlab_ starts the underlying orchestration system) *or* specify the runtime in `CLAB_RUNTIME` environment variable.

[^IDI]: Although I doubt there was much more than idle speculation behind it, and yes, blame me for merging it 🤦‍♂️

The environment variable seemed like the perfect solution, and it worked well on my test server. Alas, it failed to work on more recent versions of Ubuntu. More research by [@joebb97](https://github.com/ipspace/netlab/issues/3690#issuecomment-5085027768) and [@jbemmel](https://github.com/ipspace/netlab/issues/3690#issuecomment-5085174443) turned up the culprit: someone figured out it would be great fun to [break `sudo`](https://github.com/trifectatechfoundation/sudo-rs#differences-from-original-sudo). Gee, thanks a million, guys. That was really appreciated.

Back to the drawing board. Fortunately, new versions of *containerlab* support [sudoless operation](https://containerlab.dev/install/#sudo-less-operation), but it requires the user to be in the `clab_admins` group. Removing `sudo` from *start containerlab* commands was [easy](https://github.com/ipspace/netlab/pull/3704/changes), and a few warnings in the documentation should hopefully be enough[^NIMU].

[^NIMU]: Most users shouldn't be impacted. *netlab* checks *containerlab* version before starting the lab, and every *containerlab* upgrade should trigger the creation of the missing `clab_admins` group.

With that hurdle out of the way, we could pass the `CLAB_RUNTIME` variable to *containerlab*, and it would happily use Podman runtime (and stop complaining about the missing Docker socket). Adding a Podman installation script (you can do **netlab install podman** now) was a breeze after I figured out how to start the service that provides the socket-based API.

Next: quite a few **docker** commands are baked into the _netlab_ source code[^ECBV]. Fortunately, Podman provides a Docker-like CLI that implements most of the **docker** commands we use. Dodged that bullet 🎉.

[^ECBV]: After programming for over 40 years, I still haven't learned that every constant eventually becomes a variable.

However, Podman has a different idea of who can see a running container than Docker. By default, only the user who starts the container can see it, and because *containerlab* has to start containers as root to create vEth pairs between them, a regular user cannot see them. End result: you could start the lab, but you couldn't connect to the lab devices. For the moment, we ignored this inconvenience and [documented](https://netlab.tools/labs/clab/#podman-support) that you MUST run Podman-based labs as root 🤷🏻‍♂️ (turning a bug into a fad[^FAD]).

[^FAD]: Functions as Designed

That should be it, right? I thought so, and the feature shipped in release 26.08. As is so often the case, the dirty details surfaced when the code met reality:

* Podman provides a Docker-like CLI, but its JSON outputs [don't exactly match](https://github.com/ipspace/netlab/pull/3804) the corresponding Docker commands (gee, that's REALLY useful).
* Docker has a built-in DNS server that we used when creating the container's `/etc/resolv.conf` files. Podman uses the host's DNS resolver when creating those files, and the Docker-like settings we used to implement DNS clients on Linux-based containers failed to work with Podman. That's been [fixed as well](https://github.com/ipspace/netlab/pull/3808).

These fixes are coming in the next *netlab* release (planned for early September 2026), or you could [install the *dev* version](https://netlab.tools/install/clone/).
