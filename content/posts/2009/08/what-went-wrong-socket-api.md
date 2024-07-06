---
date: 2009-08-24 06:49:00.002000+02:00
tags:
- Internet
- networking fundamentals
title: 'What Went Wrong: the Socket API'
url: /2009/08/what-went-wrong-socket-api.html
---
You might think that the [lack of a decent session layer in the TCP/IP protocol suite](/2009/08/what-went-wrong-tcpip-lacks-session.html) is the main culprit for our reliance on IP multihoming and [related explosion of the IP routing tables](/2009/06/internet-anarchy-ill-advertise-whatever.html). Unfortunately, we have an even bigger problem: the [Berkeley Socket API](http://en.wikipedia.org/wiki/Berkeley_sockets), which is around 40 years old and used in almost all TCP/IP software implementations  and clients (including high-level scripting languages like PERL or Python).
<!--more-->
To establish a client-to-server connection using Socket API you have to perform these calls:

* Create a socket with the [*socket()*](http://en.wikipedia.org/wiki/Berkeley_sockets) call
* Convert a hostname into a L3 address (IPv4 or IPv6) with the [*getaddrinfo()*](http://en.wikipedia.org/wiki/Getaddrinfo) or (obsolete) [*gethostbyname()*](http://en.wikipedia.org/wiki/Berkeley_sockets) call.
* Connect to the remote L3 address with the [*connect()*](http://en.wikipedia.org/wiki/Berkeley_sockets) call.

The set of calls you have to perform is not surprising; Socket API is older than DNS. However, the reliance on IP addresses passed around inside the application and a total disconnect between name resolution and session establishment is a disaster.

Just to give you an example: you might have a server farm offering a service, and describe it in DNS with numerous A records for the same name (for example, *scs.msg.yahoo.com*). 

{{<cc>}}A sample DNS entry for scs.msg.yahoo.com on November 19th 2022{{</cc>}}
```
nslookup scs.msg.yahoo.com.
Server:		1.1.1.1
Address:	1.1.1.1#53

Non-authoritative answer:
scs.msg.yahoo.com	canonical name = vcs0.msg.g03.yahoodns.net.
Name:	vcs0.msg.g03.yahoodns.net
Address: 66.196.114.52
Name:	vcs0.msg.g03.yahoodns.net
Address: 66.196.114.76
Name:	vcs0.msg.g03.yahoodns.net
Address: 66.196.114.68
Name:	vcs0.msg.g03.yahoodns.net
Address: 66.196.114.97
Name:	vcs0.msg.g03.yahoodns.net
Address: 66.196.121.49
Name:	vcs0.msg.g03.yahoodns.net
Address: 66.196.120.52
Name:	vcs0.msg.g03.yahoodns.net
Address: 66.196.114.81
Name:	vcs0.msg.g03.yahoodns.net
Address: 66.196.121.40
```

The DNS entry for *scs.msg.yahoo.com* looks awesome, but doesn't help a bit unless the client application uses that information. In reality, most applications:

* Perform the *getaddrinfo()* call which returns the list of addresses (regardless of whether they are reachable or not) 
* Use the first address (or all of them in sequence) in the *connect()* call ([happy eyeballs](/2013/03/happy-eyeballs-happiness-defined-by.html) implementations are an obvious exception).

If the DNS lookup returned a temporarily unreachable IP address you're doomed.

Obviously you could reinvent happy eyeballs. You could make DNS calls yourself using the resolver library (or parse the information returned by *getaddrinfo()*), collect all IP addresses and try to connect to more than one of them. Web browsers usually do that quite well, or we would quickly stop using them.

You could even implement a connection-failure cache listing those addresses that were recently unreachable to speed up the future session setup process. But let's be realistic: how many application programmers do you know that really understand the intricacies of TCP/IP (let's lower the bar: how many of them could use the resolver library)? Most of them want to get their job done and end up using recipes from sources like [Network Programming with Perl](http://www.linuxjournal.com/article/3237).

{{<note>}}It looks like people writing Yahoo Messenger knew what they were doing; otherwise it wouldn't make sense to have numerous A records for their IM servers.{{</note>}}

The name-to-address mapping problem should have been abstracted into the OS kernel (or system library) decades ago (at the latest when DNS became widespread) and the applications should have been kept blissfully unaware of the complexities; the *connect()* call should accept a hostname and do the rest behind the scenes. Even Microsoft got that right with the NetBIOS API. But then, what could you expect: the Socket API is a direct mapping to the TCP/IP protocol stack (where DNS is just one of the applications). To make matters worse, it looks like we missed another opportunity to get networking API right -- according to Drew DeVault, [Plan9 operating system treated networking connections like files](https://drewdevault.com/2022/11/12/In-praise-of-Plan-9.html), but those ideas were never ported into Linux.

With the sorry state of the Socket API, the best you can do if your service is reachable through multiple IP addresses is to randomize the DNS responses (this will give you some limited load sharing), adjust the list of A records in the DNS responses based on server availability (while hoping that the intermediate DNS servers or the clients will not ignore the TTL settings in the DNS responses) ... and as the last resort make sure all the IP addresses are always reachable, which brings us back to where we've started: IP multihoming. You could also use a load balancer and a single (obviously multihomed) IP address.

### Revision History

2016-07-08
: gethostbyname is obsolete. Also added a reference to happy eyeballs which got popular after this blog post was written.

2022-11-19
: Added a pointer to Plan9 blog post, removed obsolete links, and polished the text a bit.
