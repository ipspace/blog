---
date: 2017-02-07 10:24:00+01:00
tags:
- automation
- data center
- Cumulus Linux
title: And This Is Why Relying on Linux Makes Sense
url: /2017/02/and-this-is-why-relying-on-linux-makes.html
---
Most networking operating systems include a mechanism to roll back device configuration and/or create configuration snapshots. These mechanisms usually work only for the device configuration, but do not include operating system images or other components (example: crypto keys).

Now imagine using RFC 1925 rule 6a and changing the "configuration rollback" problem into "file system snapshot" problem. That's exactly what [Cumulus Linux does in its newest release](https://cumulusnetworks.com/blog/new-cumulus-linux-features-snapshots-rollback/). Does it make sense? It depends.
<!--more-->
{{<note update>}}Update 2017-02-08: Added NCLU enhancements.{{</note>}}

### The Benefits

The real story behind this feature is Btree File System (BTRFS), a Linux file system with built-in support for subvolumes, snapshots and rollbacks. Leveraging an existing feature instead of reinventing an inferior wheel (like some other vendors love to do) makes perfect sense -- after all, improvements made to BTRFS by others using it will eventually appear in Cumulus Linux.

### The Drawbacks

File system rollback is like [hypervisor-based high availability](/2011/08/high-availability-fallacies.html). It's a great feature, but also an all-or-nothing one, and it's impossible to change the root file system (do a rollback) on a running system -- you need a restart to do it.

While the snapshots built in Cumulus Linux 3.2 are definitely a life-saver from some fat finger scenarios (and you can recover anything down to an individual file from the snapshot), they're not the only tool you should rely on. You should also maintain configuration archive to be able to roll back device or daemon configuration without restarting the system or digging through the snapshots... and relying on Linux yet again comes in handy -- there are tons of open-source configuration management tools like git you can use to manage Linux configuration files.

### Things got better with NCLU

Dinesh Dutt sent me a kind reminder that [some of the things I mentioned got simpler with NCLU](https://cumulusnetworks.com/blog/cumulus-linux-network-command-line-utlility/) (I should have known as I introduced NCLU at the [last week\'s webinar](http://go.cumulusnetworks.com/l/32472/2017-01-04/8v3fbr), but unfortunately couldn\'t stay to watch the good stuff)

> With NCLU, the story is a little different. You don\'t have to restart the box to rollback, the commit history in the btfs is presented in a much nicer way, rollback is better defined etc. Having said that, NCLU doesn\'t roll back everything, only the files it manages: /etc/network/interfaces, /etc/hosts, the ACLs and quagga.conf.

### Want to get started?

The networking engineers attending my [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course found it a great way to get started on their journey toward using open-source tools and automating their networks.