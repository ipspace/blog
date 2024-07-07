---
date: 2019-01-21 07:44:00+01:00
tags:
- automation
title: Continuous Integration in Network Automation
url: /2019/01/continuous-integration-in-network/
series: [ cicd ]
cicd_tag: principles
series_weight: 400
---
In the first part of his interview with [Christoph Jaggi](http://uebermeister.com/about.html) [Kristian Larsson](https://www.ipspace.net/Building_Network_Automation_Solutions#KL19) talked about the [basics of CI testing](/2019/01/what-is-continuous-integration/). Now let's see how you can use these concepts in network automation.

> How does CI testing fit into an overall testing environment?

Traditionally, in particular in the networking industry, it\'s been rather common to have proof of concepts (POC) delivered by vendors for various networking technologies and then people have sat down and manually tested that the POC meets some set of requirements.
<!--more-->
The cost of such a test is enormous and repeating it will cost just as much which makes anyone reluctant to repeat it. Change is difficult in most companies because it is expensive. If we could instead encode all that testing in terms of automatic testing rules then re-running the test doesn\'t cost more than the running rate of a few computers and for someone to push a button. CI testing can fundamentally change how this industry works and operates which I think is really exciting.

I mentioned testing in production before and I think that it is important but it shouldn\'t be the primary means of testing. The scale of a deployment has implications on its behavior and as such we are going to see different problems in a production environment compared to an artificial testing environment. We must pick up on this but CI testing is important for guaranteeing logical correctness and this should happen before deployments.

> Are there any pre-conditions for CI testing?

The only real pre-condition is that you need something to test. If you operate your network by typing into a CLI then perhaps there isn\'t much you can test in an automated CI testing environment. One should be aware that it usually needs a bit of an investment in time to get going.

> Does CI testing include security and how is security ensured?

It certainly can. I\'ve built an environment where we use CI testing to show that access lists are implemented as per specification. Being able to prove to a security team that the network behaves in a certain way is quite nice.

> What is the best way for a relative newbie to get started with CI testing?

Once you have a CI system, like GitLab CI up and running, you need to set up an environment specific to running your network tests. I recommend using virtual routers since they\'re the closest thing we have to what we run in production. It\'ll allow you to both configure and then observe the behavior of actual routers!

> What resources are available for a relative newbie to get started?

Get GitLab and GitLab CI to host your code and run tests for you. Then get vrnetlab, which is a project I\'ve written that enables running virtual routers in a docker environment. Finally, write some tests!

---

Want to know more about using CI testing in network automation?

-   Start with [Network Testing](/2017/05/network-testing-on-software-gone-wild/) episode of [Software Gone Wild](https://www.ipspace.net/Podcast/Software_Gone_Wild);
-   Watch the [Continuous Integration, Delivery and Deployment](https://my.ipspace.net/bin/list?id=AutConcepts#CICD) part of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar;
-   [Pete Lumbis](https://www.ipspace.net/Building_Network_Automation_Solutions#PL17) explained the [basics of CI/CD](https://my.ipspace.net/bin/list?id=xNetAut171#CICD) in Spring 2017 session of our [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions) and dived [deeper into Gitlab CI/CD](https://my.ipspace.net/bin/list?id=xNetAut173#GITLAB_CI) in autumn 2017;
-   [Gabriele Gerbino](https://www.ipspace.net/Building_Network_Automation_Solutions#GG18) described how you can [build a test harness using virtual network devices](https://my.ipspace.net/bin/list?id=xNetAut183#PIPELINE) in autumn 2018 automation course;
-   A large enterprise [implemented CI/CD pipeline to deploy changes to firewall rules](/2019/01/firewall-ruleset-automation-with-ci/);

[Guest speaker presentations](https://my.ipspace.net/bin/list?id=NetAutSol) from the [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions) are accessible to course attendees and ipSpace.net subscribers with [Expert Subscription](https://www.ipspace.net/Subscription/Individual) who chose the automation course as part of their subscription package.
