---
title: "Testing Network Automation Device Configuration Templates"
netlab_tag: "netlab Integration Tests"
date: 2024-05-24 08:08:00+0200
tags: [ automation, netlab ]
series: [ cicd ]
cicd_tag: testing
draft: True
---
_netlab_ has grown from a tiny Vagrantfile generator into a massive tool supporting three virtualization platforms, ~20 network devices, and a dozen technologies. Even its high-level architecture diagram became a bit of a mess:

So, how do you make sure something as complex as that works as expected? You test the heck out of it ;)
<!--more-->
{{<note info>}}The rest of this blog post will sound ridiculously obvious to any decent software engineer. If you happen to be one of them, please stop reading ;){{</note>}}

The journey starts with **pre-commit** and **pre-push** tests. [These tests](https://github.com/ipspace/netlab/blob/dev/.pre-commit-config.yaml) are implemented with the **[pre-commit](https://pre-commit.com/)** tool and executed as Git actions on the developers' machines. It's impossible to enforce them[^DIP], so we're [repeating them as Github actions](https://github.com/ipspace/netlab/blob/dev/.github/workflows/tests.yml) (running them locally just reduces the turnaround time).

[^DIP]: The developer must install and enable the **pre-commit** tool to make them work.

The **pre-commit** tests are executed on every commit and should be as quick as possible. Our tests are running **[yamllint](https://yamllint.readthedocs.io/en/stable/)** to validate the YAML markup.

The **pre-push** tests run **mypy** to check the Python code. More importantly, they run a battery of tests that check whether we broke the most complex bit of _netlab_: the transformation of lab topology data into device data models. Right now, we have [~100 transformation tests](https://github.com/ipspace/netlab/tree/dev/tests/topology/input) and another [100 tests checking _netlab_ error handling](https://github.com/ipspace/netlab/tree/dev/tests/errors).

The test harness for these tests is quite simple:

* Read the lab topology
* Run the core transformation code
* Compare the transformed data mode with the expected results (or generated error messages with the expected error messages) and report the differences

While the above approach isn't exactly equivalent to unit tests, it's pretty efficient (it has saved my bacon numerous times). It's also a fantastic tool whenever I do code refactoring; something's badly wrong if the refactored code cannot reproduce the expected results.

