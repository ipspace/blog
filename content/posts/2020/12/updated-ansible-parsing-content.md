---
title: "Updated: Getting Network Device Operational Data with Ansible"
date: 2020-12-07 07:19:00
tags: [ Ansible, automation ]
---
Recording the same content for the third time because [software developers decided to write code before figuring out what needs to be done](https://blog.ipspace.net/2019/09/measure-twice-cut-once-ansible.html) is disgusting... so it took me a long long while before I collected enough willpower to rewrite and retest [all the examples](https://github.com/ipspace/NetOpsWorkshop/tree/master/Ansible/Networking/Get-Operational-Data) and re-record the *[Getting Operational Data](https://my.ipspace.net/bin/list?id=Ansible#NET_DATA)* section of *[Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers)* webinar.

The new videos explain how to consume data generated in JSON or XML format, and how to parse the traditional **show** printouts. I dropped mentions of (semi)failed experiments like Ansible **parse_cli** and focused on things that work well: TextFSM, in particular with **ntc-templates** library, pyATS/Genie, and TTP. On the positive side, I liked the slick new **cli_parse** module... let's hope it will stay that way for at least a few years.

On a totally unrelated topic, I realized (again) that *fail fast, fail often* sounds great in a VC pitch deck, and sucks when you have to deal with its results.