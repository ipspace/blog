---
title: "Lessons Learned: Automating Site Deployments"
date: 2020-12-08 07:18:00
tags: [ automation ]
series: [ niac ]
niac_tag: solution
---
Some networking engineers renew their ipSpace.net subscription every year, and when they drop off the radar, I try to get in touch with them to understand whether they moved out of networking or whether we did a bad job.

One of them replied that he retired after building a fully automated site deployment solution (first lesson learned: you're never too old to start automating your network), and graciously shared numerous lessons learned while building that solution.
<!--more-->
---
The automation project was my 30 year career capstone and caused me to split with $vendor. While it was obvious to me that we need a centralized management controller I just couldn’t get into their $lanproduct and SDWAN. I focused on Ansible despite it being sooo slooow when looping. I also learned that process was more important than the actual automation tool. Here are some other cool things I learned along the way:

* Separate out the data from the code
* Version control with pull request workflow was key. I had Git repos for the data (CSV files), the code (Ansible playbooks), and the scripts (convert CSV files into INI inventory sources and other misc tasks)
* Develop the code with virtual devices. Test on actual hardware with the actual SW release (one each of every piece of hardware) then promote to production... NO MATTER HOW SMALL each code change seemed to be.
* Use standardized architecture. No reason to use most of the fancy knobs. Those problem can be better solved using simplified standard architecture.
* No more going into the CLI and “winging it”. Reliability shot way up
* Zero touch was over rated. I used automation to create  “bootstrap files” that our reseller loaded on the box (by serial number) before we shipped them overseas. The bootstrap file was the minimum necessary config to allow me/automation to ssh into the box. I heavily used configuration rollback or configuration change confirmation. 
* A single authoritative source of truth was key and we struggled with that. We ended up using spreadsheets under version control. I ran a separate dynamic inventory source project to test ServiceNow CMDB. We got it to work only to find out that the data was junk. I think CMDB is the way to go in the long term, but the amount of effort to remediate the data was overwhelming. I had to move on. Perfect is the enemy of done.
* I used Ansible roles for every CLI stanza
* I really liked YANG. If I had to do this again, I would do more experimenting with RESTCONF and YANG. That would solve the cruft problem. I know there was the vendor-versus-standard data model problem but I think I could overcome that with the DevOps and Git methodology. I might have tried to do this  outside of Ansible, but was concerned with supportability after I left
 
Anyway, I wanted to sincerely thank ipSpace.net for the webinars. You are making a big difference (for those who choose to learn and broaden their skills by asking “_why_”). I used your material extensively in learning Ansible and broadening my architectural skill set.