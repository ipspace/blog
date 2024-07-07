---
title: "Network Digital Twins Work Best in PowerPoint"
date: 2022-04-20 06:07:00
tags: [ automation ]
---
A friend of mine sent me the following question a few months ago:

> I thought you might know the best way (currently) to create a digital clone of parts of a production network? The objective is to test changes against a test network as part of a CI/CD process. Ideally, there would be an automation that could replicate selected parts of a production network in a test network.

**TL&DR**: Sounds great, but you might be solving the wrong problem.
<!--more-->
Ignoring for the moment the [data plane quirks](/2022/03/dataplane-quirks-virtual-devices/) that ensure you'll never be able to test the full impact of changes, and the minor details of interface names being different on physical and virtual gear, let's focus on the elephant in the room: configuration consistency.

You might have a network following a carefully thought-out design where every device performs a well-defined role. You don't need a digital twin of that network; all you need is a minimal representation that covers all device roles and potential connectivity between them.

Data center leaf-and-spine fabrics might come close to that holy grail, most other networks tend to be a haphazard pile of kludges organically grown over years or decades. How will you select a representative subset of that network so that any configuration change you might want to test will be adequately covered? I wish you luck, and I hope you won't waste too much time on that effort.

Furthermore, keep in mind that a "representative subset" is only representative if it includes every variation of device configuration found in the wild, otherwise you won't catch a weird interaction between the configuration change you want to test, and the existing configuration deployed on a particular "custom configured" device. Unless you managed to automate configuration deployments, or spent a lot of time fighting configuration drift, I'm pretty positive that after a few years, the "representative subset" might turn out to be "the whole network".

Trying to extract a meaningful test subset from a live network is an exercise in futility (see also: [building firewall rules from NetFlow data](/2020/09/flow-tracking-halting-problem/)), the only sane way to approach "I want to test configuration changes in a virtual lab" challenge is to:

* [Standardize the network services](/2022/02/cleanup-before-automation/) and minimize the number of configuration variants;
* [Clean up your network design](/2020/06/adapting-network-design-for-automation/).
* (Hopefully) Clean up existing device configurations to adhere to the new standards;
* Make changes only to standardized configurations and consistently apply them to all devices.

After you did that bit of a homework, you can [build a virtual test network based on device roles and expected connectivity specified in your design](/2019/09/if-you-have-to-simulate-your-whole/), and deploy standardized configurations on lab devices... but even then you're not done yet. Did you [write the tests](/2021/12/ci-cd-network-automation-tests/) that you'll run on the test network? No? Do tell me, [what exactly were you planning to test](/2021/12/gitops-device-configurations/)?

Does all of the above mean that the virtual test labs have no value? Absolutely not. Anything you can use to simplify or streamline pre-deployment tests is a huge improvement over "_we hope this works, and the change control board agrees with us_"... but make sure you don't get bedazzled by the shiny new tools, and keep in mind the gotchas of using an imperfect model of the real world[^AMW].

[^AMW]: All models are wrong, but some are useful ([attributed to George Box](https://en.wikipedia.org/wiki/All_models_are_wrong))