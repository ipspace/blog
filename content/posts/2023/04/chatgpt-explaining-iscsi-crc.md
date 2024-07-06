---
ai_tag: kick
title: "ChatGPT Explaining the Need for iSCSI CRC"
date: 2023-04-16 07:19:00
lastmod: 2023-04-16 15:50:00
tags: [ switching, SAN, AI ]
pre_scroll: True
---
People keep telling me how well large language models like ChatGPT work for them, so now and then, I give it another try, most often resulting in another disappointment[^NR]. It might be that I suck at writing prompts[^PE], or it could be that I have a knack for looking in the wrong places[^ID].

[^NR]: I'm a strong believer in publishing negative results, and would gladly publish an insightful conversation with ChatGPT.

[^PE]: Did you know that _prompt engineer_ is already a thing, and there's training you can attend to get better at writing prompts?

[^ID]: I do, at least according to my wife and my coworkers.

This time[^TT] I tried to "figure out[^BP]" why we need iSCSI checksums if we have iSCSI running over Ethernet which already has checksums. Enjoy the (ChatGPT) circular arguments and hallucinations with plenty of platitudes and no clear answer.

[^TT]: April 14th 2023, using free version of ChatGPT

[^BP]: After updating [this blog post](/2013/03/does-dedicated-iscsi-infrastructure.html)
<!--more-->

Based on the readers' feedback, I tried the same query using three AI tools:

* [ChatGPT using GPT-3.5](#35) (the original blog post)
* [ChatGPT using GPT-4](#G4)
* [Phind search engine](#phind) including the [benefits of FCoTR](#fcotr)

### ChatGPT using GPT-3.5{#35}

> Why is there an application-level checksum in iSCSI?

The application-level checksum in iSCSI is used to ensure data integrity during data transmission between an initiator (client) and a target (server) in a storage area network (SAN) environment. The checksum is calculated by the initiator and included in the iSCSI protocol data unit (PDU) header.

The checksum is necessary because data corruption can occur during transmission due to various reasons such as electromagnetic interference, hardware failure, or software bugs. The checksum provides a way to verify that the data received by the target is the same as the data sent by the initiator. If the checksum calculated by the target does not match the one sent by the initiator, it indicates that there has been data corruption during transmission, and the target can request the data to be resent.

Without the application-level checksum, the data transmission between the initiator and the target would be unreliable, and data corruption could go undetected, leading to potential data loss or system errors. Therefore, the application-level checksum is a crucial feature of iSCSI to ensure the integrity and reliability of data transmission in a SAN environment.

> You're mentioning transmission errors -- wouldn't Ethernet checksum catch those?

Yes, you are correct. Ethernet uses a cyclic redundancy check (CRC) to provide a basic level of data integrity checking. The Ethernet CRC is calculated by the network interface controller (NIC) in the sending device and is verified by the NIC in the receiving device. The CRC is a simple checksum that detects most common transmission errors, such as bit flips or dropped packets, but it is not foolproof and can miss some types of errors.

However, iSCSI operates at a higher layer of the network stack than Ethernet, and it uses its own protocol for encapsulating SCSI commands and data within IP packets. The iSCSI protocol includes additional error checking mechanisms, including a more robust checksum that provides a higher level of data integrity checking than the Ethernet CRC.

The iSCSI checksum is calculated by the iSCSI initiator, and it covers the SCSI command, data, and header information. It provides an end-to-end verification of the integrity of the SCSI commands and data as they are transmitted over the network. This is important because the SCSI commands and data are critical to the operation of the storage system, and any errors could cause data corruption or other issues.

Therefore, while the Ethernet CRC provides a basic level of error checking, the iSCSI checksum is an additional layer of protection that helps ensure the integrity of the data as it is transmitted over the network.

> Is Ethernet really using CRC?

Yes, Ethernet uses a cyclic redundancy check (CRC) as its error detection mechanism. When an Ethernet frame is transmitted, a CRC is calculated over the data portion of the frame and appended to the end of the frame. The receiving device recalculates the CRC over the received data and compares it with the CRC sent by the sender. If the calculated CRC does not match the one sent by the sender, the receiver knows that an error has occurred during transmission.

The Ethernet CRC is a mathematical algorithm that generates a fixed-length checksum based on the data in the frame. It is designed to detect errors such as single-bit errors, double-bit errors, and some burst errors. The CRC algorithm is chosen because it is simple, fast, and provides a high degree of error detection capability.

However, it is important to note that the Ethernet CRC is not perfect and can sometimes fail to detect errors. For example, it may not detect errors that occur in the Ethernet header or errors that are introduced by a malfunctioning network device. Additionally, the CRC cannot correct errors, it can only detect them. In cases where error correction is required, higher-level protocols such as TCP/IP may be used to provide additional error correction and recovery mechanisms.

Despite its limitations, the Ethernet CRC is still a widely used and effective method of error detection in Ethernet networks.

> Does iSCSI checksum detect more errors than Ethernet CRC? Why?

Yes, the iSCSI checksum is designed to detect more errors than the Ethernet CRC, primarily because it operates at a higher layer of the network stack and provides a more comprehensive check of the data being transmitted.

The iSCSI checksum is calculated by the initiator and covers the SCSI command, data, and header information. This means that the checksum covers not only the payload data but also the protocol information, ensuring that the entire iSCSI PDU is checked for errors. In contrast, the Ethernet CRC only covers the payload data and does not include any protocol information.

Additionally, the iSCSI checksum uses a stronger error detection algorithm than the Ethernet CRC. While the Ethernet CRC is a relatively simple algorithm that is designed to detect only certain types of errors, the iSCSI checksum uses a more complex algorithm, such as CRC-32C, which is designed to detect a wider range of errors, including more complex error patterns.

Furthermore, iSCSI checksums can be computed over multiple packets, and in some cases, over multiple TCP streams, while Ethernet CRCs are calculated on a per-packet basis. This allows the iSCSI checksum to detect errors that may span multiple packets or streams, which would not be detected by the Ethernet CRC.

Overall, the iSCSI checksum provides a more comprehensive and robust error detection mechanism than the Ethernet CRC, due to its ability to check the entire iSCSI PDU, its use of a stronger error detection algorithm, and its ability to compute checksums over multiple packets and streams.

> Which CRC algorithm is Ethernet using?

Ethernet uses the CRC-32 algorithm for error detection. The CRC-32 algorithm is a 32-bit cyclic redundancy check (CRC) that generates a checksum based on the data in an Ethernet frame. The checksum is appended to the end of the frame and is used by the receiving device to verify the integrity of the data.

The CRC-32 algorithm is widely used in many different applications, including Ethernet, because it is relatively simple, fast, and provides a high degree of error detection capability. It is designed to detect common transmission errors such as single-bit errors, double-bit errors, and some burst errors.

The CRC-32 algorithm works by dividing the data into 32-bit blocks and performing a bitwise XOR operation on each block to generate a 32-bit remainder. The remainder is then appended to the end of the data to form the checksum. The receiving device performs the same calculation on the received data and compares the resulting checksum to the one sent by the sender. If the two checksums match, the receiving device knows that the data has been transmitted without errors. If the checksums do not match, the receiving device knows that an error has occurred during transmission.

Overall, the CRC-32 algorithm provides a simple and effective means of error detection in Ethernet networks, ensuring the integrity of the data being transmitted.

---

And this, my friends, is how you write a long blog post in 10 minutes instead of wasting hours researching it -- skip the prompts and claim it's your masterpiece. I don't want to know how much bullshit there will be on the Internet in a few months.

Anyway, in case you care about the real answer: Ethernet CRC is protecting a single layer-2 segment, and data corruption could happen in intermediate nodes where it's protected by weak (but fast) [16-bit sum of the content](https://en.wikipedia.org/wiki/Transmission_Control_Protocol#Checksum_computation).

In favor of ChatGPT:
 
* "iSCSI checksum protecting the whole PDU" argument is a good one.
* It mentioned "errors that are introduced by a malfunctioning network device" (the crucial point) and then kept going.

On the other hand, the description of how CRC32 works seems a bit off.

As for real-life advantages of iSCSI CRC32C over IEEE-802 CRC32: [RFC 3385](https://www.rfc-editor.org/rfc/rfc3385) contains all the details you never wanted to know.

### Everything Is Better with GPT-4{#G4}

Following a [nudge by Andrew Yourtchenko](/2023/04/chatgpt-explaining-iscsi-crc.html#1755), I decided to waste $20 and go for GPT+ to get access to GPT-4 model. It does a much better job, misses the _weak TCP checksum_, claims TCP checksum provides integrity only on specific segments, but does mention _silent data corruption_. Overall: B+/A-

---

> Why is there an application-level checksum in iSCSI?

There are a few reasons why an application-level checksum is used in iSCSI:

* End-to-end data integrity: While lower-level protocols, such as Ethernet and TCP/IP, have their own error detection mechanisms, they only provide integrity checks on specific segments of data in transit. An application-level checksum in iSCSI provides end-to-end data integrity, ensuring that the entire data payload is accurate and reliable from the source to the destination.

* Detection of silent data corruption: Silent data corruption refers to errors that go unnoticed by the underlying hardware and software layers. An application-level checksum in iSCSI can help detect such errors and ensure data integrity.

* Redundancy: Incorporating an application-level checksum provides an additional layer of error detection that complements the existing mechanisms in the network and transport layers. This redundancy increases the likelihood of detecting and correcting errors in data transmission.

* Compatibility with diverse storage systems: iSCSI is designed to work with various types of storage systems and environments. An application-level checksum allows for a uniform and standardized method to ensure data integrity across different storage systems, regardless of their individual error-detection capabilities.

In summary, the use of an application-level checksum in iSCSI is primarily for maintaining end-to-end data integrity and providing an extra layer of error detection. This ensures that the data transmitted between the initiator and target is accurate and consistent, and helps in detecting silent data corruption.

---

However, most everyone who hasn't been dazzled by the AI-glitz agrees that (A) every large language model will eventually start hallucinating and that (B) you have to fact-check everything you get from them. GPT and friends are thus potentially useful tools   (if you use them in full awareness of their limitations), not solutions in themselves. More about that in another blog post.

### Phind Wins the Day{#phind}

[JC suggested](/2023/04/chatgpt-explaining-iscsi-crc.html#1757) using [phind search engine](https://www.phind.com/). Here's what it gave me (note how different the answer is from what JC got):

---

**Why is there an application-level checksum in iSCSI?**

The iSCSI protocol is a storage area network (SAN) protocol that enables block-level access to storage devices. It is used to send SCSI commands over IP networks, making it a cost-effective alternative to Fibre Channel. According to storage expert Dennis Martin [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin), there is an application-level checksum in iSCSI to perform data integrity checks on the storage data carried by iSCSI. This is because the TCP checksum is not considered adequate for critical storage data. The iSCSI checksum is calculated by the initiator and target and is used to verify that the data received is the same as the data sent.

Ethernet checksums are not reliable enough for data integrity, and TCP/IP checksums are weak. They might be good enough for some traffic, but not for critical storage data [\[4\]](/2015/11/ethernet-checksums-are-not-good-enough.html). Ethernet CRC is supposed to detect transmission errors, and TCP/IP checksums should detect rare intra-device data corruption errors. However, layer-3 switches recalculate the CRC, which no longer protects the integrity of Ethernet frames between end hosts [\[4\]](/2015/11/ethernet-checksums-are-not-good-enough.html). Therefore, it is recommended to implement an application-level checksum, preferably using CRC32C, which is implemented in hardware on recent CPUs [\[4\]](/2015/11/ethernet-checksums-are-not-good-enough.html).

There are two main iSCSI security measures: Challenge-Handshake Authentication Protocol (CHAP) and Internet Protocol Security (IPsec) [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin). CHAP is used to authenticate the initiator and target, while IPsec is used to encrypt the iSCSI traffic. CHAP and IPsec can handle a lot of things within iSCSI itself, but it is also possible to do other forms of encryption with the Ethernet connection, and there are other things that can be done with data at rest and the storage side [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin).

There are several ways to manage iSCSI multipathing. Most operating systems can handle multipath I/O (MPIO) [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin). Microsoft is MPIO, and there's MPxIO, but in either case, there's sort of generic multipathing that uses a single iSCSI session, and you can have multiple addresses on the initiator, the target, or both. Some iSCSI targets support what's called multiple connections, so you can use a different sort of method to log in and then accomplish the multipathing using this multiple connection option. Typically, multiple connections and things like MPIO are mutually exclusive -- you have to pick one or the other [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin).

It is best practice to run iSCSI traffic on a separate network or at least a separate virtual LAN, as iSCSI puts a different kind of traffic load on the network [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin). It is recommended to use server-class network adapters for iSCSI and not to use desktop NICs just because they're cheaper, as they can't handle all the extra features iSCSI would like to use, including Receive-Side Scaling (RSS), partial offload functions like TCP and UDP checksum offload, Large Send Offload (LSO), and Large Receive Offload [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin).

Applications don't know the difference between iSCSI and Fibre Channel, so the best thing to do is figure out what you need [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin). If you need very little latency and lots of scalability and nodes in the network, you might go with Fibre Channel. If you don't need the low latency and need something a little simpler, then you could go with iSCSI [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin). Jumbo frames give you more payload per transmission, and they can provide a performance bump, especially when running on 1 GbE [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin). However, it is recommended to use them in situations where you want to get less congestion on the network [\[1\]](https://www.techtarget.com/searchstorage/podcast/iSCSI-performance-An-expert-discussion-with-Dennis-Martin).

In summary, the iSCSI protocol uses an application-level checksum to perform data integrity checks on the storage data carried by iSCSI, as the TCP checksum is not considered adequate for critical storage data. CHAP and IPsec are the only iSCSI security measures, but other forms of encryption can be used with the Ethernet connection. There are several ways to manage iSCSI multipathing, including MPIO and multiple connections, but they are mutually exclusive. It is best practice to run iSCSI traffic on a separate network or at least a separate virtual LAN, and to use server-class network adapters for iSCSI. Applications don't know the difference between iSCSI and Fibre Channel, so it is best to figure out what you need. Jumbo frames give you more payload per transmission and can provide a performance bump, especially when running on 1 GbE, but they should be used in situations where you want to get less congestion on the network.

---

**Notes:**

* The answer is correct (as far as I understand iSCSI)
* Way too verbose, including stuff I never asked about.
* Bonus points for [quoting my blog post](/2015/11/ethernet-checksums-are-not-good-enough.html) several times ;)

#### phind on the Benefits of FCoTR{#fcotr}

Obviously the _AI-augmented search engine_ approach suffers the everyday GIGO problem: can you trust the stuff written on the Internet? For example, it gladly explained the benefits and drawbacks of FCoTR (also note that the link it provided is broken):

---

**What are the benefits of FCoTR storage technology?**

FCoTR (Fibre Channel over Token Ring) is a storage technology that enables Fibre Channel traffic to be transmitted over Token Ring networks. [treehugger.com](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/mds9000/sw/4_1/configuration/guides/cli_4_1/clibook/fcotr.html) It has several benefits, which include:

-   Cost savings: FCoTR allows organizations to use existing Token Ring networks for Fibre Channel traffic. This eliminates the need for new Fibre Channel infrastructure, which can be costly to implement.

-   Improved performance: FCoTR provides high-speed connectivity for Fibre Channel traffic over Token Ring networks, which can improve performance compared to traditional Token Ring networks.

-   Flexibility: FCoTR allows organizations to use a variety of storage devices, including SANs and NAS, with Token Ring networks.

-   Scalability: FCoTR can support large-scale storage environments, making it suitable for organizations with growing storage needs.

-   Compatibility: FCoTR is compatible with existing Fibre Channel storage systems, which means that organizations can continue to use their existing storage infrastructure while taking advantage of the benefits of FCoTR.

However, there are also some drawbacks to FCoTR technology, which include:

-   Limited availability: FCoTR is not widely used, which means that it may be difficult to find support or expertise in implementing and managing FCoTR-based storage systems.

-   Complexity: FCoTR requires specialized knowledge and expertise to implement and manage, which can increase the complexity of storage environments.

-   Compatibility issues: FCoTR may not be compatible with all storage devices, which can limit its usefulness in certain environments.

In conclusion, FCoTR technology offers several benefits for organizations looking to use Fibre Channel traffic over Token Ring networks, including cost savings, improved performance, and flexibility. However, it also has some drawbacks, including limited availability, complexity, and compatibility issues. Organizations should carefully consider these factors before implementing FCoTR-based storage systems.

### Revision History

2023-04-16 15:50Z
: Added phind answer

2023-04-16 13:26Z
: Added ChatGPT GPT-4 answer