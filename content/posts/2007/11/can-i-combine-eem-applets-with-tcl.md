---
url: /2007/11/can-i-combine-eem-applets-with-tcl.html
title: "Can I combine EEM applets with Tcl shell?"
date: "2007-11-26T07:27:00.002+01:00"
tags: [ Tcl,EEM ]
---

When I've been [describing the limitations of kron](/2007/11/kron-poor-man-cron.html), someone quickly asked an interesting question:

> As I cannot insert extra input keystrokes with EEM applet, can I run a Tcl script from it with the **action *sequence* cli command "tclsh *script*"** command and use the **typeahead** function call to get around the limitation?” 

The only answer I could give at that time was “maybe” … and obviously it was time for a more thorough test. The short result is: YES, you can do it (at least in IOS release 12.4(15)T1).
<!--more-->
I've started by creating a small Tcl script (see below) that clears the counters on *Loopback 0*. As the **clear counters** command requires keyboard input and generates a syslog message, it was a perfect test case.

``` code
typeahead "y"
exec "clear counter loop 0"
```

I've copied this script into the *flash:tcl/clearL0.tcl* and tested it:

``` code
R1#tclsh flash:tcl/clearL0.tcl
%CLEAR-5-COUNTERS: Clear counter on interface Loopback0 by console
```

So far, so good. Next, I've created an EEM applet with no trigger:

``` code
event manager applet Clear
 event none
 action 1.0 cli command "enable"
 action 1.1 cli command "tclsh flash:tcl/clearL0.tcl"
```

… enabled the EEM CLI debugging and started it:

``` code
R1#debug event man action cli
Debug EEM action cli debugging is on
R1#event man run Clear
R1#
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : CTL : cli_open called.
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : OUT :
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : OUT : R1>
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : IN  : R1>enable
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : OUT :
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : OUT : R1#
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : IN  : R1#tclsh flash:tcl/clearL0.tcl
%CLEAR-5-COUNTERS: Clear counter on interface Loopback0 by  on vty0 (EEM:Clear)
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : OUT :
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : OUT : R1#
%HA_EM-6-LOG: Clear : DEBUG(cli_lib) : : CTL : cli_close called.
```

Great. It works. Let's move on: I've inserted a trigger into the EEM applet that ran the applet when an OSPF neighbor reached *FULL* adjacency:

``` code
event manager applet Clear
 event syslog pattern "OSPF-5-ADJCHG.*to FULL"
 action 1.0 cli command "enable"
 action 1.1 cli command "tclsh flash:tcl/clearL0.tcl"
```

And now for the final test: after I've enabled the serial interface, OSPF neighbors established adjacency …

``` code
R1(config-if)#interface ser 1/0
R1(config-if)#no shutdown
R1(config-if)#
%LINK-3-UPDOWN: Interface Serial1/0, changed state to up
%LINEPROTO-5-UPDOWN: Line protocol on Interface Serial1/0, changed state to up
%OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.2 on Serial1/0 from LOADING to FULL, Loading Done
%CLEAR-5-COUNTERS: Clear counter on interface Loopback0 by  on vty0 (EEM:Clear)
```

… and the counters on Loopback0 were cleared. Mission accomplished :)
