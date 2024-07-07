---
url: /2009/01/generate-https-requests-from-tcl-shell/
title: "Generate HTTP(S) requests from Tcl shell"
date: "2009-01-19T06:40:00.002+01:00"
tags: [ Tcl ]
---
A few days ago, a reader sent me an e-mail titled “*Telnet Automation from a Cisco Router*” and complained that IOS Tcl does not support the *[expect](http://expect.nist.gov/)* commands (**spawn**, **send** and **expect**). Since [*Expect* is a Tcl extension](http://wiki.tcl.tk/201), not part of the core Tcl, it’s not included in Cisco IOS, which was the only answer I could give.

{{<note>}}You might be able to [port *Expect* to IOS as a Tcl package](/2007/09/using-tcl-packages-on-cisco-ios/) if it doesn’t require external libraries.{{</note>}}
<!--more-->
However, it turned out that the reader actually wanted to trigger HTTP requests from the router. Cisco IOS Tcl has some built-in client-side HTTP support, but it’s far simpler to rely on the built-in **http:** file system. For example, to do a HTTP GET request, use the following Tcl command:

``` code
rtr#tclsh
rtr(tcl)#set result [exec {more http://webServer/index.html}]
<h1>Empty</h1>
```

As always, there are a few caveats:

-   You can trigger HTTP GET requests, but not the PUT or POST requests.
-   The server-side script should always return the HTTP status 200 (successful), otherwise the **more** command will fail. The actual status can be passed in the HTML response.

You can use the same trick to trigger HTTPS requests from Tcl.
