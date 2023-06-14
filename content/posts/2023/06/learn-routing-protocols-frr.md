---
title: "Use FRR to Learn Routing Protocol Fundamentals"
date: 2023-06-29 06:42:00
tags: [ BGP, netlab ]
netlab_tag: use
draft: True
---
This is why you should use FRR 
<!--more-->
```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi       1.0Gi        16Gi        19Mi        44Gi        60Gi
Swap:          8.0Gi          0B       8.0Gi
```

FRR:

```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi       1.2Gi        16Gi        20Mi        44Gi        59Gi
Swap:          8.0Gi          0B       8.0Gi
```

real	0m22.131s

Cumulus:

```
free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi       2.6Gi        11Gi       468Mi        47Gi        58Gi
Swap:          8.0Gi          0B       8.0Gi
```

real	1m42.365s

Arista:

```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi        11Gi       4.8Gi       961Mi        45Gi        48Gi
Swap:          8.0Gi          0B       8.0Gi
```

real 	1m31.946s

SR Linux:

```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi        12Gi       2.0Gi        29Mi        47Gi        48Gi
Swap:          8.0Gi          0B       8.0Gi
```