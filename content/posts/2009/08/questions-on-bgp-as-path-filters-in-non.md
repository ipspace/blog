---
date: 2009-08-18 21:07:00.003000+02:00
tags:
- BGP
title: Questions on BGP AS-Path Filters in Non-Transit Networks
url: /2009/08/questions-on-bgp-as-path-filters-in-non.html
---
I've sent a link to my [*Filter excessively prepended AS-paths*](/kb/tag/BGP/Filter_Excessively_Prepended_BGP_Paths.html) article as an answer to a BGP route-map question to the NANOG mailing list and got several interesting questions from Dylan a few hours later. As they are pretty common, you might be interested in them as well.

> In my environment, we are not doing full routes. We have partial routes from AS X and then fail to AS Y. Is their any advantage for someone like me to do this, as we are not providing any IP transit so we are not passing the route table to anyone else?
<!--more-->
You could use inbound AS-path filters to protect your BGP table, but as you\'re not a transit AS, it does not make much sense. You might also use them to reduce the size of your BGP table, but obviously you've already taken care of that.

> When I run the \"sh ip bgp quote-regexp \"\_(\[0-9\]+)\_\\1\_\\1\_\\1\_\\1\_ \\1\_\" \| begin Network\" I am seeing many paths that would be filtered by this access-list.

Obviously a lot of people are prepend-happy, but as I've stated in the original article, if prepending your AS number a few times doesn't help, nothing will.

> What happens to those networks, are they unreachable from my AS, or do I just route those networks to my upstream provider and let them deal with it?

If I understood correctly, you\'re using a default route toward AS Y, which means that anything that is not in your BGP table (and consequently your IP routing table) will be sent out of your AS via the default route. If you\'re getting the paths you\'re filtering from AS X that means that more traffic will go to AS Y.

> This last question is a little off-topic, but relates to your access list. In the event of some kind of DOS attack coming from one of a few AS numbers (let\'s assume it\'s AS Z), what is the feasibility of using\
> \
> ip as-path access-list 100 deny \_(\[0-9\]+)\_\\1\_\\1\_\\1\_\\1\_\
> ip as-path access-list 100 deny Z\
> ip as-path access-list 100 permit .\*\
> \
> Would this have any affect at all, or would my pipe from my upstream still be congested with garbage traffic?

No. You cannot influence the inbound traffic apart from not advertising some of your prefixes to some of your neighbors or giving them hints with BGP communities or AS-path prepending. Whatever you do with BGP on your routers influences only the paths the outbound traffic is taking. What you\'d actually need is remote-triggered black hole. Frank Bulk provided a number of links in [this message](http://www.merit.edu/mail.archives/nanog/msg19969.html).
