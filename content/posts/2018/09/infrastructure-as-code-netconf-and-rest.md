---
date: 2018-09-19 08:18:00+02:00
tags:
- automation
- AWS
title: Infrastructure-as-Code, NETCONF and REST API
url: /2018/09/infrastructure-as-code-netconf-and-rest/
series: [ niac ]
niac_tag: rest
---
*This is the* *third* *blog post in "thinking out loud while preparing Network Infrastructure as Code presentation for the *[*network automation course*](https://www.ipspace.net/Building_Network_Automation_Solutions?utm_source=blog)*" series.* *You might want to start with* [*Network-Infrastructure-as-Code Is Nothing New*](/2018/09/network-infrastructure-as-code-is/) *and* [*Adjusting System State*](/2018/09/adjusting-system-state-with/) *blog posts.*

As I described in the previous blog post, the hardest problem any infrastructure-as-code (IaC) tool must solve is "*how to adjust current system state to desired state described in state definition file(s)*"... preferably without restarting or rebuilding the system.

There are two approaches to adjusting system state:
<!--more-->
-   **Data model** based approach: overall system state is described as a data model that can be read and manipulated with API calls. NETCONF is often used to manipulate data model of networking devices.
-   **CRUD** (Create, Read, Update, Delete) approach where API provides a gazillion calls to list, read, and manipulate individual objects. OpenStack, AWS, NSX, ACI... are typical examples of this approach.

### Replacing a Data Model

Implementing IaC for devices that allow you to **replace system state** is trivial (see [previous blog post](/2018/09/network-infrastructure-as-code-is/)), although one might get into interesting challenges when dealing with devices where system state is described in arcane domain-specific language (example: Cisco IOS configuration) instead of easy-to-parse data structures (like XML or JSON).

Even if your tool doesn't generate full system state that can be used as a replacement for existing state it can:

-   Read system state;
-   Adjust the resulting data structure based on desired (sub)state of the system;
-   Replace system state.

### Adjusting System State Data Model

Adjusting system state for devices that use a data model based approach but don't support an equivalent of **configure replace** functionality is reasonable easy *assuming we're dealing with data structures*:

-   Read system state;
-   Compare current state with desired state -- keep in mind that we're dealing with data structures, and implementing a recursive data structure diff is a simple programming exercise;
-   Tell the device to implement the differences between current and desired state.

Obviously this approach only works if the device is able to (A) generate current state as a data structure and (B) accept differences as a data structure and implement them.

Even if you have to deal with devices that use arcane data manipulation languages (DML) like Cisco IOS configuration syntax you can use tools like (now long gone) [napalm-yang](/2017/05/start-using-openconfig-with-napalm-on/) that parse the configuration into a data model, create a difference between two data models, and transform the differences back into configuration commands.

### The CRUD Hell{#crud-hell}

The worst API model you might have to deal with when implementing infrastructure-as-code is the CRUD approach: device (or system) API has calls to list, inspect, and manipulate individual objects. Using a CRUD API an infrastructure-as-code tool has to:

-   List existing objects;
-   Inspect the state of existing objects;
-   Figure out which objects to delete, modify, or create based on the desired final state of the system;
-   Perform create/delete/modify operations in just the right order based on inter-object dependencies. For example, you cannot attach a VM to a virtual network before the virtual network is created.

Does this remind you of the way we were configuring network devices in the past... executing carefully orchestrated dance of configuration commands (now API calls) to get from where we were to where we wanted to be? One has to wonder why some people prefer to call this *progress* and why they're so [obsessed with REST API](/2018/04/dont-get-obsessed-with-rest-api/).

Finally, let me mention that most orchestration systems, cloud management systems, SDN controllers and intent-based networking products I've seen use this approach. Go figure.

### More Information

We talked about [network infrastructure-as-code](https://my.ipspace.net/bin/list?id=AutConcepts#NIAC) in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.

