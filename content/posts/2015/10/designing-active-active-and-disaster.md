---
date: 2015-10-02 09:45:00+02:00
dr_tag: intro
high-availability_tag: dr
series:
- dr
tags:
- design
- data center
- cloud
- high availability
title: Designing Active-Active and Disaster Recovery Data Centers
url: /2015/10/designing-active-active-and-disaster/
---
A year ago I was a firm believer in the unlimited powers of Software-Defined Data Centers and their ability to simplify workload migrations. After all, if you can use an API to create any data center object, what's stopping you from moving the workload running in a data center to another location.

As always, there's a huge difference between theory and reality.
<!--more-->
### Reality Distortion Field Has Failed

Being a slightly skeptical eternal optimist, I [created a workshop description](https://web.archive.org/web/20151002071446/http://info.interop.com/lasvegas/scheduler/session/simplifying-application-workload-migration-between-data-centers) for Interop Las Vegas 2015 which still sounded pretty positive and mentioned SDDC as a potential solution.

In December 2014, the reality hit... hard. I was running a [workshop](http://www.ipspace.net/Customized_webinars) for a global organization that was sold on a simple idea: using SDDC (from the vendor that created the acronym) it's easy to pick up your toys (= application workload), pack them in a large bag, walk away to a different sandbox (= public cloud), drop them out of the bag and continue playing.

During the workshop we identified numerous obstacles and missing orchestration components, and concluded that it's totally impossible to achieve what they planned to do. The best they could do at that time was to *manually* recreate network infrastructure (= subnets) and services (= firewalls and load balancers) in a second virtualized environment (disaster recovery data center or public cloud), and afterwards restart VMs from the failed data center in that cloud.

The *only* approach that would do what my customer wanted at that time was automated application deployment using tools like [Cloudify](http://getcloudify.org/), but that solution was further away from their grasp than Alpha Centauri -- they were a traditional enterprise IT shop with manual non-repeatable server creation and application deployment processes.

After three days we had to conclude that there's nothing SDDC could do for them to solve their immediate workload migration problems, and that they should focus on [automating application development and deployment processes](/2013/11/typical-enterprise-application/) (yeah, I know I [sound like Captain Obvious](/2014/09/youve-been-doing-same-thing-for-last-20/)).

{{<note>}}Combining NSX-T and SRM might be a step in the right direction, but I never read the documentation to find out the potential "minor" details.{{</note>}}

### Adjusting to Reality

Based on that traumatic experience, I decided to refocus my Interop presentation on *what works now in real life* and not surprisingly the best answer is "[proper application architecture](https://www.ipspace.net/Load_Balancing_and_Scale-Out_Application_Architectures)".

Anyway, the Interop workshop documented numerous challenges you might encounter on your journey (including finite bandwidth, non-zero latency, unpredictable failures, bad application architectures, vendors promoting obviously-stupid things), and resulted in a [fantastic experience for the attendees](http://www.informationweek.com/interop/top-eight-workshops-from-interop-las-vegas-/d/d-id/1320393) even though the workshop was just before the evening party and I ran way overtime.

An updated version of that workshop is now available as a webinar with a more appropriate title: [Designing Active-Active and Disaster Recovery Data Centers](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar.
