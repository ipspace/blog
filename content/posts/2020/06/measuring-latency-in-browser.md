---
title: "Interesting: Measuring End-to-End Latency in Web Browser"
date: 2020-06-04 08:53:00
tags: [ Internet,network management ]
---
CloudFlare launched yet another service: [transfer speed- and latency measurements done from a web browser](https://blog.cloudflare.com/test-your-home-network-performance/). While it's pretty obvious how you could measure transfer speed (start an asynchronous transfer, register for the JavaScript **onreadystatechange** event to notice out when it has completed, and compute the transfer rate), measuring latency seems like a bit of black magic. After all, you can't do a **ping** from a web browser, can you?
<!--more-->
Well, CloudFlare couldn't do it either, but fortunately modern browsers have extensive [Browser Performance API](https://blog.cloudflare.com/browser-performance-api/), and part of that API includes request/response timing. Here's how you can use that API to measure end-to-end latency:

* Start a bogus request to get past TCP/SSL negotiations;
* Once the bogus request completes, the HTTPS session with the server is not torn down (modern browsers use persistent HTTP connections), and it already has decent TCP window sizes (see also: [Increasing TCP's Initial Window](https://tools.ietf.org/html/rfc6928) - RFC 6928);
* Execute next HTTP request and use browser performance API to get the difference between **requestStart** and **responseStart** timestamps. Ignoring the serialization delay of the HTTP request and response, you'll get a pretty good guesstimate of the end-to-end latency.

Interestingly, their results are pretty accurate: the latency to speed.cloudflare.com reported by my web browser was 19.9 msec, the ping-measured latency was 20.4 msec.