---
cli_tag: cli-api
date: 2017-10-24 08:18:00+02:00
series:
- cli
tags:
- automation
title: CLI or API… Again (and Again and Again…)
url: /2017/10/cli-or-api-again-and-again-and-again.html
---
Got this comment on one of my blog posts:

> When looking at some of the CLIs just front-ending RESTAPIs, I wonder if \"survival\" of CLI isn\'t just in the eyes of the beholder.

It made me really sad because I wrote about this exact topic several times... obviously in vain. Or as one of my network automation friends said when I asked him to look at the draft of this blog post:
<!--more-->
> This topic is one that\'s been beaten to death, dragged behind a tractor, resurrected, burnt, buried, dug up, set on fire again and then thrown out to sea.

Sometimes I wonder whether it's worth wasting everyone's time trying to debunk vendor myths.

### Background Reading

Anyway, here are a few things I wrote on the topic. You might want to read them first ;)

-   [What is this API thingy?](/2014/07/what-is-this-api-thingy.html) where I said "API is just CLI for program-to-program communication;
-   [CLI and API Myths](/2013/06/cli-and-api-myths.html) explaining how they're just two sides of the same coin);
-   [CLI or API? Do you really have to ask?](/2014/02/cli-or-api-wait-do-you-really-have-to.html) where I went into how trivial it is to implement both if you have the right architecture;
-   [To API or not to API?](/2016/10/to-api-or-not-to-api.html) in which I went into the details of why network device CLI (as opposed to CLI in general) sucks;

### Back to CLI versus API

Coming back to the comment. Is CLI a living dead and kept alive only because grumpy old men continue to use it? How about this:

-   Having API is great if you need access to a device/system/software package/car/whatever from upstream orchestration/provisioning system;
-   Humans don\'t cope well with program-to-program APIs like REST or gRPC. Whenever you need to touch the box/system/... directly you'd wish for a CLI before completing the first **curl** command. Just ask anyone who's old enough to remember Wellfleet Technician Interface;

In short: a CLI which talks to the API allows humans to tweak and optimize the systems directly (without going through an umbrella orchestration system UI) without the human being bogged down with the minutia of URL components, HTTP cookies, or JSON syntax.

Not surprisingly, having CLI sitting on top of API for operator's convenience is a long-standing (and pretty successful) practice. Why do you think Junos had this option for 15 years, or why there are CLI versions of AWS or OpenStack API?

### For Those Few that Actually Care

Nothing I write here will nudge the marketers or social media experts a tiny bit. They live in a different reality. You could continue drinking vendor their KoolAid and enjoying quotes that have no touch with reality, or you could decide to take the red pill: consume some quality structured content that will teach you how things get done.

There are plenty of good choices out there, including my [NetOps webinars](http://www.ipspace.net/Roadmap/Network_Automation_webinars), [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course, excellent presentations from David Barroso, Mircea Ulinic, the Facebook team and many others, most of them listed in [Awesome Network Automation](https://github.com/itdependsnetworks/awesome-network-automation) GitHub repository.
