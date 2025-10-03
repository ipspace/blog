---
title: "Spaghetti Pasta Networking"
date: 2025-10-06 08:15:00+0200
tags: [ virtualization ]
---
Here's an interesting data point in case you ever wondered why things are getting slower, even though the CPU performance is supposedly increasing. Albert Siersema sent me a link to a [confusing implementation of spaghetti networking](https://passt.top/passt/about/).

It looks like [they're trying to solve](https://passt.top/passt/about/#motivation) the *how do I connect two containers (network namespaces) without having the privilege to create a vEth pair* challenge with plenty of ~~chewing gum and duct tape~~ tap interfaces 🤦‍♂️
