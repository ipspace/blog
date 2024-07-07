---
url: /2008/09/end-to-end-responsibility/
title: "End-to-End Responsibility"
date: 2008-09-06 09:48:00
tags: [ design ]
---
If you’ve ever had the “privilege” of **buying equipment from a large systems integrator** (or directly from a large vendor), you’re probably familiar with this process:
<!--more-->
1.  The salesman (politely called the “Account Manager”) brings an engineer (“Sales Engineer”) with him. Although they do some network design in the presales cycle, their usual focus is the “kit list” they need to **place an order**.
2.  If you’re not proficient enough in the technology you’ve just bought, another team is brought in: the Professional Services (PS) team. Ideally, the kit list produced in the early design phase is accurate enough to **implement the network**. However, I’ve been involved in projects where no one knew what the kit list was trying to accomplish, and we were forced to design the network around the existing hardware (although half of it was superfluous) in order to satisfy the customer.
3.  Once the network is up and running and the ready-for-use (RFU) documentation is signed, the Professional Services team is gone. When you encounter **post-implementation issues**, you have to talk to Technical Support. If you’re a big enough customer, the Technical Support team might have the design and implementation documentation prepared by the PS team; otherwise, you have to explain to the Technical Support team what their Professional Services colleagues were doing.

When I was the technical director at a small (but fast growing) system integrator almost three decades ago we realized that this system was broken, and implemented a **completely different approach that has remained very successful** (even though the company has grown from 15 to over 100 employees in the meantime): a single engineer is responsible for all phases of the network lifecycle.

To start with, we had very few purely presales engineers. When salespeople needed technical support (whether for a customer visit or a follow-up technical solution), they got the best engineers from the support group. These engineers also prepared the network design and signed off the kit list before the proposal was sent to the customer.

Ideally, if the customer understood the value of our services, a detailed network design would be done before we even started discussing the details of the kit list; otherwise, the engineer who produced the kit list also created the network design that serves as the blueprint in the implementation phase (also led by the same engineer)… and remained the primary support contact for the customer.

This procedure ensured that **there were no easy escape routes**: if you had messed up the design, you'd have to fix it yourself and live with the network – as you’d designed it – until the next upgrade. Because no engineer wants that sort of headache, the designs were usually well planned from the start.

Sound too good to be true? It worked for us, and resulted in fantastic customer satisfaction and loyal customers.
