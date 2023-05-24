title: FIFO Queuing

Without any QoS-related interface configuration, Cisco IOS uses [fair queuing](Fair_Queuing.html) on low-speed interface (up to a few megabits) and FIFO queuing on higher-speed interfaces. Fair queuing is also used whenever a **service-policy** using a queuing action (**bandwidth**, **priority** or **fair-queue**) is applied to an interface. The actual queuing mechanism can be inspected with the **show queueing interface *name*** command.

With no QoS configuration, serial interfaces on ISR routers (2811 was used to generate the printouts) use fair queuing and the Fast Ethernet interfaces use FIFO queuing. Expect defaults to vary across router platforms.

```
a1#show queueing interface serial 0/1/0
Interface Serial0/1/0 queueing strategy: fair
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 212296
  Queueing strategy: weighted fair
  Output queue: 0/20/64/212295 (size/max total/threshold/drops)
     Conversations  0/149/256 (active/max active/max total)
     Reserved Conversations 0/0 (allocated/max allocated)
     Available Bandwidth 1158 kilobits/sec


a1#show queueing interface fast 0/0
Interface FastEthernet0/0 queueing strategy: none
```
CAPTION: Default queuing policy on LAN and WAN interfaces

The default value of the **tx-ring-limit** on the serial interfaces of a 2811 router is 2 packets:

```
a1#show controller serial 0/1/0 | include tx_limit
tx_limited = 1(2), errata19 count1 - 0, count2 - 0
```
CAPTION: Inspecting the transmit ring size of an output interface

However, if the fair queuing is disabled on the serial interface with the **no fair-queue** interface configuration command, the tx-ring-limit is set to 128 (indicating that the packets forwarded to the interface are enqueued directly into the hardware output queue):

```
a1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
a1(config)#interface serial 0/1/0
a1(config-if)#no fair-queue
a1(config-if)#^Z
a1#show queueing interface serial 0/1/0
Interface Serial0/1/0 queueing strategy: none
a1#show controller serial 0/1/0 | include tx_limit
tx_limited = 0(128), errata19 count1 - 0, count2 - 0
```
CAPTION: FIFO queuing sets tx-ring size to maximum size supported by hardware

The actual size of the output queue is set by the **hold-queue out** interface configuration parameter. In the following printout, the output FIFO queue was set to 20 packets and a UDP packet flood was started to saturate the output queue:

```
a1#show running interface serial 0/1/0
Building configuration...

Current configuration : 141 bytes
!
interface Serial0/1/0
 ip address 172.16.1.129 255.255.255.252
 encapsulation ppp
 no fair-queue
 hold-queue 20 out
end

a1#show interface serial 0/1/0
Serial0/1/0 is up, line protocol is up
  Hardware is GT96K Serial
  Internet address is 172.16.1.129 255.255.255.252
  MTU 1500 bytes, BW 1544 Kbit, DLY 20000 usec,
     reliability 255/255, txload 42/255, rxload 1/255
  Encapsulation PPP, LCP Open
  Open: IPCP, CDPCP, loopback not set
  Keepalive set (10 sec)
  CRC checking enabled
  Last input 00:00:57, output 00:00:02, output hang never
  Last clearing of "show interface" counters 01:28:07
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 213395
  Queueing strategy: fifo
  Output queue: 20/20 (size/max)
  30 second input rate 0 bits/sec, 0 packets/sec
  30 second output rate 341000 bits/sec, 43 packets/sec
     1120 packets input, 44232 bytes, 0 no buffer
     Received 0 broadcasts, 0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort
     1415160 packets output, 464661604 bytes, 0 underruns
     0 output errors, 0 collisions, 5 interface resets
     0 output buffer failures, 0 output buffers swapped out
     6 carrier transitions
```
CAPTION: Packets are dropped when the output queue size reaches 20 packets

<!-- no diagrams -->
