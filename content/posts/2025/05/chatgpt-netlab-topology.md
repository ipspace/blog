---
title: "Vibe Coding netlab Lab Topology with ChatGPT"
date: 2025-05-19 07:08:00+0200
tags: [ netlab, AI ]
netlab_tag: overview
ai_tag: kick
---
I was considering an AI add-on that would have access to the netlab documentation and help you figure out how to use it for a few years, but never got around to implementing it (and surprisingly, with all the AI hype out there, there were no volunteers submitting pull requests). A few weeks ago, someone suggested adding an MCP server as an interface to ipSpace.net content, but the discussion quickly devolved into vague ideas.

However, as ChatGPT now has access to the live Internet, I decided to try out whether it can get the job done with a bit of prompting.

**TL&DR:** After a hiccup, it worked surprisingly well.
<!--more-->
I started with a short prompt, giving ChatGPT the background information and a simple task to solve:

{{<long-quote>}}
netlab is a lab creation tool documented at https://netlab.tools/ with additional examples provided at https://blog.ipspace.net/tag/netlab/ and sample lab topologies at https://github.com/ipspace/netlab-examples. Can you use that documentation to create a lab topology with three routers (r1, r2, r3) connected in a triangle and running ospf in area 1?
{{</long-quote>}}

Here's what I got back:

{{<long-quote>}}
Certainly! Here's a `netlab` topology file that defines a lab with three routers (`r1`, `r2`, `r3`) connected in a triangle, all running OSPF in area 1.

```
defaults:
  device: frr
  module: [ospf]

nodes:
  r1:
  r2:
  r3:

links:
  - r1:
      r2:
        ospf.area: 1
  - r2:
      r3:
        ospf.area: 1
  - r3:
      r1:
        ospf.area: 1
```

**Explanation:**

-   **defaults**: Sets the default device type to FRRouting (`frr`) and includes the OSPF module.
-   **nodes**: Defines three routers: `r1`, `r2`, and `r3`.
-   **links**: Establishes point-to-point links between each pair of routers, forming a triangle. Each link is configured to be in OSPF area 1 by specifying `ospf.area: 1` for each connection.

This configuration ensures that all interfaces participating in OSPF are within area 1. For more details on OSPF configuration in `netlab`, you can refer to the official documentation. [netlab.tools](https://netlab.tools/module/ospf/?utm_source=chatgpt.com).

Let me know if you need further assistance or additional configurations!
{{</long-quote>}}

Surprisingly good for the first attempt, but ChatGPT got the indentation wrong. Vibe coding my way to a working lab, I copy-pasted the suggestion into `topology.yml` and executed **netlab up**. Of course, it failed.

{{<long-quote>}}
I tried your topology and got this error message: 

```
[ERRORS]  Errors found in test.yml
[ATTR]    links: Invalid interface attribute 'r2' found in links[1].r1
[HINT]    use 'netlab show attributes interface' to display valid attributes
[ATTR]    links: Invalid interface attribute 'r3' found in links[2].r2
[ATTR]    links: Invalid interface attribute 'r1' found in links[3].r3
[FATAL]   Cannot proceed beyond this point due to errors, exiting
```

Can you please try to fix the topology?
{{</long-quote>}}

The result: ChatGPT figured out its mistake and corrected the topology. Looks like our error messages aren't that bad ;)

{{<long-quote>}}
Thanks for sharing the error message — it looks like I made a formatting mistake in the way the links were defined. Each link should list the devices at the same level, and `ospf.area` should be an attribute of the whole link or interface, not nested incorrectly.

Here’s the corrected `netlab` topology file for a triangle of three routers running OSPF in area 1:

```
defaults:
  device: frr
  module: [ospf]

nodes:
  r1:
  r2:
  r3:

links:
  - r1: {}
    r2: {}
    ospf.area: 1
  - r2: {}
    r3: {}
    ospf.area: 1
  - r3: {}
    r1: {}
    ospf.area: 1
```

**Explanation of the Fix:**

-   Each `links` entry now correctly defines two endpoints (`r1`, `r2`, etc.) as separate keys at the same level.

-   `ospf.area: 1` is an attribute of the link, not incorrectly embedded within the device definitions.

You should now be able to use this topology file with `netlab` without hitting the attribute error. Let me know if you'd like to enable interface IP addressing, authentication, or additional features.
{{</long-quote>}}

ChatGPT still missed the _dictionary values could be empty_ trick, but the provided topology works. Pushing the envelope, I asked whether I could use the **interfaces** link attribute to make the topology cleaner.

{{<long-quote>}}
That's wonderful and it works. However, could you use the "interfaces" link attribute to define devices connected to the links?
{{</long-quote>}}

The result was all I could hope for:

{{<long-quote>}}
Absolutely! Using the `interfaces` attribute is a valid and often clearer way to define which devices are connected to each link in `netlab`. Here's your corrected triangle OSPF lab using the `interfaces` attribute:

```
defaults:
  device: frr
  module: [ospf]

nodes:
  r1:
  r2:
  r3:

links:
  - interfaces: [r1, r2]
    ospf.area: 1
  - interfaces: [r2, r3]
    ospf.area: 1
  - interfaces: [r3, r1]
    ospf.area: 1
```

**Benefits of using `interfaces`:**

-   Cleaner and more consistent syntax, especially for more complex topologies.
-   Easier to automate or modify links since you're listing devices as an array.

This version should work identically in function but may be easier to maintain or read, especially in larger topologies. Let me know if you'd like to add IP addressing, loopbacks, or OSPF router IDs!
{{</long-quote>}}

Next, I attempted to persuade ChatGPT to define the OSPF area only once, rather than for each link, which derailed the conversation. It suggested using **defaults.interfaces** (wrong) and **defaults.links** (also wrong), but when I kept reporting that the resulting lab has interfaces in OSPF area 0, ChatGPT eventually figured out it has to configure OSPF area on nodes.

However, the hallucination gave me a few ideas:

* Maybe we should start checking the contents of the **defaults** dictionary and report errors instead of silently accepting bogus default settings.
* It might be interesting to define the default interface and link parameters.

Anyway, here's the final bit of our conversation:

{{<long-quote>}}
Apologies for the confusion earlier. You're correct in observing that setting `ospf.area` under `defaults.links` or `defaults.interfaces` does not apply the desired OSPF area to all interfaces in the topology. This is due to how `netlab` propagates default values.

According to the [netlab documentation](https://netlab.tools/module/ospf/), the default OSPF area for interfaces is determined by the node's OSPF area, which in turn defaults to the global OSPF area. However, if the OSPF area is not explicitly set at the node level, interfaces may default to area 0.

To ensure that all interfaces are in OSPF area 1, you should explicitly set the OSPF area at the node level. Here's the corrected topology:

```
defaults:
  device: frr
  module: [ospf]

nodes:
  r1:
    ospf:
      area: 1
  r2:
    ospf:
      area: 1
  r3:
    ospf:
      area: 1

links:
  - interfaces: [r1, r2]
  - interfaces: [r2, r3]
  - interfaces: [r3, r1]
```

By setting `ospf.area: 1` under each node, all interfaces on these nodes will inherit area 1, ensuring consistent OSPF configuration across the topology.

Let me know if you need further assistance or additional configurations!
{{</long-quote>}}

**Long story short:** You have no excuse not to try out _netlab_ ;), and if you're OK with running FRRouting containers, you can [do it for free in a GitHub Codespace](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/).