---
title: "Blogging Rule#1: Own Your Content"
date: 2021-04-29 07:28:00
tags: [ worth reading ]
---
During my [interview with David Bombal](/2021/03/interview-is-networking-dead.html) I made a recommendation I find crucial for anyone serious about blogging:

> Make sure you own your content.

There's a simple reason for that rule: if you want to write quality content, you'll have to invest a lot of time into it. 
<!--more-->
You don't want your hard work to disappear when a popular social media platform goes kaboom, is acquired and revamped beyond recognition, or locks your content behind an annoywall/regwall/paywall (I'm looking at you Medium) to milk its residual value.

The only way to make sure that won't happen is to own your content, publish it under your own domain (total cost: about two Frappucinos per year, or one if you happen to be at Zurich Airport), and host it on a flexible platform that allows you to quickly move it. That effectively rules out all social media platforms and many hosted Wordpress solutions (remember: I did say "*quickly*").

I found static site generators integrated with Git to offer just the right mix of functionality and flexibility. I'm using [Hugo](/2020/03/ipspace-blog-runs-on-hugo.html); [here are a few more ideas](https://developers.cloudflare.com/pages/how-to).

As I have the source code for my blog (and a [hobby web site](https://sloveniahiking.rocks/)) in Git, I could save it to any hosted Git platform (GitHub, GitLab, ...) and move it around in minutes. I could generate the HTML code locally, use CI/CD pipeline offered for free by most hosted Git sites, or use a dedicated platform like Netlify.

I could also publish HTML pages to any public cloud. AWS S3 comes to mind; you could also go for Oracle Cloud if your site is popular enough to care about transfer fees (just make sure you read all the fine print -- they are known for their [excellent legal teams](https://palisadecompliance.com/oracle-org-chart/)).
 
Finally, I could use recently launched CloudFlare Pages and deploy my content in CloudFlare CDN, and that's exactly what I did when I got sick-and-tired of constant GitLab outages. It took me literally five minutes to move [one of my web sites](https://sloveniahiking.rocks/) to CloudFlare pages, including figuring out CloudFlare settings to make Hugo work, and changing the DNS records.

Does that mean you shouldn't publish stuff on Facebook or LinkedIn? Of course not. Publish the content on your own site, and add a short post pointing to it to as many social media platforms as you wish. Let them be at least marginally useful ;)
