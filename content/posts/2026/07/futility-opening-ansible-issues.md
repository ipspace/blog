---
title: "On the Futility of Opening Ansible Issues"
date: 2026-07-22 08:03:00+0200
tags: [ ansible ]
---
Remember the anonymous troll who [chided me](https://blog.ipspace.net/2025/12/ansible-abandoned-network-automation/#2821) for [writing a rant](https://blog.ipspace.net/2025/12/ansible-abandoned-network-automation/) instead of opening a GitHub issue in the relevant Ansible repository? Well, I decided to be an open-source poster boy when I stumbled upon the next Ansible bug, and ended up feeling like a sweet summer child :(
<!--more-->
I was troubleshooting a broken Cisco IOS template when I noticed that, even though the configuration commands were not accepted, Ansible **cisco.ios.ios_config** module reported no errors. I looked at the Ansible code, realized it wasn't recognizing the specific error message, and [opened an issue](https://github.com/ansible-collections/cisco.ios/issues/1301). After all, they'd just need to add another line to the list of known error messages.

What I got instead was a little better than "_did you try configuring **no router eigrp** followed by **router eigrp**_" response I got from an entry-level Cisco TAC operator[^RCE] when I reported an EIGRP bug pointing to the exact debugging message proving it was a bug. Instead of someone adding a single line to the Cisco IOS **network_cli** connection module, I got an explanation of the `ansible_terminal_stderr_re` parameter. 

Nothing wrong with that as a workaround, but an error message like "IPv6 routing not enabled" is probably not so rare that it doesn't deserve to be in the [venerable list of known Cisco IOS error messages](https://github.com/ansible-collections/cisco.ios/blob/b010de7e3e760fb135a0ee97fcc6390156c295bb/plugins/terminal/ios.py#L43)[^BEIT], and (reading the issue history) it [looks like](https://github.com/ansible-collections/cisco.ios/issues/1301#issuecomment-3966817779) one of the [Ansible developers](https://github.com/ganeshrn) agreed with me.

[^RCE]: I refuse to call that individual "an engineer".

[^BEIT]: That list includes "BGP: Error initializing topology". If someone knows how to get that one, please write a comment.

Alas, nothing happened, and the issue was automatically closed months later. Maybe I'll [write a rant](/2026/07/ansible-config-content/) the next time 🤦‍♂️, that seems to produce better results 🤷‍♂️.

**Update 2026-07-23:** A few hours after this blog post has been published, the issue was reopened, and it got fixed within another hour. I'll leave the decision whether that "ruined the blog post" as [Sander](https://blog.ipspace.net/2026/07/futility-opening-ansible-issues/#3036) claimed or proved my point 🤷‍♂️ to you.
