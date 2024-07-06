---
date: 2017-10-12 10:38:00+02:00
tags:
- automation
- Ansible
title: Turn Your Ansible Playbook into a Bash Command
url: /2017/10/turn-your-ansible-playbook-into-bash.html
lastmod: 2022-02-17 16:27:00
---
In [one of the previous blog posts](/2017/09/collect-ssh-keys-with-ansible.html) I described the playbook I use to collect SSH keys from network devices. As I use it quite often, it became tedious to write **ansible-playbook** ***path-to-playbook*** every time I wanted to run the collection process.

Ansible playbooks are YAML documents, and YAML documents use \# to start comments, so I thought "_what if I'd use a YAML comment to add [shebang](https://en.wikipedia.org/wiki/Shebang(Unix)) and turn my YAML document into a script_"

**TL&DR**: It works. Now for the longer story...
<!--more-->
Bash (or any other shell) will try to execute a file that has *execute* bit set. Use **chmod +x** ***playbook*** to make the playbook executable.

Text files with *execute* bit set are assumed to be shell scripts unless the first line in the file starts with **\#!** sequence which specifies the absolute path to the script interpreter to use.

You can use **which ansible-playbook** to find path to **ansible-playbook** command on your system and add that as the first line of your playbook:

```
#!/usr/local/bin/ansible-playbook
```

It's even better to use **env** command. It's ([almost](https://en.wikipedia.org/wiki/Shebang_(Unix)#Program_location)) always in **/usr/bin** directory and the system call it uses to transfer control to the desired interpreter ([execvp](https://linux.die.net/man/3/execvp)) uses PATH environment variable to find the command you want executed. The first line of your Ansible playbook should therefore be:

```
#!/usr/bin/env ansible-playbook
```

Cherry on the cake: add a symbolic link to your playbook into one of the directories in your search path. For example:

```
$ ln –s /vagrant/tools/ssh-keys/get-keys.yml ~/bin/get-ssh-keys
```

Now you can execute your Ansible playbook like any other Linux command.

**No idea what I'm talking about?** Check out the [Ansible for Networking Engineers](http://www.ipspace.net/Ansible_for_Networking_Engineers) webinar and online course.

### Adding Environment Variables

As Brian Coca explained in a comment, you have to use `-S` **env** parameter to add environment variables to the *shebang* line. When executing your script, the shell passes the rest of the *shebang* line as a single argument to the interpreter (**env**), and without the `-S` parameter **env** dutifully passes that argument to *execvp* as the file name to be executed. 

`-S` parameter splits the rest of the string into multiple arguments making it all work:

```
#!/usr/bin/env -S ANSIBLE_STDOUT_CALLBACK=dense ansible-playbook
```

### Revision History

2022-02-17
: Added *adding environment variables* section
