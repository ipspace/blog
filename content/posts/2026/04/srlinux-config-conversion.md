---
title: "SR Linux Configuration Conversion Tool"
date: 2026-04-02 08:35:00+0200
tags: [ automation ]
---
A year ago, I was complaining about [SR Linux breaking its configuration data model with a new software release](https://blog.ipspace.net/2025/04/api-data-model-contract/). At that time, I was promised it would only happen once a year, and, like clockwork, that moment arrived with the SR Linux release 26.03.

However, this year [Miguel Redondo](https://www.linkedin.com/in/michelredondo/) fixed the netlab SR Linux configuration templates ([VRF export policies](https://github.com/ipspace/netlab/pull/3232), [LocPref routing policy changes](https://github.com/ipspace/netlab/pull/3235)) before I could even start looking at them, and [Roman Dodin](https://www.linkedin.com/in/rdodin/) released a [tool](https://github.com/srl-labs/srlconv) that tells you exactly what changed between software releases and how to fix it.
<!--more-->
Like it's so often the case in IT (and everywhere else), that tool is standing on the shoulders of giants (and tons of right decisions Nokia made in the past):

* Like any other decent network operating system, SR Linux can convert configurations when upgrading to a new software release[^CTP].
* Unlike most network operating systems, SR Linux container images are available for a hassle-free download, making it trivial to start any SR Linux release.
* Containerlab can start containers, specify startup configurations for most supported devices, and save the current configurations for true containers.
* SR Linux is willing to work with imaginary interfaces (for most network devices, you'd have to start the containers with just the right number of interfaces)

[^CTP]: Life would be much easier if they were to make the conversion tool public, but I guess that's stretching the wish list a bit too far.

The "configuration conversion" job is thus as easy as:

* Start two SR Linux containers with the specified software releases and the same startup configuration
* Save the current configurations. At least one of them will probably be converted to a different data model.
* Give the user options to do all sorts of diffs

Assuming you have integration tests that cover every feature you use in the device configuration templates (you have them, right?), coping with a changed data model becomes reasonable:

* Run the tests, note the failures
* For every failed test, run the configuration conversion tool, find the changes in the data model, and fix the configuration templates
* Lather, rinse, repeat

If you're brave enough (and have enough tokens and the right setup), you could even ask an AI model to do it for you.

While I still hate frivolous changes in data models made mostly for aesthetic purity, knowing that vendor engineers care enough about open-source developers to make their lives easier takes a lot of that annoyance away. If only there were more vendors like Nokia...

