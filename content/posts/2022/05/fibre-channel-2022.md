---
title: "Is Fibre Channel Still a Thing?"
date: 2022-05-12 06:26:00
tags: [ SAN ]
---
Here's another "_do these things ever disappear?_" question from Enrique Vallejo:

> Regarding storage, is Fibre Channel still a thing in 2022, or most people employ SATA over Ethernet and NVMe over fabrics?

**TL&DR**: Yes. So is COBOL.

To understand why some people still use Fibre Channel, we have to start with an observation made by Howard Marks: "*Storage is different.*" It's OK to drop a packet in transit. It's NOT OK to lose data at rest.
<!--more-->
That (absolutely correct) mentality resulted in highly reliable black-box systems called _storage arrays_ that had to be accessed (due to their high costs) by many systems. Unfortunately, we had a gazillion of server operating systems in late 1980s, and the simplest way forward was to emulate the existing SCSI adapters and the 50-pin SCSI cable, resulting in [Fibre Channel](https://en.wikipedia.org/wiki/Fibre_Channel) lossless network requirements.

Fibre Channel has been around for ~30 years, and storage has changed in the meantime -- we got ~~scale-out~~ software-defined storage (SDS) and hyper-converged infrastructure (HCI). Using Fibre Channel in SDS or HCI would be like using COBOL to develop a new snazzy web app; these solutions use proprietary access methods (example: VMware VSAN) or look like an iSCSI/NFS target (example: Nutanix).

Regardless of [AWS S3 durability marketing](https://www.lastweekinaws.com/blog/s3s-durability-guarantees-arent-what-you-think/), some data is too precious to be put  into a distributed storage system; you might still want to use a dedicated storage array for your production transactional database. 

Do you have to use Fibre Channel if you decide you still need a storage array? Absolutely not. It's cheaper[^BETTER] to build a dedicated Ethernet fabric[^SANAB] to run iSCSI or NFS than it is to build a new Fibre Channel network. 

Would Fibre Channel give you better performance? Probably not. Years ago, I was told that FC works better than iSCSI because the transport stack is simpler and more standardized whereas every vendor uses a slightly different variant of TCP stack that has to be tuned for maximum performance. I hope that real-life experience and Moore's Law brought us way beyond the "_good enough_" point.

Does that make Fibre Channel dead? Of course not. People who have been building and upgrading their FC-based SAN for the last 30 years will keep doing so. Would I use Fibre Channel in a new deployment? Absolutely not.

Finally, a word on [ATA-over-Ethernet](https://en.wikipedia.org/wiki/ATA_over_Ethernet): it's a simple protocol running directly on top of Ethernet. I [considered that a bad idea in 2010](/2010/09/ataoe-for-converged-data-center/) (the [vendor using ATAoE strongly disagreed](/2010/09/ataoe-response-from-coraid/)) and I haven't changed my mind even though [someone had great experience running ATAoE on Debian](/2013/10/ataoe-is-alive-and-well/).

[^BETTER]: I wanted to write _better_, but then remembered that _better_ depends on what metric you like to choose ;)

[^SANAB]: Or two if you believe in strict SAN-A/SAN-B separation