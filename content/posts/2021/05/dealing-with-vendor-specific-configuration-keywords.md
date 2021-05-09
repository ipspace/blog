---
title: "Automation: Dealing with Vendor-Specific Configuration Keywords"
date: 2021-05-20 06:22:00
tags: [ automation ]
---
One of the students in our [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course asked an interesting question:

> I'm building an IPsec multi-vendor automation solution and am now facing the challenge of vendor-specific parameter names. For example, to select the AES-128 algorithm, Juniper uses *‌aes-128-cbc*, Arista *aes128*, and Checkpoint *AES-128*. 
> 
> I guess I need a kind of Rosetta stone to convert the IKE/IPSEC parameters from a standard parameter to a vendor-specific one. Should I do that directly in the Jinja2 template, or in the Ansible playbook calling the template?

Both options are awkward. It would be best to have a lookup table mapping parameter values from the data model into vendor-specific keywords, for example:
<!--more-->
```
aes:
  junos: aes-128-cbc
  eos: aes128-gcm-xpn
  checkpoint: AES-128
```

You could then read that lookup table into an Ansible variable (let's call it **rosetta**) with **include_vars** module, and use it in Jinja2 templates. For example, to select the vendor-specific cipher name, use...

```
{{ rosetta[cipher][ansible_network_os] }}
```

... in a Jinja2 template, assuming the cipher name is in variable **cipher** and your inventory consistently sets **ansible_network_os** for every device where you want to have IPsec/MACsec configured.

You could optimize this idea as much as you wish. For example, assuming you created Ansible inventory groups based on device operating system, you could save the vendor-specific attributes in **group_vars**.
