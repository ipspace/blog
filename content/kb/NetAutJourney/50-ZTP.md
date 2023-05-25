---
kb_section: NetAutJourney
minimal_sidebar: true
pre_scroll: true
title: Restoring or Provisioning Devices with ZTP
toc_title: Restoring or Provisioning Devices with ZTP
url: /kb/NetAutJourney/50-ZTP.html
---
The latest functionality that I added to the web interface is the ability to
restore a switch based on a configuration backup from Oxidized. The web
frontend starts a playbook on the Ansible server that sets up FreeZTP
server with the correct configuration and DHCP options (which determine whether
ZTP process on a switch starts an IOS upgrade).

{{<figure src="ZTP-Configuration-Restore.png" caption="ZTP configuration restore">}}
<div class='caption figure'>Figure 7: Combining ZTP with a simple configuration setup in the frontend means
that anyone can restore or provision a switch.</div>

What I like about the FreeZTP setup is that anyone in the IT department
(including, God forbid, the manager), could deploy configuration onto a replacement
switch to have it swapped out, or provision a new switch before having it installed.

The HTML forms I used have all the hooks you need to check the input. For instance:

* Required fields can be highlighted when left empty;
* You can set conditions for the data entered for the serial number (permitting only alphanumeric characters);
* It is easy to populate the dropdowns using a result of a database query.

Once the operator input is collected, it can be passed to a playbook using the `--extra-vars`
option,which overrides the variables specified in the playbook or Ansible inventory, so you
can start a playbook that normally runs from the CLI from the web front-end without further modification.

The same method is used to set up FreeZTP server when provisioning a new switch; the only difference
is that the configuration is not pulled from Oxidized but is instead generated from a template.

**Notes:**

* Using the JSON format, you can pass any variable (including non-string variables) to an Ansible playbook:

```
--extra-vars '{ "switch": "sw01",
  "serialnumber": "123ABC", "my_float": 2.234,
  "my_list": ["bla", 123, "etc"] }'
```

* I use the undocumented _external-template_ ZTP option, which allows the loading of a complete configuration:

```
ztp set external-template COMPLETE file '/path/to/<config>'
```

## Beyond ZTP

I have built a port configurator with a web interface for another customer. The web interface allows
selecting a switch from a dropdown, and as soon as a switch is selected, an
AJAX (_Asynchronous Javascript and XML_) function populates the second dropdown with the
interfaces available on that switch. As the next step, we could couple this functionality
to a port request form, creating a _self-service_ portal.

Another example allows uploading a CSV file with switch- and VLAN names to bulk configure
switchports across the network (1200+ devices), saving a tonne of tedious
command-line configuration. Options include a button to review the input CSV, run the configuration
playbook in checkmode, update the inventory DB, and display the status of the ports supplied in the
CSV as they currently appear in the database.

{{<figure src="Bulk-Configuration.png" caption="Bulk configuration screenshot">}}
<div class='caption figure'>Figure 8: The interface for bulk configuring switch ports.</div>
