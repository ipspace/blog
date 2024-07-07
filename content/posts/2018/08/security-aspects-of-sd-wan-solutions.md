---
date: 2018-08-23 07:48:00+02:00
tags:
- SDN
- WAN
- SD-WAN
title: Security Aspects of SD-WAN Solutions
url: /2018/08/security-aspects-of-sd-wan-solutions/
sd-wan_tag: security
---
Christoph Jaggi, the author of [Transport and Network Security Primer](https://www.ipspace.net/Transport_and_Network_Security_Primer) and [Ethernet Encryption](https://www.ipspace.net/Ethernet_Encryption) webinars [published a high-level introductory article in Inside-IT online magazine](https://www.inside-it.ch/articles/51787) describing security deficiencies of SD-WAN solutions based on the work he did analyzing them for a large multinational corporation.

As the topic might be interesting to a wider audience, I asked him to translate the article into English. Here it is...
<!--more-->
{{<note info>}}For another perspective on SD-WAN, watch the [SD-WAN 101 webinar](https://www.ipspace.net/SD-WAN_Overview) with Pradosh Mohapatra.{{</note>}}

---

*This is a guest blog post by Christoph Jaggi. The opinions expressed are entirely the author's opinions.*

---

### High-Level Summary

An SD-WAN provides less security than a properly secured traditional WAN. A properly secured traditional WAN secures the data plane and the control plane at the same network level: Layer 2 for Ethernet and layer 3 for IP. On closer look, it becomes evident that most, if not all, current SD-WAN solutions violate basic security principles.

### What Is an SD-WAN?

SD-WAN stands for software-defined WAN and belongs to the category of software-defined networks (SDN). The key differentiators from a traditional WAN are the separation of data plane and control plane, and the addition of a central SD-WAN controller and a management portal. This increases the number of connections to be secured and the complexity.

The management portal is normally used for provisioning while the SD-WAN controller controls and orchestrates the forwarding decisions of the edge devices. The division of tasks between the management portal and SD-WAN controller depends on the implementation of the particular vendor. The same is true for the operation of an SD-WAN. While the SD-WAN controller and management portal of some products are entirely operated in a vendor cloud, other products provide the flexibility to be operated in a private cloud or on premises. There is no standard.

SD-WAN can but it doesn't have to virtualize a network. In case of network virtualization, the transport network becomes the underlay network that carries the virtual logical networks that constitute the overlay network. This sounds more complex than it is.

Secure network virtualization for layer 3 is still in its infancy while it is widely used for layer 2. There are encryption solutions for Ethernet that provide the option of either encrypting each single overlay network (VLAN) individually or encrypting the underlay network. These sophisticated solutions do not come from Silicon Valley, as the US vendors are generally way behind the actual state of the art in terms of key management for network encryption and network encryption in general. The lag is at least five years. These shortcomings become highly visible when looking at the encryption of virtualized networks at layer 3.

SD-WAN can also be used in combination with hybrid networks, which use more than a single physical network for the WAN traffic.

### Network Security

The maximum achievable network security is determined by the weakest element. All connections between sites are subject to the same threat scenario and, therefore, should be equally well protected. This is true for the network layer at which the encryption takes place as well as for the protocols, algorithms, and encryption environment. The lower the encryption layer, the higher the network security when using the same algorithms and the same encryption environment. The depth of the encryption layer determines how much data remains visible and unencrypted.

{{<figure src="/2018/08/s550-SD-WAN+Architecture.png" caption="Typical SD-WAN architecture">}}

An SD-WAN adds connections to the SD-WAN controller and the management portal to the connections between sites. These connections should be equally well protected as the connections between the edge devices. The connection between the edge device and SD-WAN controller often carries the control plane and management plane. As it is a layer 3 connection (IP), the encryption should be at layer 3. If it takes place at layer 4, the protection level is reduced to application security and misses the goal of network security. It is also a common issue that the need for key change for long-lived connections is overlooked when using TLS, as TLS does not have a seamless key change facility. The current offers available on the market are limited in terms of the security level they provide and belong to the low assurance category. While this is obvious when looking at the details, it has been completely overlooked by the leading market analysts such as Gartner, Forrester Research, IDC, and Frost & Sullivan. Therefore, all of the assessments and recommendations by those companies should be taken with a pinch of salt.

#### What Are the Things to Look at?

The only common elements between the different SD-WAN offers on the market are the separation of the data plane and the control plane, and the takeover of the control plane by an SD-WAN controller. When looking at an SD-WAN solution it is part of the due diligence to look at the key management and the security architecture in detail. There are different approaches to implement network security, each having its own benefits and challenges.

Your starting point should be the review of the security architecture. If the management portal is part of a vendor cloud, there is an increased security risk as the vendor cloud can push down data to the SD-WAN controller and the edge devices. A US vendor cloud is also subject to the [CLOUD Act](https://www.congress.gov/bill/115th-congress/senate-bill/2383/text) and US national interests, which makes it a non-mitigatable security risk, especially for non-US companies.

The key management covers all the aspects of encryption for the entire system including management portal, SD-WAN controller, and edge device. For a review, it is indispensable that the vendor is willing and capable of providing detailed information in well-structured documents. If a vendor is either not willing or not capable of providing such documentation, it is a red flag. These are documents that must be available both in product management and in engineering. The publicly available marketing materials and the documentations do not provide the necessary depth.

During due diligence, the following areas should be covered:

-   Must meet the current state of the art in key management
-   Must meet the current state of the art in terms of cryptographic protocols and algorithms
-   Sufficient entropy and randomness for key generation
-   Sufficient key lengths and domain parameters
-   Correct choice of parameters for crypto functions
-   Robust and sufficiently evaluated solution.

While all the current SD-WAN solutions integrate network encryption as a function, the assurance level that they achieve is low. This is good enough for unclassified and not overly sensitive data. For standard and high assurance requirements, the current integrated solutions are insufficient -- to address them you still have to use dedicated encryption solutions.
