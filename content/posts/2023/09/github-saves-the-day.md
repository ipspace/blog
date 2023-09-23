---
title: "How GitHub Saved My Day"
date: 2023-09-28 06:53:00
tags: [ worth reading ]
pre_scroll: True
---
I always tell networking engineers who aspire to be more than VLAN-munging CLI jockeys to get fluent with Git. I should also be telling them that while doing local version control is the right thing to do, you should always have backups (in this case, a remote repository).

I'm eating my own dog food[^DC] -- I'm using a half dozen Git repositories in ipSpace.net production[^OTH]. If they break, my blog stops working, and I cannot publish new documents[^STUFF].

[^DC]: Or maybe I should say "drinking my own champagne". It sounds so much better.  

[^OTH]: Plus another dozen for open-source tools, examples, and labs.

[^STUFF]: I'm positive there's a bunch of other stuff that breaks, but fortunately, I didn't have to investigate that.

Now for a fun fact: Git is not transactionally consistent.
<!--more-->
If your machine crashes while Git is doing its stuff, you'll get a major headache. I learned that the hard way: AWS restarted my server instance, and all repositories that are continuously touched as part of various CI/CD pipelines or cron jobs got corrupted.

Next: Git could benefit from slightly better error messages. This is what I got:

```
fatal: not a git repository (or any of the parent directories): .git
```

Weird, as I had the `.git` subdirectory in the right place. A frantic consultation with Google quickly produced a nice article explaining that I could be facing a corrupt `.git/HEAD` file. Fixed that, Git stopped complaining, but its internal data structures were still broken. My precious repositories were corrupted beyond salvation.

I told you to use remote repositories, right? Here's how they came in handy:

-   I hope you have documentation listing the URLs of the remote repositories for every Git repository you work with. I know where mine is -- somewhere in the bowels of my infrastructure-as-code files. Not exactly the best place to look at when you're in near-panic. Fortunately, after I fixed the `.git/HEAD` file **git remote** command produced useful output.
-   I used the results of the **git remote** command to clone a sane copy of each repository into a new directory adjacent to the original one.
-   Two renames later, I was back in business.

Lessons learned:

-   Backups are important. Use remote repositories, even if they're just different folders on a shared file system.
-   For every Git repository you use, have the up-to-date printout of **git remote** in an easily accessible place. Your future self will be grateful.

Finally, if you love Linux commands that look like line noise, here's the one-liner that will print all Git repositories found within a directory tree, and their remote repositories.

```
find 2>/dev/null . -name '.git' -exec dirname '{}' \; -execdir git remote -v \; -exec echo \;
```  

Here's what I got when I executed it somewhere on my laptop:

```
./EmailAssistant
origin	git@github.com:ipspace/ai-email-assistant.git (fetch)
origin	git@github.com:ipspace/ai-email-assistant.git (push)

./Hiking
github	git@github.com:ipspace/sloveniahiking.git (fetch)
github	git@github.com:ipspace/sloveniahiking.git (push)
```
