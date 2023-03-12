---
date: 2018-01-09 09:42:00+01:00
tags:
- automation
- intent-based networking
- SDN
- BGP
title: 'BGP Route Selection: a Failure of Intent-Based Networking'
url: /2018/01/bgp-route-selection-failure-of-intent.html
intent-based-networking_tag: drawback
---
It's interesting how the same pundits who loudly complain about the complexities of BGP (and how it will be dead any time soon and replaced by an SDN miracle) also praise the beauties of [intent-based networking](https://blog.ipspace.net/2017/09/intent-based-hype.html)... without realizing that the hated BGP route selection process represents one of the first failures of intent-based approach to networking.

Let's start with some definitions. There are two ways to get a job done by someone else:
<!--more-->
-   You tell them **how** to do the job (algorithmic or imperative approach)
-   You tell them **what** should be done but not **how** to do it (declarative approach). Marketers love to call this **intent-based** approach.

Now think about any routing protocol implementation. Do you tell a router **how** to get the job done or do you configure **what** should be done, for example:

-   On which interfaces should a routing protocol work
-   Which interfaces are better or more preferred than others
-   Which prefixes should it advertise
-   Which prefixes should be summarized

Got it? Routing protocols were an early implementation of intent-based paradigm... but of course the marketers touting the benefits of intent-based gizmos don't want to hear that because they're telling you at the same time how much routing protocols suck.

Now imagine that you don't like the results of a routing protocol. You can't change the route selection algorithm, but you can tweak your intent, and hope that the results will be what you want them to be. There are people who tweak IGP costs to push the traffic the right way, and Cariden made a significant business out of tools that predicted how changes in costs would affect traffic flow. They even calculated the optimal link costs for your network based on the network topology and traffic matrix.

{{<note>}}I briefly mentioned Cariden in [SDN Use Cases](http://www.ipspace.net/SDN_Use_Cases) webinar. I also wanted to do a deep-dive podcast with them, but unfortunately they got acquired before we managed to schedule the recording.{{</note>}}

Things are simple in the IGP land because we have simple goals:

-   Survive failures;
-   Keep things relatively stable;
-   Spread the load across the whole infrastructure;

Now imagine business rules, commercial preferences, and contractual limitations entering the picture. Welcome to the problem BGP is trying to solve.

In an environment that would [define the problem before trying to solve it](https://lamport.azurewebsites.net/pubs/state-the-problem.pdf), the final solution would probably include a centralized controller where you'd implement business-driven decisions in your own custom path selection logic, and use simple local versions of that same algorithm as a fallback plan in case of central controller failure.

{{<note>}}There are probably people doing exactly that, and I would love to hear from them. Most of the great ideas you get in networking have already been implemented by someone... it's just that they're not bragging about what they're doing in Something-Open-Something-Something conferences.{{</note>}}

Guess what -- almost nobody wanted to go down that path (assuming they did the homework and realized what would need to be done), because it's a messy business, and really hard to get right. Everyone wanted the networking vendors to tweak their code to solve business problems one-at-a-time (without ever getting the whole picture) with tweaks to **intent-driven data model**. That's how we got:

-   Weights (I want to influence how a box does route selection)
-   Local preference (I want to influence route selection within my system)
-   MED (I want to influence how others send traffic to me)
-   Communities (I want to influence others but can't use any other tool, so let's hope they interpret my intent correctly)
-   Lists of communities to use (this is how you can signal your intent in a way that I'll understand it)
-   Weird rules about route reflector attributes affecting route selection (because it's always possible to [build a broken network](https://blog.ipspace.net/2013/10/can-bgp-route-reflectors-really.html) and then claim it's the vendor- or protocol fault)
-   Crazy stuff like copying IGP metric into BGP extended community because we want to have some more tweaks on intent without having to deal with writing the code ourselves.

In my biased view (because I don't believe in fairy tales and magic), BGP is a pretty obvious lesson in what happens when you try to solve vague business rules with intent-driven approach instead of writing your own code that does what you want to be done.

It will be great fun to watch how the next generation of intent-based solutions will fare. I haven't seen anyone beating laws of physics or RFC 1925 Rule 11 yet.

Need more (cynical) details on the intent-based hype spreading through the networking industry? You'll find them in [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.

