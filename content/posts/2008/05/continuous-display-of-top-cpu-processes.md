---
url: /2008/05/continuous-display-of-top-cpu-processes/
title: "Continuous display of top CPU processes"
date: "2008-05-26T07:35:00.003+02:00"
tags: [ Tcl ]
lastmod: 2020-11-17 11:16:00
---

When you have to monitor which processes consume router's CPU over a period of time, a Tcl script that emulates the Unix **top** command</a> might come handy. The following Tcl script continuously displays top 20 Cisco IOS processes and refreshes the update every 5 seconds.

{{<ct3_rescue>}}

### Installation

-   Download the source file into *flash:top.tcl*.
-   Configure **alias exec top tclsh flash:top.tcl**.
-   Invoke with **top**.

### Usage guidelines

Usage: **top \[ 5sec | 1min | 5min \]**

The script changes the escape character to Ctrl/C. Use **terminal escape default** to restore default settings

{{<note>}}If anyone discovered a reliable technique that detects a keypress event (= character available on *stdin*) in the Tcl loop, please let me know. The Ctrl/C solution is a kludge.{{</note>}}

### Source code

```
#
# title:    Emulate the Unix top command
# name:     top.tcl
# desc:     The script displays top CPU processes every 5 seconds
#
# ios config:
#
#           * download the file into flash:top.tcl
#           * configure alias exec top tclsh flash:top.tcl
#
#           invoke with top [5sec|1min|5min]
#

set IOS [string equal $tcl_platform(os) "Cisco IOS"];

if { $IOS } { 
  exec "terminal international"; 
  exec "terminal escape 3";
}

set arg [lindex $argv 0];
if { [string length $arg] == 0 } { set arg "5sec" } ;
if { [lsearch -exact { 5sec 1min 5min } $arg] < 0 } {
  puts {Usage: top [5sec|1min|5min]};
  return 0;
}

fconfigure stdout -buffering none;

while {1} {
  set lines [split [exec "show process cpu sorted $arg | exclude 0.00% +0.00% +0.00%"] "\n"];

  puts -nonewline "\033\[2J\033\[H";
  for { set lc 1 } { $lc < 23 } { incr lc } {
    set curline [lindex $lines $lc];
    if { [string length $curline] > 0 } { puts "$curline"; }
  }
  puts -nonewline "\nBreak with Ctrl/C --> ";
  after 5000;
}
```

