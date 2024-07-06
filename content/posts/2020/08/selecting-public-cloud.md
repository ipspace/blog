---
title: "Which Public Cloud Should I Master First?"
date: 2020-08-20 07:21:00
tags: [ cloud,AWS,Azure ]
---
I got a question along these lines from a friend of mine:

> Google recently announced a huge data center build in country to open new GCP regions. Does that mean I should invest into mastering GCP or should I focus on some other public cloud platform?

As always, the right answer is "it depends", for example:
<!--more-->
* Do you have existing customers (or potential employers you'd love to work for) asking for specific public cloud skills? There's your answer.
* Do you expect organizations that are willing to pay for your expertise to care about in-country cloud platform? If so, is there an Azure or AWS region in your country?
* Failing that, do you see high interest for specific cloud platforms in your environment?
* None of the above? You might want to hedge your bets and go with the platform with the highest market share (AWS) or enterprise mindset (Azure). You might also decide to focus on a tiny but potentially lucrative niche (like being COBOL or Haskell programming ninja) and invest in GCP, IBM cloud, or Oracle cloud... but don't expect to get a great consulting project or a job offer the moment you learn the basics.

From a purely personal standpoint:

* I love named objects in Azure API but [hate their orchestration system](/2019/06/how-microsoft-azure-orchestration.html), and the way they sometimes leave resources in limbo for hours, so I'd try to stay as far away from it as possible.
* Google killed several project I used to run my business or organize my professional life, so I can't trust them anymore... and I'm not alone. Read _[Dear Google Cloud: Your Deprecation Policy is Killing You](https://medium.com/@steve.yegge/dear-google-cloud-your-deprecation-policy-is-killing-you-ee7525dc05dc)_ for a hilarious (but true) take on the topic. Don't expect GCP content on ipSpace.net anytime soon. We're too busy doing (hopefully) useful stuff to focus on things that are deprecated-and-redesigned every few months (see also: [Ansible](/2019/09/measure-twice-cut-once-ansible.html)).
* Everything else apart from AWS is too niche to invest any time  in (unless you're well-paid to do so). As nobody ever asked for content covering smaller public cloud providers, I see no reason to create it ;)

Even though it would be nice to say "_that leaves only AWS, problem solved_", large enterprise love Azure for various reasons, so we try to have you covered regardless of whether you want to learn more about AWS or Azure networking, including:

* Platform-agnostic [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course.
* [AWS Networking webinar](https://www.ipspace.net/Amazon_Web_Services_Networking)
* [Microsoft Azure Networking webinar](https://www.ipspace.net/Microsoft_Azure_Networking)
* [Azure networking examples](https://github.com/ipspace/azure)
* [AWS and Azure automation examples](https://github.com/ipspace/pubcloud)

Final note (in case you haven't decided yet): even though we encourage course attendees to use any platform of their choice for the hands-on exercises, everyone chose AWS or Azure.
