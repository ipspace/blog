---
date: 2021-01-21 07:28:00+00:00
series:
- RPKI
tags:
- BGP
- Internet
title: How Important is BGP RPKI?
---
Corey Quinn [mentioned me in a tweet](https://twitter.com/QuinnyPig/status/1349626652674801664) linking to [AWS announcement that they are the biggest user of BGP RPKI](https://aws.amazon.com/blogs/networking-and-content-delivery/how-aws-is-helping-to-secure-internet-routing/) (by the size of signed address space) worldwide. Good for them -- I'm sure it got their marketing excited. It's also trivial to do once you have the infrastructure in place. Just saying...

On a more serious front: how important is RPKI and what misuses can it stop?

If you've never heard of RPKI, the [AWS blog post](https://aws.amazon.com/blogs/networking-and-content-delivery/how-aws-is-helping-to-secure-internet-routing/) is not too bad, Nick Matthews wrote a "*look grandma, this is how it works*" version in [280-character installments](https://twitter.com/nickpowpow/status/1349783330879889410), and you should definitely spend some time exploring [MANRS](https://www.manrs.org/) resources. Here's a short version for differently-attentive ;))
<!--more-->
**What is RPKI?** RPKI ([Resource Public Key Infrastructure](https://en.wikipedia.org/wiki/Resource_Public_Key_Infrastructure)) is a framework that provides **origin AS validation** -- when receiving an IP prefix claiming it originates in AS X, you can validate using ROA (Route Origin Authorization) records whether AS X is allowed to originate that prefix. ROA records could specify an exact prefix that the AS can originate, or maximum prefix length in case you want to originate more specific prefixes.

**What happens to invalid prefixes?** That depends on local policy. ISPs adhering to [MANRS best practices](https://www.manrs.org/isps/bcop/) should ignore *invalid* prefixes and prefer *signed* over *unsigned* prefixes... but like in real life, you cannot force anyone else on the Internet to stop listening to fake news.

**What is RPKI protecting against?** RPKI validates the correctness of origin AS, stopping stupid fat-finger mistakes like two-way BGP-OSPF-BGP redistribution, [misconfigured BGP optimizers bringing down third-party services due to clueless tier-1 provider](/2019/07/rant-some-internet-service-providers.html), or the spillover effects of [third-world countries trying to stop their population from watching unorthodox video](/2008/02/building-customer-resilient-bgp.html). Off-topic: that  spillover was caused by another clueless tier-1 provider... you see a pattern here?

**What is RPKI not?** RPKI cannot be used to validate the *path* between your network and the origin. The bad guys can still spoof the AS path.

**What could the bad guys do?** Do I really have to spell it out? I'm pretty sure I'm not spilling any beans, so here it goes:

* Get a BGP announcement with the RPKI-signed prefix you're interested in;
* Transport it halfway across the globe to a place far enough from the origin;
* Replace the original AS path with a shorter AS path claiming the origin AS is directly connected to your AS.
* Advertise shorter AS path (with IP prefix correctly signed by the origin AS) to an ignorant third party.
* Profit.

**Can we stop the bad guys doing that?** Yes, but not with RPKI. The means to stop most shenanigans have been known for decades. Many of them are documented in [BGP Operations and Security RFC](https://tools.ietf.org/html/rfc7454). [MANRS best practices](https://www.manrs.org/isps/bcop/) go way beyond that, so make sure you read them, understand them, and implement them.

**So what's the big deal with RPKI?** Keeping fat fingers from bringing down parts of the global Internet is a big win. Trust me, I know all about that. I had fat fingers a long while ago... although the blast radius was only a single country. 

Stopping bad guys with a single silver bullet belongs to a vendor slide deck fairy tale, so stop bothering. A single tool will never be enough, so use whatever tools are at your disposal, and RPKI is not a bad tool to use.

Also, keep in mind that large web properties like Microsoft, AWS, or CloudFlare peer with thousands of networks at numerous exchange points, so it's pretty hard creating an AS path that is *shorter* than their AS path.

### Related Tools

I mentioned [MANRS best practices](https://www.manrs.org/isps/bcop/) several times. You [OUGHT TO](https://tools.ietf.org/html/rfc6919#section-4) read them.

[Peerlock](https://github.com/job/peerlock) is another tool that can be used to detect and stop fat-finger mistakes. Not surprisingly, it's another brilliant idea by Job Snijders.

Anything else? Write a comment.

