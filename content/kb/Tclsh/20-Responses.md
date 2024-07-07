---
kb_section: Tclsh
minimal_sidebar: true
title: Insert Responses to Command Prompts in Tclsh
url: /kb/Tclsh/20-Responses/
---
Some IOS CLI commands (for example, the **clear counter** command) require user confirmations. The **typeahead** ***text-string*** Tcl command can be used to insert the simulated user response before an IOS CLI command is executed.

{{<note warn>}}The **typeahead** command might not work correctly in earlier IOS releases. All the tests in this article were performed with the IOS release 12.4(15)T5.{{</note>}}

Simulated typeahead is accepted only by the IOS commands executed through the **exec** Tcl command; if you execute an IOS CLI command directly from the **tclsh** script, Tcl cannot control its input/output and thus cannot insert the user response.

The **typeahead** text is consumed as needed. You can execute more than one IOS CLI command with multiple **exec** Tcl commands without replenishing the typeahead buffer; Cisco IOS obviously opens a single VTY session for the duration of the **tclsh** script and executes all IOS CLI commands requested with the **exec** command in that session.

For example, the following code sequence will clear the interface counters even though the **clear counter** command is the second command in the sequence.

{{<cc>}}Sample typeahead script{{</cc>}}
```
typeahead "y"
exec {show ip route}
exec {clear counters fa 0/0} 
```

The typeahead text shall include all required user input, including the newline character. To include the newline character in the typeahead text, use the “\\n” sequence. For example, the **reload** command asks two questions when the running configuration has been changed:

```
Test#reload
System configuration has been modified. Save? [yes/no]: y
Building configuration...
[OK]
Proceed with reload? [confirm]y
```

To reload a router from the Tcl script you can use the following code which answers “yes” to both questions (reloading a router without saving the configuration is better done through the EEM **action reload** command).

{{<cc>}}Reloading the router{{</cc>}}
```
typeahead "y\ny"
exec {reload} 
```

If the **typeahead** command is not followed by an **exec** command, the typeahead text stays in the buffer and appears as user-typed input on the command line after the **tclsh** script completes. For example, the following script clears interface counters and executes the **show ip route** command after the **tclsh** script has completed.

```
typeahead "y"
exec {clear counters fa 0/0}
typeahead "show ip route\n"
```
