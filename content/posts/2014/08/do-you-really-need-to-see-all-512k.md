---
date: 2014-08-18 06:57:00+02:00
tags:
- Internet
- BGP
title: Do You Really Need to See All 512K Internet Routes?
url: /2014/08/do-you-really-need-to-see-all-512k/
series: vagg
vagg_tag: vagg
---
Last week the global routing table (as seen from some perspectives) [supposedly exceeded 512K routes](http://www.bgpmon.net/what-caused-todays-internet-hiccup/), and weird things started to happen to some people that are using [old platforms](http://www.cisco.com/c/en/us/products/collateral/switches/catalyst-6500-series-switches/product_data_sheet09186a0080159856.pdf) that by default support 512K IPv4 routes in the switching hardware.

{{<note warn>}}
I'm still wondering whether the BGP table size was the root cause of the observed outages. Cisco's documentation (at least [this document](http://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/116132-problem-catalyst6500-00.html)) is pretty sloppy when it comes to the fact that usually 1K = 1024, not 1000 -- I'd expect the hard limit to be @ 524.288 routes ... but then maybe Cisco's hardware works with decimal arithmetic.
{{</note>}}
<!--more-->
In any case, networks relying on boxes that support 512K IPv4 routes in their switching hardware might face interesting problems in a very near future... and the workaround is: [reduce the maximum number of IPv6 routes](http://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/116132-problem-catalyst6500-00.html). Isn't that just the perfect solution for the days when most of the world already ran out of public IPv4 addresses? On the other hand, the default IPv6 table size on Cat6500 is 256K entries, and the [current size of the global IPv6 routing table is below 20K](http://bgp.potaroo.net/v6/as2.0/) (HT: [Renesys blog](http://www.renesys.com/2014/08/internet-512k-global-routes/)).

{{<note>}}
The same hard limits usually don't apply to boxes that perform packet forwarding in software, for example ISR-series routers and probably also ASR1K -- but don't forget you'll need more memory as the BGP table, RIB, and FIB continue to grow.
{{</note>}}

Regardless of the platform you're using at your Internet edge, you should ask another question: do I really need the full Internet routing table? Most edge networks don't, and I [described several techniques you can use to reduce the BGP table size](http://www.ipspace.net/BGP_Convergence_Optimization).

Furthermore, you can use [*BGP Selective Route Download*](http://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/configuration/xe-3s/irg-xe-3s-book/irg-selective-download.html) (unfortunately available only on IOS XE) or a similar Junos functionality to reduce the IP RIB and FIB sizes (see also my article on [virtual aggregation](/2010/09/virtual-aggregation-quick-fix-for/)).
