---
title: "Quality of OSPFv2 NSSA Implementations"
date: 2025-06-24 07:44:00+0200
tags: [ OSPF, netlab ]
ospf_tag: areas
netlab_tag: quirks
---
A few weeks ago, we added OSPF areas functionality to _netlab_. In the next release[^DB], you'll be able to configure stub areas, NSSA areas, inter-area route summarization and filtering (OSPF ranges), and summarization of NSSA type-7 prefixes for OSPFv2 and OSPFv3.

OSPFv2 (defined in [RFC 2328](https://www.rfc-editor.org/rfc/rfc2328.html)) is 27 years old, and NSSA functionality ([RFC 3101](https://datatracker.ietf.org/doc/html/rfc3101)) was last touched 22 years ago. One would hope the implementations in network devices are mature and feature-complete. Yeah, keep dreaming 🤦‍♂️.
<!--more-->
[^DB]: Or right away if you [clone our repo](https://netlab.tools/install/clone/) and use the *dev* branch.

When we started developing the configuration templates for OSPF areas, I wrote a comprehensive [integration test](https://blog.ipspace.net/2024/05/netlab-integration-tests/) that checks:
 
* Configuration of stub and NSSA areas;
* Summarization of intra-area routes (OSPF ranges)
* Summarization of type-7 NSSA routes (NSSA ranges)
* Setting the default route cost for stub and NSSA areas
* Totally stubby areas (no inter-area routes are inserted into the area)

The test topology is (as always) [available on GitHub](https://github.com/ipspace/netlab/blob/9031a8031e1dc0be00d3d7cfd69c2782b647ae09/tests/integration/ospf/ospfv2/40-area-parameters.yml), and the test results are summarized in the [OSPFv2](https://tests.netlab.tools/_html/coverage.ospf.ospfv2) and [OSPFv3](https://tests.netlab.tools/_html/coverage.ospf.ospfv3) test results (*Area Parameters* somewhere close to the bottom of the page; click the *Device* link to get more details).

As you can see from the test results, of the devices on which we implemented this functionality[^SPR], only Junos and the latest FRR release passed all the tests with flying colors. Meanwhile:

* Cisco IOS (release 17.12) and Arista EOS (release 4.33.1F) do not support NSSA ranges
* Aruba CX and SR Linux cannot configure the cost of the type-7 default route inserted into the NSSA area
* Cumulus Linux 5.10 (the last public version) does not translate type-7 routes into type-5 routes due to a bug in the ancient FRR release it's using
* Dell OS10 (release 10.5.6.6) does not support NSSA ranges (no big deal), but it gets confused when facing the "complex" setup described above and forgets to set the E bit on router LSA, making the translated type-5 LSAs useless.

[^SPR]: Are you sad that your favorite platform is missing? What's stopping you from submitting a PR with another configuration template?

As you can see, it's best not to trust vendors when they claim they support some functionality. I'm positive that all of the above vendors claim they support RFC 3101, and technically, they're not wrong; the devil is in the details, which are often caused by the weasely "should" wording in the RFCs.
