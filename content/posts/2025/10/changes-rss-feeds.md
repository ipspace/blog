---
title: "Changes in ipSpace.net RSS Feeds"
date: 2025-10-08 06:40:00+0200
tags: [  ]
---
**TL&DR:** You shouldn't see any immediate impact of this change, but I'll eventually clean up old stuff, so you might want to check the URLs if you use RSS/Atom feeds to get the list of ipSpace.net blog posts or podcast episodes. The (hopefully) final URLs are listed on [this page](https://www.ipspace.net/Feeds).

**Executive Summary:** I cleaned up the whole ipSpace.net RSS/Atom feeds system. The script that generated the content for various feeds has been replaced with static Hugo-generated RSS/Atom feeds. I added redirects for all the old stuff I could find (including `ioshints.blogspot.com`), but I could have missed something. The only defunct feed is the *free content* feed (which hasn't changed in a while, anyway), as it required scanning the documents database. You can use [this page](https://www.ipspace.net/Subscription/Free) to find the (ever-increasing) free content.

And now for the real story ;)
<!--more-->
After I published the latest podcast episode yesterday, I noticed that the Apple Podcast system didn't pick it up. A bit of troubleshooting quickly revealed the culprit: the Apple podcast used a Feedburner-enhanced feed to get the iTunes tags, and Feedburner failed to update the feed. No surprise there; it's another slowly failing service that Google acquired and then neglected. I was already generating [Atom](https://en.wikipedia.org/wiki/Atom_(web_standard)) feeds with Hugo; it was obviously high time to invest in a "proper" [RSS](https://en.wikipedia.org/wiki/RSS) feed with iTunes tags.

Hugo can build RSS feeds, but I wanted a generic mechanism that would allow me to create feeds from multiple blog post categories. After fighting with Hugo's *Output Formats*[^GH] for a while, I managed to create Atom and RSS feeds with the content I wanted, but they looked awful.

[^GH]: And figuring out ChatGPT hallucinations 🤷‍♂️

Next step: figuring out Hugo's [whitespace trimming](https://gohugo.io/templates/introduction/#whitespace), [HTML escaping](https://gohugo.io/functions/transform/htmlescape/) (the default HTML escaping does not result in valid XML), [content truncating](https://gohugo.io/functions/strings/truncate/) (iTunes subtitles should not be longer than 250 characters), and [converting HTML into plain text](https://gohugo.io/functions/transform/plainify/) (iTunes tags should not contain HTML). If anyone needs the results of trying out random stuff together for hours, they can find them on GitHub ([Atom](https://github.com/ipspace/blog/blob/master/layouts/feeds/list.atom.xml), [RSS](https://github.com/ipspace/blog/blob/master/layouts/feeds/list.rss.xml)).

I thought I was done, but then I noticed that the main *blog posts* feed starts with a blog post from 2022. I had to go through another round of fixing/cleaning up (results: [Atom](https://github.com/ipspace/blog/blob/master/themes/ipspace/layouts/_default/list.atom.xml), [RSS](https://github.com/ipspace/blog/blob/master/themes/ipspace/layouts/_default/list.rss.xml)). The Atom template is almost identical to the podcast template, but uses a different mechanism to collect the relevant pages; the RSS template does not have the iTunes tags.

I wanted to check the new *blog posts* feeds, so I opened my Feedly web page and checked the URL it (supposedly) uses for the ipSpace.net blog posts feed. It was an ancient URL that no longer worked (I have no idea how they get the new posts, but they do 🤷‍♂️). Just in case someone else is using that same URL, I figured out how to [implement redirects with Cloudflare Pages](https://developers.cloudflare.com/pages/configuration/redirects/) and redirected the Blogger-style feed URLs (yes, some of that stuff is going back more than a decade) to the new feeds.

After spending so much time cleaning up the feeds, I decided to fix another related annoyance. Ages ago (before the AI scrapers started to DDoS the small sites), I implemented a small script that I used to filter/munge my feeds. That script was pretty slow (fetching actual feed content from elsewhere), and multiple instances running in parallel often bogged down my content web server. With the changes to the feeds system, the script was no longer adding value, so I spent another hour or so trying to remember how [Apache RewriteRules](https://httpd.apache.org/docs/current/mod/mod_rewrite.html) work. In the end, I managed to implement permanent redirects for all valid feed URLs pointing to the static Hugo feeds.

**End result:** After a day of [yak shaving](https://en.wiktionary.org/wiki/yak_shaving), Hugo generates all ipSpace.net feeds whenever I publish a new blog post. They are (like all my Hugo-generated content) in static files hosted on Cloudflare Pages and thus pretty fast to fetch. Now go and update those old URLs, would you?
