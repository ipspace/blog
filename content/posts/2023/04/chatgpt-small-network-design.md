---
title: "Building a Small Network with ChatGPT"
date: 2023-04-13 07:25:00
tags: [ AI, design, OSPF ]
---
I must be a good *prompt engineer* -- every time I ask ChatGPT something really simple it spews out nonsense. This time I asked it to build a small network with four routers:

> I have a network with four Cisco routers (A,B,C,D). They are connected as follow: A-B, B-C, A-D, D-C. Each router has a loopback interface. Create router configurations that will result in A being able to reach loopback interfaces of all other routers.

Here's what I got back[^M31]:

> Here's an example configuration for the four routers that should allow Router A to reach the loopback interfaces of all other routers:
<!--more-->

[^M31]: ... on March 31st 2023. YMMV: ChatGPT claims it's continuously improving. For example, it realized Italy is not a constitutional monarchy during last two weeks of March.

Maybe it's just me, but I would expect an expert to ask a question or two first, like "_are there any particular IP address you'd like to use, or is it all the same to you_". Ignoring that bedside manners detail, let's inspect the configuration:

{{<cc>}}Router A{{</cc>}}
```
interface FastEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 duplex auto
 speed auto
!
interface Loopback0
 ip address 10.0.0.1 255.255.255.0
!
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.255 area 0
!
ip route 0.0.0.0 0.0.0.0 192.168.1.2
```

{{<cc>}}Router B{{</cc>}}
```
interface FastEthernet0/0
 ip address 192.168.1.2 255.255.255.0
 duplex auto
 speed auto
!
interface FastEthernet0/1
 ip address 192.168.2.1 255.255.255.0
 duplex auto
 speed auto
!
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
 network 192.168.2.0 0.0.0.255 area 0
!
ip route 0.0.0.0 0.0.0.0 192.168.2.2
```

{{<cc>}}Router C{{</cc>}}
```
interface FastEthernet0/0
 ip address 192.168.2.2 255.255.255.0
 duplex auto
 speed auto
!
interface Loopback0
 ip address 10.0.0.3 255.255.255.0
!
router ospf 1
 network 192.168.2.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.255 area 0
!
ip route 0.0.0.0 0.0.0.0 192.168.2.1
```

{{<cc>}}Router D{{</cc>}}
```
interface FastEthernet0/0
 ip address 192.168.3.1 255.255.255.0
 duplex auto
 speed auto
!
interface Loopback0
 ip address 10.0.0.2 255.255.255.0
!
router ospf 1
 network 192.168.3.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.255 area 0
!
ip route 0.0.0.0 0.0.0.0 192.168.3.2
```

ChatGPT also explained what it did, starting with:

> In this configuration, Router A is connected to Router B via FastEthernet0/0 **and to Router D via FastEthernet0/1**. It has a loopback interface with IP address 10.0.0.1.
> [...]

Figure out everything that's wrong with the above configurations before moving on ;)

How about:

* While ChatGPT mentioned the A ➔ D link, it's missing from the configuration of router A.
* Router D has a single interface that doesn't match anything else (because A ➔ D link is missing).
* Router B has no loopback interface, so it's impossible to reach it 🤔
* Loopback interfaces have overlapping subnets (they are configured as /24s not as /32s)

Then we have the chain of unnecessary static default routes: A ➔ B, B ➔ C, C ➔ B, D ➔ A?. Lovely ;)

### But Wait It Will Get Better!

Of course, it will. GPT-4 does a much better job (thanks again to Andrew Yourtchenko for running the query for me). Here's what it generated for Router A:

{{<figure src="/2023/04/gpt4-router-a.png">}}

It's a major improvement compared to what ChatGPT generated and pretty close to a perfect answer:

* All the required links are there
* Loopbacks have the expected subnet masks
* P2P links use smaller subnets
* OSPF is configured correctly, although not optimally.

Even what ChatGPT generated would be helpful if you take it with a grain of salt[^SS] as a starting point for a research project that would eventually result in a running network, but that's not how the AI cheerleaders are selling the GPT wonders.

[^SS]: ... or a salt shaker or two

Based on all I've seen so far _I cannot trust anything ChatGPT generates without validating it_, which means it could be an interesting absent-minded assistant[^BS], but I would still have to know what I'm doing.[^CCIE]

[^BS]: or a high-quality bullshit generator -- it does a wonderful job.

[^CCIE]: Note to CxO: it's too early to fire all those pesky CCIEs

Ignoring the ontological dilemmas[^LU], I don't believe it's possible to give reliably correct answers without _understanding_ what you're talking about. Large language models do a fantastic job extracting the meaning from a free-form query and generating a reply, but just because you consumed all the books in the world doesn't mean that you _know_ or _understand_ what they're all about. Don't believe me? Read a  graduate textbook about quantum physics and tell me how that worked out.

[^LU]: And our lack of understanding what *consciousness* and *intelligence* are.

One could also argue about the mysterious properties of _emergent behavior_ -- once a model is large and complex enough, it might exhibit unexpected behavior, like seemingly _understanding_ things. Does that remind you of how they told us OpenFlow would solve all networking problems?

**Takeaway:** As of March 2023, generic large language model is probably not the best tool to design networks and build network configurations. Let's see what the next week's model brings ;)