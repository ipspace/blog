---
date: 2008-09-24 06:57:00+02:00
tags:
- MPLS
- traffic engineering
- MPLS VPN
title: Do you need LDP with MPLS TE?
url: /2008/09/do-you-need-ldp-with-mpls-te/
needs_fix: true
---
An [anonymous commenter](/2008/08/is-label-imposed-in-case-of-penultimate.html?showComment=1219355400000) to my [implicit NULL/PHP post](/2008/08/is-label-imposed-in-case-of-penultimate/) made a very valid point:

> Most Cisco documentation states that you must enable LDP before doing MPLS-TE, which is a complete fallacy.

If you\'re using MPLS TE simply to shift IP traffic around your network, he\'s absolutely right: there is no need to run LDP if you have an IP-only network. If you\'re running MPLS VPN or BGP on edges/MPLS in the core, the answer becomes "it depends." 

I documented the detailed rules and undesired side effects if you ignore them a long while ago, but that article disappeared into /dev/null. Fortunately [archive.org caught a copy before that](https://web.archive.org/web/20170515160839/http://wiki.nil.com/MPLS_Traffic_Engineering_in_MPLS_VPN_environment).

{{<ct3_query>}}
