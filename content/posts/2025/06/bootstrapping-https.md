---
title: "Interesting: Bootstrapping HTTPS"
date: 2025-06-03 08:30:00+0200
tags: [ worth reading ]
---
Jan Schaumann published an [interesting blog post](https://www.netmeister.org/blog/http-123.html) describing the circuitous journey a browser might take to figure out that it can use QUIC with a web server.

Now, if only there were a record in a distributed database telling the browser what the web server supports. [Oh, wait](https://www.rfc-editor.org/rfc/rfc9460.html)... Not surprisingly, browser vendors don't trust that data and have implemented a [happy eyeballs-like protocol](https://docs.google.com/document/d/1i4m7DbrWGgXafHxwl8SwIusY2ELUe8WX258xt2LFxPM/edit?tab=t.0#heading=h.dk2fhev07ryt) to decide between HTTPS over TCP and QUIC.