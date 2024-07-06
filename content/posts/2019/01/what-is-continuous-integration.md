---
date: 2019-01-14 08:34:00+01:00
tags:
- automation
title: What Is Continuous Integration?
series: [ cicd ]
cicd_tag: principles
url: /2019/01/what-is-continuous-integration.html
series_weight: 500
---
In spring 2019 [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) course we'll have [Kristian Larsson diving into continuous integration and his virtual networking lab product](https://www.ipspace.net/Building_Network_Automation_Solutions#KL19) (you might want to listen to the [Software Gone Wild episode we did with him](/2017/05/network-testing-on-software-gone-wild.html) to get a taste of what he'll be talking about). [Christoph Jaggi](http://uebermeister.com/about.html) did a short interview with him starting with the obvious question:

> What is CI testing and how does it differ from other testing methods?

CI is short for Continuous Integration and refers to a way of developing software where changes written by individual developers are frequently (or \"continuously\") integrated together into a master branch/trunk, thus continuous integration.
<!--more-->
CI testing is about frequently running tests before and after things are merged or integrated such that quality can be upheld and feedback delivered timely to developers. CI testing itself doesn\'t dictate how you do testing, it\'s more about triggering tests, so you can use it to run unit tests, integration testing or any other test method you might come up with.

> Does CI testing cover all testing needs or is it limited to a subset?

There are probably very few theoretical limits to what can be achieved with CI testing but practically speaking it takes quite a bit of time to write tests. There are certainly ways to speed up the process, for example, for testing of network automation systems, I recommend starting with using virtual routers rather than other types of testing because it usually results in much better test coverage with less time spent on writing tests.

There\'s a trend today to do testing in production environments through observability tools and the use of deployment techniques like canaries and phased rollouts to mitigate the potential negative effects. I think it\'s great that we are seeing more of this because testing shouldn\'t stop in a CI testing environment or the lab but one should also remember that network infrastructure is fundamentally different. Rolling back a web application after a failed deployment is easy because the underlying machine is still operational while botching a network change might mean you lose connectivity, preventing you from rolling back. Networking is different from web applications and as such, we need to apply slightly different testing methodologies. I think we need more rigorous testing early on which is why I have a focus on CI testing with virtual routers.

---

Want to know more about using CI testing in network automation?

-   Start with [Network Testing](/2017/05/network-testing-on-software-gone-wild.html) episode of [Software Gone Wild](https://www.ipspace.net/Podcast/Software_Gone_Wild);
-   Watch the [Continuous Integration, Delivery and Deployment](https://my.ipspace.net/bin/list?id=AutConcepts#CICD) part of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar 
-   [Pete Lumbis](https://www.ipspace.net/Building_Network_Automation_Solutions#PL17) explained the [basics of CI/CD](https://my.ipspace.net/bin/list?id=xNetAut171#CICD) in Spring 2017 session of our [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions) and dived [deeper into Gitlab CI/CD](https://my.ipspace.net/bin/list?id=xNetAut173#GITLAB_CI) in autumn 2017;
-   [Gabriele Gerbino](https://www.ipspace.net/Building_Network_Automation_Solutions#GG18) described how you can [build a test harness using virtual network devices](https://my.ipspace.net/bin/list?id=xNetAut183#PIPELINE) in autumn 2018 automation course;
-   A large enterprise [implemented CI/CD pipeline to deploy changes to firewall rules](/2019/01/firewall-ruleset-automation-with-ci.html);
-   More and more developers believe in [testing in production](https://medium.com/@copyconstruct/testing-in-production-the-safe-way-18ca102d0ef1) that Kristian mentioned in his interview.

[Guest speaker presentations](https://my.ipspace.net/bin/list?id=NetAutSol) from the [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions) are accessible to course attendees and ipSpace.net subscribers with [Expert Subscription](https://www.ipspace.net/Subscription/Individual) who chose the automation course as part of their subscription package.
