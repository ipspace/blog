title: Executing Cisco IOS Commands from Tcl Shell

Cisco IOS provides three mechanisms to execute CLI and configuration commands from Tcl:

-   *cli\_open*, *cli\_write* and *cli\_close* commands are used in Embedded Event Manager (EEM) Tcl policies.
-   *exec* and *ios\_config* commands are used in Tcl scripts executed with **tclsh** command.
-   You can also mix IOS CLI commands with regular Tcl commands in **tclsh** scripts (but not in EEM Tcl policies). 

## Executing CLI commands in Tclsh

When you execute a CLI command in a **tclsh** script, the command is executed on the line on which the **tclsh** script was started. Results of the command are sent directly to the terminal (line) and cannot be captured in a Tcl variable for further processing. Invalid IOS CLI commands raise Tcl errors that can be caught with the **catch** command.

### Example

The following script executes the **show users** command to verify which line is used to execute the IOS commands embedded in the Tcl code. An invalid command (**show ipx route**) is then executed, first within a **catch** block, then without an error handling mechanism.

```
puts "\nexecuting show users"
show users

puts "\ncatching execution error"
if {[catch {show ipx route} e]} {
  puts "error caught: $e"
}

puts "\nexecution error, not caught"
show ipx route
puts "script ends" 
```
CAPTION: nativeExec.tcl

When you execute this script on a router, you get the following printout:

```
router#tclsh http://www/tcl/nativeExec.tcl
Loading http://www/tcl/nativeExec.tcl
executing show users

    Line       User       Host(s)              Idle       Location
*  0 con 0                idle                 00:00:00

  Interface    User               Mode         Idle     Peer Address

catching execution error
error caught: invalid command name "show"

execution error, not caught
invalid command name "show"
    while executing
"show ipx route"
    (file "http://www/tcl/nativeExec.tcl" line 10)
```

## Executing CLI commands with the Tcl **exec** command

The **exec** Tcl command executes a single IOS CLI command on another line (VTY) of the same router. The remote execution allows Tcl to collect the command output which can be stored in a Tcl variable and processed further.

Tcl accepts multiple parameters in the **exec** command to implement command pipelines. These do not work in Cisco IOS; while you can supply more than one parameter to the **exec** command, such a command will always fail.

### Example

The following script executes the **show users** IOS CLI command with the Tcl **exec** command. The results of the **show users** command are stored in a variable and displayed with the **puts** command. A valid (**show ip route**) and an invalid (**show ipx route**) command are then executed to illustrate the error handling mechanism implemented with a **catch** block.

```
puts "\nexecuting show users"
set result [exec {show users}]
puts $result

puts "\nexecuting show ip route"
if {[catch {set result [exec {show ip route}]} e]} {
  puts "error caught: $e"
} else {
  puts [format "result string length %d" [string length $result]]
}

puts "\nexecuting show ipx route"
if {[catch {set result [exec {show ipx route}]} e]} {
  puts "error caught: $e"
} else {
  puts [format "result string length %d" [string length $result]]
} 
```
CAPTION: execCommand.tcl

The *execCommand.tcl* script executed on a router generates the following printout:

```
c7200#tclsh http://www/tcl/execCommand.tcl
Loading http://www/tcl/execCommand.tcl
executing show users

    Line       User       Host(s)              Idle       Location
   0 con 0                idle                 00:00:00
*  2 vty 0                Tcl Serv - tty0      00:00:00

  Interface    User               Mode         Idle     Peer Address


executing show ip route
result string length 767

executing show ipx route
error caught:
```

The printout illustrates two important points:

-   The IOS CLI command started with the **exec** Tcl command is executed on another VTY with special host name.

NOTE: The **exec** command does not execute properly if no VTY line is available when it’s executed. You should have configured **transport input none** on one or more VTY lines to ensure the Tcl scripts will always find a free VTY.

-   When the IOS CLI command executed with the **exec** command fails, the **exec** command fails (as expected), but the IOS error message is not returned to the **catch** command.

## Routing configuration with **ios\_config** command

The Tcl **ios\_config** command can be used in **tclsh** scripts to change the router configuration. The command accepts multiple arguments, they are evaluated sequentially like they would be entered line-by-line in the configuration mode.

Usually, you would use one **ios\_config** command for each global configuration command and **ios\_config** ***mode command*** syntax to configure parameters in one of the sub-configuration modes, for example:

```
ios_config "hostname test"
ios_config "interface loopback 0" "no shutdown"
```

You can also chain numerous configuration commands in a single **ios\_config** command, for example:

```
test#tclsh
03:01:22: %SYS-5-CONFIG_I: Configured from console by console
test(tcl)#ios_config "hostname router" "interface loop 101" "shutdown"
router(tcl)#
%LINK-5-CHANGED: Interface Loopback101, changed state to administratively down
```

Similarly to the **exec** Tcl command, the **ios\_config** command executes in the context of another VTY line and returns the collected output to the caller.

```
router#tclsh
router(tcl)#ios_config "do show users"

    Line       User       Host(s)              Idle       Location
   0 con 0                idle                 00:00:00
*  2 vty 0                Tcl Serv - tty0      00:00:00
```

If no VTY line is available, the IOS configuration commands passed to **ios\_config** command are executed on the line on which the **tclsh** script is executing. The command output is not returned to the caller, but this is usually not an issue as the configuration commands rarely print important messages.
