---
cli_tag: challenge
date: 2017-04-04 10:37:00+02:00
series:
- cli
tags:
- automation
title: Let’s Drop Some Random Commands, Shall We?
url: /2017/04/lets-drop-some-random-commands-shall-we.html
---
One of my readers sent me a link to [CCO documentation](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/7-x/fundamentals/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_Fundamentals_Configuration_Guide_7x/b_Cisco_Nexus_9000_Series_NX-OS_Fundamentals_Configuration_Guide_7x_chapter_0101.html#con_1215472) containing (at that time) this gem:

> Beginning with Cisco NX-OS Release 7.0(3)I2(1), Cisco Nexus 9000 Series switches handle the CLI configuration actions in a different way than before the introduction of NX-API and DME. The NX-API and DME architecture introduces a delay in the communication between Cisco Nexus 9000 Series switches and the end host terminal sessions, for example SSH terminal sessions.

So far so good. We can probably tolerate some delay. However, the next sentence is a killer...

{{<note update>}}2017-05-08: The behavior is caused by an old bug in Linux TTY driver. Fixed NX-OS versions are planned to be shipped in late May 2017. [More details here](https://blog.ipspace.net/2017/05/follow-up-nexus-os-dropping.html).\
\
2017-04-05: The wonderful information disappeared from Cisco\'s documentation within 24 hours with no explanation whatsoever. However, I expected that and took a [snapshot of that page](http://web.archive.org/web/20170403161751/http://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/7-x/fundamentals/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_Fundamentals_Configuration_Guide_7x/b_Cisco_Nexus_9000_Series_NX-OS_Fundamentals_Configuration_Guide_7x_chapter_0101.html) before publishing the blog post ;){{</note>}}
<!--more-->
> This delay causes the configuration lines to be dropped randomly when pasting the configurations to the switches. In most cases, the severity of the issue is directly proportional to the length of the configurations that are pasted into the terminal sessions. For example, pasting an ACL with greater than 600 lines often results in more lines getting dropped than pasting an ACL with only 100 lines.

Wait, WHAT? Your latest software release is randomly dropping configuration commands and you find it appropriate to document the behavior in some obscure section of the documentation instead of fixing it? What happened to the company I liked to work with for decades? This approach literally makes me sick.

I can't possibly fathom how someone could get the idea that it's perfectly fine to take commands received over a reliable communication channel (SSH sessions ran over TCP the last time I checked) and randomly drop a few of them for convenience reasons. Would it be so hard to wait for the previous command to finish and then read the next line from the TCP buffer? Or use NX-API internally to execute CLI commands if that's the only reliable way to talk to the box?

Not only does this make any CLI-based automation totally unreliable (not that it ever was completely reliable), as the documentation succinctly explains, even cut-and-paste is no longer guaranteed to work. The only "reliable" mechanism might be **scp *file device:*running-config** unless they broke that one as well.

On a totally unrelated note, I had to switch from NX-API to CLI during my [Ansible for Networking Engineers](http://www.ipspace.net/Ansible_for_Networking_Engineers) webinar because the NX-API got less reliable with every software update, returning random 404 (page not found) errors. Admittedly I was running NX-OS image in VIRL, but I got similar reports from engineers running real-life networks.

Even though my calendar claims it's 2017 it seems like I'll have to add another line to the [Network Automation RFP Requirement](https://blog.ipspace.net/2016/10/network-automation-rfp-requirements.html): device should not drop random commands received over any management-plane communication channel. Being [big-time into Model Driven Manageability](http://blog.ipspace.net/2016/10/network-automation-rfp-requirements.html?showComment=1477403406970#c1792883115184277297) doesn't help much if you can't get the fundamentals right.
