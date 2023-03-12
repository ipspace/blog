---
title: Single Source of Truth (SSoT) in Network Automation
layout: custom
minimal_sidebar: true
sidebar_box: NetOps
---
{{<quote source="ChatGPT explaining SSoT">}}Single source of truth (SSOT) in network automation refers to a centralized and authoritative data repository that holds all the information required for network management and operation. It ensures that every network device or system uses the same accurate and up-to-date information to perform its tasks, eliminating inconsistencies and errors caused by outdated or conflicting data. SSOT enables efficient and reliable network automation by providing a unified view of the network and allowing for quick and informed decision-making.{{</quote>}}

{{<plushy confused>}}Not too bad for a statistical model that has no idea what it's talking about, right? Now for the crucial question: how exactly should one reach that holy grail?

{{<series-listing tag="build">}}

### Implementation Details

{{<plushy master>}}Ready for a deep dive into the interesting details? Off we go...

{{<series-listing tag="details">}}

### Sample Solutions

{{<plushy magic>}}Want a few success stories? Here we go:

{{<series-listing tag="solution">}}

You might also enjoy the solutions built by attendees of [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course:

-   Nicky Davey [automated large-scale DMVPN rollout](https://blog.ipspace.net/2018/04/configuration-templating-could-be-huge.html)
-   David Varnum [created a solution that deploys VXLAN/EVPN infrastructure, and layer-2 and layer-3 service in Arista EOS fabric](https://github.com/varnumd/ansible-arista-evpn-lab)
-   Valter Milanese and Emanuele Ballarini [automated VXLAN/EVPN deployment on Cisco Nexus switches](https://github.com/ipspace-netautomationlab/net-automation-lab), including pre- and post-deployment validation and **error recovery** with cleanup and configuration rollback.
-   Stephen Harding started with a [full-blown data center fabric solution](https://github.com/sjhloco/ip_auto_lab/tree/master/data_model) based on minimalistic data model that is expanded on-the-fly with a dynamic inventory script, evolved it into one of the best [data center fabric automation solutions](https://github.com/sjhloco/build_fabric) I've seen, and documented it in a [long series of must-read blog posts](https://theworldsgonemad.net/2021/automate-dc-pt1/).
-   Adrian Giacommetti [migrated Cisco ACI tenant networking into Oracle cloud](https://blog.ipspace.net/2020/10/automation-win-aci-public-cloud.html)

Want even more ideas? Check out the [solutions showcase](https://www.ipspace.net/NetAutSol/Solutions).

### More Information

{{<plushy happy>}}You'll find more details in the [Single Source of Truth](https://my.ipspace.net/bin/list?id=AutConcepts#SSOT) part of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.

Several presenters in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course implicitly described how they built the single source of truth when describing their automation solutions:

* [Sander Steffann](https://www.ipspace.net/Author:Sander_Steffann) integrated [NetBox, GitLab, and Ansible](https://my.ipspace.net/bin/list?id=xNetAut204#TOOLCHAIN).
* [Kurt Wauters](https://www.ipspace.net/Author:Kurt_Wauters) and [Wim De Hul](https://www.ipspace.net/Author:Wim_De_Hul) presented an [automation solution used in the large wholesale carrier](https://my.ipspace.net/bin/list?id=xNetAut204#WHOLESALE).
* [Damien Garros](https://www.ipspace.net/Author:Damien_Garros) explained [how to build a network automation framework from the ground up](https://my.ipspace.net/bin/list?id=xNetAut193#SRCTRUTH).
* [Dirk Feldhaus](https://www.ipspace.net/Author:Dirk_Feldhaus) described how to [automate service deployment with Ansible](https://my.ipspace.net/bin/list?id=xNetAut183) within a network fabric to make the implementation faster, more consistent and less error-prone.
* [Mark Prior](https://www.ipspace.net/Author:Mark_Prior) described how he [automated a private cloud infrastructure](https://my.ipspace.net/bin/list?id=xNetAut181#INFRA_AS_CODE), and how he uses infrastructure-as-code principles to build reliable data center networking infrastructure.
