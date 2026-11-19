---
title: "Hint: Grab the vJunos Images If You Need Them"
date: 2026-11-20 08:29:00+0100
tags: [  ]
---
HPE Marketing (I'm guessing ;) decided to redirect the `juniper.net` domain to `hpe.com`. No big deal if done right. It wasn't.

The first sign of trouble was the [broken](https://blog.ipspace.net/2026/09/srv6-junos/#3082) `community.juniper.net` website, where all pages redirected to the first page of `community.networking.hpe.com`. Fortunately, they fixed that one.

Yesterday, I wanted to download the new version of the vJunos-switch image, and the "Free Virtual Junos OS Downloads" URL that's still at the top of Google search results shows an HPE-branded 404 page on the `juniper.net` website (archive.org still has the [original page](https://web.archive.org/web/20260811092858/https://www.juniper.net/us/en/dm/vjunos-labs.html)).

Fortunately, `support.juniper.net` still works, and the *image download* links published (for example) in [containerlab.dev documentation](https://containerlab.dev/manual/kinds/vr-vjunosswitch/) still work. However, who knows when that will break; grab the images to have them handy ;)
