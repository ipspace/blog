---
url: /2008/01/generate-terminal-escape-sequences-from/
title: "Generate terminal escape sequences from Tcl"
date: "2008-01-14T06:33:00.001+01:00"
tags: [ Tcl ]
---
One of my readers (who unfortunately prefered to stay anonymous, so I cannot give credit where it's due) [figured out how to output escape sequences from IOS Tclsh](/2008/01/any-idea-how-to-generate-binary-output.html#c5412853245407117685): you have to execute [terminal international](http://www.cisco.com/univercd/cc/td/doc/product/software/ios124/124cr/hcf_r/cfn_11h.htm#wp1035628) command first.  
  
We can use that functionality to do all sorts of interesting things, like clearing the screen and displaying red header text from a Tcl script running on Cisco IOS:
<!--more-->
```
exec terminal international;
puts "\033\[2J\033\[H\033\[1;31mHeader text\033\[m"
```

Obviously, you could easily use this functionality to build a nice full-screen menu system.

Notes

-   To output the ESC character, use the \\033 code within the double quotes;
-   To output the left angle bracket, you have to use the \\\[ sequences, otherwise Tcl interprets the bracket as start of an expression;
-   The ANSI escape sequences (recognized by most terminal emulators) are [documented on Wikipedia](http://en.wikipedia.org/wiki/ANSI_escape_code);
