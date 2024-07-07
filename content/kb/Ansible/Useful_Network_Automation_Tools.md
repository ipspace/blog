---
kb_section: Ansible
minimal_sidebar: true
title: Useful Network Automation Tools
url: /kb/Ansible/Useful_Network_Automation_Tools/
---
List of useful network automation tools found on the 'net:

- [Network configuration auditing](https://networklore.com/network-config-audit/) by Patrick Ogenstad
- [Batfish](https://www.batfish.org/), an open source network configuration analysis tool
- [eNMS](https://github.com/afourmy/eNMS): a vendor-agnostic NMS for graphical network automation
- [FreeZTP server](https://github.com/convergeone/freeztp): zero-touch provisioning server for Catalyst switches
- [Rosetta](https://github.com/networktocode/ntc-rosetta): the missing link between network device CLI and YANG data models
- [NetPalm](https://github.com/tbotnz/netpalm): REST API interface to your dusty old network devices (using NAPALM and TextFSM as the back-end)
- [Jerikan+Ansible: a network configuration management system](https://vincent.bernat.ch/en/blog/2021-network-jerikan-ansible)

Ansible and Jinja2 tools:

- [Online Jinja2 parser/renderer](http://jinja.quantprogramming.com/)
- [Jinja2 Linter](https://pypi.org/project/j2lint/) (checks Jinja2 syntax and writing style)
- [NetTowel](https://github.com/InfrastructureAsCode-ch/nettowel) providers a CLI interface to Jinja2 renderer and several popular text parsers
- [Online Regex testing tool](https://regex101.com/) (described in a [NetworkToCode blog post](https://blog.networktocode.com/post/contributing-open-source-parsers/))
- Another [Learn, Build and Test RegEx](https://regexr.com/) tool
- [Ansible Silo](https://groupon.github.io/ansible-silo/)
- [Ansible MySQL Query](https://github.com/zauberpony/ansible-mysql-query)
- [Ansible Runtime Analysis](https://github.com/openstack/ara)
- [Molecule](https://github.com/metacloud/molecule/) - testing framework for Ansible roles
- [ANIT](https://github.com/networktocode/anit) - Ansible Network Infrastructure Testing framework
- [Mitogen](https://mitogen.networkgenomics.com/ansible_detailed.html) - completely redesigned Ansible connection layer. Unfortunately does not support **network_cli** connection plugin.

Python libraries:

- [Hierarchical configuration](https://github.com/netdevops/hier_config) library... and [how to use it](https://www.packetgeek.net/2016/07/network-lifecycle-management-with-hierarchical-configuration/)
- [Yangify](https://github.com/networktocode/yangify): a framework that maps unstructured data into YANG data models
* [Netutils](https://blog.networktocode.com/post/introducing-netutils/): a Python library providing utility functions for common network automation objects (ASN, FQDN, interfaces, IP addresses...)
* [scrapli](https://carlmontanari.github.io/scrapli/): a Python library focused on connecting to network devices (routers/switches/firewalls/etc.) via SSH or Telnet.
* [NetTowel](https://github.com/InfrastructureAsCode-ch/nettowel): a collection of useful network automation functions

Inventory tools:

- [motherstarter](https://github.com/writememe/motherstarter/): convert Excel, CSV, or JSON files into Ansible, Nornir, or pyATS inventories
- [NetDoc](https://www.adainese.it/blog/2022/08/28/netdoc-automated-network-discovery-and-documentation/): automated network discovery and documentation

Regular expression and parsing tools:

- [NTC templates](https://github.com/networktocode/ntc-templates) - a wide collection of TextFSM templates
- [Online regular expressions tool](https://regexr.com/)
- [Online regex tester and debugger](https://regex101.com/)
- [Online visual regex tester](https://pythonium.net/regex)
- [TextFSM Code Lab](https://github.com/google/textfsm/wiki/Code-Lab)
- [Test your TextFSM templates like Chuck Norris](http://textfsm.nornir.tech/) - online TextFSM testing tool

Building web user interface:

- [Building a web dashboard with Flask and Bootstrap](https://0x2142.com/web-dashboard-flask-and-bootstrap/)
- [Creating a Bootstrap front-end for a simple REST service](https://netdevops.me/2019/creating-a-bootstrap-based-front-end-for-your-simple-rest-service/)

Other interesting tools:

- [GraphViz](https://graphviz.org/): create graphs from text file descriptions
- [Markmap](https://markmap.js.org/): build mind maps from Markdown (HT: [John Capobianco](https://twitter.com/John_Capobianco/status/1327718529018318848))
- [NetGrph: IP network modeling database](https://github.com/yantisj/netgrph)
- [Rundeck](http://rundeck.org/index.html): job scheduled and runbook automation
- [docopt](http://docopt.org/) - command line interface description language (similar: [clint](https://github.com/kennethreitz/clint), [cement](https://github.com/datafolklabs/cement) and [invoke](http://www.pyinvoke.org/))
- [Dolt](https://github.com/liquidata-inc/dolt), Git for data (see also [Versionable Database](https://blog.networktocode.com/post/Versionable-Database/) blog post)
- [Traffic generators](https://github.com/cisco-system-traffic-generator) open-sourced by Cisco Systems
- [Ostinato](https://userguide.ostinato.org/): a packet crafter, network traffic generator and analyzer with a friendly GUI and powerful Python API for network test automation.

For an even wider list of network automation resources, check out the [Awesome Network Automation](https://github.com/networktocode/awesome-network-automation) repository.
