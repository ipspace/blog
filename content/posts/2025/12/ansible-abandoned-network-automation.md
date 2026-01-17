---
title: "Has Ansible Team Abandoned Network Automation?"
date: 2025-12-16 08:28:00+0100
lastmod: 2026-01-16 11:18:00+0100
tags: [ Ansible ]
---
A month ago, I described how Ansible release 12 [broke the network device configuration modules](/2025/11/ansible-12-different/#configs), the little engines ([that could](https://en.wikipedia.org/wiki/The_Little_Engine_That_Could)) that brought us from the dark days of copy-and-paste into the more-survivable land of configuration templates.

{{<note update>}}
In the meantime, the Ansible networking team [fixed](https://github.com/ansible-collections/ansible.netcommon/pull/743) the **ansible.netcommon** collection, but (according to that PR) the ability to process templated configurations directly in the network configuration modules is scheduled to disappear in January 2028 ([more details](https://github.com/ansible-collections/ansible.netcommon/issues/745#issuecomment-3756755302)). I moved on; _netlab_ is now [generating device configurations outside of Ansible](https://netlab.tools/release/26.01/#release-26-01-breaking).
{{</note>}}

Three releases later (they just released 13.1), the same bug is still there (at least it was on a fresh Python virtual environment install I made on a Ubuntu 24.04 server on December 13th, 2025), making all ***device*\_config** modules unusable (without changing your Ansible playbooks) for configuration templating. Even worse:
<!--more-->
* The documentation of network modules (for example, **arista.eos.eos_config**) hasn't changed and still claims one can use Jinja2 template file as the **src** parameter.
* I found no issues in either the Ansible core GitHub repo or the Arista collection repo complaining about this unwanted behavior.

What could that mean? Here are a few ideas from the end-user perspective:

* Nobody is brave enough to try pushing through the [Ansible Windows Vista](/2025/11/ansible-12-different/) moment.
* Nobody cares enough to complain about yet another minor detail in a product that is ~~broken~~ different from previous releases in so many other ways.
* Nobody uses configuration templates anymore; all the cool kids drink the Intent Kool-Aid.
* The oldtimers have working installations using old versions of the products; the newbies will try to replicate something they found on the Internet, decide they're [too stupid to make it work](https://blog.ipspace.net/2024/05/too-stupid-to-make-it-work/), and hopefully move to another solution.
* Worst case, people trying to enter the Network Automation land will decide it's simpler to stay a CLI jockey than to deal with broken bloatware and useless documentation.

OK, and what could a devious mind conclude about the viability of Ansible for network automation projects:

* It's evident nobody is testing even the most common network configuration modules, otherwise such a blatant bug couldn't survive four releases (each of them having [multiple pre-release versions](https://pypi.org/project/ansible/#history)) 
* Even worse, the "lack of templating" behavior seems to be caused by something shared by many networking modules. Even that code hasn't been tested.

Before you tell me that the paid Ansible product works (and I'm pretty sure it does), the attitude of releasing a product that's useless for a particular well-publicized use case is no better than Juniper releasing a vJunos-something VM with a [broken DHCP server on its management interface](https://blog.ipspace.net/2023/10/vjunos-declines-dhcp-address/). One of the hoped-for side effects of releasing free stuff is to enhance uptake and grow the sales funnel; releasing broken stuff tends to have the opposite effect.

Making things worse, many Ansible network automation collections are abandonware. One has to look no further than the [**nokia.grpc** collection](https://github.com/nokia/ansible-networking-collections)[^NGR] that was last updated four years ago and still has [open issues from 2020](https://github.com/nokia/ansible-networking-collections/issues), including the [Please Update the Collection](https://github.com/nokia/ansible-networking-collections/issues/30) one from 2023 saying "the SR OS collection hasn't been updated in three years"

[^NGR]: You could say I'm picking on Nokia. I might be, but someone decided to make _netlab_ dependent on those collections, so I care about them more than some other random stuff.

Draw your own conclusions :(

### More Information

* A RedHat knowledge base article [describing the fix](https://access.redhat.com/solutions/7136399)
* [Deprecating existing behavior might be a bad idea](https://github.com/ansible-collections/ansible.netcommon/issues/745) (now as a proper GitHub issue)
* [Christophe Fauveau](https://www.linkedin.com/in/cfauveau/) agrees that [network automation should become a first-class Ansible citizen](https://www.linkedin.com/posts/cfauveau_has-ansible-team-abandoned-network-automation-activity-7416750440819830786-xc_B/)
* [Sean Cavanaugh](https://www.linkedin.com/in/seanecavanaugh/) described why (in his opinion) the [whole thing is not a big deal](https://www.linkedin.com/feed/update/urn:li:activity:7406731770064355329?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7406731770064355329%2C7417311906153234432%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287417311906153234432%2Curn%3Ali%3Aactivity%3A7406731770064355329%29) ([standalone article](https://www.linkedin.com/posts/seanecavanaugh_ansible-activity-7417317909238022145-OHWx)) and why [they haven't caught the bug in months](https://www.linkedin.com/feed/update/urn:li:activity:7417317909238022145?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7417317909238022145%2C7417650705567571968%29&replyUrn=urn%3Ali%3Acomment%3A%28activity%3A7417317909238022145%2C7417657140204462080%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287417650705567571968%2Curn%3Ali%3Aactivity%3A7417317909238022145%29&dashReplyUrn=urn%3Ali%3Afsd_comment%3A%287417657140204462080%2Curn%3Ali%3Aactivity%3A7417317909238022145%29). I think we'll have to agree to disagree.

### Revision History

2026-01-16
: Added the *More Information* section with links to related opinions and articles

2026-01-13
: The [PR fixing the bug](https://github.com/ansible-collections/ansible.netcommon/pull/743) has been merged on January 12th, 2026, and will eventually appear in **ansible.netcommon** collection. However, it's interesting to note that the [potential breakage was first documented in April 2025](https://github.com/ansible-collections/ansible.netcommon/issues/698) (HT: [Tony Bourke](https://blog.ipspace.net/2025/12/ansible-abandoned-network-automation/#2830)), and the issue was closed without anyone ever testing the basic templating functionality.
