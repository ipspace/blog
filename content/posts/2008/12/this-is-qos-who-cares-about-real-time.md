---
date: 2008-12-11 06:42:00+01:00
tags:
- network management
- Tcl
- you've asked for it
- QoS
title: This is QoS; Who Cares about Real-Time Response?
url: /2008/12/this-is-qos-who-cares-about-real-time/
---
It all started with a innocuous question: can you detect voice traffic with EEM? Looks simple enough: create a QoS class-map that matches voice calls and read the `cbQosClassMapStats` table in the CISCO-CLASS-BASED-QOS-MIB. The first obstacle was finding the correct indexes, but a [Tcl script quickly solved that](/2008/12/most-convoluted-mib-ive-seen/); I was ready to create the EEM applet. The applet failed to work correctly and after lots of debugging I figured out the counters in the `cbQosClassMapStats` table [change only every 10 seconds](/2008/12/update-interval-for-ios-mib-counters/).

I couldn't believe my eyes and simply had to test other MIB variables as well. As expected, the IF-MIB (standard interface MIB) counters increase in real-time, but obviously someone had the bright idea that we need to detect changes in traffic profile only every now and then. Although I\'ve received numerous suggestions from my readers, none of them works on a Cisco 1800 or a Cisco 7200. Oh, well, Cisco developers from the days when I started working with routers would have known better...
<!--more-->
To test the MIB variable behavior I wrote a simple Tcl script to test the MIB variables (you'll find it at the bottom of the blog post).

It reads the specified MIB variable at fixed intervals and prints the values, so you can monitor the changes in the MIB variable in real-time. I started low-bandwidth UDP flood across the router and monitored the *output bytes* interface counter. As expected the counter changed in real time and accurately tracked the amount of traffic sent through the router.

``` {.code}
GW#pm ifOutOctets.3 public 10 1000          
polling ifOutOctets.3 for 10 seconds (10 iterations)

 0.000 ifOutOctets.3=42528679        
 1.000 ifOutOctets.3=42537767        
 2.000 ifOutOctets.3=42546713        
 3.000 ifOutOctets.3=42555719        
 4.000 ifOutOctets.3=42564665        
 5.000 ifOutOctets.3=42573611        
 6.000 ifOutOctets.3=42582699        
 7.000 ifOutOctets.3=42591645        
 8.000 ifOutOctets.3=42600591        
 9.000 ifOutOctets.3=42609537        
```

Then I created a simple **class-map** and **policy map** ...

``` {.code}
GW#show policy-map interface
 FastEthernet1/0 

  Service-policy output: LAN

    Class-map: Voice (match-all)
      20438 packets, 2902196 bytes
      30 second offered rate 70000 bps
      Match: access-group name Voice

    Class-map: class-default (match-any)
      41 packets, 3967 bytes
      30 second offered rate 0 bps, drop rate 0 bps
      Match: any 
```

... and monitored the pre-policy byte counter (`cbQosCMPrePolicyByte64`) for the Voice class. The value changed only once every ten seconds:

``` {.code}
GW#pm cbQosCMPrePolicyByte64.50.10767521 public 10 1000
polling cbQosCMPrePolicyByte64.50.10767521 for 10 seconds (10 iterations)

 0.000 cbQosCMPrePolicyByte64.50.10767521=0x002865366
 1.000 cbQosCMPrePolicyByte64.50.10767521=0x002865366
 2.000 cbQosCMPrePolicyByte64.50.10767521=0x002865366
 3.000 cbQosCMPrePolicyByte64.50.10767521=0x002865366
 4.000 cbQosCMPrePolicyByte64.50.10767521=0x002865366
 5.000 cbQosCMPrePolicyByte64.50.10767521=0x002865366
 6.000 cbQosCMPrePolicyByte64.50.10767521=0x00287acf8
 7.000 cbQosCMPrePolicyByte64.50.10767521=0x00287acf8
 8.000 cbQosCMPrePolicyByte64.50.10767521=0x00287acf8
 9.000 cbQosCMPrePolicyByte64.50.10767521=0x00287acf8
```

What can I say... apart from expressing my deepest disappointment :(

## Tcl Script Used in this Blog Post

The script continuously polls a MIB variable and prints the value of the specified variable at fixed intervals (default: 500 milliseconds) for the specified amount of time (default: 15 seconds). It can be used to verify whether a MIB variable is changed in real time or periodically.

### Installation

-   Download the source file into *flash:pm.tcl*.
-   Configure **alias exec pm tclsh** ***flash:pm.tcl***

### Usage guidelines

Usage: **pm variable \[ community \[ time \[ interval \] \] \]**

Command line parameters:

-   **Variable**: MIB variable to read. Symbolic names recognized by Cisco IOS can be used (for example, **ifOutOctets**). Names are case-sensitive.
-   **Community**: SNMP community used in SNMP GET requests (default: *public*)
-   **Time:** the measurement time in seconds (default: 15 seconds).
-   **Interval:** interval between MIB polls (default: 500 milliseconds).

### Source code

```
#
# author:   Ivan Pepelnjak
# title:    Poll a MIB variable
# name:     pollMib.tcl
# desc:     The script continuously polls a MIB variable and prints
#           the values at fixed intervals for the specified amount of time.
#           It can be used to verify whether a MIB variable is changed in
#           real time or periodically.
#
# ios config:
#
#           * download the file into flash:pm.tcl
#           * configure alias exec pm tclsh flash:pm.tcl
#
#           invoke with poll oid [community [time(sec) [interval(msec)]]]
#
#           unless specified otherwise, the "public" community is used
#

proc snmpGet { oid result } {
  global snmpCommunity
  upvar $result r
  if { [info exists r] } { unset r }

  set getResult [ snmp_getone $snmpCommunity $oid ]
  if { [ regexp {snmp error.*text='(.*)'} $getResult ignore errtxt ] } { 
     error "snmpGet - $errtxt"; return 0 }
  if { [ regexp {oid='(.*)'.*val='(.*)'} $getResult ignore oid result ] } {
    if { ! [ string equal $result "NO_SUCH_INSTANCE_EXCEPTION" ] } {
      set r(OID) $oid ;
      set r(VALUE) $result ; 
      return 1;
    }
  }
  return 0;
}

set oid [lindex $argv 0]
set snmpCommunity [lindex $argv 1]
set maxtime [lindex $argv 2]
set delay   [lindex $argv 3]

if { [string equal $snmpCommunity ""] } { set snmpCommunity "public" }
if { [string equal $oid ""] } { 
  puts {Usage: pollMib.tcl oid [ community [ time(sec) [ interval(msec) ]]]}
  return
}
if { [string equal $maxtime ""] } { set maxtime 15 }
if { [string equal $delay ""] } { set delay 500 }

set maxcnt [ expr { $maxtime * 1000 / $delay } ]
set cnt 0

puts "\npolling $oid for $maxtime seconds ($maxcnt iterations)\n"
while { $cnt < $maxcnt } {
  snmpGet $oid getvar
  puts [format "%6.3f %-30s" [ expr { $delay * $cnt / 1000.0 } ] "$getvar(OID)=$getvar(VALUE)"]
  incr cnt
  if { $cnt != $maxcnt } { after $delay }
}
```

