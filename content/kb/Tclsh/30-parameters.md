---
kb_section: Tclsh
minimal_sidebar: true
title: Tclsh Command Line Parameters
url: /kb/Tclsh/30-parameters.html
---
A Tcl script executed with the **tclsh** command can receive command line parameters: all words entered after the file name in the **tclsh** command line are passed to the Tcl script in the *$argv* list.

The [Tcl list commands](http://www.tcl.tk/man/tcl8.5/tutorial/Tcl14.html) can be used to examine each individual parameter. When used in a scalar context, *$argv* returns the rest of the command line after the script name.

## Scalar context example

The following script executes the **show ip interface** command and filters the outputs to include only the relevant lines (the lines with the *address* or *protocol* keywords):

{{<cc>}}ipconfig.tcl{{</cc>}}
```
puts [exec "show ip interface $argv ¦ include address¦protocol"] 
```

You can execute the script with the **tclsh flash:ipconfig.tcl** ***interface*** command. To simplify the user interface, configure an alias.

```
alias exec ipconfig flash:ipconfig.tcl
```

After the alias is configured, you can use **ipconfig** ***interface*** command to display interface’s IP address, line protocol status, NAT status and broadcast address:

```
router#ipconfig vlan1
Vlan1 is up, line protocol is up
  Internet address is 192.168.200.193/28
  Broadcast address is 255.255.255.255
  Helper address is not set
  Network address translation is enabled, interface in domain inside
```

## List context example

The following script shuts down the specified interface:

{{<cc>}}shutdown.tcl{{</cc>}}
```
#
# ifname is set to first CLI parameter (interface name)
#
set ifname [lindex $argv 0]

if {[string equal $ifname ""]} { 
  puts "Usage: shutdown ifname"; return; 
}

if { [ catch { exec "show ip interface $ifname" } errmsg ] } {
  puts "Invalid interface $ifname, show ip interface failed"; return
}

ios_config "interface $ifname" "shutdown" 
```

The script performs the following steps:

-   Variable *ifname* is set to the value of the first command-line parameter. In most programming languages, this would be written as *argv\[0\]*, Tcl extracts values from a list with the **lindex** command.
-   If the *ifname* is empty, the script aborts and prints the usage guidelines. In a more human-oriented programming language, the test would be written as *if (ifname == “”)*. The version of Tcl running on Cisco IOS does not support string comparison operators; you have to use the **string equal** command to compare two strings.
-   The **show ip interface** ***ifname*** command is executed in a **catch** block. If the **show** command fails, the interface name is not correct and the script aborts.
-   IOS configuration commands **interface** ***ifname*** and **shutdown** are executed to disable the interface.

If you store this Tcl script into the router’s flash as *shutdown.tcl* and configure **alias exec shutdown tclsh flash:shutdown.tcl**, you can execute the command **shutdown** ***interface*** to shut down an interface without entering the router configuration mode.
