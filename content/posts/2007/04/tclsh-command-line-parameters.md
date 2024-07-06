---
url: /2007/04/tclsh-command-line-parameters.html
title: "Tclsh Command Line Parameters"
date: "2007-04-09T11:27:00.001+02:00"
tags: [ Tcl,command line interface ]
---

In a previous post, I've described [how to execute a Tcl file](/2007/03/running-tcl-procedures-from-command.html) with the **tclsh** command. 

You can do even more than that: you can pass parameters to the executed file. Every word you enter after the file name in the tclsh command line is passed as a parameter to the Tcl code you execute. To get these parameters in Tcl, use Tcl commands similar to the code below:
<!--more-->
``` code
# loop.tcl: changes loopback state
#
# syntax: tclsh loop.tcl ifnum state
#
set ifnum [lindex $argv 0] # first parameter after file name
set ifstate [lindex $argv 1] # second parameter after file name
if {[string equal $ifstate ""]} {
return -code error "Syntax: loop.tcl ifnum ifstate"
}
... rest of procedure ...
```

{{<jump>}}[More details](/kb/Tclsh/30-parameters.html){{</jump>}}
