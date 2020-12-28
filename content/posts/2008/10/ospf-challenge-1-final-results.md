---
date: 2008-10-29 07:12:00.001000+01:00
tags:
- OSPF
title: 'OSPF Challenge #1: Final Results'
url: /2008/10/ospf-challenge-1-final-results.html
---
I've received several e-mails responding to the [mismatched OSPF subnet challenge](https://blog.ipspace.net/2008/10/ospf-challenge-1-establish-ospf.html). Some of the readers claimed that the configuration would work as-is; if you were one of them, I would advise you do some lab test the next time.

A few of the respondents also noted that it was more a review question than a challenge (since I've been writing about this topic a few days back) and everyone who decided the configuration has to be fixed has provided the correct solution: you have to *configure the Fast Ethernet as a point-to-point OSPF interface* and the routers stop complaining about the OSPF subnet mask mismatch.
<!--more-->}}
Unfortunately, someone decided to [prevent everyone else from having real fun](https://blog.ipspace.net/2008/10/ospf-challenge-1-establish-ospf.html#1224310020000) figuring out the solution and posted the solution as a comment to my post almost immediately after I wrote it (but I'm positive that those readers that sent me e-mails did not read that comment first). Lesson learned: the next time I'll disable comments in the challenges.
