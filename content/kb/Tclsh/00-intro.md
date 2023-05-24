title: Running tclsh Scripts
index: yes

Tcl shell (started with the **tclsh** Cisco IOS CLI command) was introduced in Cisco IOS release 12.3(2)T. The Tcl shell can be used to execute interactive Tcl commands interspersed with regular Cisco IOS CLI commands. It can also be used to run Tcl scripts that can substantially enhance the Cisco IOS CLI experience. 

WARN: Due to security considerations, primarily the ability to write IOS-based password grabbers, the **tclsh** command is available only in CLI privilege level 15.

## Running tclsh Scripts

Cisco IOS **tclsh** implementation behaves similarly to the **tclsh** implementations on other operating systems. The **tclsh** command without parameters starts the interactive shell. When one or more parameters are present in the **tclsh** command, the first parameter represents the name of the Tcl script to execute and the remaining parameters are passed to the script.

The first parameter of the Cisco IOS **tclsh** command is an Integrated File System (IFS) URL that can point to a local file (for example **flash:myScript.tcl** or **nvram:script.tcl**) or a file accessible through any of the remote file access methods available in Cisco IOS (TFTP, FTP, RCP, SCP, HTTP or HTTPS).

### Example

Store a simple *helloWorld.tcl* file on an external TFTP server with the IP address 10.0.0.10.

```
puts "hello world" 
```
CAPTION: helloWorld.tcl

Executing the command **tclsh tftp://10.0.0.10/helloWorld.tcl** on a router that can reach the TFTP server will result in the "famous" _hello world_ printout:

```
Router#tclsh tftp://10.0.0.10/helloWorld.tcl
Loading helloWorld.tcl from 10.0.0.10 (via FastEthernet0/0): !
[OK - 20 bytes]
hello, world
```

For more details read [Cisco IOS XE Scripting with Tcl](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ios_tcl/configuration/xe-16/ios-tcl-xe-16-book/Cisco_IOS_XE_Scripting_with_Tcl.html).