---
title: "Exploring the BGP Neighbor CONNECT State"
date: 2026-08-18 07:16:00+0200
tags: [ BGP ]
---
Sakar left an [interesting comment](https://blog.ipspace.net/2025/01/bgp-connect-state/#3020) on my [The Curious Case of the BGP Connect State](/2025/01/bgp-connect-state/) blog post, claiming that Cisco IOS/XE goes through a CONNECT state when opening an incoming BGP session.

I wanted to double-check this behavior, so I needed a scenario where one router would keep sending TCP SYN requests, the other would not (or we wouldn't learn anything), and the two routers could not communicate (or they'd quickly go into the OPEN state).

Here's my first attempt at meeting those requirements:
<!--more-->
* The first router (R1) is using a regular EBGP configuration
* The second router (R2) has R1 configured as a passive neighbor (so it will accept TCP SYN packets but not originate them)
* R2 would have a static discard route for the IP address of R1 to ensure its TCP SYN+ACK reply never gets back to R1.

Well, that didn't work out. BGP next hop tracking on Cisco IOS caught my dirty trick, decided to keep the neighbor *idle*, and rejected its TCP SYN packets. Back to the drawing board.

Next option: what if I had an incoming ACL on R1 dropping incoming BGP packets? That didn't work either -- the TCP SYN+ACK reply was rejected by the incoming ACL, R1 sent an ICMP unreachable to R2, and R2 immediately shut down the TCP session.

There's always one more nerd knob: I disabled the ACL-generated ICMP messages with **no ip unreachables** interface command, and finally got to the stage where R1 and R2 had a half-baked TCP session. Guess what: IOS/XE claimed the neighbor was still Idle.

The only place where Cisco IOS/XE displays a Connect BGP state is in the **debug ip bgp** printout -- when the incoming TCP session on port 179 is *established*, the neighbor state goes from *Idle* to *Connect*, and when the BGP routing process decides to send the BGP OPEN message, the state goes from *Connect* to *OpenSent*. Not exactly what [RFC 4271 claims should happen](https://datatracker.ietf.org/doc/html/rfc4271#section-8).

### Kicking the Tires

Here are a few _netlab_ topologies you can use to test your device(s). The first one uses the static discard route and should work on many devices (more details about the [dot notation](/2026/08/netlab-compress-lab-topology/) I'm using):

```
provider: clab
module: [ bgp, routing ]
plugin: [ bgp.session ]

nodes:
  r1.bgp.as: 65000
  r2:
    bgp.as: 65001
    routing.static:
    - ipv4: 10.1.0.1/32
      nexthop.discard: True

links:
- r1.ipv4: 10.1.0.1/24
  r2:
    ipv4: 10.1.0.2/24
    bgp.passive: True
```

{{<note>}}
Note that I didn't specify the default device in the lab topology. I have to start the lab with the `-d` parameter to specify the default device (for example, `netlab up -d iol` to test Cisco IOL), but that ensures I don't waste my time waiting for incorrect devices ;) I did specify the `provider` I want to use because I'm trying to run everything I do in *containerlab* containers.
{{</note>}}

The second lab topology uses ACLs (a new _netlab_ feature coming in August 2026) and a custom **no ip unreachables** command. You'll have to replace that command with whatever your device uses:

```
provider: clab
module: [ bgp, routing ]
plugin: [ bgp.session, files ]

nodes:
  r1:
    bgp.as: 65000
    routing.acl:
      nobgp:
      - action: deny
        protocol: tcp
        src:
          prefix: any
          port.eq: 179
      - protocol: ip
    config.inline: |
      interface {{ interfaces[0].ifname }}
        no ip unreachables
  r2:
    bgp.as: 65001

links:
- r1:
    ipv4: 10.1.0.1/24
    routing.acl.in: nobgp
  r2:
    ipv4: 10.1.0.2/24
    bgp.passive: True
```


