---
title: "netlab: Switch to Lab Directory After an SSH Session Loss"
series_title: "Tip: Switch to Lab Directory After an SSH Session Loss"
date: 2026-03-23 08:31:00+0100
lastmod: 2025-10-13 09:17:00+02:00
tags: [ netlab ]
netlab_tag: guidelines
---
I work on a laptop that loves to power down when not used (the right thing to do), which often breaks the SSH session to my netlab server (not so good). 

Reconnecting is trivial. Figuring out *which lab I was working on* and *where it lives on the disk* after a few hours? That’s the annoying part.

We solved most of that ages ago with the `netlab status --all` [command](https://netlab.tools/netlab/status/). It shows all running labs[^ALL] and their directories, so you can quickly jump back to where you were. However, even that gets tedious the 100th time you have to do it.
<!--more-->
[^ALL]: At least in single-user environments ;)

{{<cc>}}Typical **netlab status --all** printout{{</cc>}}
{{<ascii>}}
$ netlab status --all
Active lab instance(s)

┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┓
┃ id      ┃ directory                 ┃ status  ┃ providers ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━┩
│ default │ /home/user/net101/tools/X │ started │ clab      │
└─────────┴───────────────────────────┴─────────┴───────────┘
{{</ascii>}}

We added the `--format json` **[netlab status](https://netlab.tools/netlab/status/)** option in [release 26.02](https://netlab.tools/release/26.02/#release-26-02), so it should be pretty easy to extract the lab directory from the **netlab status** printout and use some **bash** trickery to switch to that directory, right?

Here's how I got it to work:

* The `netlab status -i default --format json` command displays the information about the **default** lab instance (I'm not using the [multilab plugin](https://netlab.tools/plugins/multilab/) for interactive work), for example:

```
$ netlab status -i default --format json
{
  "dir": "/home/user/net101/tools/X",
  "providers": [
    "clab"
  ],
  "log_line": "OK: netlab initial --no-message --deploy",
  "log": [
    "2026-03-17T11:50:07.482878+00:00: OK: containerlab version",
    "2026-03-17T11:50:07.496125+00:00: OK: bash -c [[ `containerlab version|awk '/version/ {print $2}'` > '0.71.999' ]] && echo OK",
    "2026-03-17T11:50:07.519617+00:00: OK: docker image ls --format json ceos:4.35.2F",
    "2026-03-17T11:50:07.521972+00:00: restarting lab",
...
```

* We can use **[jq](https://jqlang.org/)** to extract the **dir** value (the lab directory) from the printout:

```
$ netlab status -i default --format json | jq .dir
"/home/user/net101/tools/X"
```

* Using the `-r` **jq** option gets rid of the quotes:

```
$ netlab status -i default --format json | jq .dir -r
/home/user/net101/tools/X
```

* Using the results of that pipe as an argument to **cd** is exactly what we need:

```
$ cd $(netlab status -i default --format json | jq .dir -r)
```

* However, that's clumsy, so let's define an alias:

```
$ alias goback="cd $(netlab status -i default --format json | jq .dir -r)"
```

* After storing that alias in **.bash_aliases** script (or wherever your preferred shell keeps them), you can log in, execute **goback**, and you're ready to work.

What's not to love in the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) ;)
