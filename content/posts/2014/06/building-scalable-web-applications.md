---
date: 2014-06-02 09:49:00+02:00
title: Building Scalable Web Applications – Final Presentations
url: /2014/06/building-scalable-web-applications.html
tags: [ training ]
---
Last Friday my students attending this year's [Designing Scalable Web Applications](/2012/02/going-back-to-ivory-tower.html) course presented their semester-long assignments. I can't tell you how pleasantly surprised I was -- the results were much better and more polished than what I've seen during the previous years.
<!--more-->
A few things that particularly surprised me:

-   Most applications were deployed somewhere in the cloud. Heroku was the most popular platform (with *localhost* being a trusted backup solution ;)
-   Almost everyone used browser-based UI controller doing REST calls to the server backend;
-   Support for mobile platforms and dynamic screen resizing (aka fluid or liquid layout) was universal;
-   Most applications were integrated with Google+, Facebook and Twitter.

As always, it turned out there were a few tricks that got the job done. Everyone used browser frameworks ([Angular](http://en.wikipedia.org/wiki/AngularJS) to build the application and [Twitter Bootstrap](http://getbootstrap.com/2.3.2/) to build the UI) and most applications relied on [Firebase](https://www.firebase.com) backend.

These choices significantly reduced the development environment complexity (in the previous years the students used Django/Python backend) and the number of programming languages they had to master (most applications used exclusively JavaScript; some people even used node.js to have the same language on the backend), giving the students more time to focus on solving the application-level problem.

### Lessons learned

-   Whatever you're trying to do, there's probably a tool or framework out there that will help you get the job done quicker or easier. Invest some time in finding the tool instead of rushing into a we've-done-this-before development or deployment.
-   Minimize the complexity of your environment -- the number of programming languages, the number of technologies you use, the number of vendors in your network...
-   Learn new technologies and frameworks even though they look complicated or arcane (NETCONF comes to mind ;). I can't tell you how much boring coding third-party sign-on (like *Login with Google+*) replaces.

### Finally...

Don't be afraid of trying something new. Some of the students knew very little programming when the course started (I know that sounds totally weird, as I'm teaching at Faculty of Computer and Information Science -- welcome to the wonderful world of higher education), but registered nonetheless, struggled along, completed their assignments, and became decent programmers.

I'm positive there's something you're avoiding like black plague because you think it's too complex. Go for it, invest some time, build a lab, study the tutorials, and master it. If I hadn't jumped into the choppy waters of data center networking and virtualization, I would have forever remained the "*layer-3 guru sitting in an ivory tower of MPLS and BGP*."
