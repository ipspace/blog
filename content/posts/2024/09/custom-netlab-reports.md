---
title: "Custom netlab Reports"
date: 2024-09-19 07:15:00+0200
netlab_tag: guidelines
tags: [ netlab ]
---
A [previous blog post](/2024/07/using-netlab-reports/) described how you can use the **[netlab report](https://netlab.tools/netlab/report/)**  functionality to generate addressing, wiring, BGP, and OSPF reports from a running lab. But what could you do if you need a report that doesn't exist yet? It's straightforward to define one (what else did you expect?).

Let's create the report I used in the [EVPN Hub-and-Spoke Layer-3 VPN](/2024/09/hub-spoke-evpn/) blog post to create the VRF table.
<!--more-->
We need two bits of information to start our process:

* What should be the filename of the report definition?
* Where do we have to store it?

**netlab report** provides both answers when you invoke it with an unknown report name:

```
$ netlab report vrf.md
[ERRORS]  Errors found in topology.yml
[VALUE]   report: Cannot find "vrf.md.j2" in any of the report directories
[HINT]    A report can be specified in a file with .j2 suffix within 'reports' subdirectory in package-,
          system-, user- or current directory. You can also specify a report in a defaults.outputs.report
          setting.
```

Next, we must figure out where to get the information we want to display in the report. **netlab report** takes the information from the transformed data model (from the `netlab.snapshot.yml` file). That file is created when you start the lab with the **[netlab up](https://netlab.tools/netlab/up/)** command; you can also create it with the **[netlab create](https://netlab.tools/netlab/create/)** command.

You can inspect the transformed data with a text editor (it's a YAML file), with a tool like [yq](https://github.com/mikefarah/yq/), or with the **netlab inspect** command. I know the global VRF data is in the **vrfs** dictionary, so it was easy to display it:

```
$ netlab inspect vrfs
hub_egress:
  evpn:
    evi: 4
    transit_vni: 200003
  export:
  - '65000:4'
  id: 4
  import:
  - '65000:4'
  rd: '65000:4'
hub_ingress:
  evpn:
    evi: 3
    transit_vni: 200002
  export:
  - '65000:3'
  id: 3
  import:
  - '65000:3'
  rd: '65000:3'
s_1:
  evpn:
    evi: 1
    transit_vni: 200000
  export:
  - '65000:4'
  id: 1
  import:
  - '65000:3'
  rd: '65000:1'
s_2:
  evpn:
    evi: 2
    transit_vni: 200001
  export:
  - '65000:4'
  id: 2
  import:
  - '65000:3'
  rd: '65000:2'
```

Now we have all the information we need. Our report has to iterate over the **vrfs** dictionary and display relevant bits from it. Here's the first approximation:

```
{# description: VRF parameters #}
| VRF | RD | Export RT | Import RT | EVPN VNI |
|-----|---:|-----------|-----------|---------:|
{% for vname,vdata in vrfs.items() %}
| {{ vname }} | {{ vdata.rd }} | {{ vdata.export }} | {{ vdata.import }} | {{ vdata.evpn.transit_vni }} |
{% endfor %}
```

That's good enough for what I needed, but we can do better. For example, the import and export route targets are displayed as Python lists:

```
$ netlab report vrf.md
| VRF | RD | Export RT | Import RT | EVPN VNI |
|-----|---:|-----------|-----------|---------:|
| hub_egress | 65000:4 | ['65000:4'] | ['65000:4'] | 200003 |
| hub_ingress | 65000:3 | ['65000:3'] | ['65000:3'] | 200002 |
| s_1 | 65000:1 | ['65000:4'] | ['65000:3'] | 200000 |
| s_2 | 65000:2 | ['65000:4'] | ['65000:3'] | 200001 |
```

Also, **vdata.evpn.transit_vni** (or even **vdata.evpn**) might not be defined.

To fix the Python lists, we have to pipe the import and export route targets through a `join` filter. While doing that, we can also supply the default value in case the attribute is missing:

```
vdata.import|default([])|join('<br>')
```

Dealing with **vdata.evpn.transit_vni** is a bit harder as we're dealing with two levels of dictionaries, so we have to use something like this:

```
vdata.evpn.transit_vni|default('') if vdata.evpn is defined else ''
```

How do you put convoluted expressions like the ones above into a single like (to generate Markdown markup) without making the template look like a single-line Perl contortion? Jinja2 allows you to start a new line immediately after the `{{` sequence, so you can put each expression into a separate line, resulting in the final report:

```
| VRF | RD | Export RT | Import RT | EVPN VNI |
|-----|---:|-----------|-----------|---------:|
{% for vname,vdata in vrfs.items() %}
| {{ vname }} | {{ 
     vdata.rd|default('') }} | {{ 
     vdata.export|default([])|join('<br>') }} | {{
     vdata.import|default([])|join('<br>') }} | {{
     vdata.evpn.transit_vni|default('') if vdata.evpn is defined else '' }} |
{% endfor %}
```

Have you created your own custom reports in the past? I'd love to hear about them. Leave a comment or email me (or, even better, submit a pull request).
