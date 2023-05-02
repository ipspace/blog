---
ai_tag: kick
title: "Real-Life Not-Exactly-Networking AI Use Case"
date: 2023-02-09 06:35:00
tags: [ worth reading, AI ]
---
I get several emails every week[^LEM] from people I never heard of telling me what a wonderful job they could do writing guest blog posts on a range of topics of interest to my audience.

I'm positive you must be pretty intelligent to be a successful scammer, so I'm sure the good ones are using ChatGPT to generate the "unique" content they're promising. I felt it was high time to return the favor.
<!--more-->
After wasting a few hours figuring out how to work with OpenAI API, IMAP and SMTP in Python, I finally had a small script that would:

* Fetch a message from a predefined folder[^PF]
* Ask GPT-3 to create a reply in predefined style
* Send the reply bcc-ing me for the sole purpose of evaluating the quality of the replies[^YS]

Most of the replies are pretty boilerplate[^BP], but there's an occasional gem like this one...

> Dear Julius McGee,
>
> A considerable pleasure it was to receive your kind offer of collaboration, my curiosity has perked at the prospect of joining forces. However, I am sorry to report that the idea does not strike me as one I shall pursue with vigour. With assurance I can say that there is no doubt a veritable public interest in 'Technology needs', however in conclusion it is a field whose machinations hold little sway over me.
>
> Yours truly,
> Charles GPT Dickens

... and sometimes GPT-3 manages to nail the "_letter in the style of Charles Dickens_" part:

> It was not with a feeling of pleasure that I read your polite and earnest enquiry as to whether I would be interested in discussing things further with you. That you appeared to believe there would be some mutual benefit to be derived from such a meeting startled me more than a little. 
>
> Never before have I associated myself with something termed as 'work management', this software of yours seems an oddity to me. The concept of visual analytics and planning on something such as a canvas is beyond my comprehension and knowledge - That said, I do admire the level of commitment you hold for your goals. 
>
> My website is devised solely for the purpose of sharing ideas and experiences. To help those struggling in whatever small way I can whilst operating within the bounds of honesty and truthfulness which are so important in life, although it does sadden me that you clearly disagree on such matters when offering commissions based around sales for commercial means. On this matter I stand firmly against any notion of partnering now or in the future.  
>
> In conclusion, engaging in any conversations as suggested by yourself would not come to fruition even if opportunity were somehow created through some accidental mishap between now and eternity itself. Your links shall be forever ignored making passing time the only true victor here today. 

[Derek Lowe](https://en.wikipedia.org/wiki/Derek_Lowe_(chemist)) was obviously correct when [he wrote](https://www.science.org/content/blog-post/thoughts-chatgpt-and-its-ilk) that the large-language models are _very accomplished bullshit generators_.

Need a similar tool? Clone my GitHub repository and have fun (improvement PRs are most welcome).

[^BP]: What would you expect from an AI model that was forced to be politically correct?

[^PF]: I don't trust OpenAI language models enough to let them classify whether something is a scam.

[^LEM]: If only I knew which moron leaked my email address to the spammers...

[^YS]: Yeah, sure. I just want to have a bit of fun reading them. Many of them are mainstream boring, some are hilarious.