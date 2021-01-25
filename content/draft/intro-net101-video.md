---
draft: True
---
# (Pub) Video: Bridging, Routing, Switching

If you're working only with IP-based networks, you're probably quick to assume that hop-by-hop destination-only forwarding is the only packet forwarding paradigm that makes sense. Not true, even today's networks use a variety of forwarding mechanisms, most of them called some variant of *routing* or *switching*.

What exactly is the difference between the two, and what is bridging? I'm answering these questions (and a few others like what's the difference between data-, control- and management planes) in the Bridging, Routing and Switching Terminology video.

{{<jump>}}Watch the video{{</jump>}}

{{<note info>}}The video is part of _[How Networks Really Work](https://www.ipspace.net/Net101)_ webinar and available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).{{</note>}}

# (Pub) Video: Getting a Packet Across a Network

Now that we (hopefully) agree on what routing, bridging, and switching are, let's focus on the first important topic in this area: how do we get a packet across the network? Yet again, there are three fundamentally different technologies:

* Source node knows the full path (source routing)
* Source node opened a path (virtual circuit) to the destination node and uses that path to send traffic
* The network performs hop-by-hop destination-address-based packet forwarding.

More details in the Getting Packets Across the Network video.

{{<jump>}}Watch the video{{</jump>}}

{{<note info>}}The video is part of _[How Networks Really Work](https://www.ipspace.net/Net101)_ webinar and available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).{{</note>}}

# (Pub) Video: Multi-Layer Switching and Tunneling

After [discussing the technology options one has when trying to get a packet across the network](https://blog.ipspace.net/2020/11/video-getting-packet-across-network.html), we dived deep into two interesting topics:

* How do you combine packet forwarding at multiple layers of OSI stack (multi-layer switching)?
* What happens when you do layer-N forwarding over layer-N transport core (example: IPv6 packets over IPv4 packets) aka tunneling?

You'll find more details (including other hybrids like Loose Source Routing) in *[Multi-Layer Switching and Tunneling](https://my.ipspace.net/bin/get/Net101/SW3%20-%20Multi-Layer%20Switching%20and%20Tunneling.mp4?doccode=Net101)* video.

{{<jump>}}[Watch the video](https://my.ipspace.net/bin/get/Net101/SW3%20-%20Multi-Layer%20Switching%20and%20Tunneling.mp4?doccode=Net101){{</jump>}}

{{<note info>}}The video is part of _[How Networks Really Work](https://www.ipspace.net/Net101)_ webinar and available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).{{</note>}}

# (Pub) Video: Finding Paths Across the Network

Regardless of the technology used to get packets across the network, someone has to know **how** to get from sender to receiver(s), and as always you have multiple options:

* Almighty controller
* On-demand dynamic path discovery (example: probing)
* Participation in a routing protocol

For more details, watch Finding Paths Across the Network video.

{{<jump>}}Watch the video{{</jump>}}

{{<note info>}}The video is part of _[How Networks Really Work](https://www.ipspace.net/Net101)_ webinar and available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).{{</note>}}

# Video: Path Discovery in Transparent Bridging and Routing

In the previous video I described how path discovery works in source routing and virtual circuit environments. I couldn't squeeze the discussion of hop-by-hop forwarding into the same video (it would make the video way too long); you'll find it in the next video in the [same section](https://my.ipspace.net/bin/list?id=Net101#SWITCH).

{{<jump>}}Watch the video{{</jump>}}

{{<note info>}}The video is part of _[How Networks Really Work](https://www.ipspace.net/Net101)_ webinar and available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).{{</note>}}
