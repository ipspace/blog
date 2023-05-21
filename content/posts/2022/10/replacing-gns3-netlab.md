---
date: 2022-10-28 07:26:00+00:00
netlab_tag: video
tags:
- video
- netlab
title: Could I Use netlab instead of GNS3?
---
I'm often getting questions along the lines of _"I'm using GNS3. Could I replace it with [netlab](https://netlab.tools/)?"_

**TL&DR**: No.

You need a set of functions to build a network lab:

* Virtualization environment (netlab supports VirtualBox, libvirt, Docker, Podman)
* An orchestration tool/system that will deploy network device images in such an environment (netlab supports Vagrant and containerlab)
* A tool that will build orchestration system configuration (netlab core functionality)
<!--more-->
The above list is the absolute minimum you need to get a running lab. You could either build such an environment from individual components (*netlab* approach) or use an integrated solution often available as a deployable virtual machine (GNS3 and Cisco CML/VIRL approach).

*netlab* thus cannot replace GNS3 or VIRL, it's one of the tools in a flexible composable toolchain. It also offers tons of other features that you cannot get in GNS3 or VIRL (more about that in another blog post), and enables you to build intent-based labs[^MBS] instead of drawing them in a GUI.

[^MBS]: Marketing bullshit for "_it uses a text file to define what you want to build_."

For more details, watch the *[Why Do We Need Another Labbing Tool](https://my.ipspace.net/bin/get/NetTools/N1%20-%20Why%20Do%20We%20Need%20Another%20Labbing%20Tool.mp4?doccode=NetTools)* video I recorded in September 2022 as part of [Network Automation Tools webinar](https://www.ipspace.net/Network_Automation_Tools).

{{<jump>}}[Watch the video](https://my.ipspace.net/bin/get/NetTools/N1%20-%20Why%20Do%20We%20Need%20Another%20Labbing%20Tool.mp4?doccode=NetTools){{</jump>}}

{{<note info >}}You need [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free) to watch the video and [Standard ipSpace.net Subscription](https://www.ipspace.net/Subscription) to watch the rest of the webinar.{{</note>}}
