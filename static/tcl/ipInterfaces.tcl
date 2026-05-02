#
# Copyright (c) 2007 NIL Data Communications
# All rights reserved.
#
# by:       Ivan Pepelnjak, NIL Data Communications
# title:    Display IP interface parameters in tabular format
# name:     ipInterfaces.tcl
# desc:     This script displays IP address, subnet mask and IP MTU size in a tabular format
# history:  Version 2. Fixed the IP address format issues (see ip netmask-format).
#
# ios config:
#
#           * download the file into flash:ipInterfaces.tcl
#           * configure alias exec ipconfig tclsh flash:ipInterfaces.tcl
#
#           invoke with ipconfig [active|configured|address]
#

proc printInterface {dataName} {
  upvar $dataName data
  global lineFormat paramActive paramConfig
  if {! [array exists data]} { return }
  if {$paramActive != 0} { if {! [string equal $data(IFSTAT) "up"]} { return } }
  if {$paramConfig != 0} { if {[string equal $data(IPADDR) "no address"]} { return } }

  puts [format $lineFormat $data(IFNAME) $data(IPADDR) $data(IPMTU) $data(IFSTAT)]
}

proc usage {} { puts {Syntax: ipconfig [active|configured|address]} }

proc parseParams {} {
  global paramActive paramConfig paramAddress argv

  set paramActive  0
  set paramConfig  0
  set paramAddress 0

  foreach par $argv {
    switch $par {
      active     { set paramActive 1 }
      configured { set paramConfig 1 }
      address    { set paramAddress 1 }
      help       { usage; return 1; }
      default    { usage; return 1; }
    }
  }
  return 0;
}

if {[parseParams] == 1} {return}
set lineFormat "%-20s %-20s %5s %s"
puts [format $lineFormat {Interface} {IP Address} {MTU} {State}]
puts "=============================================================="
exec {terminal ip netmask-format bit-count}
set cmdtext [exec {show ip interface}]
##set paramActive [string equal [lindex $argv 0] "active"]

foreach line [split $cmdtext "\n"] {
  if {[regexp -nocase {^(\S+) is (.*), line protocol is (\S+)} $line ignore ifname ifstat iflstat]} {
    printInterface ifdata
    set ifdata(IFNAME) $ifname
    set ifdata(IPADDR) "no address"
    set ifdata(IPMTU) ""
    set ifdata(IFSTAT) $ifstat
    if {[string equal $ifstat "up"]} {
      if {![string equal $iflstat "up"]} { set ifdata(IFSTAT) "$ifstat/$iflstat" }
    }
    regsub -all {administratively} $ifdata(IFSTAT) "admin" ifdata(IFSTAT)
  } elseif {[regexp -nocase {internet address is ([0-9.]+/[0-9]+)} $line ignore ipaddr]} {
    set ifdata(IPADDR) $ipaddr
  } elseif {[regexp -nocase {Using address of (\S+)\s+\(([0-9.]+)\)} $line ignore ipif ipaddr]} {
    set ifdata(IPADDR) $ipif
    if {$paramAddress != 0} { set ifdata(IPADDR) "$ipaddr (U)" }
  } elseif {[regexp -nocase {MTU is ([0-9]+)} $line ignore ipmtu]} {
    set ifdata(IPMTU) $ipmtu
  }
}
if {[array exists ifdata]} { printInterface ifdata }
exec {terminal no ip netmask-format bit-count}
