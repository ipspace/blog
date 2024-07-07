---
cli_tag: basics
date: 2016-10-13 08:47:00+02:00
series:
- cli
tags:
- automation
title: Network Automation RFP Requirements
url: /2016/10/network-automation-rfp-requirements/
---
After finishing the network automation part of a recent SDN workshop I told the attendees "*Vote with your wallet. If your current vendor doesn't support the network automation functionality you need, move on.*"

Not surprisingly, the next question was "*And what shall we ask for?*" Here's a short list of ideas, please add yours in comments.
<!--more-->
{{<note warn>}}The Pass/Fail information included below was collected in 2016/2017 to the best of my knowledge with extensive help from Jason Edelman, Nick Buraglio and David Barroso (THANK YOU!). If you feel the information is incorrect, please point me to public documentation that proves me wrong. Also, do provide information on other platforms.{{</note>}}

### Programmable Interface (API)

*The device MUST have an **on-device** programmable API (NETCONF or REST)* that allows an external script to:

-   Get device configuration
-   Get operational data
-   Change device configuration.

I don't want to hear about "solutions" that insert layers of kludges between my script and the device I want to manage. If I can't access the device itself using NETCONF or REST I'm no longer interested. After all, my calendar is showing 2016.

**Pass:** Most networking vendors, at least in recent software releases.

**Fail:** List your grievances in the comments ;)

### Structured Operational Data

*The device MUST return operational data as structured data (JSON or XML format) not as text printouts wrapped in XML or JSON envelopes.*

I had enough of screen scraping in the 30 years I had to deal with networking devices. I don't want to write another Expect script or TextFSM definition. My calendar is still showing 2016.

**Pass:** Junos, Nexus OS, Arista EOS, Brocade VDX, ALU/Nokia

**Fail:** Cisco IOS

**Nice try:** Cisco IOS XE with REST API (it returns a minimalistic set of operational data, see also _feature parity_ below).

{{<note info>}}The importance of structured operational data is covered in in [module 2 (Easy Wins)](http://automation.ipspace.net/Public:Description#Easy_Wins) of [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course.{{</note>}}

### Device Configuration in Structured Format

*The device SHOULD return its configuration in structured format (JSON or XML) with meaningful structure (for example, ACL lines should be **within** the ACL).*

I don't know why I should write another configuration scraping program to figure out what BGP neighbors a device has if I could do the same thing with a simple walk down the return object. I had enough [Perl Regexps](https://xkcd.com/208/) for one life.

**Pass:** Junos, ALU/Nokia, Cisco IOS XE release 16.

**Mostly there:** Cisco IOS and IOS-XE (prior to release 16).

### Atomic configuration changes

*Changes to device configuration MUST be **atomic**, more so if the device supports NETCONF -- either all the submitted changes are accepted or none is.*

I really don't care if I can get that done in a NETCONF session with **commit** capability or as a single huge REST call, but I don't want to be cut off the box once again because the box accepted only half the ACL.

**Pass:** Junos, IOS XR, Arista EOS

**Almost:** Cisco IOS XE. REST interface is atomic within a single call, as is NETCONF implementation in release 16.x which implements rollback-on-error.

**Fail:** Cisco IOS, Nexus OS

### Configuration Rollback

*The device MUST support rollback to a previous configuration.*

If I made a mistake, I want to be able to go back to a previous configuration without spending hours hand-crafting the differences between the mess I made and the configuration that worked before I started messing it up.

**Pass:** Junos, IOS XR, Arista EOS, Cisco IOS, Nexus OS, ALU/Nokia

### Configuration Replace

*The device MUST support replacing current configuration with a new configuration without a reload.*

Sometimes I really don't want to waste my time calculating the differences that have to be made to get the device to do what I want, particularly when I create the whole configuration with a template.

**Pass:** Junos, IOS XR, Arista EOS, Cisco IOS/XE, Nexus OS

{{<note info>}}The importance of *configuration replace* functionality is the focus of [module 4 (Changing Network Configuration or State)](http://automation.ipspace.net/Public:Description#Changing_Network_Configurations_or_State) of [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course.{{</note>}}

### Configuration diff

*The device SHOULD be able to create a list of configuration commands needed to transform one configuration into another.*

It's great if you can point out the differences between two configurations to the engineer who has to approve the change. Oh, and I'm looking for the list of commands to get from A to B. I can run a **diff** on Linux myself.

**Pass:** Junos, Cisco IOS

**Fail:** Most everyone else. Many platforms use standard Linux **diff** instead of considering configuration context.

{{<note info>}}For example, if I change BGP AS number, I'd like to see **no router bgp A** followed by **router bgp B** followed by whole BGP configuration.{{</note>}}

### Support for Industry-Standard Models

*The device SHOULD support industry-standard configuration data models (IETF and/or OpenConfig).*

We waited long enough to get them. I don't want to wait another decade for the vendors to implement them.

**Pass:** Junos, Arista EOS (OpenConfig), Nexus OS (OpenConfig), IOS XE (IETF), IOS XR (OpenConfig)

**Warning:** While most vendors support some industry standard, always [check out](https://github.com/ctopher78/network-automation-course/tree/master/Homework3) what can be [configured through the standard models](/2018/01/use-yang-data-models-to-configure/).

{{<note info>}}The benefits of industry-standard data models are described in [module 3 (Data Models)](http://automation.ipspace.net/Public:Description#Data_Models) of [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course.{{</note>}}

### Feature Parity

Paraphrasing [Ron Broersma](/2016/07/cutting-through-ipv6-requirements-red/): *All functionality requested in the RFP must be fully supported by the device API and meet the above requirements*.

### Anything Else?

I probably forgot a few critical requirements. Please list them in the comments.

### Want to Know More?

Check out the [network automation webinars](http://www.ipspace.net/Roadmap/Network_Automation_webinars) and the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.

### Revision History

2023-03-12
: Removed all references to Brocade VDX which has been obsolete for years.
