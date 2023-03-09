---
date: 2014-11-03 07:24:00+01:00
ha-cloud_tag: private
high-availability_tag: cloud
series:
- ha-cloud
tags:
- design
- data center
- cloud
- high availability
title: Use a Disaster Recovery Project to Build Your New Cloud
url: /2014/11/use-disaster-recovery-project-to-build.html
---
It doesn't make sense to build a new data center network to support legacy bare-metal server infrastructure. You'll have to use relatively expensive 1G/10G ports to be able to connect the current and future servers, and once the server and virtualization engineers wake up and do hardware refresh you'll end up with way too many ports (oh, and you do know that transceivers could cost more than the switching hardware, right?).
<!--more-->
In the ideal case, you'd build a new infrastructure with high-density servers, 100% virtualized workload... and [then all you'd need would be two 1RU or 2RU ToR switches](http://blog.ipspace.net/2014/10/all-you-need-are-two-top-of-rack.html). Unfortunately most organizations can't find their path from *here* to *there* due to tons of internal red tape (aka *budgets* and *depreciation period*).

[Eric Hanselman](https://www.linkedin.com/in/erichanselman/) (then at 451 Research) provided an interesting way out of this Catch-22 during one of the Interop panels:

-   Start a *disaster recovery* project;
-   Rent space at a colocation facility ([hat tip to Rick Parker](http://blog.ipspace.net/2014/09/open-source-hybrid-cloud-reference.html));
-   Build your disaster recovery infrastructure over there;
-   Move the workload, declare success, and shut down the legacy infrastructure;
-   Start another disaster recovery project ;)

Obviously you'd want the new infrastructure to be as forward-looking as your organization feels comfortable with. [High-density servers](http://blog.ipspace.net/2014/09/building-small-cloud-with-ucs-mini.html) (each of them hosting 50 -- 100 VMs) are a no-brainer, virtualized [network services appliances](http://blog.ipspace.net/2013/04/virtual-appliance-performance-is.html) are already a harder sell because they might require [changes](http://blog.ipspace.net/2014/09/youve-been-doing-same-thing-for-last-20.html) in [processes](http://blog.ipspace.net/2013/11/typical-enterprise-application.html) and [responsibilities](http://blog.ipspace.net/2013/12/omg-who-will-manage-all-those-virtual.html) if you want to do them right, and distributed file system (like Nutanix or [VSAN](http://blog.ipspace.net/2014/08/vmware-evorail-one-stop-shopping-for.html)) might turn out to be mission impossible, because, you know, [storage](http://blog.ipspace.net/2010/08/storage-networking-is-different.html).

### More details

Design aspects of modern cloud infrastructure are covered in my [*Designing Private Cloud Infrastructure*](http://www.ipspace.net/Designing_Private_Cloud_Infrastructure) webinar and [*Data Center Design Case Studies*](http://www.ipspace.net/Data_Center_Design_Case_Studies) book (included with the webinar); other [Cloud Infrastructure and SDDC](http://www.ipspace.net/Roadmap/Cloud_computing_webinars) webinars give you the technology details you'll need to understand the design tradeoffs.