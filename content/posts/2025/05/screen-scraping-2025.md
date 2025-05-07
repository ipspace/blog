---
title: "Screen Scraping in 2025"
date: 2025-05-07 11:32:00+0200
tags: [ automation ]
series: cli
cli_tag: challenge
---
[Dr. Tony Przygienda](https://www.linkedin.com/in/dr-tony-przygienda-018501/) left a [very valid (off-topic) comment](https://blog.ipspace.net/2025/04/api-data-model-contract/#2619) to my [Breaking APIs or Data Models Is a Cardinal Sin](/2025/04/api-data-model-contract/#2619) blog post:

> If, on the other hand, the customers would not camp for literally tens of years on regex scripts scraping screens, lots of stuff could progress much faster.

He's right, particularly from Juniper's perspective; they were the first vendor to use a [data-driven approach to **show** commands](https://blog.ipspace.net/2017/12/how-did-netconf-start-on-software-gone/). Unfortunately, we're still not living in a perfect world:
<!--more-->
* Even the best vendors sometimes slip and create a **show** command that cannot produce JSON or XML output (because it's faster to sprinkle **printf** statements throughout the code than doing the right thing). In those cases, [screen scraping](https://blog.ipspace.net/kb/CiscoAutomation/050-scraping/) (collecting the results of a **show** command and trying to extract interesting bits of data from them) is the only way to go.
* Many vendors added JSON/XML output as an afterthought, and numerous **show** commands still cannot generate outputs in one of those formats.
* There are still vendors that haven't gotten the "_JSON is the new SNMP_" memo ;)

If you have to implement screen scraping for some devices, you might decide to do it for everything you have to work with as the least common denominator (and the least amount of headache).

However, let's be positive and assume we want to _Do the Right Thing_ (as opposed to _Getting the Job Done and Having a Beer_). Some devices can generate structured data in JSON or XML format, others support only JSON or only XML, and some can convert from internal XML representation into JSON with [side effects](https://blog.ipspace.net/2021/01/fixing-xml-json-challenges/) that border on hilarious (unless you have to deal with them).

Structured data is great; every bit of data is properly named/tagged. It's also bloated. A friend of mine once told me that fetching 100K routes from a device results in 4MB of text, a 100 MB JSON object, or a 500 MB XML object. Parsing a 500 MB XML object might take a bit longer than screen-scraping the text printout.

Speaking of XML: working with XML is a nightmare because you never know whether you're dealing with lists or dictionaries, and it gets way worse when namespaces are involved. Compare that with **json.load** call that you need to get JSON data into a usable data structure. Nobody in their right mind wants to touch XML (unless there is no other option), and finding a programmer who can deal with XML in Python is probably as easy as finding a COBOL programmer.

Working with large JSON objects is no walk in the park, either. Parsing the 100 MB JSON object mentioned above will take a while and result in a data structure that's at least as large. As anyone who ever had to parse a 500 MB XML object knows, there's the Right Way of parsing large objects: use a generic JSON/XML parser as a framework and use callbacks/hooks to collect/analyze/store data on the fly (as they're parsed) without ever generating the final data structure. Unfortunately, that's not a very common skill either. Most programmers were never forced to look beyond **json.load**.

Let's ignore the details and assume we got the structured data parsed somehow. Now we must navigate those data structures, and things quickly become as "easy" as navigating SNMP MIBs (or reading a James Joyce novel). Here's what I had to deal with to find out if my device had BFD running for a BGP session:

```
vrfs.default.ipv4Neighbors["10.1.0.1"].peers.Ethernet1.types.normal.peerStats["10.1.0.2"].status == "up"
```

Not good enough? Go play with Nexus OS, where every single interesting bit of information is prefixed by something like:

```
TABLE_vrf.ROW_vrf.TABLE_addrf.ROW_addrf.TABLE_prefix.ROW_prefix
```

Finally, there's the whole morass of *what is in that structured data*. Everyone will gladly tell you which IETF YANG models their boxes support, while forgetting to mention that you cannot get all the information you need from the standardized models[^ESM] and that even the augmented data model does not contain everything you can get with a **show** command.

[^ESM]: Remember the days of enterprise SNMP MIBs? We reinvented them in the brave new YANG/XML/JSON world (and renamed them to *augmentation*), yet again proving the infinite wisdom of RFC 1925 rule 11.

OK, so let's forget the standardized data models and be happy that the devices we work with can produce some structured data... if only we know how to fetch them. Everyone seems to support some variant of the **show X | format json** command that sends you the desired results in a structured format over an SSH session. There's just a tiny little gotcha: at least one vendor forgot to do control-plane prioritization for SSH data. Fetching a large routing table can kill LACP sessions.

Back to the drawing board: we'll have to use the management API our vendor decided to embrace. Some use NETCONF, others use REST API, and while NETCONF is pretty standard (but uses XML; see above), vendor-specific REST API could be anything. However, most vendors implemented NETCONF over SSH (while the rest of the world uses HTTP-based API) because the SSH hammer was conveniently close, and while there's a Python [ncclient library](https://github.com/ncclient/ncclient) you can use to implement a NETCONF client, you won't find many Python programmers who know how to use it. Oh, and do I have to mention that some vendors happily provide results of **show** commands via NETCONF as an XML-encapsulated text string?

With all that being said, do you still wonder why some people stubbornly use screen scraping in 2025? As a final nail in this coffin, let's add insult to injury: I encountered at least one vendor (and heard of another one) that made breaking changes in their structured data while keeping the text printout mostly intact.

It's easy to go to a World Congress and solve all the networking problems with PowerPoint. The real world is much messier, and every (supposed) attempt to make it more ordered usually ends up wasting energy and generating more entropy (see also: [how standards proliferate](https://xkcd.com/927/)).
