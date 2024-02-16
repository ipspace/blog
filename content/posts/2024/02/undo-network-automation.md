---
title: "Implementing 'Undo' Functionality in Network Automation"
date: 2024-02-21 07:06:00
tags: [ automation ]
series: [ ssot ]
ssot_tag: details
---
[Kurt Wauters](https://www.ipspace.net/Author:Kurt_Wauters) sent me an interesting challenge: *how do we do rollbacks based on customer requests?* Here's a typical scenario:

> You might have deployed a change that works perfectly fine from a network perspective but broke a customer application (for example, due to undocumented usage), so you must be able to return to the previous state even if everything works. Everybody says you need to “roll forward” (improve your change so it works), but you don’t always have that luxury and might need to take a step back. So, change tracking is essential.

He's right: the *undo* functionality we take for granted in consumer software (for example, Microsoft Word) has totally spoiled us.
<!--more-->
Unfortunately, there's no silver bullet unless you describe your network in YAML files, store them in a Git repository, and use **git revert** to undo changes. The moment you want to have a fancier data store, be it a relational database, key-value store, or a NoSQL database, you have to implement the change tracking in whatever application is manipulating the data[^DOLT].

[^DOLT]: In theory, you could get the best of Git and relational databases with [Dolt](https://github.com/dolthub/dolt). Still, it's probably great fun trying to undo a transaction that touched data that was subsequently partially modified by other transactions.

Network automation is not the only domain with that particular problem[^IPAM]. Have you ever tried to undo a grocery store sale or unorder a pizza? How about undoing a bank transfer?[^SRA] In all those cases, the changes must be undone manually (or by the application) and logged as yet another transaction.

[^IPAM]: IPAM tools are no better; the only exception might be Nautobot with Dolt plugin.

[^SRA]: Having sender and recipient accounts in different banks makes it even more fun.

We have to use the same approach in any system that stores data in something more structured than text files under version control:

* Keep a separate log of changes made during user transactions[^DBCL].
* Have a way to request undoing a transaction. This process should include sanity checks so you don't mess up the intervening changes and should reject the *undo* operation if those checks fail.
* Treat every *undo* transaction as a regular transaction that triggers deployment of changed network configuration.

Considering all that, maybe it's worth staying with YAML files and Git for a while longer ;)

[^DBCL]: Most relational databases have no built-in change logging. You could get fancy and use triggers to log changes, but it's messy and platform-dependent. It's much better to solve the problem in the application.