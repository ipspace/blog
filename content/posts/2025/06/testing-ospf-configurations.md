---
title: "Testing OSPF Device Configurations"
date: 2025-06-25 08:40:00+0200
netlab_tag: testing
tags: [ automation, netlab ]
series: [ cicd ]
cicd_tag: testing
---
A year ago, I described how we use the **netlab validate** command to [test device configuration templates](/2024/05/netlab-integration-tests/) for most platforms supported by _netlab_. That blog post included a simple "this is how you test interface address configuration" example; now, let's move to something a bit more complex: baseline OSPF configuration.

Testing the correctness of OSPF configurations seems easy:

* Build a lab with a test device and a few other OSPF devices
* Configure the devices
* Log into the test device and inspect OSPF operational data

There's just a tiny little fly in this ointment...
<!--more-->
It's impractical to parse the **show** printouts from over a dozen different platforms, and the temperature in hell might drop considerably[^EU] before every vendor implements the IETF (or OpenConfig) YANG data models[^DMC]. The only way to deal with a multi-platform environment is to rely on the protocol behavior, figure out the behavior of the tested device from the adjacent probes, and hope that the probes work correctly ([not always true](/2025/06/evpn-route-attributes-matter/)).

[^EU]: Assuming hell is impacted by the usual laws of physics and the expansion of the universe.

[^DMC]: Assuming these data models contain the information we need, it is not always a given.

For example, to test the **[activation of OSPF on individual interfaces](https://github.com/ipspace/netlab/blob/dev/tests/integration/ospf/ospfv2/04-passive.yml)**:

* Connect a probe (P1) to an interface that should be activated
* Connect another probe (P2) to an interface that should not be activated.
* Wait for the OSPF adjacency between P1 and the device under test (DUT). If adjacency is not established within a reasonable timeframe[^OSPF_LAN], assume the OSPF interface configuration on the DUT is faulty.
* Wait a bit longer[^GTR] (just in case, because we're trying to prove a negative) and check the OSPF adjacency between P2 and DUT. An established adjacency points to a configuration error on the DUT.

[^OSPF_LAN]: We use 50 seconds as the worst-case scenario -- 10 seconds to receive hello packets, 30 seconds to elect the DR/BDR, and an additional 10 seconds to complete the adjacency process.

[^GTR]: Getting the timing just right is a bit of a challenge. Sometimes the first adjacency is established surprisingly fast, and the second one takes way longer. You should wait an extra 2-3 hello intervals to be on the safe side.

While the above is the simplest possible test one can do, we don't start with it. It takes ridiculously long (if you have to run hundreds of tests on dozens of platforms) for OSPF to establish an adjacency on broadcast networks (the typical default setting); it's much faster to use point-to-point links[^P2PF]. Our first test is therefore **testing the configuration of OSPF network types**:

* Configure one link (P1-DUT) as an OSPF broadcast network and another link (P2-DUT) as an OSPF point-to-point link.
* Wait for both adjacencies to be established.

[^P2PF]: Most devices establish a point-to-point OSPF adjacency within a few seconds; sometimes, it's established before we even start the validation phase. The broadcast adjacency pretty consistently takes around 40 seconds. You can check the validation logs for individual devices for more details; click the device name on the [OSPFv2](https://tests.netlab.tools/_html/coverage.ospf.ospfv2)/[OSPFv3](https://tests.netlab.tools/_html/coverage.ospf.ospfv3) coverage report and then click the green checkmark in the *validated* column of the *01-network* row. View the validation results of other OSPF tests for additional data points; most of them verify the P2P adjacency as the initial step in the validation process.

If a device passes the test, we know that (A) it can activate OSPF on interfaces (but we are not yet sure whether it does that correctly) and (B) that it sets the OSPF network type correctly (because a mismatch in OSPF network type prevents the adjacency from being established). After validating this baseline, we can use the OSPF point-to-point network type in all further OSPF tests, significantly reducing the overall validation time.

You can probably guess how the other tests work:

* The **OSPF areas** test configures probes in different areas and checks for OSPF adjacencies (an area mismatch prevents an adjacency from being established)
* The **OSPF over unnumbered interfaces** tests adjacency over interfaces with "borrowed" IP addresses
* The **OSPF costs** test configures various (unusual) costs on the DUT interfaces; the probes verify the end-to-end cost of the remote probe's loopback, proving that the cost configured on the DUT interface matches the expected value.
* The **OSPF timers** test configures small values for the hello/dead intervals on all devices in the lab and checks for OSPF adjacencies (a timer mismatch also stops the adjacency from forming).

For even more details (or testing ideas), explore the [OSPFv2](https://github.com/ipspace/netlab/tree/dev/tests/integration/ospf/ospfv2) and [OSPFv3](https://github.com/ipspace/netlab/tree/dev/tests/integration/ospf/ospfv3) integration tests in the [netlab GitHub repository](https://github.com/ipspace/netlab).
