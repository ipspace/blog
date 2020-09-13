---
title: "Interesting: PyEnv"
date: 2020-09-20 11:08:00
tags: [ automation ]
---
If you're like me, you're probably sick-and-tired of Python versions, environments... Every time I update Python on my MacBook Pro with Homebrew, I lose all packages I installed for the previous version of Python (because I'm installing them system-wide and they're stored in version-specific directory).

Jon Langemak [found a potential solution](http://www.dasblinkenlichten.com/python-pieces-using-pyenv/) to this problem: [PyEnv](https://github.com/pyenv/pyenv). My first reaction was: _Great, just what I need_... but as he described how it really works, I realized that _it's always possible to add another layer of indirection_. RFC1925 strikes again.