---
kb_section: Ansible
minimal_sidebar: true
title: Using NAPALM with Ansible
url: /kb/Ansible/napalm-ansible/
---
Ansible 2.8 includes NAPALM connection plugin, making engineers trying to use NAPALM with Ansible wonder how to do it correctly. This article should provide an overview of your options.

There seem to be two ways of using NAPALM with Ansible:

* NAPALM modules like **napalm_get_facts** provided by NAPALM developers;
* New **napalm** connection plugin.

NAPALM modules like **napalm_get_facts** are not (as of today) part of Ansible core, described in Ansible documentation, or included in Ansible distribution. They are third-party modules and have to be installed separately. The process is described in [ansible-napalm documentation](https://napalm.readthedocs.io/en/latest/tutorials/ansible-napalm.html). As part of that installation, you either:

* Copy third-party modules into Ansible distribution on your system (not recommended)
* Install third-party modules in a separate directory and add the path to that directory to your [Ansible configuration](https://docs.ansible.com/ansible/latest/reference_appendices/config.html), be it through ansible.cfg file (local, per-user, or system-wide) or Ansible environment variables.

If you decide to use NAPALM modules (as supplied by the NAPALM team), then you have to read their documentation to figure out which Ansible connection type you should be using. The current examples indicate you have to use **connection: local**.

{{<note note>}}My [installation script](https://github.com/ipspace/NetOpsWorkshop/tree/master/install) installs NAPALM in the default location, and all my Ansible examples using NAPALM have ansible.cfg file with _plugins_ path that includes the NAPALM modules (example: [LLDP-to-Graph](https://github.com/ipspace/ansible-examples/tree/master/LLDP-to-Graph)).{{</note>}}

The alternative is to use NAPALM connection plugin added to Ansible 2.8. In that case, we should start our journey by [reading the plugin documentation](https://docs.ansible.com/ansible/latest/plugins/connection/napalm.html). As of Ansible 2.8, it’s cryptic and pretty useless but indicates that you have to install NAPALM as a prerequisite. I tried to find a usable example, but the only thing I found was a [discussion on whether to use it](https://github.com/napalm-automation/napalm-ansible/issues/148 ), which concluded with “_it doesn’t make sense_”, and that made me even more confused.

I would not expect **ios_command** or similar to work with **connection: napalm**, but you could try whether **cli_command** works. The current version of NAPALM Ansible modules (1.0.0) like **napalm_get_facts** doesn't make use of that connection plugin and would have to be heavily rewritten to use it.

As of November 2019, it seems like the **napalm** connection plugin was added mostly for marketing reasons, more so if it can be used only with **cli_command** module that was already platform-independent if you used **network_cli** connection plugin.

### Recommendation

If you want to use NAPALM with Ansible, use **napalm-ansible** modules, and install and use them according to [**napalm-ansible** documentation](https://napalm.readthedocs.io/en/latest/tutorials/ansible-napalm.html). You might also want to evaluate whether **Salt** or **Nornir** fit your needs better - at least Nornir [seems to be orders-of-magnitude faster than Ansible](https://networklore.com/ansible-nornir-speed/).
