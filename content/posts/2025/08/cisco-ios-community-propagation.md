---
title: "BGP Community Propagation on Cisco IOS/XE: The 90's Called"
date: 2025-08-11 08:09:00+0200
tags: [ netlab,BGP ]
netlab_tag: quirks
---
Just when I thought no vendor ~~stupidity~~ [peculiarity](https://blog.ipspace.net/tag/netlab/#quirks) could surprise me,  Cisco IOS/XE proved me wrong.

I was improving a completely unrelated BGP functionality. I ran BGP integration tests on Cisco IOL (because it's the fastest one to boot), and the [BGP community propagation](https://github.com/ipspace/netlab/blob/dev/tests/integration/bgp/05-community.yml) test failed. After verifying that I did not change the template and that the data structures had not changed, I checked the IOL release I was using.

Surprise 🎉🎉: the **neighbor send-community** configurations that worked since (at least) the IOS Classic release 15.x stopped working in Cisco IOS/XE release 17.16.01a.
<!--more-->
### Background Story

This is the help message offered by a Cisco IOS router for the **neighbor send-community** configuration command:

```
dut(config-router-af)#nei 10.1.0.1 send-community ?
  both      Send Standard and Extended Community attributes
  extended  Send Extended Community attribute
  standard  Send Standard Community attribute
  <cr>      <cr>

```

{{<note>}}
The `<cr> <cr>` bit is trying to tell you that it's OK to press ENTER without specifying the community type, but fails to mention it means *standard community propagation*. Oh well, we've seen worse.
{{</note>}}
That's super-annoying to implement in a configuration template when your data structure contains a list of community types that should be sent to a neighbor.

Purely by accident (one has to suppose), using two configuration commands gets the desired results:

{{<cc>}}Configuring standard and extended BGP community propagation on Cisco IOSv release 15.9(3){{</cc>}}
```
dut(config-router-af)#neighbor 10.1.0.2 send-community standard
dut(config-router-af)#neighbor 10.1.0.2 send-community extended
dut(config-router-af)#do show run | include neighbor 10.1.0.2 send
  neighbor 10.1.0.2 send-community both
```

The **neighbor send-community standard** command followed by the **neighbor send-community extended** command magically results in **neighbor send-community both**. Mission Accomplished!

However, that no longer works in Cisco IOS/XE release 17.16.01a (even though it worked until at least IOS/XE release 17.15.01).

{{<cc>}}Configuring standard and extended BGP community propagation on IOS/XE 17.16.01a{{</cc>}}
```
dut(config-router-af)#neighbor 10.1.0.2 send-community standard
dut(config-router-af)#neighbor 10.1.0.2 send-community extended
dut(config-router-af)#do show run | include neighbor 10.1.0.2 send
  neighbor 10.1.0.2 send-community extended
```

WTA*? The propagation of standard BGP communities is gone.

Considering all the fairy tales I've been hearing about how it's impossible to change any ridiculous old setting in a major network operating system, I'd love to know what triggered this sudden "back to the 90s" stunt.
