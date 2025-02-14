---
title: "Limit the Scope of Git Diff"
date: 2025-02-17 07:41:00+0100
tags: [ worth reading ]
---
The [results](https://tests.netlab.tools/) of [_netlab_ integration tests](https://github.com/ipspace/netlab/tree/dev/tests/integration) are stored in [YAML files](https://github.com/ipspace/netlab/tree/integration_tests), making it easy to track ~~changes~~ [improvements with Git](https://github.com/ipspace/netlab/commits/integration_tests/). However, once I added the _time of test_ and _netlab version_ to the test results, I could no longer use **git diff** to figure out which test results changed after a test run -- everything changed.

For example, these are partial test results from the OSPFv2 tests:

```
$ cat frr/clab/ospf/ospfv2/results.yaml
01-network:
  _timestamp: '2025-02-14 09:21:47'
  _version: 1.9.4-post2
  config: true
  create: true
  up: true
  validate: true
02-areas:
  _timestamp: '2025-02-14 09:22:11'
  _version: 1.9.4-post2
  config: true
  create: true
  up: true
  validate: true
...
```

After running the tests with FRR version 10.2.1, I wanted to check whether any of the tests that previously worked failed with the new version. **git diff** wasn't of much use as every single test had (at least) a different timestamp:

```
$ git diff **/ospf/**/*yaml
diff --git a/frr/clab/ospf/ospfv2/results.yaml b/frr/clab/ospf/ospfv2/results.yaml
index 3b5b00fb8..47cf36480 100644
--- a/frr/clab/ospf/ospfv2/results.yaml
+++ b/frr/clab/ospf/ospfv2/results.yaml
@@ -1,94 +1,94 @@
 01-network:
-  _timestamp: '2025-01-24 22:49:25'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:21:47'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
 02-areas:
-  _timestamp: '2025-01-24 22:49:42'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:22:11'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
```

I knew there must be a weird Git nerd knob that would limit the **git diff**, and of course there is [the `-G` flag](https://git-scm.com/docs/git-diff). It specifies a regular expression that is used to select *interesting* diffs.

All I had to do was to use `git diff **/*yaml '-Gtrue|false'`[^ER] and I got changes from all files where a line containing **true** or **false** changed. Unfortunately, **git diff** still displays _all_ changes in that file. For example, the BGP local preference test failed, but I got the printout of changes in all BGP policy tests:

[^ER]: Explanation for the need of quotes around the `-G` flag is left as an exercise for the reader.

```
$ git diff '-Gtrue|false' **/*yaml
diff --git a/frr/clab/bgp.policy/results.yaml b/frr/clab/bgp.policy/results.yaml
index 4571dc663..2f92ca794 100644
--- a/frr/clab/bgp.policy/results.yaml
+++ b/frr/clab/bgp.policy/results.yaml
@@ -1,66 +1,66 @@
 10-bgp-bandwidth-auto:
-  _timestamp: '2025-01-24 23:09:02'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:41:27'
+  _version: 1.9.4-post2
   create: false
 11-bgp-bandwidth-value:
-  _timestamp: '2025-01-24 23:09:31'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:41:51'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
 12-bgp-bandwidth-value-out:
-  _timestamp: '2025-01-24 23:10:02'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:42:17'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
 21-locpref:
-  _timestamp: '2025-01-25 11:23:48'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:42:49'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
-  validate: true
+  validate: false
 22-locpref-unnumbered:
-  _timestamp: '2025-01-25 11:24:22'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:43:27'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
 31-med:
-  _timestamp: '2025-01-24 23:11:28'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:43:39'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
 32-med-unnumbered:
-  _timestamp: '2025-01-24 23:11:40'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:43:51'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
 41-prepend:
-  _timestamp: '2025-01-24 23:11:52'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:44:03'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
 42-prepend-unnumbered:
-  _timestamp: '2025-01-24 23:12:05'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:44:15'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
   validate: true
 51-weight:
-  _timestamp: '2025-01-24 23:12:42'
-  _version: 1.9.4
+  _timestamp: '2025-02-14 09:44:43'
+  _version: 1.9.4-post2
   config: true
   create: true
   up: true
```

However, while that's annoying, at least I can limit the display to the test suites in which at least one test failed with the **--name-only** parameter:

```
$ git diff '-Gtrue|false' --name-only **/*yaml
frr/clab/evpn/results.yaml
frr/clab/isis/results.yaml
frr/clab/routing/results.yaml
```

Next step: figure out what changed between FRR release 10.0.1 (used in _netlab_ release 1.9.4) and 10.2.1 (the latest FRR release) and fix the configuration templates.
