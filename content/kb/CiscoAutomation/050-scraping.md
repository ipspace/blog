---
kb_section: CiscoAutomation
minimal_sidebar: true
title: Screen and Web Scraping
url: /kb/CiscoAutomation/050-scraping/
---
Screen/Web scraping refers to the process of translating the output displayed by software (for example, a network device CLI) into a data structure. More generally, I include in this category all automation scripts that try to emulate humans while they are interacting with a device. As you will see later, this is the rudest but also pretty effective way to automate many devices. Rude because interpreting the output of a screen is very risky, painful and slow; effective because many devices don't offer alternatives.

We can divide devices on which we can use this approach into two categories:

* Devices that can be configured using a terminal (telnet/serial or SSH),
* Devices that can be configured with a web browser.

## Screen Scraping

Screen scraping is used to automate interaction with devices that have no native APIs. While we've been using **expect** scripts for ages, these days you'd most like use tools like:

* Pexpect
* Netmiko
* NAPALM

Ansible, used with `ios_command` or `ios_config` modules also belongs to this category too, but we'll discuss it later.

All the above tools run on top of a telnet or SSH session and can thus connect only to an already-configured device - you have to use a ZTP process to bring an out-of-the-box device online. Reverse terminal servers can convert incoming telnet or SSH connections into console port connections so that you could use Pexpect and Netmiko in ZTP process.

### Pexpect

Pexpect interacts with a terminal session by sending commands and parsing received outputs. A CLI command is executed on the automation host (telnet, ssh or any other terminal command), and the input and output of that command are redirected to Pexpect. The developers must manage all interactions with the device including initial connection setup, login, sending commands, receiving output, parsing the output, and the logout process.

Because of the effort required, Pexpect is the least desirable option, and should be used solely when you cannot use Netmiko or NAPALM, for example:

* When NAPALM or Netmiko don't support the device you're trying to automate (example: Cisco Call Manager);
* When NAPALM or Netmiko don't support the connection type you have to use (example: some fancy jump host);
* When a specific terminal client must be used to connect to the device (example: some fancy firmware manager).

### Netmiko

Netmiko is the next evolutionary step from Pexpect: Netmiko automatically manages connections, login/logout process, sending commands, and receiving and parsing outputs. Using Netmiko developers can write scripts in minutes. Netmiko includes connection plugins for numerous devices from major networking vendors (i.e. Cisco, Arista, Juniper...), and a few of them can be used with both SSH or Telnet protocols.

Moreover, Netmiko uses Google TextFSM to simplify output parsing and creation of data structures (JSON) from device outputs. You can use the resulting JSON data structures in the subsequent automation steps.

You can download TextFSM templates from the network.tocode() repository (ntc-templates). Additional templates can be developed and submitted: the maintainers are pretty fast merging contributions and helping contributors.

Netmiko is a pretty good low-level option you can use to develop automation processes and should be the preferred way if you cannot use NAPALM or Ansible.

Sometimes I prefer Netmiko over Ansible even if Ansible supports the device I'm working with as I can call Netmiko from Python scripts, whereas Ansible is usually executed as an external command (I find quite hard to use Ansible Python library).

If you're complaining that Ansible has a better multi-thread connection manager than Netmiko, please continue reading this post.

### NAPALM

NAPALM is a multivendor framework that provides a unified network device configuration management and getter API. In other words, you can get (for example) LLDP neighbors from various network devices (Cisco router, Juniper router or Arista switch) in the same data structure.

Although you could find third-party NAPALM plugins, the list devices supported by core drivers is small and includes only:

* Arista EOS
* Cisco IOS, IOS-XR and NX-OS
* Juniper Junos

The list of supported getters is also relatively small and doesn't include common enterprise use cases like OSPF information.

Because of the above two reasons, I found NAPALM useful only in specific environments.

### References

* [Pexpect](https://pexpect.readthedocs.io/en/stable/ "Pexpect")
* [Netmiko](https://pynet.twb-tech.com/blog/automation/netmiko.html "Netmiko")
* [NAPALM](https://napalm.readthedocs.io/en/latest/support/index.html# "NAPALM")
* [TextFSM templates for network devices](https://github.com/networktocode/ntc-templates "TextFSM templates for network devices")

## Web Scraping

The second category of devices can be automated using web scraping tools. Devices that have REST API are not in this category, as REST API calls usually return data structures in JSON or XML format.

The most popular web scraping tools include:

* WebBot
* Mechanize
* Selenium

All three above frameworks emulate humans when interacting with web pages. In other words, web scraping tools are the "robots" that cannot solve captchas.

Web scraping frameworks are useful when you have to interact with an HTML-based web page. For example, you have to connect to a GitLab server with a web browser during a local GitLab installation procedure to set an administrative password. A short web scraping script can do that in an automated pipeline.

## Nornir

Nornir is a pure Python automation framework intended to be used directly from Python code. In other words: Netmiko + Nornir ≈ Ansible.
From the authors:

> While most automation frameworks use their Domain Specific Language (DSL) which you use to describe what you want to have done, Nornir lets you control everything from Python.

That explains why Nornir could be the best of both worlds: while Ansible requires that you develop a playbook in YAML format, when using Nornir everything can be defined by developers writing Python code.

You might find Nornir superfluous given the massive popularity of Ansible, but sometimes reinventing the wheel is not a bad idea: designing a faster wheel requires building it from scratch.

### References

* [nornir](https://nornir.readthedocs.io/en/latest/plugins/index.html "https://nornir.readthedocs.io/en/latest/plugins/index.html")

## Conclusions

Screen/Web scraping tools are the worst way to automate networking operations because any change in the output (sometimes triggered by something as trivial as a software update) can break the framework. Unfortunately, they are often the only practical way to automate interaction with network devices that support only CLI or HTML-based configuration and monitoring, and might also be the fastest way to get your job done.
