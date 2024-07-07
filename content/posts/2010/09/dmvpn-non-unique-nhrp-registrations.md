---
date: 2010-09-27 06:32:00.002000+02:00
dmvpn_tag: quirk
tags:
- DMVPN
title: 'DMVPN: Non-Unique NHRP Registrations'
url: /2010/09/dmvpn-non-unique-nhrp-registrations/
---
During my last DMVPN webinar, one of the students mentioned the need for non-unique NHRP registrations in environments where the public IP address of a DMVPN spoke site changes due to DHCP lease expiration or PPPoE session termination. Finally I found some time to recreate the scenario in my DMVPN lab; here are the results.
<!--more-->
### Default Behavior

Next-Hop Resolution Protocol (NHRP) was designed for large layer-2 switched network environments (example: ATM networks with SVC support). In those environments, the layer-2 address of a site never changes and thus NHRP clients uses *unique registrations* by default; the mapping between IP address (*protocol address* in terms of [RFC 2332](http://tools.ietf.org/html/rfc2332)) and underlying layer-2 address (RFC 2332: *NBMA address*) is not supposed to change.

NHRP clients set the *uniqueness* bit in the registration packets and Next-Hop Server (NHS) subsequently refuses all registration packets that try to set a different *NBMA address* for an already-known *protocol address*.

### Impact on DMVPN Networks

In DMVPN world, *protocol address* is tunnel interface's IP address and *NBMA address* is the IP address of the **tunnel source** (usually the outside -- Internet-facing -- interface). The tunnel interface flaps when the IP address on the outside interface changes, triggering NHRP registration request, but the registration requests are rejected by the NHS until the old registration expires (registration hold time is set by the client and configured with the **ip nhrp holdtime** interface configuration command).

### Non-Unique Registrations

If you're experiencing DMVPN downtime due to changing public IP addresses of your DMVPN spokes, apply the **ip nhrp registration non-unique** interface configuration command to the DMVPN tunnel interface. This command will reduce the recovery time to less than a minute. Faster recovery is harder to achieve as the router has to execute a number of steps following a physical interface flap:

-   Install new static routes to the hub sites;
-   Create IPSec session with the hub sites;
-   Register new public IP address with NHRP;
-   Establish routing adjacency.

You can fine-tune steps 1-3 on the spoke router; step 4 sometime requires coordinated changes throughout the network.
