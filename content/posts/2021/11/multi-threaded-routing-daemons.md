---
title: "Correction: Multi-Threaded Routing Daemons"
date: 2021-11-23 07:46:00
tags: [ IP routing ]
---
When I wrote the _[Why Does Internet Keep Breaking?](https://blog.ipspace.net/2021/11/internet-keeps-breaking.html)_ blog post a few weeks ago, I claimed that FRR still uses single-threaded routing daemons (after a too-cursory read of their documentation).

[Donald Sharp](https://www.linkedin.com/in/donaldsharp/) and [Quentin Young](https://github.com/qlyoung) politely told me ~~I was an idiot~~ I should get my facts straight, I removed the offending part of the blog post, promised to write another one going into the details, and Quentin improved the documentation in the meantime, so here we are...
<!--more-->
### Why Does It Matter?

In a word[^13]: sanity, performance and responsiveness.

[^13]: Three to be precise, or is it four, but who's counting.

Networking engineers love to build artisanal wheels, and routing protocol designers are no better. Every routing protocol has a bespoke implementation of the same three major functionalities:

* **Deal with neighbor**: discover them, keep them happy, and figure out when one of them keeps quiet for too long.
* **Deal with updates**: receive them, acknowledge them (when the protocol designer thought he could do better than TCP), send new information out, and retransmit it if needed (yet again, only for people who think TCP sucks)[^DV]
* **Deal with changes**: Update internal topology information based on received updates, calculate new routing tables, push new stuff into routing table to compete with other stuff.

[^DV]: The second half of this functionality might be tightly coupled with the next bullet, in which case we're talking about a *distance vector* protocol.

Does it make sense to do all three things in a single monolithic blob of code? Sure it does if you think juggling is a great pastime. Everyone else tries to stay sane by decoupling things into smaller bits that can be executed independently. 

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

Now that I mentioned Cisco IOS, I have to add another bit of trivia: Cisco IOS is a *non-preemptive* operating system. As long as one process keeps running, nobody else can jump in to get something done (like sending a badly needed HELLO message)[^HOG].

[^HOG]: And if the offending process doesn't give up in a reasonable time, you get the much-admired CPUHOG syslog message.

Modern operating systems like Linux can do better. Processes or threads can be interrupted or ran *in parallel* on multiple CPU cores or sockets, which means that a *keeping neighbors happy* thread can keep sending HELLO messages or BGP keepalives while the *updating the BGP table* thread scratches its head trying to figure out what to do with another half a million updates that just came in.

{{<note info>}}The benefits of being able to jump it at any time and get a small job done are even higher once we start talking about almost-real-time stuff like BFD.{{</note>}}

Coming back to FRR: according to [kernel threads documentation](http://docs.frrouting.org/projects/dev-guide/en/latest/process-architecture.html#kernel-thread-wrapper), they went way beyond the _neighbors + updates_ separation -- just look at how many threads in the **show thread cpu** printout have BGP in their name.

### Performance!

I mentioned that you could also use threads to increase performance when you happen to have too many CPU cores. For example, you could have multiple threads processing incoming BGP updates in parallel, and another bunch of threads building outgoing updates. I'm positive there would be a noticeable benefit in environments with dozens or hundreds of BGP neighbors[^THARD]. 

[^THARD]: I'm also positive that anyone taking a single-threaded BGP daemon and implementing this functionality on top of that code would get some really nice bugs on the first try.

However, assuming your code is not needlessly stuck waiting for I/O operations[^FIXCODE], parallel threads increase performance only when you can assign more CPU cores to the problem. While BGP route reflectors or BGP route servers running as VMs could experience increased performance, most hardware networking devices still ship with the cheapest CPU the vendor can buy, and those CPUs still don't have more than a few cores or hardware threads, so why bother.

[^FIXCODE]: ... in which case you REALLY SHOULD use parallel threads, or a [better event loop](https://en.wikipedia.org/wiki/Event_loop), or rearchitect your code
