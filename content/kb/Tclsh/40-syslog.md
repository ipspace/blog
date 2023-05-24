title: Generating Syslog messages from Tclsh

Tcl policies run within the Embedded Event Manager (EEM) environment can use the **action\_syslog** command to generate logging messages. Other Tcl environments within Cisco IOS (for example, **tclsh**) do not provide a *syslog* message API to Tcl scripts. You can use the **syslog:** opaque write-only file system introduced in IOS release 12.4T in these environments to generate debugging *syslog* messages from the Tcl script.

INFO: The messages written to the **syslog:** file system have the LOG\_DEBUG priority. The priority of these messages cannot be changed.

The ability to generate logging messages from a **tclsh** script allows you to separate the script output from the debugging stream. For example, you could open two Telnet sessions to the router, execute the script in one telnet session and monitor the debugging printouts in the second telnet session with the **terminal monitor** command. You can also use this approach to generate debugging messages from other Tcl-based subsystems (for example, Embedded Menu Manager or Embedded Syslog Manager).

To generate debugging messages from a Tcl script, use the following sequence:

```
set syslog [open "syslog: " w+]
puts $syslog "message"
close $syslog
```

If you want to generate numerous debugging messages from the same script, you could use the **flush** ***$syslog*** statement after each **puts** statement and close the ***$syslog*** channel identifier at the end of the script.

## Sample Tclsh script

The following **tclsh** script generates two debugging messages, one before it starts a **ping** command, the second one after the **ping** command has executed.

```
set syslog [open "syslog:" w+]
puts $syslog "%PING-6-starting ping"
flush $syslog
exec "ping 10.0.0.2"
puts $syslog "%PING-6-finished"
close $syslog 
```
CAPTION: Sample syslog script

The router on which the script is executed has been configured to generate date/time timestamps for regular *syslog* messages and uptime timestamps for debugging messages:

```
service timestamps debug uptime
service timestamps log datetime msec 
```
CAPTION: Timestamp configuration

When the script is executed, it generates two messages with uptime timestamps (proving that the **syslog:** file system results in debugging *syslog* messages). The second message appears after the router prompt, proving that it was indeed a *syslog* message and not a regular write to the TTY.

```
Router#tclsh syslog.tcl
00:19:30: %PING-6-starting ping
Router#
00:19:40: %PING-6-finished
```
