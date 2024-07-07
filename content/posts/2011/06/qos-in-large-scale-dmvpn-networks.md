---
date: 2011-06-14 07:10:00+02:00
dmvpn_tag: integrate
tags:
- DMVPN
- workshop
- QoS
title: QoS in Large-Scale DMVPN Networks
url: /2011/06/qos-in-large-scale-dmvpn-networks/
---
Got this question a few days ago:

> I have a large DMVPN network (\~ 1000 sites) using variety of DSL, cable modem, and wireless connections. In all of these cases the bandwidth is extremely dissimilar and even varies with time. How can I handle this in a scalable way?

Hub-to-spoke QoS implementations in DMVPN networks usually use one of the following options:
<!--more-->
**Per-spoke class with ACL-based classification**. If you want to implement per-spoke QoS on the hub router, you need a huge policy-map with a class for each spoke. However, as all DMVPN traffic exits the hub site through a single tunnel interface, ACL-based classification is the only mechanism you can use (QPPB won't work -- IOS supports only 100 QoS groups). Clearly not scalable and a nightmare to manage.

**Per-tunnel QoS**. The name of [this feature](http://www.cisco.com/en/US/docs/ios/sec_secure_connectivity/configuration/guide/sec_per_tunnel_qos.html) (described in my [New DMVPN features in IOS release 15.x](http://www.ipspace.net/DMVPN150) webinar) is highly misleading. It allows you to implement per-spoke QoS (maybe the developers had IPsec tunnels in mind) with the service policy being selected by the spoke router. You have to configure an NHRP group on the spoke router, the name of the group is sent to the hub router in the registration request and the hub router applies **policy-map** associated with the NHRP group to *all traffic sent to that spoke*.

**The answer to the reader's question**:

-   Define numerous policy maps on the hub router (each one with a different set of traffic shaping parameters matching the spoke bandwidth) and associate each one of them with a different NHRP group;
-   Measure the actual hub-to-spoke bandwidth;
-   Select the closest QoS policy and configure the corresponding NHRP group on the tunnel interface of the spoke router;
-   The NHRP group name will be sent to the hub router in the next registration request and the hub router will start using the new QoS policy for that spoke.
