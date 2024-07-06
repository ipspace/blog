---
title: "Vendor Marketectures in Real Life"
date: 2020-09-21 06:32:00
tags: [ virtualization, vMotion ]
---
Remember my rants about [VMware](/2020/02/live-vmotion-into-vmware-on-aws-cloud.html) and [firewall vendors](/2019/11/stretched-vlans-and-failing-firewall.html) promoting crazy solutions that work best in PowerPoint and cause more headaches than anything else (excluding increased vendor margins and sales team bonuses, of course)? 

Here's another _we-don't-need-all-that-complexity_ real-life story coming from one of my long-term subscribers:
<!--more-->
- - -

My client runs VMware NSX on top of a Nexus BGP EVPN with VXLAN network. We manage the physical network and a 3rd party manages the NSX. The 3rd party come from a VMware background and are not as strong on networking. They are using NSX-V and are about to deploy pockets of NSX-T, but NSX-V will be around for a while. 

The problem I have is they have deployed NSX-V in an active active DC design which was causing all sorts of asymmetrical routing horribleness that was upsetting the firewalls, whilst pushing all this complexity down to the physical network to resolve.

Long story short I armed myself with the facts thanks to your webinars, called a meeting and now all the stakeholders agree we need to migrate to an active/standby design, simplifying it greatly. I’m not taking all the credit for it as the 3rd party eventually came to the same conclusion as me, but it helped me build more credibility with my customer. Thanks again for making me look good ;)

- - -

Here are some ipSpace.net resources he might have used in the process:

* [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers)
* [NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)
* Disaster recovery-related blog posts
