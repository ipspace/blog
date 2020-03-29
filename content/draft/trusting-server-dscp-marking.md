---
title: Can We Trust Server DSCP Marking?
tags: [ QoS ]
draft: true
##date: 2020-05-01 00:00:00
---
A reader of my blog sent me this question:

> Do you think we can trust DSCP marking on servers (whether on DC or elsewhere - Windows or Linux )?

As they say “not as far as you can throw them”.

Does that mean that the network should do application recognition and marking on the ingress network node? Absolutely not.
<!--more-->
We have to get used to the fact that we should run our networks like a [utility service](http://localhost:1313/2013/04/they-want-networking-to-be-utility-lets.html)... and with every service comes **Service Level Agreement**.

In case of differentiated quality of service, you have to base your QoS implementation on a **service definition**: the user can generate **this much** traffic of **this traffic class**. After having that service definition (or SLA if you wish) in place, stop worrying about traffic marking. Configure ingress policing, shaping, or remarking to prevent SLA abuse, and let your customers mark their own traffic.

{{<note info>}}The mechanism to use depends on what’s available in your first-hop switching platform and how aggressive you want to be. Remarking is often better (and always more polite) than policing.{{</note>}}

Finally, make sure you have a system to monitor the per-port QoS counters, and have a nice graph explaining why the users' high-priority traffic is dropped for the moment they come screaming…