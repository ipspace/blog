---
title: "Multi-Threaded Routing Daemons"
date: 2021-11-23 07:46:00
lastmod: 2021-11-26 15:35:00
tags: [ IP routing ]
---
When I wrote the _[Why Does Internet Keep Breaking?](/2021/11/internet-keeps-breaking.html)_ blog post a few weeks ago, I claimed that FRR still uses single-threaded routing daemons (after a too-cursory read of their documentation).

[Donald Sharp](https://www.linkedin.com/in/donaldsharp/) and [Quentin Young](https://github.com/qlyoung) politely told me ~~I was an idiot~~ I should get my facts straight, I removed the offending part of the blog post, promised to write another one going into the details, and Quentin improved the documentation in the meantime, so here we are...
<!--more-->
### Why Does It Matter?

In a word[^13]: sanity, performance and responsiveness.

[^13]: Three to be precise, or is it four, but who's counting.

Networking engineers love to build artisanal wheels, and routing protocol designers are no better. Every routing protocol has a bespoke implementation of the same three major functionalities:

* **Deal with neighbors**: discover them, keep them happy, and figure out when one of them keeps quiet for too long.
* **Deal with updates**: receive them, acknowledge them (when the protocol designer thought he could [do better than TCP](/2020/11/ospf-not-using-tcp.html)), send new information out, and retransmit it if needed (yet again, only for people who think TCP sucks)[^DV]
* **Deal with changes**: Update internal topology information based on received updates, calculate new routing tables, push new stuff into routing table to compete with other stuff.

[^DV]: The second half of this functionality might be tightly coupled with the next bullet, in which case we're talking about a *distance vector* protocol.

Does it make sense to do all three things in a single monolithic blob of code? Sure it does if you think juggling is a great pastime. Everyone else tries to stay sane by decoupling things into smaller bits that can be executed independently, and according to JeffT (see comment below) most modern routing protocol stacks are implemented that way[^ORNOT].

[^ORNOT]: ... or not. Facebook [published a conference paper in early 2021](https://research.fb.com/wp-content/uploads/2021/03/Running-BGP-in-Data-Centers-at-Scale_final.pdf) in which they proudly compared their multi-threaded custom-built BGP implementation with single-threaded Bird or Quagga. Bird is (AFAIK) still one of the most popular IXP route server implementation.

For the sake of completeness: Cisco IOS programmers figured that out decades ago. For example, Cisco IOS OSPF implementation uses two processes per routing protocol: a *hello* process and a *router* process:

{{<cc>}}Multiple OSPF-related processes are running on a Cisco IOS box with a single OSPF routing process{{</cc>}}
```
s1#show ip protocols summary
Index Process Name
0     connected
1     static
2     application
3     ospf 1

s1#show processes | include OSPF
 224 Mwe  2D2CE17           23        285      80 8956/12000  0 OSPF-1 Router
 228 Mwe  2D30EB5           15        288      52 9044/12000  0 OSPF-1 Hello
```

### Processes or Threads?

The Cisco IOS printout talks about *processes*, FRR documentation talks about *threads*. What's the difference?

Here's a [sweet-and-short answer I found on (where else) StackOverflow](https://stackoverflow.com/questions/200469/what-is-the-difference-between-a-process-and-a-thread):

> The typical difference is that threads (of the same process) run in a shared memory space, while processes run in separate memory spaces.

From that perspective, Cisco IOS processes are really threads as Cisco IOS does not have inter-process isolation[^IOS-1].

The only correct answer to "_when should one use threads instead of processes_" is "_it depends_", or we could keep going for hours. To make a long story short: whenever independent bits of code share sockets (including TCP sessions) or memory structures, it's easier to say "_who cares about memory isolation_" and use threads.

[^IOS-1]: I'm positive generations of TAC engineers and software developers loved the fun-to-squash bugs you get that way.

### Responsiveness?

Now that I mentioned Cisco IOS, I have to add another bit of trivia: Cisco IOS is a *non-preemptive* (or *run-to-completion*) operating system. As long as one process keeps running, nobody else can jump in to get something done (like sending a badly needed HELLO message)[^HOG].

[^HOG]: And if the offending process doesn't give up in a reasonable time, you get the much-admired CPUHOG syslog message.

Modern operating systems like Linux can do better. Processes or threads can be interrupted or ran *in parallel* on multiple CPU cores or sockets, which means that a *keeping neighbors happy* thread can keep sending HELLO messages or BGP keepalives while the *updating the BGP table* thread scratches its head trying to figure out what to do with another half a million updates that just came in.

{{<note info>}}The benefits of being able to jump it at any time and get a small job done are even higher once we start talking about almost-real-time stuff like BFD... and yes, I'm aware that high-end platforms offloaded BFD to linecard CPUs or hardware. Replace BFD with any other time-critical control-plane protocol of your choice.{{</note>}}

Coming back to FRR: according to [process architecture documentation](http://docs.frrouting.org/projects/dev-guide/en/latest/process-architecture.html), they split BGP functionality into three threads: an I/O thread, a keepalive processing thread, and a _rest of the stuff_ thread.

Other BGP implementations use even more threads, see for example  [IOS XR BGP threads](http://ciscoiosxr.blogspot.com/2012/02/threads-cisco-ios-xr-kernel.html).

### Performance!

I mentioned that you could use threads to increase performance when you happen to have too many CPU cores. For example, you could have multiple threads processing incoming BGP updates in parallel, and another bunch of threads building outgoing updates.

Whenever you want to increase the performance of a software solution with a scale-out threading architecture you have to split the problem you're facing into smaller (hopefully independent[^LOCK]) *shards*[^THARD]. There are at least three solutions real-life BGP routing daemons use[^BGPONLY]:

[^LOCK]: If the shards you're working on aren't independent enough, you'll spend a lot of time locking the data structures and waiting for other threads to unlock them, effectively wasting CPU cycles on synchronization activities.

[^BGPONLY]: We'll focus on BGP; most other routing protocols are trivial (performance-wise) compared to what we're throwing at BGP. For example, you don't have to build outgoing updates in OSPF or IS-IS, all you have to do is to flood what came in.

[^THARD]: That tends to be a really hard problem unless you started with a routing protocol specifications and an architecture that considered scalability. I'm also positive that anyone taking a monolithic routing daemon and implementing multi-threading on top of that code would get some really nice bugs on the first try.

* **Per-neighbor thread** handling all neighbor-related I/O operations. [RustyBGP took that approach](https://twitter.com/plajjan/status/1255267401639383042) resulting in [phenomenal performance](https://elegantnetwork.github.io/posts/bgp-perf5-1000-internet-neighbors/) in an environment with many neighbors (as compared to other open-source BGP stacks). [IOS XR Distributed BGP](https://www.cisco.com/c/en/us/td/docs/routers/xr12000/software/xr12k_r4-1/routing/configuration/guide/routing_cg41xr12k_chapter1.html#con_1721889) goes a bit further, performing as much work as feasible (down to MED comparison) within the speaker threads.
* **Per address family thread**. BGP tables of individual address families are totally independent from each other apart from next-hop references between VPN address families (VPNv4/VPNv6/EVPN) and IPv4 unicast address family. Having a thread per address family is thus a (conceptual) no-brainer[^AF]. Cisco IOS XR uses this approach in their [Distributed BGP](https://www.cisco.com/c/en/us/td/docs/routers/xr12000/software/xr12k_r4-1/routing/configuration/guide/routing_cg41xr12k_chapter1.html#con_1721889) implementation.
* **RIB sharding**. Numerous threads are run in parallel on smaller chunks of BGP RIB. Junos release 19.4R1 introduced RIB sharing together with *update threading* (packing outgoing BGP updates in parallel threads). To learn more, read the *[Deploying BGP RIB Sharding and Update Threading](https://www.juniper.net/documentation/en_US/day-one-books/DO_BGPSharding.pdf)* Day One book -- chapter 1 does a great job of explaining the concepts.

[^AF]: There's probably a large gap between theory and practice.

Interestingly, it looks like the scale-out BGP daemons were implemented primarily in high-end routers used to run the Internet core, but not in data center switches[^BGP].

There might be no need for high BGP performance in data center switches considering the forwarding table sizes in merchant silicon ASICs... although I do wonder how long it takes to bring up a new BGP session in large-scale EVPN deployments considering how many vendors [insist on running BGP sessions with EVPN address family between loopback interfaces](/2020/02/the-evpnbgp-saga-continues.html).

Another reason could be the underlying hardware -- I have a feeling that the data center switches still get the cheapest reasonable CPU the vendor can buy, in which case it would make no sense to optimize a routing daemon for many-core performance.

[^BGP]: ... even though some data center pundits think BGP is the answer regardless of what the question is.

[^EVPN]: I wonder 

### Revision History

2021-11-26
: Totally rewrote the *Performance* section

2021-11-24
: * Added a pointer to IOS XR threads (HT: [Kristian Larsson](https://twitter.com/plajjan/status/1463455078900240386))
: * Added a pointer to thread-per-neighbor RustyBGP implementation (HT: [Kristian Larsson](https://twitter.com/plajjan/status/1463454631519035396))
: * Added a pointer to Junos RIB sharing (HT: [Adam Chappell](https://twitter.com/packetsource/status/1463442786158530566))
: * Added a bit of a discussion on the viability of non-multi-threaded routing protocol implementations (based on comment from JeffT and the Facebook paper mentioned by Mario).
: * Added a "BFD can be offloaded" remark for Twitter pedants who found this blog post outdated because of that omission.
: * Reworded the last paragraph a bit because _it painted a pessimistic view of multi-thread/multi-code_. Can't do more than what I did; sometimes the reality isn't bright and shiny.
