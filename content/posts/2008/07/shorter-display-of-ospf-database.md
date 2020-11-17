---
date: 2008-07-14T07:24:00.004+02:00
tags:
- OSPF
- Tcl
- command line interface
- show filters
title: Shorter Display of OSPF Database
url: /2008/07/shorter-display-of-ospf-database.html
lastmod: 2020-11-17 11:34:00
---
Recently I had to explore the behavior of Cisco IOS OSPF implementation and had to inspect OSPF database on routers in various areas. 

If you're only interested in the contents of the database (not in low-level troubleshooting), variety of LSA fields (including LS Age, Options, Checksum, Length ...) are just cluttering the printout, so I fine-tuned the show filter to exclude all the non-relevant fields, ending with **show ip ospf database *parameters* | exclude LS|Options|Check|Len|(MTID:\[ 0-9\]+$)** (the MTID field appears in IOS release 12.2SRC).

To make the command more useful, I've changed it into a short Tcl script:
<!--more-->
1. Store the following code into *flash:ospfdb.tcl*

```
set cmd {show ip ospf database }
append cmd $argv
append cmd { | excl LS|Options|Check|Len|(MTID:[ 0-9]+$)}
puts [exec $cmd]
```

2. Define **alias exec ospfdb flash:ospfdb.tcl**.

3. Enjoy. I could then easily inspect the contents of various parts of OSPF database I was interested in, for example:  

```
a3#ospfdb external 0.0.0.0
 
            OSPF Router with ID (10.0.1.3) (Process ID 1)
 
                Type-5 AS External Link States
 
  Link State ID: 0.0.0.0 (External Network Number )
  Advertising Router: 10.0.1.5
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        Metric: 1 
        Forward Address: 0.0.0.0
        External Route Tag: 1
```
