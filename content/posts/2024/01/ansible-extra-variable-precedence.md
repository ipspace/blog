---
title: "Precedence of Ansible Extra Variables"
date: 2024-01-31 08:35:00+0100
tags: [ ansible ]
pre_scroll: True
---
I stay as far away from Ansible as possible these days and use it only as a workflow engine to generate device configurations from Jinja2 templates and push them to lab devices. Still, I manage to trigger unexpected behavior even in these simple scenarios.

Ansible has a [complex system of variable (fact) precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#ansible-variable-precedence), which mostly makes sense considering the dozen places where a variable value might be specified (or overwritten). Ansible documentation also clearly states that the *extra variables* (specified on the command line with the `-e` keyword) have the highest precedence.

Now consider these simple playbooks. In the first one, we'll set a fact (variable) and then print it out:
<!--more-->
```
- name: Test external variables
  hosts: localhost
  tasks:
  - name: Set x to zero
    set_fact: x=0
  - debug: var=x
```

When running the playbook, we get the expected result: X is zero.

```
% ansible-playbook -v set.yml
Using /Users/pipi/Library/CloudStorage/Dropbox/Workshops/Fundamentals/Networking 101/Examples/tools/X/ansible.cfg as config file

PLAY [Test external variables] *****************************************************************************************************

TASK [Set x to zero] ***************************************************************************************************************
ok: [localhost] => changed=false
  ansible_facts:
    x: '0'

TASK [debug] ***********************************************************************************************************************
ok: [localhost] =>
  x: '0'

PLAY RECAP *************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Next, let's specify the value of X on the command line:

```
% ansible-playbook -v set.yml -e x=42
Using /Users/pipi/Library/CloudStorage/Dropbox/Workshops/Fundamentals/Networking 101/Examples/tools/X/ansible.cfg as config file

PLAY [Test external variables] *****************************************************************************************************

TASK [Set x to zero] ***************************************************************************************************************
ok: [localhost] => changed=false
  ansible_facts:
    x: '0'

TASK [debug] ***********************************************************************************************************************
ok: [localhost] =>
  x: '42'

PLAY RECAP *************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The results are already a bit counter-intuitive. We set the value of X to zero, but the next moment, its value is 42. The root cause: there's never a single value of X like in any reasonable programming language. Ansible keeps many values of X around, each one with its precedence value, and selects the value with the highest precedence whenever X is used in an expression. As the precedence of the value set with the **set_fact** module is lower than the precedence of an *extra* variable, you cannot change the value of X.

Now for what tripped me. We need X to meet certain conditions, and we try to be as careful as possible:

* X might not be defined, so let's specify a default value
* We need a list of strings, so let's split X into a list using commas as delimiters. 

```
- name: X needs to be a list
  hosts: localhost
  tasks:
  - name: Increase x by one
    set_fact: x={{ x|default('a')|split(',') }}
  - debug: var=x
```

The results are what one would expect:

```
% ansible-playbook set.yml

PLAY [X needs to be a list] ********************************************************************************************************

TASK [Split X into a list of items] ************************************************************************************************
ok: [localhost]

TASK [debug] ***********************************************************************************************************************
ok: [localhost] =>
  x:
  - a

PLAY RECAP *************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Now for the fun part: let's specify the value of X as an extra variable (you probably know where I'm going by now 🥲)[^SLE]:

[^SLE]: If you're wondering why I wouldn't specify a list value with an extra variable, have you ever tried doing that? It's a bit convoluted.

```
 % ansible-playbook set.yml -v -e x=b,c

PLAY [X needs to be a list] ********************************************************************************************************

TASK [Split X into a list of items] ************************************************************************************************
ok: [localhost] => changed=false
  ansible_facts:
    x:
    - b
    - c

TASK [debug] ***********************************************************************************************************************
ok: [localhost] =>
  x: b,c

PLAY RECAP *************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Even though the **set_fact** command splits X into a list of items, the value of X remains a string with commas.

Now for my gripes:

* My playbook worked in the past (or I have a terrible case of cognitive dissonance). I know it shouldn't have worked, but at that time, I failed to understand the implications of "*extra variables have the highest precedence*" and wrote broken code *that worked*.
* Assuming my memory is not failing me, and Ansible's behavior did change to comply with its documentation, it would be nice to get a warning saying, "*dude, the value of X is immutable*."

**Lessons learned:**

* Extra variables are potentially dangerous. You cannot prevent users from specifying anything you use in a playbook as an extra variable on the command line, and having an unexpected extra variable will break your playbook.
* Never reuse input variables. Create a new variable when you need to transform input values.
* Use a naming convention like "_internal variables start with an underscore_". It might make it a bit less likely that someone might try to overwrite their value with the `-e` parameter (or at least you'll be able to blame them for doing that 😵‍💫).

### Bonus: Splitting an Empty String

I wanted to split a string into a list of keywords, but what happens if the string is empty? Here's what Python does in that case (Ansible's `split` filter is just a passthrough to Python's `split` method):

```
% python3
Python 3.11.5 (main, Aug 24 2023, 15:09:45) [Clang 14.0.3 (clang-1403.0.22.14.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> ''.split(',')
['']
>>> ^D
```

Trying to split an empty string results in a list containing an empty string. Technically correct, but annoying. The correct expression to get what I want would be `x.split(',') if x else []`. I wonder why some people keep insisting it's easier to read Python code than Perl ;)
