---
date: 2025-10-02 08:19:00+00:00
netlab_tag: extend
pre_scroll: true
series_title: Applying Simple Configuration Changes
tags:
- netlab
title: "netlab: Applying Simple Configuration Changes"
---
For years, netlab has had [custom configuration templates](https://netlab.tools/custom-config-templates/) that can be used to deploy custom configurations onto lab devices. The custom configuration templates can be Jinja2 templates, and you can create [different templates (for the same functionality) for different platforms](/2022/04/multi-platform-custom-netsim-config/). However, using that functionality if you need an extra command or two makes approximately as much sense as using a Kubernetes cluster to deploy a *[BusyBox](https://en.wikipedia.org/wiki/BusyBox)* container.

_netlab_ release 25.09 solves that problem with the **[files](https://netlab.tools/plugins/files/)** plugin and the *[inline config](https://netlab.tools/plugins/files/#inline-node-group-configuration-templates)* functionality.
<!--more-->
Imagine you have a very simple BGP lab in which you want the edge router to advertise a default route over an IBGP session[^DRI].

[^DRI]: You could use the **[bgp.session.apply](https://netlab.tools/plugins/bgp.session/#applying-bgp-session-attributes-to-ibgp-sessions)** functionality of the [bgp.session](https://netlab.tools/plugins/bgp.session/) plugin to advertise a default route to *all* IBGP neighbors, but not to a single neighbor.

{{<cc>}}The lab topology -- as simple as one can make it ;){{</cc>}}
```
defaults.device: eos
provider: clab
module: [ bgp, ospf ]
bgp.as: 65000

nodes:
  edge:
  core:

links: [ edge-core ]
```

{{<figure src="/2025/10/config-inline-bgp.png" caption="BGP sessions in the above lab topology">}}

The above topology generates the following BGP configuration on the Edge router:

{{<cc>}}Arista EOS BGP configuration on the Edge router{{</cc>}}
```
router bgp 65000
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   bgp advertise-inactive
   neighbor 10.0.0.2 remote-as 65000
   neighbor 10.0.0.2 update-source Loopback0
   neighbor 10.0.0.2 description core
   neighbor 10.0.0.2 send-community standard extended large
   !
   address-family ipv4
      neighbor 10.0.0.2 activate
      neighbor 10.0.0.2 route-map next-hop-self-ipv4 out
      network 10.0.0.1/32
```

However, we'd need an extra command -- **neighbor 10.0.0.2 default-originate always**.

This is how easy it is to add that command to the Edge router configuration with *netlab* release 25.09 ([complete topology file](https://github.com/ipspace/netlab-examples/blob/master/config/simple/topology.yml)):

{{<cc>}}Modifications to the lab topology needed to add an extra configuration command{{</cc>}}
{{<printout>}}
plugin: [ files ]

nodes:
  edge:
    config.inline: |
      router bgp 65000
        neighbor 10.0.0.2 default-originate always
{{</printout>}}

**Notes:**

* **config.inline** functionality needs the new **files** plugin  (line 1) that creates custom configuration templates [behind the scenes](#BDS).
* The **config.inline** attribute (line 5) can be used on individual nodes or node groups (when you need to apply the same command to multiple nodes).
* The **config.inline** value (multiple lines of configuration commands) should always use the multiline YAML encoding (`|`, also known as _literal ‌block scalar header_).

### Behind the Scenes { #BDS }

This is what _netlab_ does with the **config.inline** attribute:

* The attribute content is stored in a file named **\_n\_*node*.j2** in the lab directory.
* The node **config** attribute is converted into a list using the node-specific filename as a custom configuration template. In our lab, the **config** attribute of the **edge** node would be set to `[ _n_edge ]`.
* Once the node has a "regular" **config** attribute, _netlab_ uses the existing mechanisms to apply the custom configuration commands.
