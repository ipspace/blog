---
url: /2007/04/executing-ios-commands-from-tcl-shell.html
title: "Executing IOS Commands from Tcl Shell"
date: "2007-04-02T19:43:00.001+02:00"
tags: [ Tcl ]
---

The Tcl procedures used to execute IOS commands in Embedded Event Manager (cli\_open, cli\_write ...) don't work when you [start Tcl shell from command line interface](/2007/03/running-tcl-procedures-from-command.html). To execute IOS commands in this context, use:

-   **exec *command*** to execute an exec-level command, for example **exec "show ip route"**
-   **ios\_config *mode* *command*** to configure the router

If the first parameter of the ios\_config command is a global configuration command, you shall omit the second parameter (for example, **ios\_config "hostname router"**). To configure a parameter in one of the sub-configuration modes (for example, interface state), use the first parameter to specify the configuration mode and the second parameter as the actual configuration command (for example, **ios\_config "interface loop 0" "no shutdown"**).

{{<jump>}}[Keep reading](/kb/Tclsh/){{</jump>}}