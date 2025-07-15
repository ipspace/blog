---
title: "Always Check Your Tests Against Faulty Inputs"
date: 2025-07-21 07:19:00+0200
tags: [ automation ]
series: [ cicd ]
cicd_tag: testing
---
A while ago, I published a blog post [proudly describing](/2025/06/testing-ospf-configurations/) the _netlab_ integration test that should [check for incorrect OSPF network types](https://github.com/ipspace/netlab/blob/d9051cf06471160a2b97791df44145351800149a/tests/integration/ospf/ospfv2/01-network.yml) in _netlab_-generated device configurations. Almost immediately, Erik Auerswald [pointed out](https://blog.ipspace.net/2025/06/testing-ospf-configurations/#2682) that my test wouldn't detect that error (it might detect other errors, though) as the OSPF network adjacency is always established even when the adjacent routers have mismatching OSPF network types.

I made one of the oldest testing mistakes: I checked whether my test would work *under the correct conditions* but not whether it would detect *an incorrect condition*.
<!--more-->
Effectively, my test was a highly dramatized version of[^GRN]:

```
def check_ospf_network_type(node):
  return true
```

[^GRN]: See also: [generating random numbers](https://xkcd.com/221/)

**Lesson learned:** Whenever you write a test, check what happens when you give it all sorts of incorrect inputs. Also, a false positive (claiming things work when they're broken) is even more annoying than a false negative (claiming things are broken when they're OK). You can oftentimes quickly fix a false negative, but you won't know you're dealing with false positives until something breaks badly enough to be noticed.
