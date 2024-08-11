---
title: "Arista cEOS Got Working MPLS Data Plane"
date: 2024-08-14 07:35:00+0200
tags: [ MPLS ]
---
[Urs Baumann](https://www.linkedin.com/in/ubaumannch/) brought me a nice surprise last weekend. He [opened a GitHub issue](https://github.com/ipspace/netlab/issues/1267) saying, "_MPLS works on Arista cEOS containers in release 4.31.2F_" and asking whether we could enable _netlab_ to configure MPLS on cEOS containers.

{{<note>}}_netlab_ already had [MPLS configuration templates for Arista EOS](https://netlab.tools/module/mpls/#platform-support) but reported an error message if you tried to use MPLS with the cEOS containers because the containers did not have a working MPLS data plane.{{</note>}}

After [a few configuration tweaks](https://github.com/ipspace/netlab/commit/3a1debf251da446a8758c8ae4f1b90bc8c938d2b) and a [batch of integration tests later](https://tests.netlab.tools/_html/eos-clab-mpls), I had the results: everything worked. You can use MPLS on Arista cEOS with _netlab_ release 1.9.0 (right now @ `1.9.0-dev2`), and I'll be able to create MPLS labs running in GitHub Codespaces in the not-too-distant future.