---
title: "Git Tip: Use Word Diff"
date: 2020-04-19 06:20:00
tags:
---
Git is great (once you get beyond the [basic recipes](https://xkcd.com/1597/)), and I love my [new blog setup](/2020/03/ipspace-blog-runs-on-hugo/) that allows me to keep track of all the changes I make with Git.

However, there's a slight gotcha if you use Git with Markdown: whenever you change something, the whole line (and using tools like IA Writer a whole paragraph is a single line) is marked as changed, for example:
<!--more-->
{{<figure src="/2020/04/git-diff.jpg" caption="Default **git diff** printout on a Markdown change" >}} 

Git has an interesting feature for scenarios like this: the **word-diff** option that tries to compare words not lines. Using that option on a Markdown text gives you more meaningful results:

{{<figure src="/2020/04/git-word-diff.png" caption="Using **word-diff** option" >}}

We're almost there. Git has identified the part of the text that has been changed, but did not correctly identify the actual change made because it considers only whitespaces to be word delimiters, so it seems like I changed `(available` to `(parts...`.

Changing the definition of what _words_ are with **word-diff-regex** option fixes that and identifies the actual change I made to the text.

{{<figure src="/2020/04/git-word-diff-regex.jpg" caption="Changing what a word is with **word-diff-regex** option" >}}



