---
date: 2020-03-22 10:13:00
title: ipSpace.net Blog Now Runs on Hugo
---

Years ago I figured out that I'd eventually have to migrate my blog from Blogger to something more independent, and based on my previous experience with Wordpress I wasn't exactly enthusiastic to go down that path.

In 2015 I've [seen Scott Lowe going from Wordpress to Jekyll](https://blog.scottlowe.org/2015/01/05/blog-migration-complete/) and [then to Hugo](https://blog.scottlowe.org/2017/09/18/some-qa-about-migration-hugo/), and decided it might make sense to recreate ipSpace.net blog with a tool that generates static web pages... but never found the time to do it.
<!--more-->
Fast forward to early spring 2020. On March 12th we were [effectively told to stay at home](https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Slovenia#Timeline) with more rigorous measures eventually put in place to contain morons who didn't get the memo, and I decided to resurface that old project. A week later the ipSpace.net blog is generated with Hugo and hosted as a set of static web pages.

Some functionality is still missing, notably:

* Popular posts
* Adding new comments

Unfortunately I don't see the quarantine lifted any time soon, so they might be done sooner than I would prefer...

Even though I tried to test the setup as much as possible, there might be other broken bits and pieces. If you find them, please [contact me](https://www.ipspace.net/Contact#Fan) (for obvious reasons you can't write a comment ;).

#### Already fixed

Of course I missed a few things (or thought they could wait for a bit longer). Here are the fixes already put in place since the blog post was published:

* Atom and RSS feeds work (had to change the URLs, but that shouldn't impact you if you used feed.ipspace.net URL in your RSS reader)
* Replaced links to ioshints.blogspot.com and blog.ioshints.into. It's so nice when you could write a script that traverses the whole directory tree and fixes stuff ;)
* Replaced links to category pages in blog posts
* After being annoyed for years, I finally managed to unify tag capitalization (yes, I'm aware this is textbook OCD behavior, but it felt so good ;)

## In case you want to know more...

It wasn't exactly an easy journey. Being of a slightly masochistic persuasion I used Python (instead of Perl) to develop all the glue I needed, including:

* Converting Blogger XML dump into Hugo posts;
* Fetching all Blogger images referred to in various blog posts into the same Git repository and updating the HTML markup on the fly (hint: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is a great tool)
* Salvage all comments you made in the last 14 years from Blogger XML dump and save them into JSON format

Next step: figuring out Hugo. I wanted to retain the existing web page format, so I had to start by creating my own Hugo theme, and learned more about Go templating than I ever wanted... and then hit the performance roadblocks. Creating _blog archive_ and _popular tags_ sidebars in Hugo took forever (as Hugo had to generate them for every single blog post). Time for more glue - a script that traverses all blog posts and generates:

* Stub pages for monthly and yearly archives;
* Sidebar HTML markup pointing to monthly and yearly archives
* List of recently-used tags and all other tags.

After fixing the sidebar performance, it was time to include existing comments into the blog posts. Dumping 15.000 comments into a single JSON file didn't seem like a good idea. Creating 4.000 JSON files and have Hugo read them all would probably be even worse. In the end, I solved the dilemma with yet another script that reads per-post comments in JSON format and creates corresponding HTML markup which is then easily included into blog posts with Hugo's **readfile** functionality.

Final touches:

* CI/CD configuration that recreates and republishes the whole blog on every change in the **publish** branch;
* A script that merges **master** branch into **publish** branch, and recreates the comments and sidebar markup. That script is run every few minutes, and as a nice side effect triggers publishing of blog posts that have **date** set into the future.
