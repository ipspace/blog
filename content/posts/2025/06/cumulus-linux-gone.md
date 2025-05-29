---
title: "Cumulus Linux (As We Know It) Is Gone"
date: 2025-06-02 08:36:00+0200
tags: [ data center ]
---
A reader of my blog pointed out the following minutiae hidden at the very bottom of the [Cumulus Linux 5.13 What's New](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-513/Whats-New/) document:

> NVIDIA no longer releases Cumulus VX as a standalone image. To simulate a Cumulus Linux switch, use NVIDIA AIR.

And what is [NVIDIA AIR](https://docs.nvidia.com/networking-ethernet-software/nvidia-air/)?
<!--more-->
> NVIDIA Air is a cloud-hosted, data center simulation platform that behaves like a real-world production environment. Use NVIDIA Air to create a digital twin of your IT infrastructure.

Why would one want to use it? The only reason I can find is the [ASIC emulation](https://www.nvidia.com/en-us/networking/ethernet-switching/air/#features):

> Verify network behavior at highest fidelity without needing dedicated hardware

Having a dataplane implementation that's reasonably close to the hardware one is awesome. However, there's no reason one could not have the same code in a public VM image (apart from the ridiculous "_but then anyone could look at it_" argument).

I completely understand that vendors want you to register (so their sales and marketing teams can harass you) and accept an EULA before using their software (to make the legal department happy), but forcing users to use a cloud product is ridiculous.

It's not like we wouldn't have precedents for that phenomenal idea. Juniper attempted to push Junosphere[^JS] but quickly gave up, finally making relevant images downloadable with no strings attached. Cisco tried something similar (IIRC), but got to their senses and released CML. Most other vendors didn't even bother.

[^JS]: I wonder how many people heard about it. If you didn't, you just proved my point.

**To recap:** In a world where most networking vendors give you VM images you can use to get familiar with their products[^FPW] in a multi-vendor environment,  NVIDIA expects you to deal with a cloud/GUI-based product that supports SONiC and Cumulus Linux on emulated NVIDIA hardware.

[^FPW]: It could be a free image or a product like CML. The image could be free to download or protected by a regwall. It doesn't matter; you can download and use it.

It's sad to see how far the [noble ideas of the original Cumulus Networks team](https://blog.ipspace.net/2015/08/video-what-is-cumulus-linux-all-about/) have fallen. Maybe [what Linus Torvalds said about NVIDIA](https://www.youtube.com/watch?v=tQIdxbWhHSM) before he became politically correct wasn't so far off the mark :(
