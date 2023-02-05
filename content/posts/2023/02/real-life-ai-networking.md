---
title: "Real-Life Not-Exactly-Networking AI Use Case"
date: 2023-02-09 06:35:00
tags: [ worth reading ]
---
I get several emails every week[^LEM] from people I never heard of telling me what a wonderful job they could do writing guest blog posts on a range of topics of interest to my audience.

I'm positive you must be pretty intelligent to be a successful scammer, so I'm sure the good ones are using ChatGPT to generate the "unique" content they're promising. I felt it was high time to return the favor.
<!--more-->
After wasting a few hours figuring out how to work with OpenAI API, IMAP and SMTP in Python, I finally had a small script that would:

* Fetch a message from a predefined folder[^PF]
* Ask GPT-3 to create a reply in predefined style
* Send the reply bcc-ing me for the sole purpose of evaluating the quality of the replies[^YS]

Most of the replies are pretty boilerplate[^BP], but there's an occasional gem like this one:

> Dear Julius McGee,
>
> A considerable pleasure it was to receive your kind offer of collaboration, my curiosity has perked at the prospect of joining forces. However, I am sorry to report that the idea does not strike me as one I shall pursue with vigour. With assurance I can say that there is no doubt a veritable public interest in 'Technology needs', however in conclusion it is a field whose machinations hold little sway over me.
>
> Yours truly,
> Charles GPT Dickens

Need a similar tool? Clone my GitHub repository and have fun (improvement PRs are most welcome).

[^BP]: What would you expect from an AI model that was forced to be politically correct?

[^PF]: I don't trust OpenAI language models enough to let them classify whether something is a scam.

[^LEM]: If only I knew which moron leaked my email address to the spammers...

[^YS]: Yeah, sure. I just want to have a bit of fun reading them. Many of them are mainstream boring, some are hilarious.