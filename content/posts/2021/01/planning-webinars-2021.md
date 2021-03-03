---
title: "Webinars in 2021"
date: 2021-01-11 07:02:00
lastmod: 2021-03-03 17:41:00
tags: [ training ]
series: coffee-break
---
After [deciding to take a slightly longer coffee break](/2021/01/planning-coffee-break.html) I went through the list of outstanding projects trying to figure out which ones I could complete in first half of 2021, which ones I'll get to "eventually" and what's a lost cause.

### Guest Speakers

[Irena](https://www.ipspace.net/Team:Irena_Marcetic) is telling me that I should stop inviting guest speakers -- our calendar is full until June 2021. Here's what we have planned and what we got done at the time of the last update ({{<lastmod>}}).
<!--more-->
* Deep dive into [NSX-T Federation](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) by [Jerome Catrouillet](https://www.ipspace.net/Author:Jerome_Catrouillet) is [complete](https://my.ipspace.net/bin/list?id=NSX#FEDERATION), and concludes the NSX-T 3.0 update process.
* In the [Kubernetes Deep Dive](https://www.ipspace.net/Kubernetes_Networking_Deep_Dive) webinar we already covered basics, services, and details of Container Network Interface. Next on the list: service mesh.
* We still have several sessions of [Cisco ACI Deep Dive](https://www.ipspace.net/Cisco_ACI_Deep_Dive) to do.
* [Rachel Traylor](https://www.ipspace.net/Author:Rachel_Traylor) started an [intensive course on reliability theory](https://www.ipspace.net/Reliability_Theory:_Networking_through_a_Systems_Analysis_Lens)
* [Jason Belk](https://www.linkedin.com/in/jason-b-4ab11635/) will redo the NETCONF/YANG material and add RESTCONF to the mix
* [Dinesh Dutt](https://www.ipspace.net/Author:Dinesh_Dutt) will talk about IP routing in 3-tier leaf-and-spine topology

### Webinar Updates

There are a few things I simply have to update to feel good (last status update on {{<lastmod>}}):

* [Networking part](https://my.ipspace.net/bin/list?id=Cloud101#NET) of *[Introduction to Cloud Computing](https://www.ipspace.net/Introduction_to_Cloud_Computing)* webinar is complete.
* Ansible webinar already got updated material on task includes, roles, collections ([published](https://my.ipspace.net/bin/list?id=Ansible#INCLUDES)). I will also redo the section on Ansible debugger, and add a short intro to Jinja2 includes. I won't however waste any more time describing their [N+1-st attempt to get networking modules right](https://my.ipspace.net/bin/get/Ansible/Errata-Network-Overview.md?doccode=Ansible).
* The [network automation curriculum](https://www.ipspace.net/Roadmap/Network_Automation_webinars) is pretty well rounded, what's missing is a [deep dive into network automation concepts](https://www.ipspace.net/Network_Automation_Concepts) (infrastructure-as-code, data models, data stores, single source of truth, intent-based networking...). We started with [data models](https://my.ipspace.net/bin/list?id=AutConcepts#DATAMODELS), more to come in late spring/early summer.
* Gateway Load Balancer has to be added to AWS webinar.
* Virtual Hub has to be added to Azure webinar.
* [Miha Markočič](https://www.ipspace.net/Team:Miha_Markocic) has developed [tons of AWS new automation examples](https://blog.ipspace.net/2021/01/aws-networking-automation-examples.html) (already published).
* I have to add more *recommended design* information to [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar
* The description of *[configuration and state management automation tools](https://my.ipspace.net/bin/list?id=NetTools#CONFIG)* is out of date -- an update is planned for late spring

### Long-term Projects

I will keep working on *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar. The current plan is to cover the details of routing protocols including fun stuff like LFA, rLFA, TI-LFA, PIC, NSF, SSO.. 

I will also add HTTP/2, HTTP/3 and QUIC to the *[TCP, HTTP and SPDY](https://www.ipspace.net/TCP,_HTTP_and_SPDY)* webinar. I will get it done -- I just don't know when it might happen.

### Potential Update Candidates

These webinars would deserve an update, but I won't make any promises:

* [VXLAN Technical Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive) would need a major rewrite. It still mentions NSX-MH and Nexus 1000v
* [Introduction to Virtualized Networking](https://www.ipspace.net/Introduction_to_Virtualized_Networking) is in no better shape
* [Network Function Virtualization](https://www.ipspace.net/Network_Function_Virtualization) webinar would need an update on fast packet switching in Linux. If only I'd be able to persuade Thomas Graf to do it ;)
* [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers) needs an update of the *[Network Reference Architecture](https://my.ipspace.net/bin/list?id=DC30#NETWORKING)* section (and no, I will **not** touch the storage part of it)

What I *can* promise is that I WILL NOT spend any more time going through the vendor data sheets to update the *product overview* parts of [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics). Creating those updates was one of the worst content creation experience I ever had.

### Not Going to Happen

I had a few more ideas on the back burner. They might happen in another lifetime ;)

* OpenStack Networking
* Open Networking on Linux
* BGP Security and MANRS

Have I missed anything? Please send me an email (if you're a subscriber you know how to reach me, otherwise use the *Contact* form).

### Revision History

2021-03-03
: * Introduction to cloud networking is complete.
  * Reliability course has started.
  * Data models part of automation concepts is mostly complete, more to come in late spring.
  * Kubernetes Deep Dive is progressing nicely.

2021-01-30
: Updated with a few more things to fix found in January 2021
  * Have to add Virtual Hub to Azure webinar
  * Ansible webinar needs an updated _debugging playbooks_ section.
  
  Status update:
  * We completed NSX-T federation sessions in January.
  * Ansible _Creating Reusable Code_ section has been updated.
  * We have the final webinar outline for _Automation Concepts_ and extensions to _Reliability Theory_.
  * Miha Markočič completed AWS examples.


