title: Conclusions
publish: 2020-09-18

A brief recap of what we discovered in this article:

* Every Docker container can start a TCP or UDP service on any port (the exception being containers using **host** network or no networking);
* The service ports SHOULD be declared as *exposed* ports in a Dockerfile, but don't have to be;
* Local processes on Docker host and all containers connected to the same Docker network can access the container services directly;
* External clients cannot access the container services directly unless the host advertises the IP prefix of the corresponding Docker network to the outside world, or if the container is using **macvlan** or **ipvlan**-based network;
* In most cases you have to *publish* a container port (map it into a host port) to offer a container service to external clients or containers connected to other Docker networks;
* Published ports can be bound to any host IP address or a specific host IP address;
* Docker uses **iptables** NAT table to perform destination port and address translation when an external client connects to a published port;
* NAT table rules do not match local processes connecting to loopback interface, or Docker containers running on the same host. In these cases Docker uses a **docker-proxy** process - a simple TCP or UDP proxy;
* The **docker-proxy** can also be used to connect IPv6 clients to IPv4-only containers.
