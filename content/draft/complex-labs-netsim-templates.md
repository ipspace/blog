---
title: "Building Complex Labs with netsim-tools Configuration Templates"
date: 2021-06-21 07:43:00
tags: [ automation ]
series: netsim-tools
draft: True
---
DMZ lab

* Build topology file step-by-step
* Start the lab
* Configure the first device
* Create the template
* Apply the template to all edge devices

config.ansible -e config=edge-bgp.j2 -l e1,e2 --check -v
