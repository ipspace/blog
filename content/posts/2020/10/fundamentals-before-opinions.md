---
title: "Grasp the Fundamentals before Spreading Opinions"
date: 2020-10-27 06:18:00
tags: [ networking fundamentals, ip routing, LISP ]
---
I should have known better, but I got pulled into another _stretched VLANs for disaster recovery_ tweetfest. Surprisingly, most of the tweets were along the lines of _you really shouldn't be doing that_ and _that would never work well_, but then I guess I was only exposed to a small curated bubble of common sense... until this gem appeared in my timeline:

![Networking Needs ZIP codes](/2020/10/Twitter-ZIP-Code.png)

Interestingly, that's exactly how IP works:
<!--more-->
* An IP address is like your street address... and if you live in a corner building and have doors facing two streets, you'll get two different addresses;
* An IP subnet is like a street;
* A summarized prefix (like what you advertise to the Internet) is like a ZIP code.

So where's the problem, and why do we need endless discussions about stretched VLANs? Unfortunately (to continue the ZIP code analogy), some people got their town planning experience playing with Lego City (aka Loopback Interface), think that whatever they figured out in that limited domain translates into real life, and expect to be able to carry their street address with them wherever they go.

That approach doesn't work in real cities, but IT is different, and anyone [throwing a big-enough tantrum](/2013/04/this-is-what-makes-networking-so-complex/) can bend reality and force everyone else to [implement the warped reality](/2013/01/long-distance-vmotion-stretched-ha/) no matter the resulting costs.

But doesn't it work really well with mobile phone numbers... and why wouldn't the same approach work with IP addresses? According to my limited understanding of how [phone number portability](https://en.wikipedia.org/wiki/Local_number_portability) works we'd be comparing apples and bricks (not even oranges):

* Phone numbers are like host names, and there's a directory service involved whenever you're trying to call someone;
* If you move too far away from where your phone number was allocated (= different country) all sorts of crazy roaming scenarios come into play, resulting in something like IP mobility with home agents.

Anyway, back to my discussion. People don't love to hear their opinions aren't grounded in reality, and so the _debate_ continued...

![Networking Needs LISP](/2020/10/Twitter-LISP.png)

While LISP might have some good ideas, it doesn't change IP addressing concepts in any way, and it's just a cache-based forwarding scheme[^1] with a DNS-like mapping service building an IP-over-IP overlay, proving the wisdom of RFC 1925 rule 6 and 6a. 

Also, once we'd decouple application endpoints from IP addresses using some sort of service discovery (see also: [missing session layer](/2009/08/what-went-wrong-tcpip-lacks-session/)) we wouldn't need LISP anyway.

The next step was a brief detour into FG NET-2030 initiative (yay, [just the right way to solve all problems Internet has](https://labs.apnic.net/?p=1318)), and I finally had enough after reading this one:

![Antiquated IP addressing](/2020/10/Twitter-Antiquated.png)

I know Twitter isn't exactly the place to exchange nuanced ideas, but the very minimum I would expect in a network engineering discussion is opinions supported by something resembling hard facts. Obviously, sometimes that's too much to ask.

To make matters worse, it's not hard to find resources explaining the relevant fundamentals, including our [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar and [tons of great books](https://my.ipspace.net/bin/list?id=Net101#TEXTBOOK) (the first two books in that list are free). All you have to do is invest time in reading some of them instead of vendor whitepapers or industry press.

[^1]: Anyone old enough to remember the Internet-wide meltdowns caused by fast switching caches is probably smart enough not to touch another cache-based data-plane technology in their lifetime. Exposure to Nexus 7000 conversation learning (in particular after configuring SVI interfaces) is an added bonus.