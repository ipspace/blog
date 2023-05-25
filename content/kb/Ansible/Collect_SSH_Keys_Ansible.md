---
kb_section: Ansible
minimal_sidebar: true
pre_scroll: true
title: Collect SSH Keys with an Ansible Playbook
url: /kb/Ansible/Collect_SSH_Keys_Ansible.html
---
One of the annoyances of running ephemeral virtual labs where you recreate the devices every time you start the lab (I'm looking at you VIRL) are the ever-changing SSH keys. Vagrant neatly solves that problem; here are a few tricks if you're using some other staging infrastructure.

### Create SSH Keys on Reload

A major nuisances of running a virtual copy of Cisco IOS in VIRL is the lack of persistent storage of SSH keys (I am positive they are permanently stored in the CSR 1000V disk image). The SSH keys are not stored in router configuration and as the only information that's retained across VIRL simulations is the router configuration the routers usually get started with no SSH keys.

Here's an EEM applet that solves that problem:

    event manager applet ssh-keys
     event syslog occurs 1 pattern "%SYS-5-RESTART: System restarted"
     action 1.0 cli command "enable"
     action 2.0 cli command "configure terminal"
     action 3.0 cli command "crypto key generate rsa modulus 1024"

However, devices geting new keys after every reboot make the ssh clients using default settings extremely unhappy.

### Ignore SSH Keys

You could add `StrictHostKeyChecking=no` to `~/.ssh/config` or `/etc/ssh/ssh_config` to stop ssh client from complaining about ever-changing SSH keys on your network devices... but every security professional would quickly point out how unsafe that is. Let's look for another solution.

### Collect SSH Keys from the Devices

Use this Ansible playbook (based on a [blog post by Larry Smith](http://everythingshouldbevirtual.com/ansible-ssh-known-host-keys)) to collect SSH keys from devices listed in your inventory file and store them in `~/.ssh/known_hosts`

```
- name: Get SSH keys  
  hosts: all  
  gather_facts: no  
  connection: local  
  vars:  
    - known_hosts: "~/.ssh/known_hosts"  
  tasks:  
    - name: scan and register  
      command: "ssh-keyscan {{ansible_host|default(inventory_hostname)}}"  
      register: "host_keys"  
      changed_when: false  

    - file: path={{known_hosts}} state=touch  
      run_once: true  

    - blockinfile:  
        dest: "{{known_hosts}}"  
        marker: "# {mark} This part managed by Ansible"  
        block: |  
          {% for h in groups['all'] if hostvars[h].host_keys is defined %}  
          {{ hostvars[h].host_keys.stdout }}  
          {% endfor %}  
      run_once: true
```

The [latest version of the playbook](https://github.com/ipspace/NetOpsWorkshop/tree/master/tools/ssh-keys) correctly handles missing devices and SSH servers running on non-default port numbers. The details of its operation are explained in the [Sample Ansible Playbooks](https://my.ipspace.net/bin/list?id=AnsibleOC#SAMPLES) section of [Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers) online course.