---
date: 2016-01-18 07:36:00+01:00
tags:
- SDN
- data center
- fabric
title: Network Node Shutdown Is a Process, not an Event
url: /2016/01/network-node-shutdown-is-process-not/
---
In theory, you should shut down a network device with a well-defined procedure:

-   Drain the traffic from the device;
-   Verify the device is no longer forwarding traffic;
-   Turn off the device.

In practice, network devices don't have a **shutdown** command, and **reload** typically just restarts the network OS.
<!--more-->
## Graceful Shutdown

Every major vendor claims they have *graceful shutdown* functionality, but there's a small problem: the shutdown is usually not so very graceful. For example:

-   BGP router tears down BGP sessions;
-   OSPF router sends a HELLO packet with no neighbors (tearing down all adjacencies).

In both cases, the neighbors immediately remove routes advertised by the device, go in panic mode and try to find alternate paths.

The only benefit of the so-called graceful shutdown is that the neighbors discover session/adjacency loss immediately and not after TCP/BGP/OSPF timeout/dead interval.

## Is there a better way?

Of course -- you could use *overload* bit in IS-IS (and IS-IS based fabrics like Cisco's FabricPath), **max-metric router-lsa** in OSPF, and route revocation in BGP. The first two can be configured with a single configuration command in many routers and data center switches, the last one requires a bit more work.

## Next steps

The very minimum you should do if you care about traffic loss following a network device shutdown/restart is a more controlled shutdown process: instead of typing **reload**, reconfigure the routing process (see above), wait for the network to converge (10 seconds should be more than enough) and then execute **reload** making sure the latest changes are not saved to permanent configuration.

You can also change the FHRP priority while waiting, and it's pretty easy to automate the whole process.

{{<note info>}}Cisco Nexus OS and Arista EOS also support *maintenance mode*, which shuts down all interfaces apart from the management port -- an ideal alternative to power-off or reload.{{</note>}}

Finally, you could sprinkle some magic SDN dust on top of this solution: verify adjacent devices stopped using the network device before shutting it down. You could use BGP-LS for OSPF or IS-IS, or [BGP Monitoring Protocol](https://tools.ietf.org/html/draft-ietf-grow-bmp-16) or BGP-based SDN controller for BGP.

## More details

Watch [BGP-based SDN](http://www.ipspace.net/BGP-Based_SDN_Solutions) webinar to see how you could solve the problem in BGP-based data center fabrics, or [Facebook's RIPE71 presentation](https://ripe71.ripe.net/archives/video/152/) to see how Facebook uses similar functionality in their network.
