---
title: "Networking Quirks Observed During netlab Tests"
url: /quirks/index.html
minimal_sidebar: True
---
One of the interesting _netlab_ use cases is the ability to explore how different vendors implement the same functionality.
For that to work, we try to [configure network devices](https://github.com/ipspace/netlab/tree/dev/netsim/ansible/templates) to maximize interoperability with devices from other vendors. We might miss some details, but as the average vendor investment in helping us get things right (so far) has been close to zero, I don't think they have a right to complain ;)

We also want to ensure the device configurations we created work as expected, so we run [hundreds of integration tests](https://tests.netlab.tools/). We run integration tests between devices from different vendors whenever possible, using FRR or Arista EOS containers as the probe device. There are a few reasons we're using these devices as probes:

* Their container versions [boot surprisingly fast](https://blog.ipspace.net/2023/02/virtual-device-boot-times/).
* They are easily configured using the "industry standard" configuration syntax[^WIOS].
* Their **show** commands produce easy-to-consume JSON data.

[^WIOS]: A weasely way of saying "Cisco IOS" without getting sued

We [prefer FRR](/2023/06/learn-routing-protocols-frr/) (it boots faster and has a much smaller memory footprint) but use Arista when needed because it can display more information (for example, [VRRP neighbors](/2025/01/sturgeon-law-vrrp-edition/)) in JSON format.

The focus on interoperability inevitably uncovers [quirks](/tag/netlab/#quirks) that would remain unnoticed when building a single-vendor network. Please don't blame us for the quirks we document or for mentioning a device on which we found the unexpected behavior. If you're working for a vendor, getting them fixed is much better.

Finally, pull requests that improve device configuration templates while keeping configurations relatively simple are always most welcome.
