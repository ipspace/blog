---
title: "Start Automating Public Cloud Deployments with Infrastructure-as-Code"
date: 2021-04-12 06:14:00
tags: [ cloud, automation ]
series: [ niac ]
niac_tag: principles
---
One of my readers sent me a series of "*how do I get started with...*" questions including:

> I've been doing networking and security for 5 years, and now I am responsible for our cloud infrastructure. Anything to do with networking and security in the cloud is my responsibility along with another team member. It is all good experience but I am starting to get concerned about not knowing automation, IaC, or any programming language.

No need to worry about that, what you need (to start with) is extremely simple and easy-to-master. [Infrastructure-as-Code](/series/niac/) is a simple concept: infrastructure configuration is defined in machine-readable format (mostly text files these days) and used by a remediation tool like Terraform that compares the actual state of the deployed infrastructure with the desired state as defined in the configuration files, and makes changes to the actual state to bring it in line with how it should look like.
<!--more-->
Cloud automation using infrastructure-as-code concepts is infinitely simpler than generic network automation. You’re using a single tool interacting with a single consistent orchestration system over a well-defined REST API interface, and the orchestration system returns data in usable (JSON) format. When dealing with generic network automation, you’re working with numerous devices, most of them using a [broken user interface](/series/cli/) (called CLI) that often can’t even execute consistent all-or-nothing transactions.

Back to automating cloud deployments with infrastructure-as-code (and we have a Buzzword Bingo Winner). Instead of chasing cloud configuration (virtual machines, disks, images, interface cards, virtual networks, subnets, access control lists, firewall settings…) through a GUI, create a text file (or a bunch of them) that defines how those objects should be configured, and mimicking Captain Picard use something like Terraform to make it so.

Next step: create a Git repository (could be just a bunch of files on a shared file system) to track changes to those configuration files, so you’ll be able to answer the “*who did what when and why*” type of questions.

Final step: don’t allow operators to run Terraform (or any such tool) directly, but run it on “official” versions of configuration files after they’ve been merged to the **master** branch (you’ll probably need a Git server to make that happen - it’s hard to protect the **master** branch on a shared file system).

Bonus points if you go one step further: every time someone submits changes to the configuration files as a Git commit (or when they ask you to merge their changes into the master branch), use your infrastructure-as-code tool to create and destroy a test environment, reporting any potential errors encountered in that process. Automated tests will ensure that the changes made to the deployment configuration files haven’t resulted in easy-to-spot errors.

## Using ipSpace.net Content to Get Started

I wrote numerous blog posts about infrastructure-as-code principles, and collected them [here](/series/niac/). I also made it part of the [Network Automation Concepts webinar](https://www.ipspace.net/Network_Automation_Concepts).

[AWS](https://www.ipspace.net/Amazon_Web_Services_Networking) and [Azure](https://www.ipspace.net/Microsoft_Azure_Networking) webinars include automation section, so you’ll find some basic ideas there, and we created a [GitHub repository](https://github.com/ipspace/pubcloud) with tons of examples using  Ansible, Terraform, and cloud-specific tools like CloudFormation templates (AWS) and Resource Manager Templates (Azure).

On the tooling side, I would recommend using Terraform to deploy cloud infrastructure and Git to manage changes to configuration files… unless your organization prefers a specific tool. You probably won’t be allowed to use public GitHub or GitLab services, but as you’re already in Azure and AWS, you could consider AWS CodeCommit or Azure DevOps Services. They would be easier to operate than setting up your own on-premises (or in-cloud) Git server like on-premises GitLab.