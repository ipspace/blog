---
date: 2013-03-27 06:41:00+01:00
tags:
- SDN
- data center
- LAN
- virtualization
title: What Did You Do to Get Rid of Manual VLAN Provisioning?
url: /2013/03/what-did-you-do-to-get-rid-of-manual.html
---
I love(d) listening to the Packet Pushers podcast and came to expect the following rant in every SDN-focused episode: "*I'm sick and tired of using CLI to manually provision VLANs*". Sure, we're all in the same boat, but did you ever do something to get rid of that problem?
<!--more-->
After all, you don't need more than a few tens of VLANs in a typical enterprise data center or private cloud (clouds with thousands of tenants are obviously a totally different story) and most vendors have some sort of [VMware-focused automatic edge port VLAN provisioning](/2011/12/vm-aware-networking-improves-iaas-cloud.html), from on-switch solutions like [VM Tracer (Arista)](/2011/06/automatic-edge-vlan-provisioning-with.html) or Automatic Migration of Port Profiles (Brocade) to network management applications (like Junos Space). Are you using them? If not, why not? What's stopping you?

But let's assume you're unfortunate and use switches that have no hypervisor integration tools. Would it be THAT hard to write an [application that would read the LLDP or CDP tables](/2011/08/vm-fex-how-convoluted-can-you-get.html) on ToR switches (populated by LLDP or CDP updates from the vSphere hosts), build a connectivity table, and allow server/hypervisor administrators to provision their own VLANs (within limits) on server-facing switch ports? I know that an intern could do it in a week (given reasonably complete functional specs), but we never did it, because doing automatic VLAN provisioning simply wasn't worth the effort.

Assuming we're truly sick-and-tired of manual VLAN provisioning in enterprise data centers, there must be other reasons we're not deploying the vendor-offered features or rolling out our own secret sauce. It might have to do with the critical impact of the networking gear.

Let's assume you manage to mess up a server configuration with Puppet -- you lose a server, and hopefully you're using a cluster or a scale-out application, so the impact is negligible.

If a vSphere host crashes, you lose all the VMs running on it. That could be 50-100 VMs if you're using recent high-end server, but if you care about their availability, you have an HA cluster and they get restarted automatically.

Now imagine the vendor-supplied or home-brewed pixie dust badly misconfigures or crashes a ToR switch. Worst case (switch hangs and links to servers are not lost), you lose connectivity to tens of physical servers, which could mean a few thousands VMs; best case those same VMs lose half the bandwidth.

Faced with this reality, it's understandable we're scared of software automatically configuring our networking infrastructure. Now please help me understand how that's going to change with third-party SDN applications.

## More Details

I'm describing various VM-aware networking solutions in numerous [webinars](http://www.ipspace.net/Webinars), including [Introduction to Virtual Networking](http://www.ipspace.net/Introduction_to_Virtualized_Networking), [VMware Networking Technical Deep Dive](http://www.ipspace.net/VMware_Networking_Deep_Dive), [Cloud Computing Networking](http://www.ipspace.net/Cloud_Computing_Networking) and [Data Center Fabric Architectures](http://www.ipspace.net/Data_Center_Fabrics).

