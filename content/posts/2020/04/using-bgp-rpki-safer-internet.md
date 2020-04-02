---
title: "MUST READ: Using BGP RPKI for a Safer Internet"
date: 2020-04-02 07:37:00
tags: [ BGP, security, Internet ]
---
As I explained in [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) and [Upcoming Internet Challenges](https://www.ipspace.net/Upcoming_Internet_Challenges) webinars, routing security, and [BGP security in particular](https://blog.ipspace.net/2019/07/rant-some-internet-service-providers.html) remain one of the unsolved challenges we've been facing for decades (see also: [what makes BGP a hot mess](https://blog.ipspace.net/2019/11/facts-and-fiction-bgp-is-hot-mess.html)).

Fortunately, due to enormous efforts of a [few persistent individuals](https://www.manrs.org/about/history/) BGP RPKI is [getting traction](https://www.manrs.org/isps/participants/) ([NTT just went all-in](https://us.ntt.net/news/view.cfm/NTT-Improves-Security-of-the-Internet-with-RPKI-Origin-Validation-Deployment?id=1470)), and Flavio Luciani and Tiziano Tofoni decided to do their part creating an [excellent in-depth document describing BGP RPKI theory and configuration on Cisco- and Juniper routers](https://blog.reissromoli.com/2020/03/bgp-rpki-instructions-for-use-en.html).

There are only two things you have to do:

* [Read the document](https://blog.reissromoli.com/2020/03/bgp-rpki-instructions-for-use-en.html);
* Implement RPKI in your network.

Thank you, the Internet will be grateful.

{{<note update>}}2020-04-02 16:00 UTC - based on [recent events](https://www.ripe.net/support/service-announcements/accidental-roa-deletion) we might need another document describing "_how to back up ROAs and have a recovery procedure that takes less than 20 hours_"{{</note>}}