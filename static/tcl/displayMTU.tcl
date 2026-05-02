#
# Copyright (c) 2007 NIL Data Communications
# All rights reserved.
#
# by:       Ivan Pepelnjak, NIL Data Communications
# title:    Displays hardware, IP and MPLS interface MTU
# name:     displayMTU.tcl
# desc:     This script displays the current values of the hardware, IP and MPLS MTU for
#           all router's interfaces
#
# ios config:
#
#           * download the file into flash:displayMTU.tcl
#           * configure alias exec mtu tclsh flash:displayMTU.tcl
#
#           invoke with mtu [mpls|ip]
#

proc displayExec {result} {
  set first 0
  foreach line [split $result "\n"] {
    regsub {\s+$} $line "" line
    if {$line != "" || $first != 0} { puts $line; incr first; }
  }
}

set disp_ip   0
set disp_mpls 0

switch [lindex $argv 0] {
  ip   { set disp_ip 1 }
  mpls { set disp_mpls 1 }
  {}      { }
  default { puts {Syntax: tclsh displayMTU.tcl [ip|mpls]}; return; }
}

set lineFormat "%-20s %8s %6s %6s"
puts [format $lineFormat {Interface} {Hardware} {IP} {MPLS}]
puts "========================================================="

set nullidx {Null 0}
set ipmtu($nullidx) 1500
set mplsmtu($nullidx) 1500

set ifList {}
set showIF [exec {show interface}]
foreach line [split $showIF "\n"] {
  if {[regexp -nocase {^(\S+)} $line ignore ifname]} {
    set currentInterface $ifname
    set ipmtu($ifname) ""
    set mplsmtu($ifname) ""
  } elseif {[regexp -nocase {MTU (\d+)} $line ignore mtu]} {
    set hwmtu($currentInterface) $mtu
    lappend ifList $currentInterface
  }
}

set showIP [exec {show ip interface}]
foreach line [split $showIP "\n"] {
  if {[regexp -nocase {^(\S+)} $line ignore ifname]} {
    set currentInterface $ifname
  } elseif {[regexp -nocase {MTU is (\d+)} $line ignore mtu]} {
    set ipmtu($ifname) $mtu
  } 
}

foreach line [split [exec {show mpls interfaces detail}] "\n"] {
  if {[regexp -nocase {^Interface (\S+):} $line ignore ifname]} {
    set currentInterface $ifname
  } elseif {[regexp -nocase {MTU = (\d+)} $line ignore mtu]} {
    set mplsmtu($currentInterface) $mtu
  } 
}

foreach currentInterface $ifList {
  set display 1
  if { $disp_ip == 1 && $ipmtu($currentInterface) == "" } { set display 0 }
  if { $disp_mpls == 1 && $mplsmtu($currentInterface) == "" } { set display 0 }
  if { $display == 1 } { 
    puts [format $lineFormat $currentInterface $hwmtu($currentInterface) $ipmtu($currentInterface) $mplsmtu($currentInterface)]
  }
} 
