---
url: /2007/03/running-tcl-procedures-from-command.html
title: "Running Tcl Procedures from Cisco IOS CLI"
date: "2007-03-19T08:12:00.001+01:00"
tags: [ Tcl,command line interface ]
---

Starting in IOS release 12.3(2)T, [Tcl shell is accessible from the command line interface](http://www.cisco.com/en/US/products/sw/iosswrel/ps5207/products_feature_guide09186a00801a75a7.html#wp1048060) with the **tclsh** command. After entering this command, you get the **Router(tcl)\#** prompt and can enter individual Tcl commands (the help is confusing, though -- you get help on exec-mode commands, but none of them work).  
<!--more-->
What the documentation fails to tell you, though, is that you can specify a file name (actually an IFS URL) as the parameter to the **tclsh** command to execute the Tcl commands in that file. The file can be local (stored in flash or [even NVRAM](https://blog.ipspace.net/2007/02/store-your-eem-tcl-policies-in-nvram.html)) or remote, in which case the router downloads the file and executes it. For example, if you store a simple helloWorld.tcl file ...

```
puts "hello world";
```

... on an external TFTP server and execute it with the tclsh tftp://10.0.0.10/helloWorld.tcl command, you'll get the "famous" printout:

```
Router#tclsh tftp://10.0.0.10/helloWorld.tcl
Loading helloWorld.tcl from 10.0.0.10 (via FastEthernet0/0): !
[OK - 20 bytes]
hello, world
```

{{<jump>}}[Keep reading](https://blog.ipspace.net/kb/Tclsh/){{</jump>}}