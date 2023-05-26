---
date: 2010-10-25 06:47:00.002000+02:00
tags:
- workshop
- MPLS VPN
- QoS
- ADSL
title: QoS over MPLS/VPN Networks
url: /2010/10/qos-over-mplsvpn-networks.html
---
A while ago John McManus wrote a great [*DSCP QoS Over MPLS Thoughts*](http://etherealmind.com/dscp-qos-over-mpls-thoughts/) article at [Etherealmind blog](http://etherealmind.com/) explaining how 6-bit IP DSCP value gets mapped into 3-bit MPLS EXP bits (now [renamed to *Traffic Class* field](http://tools.ietf.org/html/rfc5462)). The most important lesson from his post should be "there is no direct DSCP-to-EXP mapping and you have to coordinate your ideas with the SP". Let's dig deeper into the SP architecture to truly understand the complexities of this topic.

We'll start with a reference diagram: user traffic is flowing from Site-A to Site-B and the Service Provider is offering MPLS/VPN service between PE-A and PE-B. Traffic from multiple customer sites (including Site-A) is concentrated at SW-A and passed in individual VLANs to PE-A.
<!--more-->
{{<figure src="s1600-MPLSVPN_QoS.png" caption="QoS options in an MPLS/VPN network">}}

Assuming the connection between Site-A and SW-A is a native IP connection (using native VLAN with no 802.1p markings), SW-A will apply its own marking rules to the inbound packets before sending them in 802.1q-tagged frames to PE-A. Most often, the DSCP values in the inbound IP packets will be ignored.

SW-A might also perform inbound sub-rate policing. If you buy (for example) 20 Mbps service over 100 Mbps access link, it doesn't make sense to propagate your traffic bursts over the SW-A-PE-A link just to police (and drop) them on PE-A.

The link between SW-A and PE-A could become congested, resulting in queuing and dropping. Unless the service provider applies rigorous 802.1p marking on ingress traffic, the results will be random and not at all congruent with your QoS vision.

Traffic sent by Site-A enters MPLS/VPN cloud at PE-A, where your traffic is usually metered and policed to ensure you don't swamp the MPLS/VPN cloud. At the same time, the PE-router performs DSCP-to-EXP mapping. By default, the IP precedence bits (top 3 bits of the DSCP value) are copied to the EXP bits, but most service providers would use a customized mapping behavior to ensure their users can't abuse the network or send high-priority traffic they haven't subscribed for.

Once the MPLS/VPN traffic is labeled and marked, it enters the MPLS backbone. The queuing behavior in the backbone depends solely on the service provider's network design and is impossible to predict in advance. You might as well assume they offer no differentiated services unless you get a detailed written explanation from them.

When the traffic arrives at PE-B it's sent as native IP traffic toward Site-B. If you're using sub-rate service the traffic might be policed (in which case all bets are off) or shaped (don't expect it, shaping is expensive). As the traffic is shaped or queued on the physical interface, PE-B might use your original DSCP values to classify the traffic and selectively drop excess packets.

Finally, if at least one of the access links uses DSL, you have an [entirely different can of worms to deal with](https://blog.ipspace.net/2009/06/adsl-qos-basics.html).

And what can you do to influence the whole process? Not much -- you can remark your traffic on the CE-router to map your QoS schema into DSCP values that the service provider recognizes. You can also shape (and [queue within the shaping queue](/kb/tag/QoS/Traffic_Shaping.html)) your traffic to ensure it's not randomly policed on SW-A or PE-A. Apart from that, you're solely at mercy of the service provider.

## Lessons learned

-   Don't expect the service provider to understand or honor your DSCP values;
-   Start from the core network: figure out the QoS features your service provider supports (often: none);
-   Remark your traffic at CE-routers to comply with the SP-dictated values (breaks end-to-end QoS) or change your overall QoS scheme (warning: significant provider lock-in);
-   Shape the outbound traffic to avoid indiscriminate inbound policing on PE-routers. If at all possible, use a recent IOS release with Hierarchical Queuing Framework (HQF shaping introduces less delay/jitter than pre-HQF implementations).
