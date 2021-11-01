---
title: "Even Simple Data Models Are a Huge Win"
date: 2021-11-03 07:04:00
tags: [ automation ]
pre_scroll: True
---
_[Dan Augustine](https://www.linkedin.com/in/dan-augustine/) sent me a wonderful example illustrating how even a very simple data model together with some automation templates can simplify a large-scale deployment._

---

We have a 100 router installation coming up for our schools and both of our installation vendors do not use open source templating tools and they are not willing to share. 

Having taken the [Data Models in Network Automation](https://my.ipspace.net/bin/list?id=AutConcepts#DATAMODELS) part of your [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar, I decided to install GitLab, make an Ansible project and invite our installation partners to the project. 
<!--more-->
While I have used a bit of GitHub, this was my first experience using GitLab and/or Ansible. Using your "[ansible examples](https://github.com/ipspace/ansible-examples)" GitHub repository allowed me to get started.  The hard part was the data model. After a few attempts, I was able to transform using `set_facts` so I could lessen the burden of the data model and device templates. 

Here's a sample YAML file describing a site:

```
site_name: Bret Harte Middle School
site_address: "123 Main St, Yourtown USA"
net_num: 199
ptp_index: 46
```

`net_num` populates all of the VLAN interfaces which are all components of 10.199.0.0/16, the loopback at 10.1.1.199 and the EBGP AS number. `ptp_index` finds the 46th PtP VLAN within an aggregate assigned for WAN point-to-point connections.  Using `ipmath`, I can calculate the interface addresses and BGP neighbors:

```
- hosts: all
  tasks:
  - set_fact:
      ptp_hub1_prefix: "{{ '10.192.14.0/24' | ansible.netcommon.ipsubnet(31, + hostvars[inventory_hostname].ptp_index) }}"
      ptp_hub1_hub_side: "{{ '10.192.14.0/24' | ansible.netcommon.ipsubnet(31, + hostvars[inventory_hostname].ptp_index) | ansible.netcommon.ipmath(0) }}"
      ptp_hub1_site_side: "{{ '10.192.14.0/24' | ansible.netcommon.ipsubnet(31, + hostvars[inventory_hostname].ptp_index) | ansible.netcommon.ipmath(1) }}"
      ptp_hub2_prefix: "{{ '10.192.15.0/24' | ansible.netcommon.ipsubnet(31, + hostvars[inventory_hostname].ptp_index) }}"
      ptp_hub2_hub_side: "{{ '10.192.15.0/24' | ansible.netcommon.ipsubnet(31, + hostvars[inventory_hostname].ptp_index) | ansible.netcommon.ipmath(0) }}"
      ptp_hub2_site_side: "{{ '10.192.15.0/24' | ansible.netcommon.ipsubnet(31, + hostvars[inventory_hostname].ptp_index) | ansible.netcommon.ipmath(1) }}"
      ptp_hub1_legacy_prefix: "{{ '172.30.0.0/23' | ansible.netcommon.ipsubnet(30, + hostvars[inventory_hostname].ptp_index) }}"
      ptp_hub1_legacy_hub_side: "{{ '172.30.0.0/23' | ansible.netcommon.ipsubnet(30, + hostvars[inventory_hostname].ptp_index) | ansible.netcommon.ipmath(1) }}"
      ptp_hub1_legacy_site_side: "{{ '172.30.0.0/23' | ansible.netcommon.ipsubnet(30, + hostvars[inventory_hostname].ptp_index) | ansible.netcommon.ipmath(2) }}"
      ptp_hub2_legacy_prefix: "{{ '172.30.2.0/23' | ansible.netcommon.ipsubnet(30, + hostvars[inventory_hostname].ptp_index) }}"
      ptp_hub2_legacy_hub_side: "{{ '172.30.2.0/23' | ansible.netcommon.ipsubnet(30, + hostvars[inventory_hostname].ptp_index) | ansible.netcommon.ipmath(1) }}"
      ptp_hub2_legacy_site_side: "{{ '172.30.2.0/23' | ansible.netcommon.ipsubnet(30, + hostvars[inventory_hostname].ptp_index) | ansible.netcommon.ipmath(2) }}"
      bgp_as: "65{{ '%03d' % net_num }}"
      slug: "{{ hostvars[inventory_hostname].inventory_hostname }}"
  - template:
      src: router_template.j2
      dest: "rendered_configs/{{inventory_hostname}}.cfg"
```

What's interesting is all of the partners are interested in using this approach with no pushback. I think we're at a point where there's an understanding that Ansible, Git and Python are all basic skills we need. 

I'm already working on a (more complex) data model for our VOIP system with our collaboration programmer and moved our technical standards to Markdown. This is seriously fun stuff. Thank you for the excellent course and look forward to the autumn update. 