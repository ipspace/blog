---
title: "Testing Network Automation Data Transformation"
netlab_title: "netlab Data Transformation Testing"
netlab_tag: overview
date: 2024-05-20 08:08:00+0200
tags: [ automation, netlab ]
series: [ cicd ]
cicd_tag: testing
---
Every complex enough network automation solution has to introduce a high-level (user-manageable) data model that is [eventually transformed](/kb/DataModels/65-Data-Transformation/) into a low-level (device) data model. 

{{<figure src="/2021/02/dm-magic.png" caption="High-level overview of the process" width="400">}}

The [transformation code](/2021/02/data-model-transformation/) (business logic) is one of the most complex pieces of a network automation solution, and there's only one way to ensure it works properly: you test the heck out of it ;) Let me show you how we solved that challenge in _[netlab](https://netlab.tools/)_.
<!--more-->
{{<note info>}}The rest of this blog post will sound ridiculously obvious to any decent software engineer. If you happen to be one of them, you can stop reading ;){{</note>}}

_netlab_ has grown from a tiny Vagrantfile generator into a massive tool supporting a [dozen technologies](https://netlab.tools/module-reference/), each with its data transformation requirements. A rigorous automated testing process is the only way to ensure we don't break stuff every other day. In this blog post, we'll focus on the top part of the _netlab_ architecture diagram:

{{<figure src="https://netlab.tools/_images/up.png" caption="Netlab high-level architecture diagram">}}

The journey starts with **pre-commit** and **pre-push** tests. [These tests](https://github.com/ipspace/netlab/blob/dev/.pre-commit-config.yaml) are implemented with the **[pre-commit](https://pre-commit.com/)** tool and executed as Git actions on the developers' machines. It's impossible to enforce them[^DIP], so we're [repeating them as GitHub actions](https://github.com/ipspace/netlab/blob/dev/.github/workflows/tests.yml) (running them locally just reduces the turnaround time) every time a new commit is pushed to the GitHub repository[^GHPR].

[^DIP]: The developer must install and enable the **pre-commit** tool to make them work.

[^GHPR]: We cannot enforce these tests in forked repositories, so we also run them on every pull request.

The **pre-commit** tests are executed on every commit and should be as quick as possible. Our tests are running **[yamllint](https://yamllint.readthedocs.io/en/stable/)** to validate the YAML markup.

The **pre-push** tests run **mypy** to check the Python code. More importantly, they run a battery of tests that check whether we broke the most complex bit of _netlab_: the transformation of lab topology data into device data models. Right now, we have [~100 transformation tests](https://github.com/ipspace/netlab/tree/dev/tests/topology/input) and another [100 tests checking _netlab_ error handling](https://github.com/ipspace/netlab/tree/dev/tests/errors). We're adding new tests to cover new functionality and every time we deal with a major bug. The debugging process usually starts with a minimal lab topology that triggers the bug; that topology becomes a new test case once the bug is fixed.

The [test harness](https://github.com/ipspace/netlab/blob/dev/tests/test_transformation.py) for these tests is quite simple ([more details](https://netlab.tools/dev/tests/)):

* Read the lab topology
* Run the core transformation code
* Compare the transformed data mode with the expected results (or generated error messages with the expected error messages) and report the differences

While one could argue that the above approach isn't equivalent to unit tests (it runs the whole transformation code, not a single component), it's pretty efficient and has saved my bacon numerous times. It's also a fantastic tool when I do code refactoring; something's wrong if the refactored code cannot reproduce the expected results.

I also wanted to ensure that the essential bits of code (the core components used in almost any lab topology) are well-tested. The [coverage](https://coverage.readthedocs.io/en/7.5.1/) tool was a perfect solution. It reports whether each line of Python code was executed, and adding a few test cases or tweaking lab topologies can bring you as close to 100% coverage as you wish.

Last but not least, we have over 150 integration tests (more about them in the next blog post), and just to be on the safe side, we [run them through the data transformation engine](https://github.com/ipspace/netlab/blob/dev/tests/check-integration-tests.sh) on every pull request. The code merged into the main development branch is thus guaranteed to:

* Produce correct results for all transformation test scenarios.
* Not to crash on any lab topology used for integration tests.

Can you use the same approach to test your network automation solution? Of course; if you [feel like borrowing some of the source code](https://github.com/ipspace/netlab/blob/dev/LICENSE.md), please feel free to do so. There's just one gotcha if you use a [home-grown database or a third-party tool](/2019/04/text-files-or-relational-database/) (like *[Nautobot](https://networktocode.com/nautobot/)*) instead of YAML files as the [source of truth](/series/ssot/): how will you create the test scenarios?

[^MTO]: A giant test case derived from a sample database would work, but figuring out which part of the data transformation code is broken would be a nightmare. It's much better to have numerous test cases focusing on small subsets of functionality.

The most straightforward approach to that conundrum might be the one propagated by ancient Romans: divide and conquer[^MTO]. Split the SoT-to-device-data process into data extraction and data transformation and test each one individually. You could use a sample database and the expected results to test the data extraction phase and numerous test scenarios (stored as YAML files) to test the data transformation logic.

{{<next-in-series page="/posts/2024/05/netlab-integration-tests.html">}}**Coming up next**: Testing Network Automation Device Configuration Templates{{</next-in-series>}}