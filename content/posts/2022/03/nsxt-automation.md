---
date: 2022-03-21 07:54:00+00:00
niac_tag: solution
series:
- niac
tags:
- NSX
- automation
title: Automating NSX-T Deployments
---
Nicholas Michel [open-sourced an automation solution](https://github.com/vmware-nsx/sddc-demos) ([video](https://www.youtube.com/watch?v=9M0UJXiBVbw)) that deploys the whole NSX-T infrastructure stack including:

* NSX-T manager virtual machines
* NSX-T uplink profiles and IP pools
* Transport zones and transport nodes (NSX-T modules on ESXi hypervisors)
* Edge clusters including BGP, EVPN and BFD

Once the infrastructure is set up, his solution uses a Terraform configuration file to deploy multiple tenants: external VLANs, tier-0 gateways, BGP neighbors, tier-1 gateways, and application segments.

While the infrastructure part of his solution might be fully reusable, the tenant deployments definitely aren't, but they provide a great starting point if you decide to build a fully automated provisioning system.
