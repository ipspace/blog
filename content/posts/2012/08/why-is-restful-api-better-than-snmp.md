---
title: "Why is RESTful API better than SNMP?"
date: "2012-08-14T06:23:00.000+02:00"
tags: [ SNMP,SDN,network management ]
---
Brian Christopher Raaen asked a great question in a comment to my [*OpenStack/Quantum SDN-Based Virtual Networks*](/2012/08/openstackquantum-sdn-based-virtual/) post:

> Other than some syntax difference what do these new HTTP-based APIs add that SNMP couldn't already do?

**Short answer**: In theory nothing, apart from familiarity and convenient programming libraries. In practice, there's a huge gap between theory and practice. See "Hands-on experience" at the bottom of the article.
<!--more-->

{{<note>}}This post was edited and updated based on readers' comments in September 2020.{{</note>}}

### What is a RESTful service

If you’re not familiar with the concept of Representation State Transfer (REST) you might want to [read this Wikipedia entry](http://en.wikipedia.org/wiki/Representational_state_transfer) that describes REST as an architectural solution, not a specific protocol or data format.

The most interesting part of the article is the description of the [REST constraints](http://en.wikipedia.org/wiki/Representational_state_transfer#Constraints). A RESTful service should be a stateless client-server service – clearly SNMP fits that role well. It’s harder to shoehorn SNMP into other constraints (cacheable layered system), but these constraints aren’t that important in the network programming space.

Moving forward to the [guiding principles of a REST interface](http://en.wikipedia.org/wiki/Representational_state_transfer#Guiding_principles_of_the_interface), the differences with SNMP become more pronounced. SNMP requires an external schema (MIB) to describe the data model, whereas a REST interface should provide self-descriptive messages.

Finally, while you could (in principle) run a RESTful service over an [RFC 1149-based infrastructure](http://tools.ietf.org/html/rfc1149), most real-life implementations run over HTTP(S), reuse existing Web services authentication/authorization mechanisms (HTTP authentication or cookies), and use JSON or XML as the data transfer format.

### Why is REST better than SNMP?

Imagine you’re looking for someone to write detailed technical documentation for your new SDN gizmo. Would it be simpler to find someone fluent in English or in [Elbonian](http://en.wikipedia.org/wiki/Dilbert#Elbonia)?

The situation is no different in the programming world – anyone can write a client script that uses HTTP(S) to send form data to a web server and process JSON response (XML-based requests and responses might already represent significant mental challenges to some youngsters).

HTTP(S) client is usually included with modern programming languages and available (at least as a library) in every single language I’ve tried to use in the last decade (before you ask: there was no HTTP client in Turbo Pascal, PL/I or Fortran IV when I was still using them), and a lot more programmers were exposed to HTTP than to SNMP, some of them probably never realizing where the HTTP part of the [XMLHttpRequest object](http://en.wikipedia.org/wiki/XMLHttpRequest) comes from.

Amazingly, there’s an [SNMP library for PHP](http://php.net/manual/en/book.snmp.php) and [Ruby](http://snmplib.rubyforge.org) … or [you could use Erlang](http://www.erlang.org/doc/apps/snmp/index.html) (although I still can't figure out whether that's a joke as the manual was published on April 1st).

The situation is no different on the server side. You can implement a RESTful server in any programming language using any open-source web server, from [standalone PERL scripts](http://perldancer.org) and [lightweight options](http://www.lighttpd.net) to full-blown web servers. SNMPv3 server? Not so easy.

### Summary

I can’t see a major functional difference between a RESTful service and SNMP (but see below). Also, I can’t see where SNMP would be better than a RESTful interface now that we’re past the days of [Z80 processors](http://en.wikipedia.org/wiki/Zilog_Z80) being used in networking devices.

BTW, don’t tell me most SNMP MIBs are read-only. I’m well aware of that – but that’s not a limitation of the SNMP protocol, but of its implementations in specific network devices. [Wellfleet](http://en.wikipedia.org/wiki/Wellfleet_Communications) was more than happy to have their routers fully configurable through SNMP … unfortunately that was the only configuration mechanism they offered, and their SNMP-based CLI was a royal pain.

However, regardless of what our opinions might be, REST is clearly a mainstream solution and SNMP is limited to a very specific field. Which one do you think will be used more?

### Hands-On Experience

At the time this blog post was published, [John Gruber wrote a great reply to the original question](/2012/08/openstackquantum-sdn-based-virtual/#c1415977561055230319):

---

In scale, HTTP is quite a bit better than SNMP. RESTful APIs use HTTP GETs to retrieve data. SNMP is used extensively to retrieve stats data from devices. When the number of tenants retrieving stats from an infrastructure has to scale to the public, SNMP agents on various devices will indeed stress their control planes. Most embedded system control planes don't have an excess of CPU cycles to burn as it is. Nor do they have the intelligence for rate limiting or caching of management requests in scale.  
  
With HTTP we have a rich and well proven delivery and caching mechanism which can be used to impose appropriate limits simply by serving requests out of CHEAP and available application level RAM caches. HTTP delivery and rewrite proxies are available at a MUCH lower cost and point of entry than similar mechanism which use SNMP.  
  
Even for validating provisioning requests, using HTTP POST or PUT, verse SNMP sets, opens up a world of scripting and coding that SNMP doesn't support readily. Everyone can setup an HTTP rewrite and cache engine in half a dozen scripting languages. How many of us can say the same for SNMP?  
  
While SNMP is wonderful, it's not as accessible or as cheap to get working well as HTTP in our day and age. That's why we are all moving towards HTTP as an application level protocol and web based data structures, like JSON. Ask yourself how many of us thought HTTP would be the world's most popular transport for video 5 years ago? It is. It may not be as optimal for the job as RTP, but it has won the day. Viva La Web..  

---

Tristan Colgate-McFarlane added his thoughts in a comment copied into the main blog post for your convenience:

---

HTTP/REST is certainly easier in some respects, but SNMP does have quite a few advantages. It supports types, MIBs are an excellent source of documentation for an API and those APIs tend to be considerably more stable than their RESTful cousins (the RabbitMQ management plugin API has changed in every single version I've deployed and broken nagios checks every time). Many of these APIs are even standardised (and some vendors even stick to them sometimes). There are some missing things, like properly standardised floats and doubles.

Not to mention traps, a decent (if loathed) security model in v3, no TCP 3 way handshake (unless you want it). Stuff like EVENT-MIB and EXPRESSION-MIB give you standard server-side functionality. net-snmp does a pretty good job of doing most of the really hard stuff for you.

The real problem for SNMP is that it is something else to learn and doesn't work well if you stick to the bare minimum. Doing tables properly is hard (that's trivial in a XML or JSON based REST API). People don't even think about using things like contexts. MIBs are also scarily close to actually writing documentation, which is never going to go down well with the majority of developers. It hasn't helped that most examples of SNMP usage try and bypass MIBs completely and use numeric oids for everything which makes examples practically impossible to read and gives SNMP a scary, super complicated air about it. You can do without MIBs, but that doesn't mean you should, you can always replace the textual values with the OIDs once you've worked everything out.

I think SNMP's time may have come, but it has merits that we are losing with HTTP REST APIs, just not ones that people care about that much. How much they should care is open for debate.

---

Finally, in September 2020 Rich Smith described his experience with SNMP nightmares:

---

I know this article is very old by now, but as someone who spent many years working with SNMP, I strongly disagree with the conclusion. SNMP has one (possible) advantage over REST, which is that it is connectionless. After that, it is a horror show.

The biggest issue is probably the amount of space that OIDs consume in limited-size packets. GetBulk did not end up implementing any OID compression, and so when walking a table of counters, gauges, or states, for example, almost the entire, precious 1500 byte packet capacity is consumed transporting OIDs. In the real world, packet fragmentation and reassembly does not work well, and so you have to carefully craft your request packets to avoid size overruns in responses.

The only traversal semantic is SNMP is GetNext/GetBulk. There is no filtering, that I am aware of, and scoping is only available by specifying more of the OID prefix, which is limiting.

Table walk semantics are difficult to implement correctly for sparse tables. Even if you implement that correctly, you have to be careful which other columns your GetBulk runs over into at the end of the table. We had a case where the last row of a table could never be fetched due to running over into an unrelated table with a too-large OCTET STRING. We had to create a custom table-walk algorithm for that specific table.

Because many agents are single-threaded, you have to implement throttling on the management side to avoid spurious timeouts and retries. (Without throttling, requests queue up in the agent, including retries, and everything times out.)

CRUD semantics for tables are difficult to implement correctly. At my last job, we almost got sued by a customer because one out of a sequence of SetRequest packets failed, and left a wide-open WLAN on their network. Since SetRequest is not idempotent, you cannot even retry those.

There are other parts of the protocol I could pick on, such as community strings for authentication, or OID index parsing, or the difficult-to-use InetAddress/InetAddressType data types. There is a lot that did not age well.

Another commenter stated that SNMP is a terrible protocol that needs to die. I don't know if I'd go that far, but for managing a device of any complexity, it is so much better to implement a REST API. You have reliability and the ability to stream large amounts of data, if needed. Scoping and filtering are available via URLs and query parameters. JSON encoding is not even much more verbose than all of the SNMP OIDs that come back in GetBulk. When you ask for a table of data, you don't get unrelated tables. You don't have to implement "sparse walk".

REST APIs also allow for various authentication schemes that HTTP supports. TLS is supported simply.

There are dozens of open source libraries and frameworks for HTTPS, REST, and JSON.

REST is just superior. Anyone who says "SNMP can do anything that REST does" has, I would wager, never spent much time maintaining a sophisticated SNMP-based management application. I have done that, and I guarantee that the statement that the two protocols are equivalent is naive.

---

Also, you might enjoy dozens of comments that accumulated since   the original blog post was published in 2012.
