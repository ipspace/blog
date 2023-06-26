---
title: "Implementing 'Undo' Functionality in Network Automation"
date: 2023-09-15 07:06:00
tags: [ automation ]
draft: True
---
From [Kurt Wauters](https://www.ipspace.net/Author:Kurt_Wauters)

Still nice to read these weekly mails but I think you forgot about another rollback scenario. What about the need to rollback on customer request?

You might have deployed a change which works perfectly from network perspective but that broke a customer application (undocumented usage, specifications to an application,..) you also need to be able to return to the previous successful state even if everything works. Everybody says you need to “rollforward” (improve your change so it works) but you don’t always have that luxury and might need to take a step back. So change tracking is also important.
 
For the ones who have the possibility it might also be advisable to do your changes over  a mgmt. or OOB network as this guarantees that you can’t “cut the branch on which your sitting” and it’s less intrusive has “reboot in 5”.

