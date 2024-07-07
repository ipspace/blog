---
kb_section: NetAutJourney
minimal_sidebar: true
pre_scroll: true
title: 'Next Step: Network Inventory Database'
toc_title: Network Inventory Database
url: /kb/NetAutJourney/20-Inventory/
---
It's easy to collect live inventory data with Ansible and NAPALM, and it's just as
easy to store the collected data in a database. Initially, I used sqlite3, which
is great for ad-hoc use as you can create databases on the fly. You can then use
SQL and database functions on the data, for instance, compare tables before and
after a change, which is much easier than scripting it from scratch. Sqlite3 does
have its limitations;  the current mainstream version does not support full joins,
insert-or-update ([upsert](https://wiki.postgresql.org/wiki/UPSERT)) operations,
or transactions. Besides, MySQL is just as easy to use and can run on a different
server, so I went with that for the inventory database.

Having data in a database gives you great flexibility. You can create a query to
display an overview of all different OS’s in the network and how many devices run
each version, a count of all different device models... and if you want to include
only specific devices in a drop-down field in the front-end (more about that later)
all you need to do is edit the associated SQL query.

The playbook below is what I use for all backend data gathering, with different
included playbooks collecting and updating data. The var.yml file is encrypted
with **ansible-vault**, and includes database and network authentication credentials:

```
- hosts: all
  connection: local
  strategy: free
  serial: 5
  tasks:
  - set_fact:
      outputdir: '{{ playbook_dir }}/.sqltmpdir'
  - include_vars: '{{ playbook_dir }}/vars/vars.yml'
    no_log: true

- import_playbook: setup_db.yml
- import_playbook: collect_data.yml
- import_playbook: add_to_db.yml
```

The imported playbooks do the following: _setup_db.yml_ creates the temporary directory,
_collect_data.yml_ collects the data (inventory, ARP, MAC, DHCP) and generates output
in the form of SQL statements. Finally, _add_to_db.yml_ rounds up the output files
generated for each device, generates a single SQL file, and imports it into the database
in a single transaction:

```
- hosts: all
  connection: local
  gather_facts: no
  tasks:
  - include_vars: {{ playbook_dir }}/vars/vars.yml
  - block:
    - name: Add BEGIN to INSERT file
      shell: "echo 'BEGIN;' > {{ outputdir }}/000.insert"

    - name: Add COMMIT to INSERT file
      shell: "echo 'COMMIT;' > {{ outputdir }}/zzz.insert"

    - name: Assemble INSERT SQL statements in single file
      assemble:
        src: "{{ outputdir }}/"
        regexp: "insert$"
        dest: "{{ outputdir }}/DBinsert.sql"

    - name: Add INSERT statements to database
      shell: >
        mysql -u {{ DBuser }} -p"{{ DBpw }}" -h {{ DBhost }} {{ DBname }}
        <{{ outputdir }}/DBinsert.sql

    run_once: true
    no_log: true
```
{{<note info>}}The `strategy: free` statement prevents Ansible from waiting for all devices to complete a task within a batch. This results in a huge speed increase compared to the default _linear_ strategy -- the inventory playbook ran 50% faster
on a batch of ~1200 hosts.{{</note>}}
