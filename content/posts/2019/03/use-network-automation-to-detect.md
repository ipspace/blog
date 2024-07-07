---
date: 2019-03-12 09:19:00+01:00
tags:
- automation
title: Use Network Automation to Detect Software Bugs
url: /2019/03/use-network-automation-to-detect/
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

Here's a question I got from one of the attendees of my [network automation online course](https://www.ipspace.net/Building_Network_Automation_Solutions):

> We had a situation where HSRP was configured on two devices and then a second change was made to use a different group ID. The HRSP mac address got \"corrupted\" into one of devices and according to the vendor FIB was in an inconsistent state. I know this may be vendor specific but was wondering if there is any toolkit available with validation procedures to check if FIB is consistent after implementing L3 changes.

The problem is so specific (after all, he's fighting a specific bug) that I wouldn't expect to find a generic tool out there that would solve it.
<!--more-->
I might be wrong and someone will correct me (write a comment), but it looks like the customers are not willing to pay for additional software that would detect vendor bugs. A major vendor tried to sell an *assurance engine* -- reassuringly-priced software that validated that another reassuringly-priced solution worked correctly -- and killed it a few years later (probably not because their software got bug-free).

Ignoring that, what you could do in a situation like this is:

-   Figure out how to identify the problem with **show** commands (assuming it can be done) and how to fix it when you find it (reload might be the only option);
-   Write a script to use those **show** commands to check whether the forwarding state is still consistent with your expectations;
-   Run that script periodically and do something when it detects the inconsistency;

... assuming, of course, that the problem is bad enough that it warrants the time and effort needed to write such a script.

**Note:** when evaluating whether it makes sense to invest time into writing a validation script, keep in mind that it will be a major effort when you start, but once you have the infrastructure in place it will be pretty easy to add further validation checks. I created a [sample validation framework](https://github.com/ipspace/ansible-examples/tree/master/Sample-Compliance-Check) (feel free to use and extend it) as a case study for the [Easy Wins](https://my.ipspace.net/bin/list?id=NetAutSol&module=2) module in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.

Facebook used a similar approach when [dealing with memory leaks in high-end routers](https://ripe71.ripe.net/archives/video/152/) -- I talked about that in more details in the [*automated remediation*](https://my.ipspace.net/bin/list?id=NetAut101#HIERARCHY) part of [Network Automation 101](https://www.ipspace.net/Network_Automation_101) webinar.

Finally, scream and kick the vendor. Bugs are to be expected but having to write custom scripts to check whether the \$vendor bloatware messed it up (again) instead of getting a quick bug fix is inexcusable.

### Revision History

2022-07-12
: Cisco Network Assurance Engine [reached its untimely demise](https://www.cisco.com/c/en/us/products/collateral/data-center-analytics/network-assurance-engine/nae-software-v-5-1-eol.html) on December 31st 2021.
