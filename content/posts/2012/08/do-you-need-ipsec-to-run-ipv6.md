---
date: 2012-08-09 06:27:00+02:00
tags:
- IPv6
- security
title: Do You Need IPsec to Run IPv6?
url: /2012/08/do-you-need-ipsec-to-run-ipv6/
---
The usual claim that "[IPv6 has better security because it includes mandatory IPsec support](/2010/02/ipv6-myths/)" is evidently creating some confusion, at least based on a set of questions I received from one of my readers.

> Can IPv6 work without IPsec?

Absolutely. Most IPv6 deployments don't use IPsec (unless you're building IPsec-based VPNs over IPv6 transport infrastructure).
<!--more-->
In December 2011, IPsec support in IPv6 was [downgraded from MUST to SHOULD](http://tools.ietf.org/html/rfc6434#section-11) by [RFC 6434](http://tools.ietf.org/html/rfc6434).

{{<note update>}}**Update 2020-12-25**: This blog post has only historic significance. Nobody is talking about IPsec with IPv6 anymore. Most everyone gave up and moved to SSL/TLS and/or HTTP/2.{{</note>}}

> When we want to connect to a server with IPsec over IPv6, shall we have certificates on the clients or will it be like HTTPS?

There's no difference between IPsec running on top of IPv4 or IPv6. The first step in every IPsec session setup is key exchange; default key management protocol specified in RFC 6434 is IKEv2. IKEv2 can use preshared keys or certificates.

> Is it mandatory to have a Cisco IOS image that includes IPsec support to deploy IPv6?

No. For example, [IP Base technology package on ISR G2 includes IPv6 support](http://www.cisco.com/en/US/prod/collateral/routers/ps10616/white_paper_c11_556985_ps10537_Products_White_Paper.html#wp9000809). However, you should use the [feature navigator](http://tools.cisco.com/ITDIT/CFN/jsp/index.jsp) to confirm which images support IPv6 on your specific platform/release.

## More information

* To get an overview of IPv6 deployment requirements, watch the [*Enterprise IPv6 -- the first steps*](http://www.ipspace.net/Enterprise_IPv6_-_the_First_Steps) webinar or its [*service provider equivalent*](http://www.ipspace.net/Service_Provider_IPv6_Introduction). 
* You'll find IPv6 network design and deployment guidelines in the [*Building Large IPv6 Service Provider Networks*](https://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks) webinar.
* All three webinars are included in the [yearly subscription](http://www.ipspace.net/Subscription).
