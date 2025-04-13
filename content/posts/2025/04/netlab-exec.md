---
title: "netlab: Execute a Command on Multiple Devices"
series_title: "Execute a Command on Multiple Devices"
date: 2025-04-16 07:47:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
When I was updating the [Network Migration with BGP Local-AS Feature](/2009/03/bgp-local-as-feature-basics/) blog post, I wanted to execute the same command (**show ip bgp**) on all routers in my network.

Not a problem: since [Dan Partelly added](https://github.com/ipspace/netlab/pull/1398) the **[netlab exec](https://netlab.tools/netlab/exec/)** command, it's as simple as **netlab exec \* show ip bgp**. Well, not exactly; there are still a few quirks.
<!--more-->
The easy one first: any decent Unix shell thinks it should expand the `*` in the command line, resulting in a command that includes every filename in the current directory. Not exactly helpful; we have to quote the `*` to make the command work:

```
$ netlab exec '*' show ip bgp
```

{{<note>}}
A message from the Department of Bizarre Things: **bash** expands the *[glob pattern](https://en.wikipedia.org/wiki/Glob_(programming))* (yeah, that's what they are called) only if at least one file matches it, otherwise it leaves it intact. That leads to total confusion when `netlab exec r*` works but `netlab exec *` does not.
{{</note>}}

Here  are the first few lines produced by the above command:

```
Connecting to clab-LocalAS_Migr-custa using SSH port 22, executing show ip bgp



BGP table version is 4, local router ID is 10.0.0.4
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
              t secondary path, L long-lived-stale,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      10.1.0.10                              0 64510 64500 i
 *>   10.8.8.0/24      0.0.0.0                  0         32768 i
 *>   10.9.9.0/24      10.1.0.10                              0 64510 65100 iConnection to clab-localas_migr-custa closed by remote host.
```

We have the results we need, but they're full of noise. For example, we should get rid of the BGP table legend. We can use the `| begin Network` filter on Cisco IOS to do that, but it's a bit hard to add that filter to a **bash** command without starting a Linux pipe. Fortunately, we can quote the `|` symbol:

```
$ netlab exec '*' show ip bgp \| begin Network
Connecting to clab-LocalAS_Migr-custa using SSH port 22, executing show ip bgp | begin Network


     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      10.1.0.10                              0 64510 64500 i
 *>   10.8.8.0/24      0.0.0.0                  0         32768 i
 *>   10.9.9.0/24      10.1.0.10                              0 64510 65100 iConnection to clab-localas_migr-custa closed by remote host.
```

It would also be nice to get rid of the *Connecting to...* header but still retain some information about the device on which we're executing the command. Let's use the `-q` (quiet) flag together with the `--header` flag:

```
$ netlab exec -q --header '*' show ip bgp \| begin Network
================================================================================
custa: executing show ip bgp | begin Network
================================================================================


     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      10.1.0.10                              0 64510 64500 i
 *>   10.8.8.0/24      0.0.0.0                  0         32768 i
 *>   10.9.9.0/24      10.1.0.10                              0 64510 65100 iConnection to clab-localas_migr-custa closed by remote host.
```

Finally, there's the annoying "*Connection closed by remote host*" message appended at the end of the last line. I couldn't get rid of it (and StackOverflow and friends were no help) or persuade Cisco IOS to terminate the last line with a newline; if you have an idea, please add a comment.
