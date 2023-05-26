---
date: 2007-08-27T07:27:00.001+02:00
tags:
- Tcl
title: Insert Responses to Command Prompts in Tclsh
url: /2007/08/insert-responses-to-command-prompts-in.html
---

I have been aware of the [**typeahead**](http://www.cisco.com/en/US/products/sw/iosswrel/ps5207/products_feature_guide09186a00801a75a7.html#wp1027195) Tcl command for months, but somehow I never got it to work. 

It works perfectly in IOS release 12.4(15)T (it might have something to do with [other fixes to Tclsh](https://blog.ipspace.net/2007/08/you-fix-some-you-break-some.html)), so to clear interface counters ([as Michal would like to do](https://blog.ipspace.net/2007/04/execute-multiple-commands-at-once.html#comment-1688346259298046702)), this is what you can do:
<!--more-->
``` code
typeahead "y"
exec "clear counter dialer 0";
```

**Warning:** if the input is not consumed by the executed commands, it stays in the typeahead buffer; quite dangerous if you have a sequence of commands, as the wrong command could be acknowledged.

{{<jump>}}[Keep reading](https://blog.ipspace.net/kb/Tclsh/){{</jump>}}