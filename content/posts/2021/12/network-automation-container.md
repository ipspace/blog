---
title: "Running Network Automation Tools in a Container"
date: 2021-12-13 07:14:00
tags: [ automation, Docker ]
---
Setting up a network automation development environment is an interesting task: 

* You have to install a half-dozen tools, each one with tons of dependencies;
* SSH libraries like *paramiko* have to installed manually;
* Ansible modules for individual network devices might need extra libraries;
* Parsing tools invoked with Ansible Jinja2 filters have to be installed separately;
* Add your pet peeve here ;)

Now imagine having to do that for a dozen networking engineers and software developers working on all sorts of semi-managed laptops. *Containers* seem to be one of the sane solutions[^CA].
<!--more-->
[^CA]: *Containers* seem to be an an answer to every challenge one might have these days (unless it's LISP or BGP).

There are just two minor hurdles between where you are and a container-based nirvana[^DCK]:

* You have to build the container
* You have to figure out how to use it.

[^DCK]: Ignoring for the moment the time it will take to get Docker running on MacOS or Windows Linux Subsystem. It usually works... until it doesn't.

## Building an Automation Container

A long while ago I put together a build recipe for a [network automation container](https://github.com/ipspace/NetOpsWorkshop/tree/master/Docker) that contains these tools and libraries[^SMALLER]:

* Git
* Ansible
* NAPALM
* netlab
* PyATS
* PyNetBox
* paramiko, netlike, textfsm, jmespath, ntc-tempaltes, ttp
* jq, yq, yamllint

[^SMALLER]: [Another recipe](https://packetpushers.net/building-a-docker-network-automation-container/) published by Jaap de Vos builds a minimalistic container with Ansible, napalm, and nornir.
  
I created a [Ubuntu-based](https://github.com/ipspace/NetOpsWorkshop/tree/master/Docker/Ubuntu) and a [Centos-based](https://github.com/ipspace/NetOpsWorkshop/tree/master/Docker/Centos) version. You can [download the containers from Docker Hub](https://hub.docker.com/r/ipspace/automation); select **ipspace/automation:ubuntu** or **ipspace/automation:centos** You can also build them yourself:

* Download the desired directory from GitHub
* Modify the *requirements\*.txt* files to select the packages you want to install
* Modify the *requirements.yml* file to select the Ansible collections you want to install
* Run **docker build**

## Running a Network Automation Container

Containers are started with **docker run** command, and if you want to have an interactive container you should add `-it` flags. You probably don't want to have a ton of expired containers lying around, so let's add `--rm` flag (remove a container after it exits). For more details, watch *[Starting, Stopping and Removing Containers](https://my.ipspace.net/bin/get/Docker101/2.1%20-%20Starting%2C%20Stopping%20and%20Removing%20Containers.mp4?doccode=Docker101)* part of *[Basic Docker Commands](https://my.ipspace.net/bin/list?id=Docker101#CLI)*

The rest of the command line is passed straight to the container -- this is how you would run **ansible-playbook**:

```
docker run -it --rm ipspace/automation:ubuntu ansible-playbook
```

The "only" problem: the container cannot access your playbooks. You have to map the directories that should be accessible to your automation tools with the `--volume` parameter, and make sure the target directory is the current (working) directory when the desired command is executed. You could set the working directory with the `-w` flag, or map the current directory into the initial working directory specified in the Dockerfile (`/ansible`) -- that's what we'll do (more details in *[Mapping Host Directories into Containers](https://my.ipspace.net/bin/get/Docker101/2.2%20-%20Mapping%20Host%20Directories%20into%20Containers.mp4?doccode=Docker101)*)

You might also want to map your home directory into the container to get default settings like `.bashrc`. The simple command we started with thus becomes:

```
docker run -it --rm \
    --volume $(pwd):/ansible \
    --volume="/home/$USER:/home/$USER" \
    ipspace/automation:ubuntu ansible-playbook
```

{{<note warn>}}As Daniel Justice pointed out in a comment, it's a terrible idea to give a container access to your home directory unless you can absolutely trust it (for example, you built it yourself).{{</note>}}

This approach works (try it out), but there's one more thing to do: programs inside the container run as *root* user and create files owned by *root* in your directories. Cleaning them up is annoying; wouldn't it be better if we could run the container as the current user? Sure, here's the final command (based on [this blog post](https://faun.pub/set-current-host-user-for-docker-container-4e521cef9ffc)):

```
docker run -it --rm \
    --user $(id -u):$(id -g) \
    --volume $(pwd):/ansible \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/home/$USER:/home/$USER" \
    ipspace/automation:ubuntu $@
```

No-one in their right might would want to use such a command on a daily basis, so I created a shortcut script (**run-automation**) in both directories. Put it somewhere in your PATH and you can do:

```
run-automation ansible-playbook...
```

Alternatively, you can create a shell function (for example in `~/.bash_profile`[^ORNOT]):

```
run-automation ()
{
docker run -it --rm \
    --user $(id -u):$(id -g) \
    --volume $(pwd):/ansible \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/home/$USER:/home/$USER" \
    ipspace/automation:ubuntu $@
}
```

[^ORNOT]: Or not. I have no idea how to set up my *nix environment properly; I know just enough to have opinions and do damage.

To make the automation container even more convenient to use, create a series of aliases (yet again, `~/.bash_profile` might be a good place to store them[^ORNOT]):

```
alias ansible-playbook='run-automation ansible-playbook'
alias ansible-galaxy='run-automation ansible-galaxy'
alias git='run-automation git'
```

**Final tip**: if you're going to execute a series of automation commands, use `run-automation bash` to start a new shell within the automation container.

For more details on building and running Docker containers, watch the _[Introduction to Docker](https://www.ipspace.net/Introduction_to_Docker)_ webinar.

## Revision History

2021-12-13
: Added a warning about giving container access to your home directory.

