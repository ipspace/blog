---
cli_tag: basics
date: 2014-07-01 07:04:00+02:00
series:
- cli
tags:
- SDN
title: What Is This API Thingy?
url: /2014/07/what-is-this-api-thingy.html
---
A reader sent me this question:

> I am hearing a lot about API in reference to SDN. I do not have any software or programming background but would like to understand this API in practical way. Could you help me?

**TL&DR:** API is CLI for program-to-program communication
<!--more-->
More seriously, API stands for Application Programming Interface -- a definition how programs (or clients) could use a library (or a server). Sometimes it's as easy as defining functions a program can call, the parameters those functions accept, and the acceptable values of those parameters.

For example, when a C program wants to open a file, it calls the *open* function, which accepts a file name, and the way the file should be opened (Could the program write into the file? Should the file be created if it doesn't exist?).

It seems Cisco's OnePK follows this path -- it defines a large number of functions that a Java program can call to influence Cisco IOS behavior, either on the local device (if you somehow manage to run Java on a Cisco's box) or on a device to which the Java program has previously connected using yet-another function call.

Client-server APIs usually use a request-response protocol, where the client encodes its function call into whatever protocol message, sends the message to the server, which executes the call, and returns the results of the function back to the client.

One of the most popular client-server API methods is [REST](https://blog.ipspace.net/2012/08/why-is-restful-api-better-than-snmp.html), which encodes the parameters or function results in JSON (think: JavaScript) or XML format (both of them are pretty easy to parse in a computer program) and uses HTTP(S) as the transport protocol to exchange data between the client and the server.

{{<note>}}One of the beauties of the REST API is that you can use Unix/OSX command line utilities like *curl* to execute function calls on a remote device.{{</note>}}

For example, you can use REST API to configure an Arista switch. Instead of logging into the switch and typing **show ip interface**, your network configuration program could execute the following HTTP request:

{{<figure src="/2014/07/s1600-AristaEAPI.png" caption="An example of interactive eAPI browsing (source: Arista Networks)">}}

{{<note info>}}Junos had similar functionality for years, but it's not as easily accessible as REST API. They use [NETCONF](https://blog.ipspace.net/2012/06/netconf-expect-on-steroids.html) and XML, and neither one of them is exactly a mainstream programming technology these days.{{</note>}}

Obviously there's no need for the [API to mirror the CLI functionality](https://blog.ipspace.net/2014/02/cli-or-api-wait-do-you-really-have-to.html). The features available through the API could be totally different from the CLI commands, or a small subset of them. The API could also work on the control plane, or allow you to plug your code straight into the data plane (like F5 iRules).

{{<note info>}}For a more in-depth discussion of APIs, read [an excellent intro by The API Evangelist](http://apievangelist.com/index.html).{{</note>}}
