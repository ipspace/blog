---
title: "Molly-Guard: a Lifesaver on a Ubuntu Server"
date: 2025-07-02 08:18:00+0200
tags: [  ]
---
Have you ever managed to type **reload** in the wrong terminal window and brought down a core switch (I probably did)? I managed to do the Ubuntu equivalent of that stupidity: I told my main Ubuntu server to **sudo poweroff** instead of doing that to a Vagrant VM.

Fortunately, the open-source world doesn't have to rely on the roadmaps created by networking vendors' product managers; if there's a big enough pain, someone will solve it.
<!--more-->
It took me seconds to find the **molly-guard**[^MG] Ubuntu package. It [intercepts all reboot-related commands](https://manpages.ubuntu.com/manpages/focal/man8/molly-guard.8.html), checks whether you're on an SSH session, and asks for the hostname you want to reboot/power off:

```
$ sudo poweroff
W: molly-guard: SSH session detected!
Please type in hostname of the machine to poweroff: ^C
Good thing I asked; I won't poweroff brick2 ...
```

We've been rebooting the wrong Cisco IOS boxes for decades, and they still lack an equivalent mechanism. Even worse, I don't remember ever seeing a reboot molly-guard on a networking device[^TAC]. Have I missed something? Please leave a comment.

[^MG]: Thanks to [Wiktionary](https://en.wiktionary.org/wiki/molly-guard), we know who Molly was and what she did.

[^TAC]: Yeah, I know I could use EEM or TACACS+ and check the **reason**, but hey, come on!