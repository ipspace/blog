---
index: true
index_title: Docker Networking for Container-Based Services
kb_section: DockerSvc
minimal_sidebar: true
title: Starting Container-Based Services
toc_title: Overview
url: /kb/DockerSvc/index.html
---
One of the most common container use cases is providing services to other parts of application stack (probably running in other containers) or to external users. While it's extremely easy to set up container-based servers (and most open-source products now include a container-based version), the networking aspects of container services can get intriguingly tricky, as you'll find out in this article.

## Starting Services in Docker Containers

Starting services in Docker containers is as simple as:

* Find the software you're interested in on Docker Hub
* Download the Docker image
* Start a container.

For example, you can start Apache HTTP server with a single command:

```
$ docker run --name web -d httpd
Unable to find image 'httpd:latest' locally
latest: Pulling from library/httpd
8559a31e96f4: Pull complete
bd517d441028: Pull complete
f67007e59c3c: Pull complete
83c578481926: Pull complete
f3cbcb88690d: Pull complete
Digest: sha256:387f896f9b6867c7fa543f7d1a...
Status: Downloaded newer image for httpd:latest
5cc2cded1e38ea265f5c38c06f03a94d45754a588...
```

The container started with the above command is connected to the default Docker bridge and gets an IP address from the IP prefix assigned to **docker0** interface (default: 172.17.0.0/16).

You can check the IP prefix assigned to **docker0** with the following command:

```
$ ip address show dev docker0
4: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc...
    link/ether 02:42:70:ac:28:4a brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:70ff:feac:284a/64 scope link
       valid_lft forever preferred_lft forever
```

It's a bit harder to get the IP address assigned to a running container; you have to use **docker inspect *[name|id]*** command to display it. That command returns tons of JSON-formatted data, but fortunately includes a **format** parameter that allows you to extract just the data you need, for example:

```
$ docker inspect -f '{{range .NetworkSettings.Networks}}
  {{.IPAddress}}{{end}}' web
172.17.0.2
```

INFO: You could also use **jq** to filter the JSON data structures returned by various **docker** commands.

## Using Container-Based Services

Connecting to HTTP port on 172.17.0.2 (IP address of our **web** container) returns the expected result:

```
$ curl http://172.17.0.2
<html><body><h1>It works!</h1></body></html>
```

It seems almost too good to be true... and it is. We have just a tiny problem to solve: while you can always connect to a Docker container from the host running it, the IP address of the Docker container is usually not accessible from the outside network.

You can solve that problem in one of three ways:

* Connect Docker container directly to the external network using **macvlan** or **ipvlan** drivers;
* Advertise the IP prefix assigned to the Docker bridge to the outside world (Calico uses a similar approach);
* Use *published* ports to map a container port into a port bound to a Docker host IP address.

In the rest of this article we'll focus on *published ports* but before going there, we'll do a brief detour into *exposed ports*.
