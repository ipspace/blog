---
date: 2021-11-16 07:12:00+00:00
high-availability_tag: app
tags:
- design
- high availability
- cloud
title: Optimizing the Time-to-First-Byte
---
I don't think I've ever met someone saying "_I wish my web application would run slower_." Everyone wants their stuff to run faster, but most environments are not willing to pay the cost (rearchitecting the application). Welcome to the wonderful world of PowerPoint "solutions".

**The obvious answer**: The Cloud. Let's move our web servers closer to the clients -- deploy them in various cloud regions around the world. Mission accomplished.

Not really; the laws of physics (latency in particular) will kill your wonderful idea. I [wrote about the underlying problems years ago](/2015/01/latency-killer-of-spread-out/), wrote another blog post [focused on the misconceptions of cloudbursting](/2020/02/the-myth-of-scaling-from-on-premises/), but I'm still getting the questions along the same lines. Time for another blog post, this time with even more diagrams.
<!--more-->
Let's assume your customer sits 10 msec away from your data center.

{{<figure src="/2021/11/TTFB-challenge.png" caption="Optimizing Time to First Byte: The Challenge">}}

When the client tries to open a web page for the first time, it takes a long while before the first usable byte arrives at the web browser[^1]:

[^1]: A lot of discussions are focused on Time to First Byte, but what some companies are interested in is really Time to First Ad ;)

* One round-trip time (RTT) is spent on TCP SYN/ACK
* Two more RTTs are spent [negotiating TLS](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake).
* Another RTT is spent sending HTTP request and receiving the initial few packets of the response.
* At least one more RTT is spent receiving the rest of the HTTP response.

{{<figure src="/2021/11/TTFB-end-to-end.png" caption="Too many round-trip times kill performance">}}

You could solve this conundrum with a new protocol that reduces the number of RTTs needed to establish a session (see: [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3)) or you could deploy the web server closer to the client:

{{<figure src="/2021/11/TTFB-web.png" caption="Deploying a web server closer to the client">}}

Guess what... as I [explained](/2015/01/latency-killer-of-spread-out/) [several times](/2020/02/the-myth-of-scaling-from-on-premises/) pulling the web server away from the underlying infrastructure only makes the situation worse -- a web application usually makes many back-end requests to collect data needed by a single client request.

The only working solution is thus a *web proxy* -- a local web server that terminates the client session and uses an *existing HTTP session* with the back-end web server, spending a single RTT for the HTTP request and response.

{{<figure src="/2021/11/TTFB-proxy.png" caption="Deploying a web proxy closer to the client">}}

Using web proxies has another advantage: if you deploy web servers all around the world you have to manage them, but if you settle for a web proxy you can buy it as a service from any CDN provider. I'm using CloudFlare; you could easily get the same service from AWS, Azure, or a dozen other companies.

For more information, watch the _[TCP, HTTP and SPDY](https://www.ipspace.net/TCP,_HTTP_and_SPDY)_ webinar. For even more details, read the awesome _[High Performance Browser Networking ](https://hpbn.co/)_ book by Ilya Grigorik.


