---
title: "Worth Exploring: bgpstuff.net"
date: 2020-10-20 06:31:00
tags: [ BGP, Internet ]
---
[Darren O'Connor](https://www.linkedin.com/in/darren-o-connor-33b393b/) put together a [BGP looking glass with web GUI](https://bgpstuff.net/). Nothing fancy so far... but he also offers REST API interface (because REST API sounds so much better than HTTP).

The REST API calls return text results, so you can use them straight in a Bash script. For example, here's a simple script to print a bunch of details about your current IP address:
<!--more-->
```
#!/bin/bash
IP=$(curl -s ifconfig.me)
echo Your public IP address: $IP
echo
curl https://bgpstuff.net/route?ip=$IP
curl https://bgpstuff.net/aspath?ip=$IP
curl https://bgpstuff.net/origin?ip=$IP
```

But of course we should frown on text printouts in the days of glorious JSON, and fortunately Darren thought about that and implemented JSON-formatted results (just add `format=json` to the URL). Combine that with **[jq](https://blog.scottlowe.org/2015/11/11/handy-cli-tool-json/)** and you could do almost anything without invoking the magic powers of Perl Regular Expressions, for example:

```
#!/bin/bash
IP=$(curl -s ifconfig.me)
ASN=$( curl -s "https://bgpstuff.net/origin?ip=$IP&format=json"|\ 
   jq '.originAsn')
```

Happy scripting ;)