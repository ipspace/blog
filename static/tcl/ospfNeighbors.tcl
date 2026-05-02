#
# Copyright (c) 2007 NIL Data Communications
# All rights reserved.
#
# by:       Ivan Pepelnjak, NIL Data Communications
# title:    Display OSPF neighbors
# name:     ospfNeighbors.tcl
# desc:     This script displays OSPF neighbors, including OSPF area, sorted by process ID
#
# ios config:
#
#           * download the file into flash:ospfNeighbors.tcl
#           * configure alias exec ospfNeighbors tclsh flash:ospfNeighbors.tcl
#
#           invoke with ospfNeighbors
#

proc printNeighbor {dataName} {
  upvar $dataName data
  global lineFormat
  if {! [array exists data]} { return }
  puts [format $lineFormat $data(ID) $data(AREA) $data(STATE) $data(IFADDR) $data(IFNAME)]
}

proc printProcess {pid} {
  global lineFormat
  set lineFormat "%-15s %-15s %-10s %-15s %s"
  set cmdtext [exec "show ip ospf $pid neighbor detail"]
  if { $cmdtext == "" } { return }

  puts "\nOSPF neighbors for process ID $pid\n"
  puts [format $lineFormat {Router ID} {Area} {State} {Address} {Interface}]
  foreach line [split $cmdtext "\n"] {
    if {[regexp -nocase {neighbor ([0-9.]+).*interface address ([0-9.]+)} $line ignore id ifaddr]} {
      printNeighbor neighbor
      set neighbor(ID) $id
      set neighbor(IFADDR) $ifaddr
    } elseif {[regexp -nocase {area ([0-9.]+).*interface (\S+)} $line ignore area ifname]} {
      set neighbor(AREA) $area
      set neighbor(IFNAME) $ifname
    } elseif {[regexp -nocase {state is (\w+)} $line ignore state]} {
      set neighbor(STATE) $state
    } elseif {[regexp -nocase {DR is ([0-9.]+).*BDR is ([0-9.]+)} $line ignore dr bdr]} {
      if {[string equal $dr $neighbor(IFADDR)]} {set neighbor(STATE) "$neighbor(STATE)/DR" }
      if {[string equal $bdr $neighbor(IFADDR)]} {set neighbor(STATE) "$neighbor(STATE)/BDR" }
    }
  }
  if {[array exists neighbor]} { printNeighbor neighbor }
}

set ospfProc [exec "show ip protocols summary | include ospf"]
foreach line [split $ospfProc "\n"] {
  if {[regexp -nocase {ospf ([0-9]+)} $line ignore id] } { printProcess $id }
}