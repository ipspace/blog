---
date: 2008-10-29 07:12:00.001000+01:00
ospf_tag: adj
tags:
- OSPF
title: 'OSPF LAN Adjacency Challenge: Final Results'
url: /2008/10/ospf-challenge-1-final-results.html
---
I've received several e-mails responding to the [mismatched OSPF subnet challenge](/2008/10/ospf-challenge-1-establish-ospf.html). Some of the readers claimed that the configuration would work as-is; if you were one of them, I would advise you to do some lab tests the next time.

A few of the respondents also noted that it was more a review question than a challenge (since I've been writing about this topic a few days back), and everyone who decided the configuration has to be fixed has provided the correct solution: you have to *configure the Fast Ethernet as a point-to-point OSPF interface* and the routers stop complaining about the OSPF subnet mask mismatch.
