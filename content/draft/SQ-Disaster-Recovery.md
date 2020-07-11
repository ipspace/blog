---
title: "Disaster Recovery topics"
# date: 2020-07-04 15:30:00
tags:
draft: True
---
## Justifying Disaster Recovery Sites

There is no justification to have an idle site in case something breaks. What is required is an architecture where applications are used and balanced across multiple locations.

## Cloud Doesn't Make Disaster Recovery Obsolete

Disaster Recover is a pre-cloud thing where a company was reliant on local onsite infrastructure.

## Disaster Recovery Done Right

Let's start with paraphrasing [Helmuth von Moltke the Elder](https://en.wikiquote.org/wiki/Helmuth_von_Moltke_the_Elder): "*No disaster recovery plan survives the first contact with reality*"... unless we continuously test it in real-life environment, and here's an interesting idea [Nicola Modena](https://www.ipspace.net/Expert:Nicola_Modena) shared with us during the recent ipSpace.net Technology Summit.

Idea from Nicola:

* Storage replication to DR site
* Create a snapshot at DR site
* Use snapshot to start the whole infrastructure in an isolated environment

Apart from testing external connectivity you can do it at any time.