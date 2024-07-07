---
date: 2008-03-10T07:39:00.004+01:00
tags:
- Tcl
- command line interface
- show filters
title: Display the names of the configured route-maps
url: /2008/03/display-names-of-configured-route-maps/
---
I'm probably getting old … I keep forgetting the exact names (and capitalization) of route-maps I've configured on the router. The **show route-maps** command is way too verbose when I'm simply looking for the exact name of the **route-map** I want to use, so I wrote a Tcl script that displays the names of the **route-maps** configured on the router. If you add a **-d** switch, it also displays their descriptions (to be more precise, the first description configured in the **route-map**).
<!--more-->
{{<note>}}When using the **-d** switch, the script executes the **show running** command and might take a while to complete.{{</note>}}

To use the script, download the [routeMaps.tcl](http://www.zaplana.net/Articles/index.asp?view=tcl/routeMaps.tcl) file (available from [my web site](http://www.zaplana.net/Articles/index.asp?a=tcl)) into the router's flash and follow the [installation instructions in the source](http://www.zaplana.net/Articles/index.asp?view=tcl/storeFile.tcl).

Here is a sample printout from one of my routers:

```
R1#show alias | include rm

  rm                    tclsh flash:routeMaps.tcl
R1#rm
LocPref
SetCommunity
TestRange
prepend
 
R1#rm -d
Route map name       Description
========================================================================
LocPref
SetCommunity         Sets time-based communities on local routes
TestRange
prepend
```
