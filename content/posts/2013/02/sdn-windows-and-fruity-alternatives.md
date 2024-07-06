---
comment: '“Openness” (for whatever value of “Open”) is another perceived benefit of
  SDN. In reality, you’re trading hardware vendor lock-in for controller vendor lock-in.

  '
date: 2013-02-05 06:42:00+01:00
sdn_101_tag: extra
series:
- sdn_101
series_weight: 90
tags:
- SDN
- OpenFlow
title: SDN, Windows and Fruity Alternatives
url: /2013/02/sdn-windows-and-fruity-alternatives.html
---
Brad Hedlund made a [pretty valid comment](/2013/01/nec-launched-virtual-openflow-switch.html?showComment=1359669279989#c3603529289800692734) to my "[*NEC Launched a Virtual OpenFlow Switch*](/2013/01/nec-launched-virtual-openflow-switch.html)*"* blog post: "On the other hand, it\'s NEC end-to-end or no dice", implicating the ultimate vendor lock-in.

Of course he's right and while, as Bob Plankers explains, you can never escape some lock-in ([part 1](http://lonesysadmin.net/2012/12/29/openstack-isnt-our-savior-from-lock-in-or-support-costs/), [response from Greg Ferro](http://etherealmind.com/response-openstack-isnt-our-savior-from-lock-in-or-support-costs-the-lone-sysadmin/), [part 2](http://lonesysadmin.net/2013/01/31/openstack-lock-in-support-costs-and-open-source-free-lunches/) -- all definitely worth reading), you do have to ask yourself "*am I looking for Windows or Mac?*"
<!--more-->
There are all sorts of arguments one hears from Mac fanboys (here's a [networking related one](https://web.archive.org/web/20121014054200/http://community.brocade.com/community/brocadeblogs/data_center/blog/2012/09/07/what-networking-needs-to-learn-from-steve-jobs)) but regardless of [what you think of Mac and OSX](/2011/11/macbook-air-mixed-feelings-or-is-it.html), there's the undisputable truth: compared to reloadful experience we get on most Windows-based boxes, Macs and OSX are rock solid; I have to reboot my Macbook every other [blue moon](http://en.wikipedia.org/wiki/Blue_moon). Even Windows is stable when running on a Macbook (apart from upgrade-induced reboots).

Before you start praising Steve Jobs and blaming Bill Gates and Microsoft at large, consider a simple fact: OSX runs on a tightly controlled hardware platform built with stability and reliability in mind. Windows has to run on [every possible underperforming concoction a hardware vendor throws at you](http://blog.fosketts.net/2013/01/07/microsoft-kill-craptops-destroy-windows/) (example: my "high-end" laptop cannot record system audio because Lenovo wanted to save \$0.02 on the sound chipset and chose the cheapest possible one), and has to deal with all sort of crap third-party device drivers loaded straight into the operating system kernel.

Now, what do you want to have in your mission-critical data center networking infrastructure: a Mac-like tightly controlled and vendor-tested mix of equipment and associated controller, or a Windows-like hodgepodge of boxes from numerous vendors, controlled by third-party software that might have never encountered the exact mix of the equipment you have.

If you're young and brazen (like I was two decades ago), go ahead and be your own system integrator. If you're too old and covered with vendor-inflicted scars, you might prefer a tested end-to-end solution regardless of what [Gartner says](https://www.information-age.com/when-two-vendors-are-better-one-gartner-123458431/) (and even solutions that vendor X claims were tested don't always work). Just don't forget to [consider the cost of downtime](http://erratasec.blogspot.com/2013/02/risk-analysis-v-downtime.html) in your total-cost-of-ownership calculations.
