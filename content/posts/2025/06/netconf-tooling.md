---
title: "Where Are the NETCONF/YANG Tools?"
date: 2025-06-04 07:38:00+0200
tags: [ NETCONF ]
---
Jo attempted to follow the vendor Kool-Aid recommendations and use NETCONF/YANG to configure network devices. Here's what he [found](https://blog.ipspace.net/2025/05/screen-scraping-2025/#2644) (slightly edited):

---

IMHO, the whole NETCONF ecosystem primarily suffers from a tooling problem. Or I haven't found the right tools yet.

[ncclient](https://ncclient.readthedocs.io/en/latest/) is (as you mentioned somewhere else) an underdocumented mess. And that undocumented part is [not even up to date](https://github.com/ncclient/ncclient/issues/374#issuecomment-595092038). The commit hash at the bottom of the docs page is from 2020... I am amazed how so many people got it working well enough to depend on it in their applications.
<!--more-->
The tools for browsing and inspecting YANG models are also not really there. Everything is abandoned. Cisco killed/abandoned two of its projects already. [YANG Explorer](https://github.com/CiscoDevNet/yang-explorer) is dead, and yangsuite fails to install and has outdated docs. [Installation documentation](https://developer.cisco.com/docs/yangsuite/welcome-to-cisco-yang-suite/#python-virtualenv-installation) talks about Python 3.6 to 3.8, the [README](https://github.com/CiscoDevNet/yangsuite) is stuck at 3.9+ with 3.10 recommended. However, installations fail for more modern versions. All the systems I am working on ship 3.11 or newer by default now.

The Docker container was also an insane amount of pain until it worked. And of course, the code is not on GitHub; the repo there is just a dummy repo for the Docker container. All I was looking for was a nice way to display what my device supports and to display and edit the values so that I can see what I am doing in a sea of XML

There have been a couple other tools that I have found which were dead even longer.

Am I missing some nice tool? What are people actually using to get things done with NETCONF?

---

I had [similar experiences](https://blog.ipspace.net/2017/03/to-yang-or-not-to-yang-thats-question/). I tried to demonstrate how to use YANG to validate a custom network automation data model, but I failed miserably.

Kristian Larsson [wrote a blog post at that time](https://plajjan.github.io/2017-03-15-validating-data-with-YANG.html) explaining how you can get the job done, so I'm guessing there must be solutions out there that work, and it's just that our Google-Fu is failing us. **[pyang](https://github.com/mbj4668/pyang/wiki/Documentation)** seems to be a tool that could accomplish some YANG-related tasks; pointers to other working, up-to-date tools would be highly appreciated.
