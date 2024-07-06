---
title: "OMG: VTP Is Insecure"
date: 2022-02-09 09:35:00
tags: [ switching, security ]
---
One of my readers sent me an interesting pointer:

> I just watched a [YouTube video](https://youtu.be/u5cp_hcwq2c) by a security researcher showing how a five line python script can be used to unilaterally configure a Cisco switch port connected to a host computer into a trunk port. It does this by forging a single virtual trunk protocol (VTP) packet. The host can then eavesdrop on broadcast traffic on all VLANs on the network, as well as prosecute man-in-the-middle of attacks.

I'd say that's a "startling revelation" along the lines of "[OMG, VXLAN is insecure](/2018/11/omg-vxlan-is-still-insecure.html)" -- a wonderful way for a security researcher to gain instant visibility. From a more pragmatic perspective, if you enable an insecure protocol on a user-facing port, you get the results you deserve[^FW].

While I could end this blog post with the above flippant remark, it's more fun considering two fundamental questions.
<!--more-->
[^FW]: I know some of my readers mentioned other similar failures in comments to other blog posts, including some that were never fixed, but my Google-Fu isn't at its best today.

**Why are so many networking protocols insecure?** In a nutshell: creating a secure solution is hard work. It's much faster and cheaper to create an MVP (Minimum Viable Protocol) and declare the Mission Accomplished. SMTP anyone?

To make matters worse: applying some security lipstick to an insecure piglet usually creates more problems than it solves. For example, you could use hashes based on secret keys to ensure you're talking to a trusted peer, but then you have to solve the key distribution and key rollover problems[^MD5]. You could also use certificates, but nobody wants to set up a proper PKI infrastructure (and certificate enrollment is a headache anyway), and so you end with self-signed certificates that are no better than a [cozy security blanket](https://networkingnerd.net/2011/03/06/my-buzzword-security-blanket/).

[^MD5]: Not to mention changing the hashing algorithm every decade or so which requires extra fields in every data packet to specify the version of the hashing algorithm, and a rollover mechanism. At least OSPF got it right -- there's an RFC out there specifying specifying [how to use SHA algorithms for OSPF authentication](https://datatracker.ietf.org/doc/html/rfc5709).

On the other hand, many networking protocols aren't supposed to be used with untrusted peers (like security researchers). They are supposed to be used in a trusted network core, and if someone hacks into the network core it's game over anyway. The moment you can insert traffic into a core link you can spoof VLANs, VXLAN segments, MPLS labels... unless you're encrypting the traffic on core links, in which case you wouldn't have to worry about securing another control-plane protocol anyway, right?

Not really. In the words of my reader:

> This was a Cisco switch, and apparently the default configuration permits this. I haven’t delved into the details yet, but I’m hoping that there are straightforward configuration settings that can prevent this kind of attack. I gather, though, that it isn’t as simple as just adding a line code to IOS. It looks like what’s needed is very specific pruning of VLANs to ports for devices that are not switches, and that sounds like a big, ongoing maintenance task prone to human error.

In the VTP case, most everyone agrees [VTP should be disabled](/2008/12/should-vtp-be-disabled-by-default.html), which raises the next obvious question: **Why are most networking devices insecure by default?**

As hard as I try, the only answers I can come up with are the cynical ones along the lines of *because nobody cares* or *[to lower the vendor support costs](/2018/01/revisited-need-for-stretched-vlans.html)*. To make matters worse, most devices ship with abhorrent (security-wise) defaults, and *device hardening guides* (when a vendor publishes them) quickly turn into a Bible-sized list of things to configure[^HARD]... and even then they don't cover everything they should. Back to my reader:

[^HARD]: See for example the comments to [Should VTP be Disabled by Default](/2008/12/should-vtp-be-disabled-by-default.html) published in 2008. More than a decade later we're still dealing with VTP SNAFUs.

> It’s easy to overlook common pitfalls. Like most network engineers, I tended to just follow the vendor’s hardening checklist and thought that was more or less complete. That’s why I was surprised that Cisco never mentions this in their Hardening IOS book.

That book must have been written by router-minded engineers, and the extra switching "features" thrown into Cisco IOS when it was hammered into another heptagonal hole (to replace CatOS) obviously never got considered.

Good engineers try their best to fix the problem, but it feels like a Sisyphean task considering the state of today's network operating systems:

> I’d love to see a strategy for proactively designing security measures into networks works for this vulnerability and others recently discovered. Every network I’ve ever worked on, all the security stuff seem to be bolted on after the fact, rather than designed in from the beginning.

Would it be really THAT hard to have two sets of defaults for *core* (trusted) and *edge* (hardened) ports and apply *edge* defaults to every device port or interface that is not explicitly configured as a *core* port? Has any vendor ever shipped a router or a switch designed along these lines (firewalls don't count for obvious reasons)? Your comments would be most welcome!
