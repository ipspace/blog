---
date: 2009-08-28 06:35:00+02:00
tags:
- BGP
title: Disable Flapping BGP Neighbors
url: /2009/08/disable-flapping-bgp-neighbors/
lastmod: 2020-12-29 09:51:00
---
It looks like we're bound to experience a widespread BGP failure once every few months. They all follow the same pattern:

-   A "somewhat" undertested BGP implementation starts advertising paths with "unexpected" set of attributes.
-   A specific downstream BGP implementation (and it could be a different implementation every time) a few hops down the road hiccups and sends a BGP notification message to its upstream neighbor.
-   BGP session must be reset following a notification message; the routes advertised over it are lost and withdrawn, causing widespread ripples across the Internet.
-   The offending session is reestablished seconds later and the same set of routes is sent again, causing the same failure and a session reset. If the session stays up long enough, some of the newly received routes might get propagated and will flap again when the session is reset.
-   The cyclical behavior continues until a manual intervention.
<!--more-->
I don't understand why network OS vendors allow the cyclical BGP session behavior (as it's pretty obvious things will not get better by themselves once the same session is reset a few times), but there's at least something we can do on Cisco IOS with Embedded Event Manager: shut down the offending neighbor after seeing the *BGP-3-NOTIFICATION* syslog message often enough in a short period of time.

{{<note update>}}**Update 2020-12-29:** Many modern network operating systems provide similar functionality; worst case, you can deploy a Python script on most of them.{{</note>}}

The following EEM applet is triggered when the *BGP-3-NOTIFICATION* syslog message occurs more often than three times in the last 60 seconds. It extracts the BGP neighbor ID from the syslog message, fetches local AS number from an SNMP variable and shuts down the offending neighbor using **neighbor shutdown** BGP router configuration command.

{{<cc>}}EEM 3.0 applet source code{{</cc>}}
```
event manager applet BGPNotification
 event syslog occurs 3 pattern "BGP-3-NOTIFICATION" period 60
 action 100 regexp "neighbor\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"   →
   "$_syslog_msg" match id
 action 200 if $_regexp_result eq 1
 action 300  info type snmp oid bgp.2.0 get-type exact
 action 400  cli command "enable"
 action 410  cli command "configure terminal"
 action 420  cli command "router bgp $_info_snmp_value"
 action 430  cli command "neighbor $id shutdown"
 action 500  syslog msg "Shut down BGP neighbor $id"
 action 510  info type routername
 action 520  mail server $_mail_smtp to $_mail_rcpt →
   from "$_info_routername@$_mail_domain" →
   subject "ALERT: BGP neighbor $id shutdown due to excessive notifications" →
   body "\n$_syslog_msg"
 action 999 end 
```

**Notes**

* The EEM applet does not track session failures per neighbor. It might hit a random BGP neighbor that just happens to have a bad-hair microsecond while another neighbor is flapping;
* There is no recovery logic -- once the neighbor is shut down you have to reenable it manually;
* You better have pretty good monitoring in place to be alerted when this hammer-of-Thor strikes.
