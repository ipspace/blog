---
title: When Machine Learning in Networking Might Make Sense
date: 2020-09-24 07:13:00
tags: [ automation ]
---
In March I explained why it's [unrealistic to expect to use machine learning to solve unknown problems in today's snowflake networks](/2020/03/machine-learning-in-networking-products/)... but are there other problems that could be solved?

Here's an idea [Paul Greenberg](https://www.linkedin.com/in/greenpau/) pointed me to: [machine learning on public DNS data](https://github.com/chanakyaekbote/coredns_ml_plugin). Let's see whether it might make sense:
<!--more-->
* The training data is available (public DNS domain names) and does not depend on specific network design (everyone is querying the same public DNS records);
* The project uses two sets of training data: DNS names that are known to be good, and DNS names that are known to be malicious. The two sets are coming from trusted sources.

So far so good. The sample neural network got to 98% accuracy, and I'm positive it's pretty easy to make it a bit better with a larger training set and larger neural net.

What I'm struggling with is whether that's good enough. Like any other _pretty-reliable_ test this one has deal with

* **False negatives** - how often a malicious domain name is not identified as such;
* **False positives** - how many times a valid domain name is blocked because it's identified as malicious.

Considering that one (hopefully) wouldn't use a DNS blocker as the only security tool, I would be worried about false positives. Getting 2% of valid domain names blocked seems a bit high to me... but then I have no baseline to compare it to. Pointers would be highly appreciated.