---
date: 2010-09-17 15:12:00.001000+02:00
tags:
- data center
- SAN
title: ATAoE for Converged Data Center Networks? No Way
url: /2010/09/ataoe-for-converged-data-center.html
---
When I started writing about storage industry and its attempts to tweak Ethernet to its needs, someone mentioned ATAoE. I read the [ATAoE Wikipedia article](http://en.wikipedia.org/wiki/ATA_over_Ethernet) and concluded that this dinky technology probably makes sense in a small home office... and then I've stumbled across an [article in The Register that claimed you could run a 9000-user Exchange server on ATAoE storage](http://www.theregister.co.uk/2010/08/10/coraid_esg/). It was time to deep-dive into this "interesting" L2+7 protocol. As expected, there are numerous good reasons you won't hear about ATAoE in my [Data Center 3.0 for Networking Engineers](https://www.ipspace.net/DC30) webinar.

{{<note info>}}The following text has been published on SearchNetworking's Fast Packet blog in 2010. That web site disappeared in the meantime, and the URL returns a 404 error. Fortunately I found a snapshot of the article on the Internet Archive.{{</note>}}
<!--more-->
When I started exploring storage networking technologies from a networking engineer's perspective, I stumbled across ATA over Ethernet (ATAoE) – or ATA command set transported directly within Ethernet frames. The approach seemed similar to Fibre Channel over Ethernet (FCoE) – only with even less industry acceptance.

As I abhor protocol designers who are shortsighted enough to purposely limit themselves to a single LAN domain, I never looked deeper into the technology until I stumbled across an article in The Register praising the virtues of ATAoE.

Further research quickly confirmed that ATAoE is limited primarily to a single vendor (Coraid) and the Wikipedia article on ATAoE revealed an "amazing" fact: "AoE specification is 12 pages compared with iSCSI's 257 pages." While I never considered the length of protocol specification to be an indication of its quality, in this case, unfortunately, you get what you see: a whole lot of nothing.

It could be that ATAoE is blindingly fast technology (so is iSCSI), but the protocol is so broken that I would sincerely recommend staying as far away from it as possible. Let's go through the details.

**No sequencing:** The protocol does not contain a single sequence number that would allow servers and storage arrays to differentiate between requests or split a single request into multiple Ethernet frames. A server can thus have only a single outstanding request with any particular storage array. (Or maybe LUN -- who knows? The protocol specifications are silent.)

**No retransmissions:** The protocol does not specify any packet loss detection or recovery mechanism. I can only assume that the only recovery the creators envision is request retransmission after a timeout, hoping that all requests can be repeated multiple times without side effects.

**No fragmentation:** ATAoE requests fit directly into Ethernet frames, and there's no way to fragment a single request into multiple frames and achieve streamlined data flow. Unless you use jumbo frames, you'll be able to transfer at most two sectors (at 512 bytes) in each request. (iSCSI can transfer megabytes in a single transaction.) Add a few switches to the mix, and watch performance plummet.

**No authentication:** Can you imagine that? A protocol proposed for use in the data center that has no authentication whatsoever! The Wikipedia article proves that whoever designed (or described) this protocol was a total stranger to the finer details of network security when they wrote: "The non-routability of AoE is a source of inherent security."

The protocol does provide MAC Mask List command, which should provide a basic access control. Did those people ever hear of MAC address spoofing? With iSCSI, at least you have to hijack the TCP session (not impossible, but not trivial either). With ATAoE, all you have to do is generate random Ethernet frames with a spoofed source MAC address and you can quickly scramble someone's disk.

**No sessions:** Another amazing omission. A server does not have to establish a session with the storage. As soon as you guess a LUN number, you can start reading and writing its data.

**Weak support of asynchronous writes:** Due to lack of sequencing and retransmissions, asynchronous writes are handled in a truly cavalier fashion: You can use them and the storage array always returns a success status, but the actual operation might fail -- and the server will never be informed. I thought it would be nice to know if your write operation fails (after all, you might need that data in the future), but apparently that's not the case.

A protocol like this could have been good enough 30 years ago when TFTP was designed, but today it would make a great example of a totally broken protocol in any protocol design class. As for its usability: Go ahead and use it when building your home network. I would definitely not consider it for mission-critical data center applications.

### Related Blog Posts

* [ATAoE: response from Coraid](/2010/09/ataoe-response-from-coraid.html)
* [ATAoE Is Alive and Well](/2013/10/ataoe-is-alive-and-well.html)
