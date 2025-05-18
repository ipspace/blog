---
title: "Netlab Examples in GitHub Codespaces"
date: 2024-07-01 07:59:00+0200
tags: [ netlab ]
netlab_tag: codespace
---
A few days ago, someone asked me about the IPv4 next-hop details of running interface EBGP sessions. I pointed him to a [blog post explaining them](/2022/11/bgp-unnumbered-duct-tape/), adding, "And of course, you can test that in _[netlab](https://netlab.tools/)_." A few minutes later, it hit me: instead of asking him to set up _netlab_ locally, I could enable him to do that in a minute with GitHub Codespaces.

Setting that up was easy: copy the `.devcontainer` directory from the [BGP labs repository](https://github.com/bgplab/bgplab) into the [netlab examples repository](https://github.com/ipspace/netlab-examples) and commit the change. After a brief yak-shaving exercise (writing README files and rearranging a few folders), I successfully [started the codespace](https://github.com/codespaces/new/ipspace/netlab-examples) and was ready for this blog post. There was just one gotcha...
<!--more-->
I couldn't find a way to pass a different working directory to GitHub Codespaces; when a new codespace opens in a browser window, it always starts in the top directory. Here's what you have to do afterward:

* Get the URL of the netlab example you want to run (for example, `https://github.com/ipspace/netlab-examples/tree/master/BGP/Unnumbered`)
* Get the example directory name from the URL (`BGP/Unnumbered`)
* Change into that directory (`cd BGP/Unnumbered`)
* Execute **netlab up**
* Wait for the container images to download and the lab to start (assuming the lab uses images from vendors that understand the benefits of hassle-free downloads)
* Have fun ;)

Finally, when you're done, don't forget to shut down the lab (with **netlab down**) and [stop the GitHub codespace](https://bgplabs.net/4-codespaces/#cleanup-and-shutdown).
