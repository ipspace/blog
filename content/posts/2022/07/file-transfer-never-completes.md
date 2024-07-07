---
title: "Twilight Zone: File Transfer Never Completes"
date: 2022-07-27 06:27:00
tags: [ history, WAN ]
---
Ages ago when we were building networks using super-expensive 64kbps WAN links, a customer sent us a weird bug report:

> Everything works fine, but we cannot transfer one particular file between two locations -- the file transfer stalls and eventually times out. At the same time, we're seeing increased number of CRC errors on the WAN link.

My chat with the engineer handling the ticket went along these lines:
<!--more-->
Me: _What kind of modems are they using?_\
Him: _One of those weird baseband modems[^BB] running at 128 or 256 kbps_\
Me: _Try enabling link compression_[^LC]

A few hours later, he came back to me saying "_That solved the problem. How did you know?_"

### WTF?

At that time, I had a [few bad experiences with the baseband modems](/2022/07/file-transfer-drops-link/) pushing the performance envelope way past the breaking point, and suspected that it might be a clock synchronization issue: a long sequence of zeroes or ones would cause the receiving modem to lose synchronization with the transmitting modem's clock. A well-designed solution should use line encoding that would allow the receiver to recover clock from any input data, but when you buy magic products, you get magic behavior.

A long sequence of ones shouldn't be a problem on an HDLC[^HDLC] link -- the HDLC encoding inserts a zero after five consecutive ones to avoid end-of-frame sequence (six consecutive ones) -- but there's nothing HDLC can do about long sequences of zeroes. Link compression replaced long sequences of zeroes with some other sequence of bits. Problem solved.

Encryption would probably work equally well, as would [NRZI encoding](https://en.wikipedia.org/wiki/Non-return-to-zero#Non-return-to-zero_inverted). I don't think Cisco IOS had encryption at that time (and we'd be wasting CPU cycles without any performance gain), and you couldn't set NRZI encoding on some serial interfaces. Using link compression made our customer happy, and their network seemingly faster.

### More to Explore

Why don't you check out _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar -- you can watch [numerous videos](https://my.ipspace.net/bin/list?id=Net101) in that webinar with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).

[^BB]: Some creative modem manufacturers managed to push up to 1 Mbps over a telephone circuit that was supposed to be able to carry 28 kbps, relying on the fact that there was a pair of physical wires (thus _baseband_) between the modems. These tricks worked best when the stars were properly aligned.

[^LC]: Cisco routers had software link compression on PPP/HDLC links.

[^HDLC]: HDLC is the data link layer protocol used by PPP. Whenever you're running PPP over a serial line, you're using HDLC.