---
kb_section: NetAutJourney
minimal_sidebar: true
pre_scroll: true
title: 'First Step: Configuration Templates'
toc_title: Configuration Templates
url: /kb/NetAutJourney/10-Templates.html
---
Creating configuration templates with Jinja2 is an excellent initial use-case for Ansible.
One very beneficial aspect of any network automation journey is that it encourages
a systematic and progressively organized approach to network engineering. Before long,
you will have weeded out all those pesky exceptions in your network, as they hinder any
automation effort you would like to subject them to, and conversely uniformity brings great rewards.

You should always start with the Ansible inventory, which should be a structured reflection of the
makeup of your install base, and continue to be consistent when defining configuration templates.
Use templates to define the configuration standard with global management parameters, access-lists,
policies..., and get rid manually hacked together configs with omissions and deviations from the
standard. At the very least, you can start by ensuring no new devices will be deployed with
configuration deviating from the defined standard.

{{<note info>}}Tip for Cisco IOS templates: include an EEM applet in the template to have the device generate
a key and enable ssh upon booting, see the appendix.{{</note>}}

With the inventory set up, the next step is to use Ansible to interact with devices directly.
A useful example is preparing network devices for firmware upgrades. I wrote a playbook that
prepared all devices for upgrading, leaving the actual software reload as the only manual step
required to activate the new image. However, after creating an elaborate playbook doing all
kinds of checks, I realized a better approach for upgrading Cisco IOS devices is grabbing
the tar file and using the **archive download-sw** command. With this command, you can do
everything, including checks on platform compatibility, feature set, and memory. It can
also set the boot statement and reload the device (if you want to do that)... all with a
single command (refer to the appendix for the available options for the **download-sw** command).

The playbook can then be as simple as this:

```
- name: Upgrade IOS image if not compliant
  block:
  - name: Run download-sw for IOS image
    ios_command:
      commands:
        - "archive download-sw /imageonly tftp://{{TFTPHOST}}/{{fw_tar}}"
      wait_for: |
        result[0] contains All software images installed.
  when: |
    ansible_net_version != compliant_ios_version
    and not ansible_net_stacked_models[1:]
```

The `ansible_net_stacked_models[1:]` expression is true when there is more than one switch present in the ansible_net_stacked_models array; in other words, when the device is a stack. Note that waiting for the confirmation that the software image is installed can take a while. To be able to have Ansible catch the confirmation in the playbook, increase the Ansible **command_timeout** to a sufficiently long time. I found that while most switches complete the procedure within five or six minutes, sometimes it takes much longer for the same device. Regardless of whether Ansible decides to time out the operation, the switch will continue to complete the **download-sw** command in the background, and so far, each time the switch eventually got through it. An assert task which runs after a while to doublecheck may be in order. YMMV.

The **fw_tar** variable can be the result of a database or CSV lookup for the **compliant_ios_version**. In my case, the compliant_ios_version is queried from the database, which brings me to the next step in the network automation journey: collecting Ansible outputs and manipulating them in a database.
