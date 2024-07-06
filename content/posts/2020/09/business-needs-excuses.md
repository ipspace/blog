---
date: 2020-09-17 06:48:00+00:00
high-availability_tag: need
series_weight: 750
tags:
- virtualization
- vMotion
- design
- high availability
title: Are Business Needs Just Excuses for Vendor Shenanigans?
---
Every now and then I [call someone's baby ugly](/2011/09/long-distance-irf-fabric-works-best-in.html) (or maybe it was their third cousin's baby and they nonetheless feel offended). In such cases a common resort is to cite _business_ or _market needs_ to prove how ignorant and clueless I am. Here's a sample LinkedIn comment talking about my ignorance about the need for smart NICs:

> The rise of custom silicon by Presando [sic], Mellanox, Amazon, Intel and others confirms there is a real market need.

Now let's get something straight: while there are good reasons to use tons of different things that might look inappropriate, irrelevant or plain stupid to an outsider, I don't believe in _real market need_ argument being used to justify anything without supporting technical facts (tell me _why_ you need that stuff and prove to me that _[using it is the best way of solving a problem](/2019/12/questions-to-ask-about-product-using.html)_).
<!--more-->

For example, Amazon has a real need for smart NICs to [support bare-metal server instances in their Virtual Private Clouds](/2020/06/cloud-networking-architectures.html). That doesn't justify them being used in any other scenario (see also: [you're not Google](/2020/03/the-stupidity-of-trying-to-be-like.html)).

Just because [someone manages to sell something](/2019/10/the-cost-of-disruptiveness-and.html), and other vendors jump on the same bandwagon because their product managers smell new markets, doesn't mean that anyone really needs it, or that the challenge the new stuff is supposedly solving couldn't have been solved in a simpler or better way. Let me illustrate this claim with a quick digression into my favorite topic: using [long-distance vMotion](/2015/02/before-talking-about-vmotion-across.html) for disaster recovery (because it [wouldn't work for disaster avoidance anyway](/2011/09/long-distance-vmotion-for-disaster.html)).

**Business continuity** is the unquestionable real business need here.

That business need could be implemented with proper application architecture, **disaster avoidance** or **disaster recovery**. Which one of these is still acceptable is another business decision; what can be reasonably done based on the current state of company's IT, and applications the business runs on, is already a technology fact that cannot be avoided no matter [how much pixie dust you sprinkle on it](/2016/01/the-sad-state-of-enterprise-networking.html). For example, there's absolutely no way to implement 99.999% service availability if your application stack rides on a single database instance... and here's the first opportunity for a vendor to jump in and start selling unicorn farts.

Remember **fault-tolerant servers** - the super-expensive thingies that had full hardware redundancy, promising non-stop operation of your business-critical applications? Or the software equivalent promoted by VMware? There's just a bit of a problem with that approach: most failures experienced today are software failures, and two copies of a buggy program running in sync on two independent pieces of hardware will consistently crash at exactly the same time. [Some of those fault-tolerant servers](https://en.wikipedia.org/wiki/NonStop_(server_computers)) lived up to vendor promises because the vendor also shipped the properly designed operating system, database servers, and transaction handling environments. Cheap knockoffs sold by virtualization vendors were just snake oil... and whoever pointed that out was usually faced with the *real business need* wall of denial.

But wait, it gets worse... we could use stretched VLANs and long-distance vMotion to implement disaster recovery (or so the [$vendor consultants told us](/2020/02/live-vmotion-into-vmware-on-aws-cloud.html)). At this point we're way beyond the sane discussions of actual business needs. The whole idea was created by vendor marketers to sell more of their complex products, and happily adopted by most everyone in enterprise IT because it conveniently allows them to [push the problem down the stack](/2013/04/this-is-what-makes-networking-so-complex.html) until the brown substance lands in the networking team, which is then [blamed for being too rigid and too expensive](/2016/07/why-is-every-sdn-vendor-bashing.html)... and ripe to be replaced by another $vendor magic, this time either software-defined, [intent-based](/2020/05/intent-networking-marketing-ploy.html), or [machine-learned](/2020/03/machine-learning-in-networking-products.html).

**Long story short**: PLEASE, do your homework, and don't ever use the _some vendors are making it, so there must be a real market need for it_ or _[some people are using it, so there must be a real business need for it](/2013/01/long-distance-vmotion-stretched-ha.html)_ argument. You just might end with an egg on your face (although most people using these arguments happen to be egg-blind so they wouldn't ever realize what happened).

---

Addendum based on a [tweet by Andrew Yourtchenko](https://twitter.com/ayourtch/status/1306505455393439744):

Obviously most of the products, services and solutions out there solve a real or perceived need (and there's sometimes a huge gap between the two).

What I'm pointing out in this rant is the reverse reasoning along the lines "_vendor X is doing something, which confirms there's a real market need for it_". I've been in IT too long, and seen how the startup/VC sausage is made, to believe that fairy tale... and even when it's true, it doesn't necessarily imply that you need whatever vendor X is selling.

For example, just because a mining operation needs huge trucks, it doesn't mean that everyone else needs them as well, regardless of what the truck manufacturers would love you to believe.
