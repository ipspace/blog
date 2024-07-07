---
date: 2018-09-08 11:59:00+02:00
series:
- valley-free
tags:
- design
- data center
- IP routing
title: 'Repost: Tony Przygienda on Valley-Free (or Non-ZigZag) Routing'
url: /2018/09/repost-tony-przygienda-on-valley-free/
---
Most blog posts generate the usual noise from the anonymous peanut gallery (if only they'd have at least a sliver of Statler and Waldorf in them), but every now and then there's a comment that's pure gold. The one [made by Tony Przygienda](/2018/09/valley-free-routing/#c9162579753181718524) (of [RIFT fame](/2018/03/data-center-routing-with-rift-on/)) on [Valley-Free Routing](/2018/09/valley-free-routing/) post is so good and relevant that I decided to republish it as a separate blog post. Enjoy!
<!--more-->

---
Valley free routing (which I call more generically no-zigzag routing, you can easily figure out what I mean, you go north until you change direction and go south which you do with the 0 and +/-, unsurprisingly major principle in RIFT again ;-) is a very desirable, very hard to achieve property unless you have a sense of N-S on the substrate (fabric, AS-mesh, whatever) which preconditions sense of direction (to be bit bloated, you need a partial mesh with a max-upper and lower bound). And hence, if done extremely well you are not even bound by ECMP anymore ;-)

I do obviously think for locally provisioned bandwith (such as IP fabrics) this is a natural way to progress and will become stronger with the demise of "artisanal local network configuration skills". Whether it will be Clos or some variant thereof is not very interesting, routing will adjust, the more "interconnected" your fabric in terms of shortcut the more routing information you'll have to slosh around @ convergence cost @ failure and so on. For things like WAN & AS meshes this is much, much harder thing to achieve, see also the "peer complex role" route leaking discussions in GROW. Hence I don't think lots of progress will be made unless some kind of economic cost will be imposed on hot potato routing ;-)
