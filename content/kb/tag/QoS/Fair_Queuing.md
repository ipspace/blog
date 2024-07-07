---
kb_section: QoS
minimal_sidebar: true
pre_scroll: true
title: Fair Queuing in Cisco IOS
url: /kb/tag/QoS/Fair_Queuing/
---
Fair queuing is enabled by default on all low-speed interfaces on Cisco IOS devices (high-speed interfaces use FIFO queuing as the default mechanism). It's also used to implement the queuing actions (**bandwidth** and **fair-queue**) offered by the Modular QoS CLI (MQC).

The default queuing mechanism on a LAN interface of a Cisco 2811 router (the platform used to generate the following printouts) is thus [FIFO queuing](FIFO_Queuing.html). However, as soon as a simple queuing policy is applied to the interface with the **service-policy** interface configuration command, the queuing mechanism changes to fair queuing.

{{<cc>}}Service policy is configured on an Ethernet interface{{</cc>}}
```
a1#show run | section Simple|Fast
policy-map Simple
 class class-default
  bandwidth 20000
interface FastEthernet0/0
 ip address 10.0.0.5 255.255.255.0
 service-policy output Simple
```

{{<cc>}}Interface queuing strategy is changed to fair queuing{{</cc>}}
```
a1#show queueing interface FastEthernet 0/0
Interface FastEthernet0/0 queueing strategy: fair
  Input queue: 0/75/55887/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: Class-based queueing
  Output queue: 0/1000/64/0 (size/max total/threshold/drops)
     Conversations  0/1/256 (active/max active/max total)
     Reserved Conversations 1/1 (allocated/max allocated)
     Available Bandwidth 55000 kilobits/sec
```

If the **policy-map** applied as an outbound service policy does not include queuing actions, the interface queuing model reverts back to the default (FIFO for high-speed interfaces, fair queuing for low-speed ones).

{{<cc>}}Policing-only service policy applied to LAN interface{{</cc>}}
```
a1#show run | section Simple|Fast
policy-map Simple
 class class-default
  police rate 50000000 bps
    exceed-action drop
interface FastEthernet0/0
 ip address 10.0.0.5 255.255.255.0
 service-policy output Simple
```

{{<cc>}}Policing requires no software queueing strategy{{</cc>}}
```
a1#show queueing interface FastEthernet 0/0
Interface FastEthernet0/0 queueing strategy: none
```

You could also combine non-queuing service policies with the **fair-queue** interface configuration command to change the default interface queuing mechanism.

{{<cc>}}Combine fair queueing with a policing service policy{{</cc>}}
```
interface FastEthernet0/0
 fair-queue
 service-policy output Simple
```

{{<cc>}}Service policy contains no queuing actions{{</cc>}}
```
a1#show policy-map interface FastEthernet 0/0
 FastEthernet0/0

  Service-policy output: Simple

    Class-map: class-default (match-any)
      576 packets, 40292 bytes
      5 minute offered rate 0 bps, drop rate 0 bps
      Match: any
      police:
          rate 50000000 bps, burst 1562500 bytes
        conformed 0 packets, 0 bytes; actions:
          transmit
        exceeded 0 packets, 0 bytes; actions:
          drop
        conformed 0 bps, exceed 0 bps
```

{{<cc>}}Fair queuing is used even though the service policy doesn't require it{{</cc>}}
```
a1#show queueing interface FastEthernet 0/0
Interface FastEthernet0/0 queueing strategy: fair
  Input queue: 0/75/55887/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: weighted fair
  Output queue: 0/1000/64/0 (size/max total/threshold/drops)
     Conversations  0/1/256 (active/max active/max total)
     Reserved Conversations 0/0 (allocated/max allocated)
     Available Bandwidth 75000 kilobits/sec
```

<!-- no diagrams -->
 