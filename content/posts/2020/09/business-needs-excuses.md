---
title: Are Business Needs Just Excuses for Vendor Shenanigans?
date: 2020-09-10 06:48:00
tags: [ virtualization, vMotion, design ]
---
Every now and then I inadvertently call someone's baby ugly (or maybe it was their third cousin's baby and they nonetheless feel offended). In such cases a common resort is to cite _business_ or _market needs_ to prove how ignorant and clueless I am. Here's a sample LinkedIn comment talking about my ignorance about the need for smart NICs:

> The rise of custom silicon by Presando [sic], Mellanox, Amazon, Intel and others confirms there is a real market need.

Now let's get something straight: while there are good reasons to use tons of different things that might look inappropriate, irrelevant or plain stupid to an outsider, I don't believe in _real market need_ argument being used to justify anything without supporting technical facts (tell me _why_ you need that stuff and prove to me that _using it is the best way of solving a problem_).

For example, Amazon has a real need for smart NICs to support bare-metal server instances in their Virtual Private Clouds. That doesn't justify them being used in any other scenario (see also: you're not Google).

Just because someone manages to sell something, and other vendors jump on the same bandwagon because their product managers smell new markets, doesn't mean that anyone really needs it, or that the challenge they new stuff is supposedly solving couldn't have been solved in a simpler or better way. Let me illustrate this claim with a quick digression into my favorite topic: using long-distance vMotion for disaster recovery (because it wouldn't work for disaster avoidance anyway).

**Business continuity** is the unquestionable real business need here.

That business need could be implemented with proper application architecture, **disaster avoidance** or **disaster recovery**. Which one of these is still acceptable is another business decision; what can be reasonably done based on the current state of company's IT and applications the business runs on is already a technology fact that cannot be avoided no matter how much pixie dust you sprinkle on it. For example, there's absolutely no way to implement 99.999% service availability if your application stack rides on a single database instance... and here's the first opportunity for a vendor to jump in and start selling unicorn farts.

Remember **fault-tolerant servers** - the super-expensive thingies that had full hardware redundancy, promising non-stop operation of your business-critical applications? Or the software equivalent promoted by VMware? There's just a bit of a problem with that approach: most failures experienced today are software failures, and two copies of a buggy program running in sync on two independent pieces of hardware will consistently crash at the exactly same time. Some of those fault-tolerant servers lived up to the vendor promises because the vendor also shipped the properly designed operating system, database servers, and transaction handling environments. Others were just snake oil... and whoever pointed that out was faced with the *real business need* wall of denial.

But wait, it gets worse... we could use stretched VLANs and long-distance vMotion to implement disaster recovery (or so the $vendor consultants told us). At this point we're way beyond the sane discussions of actual business needs. The whole idea was created by vendor marketers to sell more of their complex products, and happily adopted by most everyone in enterprise IT because it conveniently allows them to push the problem down the stack until the brown substance lands in the networking team, which is then blamed for being too rigid and too expensive... and ripe to be replaced by another $vendor magic, this time either software-defined, intent-based, or machine-learned.

**Long story short**: PLEASE, do your homework, and don't ever use the _some vendors are making it, so there must be a real market need for it_ or _some people are using it, so there must be a real business need for it_ argument. You just might end with an egg on your face.
