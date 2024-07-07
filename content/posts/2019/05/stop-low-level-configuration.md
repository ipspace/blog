---
cli_tag: real
date: 2019-05-16 08:39:00+02:00
niac_tag: implement
series:
- niac
- cli
tags:
- automation
- configuration
title: Stop the Low-Level Configuration Manipulation
url: /2019/05/stop-low-level-configuration/
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

Imagine a small bank deciding in their infinite wisdom (in reality: because their CIO attended a conference organized by a database vendor) to implement their banking software by teaching bank tellers how to type SQL transactions by hand.

For example, to transfer money from one account to another account, a bank teller could simply type:
<!--more-->
```
BEGIN;
UPDATE accounts SET amount = amount - 100 WHERE accno = '123';
UPDATE accounts SET amount = amount + 100 WHERE accno = '321';
COMMIT;
```

What could possibly go wrong? How about:

-   Some bank tellers mistype the account numbers, taking money from a wrong account;
-   Others take more money from one account than they put into another account because they have to type the same number twice;
-   A few of them get distracted by a phone call and never complete the transaction;

To make matters worse, imagine that the database has no transactional consistency - you could complete half the transaction (taking the money from the account) even if the other half would fail (because you mistyped the destination account number). Also, there would be no protection against multiple bank tellers tweaking the same numbers... and we can make this one even funnier if we assume that the bank tellers cannot use atomic UPDATE and have to:

-   Read the account amount;
-   Do the math (add or subtract a number)
-   Set the account amount to the new value.

Nobody in their right mind would even think about doing something this stupid, right? And yet this is how we keep configuring our networks more than half a century after software developers started creating *transactions* to keep things consistent.

Maybe we should stop yammering how networking is special and start learning from other people's lessons-learned... in this particular case creating scripts that would take simple input values that operators can understand because they're related to task-at-hand (like customer names instead of VLAN numbers), create configuration commands (SQL transactions in my analogy) that would be consistent and repeatable, and push the configuration commands to the network devices.

Obviously, software developers have it easier because they're dealing with databases that have ACID properties (your network devices could have them as well [if you'd care about that when buying them](/2016/10/network-automation-rfp-requirements/)) but that shouldn't be an excuse not to get started. Welcome to the world of network automation ;)... and once you decide to get serious about it, we might have a [few webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars) and [courses](https://www.ipspace.net/Building_Network_Automation_Solutions) that could help you on the way.
