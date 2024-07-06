---
date: 2014-06-26 07:16:00+02:00
tags:
- automation
- fabric
series: [ niac ]
niac_tag: principles
title: Infrastructure as Code Actually Makes Sense
url: /2014/06/infrastructure-as-code-actually-makes.html
---
When I heard people talking about "networking infrastructure as code" I dismissed that as yet another Software-Defined-Everything one-controller-to-rule-it-all hype. Boy was I wrong.
<!--more-->
### Imagine...

Imagine an application development environment where programmers debug and change source code of a deployed application in real time. How reliable would that application be? Someone would immediately put a freeze on that stupidity and allow programmers to change code only every fifth Friday of the month at 5AM (and blame ISO 9001).

Smarter programmer would figure out they still need to get work done between the Magic Fridays and would create a local copy of the application code, test their ideas on the local copy of the code, and then cut-and-paste their changes into the production source code during the Magic Friday maintenance window.

Sounds crazy? That might have been how things were done in the days of [punched cards](http://en.wikipedia.org/wiki/Punched_card), and yet that's exactly how we configure our networking devices (replace *local copy of the application source code* with *test lab* or *simulation*).

### How the Sausage Is Really Made

I know way too little about proper application development processes (please correct me in the comments), but things usually work along these lines:

-   A team of developers uses a central source code repository.

{{<note info>}}You should use source code control system like *git* or *svn* even if you're a lone wolf. You wouldn't believe how many times it saved my day when I was able to remove my blunders by reverting to a working copy of a module. Using *github* gives you bonus points -- you have a backup of your source code in the cloud.{{</note>}}

-   A developer working on a new feature or fixing a bug works on a local copy of the source code.
-   When the development work is done, the developer runs unit tests, potentially also integration and validation tests, and submits the changed source code to the repository.
-   In environments stuck in 19th century someone builds the application from the source code once every three months; well-run shops have a build process that automatically collects the source code and builds the application.
-   Final tests are run on the new release of the application.
-   The new version of the application is deployed.

{{<note info>}}[Continuous integration](http://en.wikipedia.org/wiki/Continuous_integration) is an improvement of this process that streamlines application builds. Continuous deployment is the next step after that: automatic deployment.{{</note>}}

### Infrastructure as Code

Contrary to what some SDN evangelists want you to think, we configure most application infrastructure with text files, CLI commands, or scripts. Applications are built using *makefiles*, servers are deployed using Ansible playbooks or Puppet or Chef recipes, and cloud-based application stacks are built with infrastructure-as-code systems like Terraform.

Hopefully you already store the configurations and recipes in a source code control system (many people are doing that with router, switch or firewall configurations as well). Now imagine having a build system that automatically creates VM images from Puppet recipes, configures web and database servers using those same recipes, installs the application code into the VM virtual disk from a source code or build repository, and runs automated integration and system tests. All of a sudden, you started treating your infrastructure the same way you treat application source code, hence *infrastructure as code*.

### Network Infrastructure as Code

Can we do the same thing with the networking infrastructure? Not if we use the traditional hardware approach -- it's hard to build local copy of the networking infrastructure for every networking engineer, or an automated test environment.

On the other hand, if we manage to [virtualize everything](/2013/04/virtual-appliance-performance-is.html), including networks and network services (load balancers, firewalls...), we can deploy them on-demand. Using cloud orchestration system automation it's pretty easy to create new subnets, and deploy firewalls and load balancers in VM format. Problem solved -- you can [recreate a whole application stack](/2013/05/simplify-your-disaster-recovery-with.html), either for the use of individual networking engineer working on a particularly interesting challenge, or to build QA or UAT environments.

Once the modified application stack passes all the tests, it's [easy to deploy the changes in production](/2013/11/typical-enterprise-application.html): shut down the old VMs and start new ones, or (if you made more drastic changes) tear down the old application stack and build a new one using the already-tested build recipes.

### How Can I Get Started?

Virtualize everything. You won't be able to create new application environments on demand till you're able to create virtual networks and network services on demand. Overlay virtual networks and virtual network services appliances are an ideal solution.

### Stop Changing the Hardware Configurations

Finally, it's time to get rid of cut-and-paste method of network configuration. Make sure you're not doing anything that is not repeatable and [cannot be fully cloned](/2014/04/puppet-is-tool-devops-is-lifestyle.html) in a development or test environment.

Ideally, you'd [totally decouple the virtual networks and services from the physical hardware](/2011/12/decouple-virtual-networking-from.html), and change the physical hardware configuration only when you need to build a new data center fabric or extend an existing one.

### Like the Vision?

Now go and evaluate how existing vendor offerings and architectures fit into this vision. I'll stop here; make your own conclusions.

### Need More Information?

We talked about [network infrastructure-as-code](https://my.ipspace.net/bin/list?id=AutConcepts#NIAC) and [continuous integration, delivery and deployment](https://my.ipspace.net/bin/list?id=AutConcepts#CICD) in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.
