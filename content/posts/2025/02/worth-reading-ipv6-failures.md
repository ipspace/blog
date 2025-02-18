---
title: "Worth Reading: The IPv6 Agnostic Blog"
date: 2025-02-26 08:19:00+0100
tags: [ worth reading, IPv6 ]
---
Ole Troan, an excellent networking engineer working on IPv6 for decades, has decided to comment on the color of the IPv6 kettle, starting with:

* [Is the transition to IPv6 inevitable?](https://ipv6.hanazo.no/posts/ipv6-transition-inevitable/) (hint: [Betteridge's law of headlines](https://en.wikipedia.org/wiki/Betteridge%27s_law_of_headlines))
* [The mistakes and missed opportunities in the design of IPv6 - episode 1](https://ipv6.hanazo.no/posts/ipv6-missed-opportunities-1/) (aka [Second System Effect](https://en.wikipedia.org/wiki/Second-system_effect)[^WK])

I'm pretty sure Ole won't stop there, so stay tuned.
<!--more-->
[^WK]: I love that Wikipedia authors used IPv6 deployment as an example of second-system effect.

### Behind the Scenes

Ole initially published his articles on Medium, so I sent him a polite email asking whether he could move them to a platform with somewhat less blatantly aggressive in-your-face monetization attempts. He quickly responded and asked for ideas, and one of my suggestions was the Hugo/GitHub/CloudFlare Pages pipeline I'm using.

A day later, I received another email from him, asking a rhetorical question: "How can we make self-hosting of anything easier?" His Hugo-built website was up and running on a Linode S3 bucket.

If you want to do something similar:

* Read the [Linode Hugo tutorial](https://www.linode.com/docs/guides/host-static-site-object-storage/)
* Explore [Hugo hosting and deployment options](https://gohugo.io/hosting-and-deployment/)
* Cloudflare Pages might be an [interesting hosting option](https://developers.cloudflare.com/pages/framework-guides/deploy-a-hugo-site/) that I'm using for all my projects. They handle domain registration, TLS termination, website deployment, and global hosting for you. Another free alternative is [GitHub Pages](https://gohugo.io/hosting-and-deployment/hosting-on-github/).

However, never forget that "_perfect is the enemy of published_." It took a friend of mine forever to set up his Hugo web site because (in his own words):

> I tried to run it locally and applied some templates, and it went... well, until I felt the urge to "improve it". Perfection is the mother of all disgraces. It all went down from there.

He got his site up and running in the meantime, but probably spent way too much time on irrelevant details (trust me, I've been there).