---
date: 2017-10-09 08:48:00+02:00
high-availability_tag: app
tags:
- design
- data center
- high availability
title: Solving the Problem in the Right Place
url: /2017/10/solving-problem-in-right-place/
---
Sometimes I have this weird feeling that I'm the only loony in town desperately preaching against the [stupidities heaped upon infrastructure](/2013/04/this-is-what-makes-networking-so-complex/), so it's really nice when I find a fellow lost soul. This is what another senior networking engineer sent me:

> I\'m belonging to a small group of people who are thinking that the source of the problem are the apps and the associated business/security rules: their nature, their complexity, their lifecycle\...

Sounds familiar (I probably wrote a [few blog posts](/2013/11/typical-enterprise-application/) on this topic in the past), and it only got better.
<!--more-->
> You could add the maximum agility at every layer and the orchestrator of your dream, it would not change the complexity of an app. and its security (and small networking) requirements.
>
> The vast majority of the traditional apps was and still is designed with a scale-up and infrastructure redundancy approaches:
>
> -   Layer-2
> -   Networking issues generate application disruption : configurations freezes, few software updates
> -   Security is managed by the infrastructure: firewalls and segmentation
>
> Modern Applications are designed with a scale-out approach:
>
> -   Born to be deployed in-house or moved into the cloud
> -   Layer-3 and DNS are theoretically sufficient
> -   Fail-Fast, rollback, incremental data model
> -   Security is managed by the applications: hardening, centralized filtering, patching (hot and cold), fast-restart, self-healing
>
> IMHO, if new apps are deployed with the 2nd approach (in the cloud or in-house), life would be much more easy for infrastructure industrialization, automation and \"intent-based\" thing stuff.

Amen.

Not surprisingly, some vendors vigorously disagree, particularly if they're selling the Aspirin to reduce the headaches of "traditional" app brokenness. On a more optimistic front, even engineers working for said vendors [sometimes see the light](http://www.it20.info/2014/12/cloud-native-applications-for-dummies/)... and eventually [move on](http://www.it20.info/2017/09/so-long-vmware-hello-aws/).

### Want to Know More?

Some network engineers found my [*Designing Active-Active and Disaster Recovery Data Centers*](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar pretty useful when trying to persuade everyone else not to implement vendor marketectures.