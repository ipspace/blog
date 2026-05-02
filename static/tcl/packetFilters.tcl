#
# Copyright (c) 2007 NIL Data Communications
# All rights reserved.
#
# by:       Ivan Pepelnjak, NIL Data Communications
# title:    Display packet filters applied to interfaces
# name:     packetFilters.tcl
# desc:     This script displays input and output IP packet filters applied to interfaces
#
# ios config:
#
#           * download the file into flash:packetFilters.tcl
#           * configure alias exec filters tclsh flash:packetFilters.tcl
#
#           invoke with filters
#

proc displayExec {result} {
  set first 0
  foreach line [split $result "\n"] {
    regsub {\s+$} $line "" line
    if {$line != "" || $first != 0} { puts $line; incr first; }
  }
}

proc printInterface {dataName} {
  upvar $dataName data
  global lineFormat
  global full
  global verbose
  if {! [array exists data]} { return }
  if {$data(INACL) == "" && $data(OUTACL) == "" && $full == 0 } { return; }
  if {$verbose == 0} {
    puts [format $lineFormat $data(IFNAME) $data(INACL) $data(OUTACL) ]; return; }
  puts ""
  puts $data(IFNAME)
  puts "===================="
  if {$data(INACL) != ""} {
    puts -nonewline "in: "; displayExec [exec "show ip access-list $data(INACL)"] }
  if {$data(OUTACL) != ""} {
    if {$data(INACL) != ""} { puts "" }
    puts -nonewline "out:"; displayExec [exec "show ip access-list $data(OUTACL)"] }
}

set verbose 0
set full    0

switch [lindex $argv 0] {
  all     { set full 1 }
  verbose { set verbose 1 }
  {}      { }
  default { puts {Syntax: tclsh packetFilters.tcl [all|verbose]}; return; }
}

set lineFormat "%-20s %15s %15s"
if { $verbose == 0 } {
  puts [format $lineFormat {Interface} {Inbound} {Outbound}]
  puts "========================================================="
} else { set full 0 }

set cmdtext [exec {show ip interface}]
foreach line [split $cmdtext "\n"] {
  if {[regexp -nocase {^(\S+)} $line ignore ifname]} {
    printInterface ifdata
    set ifdata(IFNAME) $ifname
    set ifdata(INACL)  ""
    set ifdata(OUTACL) ""
  } elseif {[regexp -nocase {Outgoing access list is (.*)} $line ignore acl]} {
    regsub {\s+$} $acl "" acl
    if { $acl == "not set" } { set acl "" }
    set ifdata(OUTACL) $acl
  } elseif {[regexp -nocase {Inbound  access list is (.*)} $line ignore acl]} {
    regsub {\s+$} $acl "" acl
    if { $acl == "not set" } { set acl "" }
    set ifdata(INACL) $acl
  } 
}
if {[array exists ifdata]} { printInterface ifdata }
