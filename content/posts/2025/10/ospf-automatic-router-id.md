---
title: "OMG: Automatic OSPFv3 Router ID on Cisco IOS"
date: 2025-10-28 07:52:00+0100
tags: [ OSPF ]
ospf_tag: rant
---
Found this incredible gem[^NGD] hidden in the Usage Guidelines for the [OSPFv3 **router-id** configuration command](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6/command/ipv6-cr-book/ipv6-r1.html#wp4240068693) part of the [Cisco IOS IPv6 reference guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6/command/ipv6-cr-book/ipv6-r1.html).

The whole paragraph seems hallucinated[^SH], but that couldn't be because the page was supposedly last updated in 2019, and LLMs weren't good enough to write well-structured nonsense at that time:

[^SH]: I doubt anyone will bother fixing that old document, but just in case, I [took a screenshot](/2025/10/ospfv3-router-id.jpg) in October 2025.

[^NGD]: Proving yet again that the [vendor documentation quality](/2025/10/shoddy-documentation/) has been going down the drain for ages.

> OSPFv3 is backward-compatible with OSPF version 2.

No, it is not.
<!--more-->
> In OSPFv3 and OSPF version 2, the router uses the 32-bit IPv4 address to select the router ID for an OSPFv3 process.

Sort of, but let's not be picky. We have bigger fish to fry.

> If an IPv4 address exists when OSPFv3 is enabled on an interface, then that IPv4 address is used for the router ID.

Really? The writer couldn't check that with someone who passed a CCNP exam? The router ID is selected when the routing process is started, not when OSPFv3 is enabled on an interface. Furthermore, any IPv4 address can be used as the router ID, not just from interfaces that use OSPFv3.

> If more than one IPv4 address is available, a router ID is chosen using the same rules as for OSPF version 2.

That is one of the two correct sentences in the whole paragraph.

> If no IPv4 addresses are configured, the router selects a router ID automatically.

OMG, seriously? Where did this amazing discovery come from? Anyone with a bit of OSPF background should be furiously asking two questions at this point:

* How exactly does the router *automatically select* the router ID?
* How does it ensure the router ID is unique *before receiving the link state database from all its neighbors*?

No worries, though. The code is saner than the documentation. If you start OSPFv3 on a router with no IPv4 addresses and do not configure the **router-id**, the OSPFv3 process does not start (I [wrote about that](/2008/04/ipv4-forever/) in 2008). All you get is something like this:

```
r#show ipv6 ospf interface
%OSPFv3 1 address-family ipv6 not running, please configure a router-id
```

> Each router ID must be unique.

And this is the second correct sentence in that paragraph.

Now, the next time you ask your new LLM friend for an opinion, consider that companies like OpenAI train their models on (~~stolen~~ borrowed) content of this quality.