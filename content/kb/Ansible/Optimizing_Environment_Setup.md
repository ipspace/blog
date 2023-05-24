title: Optimizing Environment Setup in Ansible Playbooks

One of the simplest network automation tasks is generating device configurations from data models, service descriptions, and configuration templates. You can use almost any tool to do that - from Excel to Ansible, Python or Nornir. However, it makes sense if the tool is easy to use and can handle device inventory and data models out-of-the box, making Ansible a common choice.

After the first few failed attempts, most engineers quickly discover the need for structured templates, and might start liking Ansible roles and **assemble** task to merge configuration snippets into final configuration... requiring numerous work directories (usually one per managed device).

If you want to write reliable playbooks, you shouldn't assume a particular state of your working directories. Always assume the worst, reset everything to a known state, and start from there. A typical setup sequence might include:

* Create final configuration directory (if it doesn't exist)
* Cleanup and/or create working directory
* For every managed device, create a subdirectory in the working directory.

When using Ansible as a tool, **file** modules seem to be the obvious choice, resulting in something along these lines:

    - name: Prepare for configuration build
      hosts: all
      tasks:
      - file: path={{build_dir}} state=directory
      - file: path={{config_dir}} state=directory
      - file: path={{build_dir}}/{{inventory_hostname}} state=absent
      - file: path={{build_dir}}/{{inventory_hostname}}

Seems simple, right? It is until you figure out all the annoying details:

* You don't want the working environment created on the managed devices but on the Ansible host;
* It doesn't make sense to create the common directory many times (once per managed device), the task should be executed only once;
* It doesn't make sense to count and report changes to managed devices just because we had to create working directories;
* It's probably a good idea to create those directories even when the playbook is run in **check** mode.

Here's the final snippet:

    - name: Prepare for configuration build
      hosts: all
      tasks:
      - file: path={{build_dir}} state=directory
        check_mode: no
        run_once: yes
        delegate_to: localhost
      - file: path={{config_dir}} state=directory
        check_mode: no
        run_once: yes
        delegate_to: localhost
      - file: path={{build_dir}}/{{inventory_hostname}} state=absent
        changed_when: false
        check_mode: no
        delegate_to: localhost
      - file: path={{build_dir}}/{{inventory_hostname}} state=directory
        changed_when: false
        check_mode: no
        delegate_to: localhost

INFO: Of course you could optimize the above play a bit, but you get the idea...

I've seen numerous examples where setting up the environment took more space in a playbook than the actual tasks that had to be executed.

Is there a better way of setting up things? How about:

* Extract the setup process into a separate file;
* Include the setup code into all playbooks that need it with **import_tasks** or **import_playbook**
* Execute a **shell** module to get the job done instead of a series of **file** modules

For example:

    - name: Prepare for configuration build
      hosts: localhost
      tasks:
      - shell: |
          mkdir -p {{config_dir}}
          rm -fr {{build_dir}}
          mkdir -p {{build_dir}}
          cd {{build_dir}}
          mkdir {{groups['all']|join(' ')}}
        args:
          warn: false
        changed_when: false

It's definitely cleaner, much faster, and doesn't pollute your Ansible log with tons of printouts, as Ansible executes a single module versus two modules per managed device. Should you use it? That depends on how you answer this question: "*Would my support team understand it at 2AM on a Sunday morning when trying to figure out why automation broke?*"
