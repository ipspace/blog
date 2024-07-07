---
date: 2021-01-26 07:06:00+00:00
lastmod: 2021-03-17 06:40:00
series:
- xml-json
tags:
- automation
title: Fixing XML-to-JSON Conversion Challenges
---
In the last weeks I described the challenges you might face when converting XML documents that contain lists with a single element into JSON, be it on device (Nexus OS) or in an Ansible module. Now let's see how we can fix that.

{{<series single="1">}}
<!--more-->
### The Provably Correct Way

Networking vendors are very vocal about their support for YANG data models. The correct approach would thus be to read the YANG data model before converting the XML document, identify XML elements that are supposed to be lists, and convert them into Python/JSON lists/arrays regardless of how many elements they have.

It makes perfect sense to use YANG data model on the device when generating XML or JSON from common data structure, but doing it on your own just to convert some data you got from a **show** command sounds like using a [Canadair CL-415](https://en.wikipedia.org/wiki/Canadair_CL-415) to put out a dumpster fire (if you ever find a video of that, please post it in the comments), but I'm positive there's a library out there doing exactly that (or a Rube Goldberg hack involving a half-dozen disparate projects glued together with Super Glue).

Gerhard Wieser was [quick to point out](https://twitter.com/G_wieser/status/1349658380034519040) that they wrote a tool to do exactly what I was asking, but looking at their [getting started page](https://docs.frinx.io/frinx-odl-distribution/oxygen/getting-started.html) it looks like the tool is focused more toward device configurations (that's a different problem) and running on top of Open Daylight, which feels like acquiring an aircraft carrier so you'll be able to launch your Canadair to put out that dumpster fire.

In any case, life would be much simpler if there would have been an attribute in XML tags that are supposed to be lists, but that boat sailed decades ago...

### The Idealistic Way

Sander Steffann proposed an idealistic solution that's too good to ever get implemented (it does have a few side effects though): what if Ansible would use a modified *dict* object that would behave like a one-element list when used in Jinja2 list context.

Unfortunately, I'm positive a lot of people use dictionaries like lists (either intentionally or by mistake/ignorance), figure out that's a way to get keys out of the dictionary (instead of using **dict.keys()**) and move on. Don't ever tell me how Python is better than Perl because there's only one way of doing things.

Making the change Sander is proposing would break all that stuff. Not going to happen...

### The Pragmatic Way

We want to have a list, and we got a dictionary. How about writing a small filter plugin that would return a list no matter what's passed to it:

```
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from jinja2 import TemplateError

def make_list(l):
  return l if type(l) is list else [l]

class FilterModule(object):
  def filters(self):
    return {
      'make_list': make_list
    }
```

Here's how you can use that plugin to create a list of VLANs configured on a Nexus switch:

```
- hosts: c_nxos
  gather_facts: false
  tasks:
  - cisco.nxos.nxos_command:
      commands: "show vlan | json"
    register: vlans
  - debug:
      msg: |
        {% for vlan in 
          vlans.stdout[0].TABLE_vlanbrief.ROW_vlanbrief
            |make_list %}
        id: {{ vlan['vlanshowbr-vlanid'] }} name: {{ vlan['vlanshowbr-vlanname'] }}
        {% endfor %}
```

The "only" drawback of this approach: you have to be careful to pass all data that could be lists through that filter, otherwise you're bound to create some nasty hard-to-find bugs.

---

**True story**: I stumbled upon this problem almost exactly four years ago when I was creating a sample solution to deploy VLAN services on Nexus switches for the first run of our automation course. Everything worked fine until I tested the playbooks on a newly provisioned switch that had only the default VLAN. Kaboom...

---

[Christopher Hart solved the same problem in a more creative way](https://www.chrisjhart.com/Normalizing-JSON-Data-Structure-Output-On-Cisco-NX-OS-With-Python/): Nexus OS uses a naming convention where everything that should be a list has a name starting with **ROW\_**, so it's pretty easy to take the whole data structure returned by Nexus OS and fix it in one go. One has to wonder why they didn't do it that way in the first place...

### The Hack (Take One)

This is the [original Jinja2 hack](https://github.com/ipspace/VLAN-service/blob/VLAN_Cleanup/getinfo/nxos-vlans.j2) I used in January 2017. It relies on Jinja2 treating lists almost like dictionaries: if the VLAN row data contains a well-known attribute (VLAN ID) it must be a dictionary, otherwise it's a list and we need to iterate over a list. 

```
{% set data = nxos_results.stdout[0].TABLE_vlanbrief.ROW_vlanbrief %}
{% if data['vlanshowbr-vlanid-utf'] is defined %}
{{ vlan(data) }}
{% else %}
{%   for v in data %}
{{ vlan(v) }}{% if not(loop.last) %},
{%     endif %}
{%   endfor %}
{% endif %}
```

Interestingly, the same is true for Python. If you know a name of a dictionary key, you can figure out whether you'd dealing with a dictionary *or something else* (but you don't know what it is) just by testing for presence of that key... unless, of course, you're dealing with a string, so don't. Use **type** or **isinstance**.

```
$ python3
>>> lst=(1,2,3)
>>> dct={'a': 1}
>>> print('a' in lst)
False
>>> print('a' in dct)
True
>>> print('a' in 'a stupidity')
True
```

### The Hack (Take Two)

Since the times I wrote my original hack Ansible got **flatten** filter, so you can embed your data into a single-element list, push it through **flatten** and you'll get either a single-element list or the original list. I'm positive this hack can also break in horrendous ways, but I'm not devious enough to find them in five seconds so whatever.

```
- hosts: c_nxos
  gather_facts: false
  tasks:
  - cisco.nxos.nxos_command:
      commands: "show vlan | json"
    register: vlans
  - debug:
      msg: |
        {% for vlan in 
            [ vlans.stdout[0].TABLE_vlanbrief.ROW_vlanbrief ]
              |flatten(levels=1) %}
        id: {{ vlan['vlanshowbr-vlanid'] }} name: {{ vlan['vlanshowbr-vlanname'] }}
        {% endfor %}
```

### Getting Your Hands Dirty

Download the [source code](https://github.com/ipspace/netlab-examples/tree/master/Ansible/XML) for these examples, [setup your virtual lab](https://github.com/ipspace/netlab-examples/blob/master/Ansible/XML/README.md), and have fun.

## Revision History

2021-03-17
: Added a pointer to a Python-based workaround by Christopher Hart

