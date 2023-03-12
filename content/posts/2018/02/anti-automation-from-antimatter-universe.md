---
cli_tag: fail
date: 2018-02-26 09:08:00+01:00
series:
- cli
series_weight: 2000
tags:
- automation
- firewall
title: Anti-Automation from the Antimatter Universe
url: /2018/02/anti-automation-from-antimatter-universe.html
---
One of my readers sent me a vivid description of his interactions with one of the so-called next-generation firewall vendors. Enjoy!

---

We're using their highly promoted Next Generation Firewall (NGFW) management solution. New cutting edge software, centralized manager... but no CLI for configuration (besides some initial bootstrap commands). \"*You don\'t need that because everything is managed from our centralized manager GUI*\", says \$vendor sales managers.
<!--more-->
After clicking dozens of settings via manager GUI, reference setup is prepared for NGFW appliance.

Having multiples sites with similar architecture, we would like to replicate setup for another NGFW appliances. A perfect automation case: change a few input parameters, produce rest of the typical configuration.

Ouch. CLI is not supported. Forget Python or Ansible.

Even worse: configuration templates or configuration cloning is not supported in centralized manager GUI. \"*Good idea, please create enhancements request*\", says \$vendor sales managers. \"*And by the way we have REST API support in our centralized manager*\"

OK, sounds acceptable. After wasting hours and opening numerous TAC cases, it appears that:

-   There's \~30% feature parity between REST API and GUI configuration options. You still need to tweak majority of the configuration manually in manager GUI.
-   Even for configurable parameters not all REST API methods are supported. For example, to update an Object List to add a new host, you need to download the whole Object List, parse and modify its JSON structure, and upload the whole list with another REST API call. A single mistake and your list is gone.

Here's the result of a long discussion with \$vendor engineers:

> Currently our REST API implementations is very raw. We don\'t recommend to use it in production. We're accepting all your observations and will work toward improving the API. Stay tuned and check the next SW releases

Let's not comment how our team is feeling at this moment...

### Going Further

So we manually (clicking madness) replicated configuration to other appliances. We're making progress, everything is fine... until you have your first NGFW appliance hardware failure.

According to the RMA procedure, a new appliance is shipped and replaces the failed one. You set some initial settings to pair it with the centralized manager.

Configuration from the failed appliance is already in the centralized manager. You just need to sync/deploy it... but nothing happens. You get multiple error messages. Documentation is silent.

Then you get this explanation after lengthy investigation by \$vendor TAC:

> Currently it is not possible to Sync/Deploy config from centralized manager to replaced appliances due to some internal reasons, which we cannot disclose. As workaround please delete all configuration from manager and implement all from the scratch, as during new implementation. Please don\'t forget to make dozens of screen shots with existing configuration options

You could guess how our team is feeling after this revelation.

After long discussions with \$vendor sales engineers they tell us: \"*We understand your frustration, we indeed registered some enhancements request. Based on priorities, they will be implemented*\"

---

### I Couldn't Resist Adding...

And this is what happens when you buy things based on glitzy PowerPoint without [ever considering what you should ask for to make your operations easier](https://blog.ipspace.net/2016/10/network-automation-rfp-requirements.html).

Next step: CxO (who made the purchasing decision in the first place) will complain how expensive his internal security and networking teams are.

I also sent a draft of this blog post to my friends working in the security industry and one of them replied:

> I don't understand why some vendors actually believe that CLI's will die. I think their vision of automation is a monkey trained to click certain sequences of GUI buttons to get to a banana...

As we all know it's not just the vendors. So-called thought leaders with zero operational experience are no better.

#### But Wait, That's Not All

Finally, the icing on the cake. The same reader sent me this gem a few days after the original email:

> We asked the vendor: "Could you please officially share other customers' experience with us?"
>
> Their answer: "No, because that would affect our business"

Now you know how some players in this industry work.

#### But Wait, There's Even More

Got more feedback from another unhappy customer (probably using the same gear). Here it is:

---

Allow me to add my experiences with \$vendor and his \$product (I had a look at all releases starting from 6.0 to the first 6.2 releases in the course of about 2015-2017):

-   Management access is utterly slow, needs an awful lot of resources to run just below an acceptable speed baseline,
-   The whole thing is a huge pile of bugs in runtime as well as management code,
-   Numerous TACs, often taking weeks to resolve one issue,
-   Essentially no help in \$vendor forums (often discussions cease with "open a TAC").

\$vendor bought \$product with the acquisition of \$company some years ago and struggles since then to get the whole pile transformed to something I could recommend to customers with good faith.

On the other hand, I had contact with some techs at \$vendor and they are competent and know how to diagnose problems.

The best part (for \$vendor) is that \$vendor charges customers money (via a so called \"support contract\") for allowing customers to help finding and (hopefully) fixing bugs the software shouldn\'t have in the first place. At least not in the given amount.

Looking at the base FW (without the shiny NG): it's mature, has a lot less of features in comparison but is reasonably stable.

Seems to be a good lesson in how to upset customers.
