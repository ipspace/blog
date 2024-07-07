---
date: 2010-07-26 07:17:00+02:00
tags:
- service providers
- Internet
- QoS
title: P2P Traffic Is Bad for the Network
url: /2010/07/p2p-traffic-is-bad-for-network/
---
I'm positive you all know that. I also hope that you're making sure it's not hogging your enterprise network. Service Providers are not so fortunate -- some Internet users claim using unlimited amounts of P2P traffic is their birthright. I don't really care what kind of content these users transfer, they are consuming enormous amounts of network resources due to a combination of P2P client behavior (which is clearly "optimized" to grab as much as possible) and the default TCP/QoS interaction.
<!--more-->
Let's start with the P2P behavior:

-   P2P implementations (for example, BitTorrent clients) open a large amount of simultaneous TCP sessions. 200 concurrent sessions is a very "reasonable" number and some people claim that the [10 new sessions per second limit imposed by Windows XP SP2](http://www.techiecorner.com/34/how-to-adjust-your-window-xp-tcp-connection-to-boost-your-bt-download-speed/) is reducing their speed... now you know how many sessions they tend to open.
-   P2P client can saturate any link for a very long time. I'm a heavy Internet user, but I still use around 1% of my access speed (long-term average). A P2P client can bring the long-term average close to 100%.

I wouldn't mind the reckless implementations of P2P clients if the Internet would be an infrastructure where every user gets its fair share of bandwidth. Unfortunately, the idealistic design of the early Internet ensures that (using default router settings) every *TCP session* gets the same amount of bandwidth. A P2P user with 200 concurrent sessions thus gets 200 times the bandwidth of another user downloading her e-mail with a POP3 session. Clearly not a win-win situation (for anyone but the P2P guy) that could easily result in "a few" annoyed calls to the SP helpdesk.

What we would need to cope with the P2P users is per-user (per-IP-address) queuing, which is not available on any router that I'm familiar with (let alone on any high-speed platform). If you have other information, please share it in the comments.

The best solution I'm aware of is a dedicated box that can perform per-user measuring with real-time actions. Unfortunately, they are usually to expensive to deploy at every bottleneck in the network; they are usually deployed somewhere between the access and core network with plenty of bandwidth surrounding them.

To address the P2P challenge with bandwidth control devices, you could define very smart bandwidth groups or you track per-user quotas (actually per-IP-address quotas) and act once a user exceeds her quota -- for example, by hard-limiting the user's bandwidth or remarking her packets with a low-priority DSCP value which can then be used to select a different (low-priority) queue on congested links. That's exactly the approach Comcast took in the end and documented in [RFC 6057](https://tools.ietf.org/html/rfc6057).