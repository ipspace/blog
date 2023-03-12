---
cli_tag: basics
date: 2016-10-27 08:30:00+02:00
series:
- cli
tags:
- automation
- SDN
title: To API or Not To API
url: /2016/10/to-api-or-not-to-api.html
---
One of my readers left this comment (slightly rephrased) on my [Network Automation RFP Requirements](https://blog.ipspace.net/2016/10/network-automation-rfp-requirements.html) blog post:

> Given that we look up to our \*nix pioneers as standard bearers for system automation, why do we demand an API from network devices? The API requirement would make sense if the vendor OS is a closed system. If an open system vendor creates APIs for applications running on their system (say for BGP configs) - kudos to them, but I no longer think that should be mandated.

He's right - API is not a mandatory prerequisite for reliable network automation.
<!--more-->
{{<note info>}}Getting started with network automation? My [online course](http://www.ipspace.net/Building_Network_Automation_Solutions) might be just what you need.{{</note>}}

It doesn't matter (from the reliability perspective) whether you make changes to a system configuration by modifying a text file and reloading the configuration, by running a CLI command, or by executing an API call. What does matter is that:

-   The change operation returns a well-defined and easy-to-detect OK/FAIL status;
-   The FAIL status includes an easy-to-detect error message;
-   The changes done through any of the above methods are *atomic* (all-or-nothing);
-   You can change many parts of the configuration in a single atomic transaction.

{{<note>}}Anyone who cut himself off a router while configuring an access list should be very familiar with the last requirement.{{</note>}}

While Linux or Windows CLI commands usually meet most of these requirements (exit codes, error messages sent to STDERR), many networking devices don't come even close.

Moving from system configuration to operational data: while it's not mandatory that the system returns operational data as structured data in easy-to-parse presentation format (XML or JSON), it helps immensely if it does, and Linux CLI is often no better than the stuff we have to deal with on networking devices. Linux forums are littered with arcane pipelines of commands that resemble line noise but produce exactly what you need if you ever master to understand how to tweak them.

APIs have obvious benefits over CLI commands, for example exposing just the functionality you want third parties to consume, but in the context of minimum mandatory requirements API is really just a [highly appreciated convenience mechanism](https://blog.ipspace.net/2014/02/cli-or-api-wait-do-you-really-have-to.html). It's so [much easier for a programmer to execute an HTTP(S) GET or POST request](http://blog.ipspace.net/2012/08/why-is-restful-api-better-than-snmp.html) than logging into the box via SSH and executing CLI commands or trying to figure out how to spell [NETCONF](http://blog.ipspace.net/2012/06/netconf-expect-on-steroids.html).
