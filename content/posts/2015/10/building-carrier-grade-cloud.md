---
date: 2015-10-06 08:05:00+02:00
ha-cloud_tag: private
high-availability_tag: cloud
series:
- ha-cloud
tags:
- design
- cloud
- high availability
title: Building Carrier-Grade Cloud Infrastructure
url: /2015/10/building-carrier-grade-cloud.html
---
During one of my [SDN workshops](http://www.ipspace.net/SDN,_OpenFlow_and_NFV_Workshop), an attendees asked me "*How do you build carrier-grade (5 nines) cloud infrastructure with VMware NSX?*"

**Short answer**: You don't... and it's a wrong question anyway.
<!--more-->
### Before Delving into Details (aka Disclaimer)

This is not an NSX-related blog post. It just happened that the attendee tried to accomplish the Mission Impossible with NSX. He could have chosen Juniper Contrail or Nuage VSP or anything else while facing the same pointless task.

### The Problem

I've encountered two compute infrastructure products that were probably close to what people call [*carrier-grade*](https://en.wikipedia.org/wiki/Carrier_grade) in my days -- IBM mainframes and Tandem minicomputers. Both were incredibly complex and expensive, and ran short user-written transactions on top of fully redundant software and hardware infrastructure.

It's impossible to reproduce the same feat in an Infrastructure-as-a-Service cloud environment because the workload isn't composed of short ACID transactions but of servers of unknown quality. You *might* be able to build a cloud infrastructure with [5-nine reliability](https://en.wikipedia.org/wiki/Five_nines), but it would be a totally wasted effort if the workload running on top of it crashes (or is brought down for patching). See also [High Availability Fallacies](http://blog.ipspace.net/2011/08/high-availability-fallacies.html) for more details.

The only way to build a solution with more than 99.9% availability is ([according to James Hamilton](https://youtu.be/JIQETrFC_SQ?t=18m50s)) to build an application-layer solution running in multiple availability zones, and once you do that, you don't care that much about the availability of individual zones as long as it's reasonably high.

### Building Carrier-Grade Infrastructure

Twenty-five years ago we had simple routers and switches, and we knew how to build resilient networks with redundant boxes and routing protocols. Then the traditional service providers learned how to spell IP and wanted to implement their existing operational practices in this brave new world... prompting the networking vendors to build increasingly complex infrastructure products like redundant supervisors, non-stop forwarding, and [in-service software upgrade](http://blog.ipspace.net/2015/06/so-you-need-issu-on-your-tor-switch.html).

Guess what -- complex products tend to be expensive to build and operate. The carriers complaining about high cost of the networking gear and lustfully looking at what Google, Facebook, Amazon and Azure are doing should stop yammering and admit that they got what they asked for.

{{<note info>}}Randy Bush [talked about this problem more than two decades ago](https://www.nanog.org/meetings/nanog26/presentations/bushcomplex.pdf), but of course nobody listened.{{</note>}}

Obviously some people never learn, and now that the carriers turn their attention toward the new fad -- Network Function Virtualization -- they want to repeat the same mistake, and want cloud architects to build carrier-grade infrastructure on which they'll run unreliable workloads.

{{<quote source="Definitely not Einstein">}}**Insanity**: doing the same thing over and over again and expecting different results.{{</quote>}}

### The Way Forward

The more I look at what various organizations are doing (and succeeding or failing along the way), the more I'm convinced that there's only way to reduce the overall costs of running your IT infrastructure:

-   Set realistic goals based on actual business needs;
-   Build good enough infrastructure that is easy to operate at reasonable costs;
-   Build the few applications that actually need very high availability (not everything needs five nines) using modern design-for-failure architectural principles. See also [Cloud Native Applications for Dummies](http://it20.info/2014/12/cloud-native-applications-for-dummies/).

Numerous large-scale companies have proven that this approach works, but of course it requires a major change in the way your company develops and deploy applications.

You could also decide to ignore this trend and continue building [ever](http://blog.ipspace.net/2014/10/vxlan-and-otv-saga-continues.html) [more](http://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html) [complex](http://blog.ipspace.net/2015/09/vsan-as-always-latency-is-real-killer.html) infrastructure, and [get the results you deserve](http://blog.ipspace.net/2013/09/sooner-or-later-someone-will-pay-for.html).

### Want to know more?

You might find some answers in my [Designing Private Cloud Infrastructure](http://www.ipspace.net/Designing_Private_Cloud_Infrastructure) or [Designing Active-Active and Disaster Recovery Data Centers](http://www.ipspace.net/Designing_Private_Cloud_Infrastructure) webinars, or maybe what you need is a [more comprehensive overview of data center networking](http://www.ipspace.net/Roadmap/Data_center_webinars).
