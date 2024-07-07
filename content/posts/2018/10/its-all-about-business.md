---
date: 2018-10-30 08:53:00+01:00
lastmod: 2021-01-15 17:02:00
series:
- RPKI
tags:
- Internet
- BGP
title: 'Internet Routing Security: It’s All About Business…'
url: /2018/10/its-all-about-business/
---
A few years ago I got cornered by an enthusiastic academic praising the beauties of his cryptography-based system that would (after replacing the whole Internet) solve all the supposed woes we're facing with BGP today.

His ideas were technically sound, but probably won't ever see widespread adoption -- it doesn't matter if you have great ideas if there's not enough motivation to implementing them ([The Myths of Innovation](https://www.amazon.com/gp/product/1449389627/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=cisioshinandt-20&creative=9325&linkCode=as2&creativeASIN=1449389627&linkId=c9a976737625d7da43044086479fad50) is a mandatory reading if you're interested in these topics).
<!--more-->
Here's a pretty useful filter you can use when someone tries to tell you he solved a really hard problem:

-   Find out all the prior proposed solutions (if the problem is worth solving, someone else probably tried to solve it before);
-   Figure out whether the other solutions failed due to technical reasons (in which case there might be hope);
-   If the prior solutions were technically feasible but weren't accepted, there might be a business reason for that;
-   If the proposed solution sufficiently changes the business model, there might be hope. Otherwise, move on.

Coming back to BGP example:

-   We had RPKI for years. Uptake was minimal until very recently when large ISPs started using it ([NTT announcement](https://www.gin.ntt.net/support-center/policies-procedures/routing-registry/)) and [owners of large parts of IP address space deployed ROA records](https://aws.amazon.com/blogs/networking-and-content-delivery/how-aws-is-helping-to-secure-internet-routing/). For more details, check [MANRS participants](https://www.manrs.org/isps/participants/).
-   BGPsec was also developed years ago. Nobody even thinks about using it due to the additional compute overload it would create;
-   There are tools to generate prefix lists from public routing databases. A very small percentage of ISPs cared enough about the quality of Internet routing to use them... until passionate engineers like [Job Snijders](http://instituut.net/~job/) started [MANRS community](https://www.manrs.org/) and created enough buzz and visibility to make Internet routing security relevant..

In case you're wondering what's wrong with the BGP world, [Russ White](https://www.ipspace.net/Author:Russ_White) nicely explained it in [*BGP Security: A Gentle Reminder that Networking Is Business*](https://rule11.tech/bgp-security-a-gentle-reminder-that-networking-is-business/). Have fun!

### Revision history

2021-01-15
: Updated the RPKI status - it's now used by large ISPs and content providers.
