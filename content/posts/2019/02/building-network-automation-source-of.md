---
date: 2019-02-26 08:26:00+01:00
tags:
- automation
- Ansible
title: Building the Network Automation Source of Truth
url: /2019/02/building-network-automation-source-of/
series: [ ssot ]
ssot_tag: build
---
*This is one of the "thinking out loud" blog posts as I'm preparing my presentation for the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course. I'm probably missing a gazillion details - your feedback would be highly appreciated*

One of the toughest challenges you'll face when building a network automation solution is "where is my source of truth" (or: what data should I trust). As someone way smarter than me said once: "*You could either have a single source of truth of many sources of lies*", and knowing how your devices should be configured and what mistakes have to be fixed becomes crucial as soon as you move from gathering data and creating reports to provisioning new devices or services.
<!--more-->
The first step on your journey should be **building reliable device inventory** - if you have no idea what devices are in your network, you cannot even consider automating the network deployment or operations. Don't even try to use Ansible or a similar tool to get it - there are tons of open-source and commercial network discovery tools out there, and every decent network management system has some auto-discovery functionality, so finding the devices shouldn't be a big deal.

Now for the fun part: assuming you didn't decide to do a one-off discovery to populate the device inventory, will you trust the data in the network management system, or will you migrate the data to some other database (IPAM/CMDB software like NetBox immediately springs to mind) and declare that database your source of truth... as far as device inventory goes.

In any case, your network automation tool (Ansible, Chef, Puppet, Salt, Nornir... isn't it wonderful to have so many choices?) expects to get device inventory in its own format, which means that you have to export data from your chosen source of truth into the format expected by your tool, unless of course, you believe that a bunch of YAML or JSON files stored in semi-random places and using interestingly convoluted inheritance rules is the best possible database there is.

{{<note info>}}
If you decide to use text files as your database and Notepad as your UI, go with YAML. Regardless of all the complaints you might be hearing on Twitter, it's still easier to read than JSON.
{{</note>}}

Should you do the export/translation every time you run your automation tool, periodically, whenever something changes, or what? Welcome to one of the [hard problems of computer science](https://www.twitter.com/codinghorror/status/506010907021828096). I'll try to give you a few hints in an upcoming blog post (as well as tackle another challenge: is your device configuration your source of truth and why is that a bad idea).

---
In case you want to know more:

-   [Single Source of Truth](https://my.ipspace.net/bin/list?id=AutConcepts#SSOT) is one of many topics covered in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.
-   We [covered Ansible inventory](https://my.ipspace.net/bin/list?id=Ansible#ANSIBLE_DD) in [Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers) webinar;
-   We talked about dynamic Ansible inventory in [Putting It All Together](https://my.ipspace.net/bin/list?id=NetAutSol&module=6) module of Building Network Automation Solutions online course;
-   In the same online course I did a [thorough overview of data models and data stores](https://my.ipspace.net/bin/list?id=NetAutSol&module=3#M3S1) (covering everything from text files to IPAM systems and relational databases).

You can get access to the ipSpace.net webinars with [Standard ipSpace.net Subscription](https://www.ipspace.net/Subscription) and access to the network automation online course with [Expert Subscription](https://www.ipspace.net/Subscription/Individual).
