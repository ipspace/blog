---
title: "Fast Failover Techniques and Technologies"
date: 2020-11-06 18:59:00
draft: True
tags: [ IP routing ]
---
Actually, looking at the original question, some clarifications would help.
Terminology/complexity from high to low:
FRR = RSVP-TE
IP FRR = xLFA
Fast rehash is not a standard and based on common implementations in forwarding silicon.

FRR provides(requires RSVP-TE signalling): link protection/node protection/path protection 

IP FRR provides(requires LS IGP and LFA computation):
-LFA: link protection/node protection and is topology dependent
-rLFA: link protection/node protection and is topology dependent
TI-LFA: link protection/node protection and is topology independent (uses SR to tunnel to PQ node)

Fast-rehash provides link protection in ECMP topologies

I have addressed some of it in one of “between 0x2 nerds” webinars.
In general - you are comparing 2 different techniques - IP FRR vs fast-rehash. IP FRR (xLFA) relies on a pre-computed backup next-hop (it is more complex in rLFA/TI-LFA) that is loop-free (could be ECMP) and is a control plane function (eventually end-result is downloaded into HW), it could take into consideration some additional data - SRLGs, interface load, etc.
Fast-rehash is a forwarding construct, where the next-hop (could be called differently) is not a single entry but an array of entries (ECMP bundle as downloaded by the control plane).
If one of them becomes unavailable (BFD DOWN or LoS or interface down events) it is simply removed from the array and the hashing is updated accordingly, hence the name.
Usually - you’d see LFA implemented on a high end routers, it is much more intelligent and provides non connected bypass to reach PQ (rLFA/TI-LFA). 

Fast-rehash on contrary protects only connected links and doesn’t require any additional computation (ECMP alternatives are per definition loop-free). Usually implemented in DC environments. Hope this explains it.
IP FRR RFCs are produced by IETF RTGWG (LFA RFC5286)

Let's go through all possible scenarios (basic/naive), 
note - we talk underlay only, fast convergence in overlay is a completely separate topic. 

No xFRR:
all routes in RIB have 2x NHs - A and B (ECMP); link A goes down, 
routing gets notified (thought NH registration), 
routes with single NH B ->RIB->FIB
takes ~50-100ms

LFA:
all routes in RIB have 2x NHs - X {A/B} and Y {B/A} (ECMP), IGP computes LFAs for all primary NHs.
NH A is protecting (LFA) for NH B and the other way around and downloaded to HW.
link A goes down LFA structure (double or indirect NH) in forwarding gets notified and swaps in Y protected by protecting NH
Y{A}, eventually X gets removed (no protection)
takes below 1ms

fast-rehash:
NH Z for destination D is an array of {A,B}, link A goes down, FW gets notified, 
removes A from Z and rehashes all flows to B
takes below 1ms