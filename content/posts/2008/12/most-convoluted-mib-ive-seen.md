---
url: /2008/12/most-convoluted-mib-ive-seen/
title: "The most convoluted MIB I’ve seen"
date: "2008-12-10T10:12:00.002+01:00"
tags: [ network management,Tcl,QoS ]
lastmod: 2020-11-17 11:51:00
---
Jared Valentine sent me a really interesting problem: he would like to [detect voice traffic and start shaping TCP traffic for the duration of the voice call](http://www.xmission.com/~hidden/aatqos/). The ideal solution would be an EEM applet reacting to the changes in the CISCO-CLASS-BASED-QOS-MIB; one of its tables contains the amount of traffic for each class configured in a service policy.

The MIB navigation looks simple: you just read the values from the `cbQosClassMapStats` table, indexed by policy ID and class ID. The real problem is finding the correct index values. I could walk the MIB manually with a MIB browser or **snmp\_getnext** TCL calls, but this approach is obviously not scalable, so I wrote a script that walks through the `cbQosServicePolicy`, `cbQosObjects`, `cbQosPolicyMapCfg` and `cbQosClassMapCfg` tables and prints the index values you need.

{{<ct3_rescue>}}

This script traverses the Class-based QoS MIB and displays service policies and classes attached to individual interfaces. The policy index and class index values are printed next to the policy/class name to help the operator fetch the desired SNMP variable from the statistics tables of the CISCO-CLASS-BASED-QOS-MIB.

### Installation

-   Download the source file into *flash:cbindex.tcl*
-   Configure **alias exec cbindex tclsh** ***flash:cbindex.tcl***
-   Configure persistent CBQoS indexes with the **snmp mib persist cbqos** (otherwise the indexes will change after the router reload).

### Usage guidelines

Usage: **cbindex** ***community***

Command line parameters:

-   **Community**: SNMP community with R/O access to the CISCO-CLASS-BASED-QOS-MIB

## Source code

```
#
# title:    Displays MQC class map indexes
# name:     cbindex.tcl
# desc:     The script traverses the Class-based QoS MIB and
#           displays service policies and classes attached to 
#           individual interfaces. The policy index and class
#           index values are printed next to the policy/class
#           name to help the operator fetch the desired SNMP 
#           variable from the statistics tables of the 
#           CISCO-CLASS-BASED-QOS-MIB.
#

proc snmpInit { oid } {
  global snmpCommunity
  set getResult [ snmp_getnext $snmpCommunity $oid ]
  if { [ regexp {snmp error} $getResult ] } { 
    puts "SNMP calls with community $snmpCommunity fail"; return 0 
  }
  if { [ regexp {oid='(.*)'} $getResult ignore nxtoid ] } {
    if { [string first $oid $nxtoid] == 0 } { return 1 }
  }
  puts "MIB $oid not implemented in this IOS release"; return 0;
}
  
proc snmpGet { oid result } {
  global snmpCommunity
  upvar $result r
  if { [info exists r] } { unset r }

  set getResult [ snmp_getone $snmpCommunity $oid ]
  if { [ regexp {snmp error.*text='(.*)'} $getResult ignore errtxt ] } { 
    error "snmpGet - $errtxt"; return 0 
  }
  if { [ regexp {oid='(.*)'.*val='(.*)'} $getResult ignore oid result ] } {
    if { ! [ string equal $result "NO_SUCH_INSTANCE_EXCEPTION" ] } {
      set r(OID) $oid ;
      set r(VALUE) $result ; 
      return 1;
    }
  }
  return 0;
}

proc snmpGetNext { oid result } {
  global snmpCommunity
  upvar $result r
  if { [info exists r] } { unset r }

  set getResult [ snmp_getnext $snmpCommunity $oid ]
  if { [ regexp {snmp error.*text='(.*)'} $getResult ignore errtxt ] } { 
    error "snmpGet - $errtxt"; return 0 
  }
  if { [ regexp {oid='(.*)'.*val='(.*)'} $getResult ignore oid result ] } {
    if { ! [ string equal $result "NO_SUCH_INSTANCE_EXCEPTION" ] } {
      set r(OID) $oid ;
      set r(VALUE) $result ;
      set oidSplit [ split $oid "." ]
      set r(NAME)  [ lindex $oidSplit 0 ]
      set r(INDEX) [ lreplace $oidSplit 0 0 ]
      set r(IDXLIST) [ join $r(INDEX) "." ]
      return 1;
    }
  }
  return 0;
}

proc snmpGetInTable { oid result { parentoid "" }} {
  global snmpCommunity
  upvar $result r

  snmpGetNext $oid r
  if { ! [info exists r(OID)] } { return 0 }
  if { [string equal $parentoid ""] } {
    set oidSplit [ split $oid "." ]
    set parentoid [lindex $oidSplit 0]
  }
  if { [string first $parentoid $r(OID)] != 0 } { return 0 }
  return 1;
}

proc printQosClassIndex {} {
  global snmpCommunity
  set oid "cbQosIfIndex"
  array set dirLookup { 1 in 2 out }
  set cnt 0
  while { [ snmpGetInTable $oid svcPolicy ] } {
    if { [snmpGet "ifDescr.$svcPolicy(VALUE)" ifDescr] } {
      snmpGet "cbQosPolicyDirection.$svcPolicy(INDEX)" svcDirection
      snmpGetNext "cbQosConfigIndex.$svcPolicy(INDEX)" policyObject
      snmpGet "cbQosPolicyMapName.$policyObject(VALUE)" policyName
      puts "\n$ifDescr(VALUE) ($dirLookup($svcDirection(VALUE))): $policyName(VALUE) ($svcPolicy(INDEX))"
      set coid "cbQosObjectsType.$svcPolicy(INDEX)"
      set parentoid $coid
      while { [ snmpGetInTable $coid svcClass $parentoid ] } {
        if { $svcClass(VALUE) == 2 } {
          snmpGet "cbQosConfigIndex.$svcClass(IDXLIST)" svcClassConfig
          snmpGet "cbQosCMName.$svcClassConfig(VALUE)" svcClassName
          puts "  $svcClassName(VALUE) $svcClass(IDXLIST)"
        }
        set coid $svcClass(OID)
      }
    } else { error "Cannot get interface name for service policy $svcPolicy(VALUE)" }
    set oid $svcPolicy(OID)
  }
}

set snmpCommunity [lindex $argv 0]
if { [string equal $snmpCommunity ""] } { set snmpCommunity "public" }
if { ! [ snmpInit "cbQosObjectsType" ] } return
printQosClassIndex
```

## Sample usage scenario

The following QoS classes and policies have been configured on the router:

```
class-map match-all Mail
 match protocol smtp
!
class-map match-all Web
 match protocol http
!
class-map match-all SecureWeb
 match protocol secure-http
!
class-map match-any Surfing
 match class-map Web
 match class-map SecureWeb
!
class-map match-all Files
 match protocol ftp
!
policy-map Internet
 class Web
    bandwidth 128
 class SecureWeb
    priority 64
 class Mail
    bandwidth 32
!
policy-map MailOrFtp
 class Mail
  set ip precedence 0
 class Files
  set ip precedence 0
 class Surfing
    police 16000
 class class-default
   police cir 8000
     exceed-action drop 
!
interface Serial1/0
 service-policy input MailOrFtp
 service-policy output Internet
!
interface Serial1/1
 service-policy output MailOrFtp
```

The **cbindex** script reported the following SNMP indexes:

```
c7200#cbindex Test

Serial1/0 (in): MailOrFtp (48)
  Web 48.383777
  Surfing 48.1970017
  Mail 48.4297921
  Files 48.13110129
  class-default 48.14779377
  SecureWeb 48.15077857

Serial1/0 (out): Internet (50)
  Mail 50.10516033
  Web 50.14007809
  SecureWeb 50.14520625
  class-default 50.15008753

Serial1/1 (out): MailOrFtp (66)
  Web 66.383777
  Surfing 66.1584993
  Files 66.4236097
  Mail 66.11615889
  SecureWeb 66.15077857
  class-default 66.15082481
```

Based on these indexes, you could monitor the bit rate of the Web class in outbound policy configured on Serial 1/1 with SNMP variable `cbQosCMPrePolicyBitRate.66.383777`.

```
c7200#tclsh
c7200(tcl)#snmp_getone Test cbQosCMPrePolicyBitRate.66.383777
{<obj oid='cbQosCMPrePolicyBitRate.66.383777' val='0'/>}
```
