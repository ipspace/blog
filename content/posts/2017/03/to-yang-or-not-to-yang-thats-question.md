---
cicd_tag: tools
date: 2017-03-15 07:38:00+01:00
series:
- cicd
tags:
- automation
- NETCONF
title: To YANG or Not to YANG, That’s the Question
url: /2017/03/to-yang-or-not-to-yang-thats-question.html
---
Yannis sent me an interesting challenge after reading my short "[*this is how I wasted my time*](/2016/12/generating-ospf-bgp-and-mplsvpn.html)" update:

> We are very much committed in automation and use Ansible to create configuration and provision our SP and data center network. One of our principles is that we do rely solely on data available in external resources (databases and REST endpoints), and avoid fetching information/views from the network because that would create a loop.

You can almost feel a *however* coming in just a few seconds, right?
<!--more-->
> Having said that, we are assessing options on how to maintain our network topology using a descriptive manner. Could be a database using a proprietary schema, but we\'d definitely prefer a more standard way. I am not sure if YANG is suitable for this, and hence this message.

As Yannis asked my opinion on using YANG, let's focus on that challenge first.

YANG is a *data model description language* -- you can use it to [describe how your data model looks like](/2012/06/netconf-expect-on-steroids.html), for example what attributes you use to describe a router or IP subnet object.

{{<note info>}}I covered data stores, databases, and data model description languages in more details in the [*Data models*](http://automation.ipspace.net/Public:3-Data_Models) section of the [Building Network Automation Solutions online course](http://www.ipspace.net/Building_Network_Automation_Solutions).{{</note>}}

For example, looking at the [data model I used for my fabric](https://github.com/ipspace/ansible-examples/blob/master/Routing-Deployment/fabric.yml):

-   The fabric description has five attributes: *fabric, interas, asn, services* and *nodes.*
-   *Fabric* and *nodes* attributes are mandatory, *interas, asn* and *services* attributes are optional.
-   If the model has *interas* attribute, it must have *asn* attribute.
-   *Fabric* attribute is a list of dictionaries (in Python terms, you could also model it as a relational database table);
-   Each element of the *fabric* attribute must have *left, right, left_port* and *right_port* attributes. *Left_ip, right_ip* and *cost* attributes are optional.

If I had had too much time, I could have created a YANG data model describing these restrictions and used it to validate my data model. Alas, I have better things to do, and it seems there are no tools out there to do that.

{{<note info>}}I wanted to use a YANG model in the [data validation part](http://automation.ipspace.net/Public:5-Validation,_Error_Handling_and_Unit_Tests) of the [Building Network Automation Solution](http://www.ipspace.net/Building_Network_Automation_Solutions) online course, but to my great dismay couldn't find any YANG validators -- tools that would take a data structure and verify that it complies with a data model described in YANG. Kristian Larsson is way more familiar with YANG tools and quickly wrote a [blog post explaining how you can validate XML data with YANG](http://plajjan.github.io/validating-data-with-YANG/). It\'s still not what I\'d love to have (I\'d have to transform my data from YAML to XML first), but we\'re getting close.{{</note>}}

YANG is thus not the answer to the question. OpenConfig might be, depending on what data you want to handle. I know customers using OpenConfig with extensions in their automation solutions, and David Barroso is working hard to make it part of NAPALM.

If you're interested in the technical realities of OpenConfig (as opposed to marketing nirvana), listen to the [Software Gone Wild podcast with Marcel Wiget](/2017/02/openconfig-from-basics-to.html), who was also the [guest speaker](http://automation.ipspace.net/Public:Speakers) in the [Data Models](http://automation.ipspace.net/Public:3-Data_Models) part of my [network automation online course](http://www.ipspace.net/Building_Network_Automation_Solutions).
