---
date: 2009-11-13 07:29:00.002000+01:00
tags:
- security
- WAN
- EEM
title: Detect DoS Attacks with EEM
url: /2009/11/detect-dos-attacks-with-eem/
---
Someone sent me an interesting question a while ago: "is it possible to detect DOS flooding with an EEM applet?" Of course it is (assuming the DOS attack results in very high load on the Internet-facing interface) and the best option is the EEM interface event detector.

{{<figure src="/2009/11/s400-Detect+interface+overload.png" caption="Detecting interface overload with EEM">}}

The **interface** event detector is more user-friendly than the SNMP event detector. You can specify interface name and parameter name in the **interface** event detector; with SNMP event detector you have to specify SNMP object identifier (OID). The **interface** event detector stores the interface name, measured parameter name and its value in three convenient environment variables that you can use to generate *syslog* messages or alert the operators via e-mail.
<!--more-->
**Notes:**

-   You must use the **bandwidth** command to set the interface bandwidth to the actual line speed.
-   Set the **bandwidth** to the access speed of your Internet service on Ethernet uplinks.
-   The range of the **rxload** and **txload** parameters is between 0 and 255.
-   Interface load is computed as 256 \* input-or-output-rate / configured-bandwidth.
-   The input-or-output-rate is a weighted average computed over the **load-interval**.
