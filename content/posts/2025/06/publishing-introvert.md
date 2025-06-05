---
title: "Publishing Content as an Introvert"
date: 2025-06-09 07:56:00+0200
tags: [ certifications ]
---
I got an interesting question from a reader. He listened to my podcast with Eric Chou and decided to try to *learn in public*:

> Currently, I'm studying for the CCNP ENARSI exam, and would like to start posting my labs to LinkedIn, and perhaps even upload my lab topologies and configs to Git.

That's a great idea. I would minimize the LinkedIn part[^FTT] and focus on Git:

[^FTT]: If you're a regular reader, you probably know my thoughts on ~~feeding~~ financing the social media ~~trolls~~ juggernauts with your content.

* Create a Git repo for your lab content and host it on GitHub (or any other similar service of your choice). While you're at it, add another one for your future website.
* Publish each lab in a separate directory. Add a diagram (JPG/PNG), the lab topology if you're using a tool like _netlab_ or _containerlab_, and the device configuration files.
* Describe the lab, your goals, your experience, and what you learned in a README.md file in that directory.
* Keep an index of your work in the repository's top README.md file.
* Publish only a short description of your work, together with the link to the relevant GitHub directory on LinkedIn.

My reader already figured out why he'd want to do that:

> I figure it will push me out of my comfort zone and finally get me to learn Git.

Getting out of one's comfort zone in a low-risk environment is always a great idea. Also, I don't know anyone being fired for knowing Git[^KG].

[^KG]: OTOH, I do know someone who became the local Git Janitor after asking, "And why don't we have source control like Git?" in a meeting. Be careful what you ask for ;)

> Plus, it could help me stand out to potential future employers.

That's true, but there's just a tiny gotcha: you have to get pretty deep into the selection process (for example, close to the in-person interview) to persuade your potential employers to look at your work. You still have to pass the initial filters, or (even better), establish contacts that will allow you to bypass those filters with a timely recommendation.

However:

> My problem is that this goes against every shred of my introverted nature, and I'm worried about 'looking basic or silly' on a platform where so many talented people, such as yourself, post interesting and more advanced stuff daily.

Keep in mind you're not competing for attention. You're building a portfolio of your work, and it should reflect your progress[^CUOS]. All the talented people[^TL] needed decades to get the experience that allowed them to create and post advanced stuff.

[^CUOS]: Also, occasionally clean up the old stuff

[^TL]: Please note that this does not include *Thought Leaders*™ or AI slop regurgitators now dominating social media.

Next, most people are not jerks[^WR]. If you clearly state what you're doing, most readers won't be too upset even if you make a mistake or two. You should also differentiate between facts, conclusions, and opinions. It's OK to reach incorrect conclusions or hold differing opinions, but there are no 'Alternate Facts' (regardless of what some people think). Additionally, if I'm in serious doubt about my claims, I always ask readers for comments, and you could easily ask readers to submit pull requests with fixes.

[^WR]: Although the Internet sadly gives jerks wider reach and no accountability. A century ago, they would be ignored (or worse) in the village pub.

Finally, the sad fact (unless you're an introvert, in which case it might be comforting) is that content from new creators gets very little visibility. When I started publishing stuff (in the heyday of exponential growth of blogging), my blog received around 100 page views every week[^HTSE]. Here are the (weekly) stats for the first few months after I started publishing blog posts:

[^HTSE]: Half of them were probably coming from search engines

{{<figure src="/2025/06/blog-stats-2006.png">}}

It's much harder to attract visitors these days because there is so much more content available[^SL] and everyone believes backflipping squirrels on TikTok is the way to go.

[^SL]: Most of it conforming to [Sturgeon's Law](https://en.wikipedia.org/wiki/Sturgeon%27s_law).

My reader concluded his email with a bit more personal question:

> Did you ever have these same concerns about posting publicly, and if so, how did you get over them?

Of course I did. I was a total disaster when trying to explain things or write a coherent article (just ask my wife). Fortunately, I was forced into an early version of Cisco's instructor certification program, which included two weeks of intensive training in presentation skills. After that, the only way forward was to create my own training content[^2MP], and that forced me to start organizing my thoughts. Admittedly, most of my early courses started as crappy slideware that was slowly improved after being delivered a dozen times. Nothing makes you think faster than having to explain a concept on a whiteboard to a roomful of bright engineers[^TT], and I made sure that the good explanations made it back to the slide deck.

The book I decided to write for Cisco Press (another major leap out of my comfort zone) was another huge step forward. Not only was I forced to organize my thoughts into a format that was reasonably easy to digest, but my editor did a marvelous job making my writing sound almost English. Additionally, I was fortunate to have phenomenal tech reviewers, including Russ White, who rewrote large parts of my text to make it flow better. If you like reading my rants, thank them ;)

[^2MP]: Somehow, we failed to fill more than a few classes with networking engineers interested in how Cisco routers work in a country with two million inhabitants in the 1990s.

[^TT]: One of my audiences was Cisco's European TAC engineers.

While it's hard to replicate that same approach, most engineers might benefit from good presentation skills training. There are also other mechanisms that you could use to force yourself to appear in (controlled) public, for example, the [Toastmasters](https://www.toastmasters.org/) or debate clubs. After gaining the initial confidence (as in "not being a total disaster in front of an audience"), start applying as a speaker to local conferences; some of them might appreciate someone willing to invest their time into creating an interesting presentation for free[^SFF].

[^SFF]: I might be living in the wrong part of the world, but I've never heard of small local conferences paying their speakers.
