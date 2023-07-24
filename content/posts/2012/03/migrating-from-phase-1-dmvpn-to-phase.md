---
date: 2012-03-28 15:19:00+02:00
dmvpn_tag: deploy
tags:
- design
- DMVPN
title: Migrating from Phase 1 DMVPN to Phase 2/3 Network
url: /2012/03/migrating-from-phase-1-dmvpn-to-phase.html
---
Chris sent me an interesting question that I haven't covered in any of my DMVPN webinars: "How would you migrate a part of a Phase-1 DMVPN network to a Phase-2 or Phase-3 network if you can only migrate one spoke site at a time? Can I just upgrade the spokes that need spoke-to-spoke connectivity?"

While it might be theoretically possible to have a mixed Phase-1/Phase-2 DMVPN tunnel (and I just might be able to get it to work in a lab), such a solution definitely violates the [KISS principle](http://en.wikipedia.org/wiki/KISS_principle).
<!--more-->
I would prefer to create a second Phase-2/3 DMVPN tunnel on the hub router(s) and migrate spoke sites that need any-to-any connectivity to this new Phase-2/3 DMVPN tunnel. The new tunnel would be used in parallel with the old one, and you could keep both of them running in parallel, or shut and remove the old one after all the spokes have been migrated to Phase 2/3 DMVPN.

{{<figure src="http://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Waders_in_flight_Roebuck_Bay.jpg/800px-Waders_in_flight_Roebuck_Bay.jpg" caption="Unfortunately you can\'t migrate DMVPN spokes in flocks">}}

Interestingly, the second tunnel does not diminish the network performance. In a Phase-1 DMVPN network all the traffic goes through the hub anyway, so it doesn't matter if you have one or more tunnels on the hub router -- changing the tunnel interface while forwarding an IP packet does not impact the forwarding performance. Creating a new DMVPN tunnel on the hub router thus doesn't cause any change in performance or traffic flow.

{{<note warn>}}You might need two tunnel transport IP addresses if you don't use GRE keys in your existing setup.{{</note>}}

### More Information

You'll find (almost) all you need to know about DMVPN in the [*DMVPN webinars*](http://www.ipspace.net/DMVPN_trilogy), which are (like all other webinars) part of the [yearly subscription](http://www.ipspace.net/Subscription).
