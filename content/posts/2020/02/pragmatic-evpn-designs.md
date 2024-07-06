---
date: 2020-02-25 08:48:00+01:00
evpn_tag: design
tags:
- design
- EVPN
title: Pragmatic EVPN Designs
url: /2020/02/pragmatic-evpn-designs.html
---
While running the *[Using VXLAN And EVPN To Build Active-Active Data Centers](https://www.ipspace.net/Using_VXLAN_And_EVPN_To_Build_Active-Active_Data_Centers)* workshop in early December 2019, I got the usual set of questions about using BGP as the underlay routing protocol in EVPN fabrics, and the [various convoluted designs](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics) like IBGP-over-EBGP or EBGP-between-loopbacks over directly-connected-EBGP that some vendors love so much.

I got a question along the same lines from one of the readers of my [latest EPVN rant](/2020/02/the-evpnbgp-saga-continues.html) who described how convoluted it is to implement the design he'd like to use with the gear he has (I won't name any vendor because hazardous chemical substances get mentioned when I do).
<!--more-->
Here's what you have to keep in mind when considering what design to use in your network (and it applies to everything, not just EVPN): while I [love to fight the windmills](/2019/04/dont-sugarcoat-challenges-you-have.html) of overly-complex designs, and [annoy the vendors by pointing out weaknesses in their arguments](/2020/02/the-evpnbgp-saga-continues.html), you have a network to run, so be pragmatic.

**Do whatever your vendor describes as the reference design... and if you have multiple reference designs, choose the simplest one that meets your scalability requirements.**

You might not like the design your vendor loves and find it too complex. Guess what? There are multiple vendors out there, and they are all keen to take your money. Vote with your wallet—that's the only way to bring some common sense to this industry.

### In Case You're Not Persuaded (Yet)

While every vendor (marketing department) claims they support whatever you'd like to do, or as Aldrin said in [his comment](/2019/11/the-evpn-dilemma.html?showComment=1575211955484#c831176054126186737) to my [EVPN Dilemma](/2019/11/the-evpn-dilemma.html) blog post...

> Pretty much all EVPN implementations support multiple routing protocols, including IS-IS, OSPF, and EBGP as IGP. There's a difference between a reference design and feature support.

.. there truly is a difference between the two: reference design is tested much better than all other combinations of supposedly supported features. If you don't fancy providing free QA/troubleshooting resources to your \$vendor (and arguing with their level-1 TAC that reloading the box doesn't help while doing that), stick with whatever the vendor recommends.

As always, there will be consequences. In this particular case:

-   As no two vendors use the same preferred reference design, forget about multi-vendor EVPN fabrics (which is probably a good idea anyway);
-   Some reference designs tend to be overly complex. Someone will have to troubleshoot them at 2 AM on a Sunday (hint: that might be you, or they might call you after they get hopelessly lost). All other things being equal, choose the vendor with the most straightforward reference design.
-   Some reference design configurations read like a Tolstoy novel. Prefer vendors that can implement your needs with minimum configuration hassle ([example](/2019/10/auto-mlag-and-auto-bgp-in-cumulus-linux.html))

You can always generate device configurations with templates, and the vendors with overly verbose configurations will quickly point out the powers of automation. However, someone has to design those templates, and someone might have to troubleshoot them (or the actual device configurations)... yet again, most probably at 2 AM on a Sunday [when the automation system breaks down](/2018/02/big-red-button-for-network-automation.html). Regardless of what the thought leaders love to tell you, if you want to have a stable solution, [hidden complexity](/2015/11/can-you-afford-to-reformat-your-data.html) tends to be [worse than explicit complexity](/2018/02/how-self-sufficient-do-you-want-to-be.html).
