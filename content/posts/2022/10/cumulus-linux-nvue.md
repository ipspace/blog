---
cli_tag: fail
date: 2022-10-11 06:11:00+00:00
pre_scroll: true
series:
- cli
series_weight: 400
tags:
- Cumulus Linux
title: 'Cumulus Linux NVUE: an Incomplete Data Model'
---
A few weeks ago I described how Cumulus Linux tried to ~~put lipstick on a pig~~ [reduce the Linux data plane configuration pains](/2022/09/linux-data-plane-configuration.html) with [Network Command Line Utility](/2022/09/cumulus-nclu.html). NCLU is a thin shim that takes CLI arguments, translates them into *FRR* or *ifupdown* configuration syntax, and updates the configuration files (similar to what Ansible is doing with ***something*\_config** modules).

Obviously that wasn't good enough. [Cumulus Linux 4.4 introduced NVIDIA User Experience](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-44/System-Configuration/NVIDIA-User-Experience-NVUE/)[^NV] -- a full-blown configuration engine with its own data model and REST API[^NNC].
<!--more-->
[^NV]: I was told NVIDIA always made sure Linux users had interesting user experiences.

[^NNC]: ... and probably no NETCONF or OpenConfig, at least I couldn't find anything along those lines in the documentation. Who would need one of those in 2022 anyway. It also doesn't use YANG, but OpenAPI Specification. I was under the impression I was dealing with networking gear, but I was obviously wrong.

NCLU was an add-on to Linux configuration files, NVUE is an authoritative source of configuration information. You can change the data model through the API calls (or command line), and once you apply the changes, NVUE generates *FRR* and *ifupdown* configuration *from scratch*.

With NCLU, you could go straight into FRR configuration or change `/etc/network/interfaces` if NCLU didn't support a parameter you needed. There's no such backdoor with NVUE.

Having a strict data model could be a good thing. It prevents all sorts of weird things networking engineers love to do when trying to build a ladder to get out of the corner they painted themselves into[^BM]. It could also be a bad thing if the vendor forgot to include obvious things in the data model.

[^BM]: While blaming the vendors supplying the paint for the path they took while painting the room.

Here's one that triggered this blog post[^YK]: it's impossible to set the source IP address of an IBGP session (the equivalent of **neighbor update-source** *FRR* configuration command). 

{{<note update>}}**2022-12-01**: According to an email I got from [Eric Pulvino](https://www.linkedin.com/in/pulvino/) a few days ago, Cumulus Linux v5.3.0 includes support for **neighbor update-source** configuration via NVUE. Well done!{{</note>}}

Here's what Cumulus Linux 5.2.1 allows you to set on a BGP neighbor:

[^YK]: You knew it was coming, didn't you?

```
cumulus@r1:mgmt:~$ nv set vrf default router bgp neighbor 10.0.0.3 -h
usage:
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [address-family ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [bfd ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [capabilities ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [description ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [enable ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [enforce-first-as ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [graceful-restart ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [local-as ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [multihop-ttl ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [nexthop-connected-check ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [passive-mode ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [password ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [peer-group ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [remote-as ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [timers ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [ttl-security ...]
  nv [options] set vrf <vrf-id> router bgp neighbor <neighbor-id> [type ...]

Description:
  <neighbor-id>         Peers

Identifiers:
  <vrf-id>              VRF (vrf-name)
  <neighbor-id>         Peer ID (ipv4 | ipv6 | interface-name)

Attributes:
  address-family        Address family specific configuration
  bfd                   Specifies whether to track BGP peering sessions using this configuration via BFD.
  capabilities          Capabilities
  description           neighbor description
  enable                Turn the feature 'on' or 'off'.  The default is 'on'.
  enforce-first-as      If on, when BGP updates are received from EBGP peers with this config, check that first AS matches peer's AS
  graceful-restart      BGP Graceful restart per neighbor configuration
  local-as              Local AS feature
  multihop-ttl          Maximum hops allowed.  When 'auto', the type of peer will determine the appropriate value (255 for iBGP and 1 for eBGP).  This is the default.
  nexthop-connected-check
                        If 'on', it disables the check that a non-multihop EBGP peer should be directly connected and only announce connected next hops
  passive-mode          If enabled, do not initiate the BGP connection but wait for incoming connection
  password              Password
  peer-group            Optional peer-group to which the peer is attached to inherit the group's configuration.
  remote-as             ASN for the BGP neighbor(s) using this configuration.  If specified as 'external', it means an EBGP configuration but the actual ASN is immaterial. If specified as 'internal', it means an IBGP configuration.
  timers                Peer peer-timerss
  ttl-security          RFC 5082
  type                  The type of peer
```

I'm a bit old and I might be missing things, and there might be a way to set the source IP address of a TCP session, but I was looking at the above printout for too long and couldn't find it.

Does it matter? It depends. Do you want to deploy an "obscure" BGP design where you run IBGP sessions between loopback interfaces advertised with an IGP? Good luck, you can't use NVUE to configure that. Interestingly, the capability to set BGP update source was present in NCLU (`net add bgp neighbor <bgppeer> update-source (<ipv4>|<ipv6>|<interface-source>)`), so it was recognized as an important parameter, and someone must have made a conscious decision not to implement it in NVUE.

{{<note>}}Joe Hlasnik found a way to set update source for a BGP session: you have to create a peer group, and set the update source as part of *peer group capabilities*. 

Obvious, right 🥴 Nonetheless, I still couldn't find that mentioned anywhere in the documentation (apart from *list of NVUE commands*).{{</note>}}

Well, as always there's an ugly workaround -- you can use [NVUE snippets](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-52/System-Configuration/NVIDIA-User-Experience-NVUE/NVUE-Snippets/) to add stuff to *FRR* or *ifupdown* configuration[^OTF]. That sounds cool until you get tired of configuring half of the BGP neighbor parameters with NVUE API calls and the other half with *FRR* configuration commands[^CNC] passed through NVUE API calls[^NXOS].

[^OTF]: ... or any other text file if you like editing files through REST API

[^CNC]: [Other vendors aren't much better](/2018/01/use-yang-data-models-to-configure.html)

[^NXOS]: The whole thing reminds me of early NETCONF on Cisco Nexus OS that produced **show** printout in text format... but nicely wrapped in XML envelope.

I'm positive that NVUE developers implemented what Cumulus customers were asking for, which tells you much about who and how uses Cumulus Linux. I also don't care why they didn't implement the most fundamental parameter you need to have  in an IBGP-based network. I simply [documented the shortcomings](https://netlab.tools/caveats/#cumulus-5-0-with-nvue) in *Platform Caveats* and moved on, but the whole thing did leave a pretty sour aftertaste.

### Revision History

2022-12-01
: Cumulus Linux v5.3.0 includes support for NVUE-based **neighbor update-source** configuration

2022-10-12
: Joe Hlasnik found a way to set the BGP update source. Thanks a million!
