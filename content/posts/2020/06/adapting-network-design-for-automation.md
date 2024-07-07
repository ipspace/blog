---
title: Adapting Network Design to Support Automation
date: 2020-06-24 05:34:00
tags: [ automation, design ]
---
*This blog post was initially sent to the subscribers of my SDN and Network Automation mailing list. [Subscribe here](http://www.ipspace.net/Subscribe/Five_SDN_Tips).*

Adam left a [thoughtful comment addressing numerous interesting aspects of network design in the era of booming automation hype](/2020/06/network-architects-facing-automation/#73) on my *[How Should Network Architects Deal with Network Automation](/2020/06/network-architects-facing-automation/)* blog post. He started with:

> A question I keep tasking myself with addressing but never finding the best answer, is how appropriate is it to reform a network environment into a flattened design such as spine-and-leaf, if that reform is with the sole intent and purpose to enable automation?

A few basic facts first:
<!--more-->
* Anything that can be described to a level that a total moron with infinite patience (also called _computer_ or _Turing machine_) can execute can be automated. 
* Corollary: You don't need a decent network design to automate stuff, you can automate any organically-grown spaghetti mess if you so desire;
* The cost of describing convoluted operations in a snowflake design, and the cost of implementing such operations might be too high to be practical. Automating an existing mess is often unfeasible.
* Automation code cannot become as obsolete as your network documentation. You MUST sync changes in network design with your automation code, or face the music once the inevitable disaster strikes.

With all that in mind, it does make sense to simplify a network design as much as possible (which is a good idea anyway), and to adapt it to be easy-to-automate if at all possible... assuming you don't sacrifice other required network properties on the altar of automation gods.

**TL&DR:** Support for network automation is just another business requirement like security, fast convergence, low jitter... You know how to deal with all the others, just add one more requirement to the mix and move on.

>  And at what cost to my own skills as a network engineer as I move further and further from the path of needing to understand and appreciate protocols and functionality when "the code simply handles it".

We've been in that boat a gazillion times in the past, and we lost fundamental knowledge every time something became stable- and commoditized enough that we no longer needed to care about it. In computing it all started with the first compilers - imagine how scary it must have been to people used to fine-tune their assembly-language code to fit into 32 KB of magnetic-core memory when the first FORTRAN compiler appeared. Most of us also forgot how transistors, CMOS, static and dynamic RAM, or modems work. It's probably hard to find someone who truly understands how to troubleshoot Ethernet cables as opposed to [plugging them into a tester and reading out the results](/2018/02/how-self-sufficient-do-you-want-to-be/).

I would love to predict when general networking will be at that stage, but so far the ["disruptive" vendors](/2019/10/the-cost-of-disruptiveness-and/) and the [industry MacGyvers](/2013/08/temper-your-macgyver-streak/) successfully keep that scary thought at bay... and until we get there, we'll still need people who can figure out what exactly went wrong when an [automated network crashes](/2018/02/big-red-button-for-network-automation/).

Alternatively, we'll dumb ourselves to the point we did in PC support. Instead of trying to fix stuff, it's cheaper and easier to reformat the disk and start from scratch, or start a new VM if you were smart enough to figure out VDI is more than a TLA that will be big three years from now... for the last 30 years. 

Let's wait and see how well [the dumbing down works in large-scale networking](/2015/11/can-you-afford-to-reformat-your-data/)... I'm positive some corporate bozos will buy into a $vendor fairy tale any time now and reap the results they deserve.

> IaC is the future. It is unavoidable. But the question I constantly contend with is at what cost, and at what point will my skill set as a network engineer/architect become irrelevant at the negotiating table for a new job or a raise request?

30 years ago I was able to write a complete multitasking operating system in Z80 assembly code. I can no longer do that, and nobody is willing to pay me for that skill set. The world has moved on, and so did I. We'll simply have to go through that same journey one more time (see also: [who moved my cheese](https://en.wikipedia.org/wiki/Who_Moved_My_Cheese%3F)).

> Particularly when they can relabel our roles by the promise of SD* and map us against the pay scale for developers once their non-complex spine-and-leaf topology goes live with only BGP and thousands of leaf switches merely needing the concept of overlay networking to be maintained in code.

There will always be well-paid jobs for smart people willing to work hard and apply their accumulated skills to tough problems... but unfortunately you can no longer expect to land a well-paid job and keep it for the next 40 years. There might be exceptions - people are still willing to pay for COBOL developers - but don't expect to be one.

Also, there's _developers_ and there's _software engineers_ and _architects_. Software architects in US are paid slightly better than network architects according to PayScale, so no worries there. OTOH, if your employer compares your skills to script kiddies hacking away low-quality Python code, it might be time to move on.

> It's coming, it's unstoppable, but it's scary. Alongside conforming with the progression, how do I stop being scared of the implied threat?

There's only one way to deal with the threat of becoming irrelevant: change and move on (burning cotton mills didn't work out too well I've heard).

Find a promising adjacent area you might be good in that meshes will with what you already know, and invest some time in becoming good in that area, keeping in mind that it [gets easier once you've accumulated enough knowledge](/2015/08/how-did-you-learn-so-much-about/), and that it's [better to be good at many things than excellent in a tiny niche](/2015/05/on-i-shaped-and-t-shaped-skills/) (see also this [excellent advice by Scott Adams](https://dilbertblog.typepad.com/the_dilbert_blog/2007/07/career-advice.html)). And guess what - cloud networking or network automation might be a perfect fit, and if you need a helping hand on this (supposedly) scary journey, check out our [online courses](https://www.ipspace.net/Courses).