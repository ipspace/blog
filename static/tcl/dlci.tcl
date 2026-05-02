#
# Copyright (c) 2007 NIL Data Communications
# All rights reserved.
#
# by:       Ivan Pepelnjak, NIL Data Communications
# title:    Display DLCIs in tabular format
# name:     dlci.tcl
# desc:     This script displays all DLCIs on a router in a tabular format
#           grouped by WAN interfaces
#
# ios config:
#
#           * download the file into flash:dlci.tcl
#           alias exec dlci tclsh flash:dlci.tcl
#
#           invoke with dlci
#
set lineFormat "%4s %-10s %-10s %s"
set text [exec "show frame-relay pvc"]
foreach line [split $text "\n"] {
  if {[regexp {PVC Statistics for interface\s+(\S+)} $line ignore ifname]} {
    set dce [if {[regexp {DCE} $line]} {set dce " (DCE)"}]
    puts ""
    puts "Interface $ifname$dce"
    puts ""
    puts [format $lineFormat "DLCI" "Status" "Usage" "Interface"]
    puts "============================================="
  }
  if {[regexp {DLCI = ([0-9.]+).*USAGE = (\w+).*STATUS = (\w+).*INTERFACE = (\S*)} $line ignore dlci usage status subif]} {
    if {[string equal -nocase $ifname $subif]} { set subif "" }
    puts [format $lineFormat $dlci $status $usage $subif]
  }
}