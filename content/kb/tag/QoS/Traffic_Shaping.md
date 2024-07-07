---
kb_section: QoS
minimal_sidebar: true
title: Traffic Shaping
url: /kb/tag/QoS/Traffic_Shaping/
---
*Traffic shaping* is a QoS mechanism that creates an artificial congestion point and sends packets at a predefined (shaping) rate regardless of the output interface congestion state. You can use it to enforce a traffic contract even when the bandwidth of the outbound interface far exceeds the contractual rate.

In Cisco IOS Modular QoS CLI framework you configure traffic shaping with the **shape** command within a **policy-map class**. 

Both shaping and [policing](/kb/tag/QoS/QoS_Policing/) can be used to in Cisco IOS to enforce the traffic contract. Policing drops or relabels out-of-contract packets without incurring any transmission delay or processing overhead while shaping delays out-of-contract packets, resulting in increased delay and jitter. Most TCP implementations respond much better to shaping of excess traffic (increased transmission delay) than policing which result in packet drops, retransmissions, and drastic reduction in transmission rate. On the other hand, excessive amount of shaping and buffering results in [buffer bloat](https://en.wikipedia.org/wiki/Bufferbloat).

The configuration details of this article apply to Cisco IOS traffic shaping on non-distributed software switching architecture (low-end and midrange routers). High-speed routers and devices using hardware packet switching use a variety of device-specific shaping mechanisms (assuming the hardware is complex enough to support traffic shaping).

## Typical Usage Scenarios

Traffic shaping is commonly used when the traffic has to be prioritized on a link which is too fast to experience output queue congestion, for example:

* On a core site in an MPLS VPN network
* On a hub site in a DMVPN network
* On a virtual machine connected to a virtual switch

{{<figure src="/kb/tag/QoS/Shaping_Usage.png" caption="Using traffic shaping on a DMVPN hub site">}}

The obvious bottleneck in the above DMVPN network is the uplink of the *Spoke* router, and if the provider does not implement the desired QoS mechanisms on this link, the high-priority traffic sent from the *Hub* site to the *Spoke* site might be delayed due to the output queue congestion on outbound interface of the service provider router on which the customer has no influence.

{{<note note>}}The issues described in this section are not limited to DMVPN networks; similar problems occur in most access networks including xDSL- and cable networks.{{</note>}}

The only alternative to proper outbound queuing within the service provider network is the introduction of an artificial bottleneck (implemented with traffic shaping) on the outbound interface of the *Hub* router. Once the bottleneck is introduced, the packets that exceed the transmission capacity of the *Spoke* uplink are delayed and stored into the shaping queue  on the *Hub* router where they can be prioritized and reordered.

## Cisco IOS Configuration

Historically Cisco IOS implemented numerous somewhat incompatible standalone traffic shaping mechanisms, including *Generic Traffic Shaping (GTS)* and *Frame Relay Traffic Shaping (FRTS)*. With the introduction of Modular QoS CLI (MQC) framework the traffic shaping is usually configured within individual traffic classes with the **shape** configuration command.

The **shape** command allows you to specify average or peak traffic rate, adaptive Frame Relay traffic shaping and even voice-sensitive Frame Relay traffic shaping. Most variants of the **shape** command allow you to specify token bucket parameters (Bc and Be) in addition to the desired traffic rate.

All traffic shaping mechanisms use identical technology, they differ in their traffic classification capabilities (GTS uses IP access lists, FRTS uses Frame Relay virtual circuits) and underlying queuing structures (GTS uses Weighted Fair Queuing, whereas FRTS uses custom- or priority queuing). MQC offers the most versatile configuration model; it gives you very fine control over traffic classification and queuing mechanisms.

## Traffic Shaping Mechanisms

Cisco IOS shapes outbound traffic using the following steps:

-   If shaping is not yet active (forwarded traffic has not exceeded the traffic contract), the traffic is measured with a [token bucket algorithm](/kb/tag/QoS/QoS_Policing/). If a packet exceeds the token bucket capacity, it’s queued in the shaping queue structures (activating the shaping mechanism).
-   If shaping is active (the shaping queues are not empty), forwarded traffic is not measured but queued directly into the shaping queues.
-   Every *Tc*, the router removes up to *Bc* packets (or bytes) from the shaping queues and re-queues them into the interface queue.

{{<note info>}}There is no inbound traffic shaping on Cisco IOS{{</note>}}

The complete algorithm is illustrated in the following diagram:

{{<figure src="/kb/tag/QoS/Shaping_Mechanism.png" caption="Traffic shaping mechanisms in Cisco IOS">}}

{{<note note>}}The *Bc* and *Be* parameters can be specified in the **shape** command. If you don't specify them, Cisco IOS selects reasonable values. *Tc* is always computed from the shaping rate and *Bc*.{{</note>}}

### Implications of Traffic Shaping Mechanism

The traffic shaping mechanism used by Cisco IOS has the following side effects:

-   The packets in the shaped class are not delayed unless they exceed the traffic contract (more than Bc bytes in Tc period).
-   Once the traffic contract is exceeded, all subsequent traffic in the same class is shaped until the shaping queues are empty.
-   Relatively large amount of data is simultaneously dequeued from the shaping queues every Tc and sent as a single packet burst. These bursts might interfere with the traffic from other QoS classes in the interface output queue.

The secondary queue structure introduced by the traffic shaping mechanism works as follows:

-   Packets delayed by the shaping mechanism are entered into the shaping queue according to its queuing policy.

{{<note note>}}The shaping queues use per-flow weighted fair queuing unless you change the queuing structure of the shaped traffic with the hierarchical **service-policy**.{{</note>}}

-   The packets dequeued from the shaping queue (or packets transparently passed without being delayed) are queued in the interface output queue according to the **bandwidth** or **fair-queue** parameter of the shaped class.

{{<note warn>}}If you expect interface output queue congestion, make sure you assign enough bandwidth to the shaped traffic with the **bandwidth** command. The bandwidth assigned to the shaped class should be equal to the shaping rate.{{</note>}}

<!-- Source of diagrams: Wiki/Archive/QoS Mechanisms in Cisco IOS and Wiki/ipSpace/Articles and Blogs Diagrams (2020) -->

