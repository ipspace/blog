---
url: /2008/01/tabular-display-of-ospf-external-routes.html
title: "Tabular Display of OSPF External Routes"
date: "2008-01-20T07:31:00.001+01:00"
tags: [ OSPF,Tcl ]
lastmod: 2020-11-17 11:46:00
---
I was testing OSPF external routes recently and wanted to have a comprehensive display of OSPF type-5 LSAs (not the too-verbose information IOS generates), so I created the following Tcl script to displays type-5 (external) LSAs from the OSPF database in a tabular format. 

Here is a sample printout from one of my lab routers:

``` code
S1#ospfExternal
 
External OSPF routes for OSPF process ID 1
 
  Prefix                Cost   Tag            ASBR Forward addr
==================================================================
> 10.1.0.1/32          10 E1     1        10.0.0.3
  10.1.0.1/32        2000 E1     1       10.0.0.11
> 10.1.0.2/32           5 E2     2        10.0.0.3
  10.1.0.2/32         200 E2     2       10.0.0.11
```
<!--more-->
### Installation instructions
* download the file into flash:ospfExternals.tcl
* configure **alias exec ospfExternal tclsh flash:ospfExternals.tcl**
* invoke with **ospfExternal**

### Tcl script
```
proc printLSA {dataName} {
  upvar $dataName data
  global lineFormat
  if {! [array exists data]} { return }
  if {! [info exists data(ID)]} { return }

  if {! [info exists data(TAG)]} { set data(TAG) {} }
  if {! [info exists data(FWADDR)]} { set data(FWADDR) {} }

  puts [format $lineFormat $data(USED) $data(ID) $data(METRIC) $data(TAG) $data(ASBR) $data(FWADDR)]
  array unset data
  set data(USED) {}
}

proc printDB {pid} {
  global lineFormat
  set lineFormat "%1s %-15s %10s %5s %15s %-15s"
  set cmdtext [exec "show ip ospf $pid database external"]
  if { ! [regexp -nocase {LS age} $cmdtext] } { return }

  puts "\nExternal OSPF routes for OSPF process ID $pid\n"
  puts [format $lineFormat {} {Prefix} {Cost} {Tag} {ASBR} {Forward addr}]
  puts "=================================================================="
  foreach line [split $cmdtext "\n"] {
    if {[regexp -nocase {LS Age|Routing Bit Set} $line ignore]} { 
      printLSA lsa }
    if {[regexp -nocase {Routing Bit Set on this LSA} $line ignore]} {
      set lsa(USED) {>}
    } elseif {[regexp -nocase {Link State ID: ([0-9.]+)} $line ignore id]} {
      set lsa(ID) $id
      set lsa(FWADDR) {}
    } elseif {[regexp -nocase {Advertising Router: ([0-9.]+)} $line ignore asbr]} {
      set lsa(ASBR) $asbr
    } elseif {[regexp -nocase {Network Mask: (/[0-9]+)} $line ignore mask]} {
      append lsa(ID) $mask
    } elseif {[regexp -nocase {Metric Type: ([0-9]+)} $line ignore type]} {
      set lsa(METRIC) "E$type"
    } elseif {[regexp -nocase {Metric: ([0-9]+)} $line ignore metric]} {
      set lsa(METRIC) [concat $metric $lsa(METRIC)]
    } elseif {[regexp -nocase {Forward Address: ([0-9.]+)} $line ignore fwaddr]} {
      if {$fwaddr != "0.0.0.0"} { set lsa(FWADDR) "$fwaddr" }
    } elseif {[regexp -nocase {External Route Tag: ([0-9]+)} $line ignore tag]} {
      set lsa(TAG) $tag
    }
  }
  printLSA lsa
}

set ospfProc [exec "show ip protocols summary"]
foreach line [split $ospfProc "\n"] {
  if {[regexp -nocase {ospf ([0-9]+)} $line ignore id] } { printDB $id }
}
```