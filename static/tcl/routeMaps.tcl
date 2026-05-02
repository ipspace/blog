#
# Copyright (c) 2008 NIL Data Communications
# All rights reserved.
#
# by:       Ivan Pepelnjak, NIL Data Communications
# title:    Displays configured route-maps (optionally with descriptions)
# name:     routeMaps.tcl
# desc:     This script displays route-maps configured on the router, optionally with
#           their description
#
# ios config:
#
#           * download the file into flash:routeMaps.tcl
#           * configure alias exec routemaps tclsh flash:routeMaps.tcl
#
#           invoke with routemaps or routemaps -d
#

if { ! [string equal $tcl_platform(os) "Cisco IOS"] } {
  proc exec {fileName} {
    regsub -all {[|:\\]} $fileName {} fileName
    regsub -all {  } $fileName { } fileName
    set srcFile [open "$fileName.txt" "r"]
    set data [read $srcFile]
    close $srcFile
    return $data
  }
}

proc routemapSimple {} {
  foreach line [split [exec "show route-map"] "\n"] {
    if {[regexp -nocase {^route-map (\w+)} $line ignore rmap]} {
      set rmNames($rmap) "*"
    }
  }
  foreach rmap [lsort [array names rmNames]] {
    puts $rmap
  }
}

proc printInterface {dataName} {
  upvar $dataName data
  global lineFormat
  global paramActive
  if {! [array exists data]} { return }
  if {$paramActive != 0} { if {[string equal $data(IPADDR) "no address"]} { return } }
  puts [format $lineFormat $data(IFNAME) $data(IPADDR) $data(IPMASK) $data(IPMTU) $data(IFSTAT)]
}

proc routemapWithDescription {} {
  set lineFormat "%-20s %-50s"
  puts [format $lineFormat {Route map name} {Description}]
  puts "========================================================================"
  foreach line [split [exec "show running | section ^route-map"] "\n"] {
    if {[regexp -nocase {^route-map (\w+)} $line ignore rmap]} {
      if {![info exists rmNames($rmap)]} { set rmNames($rmap) {} }
    } elseif {[regexp -nocase {^\s+description (.*)$} $line ignore rdesc]} {
      if {[string length $rmNames($rmap)] == 0} { 
        regsub -all {\n|\r} $rdesc {} rdesc
        set rmNames($rmap) $rdesc 
      }
    }
  }
  foreach rmap [lsort [array names rmNames]] {
    puts [format $lineFormat $rmap $rmNames($rmap)]
  }
}

set description [string equal [lindex $argv 0] "-d"]
if { $description != 0 } then { routemapWithDescription } else { routemapSimple }