---
title: "Response: Vendor Network Automation Tools"
date: 2023-12-11 08:03:00+01:00
tags: [ automation ]
---
Drew Conry-Murray published a [excellent summary of his takeaways from the AutoCon0 event](https://packetpushers.net/3-takeaways-from-autocon0/), including this one:

> Most companies want vendor-supported tools that will actually help them be more efficient, reduce human error, and increase the velocity at which the network team can support new apps and services.

Yeah, that's nothing new. Most Service Providers wanted vendors to add tons of nerd knobs to their products to adapt them to existing network designs. Obviously, it must be done for free because a vast purchase order[^VP] is dangling in the air. We've seen how well that worked, yet learned nothing from that experience.
<!--more-->
[^VP]: Worst case, just a vague promise of a potential network refresh if only the vendor would have just the right features.

It's easy to create a tool that will automate a greenfield network with no external dependencies in which the customer has no say in how the infrastructure is set up. That's why we have so many cloud provisioning tools -- AWS will not argue with you whether they should add a nerd knob to their services. You can either use what they have or walk away.

Automating an existing enterprise network is a never-ending integration nightmare, and the only way to sell a vendor-supported tool is to [create a framework tool](https://blog.ipspace.net/2018/05/why-is-network-automation-so-hard.html) that can be extended in any direction the customer wants. If you want to know how well that ends, look no further than [Enterprise Resource Planning](https://en.wikipedia.org/wiki/Enterprise_resource_planning):

* Small organizations use fixed-capability tools because they cannot afford a framework tool and adapt their processes to what the tool can do. Networking is different. When you find an enterprise networking team saying, "_we'll standardize our [network design](https://blog.ipspace.net/2013/04/this-is-what-makes-networking-so-complex.html) because we cannot afford to be a snowflake,_" please let me know.
* Large organizations buy ridiculously expensive framework tools like SAP or Oracle ERP and spend years adapting them to their unique environment.

Not surprisingly, the two well-known network automation framework products (tail-f, now Cisco NSO, and Apstra, now part of Juniper) are so expensive most organizations don't want to buy them and require tons of extra consulting services to adapt them to the customer requirements.

Then there's another snag: consulting services have a low margin and rely on experts who can quickly run away. Having a "_we'll build a framework tool and make money on consulting services_" business model will not get you funded or acquired. tail-f and Apstra were lucky exceptions because Cisco and Juniper desperately needed a believable SDN story.

Is there another way out of this conundrum? Of course, there is. [Quoting Gartner](https://www.gartner.com/en/documents/3446727) like a pro:

> This research shows that purposefully shifting network spend from products to personnel can lead to yearly savings of over 25% in five years while improving network agility, but network VPs and directors must reskill their organizations and foster a new mentality to achieve that.

However, I [wrote about the same topic](https://blog.ipspace.net/2013/03/where-is-my-vlan-provisioning.html) more than a decade ago, and it looks like nothing has changed in the meantime. I guess that's one of the Gartner reports no CxO ever wants to read (another one being "[long-distance vMotion sucks](https://www.gartner.com/en/documents/3869101)").
