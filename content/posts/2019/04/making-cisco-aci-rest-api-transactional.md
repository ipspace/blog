---
cli_tag: api-challenge
date: 2019-04-18 18:07:00+02:00
series:
- cli
tags:
- automation
- ACI
title: Making Cisco ACI REST API Transactional
url: /2019/04/making-cisco-aci-rest-api-transactional.html
---
*This is a guest blog post by [Dave Crown](https://twitter.com/_davecrown), Lead Data Center Engineer at the State of Delaware. He can be found automating things when he\'s not in meetings or fighting technical debt.*

---

In a [recent blog post](http://blog.ipspace.net/2019/04/rest-api-is-not-transactional.html), Ivan postulated "*You'd execute a REST API call. Any one of those calls might fail. Now what? \... You'll have absolutely no help from the orchestration system because REST API is not transactional so there's no rollback.*" Well, that depends on the orchestration system in use.

The promise of controller-based solutions (ACI, NSX, etc.) is that your unicorn powered network controller should be an all seeing, all knowing platform managing your network. We all have hopefully learned about the importance of backups very early on our careers. Backup and, more importantly, restore should be table stakes; a fundamental feature of any network device, let alone a networking system managed by a controller imbued with magical powers (if the vendor is to be believed).
<!--more-->
If we look at a traditional solution built around Junos, the steps should be pretty simple.

-   Determine our blast radius for the rollback
-   SSH in (or use a nifty ansible play) and run `rollback 1`

This works pretty well due to the way configs work on Junos. We could do the same thing with other platforms, by backing up the config first, attempt a change, determine the rollback blast radius, and then restore it. Under the covers, ACI is doing the same thing as a Junos rollback. The APIC (the controllers for ACI) compares the current state with selected config snapshot, then pushes out the changes to bring the fabric to the requested state. But for an omnipotent, magical controller, this shouldn't be hard.

This is actually pretty simple to do in ACI with Ansible due to the `aci_config_snapshot` and `aci_config_rollback modules. At the beginning of a play, call `aci_config_snapshot` with `state: present` and that will take a backup and, and store it on the controller. Then on failure, it's as simple as:

-   Get the config snapshots using `aci_config_snapshot` with `state: query` and register the results to a variable
-   Use `set_fact` to store your latest snapshot in a second variable
-   Call `aci_config_rollback` with your latest snapshot with `import_type: replace`

Putting an "*on any failure do X*" in an ansible play isn't feasible. I put this into a single play that can be executed from the command line on failure. Generally I don't like to have processes for people to follow that have conditional logic in them, but a condition of "*any issue*" and a single recovery step is acceptable. If you want to have Ansible Tower run your plays to configure ACI, breaking out the rollback is a necessity so that workflow can run it on any failure condition.

One thing I know I glossed over is how to find your latest snapshot. I did this with a custom filter plugin. Custom Jinja filter plugins are a very powerful tool in your Ansible toolbox. There are things that Ansible is very good at, and other things it is not. One thing it falls short on is handling complex data structures. Custom filters plugins let you drop into Python and bang out code without resorting to complex Jinja statements. This is especially nice when your only other option is an overly complex **jquery** statement embedded in Jinja. Another upside of using custom Python filters is moving the more "complex" logic into a single place to maintain that logic.

You may be wondering, "*Why don't I worry about the roll back blast radius?*" Simple: I start with the assumption that the running state of the fabric is one I found to be acceptable. The network was running well enough before I decided to change it. As ACI is managed as a single logical device from one control point, I don't need to determine which individual entities need to changed. Plus, we're talking about a physical data center fabric, where I shouldn't have a very high volume of configuration changes. The end result is I can treat the entire batch of changes as a single transaction, and rollback the entire batch at once.

I'm not saying Rest API driven platforms are great and are able to provide feature parity with platforms like Junos. I'd like to think The Rolling Stones were right, "You can't always get what you want, but if you try sometimes, you might find you get what you need." Understand and work with what your platforms and tools have available, and you can get close enough for government work.

---

Please note that Cisco ACI does not provide [*atomic transactions*](https://en.wikipedia.org/wiki/ACID_(computer_science)) as every API changes the state of the running system, and that you can do rollbacks mentioned by Dave only because ACI REST API implements *rollback* functionality. That functionality is not present in most other REST API implementations. - Ivan

On a totally different note, if you'd like to start automating your network but don't know how/where to start, check out our [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.
