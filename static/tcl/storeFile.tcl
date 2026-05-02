#
# Copyright (c) 2008 NIL Data Communications
# All rights reserved.
#
# by:       Ivan Pepelnjak, NIL Data Communications
# title:    Copies file from STDIN to flash
# name:     storeFile.tcl
# desc:     The script copies text content from STDIN to specified file
# params:   fileName - name of the file to be written
#           force    - optional, force the overwrite
#
# ios config:
#
#           * download the file into flash:storeFile.tcl
#           * configure alias exec store tclsh flash:storeFile.tcl
#
#           * optionally configure alias for a single file
#             configure alias exec sf tclsh flash:storeFile.tcl flash:myfile.tcl force
#
#           invoke with store fileName [force]
#


set fileName [lindex $argv 0]
set force    [string equal [lindex $argv 1] "force"]

if { [file exists $fileName] == 1 && $force == 0 } {
  puts -nonewline "File $fileName exists, overwrite? "; flush stdout
  if { ! [string equal [string tolower [string index [gets stdin] 0]] "y"] } {
    puts "Aborted"; return
  }
}

fconfigure stdin -blocking 1 -buffering full
puts "Enter content for $fileName, finish with ctrl/C"
set content [read stdin]
set channel [open "$fileName" w+]
puts $channel $content
close $channel
puts "File $fileName successfully written"