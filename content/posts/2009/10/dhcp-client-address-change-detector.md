---
date: 2009-10-07 06:56:00+02:00
tags:
- DHCP
- EEM
title: DHCP Client Address Change Detector
url: /2009/10/dhcp-client-address-change-detector.html
lastmod: 2020-12-05 08:36:00
---
In a previous post I've described [how useless DHCP logging is when you try to detect change in DHCP-assigned IP address](/2009/09/dhcp-logging-in-cisco-ios-is-nightmare.html). Fortunately the removal of the old IP address (triggered by the DHCPNAK server response) and configuration of the new IP address (sent in the DHCPACK response) triggers a change in the IP routing table that can be detected with the IP routing table event detector introduced in EEM 3.0 (available from Cisco IOS release 12.4(22)T).
<!--more-->
{{<ct3_rescue>}}

Symptom
: Change in the client IP address assigned by a DHCP server to a Cisco router is hard to detect due to lack of consistent DHCP-related <em>syslog</em> message. Cisco IOS generates a DHCP-6-ADDRESS_ASSIGN <em>syslog</em> message when an interface configured with <strong>ip address dhcp</strong> acquires its initial address through DHCP, but not when the address is subsequently changes due to a DHCP NAK response from the DHCP server.

Solution
: Change in an interface IP address always generates a change in the IP routing table: the connected route to the subnet of the old IP address is removed and new connected route is inserted in the IP routing table. The change in the IP routing table can be detected with the IP routing event detector introduced in EEM 3.0.

The following EEM applet requires the IP routing event detector, programming logic and regular expression support available in Embedded Event Manager 3.0 (first released with Cisco IOS release 12.4(22)T).

{{<cc>}}Applet source code{{</cc>}}
```
event manager applet DHCPAddressChange
 event routing network 0.0.0.0/0 type add protocol connected ge 1
 !
 action 100 cli command "show ip interface brief | include $_routing_lastinterface"
 !
 action 110 regexp "YES\s+DHCP" "$_cli_result"
 !
 action 200 if $_regexp_result eq 1
 action 220  set ipaddress "unknown"
 action 230  regexp " ([0-9.]+) " "$_cli_result" match ipaddress
 action 240  info type routername
 action 250  mail server "$_mail_smtp" to "$_mail_rcpt" from "$_info_routername@$_mail_domain" →
             subject "DHCP address on $_routing_lastinterface changed to $ipaddress" →
             body "\n$_cli_result"
 action 299 end 
```

The **event routing network 0.0.0.0/0 type add protocol connected** event detector detects all additions of connected routes (the 0.0.0.0/0 mask indicates we want to catch all changes regardless of the actual IP prefix).

Connected routes could change after interface flaps or manual configuration changes. The **show ip interface brief** command is thus used to inspect the IP address allocation method of the affected interface (the interface name is available in the **$\_routing\_lastinterface** EEM variable).

The presence of “YES\\s+DHCP” pattern in the **show ip interface brief** command output indicates the interface is operational and got its IP address via DHCP. In this case, the actual IP address is extracted from the **show ip interface brief** command output and sent in an e-mail to the network operator.

## Additional configuration

The EEM applet expects several EEM environmental variables defining your SMTP environment. A sample configuration is included in the following printout (you could also replace these variables with hardcoded values in the EEM applet).

```
event manager environment _mail_smtp 10.17.0.2
event manager environment _mail_domain example.com
event manager environment _mail_rcpt operator@example.com
```

