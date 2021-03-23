---
title: "Another Take on MPLS-versus-VXLAN in Overlay Networks"
# date: 2021-03-22 16:35:00
tags: [ MPLS, VXLAN, overlay networks ]
draft: True
intro: |
  Another "VXLAN versus MPLS" saga with Minh Ha
---
I feel you’re conflating service provider use case with public cloud use case. There’s no need for TE or multihoming in public clouds.

Also, remember that in public clouds you could have 100K+ VTEPs per data center.

Will write a blog post as a reply to this comment, but it will take time.

All the best, and thanks a million for all the excellent comments!
Ivan
On 22 March 2021 at 05:33:54, ipSpace.net Server (bounce@ipspace.net) wrote:

New comment on ipSpace.net blog

Minh Ha (minh.ha@unsw.edu.au) submitted the following comment to https://blog.ipspace.net/2020/05/need-vxlan-transport.html.

Ivan, I'm very much in sync with you re MPLS requiring tight coupling between edge and core :)). But I think if that's the selling point of VXLAN, then it has a long way to go. Gotta try much harder than that. Let me explain.

Yes, MPLS is tighly-coupled, but all of the complexity and heavy-duty work -- keeping track of VRFs and all -- are done by the PE at the edge. The core routers only concern with building a map between PEs, so the amount of state they keep is very much manageable, even if we speak of say, a few thousand PEs. With modern-day ASIC, this is doable, and it's high-end environments when we speak of PEs in the thousands. Both MPLS and VXLAN have to deal with IGP calculation, and at large scale, the overhead is fair game for both. LDP overhead is nowhere like that of Link State calculation, or TCAM programming delay.

With MPLS in the core, we don't have BGP next hop's trust issue resulting from control and data path inconsistency. This is not a big deal for small networks, but can happen in big networks due to complexity.

MPLS can do TE, VXLAN cannot.

MPLS ESI multi-homing label is more natural, while with VXLAN it's more convoluted.

VXLAN encapsulation overhead is huge vs MPLS.

Re DC environment, as I said in the Cloud post (and was actually mentioned on page 1 of the VFP paper) the Cloud went with overlay model mainly because it's the cheapest they can use to implement virtual networking. Cloud providers make use of commoditized routers/switches in their environment, so MPLS is mostly not an option. By going with Directory service mapping in software, they sacrifice the performance of their vnet for lowering cost. MPLS is high-performance.

But saying it like it is doesn't sound good for marketing purpose, for winning customers. When they say nothing scales to our environment, so we have to invent our own, they basically just dress it up in nice excuse, and it makes them look so cool and holier than thou as well ;).

For ex, check out section 4.2 of this paper, you'll quickly find out MS reasoning for using Directory service is a direct result of bad design aka Flat-Earth, resulting in massive churns if done in hardware:

https://web.eecs.umich.edu/~mosharaf/Readings/VL2.pdf

Regardless, they are slowly coming full circle back to hardware, with their FPGA offloading :)).

Also, modern ASICs have enough TCAM space to store 4 million LPM entries, e.g. Cisco NCS 6k. It's off-chip and so slower than on-ASIC TCAM of course, but still way faster than having the table stored in a different device, and in RAM, so the 'scale factor' is a non-issue AFAIK.

Minh

====

You’re right 😊. I brought up TE just for the sake of comparison, but it’s not needed.

 

In public cloud, as I mentioned in the other emails, the software switching model won’t scale (slow), and so they don’t use software switches as full-blown VTEP but rely on external mapping service as well.

 

I understand your reasoning for having the software switches acting as the VTEP/PE. That way people who build virtualized network are totally decoupled from the physical infrastructure guys. But say, if we are to build a Cloud service offering, our network infras team would be in charge of creating the whole network, including the virtual parts. So with that kind of control, we can integrate the virtual and the physical in a way that maximizes performance.

 

Why do I bring this up? From a practical perspective, it doesn’t matter what we say; it’s not gonna change anything. Cloud providers are motivated by profit, not by sound architecture. As long as they can sell what they create to the most customers, that’s all that matters. Oracle Cloud for ex, exploit L2 niche even though it’s not technically sound, because it makes great sense business-wise. It’d be suicidal to compete in the same segment as the big 3 AWS, Azure, and GCP, so they have to exploit a niche to carve out a place for themselves. If they offer a sound L3 infras, they will be seen as just another commodity provider like all the rest and that offers them no competitive advantage.

 

But business aside, if we are to call ourselves engineer, I think we should able to analyze and see thru all the pros and cons with each solution, instead of just following the herd and sing the same tune, ala if these big Cloud guys do things this way, that must be because that’s the only way to scale.

 

So coming back to the VTEP/PE in the cloud, say if we use MPLS and SR-IOV hardware offload, then the TORs can store all the VRF info, and the VM can send packets directly to it, doing away with software VTEP and slow external directory service lookup. This way, we cut the layers and the latency. And say, by building a network with high-radix routers acting as TORs, we can reduce device counts in DCs, which adds to infrastructure saving too.

 

Of course this is a hypothetical solution that I’m discussing with you right here, but I bring it up because I think it’s viable, and it has better performance than the existing software-based architecture.

 

Wrt SRV6, it’s a big scam AFAIK 😝. If someone subsidizes my power bill, then I’ll think twice about using it. From the very beginning, IPv6 was about politics. It’s pathetic as a architecture and low-performance. SRV6 does a good job amplifying the resource hog!