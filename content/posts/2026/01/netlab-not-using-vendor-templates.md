---
title: "Why Doesn't netlab Use X for Device Configuration Templates?"
date: 2026-01-22 08:14:00+0100
tags: [ netlab ]
netlab_tag: contribute
---
Petr Ankudinov made an [interesting remark](https://www.linkedin.com/feed/update/urn:li:activity:7397274499341053953?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7397274499341053953%2C7397617419760058368%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287397617419760058368%2Curn%3Ali%3Aactivity%3A7397274499341053953%29) when I [complained](https://www.linkedin.com/feed/update/urn:li:activity:7397274499341053953/) about how much time I wasted waiting for Cisco 8000v to boot when developing _netlab_ device configuration templates:

> For Arista part - just use AVD with all templates included and ANTA for testing. I was always wondering why netlab is not doing that.

Like any other decent network automation platform, _netlab_ uses a high-level data model (lab topology) to describe the network. That data model is then transformed into a device-level data model, and the device-level data structures are used to generate device configurations.
<!--more-->
This diagram from a [blog post](/2021/02/data-model-transformation/) I wrote almost exactly five years ago nicely illustrates the concept[^TBM]:

[^TBM]: That blog post also includes a "there be magic" diagram for people who hate the details.

{{<figure src="/2021/02/dm-multi-platform.png" caption="Multi-platform automation solution">}}

Any network automation platform has to deal with three challenging questions:

1. What high-level data model will you use to describe the network and network services?
2. What data model will be used to describe device data?
3. What mechanism will be used to configure network devices?

There are high-level data models describing network services (IETF working groups produced plenty of them), but they tend to be a union of all possible nerd knobs ever dreamed of and thus way too complex for what we were trying to achieve. Compare, for example, the [IETF EVPN YANG data model](https://datatracker.ietf.org/doc/html/draft-ietf-bess-evpn-yang-07)[^IEY] with the [few parameters](https://netlab.tools/module/evpn/#global-evpn-parameters) we use to configure baseline EVPN functionality[^NM]. Using a select few high-impact parameters per technology/protocol seemed like a much better option.

[^IEY]: The fact that all YANG data models for BGP-based services are expired IETF drafts is not comforting either.

[^NM]: _netlab_'s mission is to help network engineers build baseline labs, not to have a way to implement every nerd knob out there.

Selecting a device data model was also easy. As we wanted to support a [very large number of different platforms](https://netlab.tools/platforms/) with _netlab_, we couldn't rely on cool kids like OpenConfig or IETF YANG data models; too many devices still don't support them. Furthermore, these data models are either focused on the needs of their creators (OpenConfig) or represent the least common denominator of humming consensus[^IHC] (IETF). They might thus not contain all the parameters we might care about. Finally, even though a device might implement a data model, it doesn't necessarily implement all its nuances (data model *augmentation* is part of the YANG RFC). The only sane choice seemed to be a data model that is as simple as possible while still covering the parameters we need.

[^IHC]: As expected, there's an [RFC](https://datatracker.ietf.org/doc/html/rfc7282) describing that "process"

Finally, the configuration mechanism. We try to be as flexible as possible. Most devices are configured with device configuration snippets; we use **bash** scripts with some Linux-based containers or VMs, JSON-RPC for SR-Linux, and gRPC for SR-OS[^DAW]. In all cases, we use Jinja2 templates to transform our device-level data into configuration snippets or JSON[^JY] data structures.

[^DAW]: Please don't ask why

[^JY]: Actually YAML, because it's much easier to create YAML data structures in a text template than to deal with JSON commas.

Could we use our approach with Arista AVD? Sure, but we'd either have to adopt their data models, which would make even less sense (considering our multi-platform focus) than using IETF data models, or transform our device data into Arista AVD device data, and then use Arista's configuration templates to generate configuration snippets.

Likewise, we could have a template that would transform our device data into OpenConfig- or IETF-defined device data. Unfortunately, we'd still have to check whether the [transformation is done correctly](/2024/05/network-automation-testing/) and whether the [transformation results work as expected on network devices](/2024/05/netlab-integration-tests/), so we'd still be limited primarily by how fast the virtual devices boot (which, in Arista's case, is not a bottleneck at all -- I love their containers[^ETD]).

[^ETD]: If only their engineers would be able to persuade powers-that-be to make them easier to download.
