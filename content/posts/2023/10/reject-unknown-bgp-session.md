---
title: "Will Network Devices Reject BGP Sessions from Unknown Sources?"
date: 2023-10-17 05:48:00
tags: [ BGP, security, netlab ]
pre_scroll: True
netlab_tag: use
---
TL&DR: Violating the [Betteridge's Law of Headlines](https://en.wikipedia.org/wiki/Betteridge%27s_law_of_headlines), the answer is "_Yes, but the devil is in the details._"

It all started with the following observation by Minh Ha left as a comment to my previous [BGP session security blog post](https://blog.ipspace.net/2023/10/bgp-session-security-snafu.html):

> I'd think it'd be obvious for BGP routers to only accept incoming sessions from configured BGP neighbors, right? Because BGP is the most critical infrastructure, the backbone of the Internet, why would you want your router to accept incoming session from anyone but KNOWN sources?

Following my "_opinions are good, facts are better_" mantra, I decided to run a few tests before opinionating[^UNP].
<!--more-->
[^UNP]: That seems to be quite an unpopular approach based on what one can read on the Internet ;) 

### Before Moving On

I want to make a few things crystal clear before someone writes a _you have no clue_ comment:

* It's the methodology that matters, not the specific test results. I wanted to show how easy it is to run some basic tests checking things vendors never want to talk about.
* Things change. You will probably test a different software version than I did and get different results. That's OK.
* I was running tests with virtual machines to ensure every network device uses its own TCP stack. You might get different results with containers as they use the host TCP stack.
* Finally, you should always use the "_trust but verify_" approach[^LENIN] -- the networking vendors might decide to do the _easiest_ not the _right_ thing.

[^LENIN]: Supposedly [coming from Lenin](https://en.wikipedia.org/wiki/Trust,_but_verify). I'm pretty sure he knew what he was talking about ;)

You should also keep in mind that the virtual machines are never  an exact replica of the physical hardware. If you do care about the security of your BGP routers, you REALLY SHOULD rerun the tests on the actual hardware and check whether the TCP SYN packets from the intruder are dropped by an interface ACL, control-plane policing ACL, operating system kernel, or the BGP daemon.

And now let's move on to the fun part.

### Test Setup

I created a simple _netlab_ topology with three routers:

* Device under test (`dut`)
* A valid BGP peer (`peer`)
* An intruder that tries to establish a BGP session with the device under test (`fake`)

```
defaults.device: eos

module: [ bgp ]

plugin: [ nofake ]      # This plugin removes BGP neighbors in AS 65013
                        # ... making the 'fake' device unknown to 'dut'
nodes:
  dut:                  # Device under test, change with 'netlab up -d'
    bgp.as: 65000
  peer:                 # A valid peer -- FRR daemon running in a container
    bgp.as: 65001
    device: frr
    provider: clab
  fake:                 # An intruder -- FRR daemon running in a container
    bgp.as: 65013
    device: frr
    provider: clab
    id: 13

links:
- dut:
  peer:
- dut:                  # Link type set to LAN on the intruder link to make it easier
  fake:                 # ... to find the interface to listen to with tcpdump
  type: lan
```

I had to create a simple plugin that removed `fake` device as a BGP neighbor from all other nodes, resulting in a lab where the `fake` device (172.16.1.13) has `dut` (172.16.1.1) configured as a BGP neighbor, but `dut` knows nothing about 172.16.1.13. Here's the plugin source code in case you're interested in the dirty details:

```
from box import Box

def post_transform(topo: Box) -> None:
  for ndata in topo.nodes.values():
    if not ndata.get('bgp.neighbors',[]):
      continue

    ndata.bgp.neighbors = [ ngb for ngb in ndata.bgp.neighbors if ngb['as'] != 65013 ]
```

After starting the lab with `netlab up -d $dutDeviceType` command I used `virsh` commands to find the Linux bridge connecting `fake` and `dut` nodes and ran `tcpdump` on it to see what's going on.

### Test Results

The good news: I was not able to find a device that would accept a BGP OPEN message and then reply "GO AWAY". The not-so-good news: as expected, I got three types of behavior.

There are devices that run the BGP daemon on top of an unprotected TCP/IP stack. These devices:

* Receive the TCP SYN packet.
* Reply with TCP SYN/ACK packet (directly from the Linux kernel)
* Pass the new connection to the BGP daemon which figures out something's wrong and closes the TCP session.

A typical example is Cumulus Linux. I decided to test the newest community cumulus-vx image (version 5.6.0) and started the lab with **netlab up -d cumulus -s nodes.dut.image=CumulusCommunity/cumulus-vx:5.6.0 -s nodes.dut.memory=4096**

Here's the resulting `tcpdump` printout. You can see that the TCP session is accepted and then immediately closed, first with a FIN and then with a RST packet. 

```
15:49:30.581073 IP 172.16.1.13.60868 > 172.16.1.1.bgp: Flags [S], seq 2075600350, win 64240, options [mss 1460,sackOK,TS val 4031358299 ecr 0,nop,wscale 7], length 0
15:49:30.581345 IP 172.16.1.1.bgp > 172.16.1.13.60868: Flags [S.], seq 1417276596, ack 2075600351, win 64148, options [mss 9176,sackOK,TS val 2284875739 ecr 4031358299,nop,wscale 8], length 0
15:49:30.581368 IP 172.16.1.13.60868 > 172.16.1.1.bgp: Flags [.], ack 1, win 502, options [nop,nop,TS val 4031358299 ecr 2284875739], length 0
15:49:30.581530 IP 172.16.1.13.60868 > 172.16.1.1.bgp: Flags [P.], seq 1:97, ack 1, win 502, options [nop,nop,TS val 4031358299 ecr 2284875739], length 96: BGP
15:49:30.581567 IP 172.16.1.1.bgp > 172.16.1.13.60868: Flags [F.], seq 1, ack 1, win 251, options [nop,nop,TS val 2284875740 ecr 4031358299], length 0
15:49:30.581711 IP 172.16.1.1.bgp > 172.16.1.13.60868: Flags [R], seq 1417276597, win 0, length 0
```

{{<note>}}Please note that the BGP OPEN message (`IP 172.16.1.13.51676 > 172.16.1.1.bgp: Flags [P.]`) is sent concurrently with the TCP FIN packet (`P 172.16.1.1.bgp > 172.16.1.13.51676: Flags [F.]`) so they appear in random order in the printout.{{</note>}}

I also checked FRR source code (yay, Open Source Rulz!) and the [`bgp_accept` function](https://github.com/FRRouting/frr/blob/c8d568487c7c055c8ca503357887de0928b1476b/bgpd/bgp_network.c#L393) does the right thing (from the BGP daemon perspective):

* It accept the incoming TCP session
* It checks the source IP address
* It immediately closes the incoming TCP session if it can't match the source IP address with a known static- or dynamic BGP neighbor.

Cisco Nexus 9300v is exhibiting the exact same behavior:

```
16:19:20.519712 IP 172.16.1.13.51676 > 172.16.1.1.bgp: Flags [S], seq 2181199241, win 64240, options [mss 1460,sackOK,TS val 4033148237 ecr 0,nop,wscale 7], length 0
16:19:20.520233 IP 172.16.1.1.bgp > 172.16.1.13.51676: Flags [S.], seq 1453993839, ack 2181199242, win 28960, options [mss 1460,sackOK,TS val 4294924060 ecr 4033148237,nop,wscale 2], length 0
16:19:20.520271 IP 172.16.1.13.51676 > 172.16.1.1.bgp: Flags [.], ack 1, win 502, options [nop,nop,TS val 4033148238 ecr 4294924060], length 0
16:19:20.520597 IP 172.16.1.13.51676 > 172.16.1.1.bgp: Flags [P.], seq 1:97, ack 1, win 502, options [nop,nop,TS val 4033148238 ecr 4294924060], length 96: BGP
16:19:20.520635 IP 172.16.1.1.bgp > 172.16.1.13.51676: Flags [F.], seq 1, ack 1, win 7240, options [nop,nop,TS val 4294924061 ecr 4033148238], length 0
16:19:20.520918 IP 172.16.1.1.bgp > 172.16.1.13.51676: Flags [R], seq 1453993840, win 0, length 0
```

Cisco IOSv is a bit better. It uses a custom TCP stack that can (apparently) filter incoming TCP SYN requests based on the source IP address -- the TCP SYN packet is immediately answered with a TCP RST packet:

```
16:11:49.683959 IP 172.16.1.13.48878 > 172.16.1.1.bgp: Flags [S], seq 1311594461, win 64240, options [mss 1460,sackOK,TS val 4032697402 ecr 0,nop,wscale 7], length 0
16:11:49.684419 IP 172.16.1.1.bgp > 172.16.1.13.48878: Flags [R.], seq 0, ack 1311594462, win 0, length 0
```

The absolute winner is Arista EOS. It does not reply to the TCP SYN packets at all.

```
15:52:00.908389 IP 172.16.1.13.38022 > 172.16.1.1.bgp: Flags [S], seq 3074546515, win 64240, options [mss 1460,sackOK,TS val 4031508625 ecr 0,nop,wscale 7], length 0
15:52:01.913337 IP 172.16.1.13.38022 > 172.16.1.1.bgp: Flags [S], seq 3074546515, win 64240, options [mss 1460,sackOK,TS val 4031509631 ecr 0,nop,wscale 7], length 0
15:52:03.929317 IP 172.16.1.13.38022 > 172.16.1.1.bgp: Flags [S], seq 3074546515, win 64240, options [mss 1460,sackOK,TS val 4031511647 ecr 0,nop,wscale 7], length 0
15:52:08.089356 IP 172.16.1.13.38022 > 172.16.1.1.bgp: Flags [S], seq 3074546515, win 64240, options [mss 1460,sackOK,TS val 4031515807 ecr 0,nop,wscale 7], length 0
```

It turns out Arista EOS configures **iptables** to drop unexpected BGP packets early in the packet processing path. Here's the relevant part of **iptables** from my vEOS device:

```
-A SERVICE -p tcp -m tcp --sport 179 -j BGP
-A SERVICE -p tcp -m tcp --dport 179 -j BGP
-A SERVICE -j ACCEPT

-A BGP -s 172.16.0.2/32 -j BGPSACL
-A BGP -j DROP
-A BGPSACL -j ACCEPT
```

### Now What?

* Devices that are willing to accept TCP sessions on port 179 from unknown source IP addresses are a pretty good target for a TCP SYN flood. After all, your TCP SYN flood will saturate the BGP daemon and might be able to bring down other BGP sessions due to keepalive timeouts.
* Cisco IOSv is better, but we don't know how early in the packet processing path the TCP SYN packet is rejected.
* Arista EOS (and any other device using a similar approach) will waste the fewest amount of CPU cycles fighting the TCP SYN flood, but might still be prone to denial-of-service attacks.

Here's another opportunity for a _you have no clue_ comment -- after all, most high-speed network devices protect their CPU with [Control Plane Protection](https://blog.ipspace.net/2008/11/control-plane-protection-overview.html) (or Policing). That's cool, but yet again the details matter:

* Is there a hardware mechanism that drops TCP SYN packets for port 179 coming from unknown IP addresses? Lacking that, valid BGP sessions and TCP SYN floods end in the same category.
* Is there a separate CoPP entry that limits TCP SYN packets or do all BGP packets pass the same rate-limiting hardware? If a device treats all BGP packets in the same way it's trivial to bring down all BGP sessions with a TCP SYN flood or a stream of fake packet that consume enough bandwidth.

In the end, you'll probably have to protect the services daemons on the PE-devices with infrastructure ACLs deployed on all external interfaces, but even then someone could send you BGP traffic with spoofed source IP address that will pass that ACL. 

GTSM (TTL protection) was designed to deal with that scenario, but is it good enough? We'll cover that in another blog post.
