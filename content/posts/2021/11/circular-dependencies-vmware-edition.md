---
title: "Circular Dependencies, VMware NSX-T Edition"
date: 2021-11-25 07:41:00
tags: [ NSX ]
---
A friend of mine sent me a link to a [lengthy convoluted document](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/3.1/installation/GUID-3770AA1C-DA79-4E95-960A-96DAC376242F.html) describing the 17-step procedure (with the last step having 10 micro-steps) to follow if you want to run NSX manager on top of N-VDS, or as they call it: _Deploy a Fully Collapsed vSphere Cluster NSX-T on Hosts Running N-VDS Switches_[^1].

You might not be familiar with vSphere networking and the way NSX-T uses that (in which case I can highly recommend [vSphere](https://www.ipspace.net/VSphere_6_Networking_Deep_Dive) and [NSX](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) webinars), so here's a CliffsNotes version of it: you want to put the management component of NSX-T on top of the virtual switch it's managing, and make it accessible only through that virtual switch. What could possibly go wrong?
<!--more-->
[^1]: I saved the documentation in PDF format just in case that masterpiece gets removed ;)

Well, even VMware technical marketing didn't risk NOT describing the biggest caveat:

> In a single cluster configuration, management components are hosted on an N-VDS switch as VMs. The N-VDS port to which the management component connects to by default is initialized as a blocked port due to security considerations. If there is a power failure requiring all the four hosts to reboot, the management VM port will be initialized in a blocked state[^2]. 

[^2]: Let me translate that into less complex language: you'll be dealing with a bricked cluster. Congratulations. Oh, and a power failure would never cause all hosts to reboot, would it?

To "solve" that, you have to follow the ten substeps of step 17. Those steps involve writing JSON documents in a text editor and executing **curl**. Yeah, that's definitely the best they way to configure any product. The last time I've seen something like that was the Wellfleet Technician Interface where you had the privilege of configuring the box by writing values into SNMP OIDs.

For those of you who still don't appreciate how ridiculous the whole idea is: imagine migrating from EIGRP to OSPF, but with the following minor limitations:

* There is no out-of-band interface (pretty normal so far).
* You cannot run the routing protocols in parallel (WTx?)
* You have to type in individual commands (OK).
* You cannot do cut-and-paste, and you definitely cannot cheat by copying commands into a file and executing them locally (OMG).
* Every command is executed immediately (as usual) and immediately stored into the permanent configuration file (WTx???).
* Reloading or power-cycling the box cannot bring the box to a previous state (I'm out of here)
* While there is some rollback capability, you have to be able to reach the box to execute it (fun times).

Now don't get me wrong. If someone has a desperate urge to participate in Red Bull Flying Contest, I'm all for it, but describing the resulting Hero's Journey as part of official product documentation is a bit over the top. I can only hope there was a ginormous purchase order behind this requirement; bravado for bravado's sake never made much sense to me.

Careful readers might point out that Nutanix uses a similar trick: a VM exposing an iSCSI or NFS target is running on top of a hypervisor using that same target[^NCD]. There's just a slight difference between the two: Nutanix comes as a prepackaged solution, not as a loose collection of hard-to-fit parts and IKEA-like instructions.

[^NCD]: Although, as Erik Auerswald [explained in his comment](/2021/11/circular-dependencies-vmware-edition.html#878), that does not create a circular dependency as the Nutanix VM runs off local storage in the ESXi host, and only then offers NFS/iSCSI target as an additional data store for other VMs.

Finally, let's assume VMware does care enough about customers who want to deploy NSX-T on a 4-node cluster. The only sane way to meet that requirement would be to create a prepackaged one-click solution (aka "automate it", but with proper rollbacks when an error is encountered), not a Rube Goldberg machine. Come on, VMware, we know you CAN do better than that.

### Release History

2021-11-25
: * Footnote: Nutanix does not create circular dependencies (based on the comment by Erik Auerswald).
