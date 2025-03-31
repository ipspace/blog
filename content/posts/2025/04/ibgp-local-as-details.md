---
title: "iBGP Local-AS Details"
date: 2025-04-08 08:08:00+0200
tags: [ BGP ]
draft: True
---
Did you know that you could use the **neighbor local-as** BGP functionality to fake an iBGP session between different autonomous systems? I knew Cisco IOS supported that monstrosity for ages (supposedly "_to merge two ISPs that have different AS numbers_") and added the appropriate tweaks[^HNUI] into _[netlab](https://netlab.tools/)_ when I added the [BGP **local-as** support](https://github.com/ipspace/netlab/commit/0943d5fe5686adf1766fc1062313ef2ed55f50e3) in release 1.3.1. Someone couldn't resist [pushing us down that slippery slope](https://github.com/ipspace/netlab/issues/368), and we ended with IBGP local-as implemented on [18 platforms](https://netlab.tools/module/bgp/#platform-support) (almost a dozen network operating systems).

I even wrote a [related integration test](https://github.com/ipspace/netlab/blob/release_1.9.5/tests/integration/bgp/08-ibgp-localas.yml), and all our implementations passed it until I asked myself a simple question: "But does it work?" and the number of correct implementations that passed the test without warnings dropped to zero.
<!--more-->
[^HNUI]: Together with "I hope no one uses it," rephrased as "viability of IBGP local-as is not checked yet." in the commit message.

{{<long-quote>}}
This blog post is a _thinking-out-loud_ exercise and should document most of the caveats you might encounter if you decide to use this feature.

**Before you start:** Just because you could does not mean that you should. You've been warned.
{{</long-quote>}}