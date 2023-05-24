title: Exposed Ports
publish: 2020-08-28

Any Docker container (assuming default Docker settings) can start a TCP or UDP service on any port. After all, the top process in every container runs as root, and every container gets its own IP address and TCP/IP stack (network namespace).

It's good form to document the ports a container listens on using the **EXPOSE** command in Dockerfile (the file used to build a Docker container image), but the container-based services work even without that.

Let's use the [following Dockerfile](https://github.com/ipspace/docker-examples/blob/master/app/websvc/Dockerfile.noexpose) to build a Docker container running a Python [Flask application listening on TCP port 80](https://github.com/ipspace/docker-examples/tree/master/app/websvc). The application returns the container ID (useful when testing Docker Swarm environment) and the IP address of the HTTP client (useful when trying to figure out the convoluted setup Docker uses to implement published ports).

```
FROM python:2.7-slim
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

After staring the container it's possible to access the Flask application even though the container image exposed no TCP or UDP ports:

```
$ docker run --rm -d --name flask webapp:noexpose
f9dc192442ee55f054ba167e730b15ebadc0f635630d8f6e886aae650c1d3329
$ docker inspect -f '{{range .NetworkSettings.Networks}}
>   {{.IPAddress}}{{end}}' flask
  172.17.0.3
$ curl http://172.17.0.3/
<b>Hostname:</b> f9dc192442ee<br/>
<b>Remote IP:</b> 172.17.0.1
```

The only difference you'll notice between a container exposing its ports and a container lacking that decency is the list of ports in **docker ps** printout (shortened to fit into the page width):

```
$ docker ps
CONTAINER ID  IMAGE           COMMAND            PORTS   NAMES
f9dc192442ee  webapp:noexpose "python app.py"            flask
5cc2cded1e38  httpd           "httpd-foreground" 80/tcp  web
```

You can also use a *format string* in **docker ps** command to list a subset of usually-displayed information:

```
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Ports}}"
CONTAINER ID    IMAGE               NAMES               PORTS
f9dc192442ee    webapp:noexpose     flask
5cc2cded1e38    httpd               web                 80/tcp
```

Now that you know what *exposed* ports are, we're ready do dive into the concept of *published* ports.
