---
kb_section: DockerSvc
minimal_sidebar: true
title: Docker Userland Proxy
url: /kb/DockerSvc/40-userland-proxy.html
---
In the [previous section](30-nat-iptables.html) we identified two scenarios where Docker cannot use **iptables** NAT rules to map a [*published* port](20-Published.html) to a container service:

* When a container connected to another Docker network tries to reach the service (Docker is blocking direct communication between Docker networks);
* When a local process tries to reach the service through loopback interface.

In both cases, Docker uses a userland (Linux process) TCP or UDP proxy. You can easily identify the proxy with **netstat** command after starting a container with a published port (we'll yet again use [our standard Flask application](10-Exposed.html)):

{{<cc>}}Userland proxy created to support a published port{{</cc>}}
```
$ docker run --rm -d --name web_1 -p 8080:80 webapp
3398eae2649a55d2b9aa11c4979a50e025c035e34227537f4f4bd91c3ba44c9f
$ netstat -lnt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address    Foreign Address   State
tcp        0      0 0.0.0.0:111      0.0.0.0:*         LISTEN
tcp        0      0 127.0.0.53:53    0.0.0.0:*         LISTEN
tcp        0      0 0.0.0.0:22       0.0.0.0:*         LISTEN
tcp6       0      0 :::111           :::*              LISTEN
tcp6       0      0 :::8080          :::*              LISTEN
tcp6       0      0 :::22            :::*              LISTEN 
```

{{<note info>}}We used these options of the **netstat** command: **-t** to limit the printout to TCP connections, **-n** to display port numbers instead of symbolic names (like *http-alt* for port 8080) and **-l** to display the listening sockets (as opposed to established sessions).{{</note>}}

When executing **netstat** as root with the **-p** option, you can also see the process connected to the socket (send-q and recv-q columns have been removed from the printout):

```
$ sudo netstat -tlnp
Active Internet connections (only servers)
Proto Local Address Foreign Address State   PID/Program name
tcp   0.0.0.0:111   0.0.0.0:*       LISTEN  448/rpcbind
tcp   127.0.0.53:53 0.0.0.0:*       LISTEN  484/systemd-resolve
tcp   0.0.0.0:22    0.0.0.0:*       LISTEN  805/sshd
tcp6  :::111        :::*            LISTEN  448/rpcbind
tcp6  :::8080       :::*            LISTEN  6413/docker-proxy
tcp6  :::22         :::*            LISTEN  805/sshd
```

{{<note info>}}Linux sockets have *[IPV6_V6ONLY](https://man7.org/linux/man-pages/man7/ipv6.7.html)* option turned off by default, allowing an IPv6 socket bound to *in6addr_any* to accept IPv6 and IPv4 connections. **docker-proxy** therefore does not need to create separate IPv4 and IPv6 sockets.{{</note>}}

It's hard to detect transient HTTP session created by **curl** or **wget**, so we'll use a slightly different approach to see the connections through **docker-proxy**:

* Start a *busybox* container connected to another Docker network
* Use **telnet** to connect to published port 8080 to give us enough time to display the established sessions
* Type 'GET /' followed by two newlines in the telnet session to get the response from the web server. 

{{<cc>}}Establishing telnet session to published container port{{</cc>}}
```
$ docker run -it --rm --network br0 busybox
/ # telnet 192.168.33.2 8080
Connected to 192.168.33.2
GET /


<b>Hostname:</b> 3398eae2649a<br/>
<b>Remote IP:</b> 172.17.0.1
```

While the telnet session is active we can use **netstat** to display the established TCP sessions, proving that the userland proxy establishes two IPv4 sessions:

* An incoming session from the *busybox* container to port 8080 on IP address 192.168.33.2
* An outgoing session from userland proxy to port 80 on our web server container. Note that the source IP address of the outgoing session matches *Remote IP* information returned by our Flask application.

{{<cc>}}TCP sessions established through the userland proxy{{</cc>}}
```
$ netstat -tn
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address     Foreign Address    State
tcp        0      0 172.17.0.1:52868  172.17.0.2:80      ESTABLISHED
tcp6       0      0 192.168.33.2:8080 192.168.99.2:38708 ESTABLISHED
```

We can repeat the test from a local process connecting to port 8080 on the loopback interface (127.0.0.1). The resulting TCP sessions are displayed in the following printout:

{{<cc>}}TCP sessions established through loopback interface{{</cc>}}
```
$ netstat -tn
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address    Foreign Address State
tcp        0      0 127.0.0.1:55058  127.0.0.1:8080  ESTABLISHED
tcp        0      0 172.17.0.1:52872 172.17.0.2:80   ESTABLISHED
tcp6       0      0 127.0.0.1:8080   127.0.0.1:55058 ESTABLISHED
```

Not surprisingly, if we bind a published port to a specific IPv4 address, that IP address appears in the list of listening sockets:

{{<cc>}}Docker proxy listening on a specific IPv4 address{{</cc>}}
```
$ docker run --rm -d --name web_2 -p 192.168.33.2:8081:80 webapp
15d5ebf7ca85fb0258386366ebf68abcc9ebc2ae2bb345ecdf10aaa1843693ad
$ netstat -tln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address     Foreign Address  State
tcp        0      0 0.0.0.0:111       0.0.0.0:*        LISTEN
tcp        0      0 192.168.33.2:8081 0.0.0.0:*        LISTEN
tcp        0      0 127.0.0.53:53     0.0.0.0:*        LISTEN
tcp        0      0 0.0.0.0:22        0.0.0.0:*        LISTEN
tcp6       0      0 :::111            :::*             LISTEN
tcp6       0      0 :::8080           :::*             LISTEN
tcp6       0      0 :::22             :::*             LISTEN
```

Docker creates a different process for each published port; you can easily verify that with either **ps -ef** (the printout has been wrapped into multiple lines) or **sudo netstat -tlnp**:

{{<cc>}}Each published port is served by another Linux process{{</cc>}}
```
$ ps -ef|grep docker-proxy
root      6413   793  0 07:59 ?  00:00:00 /usr/bin/docker-proxy 
    -proto tcp -host-ip 0.0.0.0 -host-port 8080
    -container-ip 172.17.0.2 -container-port 80
root      7613   793  0 08:28 ?  00:00:00 /usr/bin/docker-proxy 
    -proto tcp -host-ip 192.168.33.2 -host-port 8081
    -container-ip 172.17.0.3 -container-port 80
```
