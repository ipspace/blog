---
kb_section: ConfigRegex
minimal_sidebar: true
title: Simple Implementation in Ansible and Jinja2
url: /kb/ConfigRegex/10-Implementation.html
---
The Cisco IOS configuration is a structured text file that uses indentation to group configuration sections.

For example, the definition of a client switchport starts with the header-line **interface GigabitEthernet1/0/2** and all configuration lines for this interface are indented by one blank.

    interface GigabitEthernet1/0/2
     description Door-Lock no Voip
     switchport mode access
     switchport access vlan 40
     ip flow monitor IPv4_STEALTHWATCH_NETFLOW input
     storm-control multicast level 5.00
     storm-control broadcast level 5.00
     storm-control action trap
     storm-control action shutdown
     spanning-tree portfast
     spanning-tree guard root
     ip arp inspection limit rate 400 burst interval 3
    !

The rest of this page describes YAML configuration, Ansible playbook, and Jinja2 template I used to remove configuration section from Cisco IOS device configuration with regex matches (the full source of the playbook can be [found on github](https://github.com/jifox/set_managed_configuration_ios)).

The playbook uses the following variables to describe the configuration sections that have to be removed. You could place the variables at the top of the play (under **vars**), or include them with **include_vars**.

{{<note>}}Long lines have been wrapped to fit the page width. Editor{{</note>}}

    ...
    vars:
      # Switch configuration backup file. if empty the device's
      # current running-config will be used
      src_config_filename: ""
      #
      # Filename of assembled new configuration
      managed_config_dest: >
        {{ config_dir }}/{{ inventory_hostname }}
        _managed_configuration.{{ ansible_network_os }}
      #
      # Filename or remaining unmanaged configuration
      unmanaged_config_dest: >
        {{ host_tmpdir }}/{{ inventory_hostname }}
        _0001_unmanaged_configuration.{{ ansible_network_os }}"
      #
      # Regex to remove managed configuration sections from current switch
      delete_section_regex:
        - ^interface\s+GigabitEthernet.*$$
        - ^Building\s+configuration.*$$
        - ^Current\s+configuration.*$$
        - ^Load\s+for\s+five\s+secs.*$$
        - ^Time\s+source\s+is\s+NTP.*$$
        - ^vlan\s+\d*$$
        - ^ip access-list\s+standard\s+emergency-access$$
        - ^banner\s+.*\^C$$
        - ^end$$
        - ...
      #
      # Regex to remove messages from config compare result
      delete_section_diff_result:
      - ^Load\s+for\s+five\s+secs.*$$
      - ^Time\s+source\s+is\s+NTP.*$$

The **delete\_section\_regex** defines the parts of the configuration we'd like to remove (for example, the '^interface..' expression). It has to include texts that we get when executing **show running** like *Building configuration*. We also have to remove the final **end** as we'll append new configuration elements after what's left of current device configuration, and a premature **end** would stop configuration parsing on Cisco IOS device.

The playbook uses **napalm\_get\_facts** module to fetch the running configuration from a device and store it into **src\_config** variable. Generating running configuration is time consuming, but it makes sure that all the latest changes made to the unmanaged parts of device configuration are taken into account.

    tasks:
      ...
      - name: Read configuration from switch and store into src_config
        block:
          - napalm_get_facts:
              hostname: "{{ ansible_host  }}"
              username: "{{ ansible_user }}"
              dev_os: "{{ ansible_network_os }}"
              password: "{{ ansible_ssh_pass }}"
              timeout: 120
              filter:
                - "config"
          - set_fact:
              src_config: "{{ napalm_config.running }}"
        when:
          - src_config_filename == ""

To remove parts of configuration we include a task list (described below) within a loop that is executed for every entry in **delete\_section\_regex** (unfortunately, that's the only mechanism Ansible provides to execute more than one task in a loop).

    - name: Remove all blocks or commands defined in delete_section_regex
      # The included tasks will re-read the var src_config from template output
      include_tasks: "{{ include_dir }}/inc_gen_unmanaged_configuration.yml"
      vars:
        template_dest: "{{ unmanaged_config_dest }}"
        del_section_regex: "{{ item }}"
      delegate_to: localhost
      loop: "{{ delete_section_regex }}"

The **inc\_gen\_unmanaged\_configuration** task list uses a Jinja2 template to remove parts of device configuration matched by current regular expression, and stores the results in a file which is then read back into **src\_config** (alternatively, you could use **template** lookup plugin to achieve the same results).

    ---
    #
    # file: inc_gen_unmanaged_configuration.yml
    #
    - name: Check inc_gen_unmanaged_configuration Parameters
      assert:
        msg: >
          Missing Parameter in inc_gen_unmanaged_configuration.yml:
          del_section_regex or template_dest is not defined!
        that:
          - del_section_regex is defined
          - del_section_regex > ""
          - template_dest is defined
          - template_dest > ""
      delegate_to: localhost
    #
    # The template uses the var src_config to render the output.
    - template:
        src: "{{ template_dir }}/config_section_remover.j2"
        dest: "{{ template_dest }}"
        lstrip_blocks: true
      delegate_to: localhost
    #
    - name: Read the rendered output back to src_config. (chain)
      set_fact:
        src_config: "{{ lookup('file', template_dest ) }}"
      changed_when: false
      delegate_to: localhost

After all managed parts have been removed from the original device configuration we can start generating new managed configuration parts. I'm using **assemble** module to merge parts of device configuration, and as it merges files within a directory in alphabetical order of their name, I prefixed the configuration parts with an 4 digit integer. The variable **host\_tmpdir** points to a directory that includes the **inventory\_hostname**. This ensures that the configurations are kept separate per device.

    - name: Generate VLAN Device-VLAN configuration
      include_tasks: "{{ include_dir }}/inc_template.yml"
      vars:
        dest_filename_part: "0010_vlan_configuration"
        template_dest: >
          {{ host_tmpdir }}/{{ inventory_hostname }}
          _{{dest_filename_part}}.{{ ansible_network_os }}
        template_name: "config_vlans.j2"
      delegate_to: localhost
    #
    - name: Write end marker
      copy:
        content: "end"
        dest: >
          {{ host_tmpdir }}/{{ inventory_hostname }}
          _9999_end.{{ ansible_network_os }}
      delegate_to: localhost

After all configuration snippets are available in directory **host\_tmpdir**, the assemble statement selects all _\*.ios_ files and saves the final configuration as file specified in **managed\_config\_dest**.

    - name: Assemble configuration
      assemble:
        src: "{{ host_tmpdir }}"
        dest: "{{ managed_config_dest }}"
        regexp: "^.*\\.{{ ansible_network_os }}$$"
      delegate_to: localhost

Finally, the configuration is pushed to the device with the **napalm\_install\_config** module.

    - name: Set Configuration - Check-Mode if do_commit is not defined
      napalm_install_config:
        config_file: "{{ managed_config_dest }}"
        commit_changes: "{{ do_commit is defined}}"
        replace_config: true
        get_diffs: true
        diff_file: "{{ managed_config_dest }}.diff"
        hostname: "{{ ansible_host  }}"
        username: "{{ ansible_user }}"
        dev_os: "{{ ansible_network_os }}"
        password: "{{ ansible_ssh_pass }}"
        timeout: 120
      register: result
      tags: [print_action]

Ansible provides **check\_mode** mechanism that enables you to make a dry-run. I personally don't like that the default behavior is *commit configuration* and therefore introduced the **do\_commit** variable that has to be specified as a command line parameter when you want the playbook to commit the changes.

    ansible-playbook -i inv_production --limit SWITCH01 \
      set_managed_configuration.yml -e do_commit=1

## Jinja2 Template that Removes Configuration Section

This template removes configuration section matched by **del\_section\_regex** from **src\_config**:

    {# file: config_section_remover.j2 #}
    {# parameters: src_config, del_section_regex #}
    {% set ns = namespace(is_in_block = false) %}
    {% for line in src_config.split('\n') %}
    {%   if ns.is_in_block %}
    {%     if (line ~ 'x')[0] != ' ' %}
    {%       if line != '!' %}
    {%         set ns.is_in_block = false %}
    {%       endif %}
    {%     endif %}
    {%   endif %}
    {%   set found=line | regex_search(del_section_regex) %}
    {%   if found %}
    {%     set ns.is_in_block = true %}
    {%   endif %}
    {%   if not ns.is_in_block %}
    {{ line }}
    {%   endif %}
    {% endfor %}

## Jinja2 Configuration Section Extractor Template

I also created a similar template that extracts a configuration section. You can use it to save configuration sections matching a regular expression to a separate file.

    {# file: config_section_extractor.j2 #}
    {# parameters: src_config, del_section_regex #}
    {% set ns = namespace(is_in_block = false) %}
    {% for line in src_config.split('\n') %}
    {%   if ns.is_in_block %}
    {%     if (line ~ 'x')[0] != ' ' %}
    {%       if line != '!' %}
    {%         set ns.is_in_block = false %}
    {%       endif %}
    {%     endif %}
    {%   endif %}
    {%   set found=line | regex_search(del_section_regex) %}
    {%   if found %}
    {%     set ns.is_in_block = true %}
    {%   endif %}
    {%   if ns.is_in_block %}
    {{ line }}
    {%   endif %}
    {% endfor %}

### Banner Templates

While you can use any character as a delimiter when configuring a banner, Cisco IOS returns the banners with EXT character (ASCII 3) as the separator. EXT character is displayed as ^C in the configuration file, but has to be a single character (ASCII 3) if you want to replace device configuration _(Barroso 2016, <https://napalm.readthedocs.io/en/latest/support/ios.html>)_.

To cope with this behavior we must remove (or extract) banner from device configuration and replace it in the managed part of device configuration.

You can use this template to remove specified banner:

    {# file: config_ios_banner_remover.j2 #}
    {# parameters: src_config, banner_name #}{% set ns = namespace(is_in_block = false) %}
    {% set ns.searchfor = '^banner\s+' ~ banner_name ~ '\s+\^C$$' %}
    {% for line in src_config.split('\n') %}
    {%   set found=line | regex_search(ns.searchfor) %}
    {%   if found %}
    {%     set ns.is_in_block = true %}
    {%   elif ns.is_in_block %}
    {%     if line.find('^C') != -1 %}
    {%       set ns.is_in_block = false %}
    {%     endif %}
    {%   else %}
    {{     line }}
    {%   endif %}
    {% endfor %}

Similarly, this template extracts the desired banner and recreates the banner in correct syntax (with ASCII 3 character as delimiter).

    {# file: config_ios_banner_extractor.j2 #}
    {# parameters: src_config, banner_name #}
    {% set ns = namespace(is_in_block = false) %}
    {% set ns.searchfor = '^banner\s+' ~ banner_name ~ '\s+\^C$$' %}
    {% set ns.is_first = true %}
    {% for line in src_config.split('\n') %}
    {%   set found=line | regex_search( ns.searchfor ) %}
    {%   if found and ns.is_first %}
    {%     set ns.is_in_block = true %}
    {%     set ns.is_first = false %}
    banner {{ banner_name ~ " \x03" }}
    {%   elif ns.is_in_block %}
    {%     if line.find('^C') != -1 %}
    {%       set ns.is_in_block = false %}
    {{       "\x03" }}
    {%     else %}
    {{       line }}
    {%     endif %}
    {%   endif %}
    {% endfor %}
