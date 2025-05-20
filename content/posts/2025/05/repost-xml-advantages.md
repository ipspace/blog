---
title: "Repost: On the Advantages of XML"
date: 2025-05-26 08:07:00+0200
tags: [ automation ]
series: cli
cli_tag: challenge
---
Continuing the discussion started by my [Breaking APIs or Data Models Is a Cardinal Sin](/2025/04/api-data-model-contract/) and  [Screen Scraping in 2025](/2025/05/screen-scraping-2025/) blog posts, [Dr. Tony Przygienda](https://www.linkedin.com/in/dr-tony-przygienda-018501/) left another thoughtful comment worth reposting as a publicly visible blog post:

---

Having read [your newest rant around my rant](/2025/05/screen-scraping-2025/) ;-} I can attest that you hit the nail on the very head in basically all you say:

* XML output big? yeah.
* JSON squishy syntax? yeah.
* SSH prioritization? You didn't live it until you had a customer where a runaway python script generated 800+ XML netconf sessions pumping data ;-)

So, all very correct what you say _however_ having lived all the dreams, I'm still very much for XML. Yes, XSLT and XML matching ain't for the faint of heart, but unless you properly account for the semantic structure of the data, a reliable, maintainable network automation is looking for a free lunch AFAIS.

Which all boils down to the same underlying principle. You have complex problems, you need to hire smarter and smarter (well-educated) folks to deal with them. AI can help some, and the more structured the data, the more it can help, but complexity calls for general intelligence, something today only smart people bring to the table IME.

---

Tony is right; AI can help some. ChatGPT generated a correct XPath expression to count the number of IS-IS adjacencies in the  Junos **show isis adjacency** XML printout and flawless Python code to go with it.

And just when I thought we ran out of excuses for not using XML, ChatGPT asked me whether I would like to use **ncclient** for a full-blown solution, and then generated three versions of the code that failed miserably. Admittedly, it got it right on the fourth attempt. Well, make that a *maybe*; there were no syntax errors, and I got the expected result back, but who knows what gremlins are still hidden in the code.
