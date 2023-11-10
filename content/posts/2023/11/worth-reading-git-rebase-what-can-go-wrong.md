---
title: "Git Rebase: What Can Go Wrong?"
date: 2023-11-11 09:03:00
tags: [ worth reading ]
---
Julia Evans wrote another must-read article (if you're using Git): [git rebase: what can go wrong?](https://jvns.ca/blog/2023/11/06/rebasing-what-can-go-wrong-/)

I often use **git rebase** to clean up the commit history of a branch I want to merge into a main branch or to prepare a feature branch for a pull request. I don't want to run it unattended -- I'm always using the interactive option -- but even then, I might get into tight spots where I can only hope the results will turn out to be what I expect them to be. Always have a backup -- be it another branch or a copy of the branch you're working on in a remote repository.

