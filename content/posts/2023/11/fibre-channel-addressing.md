---
title: "Fibre Channel Addressing"
date: 2023-11-06 07:06:00
tags: [ networking fundamentals ]
comment: |
  In early 2020 I created the _[Local Area Network Addressing](https://my.ipspace.net/bin/get/Net101/NA2.2%20-%20Local%20Area%20Network%20Addressing.mp4?doccode=Net101)_ video as part of the _[How Networks Really Work webinar](https://www.ipspace.net/How_Networks_Really_Work)_. This blog post is an edited transcript of the first part of that video.
---
Whenever we talk about LAN data-link-layer addressing, most engineers automatically switch to the "*must be like Ethernet*" mentality, assuming all data-link-layer LAN framing must somehow resemble Ethernet frames.

That makes no sense on point-to-point links. As explained in *[Early Data-Link Layer Addressing](https://blog.ipspace.net/2023/10/data-link-addressing.html)* article, you don't need layer-2 addresses on a point-to-point link between two layer-3 devices. Interestingly, there is one LAN technology (that I'm aware of) that got data link addressing right: [Fibre Channel](https://en.wikipedia.org/wiki/Fibre_Channel) (FC). 
<!--more-->
Fibre Channel[^FCSP] switches are routers. To understand that claim, we have to dive a bit deeper into the [Fibre Channel Protocol](https://en.wikipedia.org/wiki/Fibre_Channel_Protocol) stack because Fibre Channel layers don't line up with the OSI layer we're familiar with:

[^FCSP]: Yes, it is spelt that way to (quoting Wikipedia) "_avoid confusion and to create a unique name._"

-   FC0 is the physical layer. No doubt there.
-   They call FC1 the "transmission protocol." This layer handles encoding, error control, framing, and start/end of frame signaling. FC1 is what we would call the data link layer. 
-   Signaling protocol (FC2) provides end-to-end transport, which we would call the network+transport layer.
-   FC3 provides common services for advanced features, including hunt groups and multicast. FC3 might be the FC equivalent of a session layer.
-   Finally, FC4 is the application layer.

There are only FC2 addresses in the FC. There is no need for FC1 addressing because every FC switch (intermediate node in an FC network) is an FC2 forwarder. It might not be correct to call an FC switch a router or a bridge -- those are IP/Ethernet terms. However, an FC switch forwards packets based on FC2 addresses, and because FC2 is the FC network layer equivalent, we would call it a layer three switch or a router in the IP world.

{{<figure src="/2023/11/dll-fibre-channel.png">}}

I had [heated discussions with FC gurus](https://blog.ipspace.net/2011/07/is-fibre-channel-switching-bridging-or.html) who claimed that FC switches were bridges. I read the FC standards, which used "*routing*" to describe FC packet forwarding. So, I don't think you should blame me for the terminology straight out of the FC standards. However, what tripped the FC gurus was the lack of two pairs of source and destination addresses. Their conclusion: "_Obviously, the first address in the payload must be the MAC address._" "_FC must be bridging,_" they said because they've never seen a data link layer with no addresses.   

However, all FC switches are layer-3 (FC2) switches, and because there are only point-to-point links between a fiber channel node and a fiber channel switch, there is absolutely no need for data link layer (FC1) addressing.
