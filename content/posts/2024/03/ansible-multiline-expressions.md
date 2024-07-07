---
title: "Multiline Expressions in Ansible Playbooks"
date: 2024-03-06 07:33:00+0100
tags: [ Ansible ]
pre_scroll: True
lastmod: 2024-03-07 16:05:00+0100
---
Another week, another Ansible quirk 🤷‍♂️ Imagine you have a long Jinja2 expression, and you want to wrap it into multiple lines to improve readability. Using multiline YAML format seems to be the ideal choice:

```
---
- name: Test playbook
  hosts: localhost
  tasks:
  - set_fact:
      a: >
        {{ 123 == 345 or
           123 > 345 }}
```

It works every time 50% of the time (this time depending on your Ansible version).
<!--more-->
{{<note>}}Before someone accuses me of picking on Ansible, this is a *hope I'll remember this for the next time* note I wrote after [dealing](https://github.com/ipspace/netlab/commit/d58fcec11fbdab903c449f4c2bb3b251a8346014) with [this stupidity](https://github.com/ipspace/netlab/issues/1042) I [introduced into netlab](https://github.com/ipspace/netlab/commit/c22efeb79c83a2070239ad62ec910d2775d7809b#diff-6cba0002bb852e6e91731d08010905d84bd9fad2ec68515e0333d397a098d63fR22).{{</note>}}

If you use the community version of Ansible, you'll get the expected results: **a** is **false**:

```
$ ansible-playbook -v x.yml
...
TASK [set_fact] ********************************************************************************************************************
ok: [localhost] => {"ansible_facts": {"a": false}, "changed": false}
```

However, if you use an older Ansible core release (for example, Ansible core 2.12.10 that you could find in RHEL 9.0), you'll get this outstanding result:

```
$ ansible-playbook -v x.yml
...
TASK [set_fact] ********************************************************************************************************************
ok: [localhost] => {"ansible_facts": {"a": "False\n"}, "changed": false}
```

Notice how the extra newline throws off Ansible? It evaluates the expression as a string; a non-empty string is **true**, not **false**.

**Lesson learned**: you MUST NOT use multiline YAML format in Ansible expressions.

You could enclose expressions in quotes like this:

```
---
- name: Test playbook
  hosts: localhost
  tasks:
  - set_fact:
      a:
        "{{ 123 == 345 or
            123 > 345 }}"
```

You could also use the [YAML Block Chomping Indicator](https://yaml.org/spec/1.2.2/#8112-block-chomping-indicator) to remove the trailing newline:

```
---
- name: Test playbook
  hosts: localhost
  tasks:
  - set_fact:
      a: >-
        {{ 123 == 345 or
           123 > 345 }}
```

You'll find more details on a website dedicated to [multiline YAML strings](https://yaml-multiline.info/).

### Revision History

2024-03-07
: Added Block Chomping as an alternate solution based on [Miguel's comment](#2129).