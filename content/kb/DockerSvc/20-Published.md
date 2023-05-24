title: Published Ports
publish: 2020-08-28

As mentioned in the [overview](index.html) part of this article, the default Docker networking implementation makes it hard to reach a service running in a container from an external client; the usual solution is to *publish* a container port (map a container port into a port on the Docker host).

INFO: Other containers connected to the same Docker network can reach container services without additional configuration - unless configured otherwise Docker does not limit intra-network communication.

## Publishing a Container Port

You can publish a container port when starting the container, for example with the **-p** parameter of the **docker run** command. It's impossible to publish a port once the container is running.

Although it's recommended for documentation purposes, a published container port does not have to be listed as an *exposed* port. For example, using our [Flask application](10-Exposed.html) it's perfectly OK to map container port 80 into host port 8080 even though the container port 80 is not declared as an exposed port.

```
$ docker run --rm -d --name flask -p 8080:80 webapp:noexpose
59e3bfe14b3af8399c278e97e97da48c4cb5b95294989b9b5ba1300dd48b49d0
$ docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
NAMES               IMAGE               PORTS
flask               webapp:noexpose     0.0.0.0:8080->80/tcp
$ curl http://127.0.0.1:8080/
<b>Hostname:</b> 59e3bfe14b3a<br/>
<b>Remote IP:</b> 172.17.0.1
```
CAPTION: Publishing container port 80 to host port 8080

INFO: Please note that the **docker ps** command lists host-to-container port mapping even though the container port 80 was not declared as an exposed port.

The simple version of the **docker run -p** command binds the published port to all IP addresses available on the Docker host (as indicated by 0.0.0.0:8080 listing in the above printout). The web server running in the container can thus be reached from any IP address configured on the Docker host, including the IP address assigned to the **docker0** interface.

The following IP addresses are configured on the Docker host running our Flask application:

```
$ ip address show dev docker0
4: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500...
    link/ether 02:42:70:ac:28:4a brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:70ff:feac:284a/64 scope link
       valid_lft forever preferred_lft forever
$ ip address show dev eth1
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500...
    link/ether 08:00:27:9b:8a:66 brd ff:ff:ff:ff:ff:ff
    inet 192.168.33.2/24 brd 192.168.33.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe9b:8a66/64 scope link
       valid_lft forever preferred_lft forever
```
CAPTION: IP addresses configured on the Docker host

When trying to reach the Flask application through various IP addresses available on the Docker host the source IP address used by the HTTP client (as reported by the Flask web server) matches the IP address of the interface through which we tried to reach the published port... apart from the loopback case (the reasoning behind that decision is left as an exercise for the reader).

```
$ curl http://172.17.0.1:8080/
<b>Hostname:</b> 59e3bfe14b3a<br/>
<b>Remote IP:</b> 172.17.0.1
$ curl http://192.168.33.2:8080/
<b>Hostname:</b> 59e3bfe14b3a<br/>
<b>Remote IP:</b> 192.168.33.2
$ curl http://127.0.0.1:8080/
<b>Hostname:</b> 59e3bfe14b3a<br/>
<b>Remote IP:</b> 172.17.0.1
```
CAPTION: Client IP address depends on the target address used

## Limiting Host IP Addresses Binding for Published Ports

It's also possible to limit the published port to a single host IP address, for example:

```
$ docker run --rm -d --name flask -p 192.168.33.2:8080:80 webapp:noexpose
e399c2be07f9232c59866cac58bebe80da1ac17f8609cd3c4db399f4578a4869
$ docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
NAMES    IMAGE               PORTS
flask    webapp:noexpose     192.168.33.2:8080->80/tcp
```
CAPTION: Publishing container port 80 to port 8080 on eth1 interface

The Flask application can now be reached directly (on port 80) or through IP address 192.168.33.2 on port 8080. Other host IP addresses can no longer be used to reach the container service:

```
$ curl http://192.168.33.2:8080/
<b>Hostname:</b> e399c2be07f9<br/>
<b>Remote IP:</b> 192.168.33.2
$ curl http://172.17.0.1:8080/
curl: (7) Failed to connect to 172.17.0.1 port 8080: Connection refused
$ curl http://127.0.0.1:8080/
curl: (7) Failed to connect to 127.0.0.1 port 8080: Connection refused
```

Finally, when trying to reach the Flask application from an external client, the application correctly reports the client IP address, indicating that Docker probably destination NAT rules instead of a TCP/UDP proxy when publishing a port.

```
worker1:~$ ip address show dev eth1
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500...
    link/ether 08:00:27:66:ac:c2 brd ff:ff:ff:ff:ff:ff
    inet 192.168.33.3/24 brd 192.168.33.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe66:acc2/64 scope link
       valid_lft forever preferred_lft forever
worker1:~$ curl http://192.168.33.2:8080/
<b>Hostname:</b> e399c2be07f9<br/>
<b>Remote IP:</b> 192.168.33.3
```
CAPTION: Accessing Flask application from another Linux host

In the next part of this article we'll explore how Docker uses NAT **iptables** rules to implement port publishing.

