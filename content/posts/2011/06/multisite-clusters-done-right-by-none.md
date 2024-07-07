---
date: 2011-06-30 06:13:00.003000+02:00
tags:
- data center
- load balancing
title: Multisite Clusters Done Right... by None Other than Microsoft
url: /2011/06/multisite-clusters-done-right-by-none/
---
I had to check the Microsoft clustering terminology a few days ago, so I used Google to find the most relevant pages for "Windows cluster" and landed on the *Failover clustering* home page where the *Multisite Clustering* link immediately caught my attention. Dreading the [humongous amount of layer-2 DCI stupidities](/2011/06/stretched-clusters-almost-as-good-as/) that could lurk hidden behind such a concept, I barely dared to click on the link... which unveiled one of the most pleasant surprises I've got from an IT vendor in a very long time.
<!--more-->
{{<note warn>}}The links to the Microsoft documentation used in the original version of this blog post are broken, so I removed them. You'll have to rely on your Google-Fu.{{</note>}}

Microsoft actually understands that some people prefer to keep their IT infrastructure stable and supported *multi-subnet clusters* for quite some time. What a revolutionary concept for the L2-crazed flat-earth world some other vendors are busy promoting.

The details of Microsoft's multisite cluster implementation made me smile (and some people know that's a tough call) -- cluster resources register their A and AAAA records with DNS (yes, contrary to some networking vendors, Microsoft does support IPv6 in the data center) and there are two property settings that you can fine-tune: the DNS TTL and the registration of all (or just one) IP address.

The failover between subnets is completely controlled by DNS -- not suitable for web servers due to browsers' DNS pinning, but let's hope your application architects know a scale-out approach is a better fit for a web server farm than a failover cluster. However, the DNS-based failover is a pretty good fit for other back-end services, for example the SQL server (don't forget that a service needs to be *restarted* in a failover cluster and the restart time is significantly longer than the DNS failover time). What Microsoft does is almost exactly the same concept I was recommending in my [Data Center Interconnects](https://www.ipspace.net/DCI) webinar; the only difference is the implementation method -- they use their own DNS, I recommended using local and global load balancing.

Assuming more OS vendors see the same light Microsoft did, the shiny new L2 DCI technologies just might land where they belong -- the same technology graveyard where LANE and ATM-to-the-desktop are lovingly preserved. Oh, and whenever the application people or server administrators tell you they need L2 DCI for Windows failover clusters, tell them Microsoft solved their problem over a year ago in Windows Server *2008*.
