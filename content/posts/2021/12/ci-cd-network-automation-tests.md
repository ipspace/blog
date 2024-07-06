---
title: "What Are You Going to Test in Network Automation CI/CD Pipeline?"
date: 2021-12-08 07:25:00
tags: [ automation ]
series: [ cicd ]
cicd_tag: testing
---
Network automation [CI/CD pipeline](https://en.wikipedia.org/wiki/CI/CD) seems to be the next hot thing, with [vendors](https://techfieldday.com/video/arista-next-generation-automation-architectures/) and [bloggers](https://juliopdx.com/2021/10/20/building-a-network-ci-cd-pipeline-part-1/) describing in detail how you could get it done. How realistic is that idea for an average environment that's barely starting its automation journey? 

**TL&DR**: it will take a long time to get there, and lack of tests is the first showstopper.
<!--more-->
Starting with the basics: [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration) is "_the practice of merging developer working copies to a shared mainline several times a day_,"... and the merge process should include rigorous tests unless you want to see a badly broken mainline environment daily.

[Continuous deployment](https://en.wikipedia.org/wiki/Continuous_deployment) adds automated deployments to the mix, and rigorous testing becomes even more critical. You wouldn't want to break your production environment every time you deploy a change, would you?

Coming back to network automation: what tests could you run before merging and deploying changes? If you're developing a network automation solution from scratch, the answer is easy:

* Write unit tests for every feature;
* Run as many unit tests as possible when committing or merging changes;
* Run integration tests in a virtual or physical test lab that is large enough to allow you to test all features you want to see implemented.

I'm doing something along those lines in *netlab* -- running tons of transformation tests on every change and having integration tests that could run on a properly configured Ubuntu server (the hard part is the need for NOS images). Want a more complex example? [Kristian Larsson](https://www.ipspace.net/Author:Kristian_Larsson) described a [testing methodology his team is using to build large-scale automation solutions](https://my.ipspace.net/bin/list?id=NetAutSol&module=5#M5S3C) in the *[Validation, Error Handling and Unit Tests](https://my.ipspace.net/bin/list?id=NetAutSol&module=5)* part of *[Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions)* online course.

If you're not developing a full-blown automation solution, you might be using tools like Ansible/Jinja2 to generate and deploy router configurations. How are you going to test them? [Some ideas are obvious](/2020/10/validating-data-gitops-automation.html):

* You could run YAML, Ansible, and Jinja2 [linters](https://en.wikipedia.org/wiki/Lint_(software)) to identify the simple errors.
* You could create a data model schema for your configuration files (aka *source of truth*) to check that no one made a foolish change.
* You could create a virtual lab and run your Ansible playbooks to configure it.

Now what? How are you going to check that the valid changes to your data model did not break connectivity? How are you going to validate that the Jinja2 templates did not generate syntactically correct but broken configurations? You need *tests*, and you have none.

Of course, you could use tools like *[Batfish](https://www.batfish.org/)*, and they will help you do **static analysis of router configurations**. They will also identify common SNAFUs like mismatched OSPF parameters, but can they tell you whether your network will be working as expected after an ACL or route map change? Of course not unless you created tests based on what end-to-end connectivity you expect.

Similarly, you could create a virtual lab, configure it with your Ansible playbooks, and use a tool like [SuzieQ](https://suzieq.readthedocs.io/en/latest/) to **extract operational data from the lab and compare it to a known baseline**. Great idea, assuming *you created the baseline to compare the data with* (I [described an overly-simplified example](https://my.ipspace.net/bin/list?id=NetAutSol&module=2#M2S2A) in _[Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions)_ online course).

You should also test **end-to-end connectivity**: deploy a few endpoints in your virtual lab and check whether they can reach each other. Going a step further, you could define *valid* and *invalid* flows to test your packet filters.

Finally, there's **performance testing**, but that obviously requires a physical lab.

An aside: creating a test environment gets more manageable if you're developing tenant automation for a multi-tenant solution like Cisco ACI, VMware NSX, or a public cloud. You could create a test tenant, run your tests, destroy the tenant, and have a pretty high level of confidence that you won't break the production environment assuming you wrote a comprehensive battery of tests.

**Long story short**: you will have to write an awful lot of tests if you want to have a reliable CI pipeline, and even more tests if you plan to automate your deployments.

Finally, you might still be working with device configurations. There's even less you could do in that case (you could still use *Batfish*), but it's possible to put some rudimentary guard rails in place. More about that in another blog post.
