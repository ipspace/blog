---
title: "[FATAL] Ansible Release 12.0 Breaks netlab Jinja2 Templates"
series_title: "Fixing Ansible-induced Templating Crashes (Release 25.09-post1)"
date: 2025-09-14 19:25:00+02:00
tags: [ netlab ]
netlab_tag: release
---
On September 9th, the [**ansible** release 12.0](https://pypi.org/project/ansible/#history) appeared on PyPi. It requires [**ansible-core** release 2.19](https://pypi.org/project/ansible-core/#history), which [includes breaking changes](https://github.com/ansible/ansible/blob/v2.19.2/changelogs/CHANGELOG-v2.19.rst#breaking-changes-porting-guide) to Jinja2 templating. _netlab_ Jinja2 templates rely on a few Ansible Jinja2 filters; _netlab_ thus imports and uses those filters, and it looks like those imports pulled in the breaking changes that consequently broke the _netlab_ containerlab configuration file template ([details](https://github.com/ipspace/netlab/issues/2683)).

_netlab_ did not check the Ansible core version (we never had a similar problem in the past), and the installation scripts did not pin the Ansible version (feel free to blame me for this one), which means that any new _netlab_ installation created after September 9th crashed miserably on the simplest lab topologies.

This is the workaround we implemented in [_netlab_ release 25.09-post1](https://netlab.tools/release/25.09/#release-25-09-post1) (released earlier today):
<!--more-->
* The **netlab** command checks the Ansible core version and refuses to run with Ansible core 2.19 or greater.
* The only exception to the above rule is the **netlab install** command, which is the recommended mechanism for downgrading Ansible in simple installations.
* The installation script used by the **netlab install ansible** command pins the Ansible release to 11.10 or lower.

I also added more information to the **netlab version** command to simplify troubleshooting of similar issues.

### Potential Root Cause

I'm suspecting [this](https://github.com/ansible/ansible/blob/ca99cc7e555443ee211c155d26456d0ecc2f3fec/changelogs/CHANGELOG-v2.19.rst?plain=1#L255) is the root cause of the crashes we're experiencing:

> templating - Access to `_` prefixed attributes and methods, and methods with known side effects, is no longer permitted. In cases where a matching mapping key is present, the associated value will be returned instead of an error. This increases template environment isolation and ensures more consistent behavior between the `.` and `[]` operators.

_netlab_ heavily uses `_` prefixed attributes for internal data that is not checked against the lab topology schema. The _netlab_ data transformation code computes some of those attributes, which are later used in the device configuration templates. Sometimes these attributes are not defined, so we're using the `|default()` filter on them, and that seems to trigger Jinja2 templating errors. Every use of `_` prefixed attribute with Ansible release 12.0 is thus a ticking bomb.

### What's Next?

Here are my early ideas on what to do next (they will probably change as we discuss them):

* Keep the _netlab_-installed Ansible version pinned to release 11.10 (or lower) for the foreseeable future.
* Remove the dependency on Ansible filters used in _netlab_ templates (primarily the **ipaddr** filter), either using another library like [j2ipaddr](https://pypi.org/project/j2ipaddr/) or writing our own filters.

Eventually, we'll have to bite the bullet and figure out how to handle device configuration templates. We could:

* Create device configurations with _netlab_ and use Ansible solely to push them to network devices, or
* Thoroughly check all our Ansible playbooks and Ansible-rendered device configuration templates.

Finally, I don't blame the Ansible team for anything that happened. They do what they feel is the right thing for their project. I just hate that there's no feature flag we could set to disable a breaking change.

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
