index: yes
toc_title: Overview

# Brownfield Network Automation with Ansible

One of the problems that I ran into when starting with network automation was the decision on how to migrate network device configurations from manually-configured ones to fully managed configurations.

In a first step I’ve tried to use Ansible standard modules to manage device configurations on Cisco IOS devices. For some parts of the configuration this works fine but when it comes to access lists, device-vlan configurations etc. the complexity of Ansible playbooks starts growing rapidly. Most of the complexity is introduced by the need to figure out the sequence of add- and delete configuration commands needed to transform the current running configuration into desired managed configuration.

After further investigating this problem, I switched over to Ansible NAPALM modules. The **napalm\_install\_config** module is used to replace the whole device configuration at once and provides a mechanism to show the difference between current and target configuration, and commit or rollback the changes.

Replacing the whole configuration is an elegant way of removing unwanted parts of device configuration and simplifying the playbooks. The next problem I needed to solve was how to migrate just the parts of the device configuration that I wanted to manage while keeping the rest of the configuration (defaults, model-specific commands, things I don't care about) unchanged.

None of the existing Ansible modules provides sufficient support for changing parts of Cisco IOS device configuration. I resolved this problem by implementing a playbook that uses a list of regular-expressions to identify the managed parts of configuration and Jinja2 templates to remove or extract the selected configuration sections.

## Brownfield Workfow

To replace Cisco IOS device configuration in cases where only some parts of it are managed by the network automation solution I implemented a playbook that:

* Reads the device configuration from a network device or a backup file;
* Removes the parts that are managed by an automation solution from the *running configuration* using a list of regular expressions that selects the sections to be removed;
* Saves the remaining configuration as unmanaged configuration;
* Generates the managed configuration from a hardware-agnostic data model via Jinja2 templates;
* Assembles the configuration parts into a single configuration file.
* Uses **napalm\_install\_config** module to push configuration to device.
* Displays the configuration differences that will be applied.

A big advantage in my opinion is that this workflow will allow the network operators to continue doing their work using the existing manual or semi-manual processes. They just need to know which parts of the configuration are managed (and shouldn't be changed), but even if they change a part of the managed configuration, the playbook will list the difference before installing the changes, so that appropriate actions can be taken.

## Known Limitations

* The **napalm\_install\_config** module will not allow to change the switchport type from **switchport mode trunk** to **switchport mode access**. Execute **default interface INTERFACENAME** for those ports before applying new configuration. The configuration diff works without problem.
