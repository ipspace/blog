---
title: "Response: CLI Is an API"
date: 2025-05-14 08:32:00+0200
tags: [ automation ]
series: cli
cli_tag: challenge
---
[Andrew Yourtchenko](https://www.linkedin.com/in/andrew-yourtchenko-9304551/) and [Dr. Tony Przygienda](https://www.linkedin.com/in/dr-tony-przygienda-018501/) left wonderful comments to my [Screen Scraping in 2025](/2025/05/screen-scraping-2025/) blog post, but unfortunately they prefer commenting on a closed platform with ephemeral content; the only way to make their thoughts available to a wider audience is by reposting them. Andrew first:

---

I keep saying CLI is an API. However, it is much simpler and an *easier* way to adapt to the changes, if these three conditions are met:
<!--more-->
1. regexes are written in a defensive, yet permissive fashion (generously ignore the spaces and lines that do not match, but make sure you ignore both spaces and tabs)
2. for the data that you *do* capture, be very conservative, such that your likely outcome if something goes awry is no data rather than garbage data.
3. handle all the parsed data as Option enum in a language which allows for that and always check whether it is Some(value) or None before using it.

The (3) you will have to do anyway even with structured API, when handling the changes. For the (1) and (2), if (in some mythical universe), vendors were to publish the regexes, it will be indistinguishable from the other transports. (I am of course leaving aside the question of data conversions, because they are equally a problem when using the “structured” APIs as well, just of a different shape.

---

Not surprisingly, Tony disagreed (probably based on his battle scars):

---

Sorry, it's largely putting lipstick on you know what. It's _impossible_ to know as a vendor what kind of "smart regexes" some customer put in that can deal with "any change" until they can't. Because whatever the "smart regex" is it is still something that does fundamentally not understand the semantic structure of the underlying output. And having dealt with some of it it's about the third circle of hell to maintain such "super smart regexes" with backtracking and whatever else not ...
