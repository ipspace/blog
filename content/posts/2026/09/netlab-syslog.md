---
title: "Using Syslog in netlab Labs"
date: 2026-09-24 08:17:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
_netlab_ [release 26.09](https://netlab.tools/release/26.09/) added support for Syslog clients and servers. We implemented the clients on [numerous platforms](https://netlab.tools/module/services/#platform-support); the only Syslog server implementation is the **dnsmasq** container.

Adding Syslog to a _netlab_ lab is (almost) trivial:

* You have to (re)build the **dnsmasq** container with the **netlab clab build dnsmasq** command to add *rsyslogd* to the container image
* When you add a **dnsmasq** node to a lab, it automatically starts a Syslog server
* The Syslog client is [enabled](https://netlab.tools/module/services/#syslog-parameters) on other nodes (or globally) with the **services.syslog.server** setting.
<!--more-->
Here's the simplest possible lab topology using Syslog (see also the [Syslog client integration test](https://github.com/ipspace/netlab/blob/dev/tests/integration/services/11-syslog-client.yml)):

{{<printout>}}
provider: clab
defaults.device: eos

nodes:
  router:
    module: [ services ]
    services.syslog.server: srv
  srv:
    device: dnsmasq

links: [ router-srv ]
{{</printout>}}

* The topology is using Arista cEOS containers (lines 1-2)
* The router node is using the **[services](https://netlab.tools/module/services/)** module (network services are optional, so you have to enable them) (line 6) with SRV as the Syslog server (line 7)
* The SRV node is a dnsmasq container (line 9). The Syslog server on **dnsmasq** nodes is enabled by default.

Once the lab is started, you can observe the Syslog messages in the `/var/log/syslog` file on the SRV node, for example:

```
$ netlab connect srv tail /var/log/syslog
Connecting to container clab-X-srv, executing tail /var/log/syslog
2026-09-21T06:31:53.638666+00:00 srv kernel: systemd-sysv-generator[44]: SysV service '/etc/rc.d/init.d/snmpd' lacks a native systemd unit file. Automatically generating a unit file for compatibility. Please update package to include a native systemd unit file, in order to make it more safe and robust.
2026-09-21T06:31:53.790613+00:00 srv kernel: systemd-journald[80]: Received client request to flush runtime journal.
2026-09-21T06:32:42+00:00 router Stp: %SPANTREE-6-STABLE_CHANGE: Stp state is now stable
2026-09-21T06:33:06+00:00 router SystemInitMonitor: %SYS-5-SYSTEM_INITIALIZED: System is initialized
2026-09-21T06:33:06+00:00 router SuperServer: %SYS-5-CLI_SCHEDULER_ENABLED: CliScheduler is enabled, continuing its execution of scheduled CLI jobs.
2026-09-21T06:33:06+00:00 router ProcLauncher-1: %LAUNCHER-6-PROCESS_STOP: Configuring process 'SystemInitMonitor' to stop in role 'ActiveSupervisor'
2026-09-21T06:33:07+00:00 router ProcMgr: %PROCMGR-6-COMMAND_RECEIVED: ProcMgr has received 'warm start' command
2026-09-21T06:33:07+00:00 router ProcMgr: %PROCMGR-6-WORKER_WARMSTART: ProcMgr worker warm start. (PID=632)
2026-09-21T06:33:07+00:00 router ProcMgr: %PROCMGR-6-TERMINATE_RUNNING_PROCESS: Terminating deconfigured/reconfigured process 'SystemInitMonitor' (PID=1070)
2026-09-21T06:33:07+00:00 router ProcMgr: %PROCMGR-6-PROCESS_TERMINATED: 'SystemInitMonitor' (PID=1070, status=-9) has terminated.
```

### Using Syslog Clients on All Nodes

We did not implement the Syslog client on Linux in release 26.09. Setting the global **services.syslog.server** parameter will thus result in an error, as *dnsmasq* (derived from Linux) does not support a Syslog client. As a workaround, set the **services.syslog** parameter[^CCNS] to `False` on the Syslog server, for example:

[^CCNS]: This parameter controls the Syslog client. The Syslog server is enabled with the **services.server.syslog** parameter.

```
provider: clab
defaults.device: eos
services.syslog.server: srv

nodes:
  router:
    module: [ services ]
  srv:
    device: dnsmasq
    services.syslog: False

links: [ router-srv ]
```

### Persistent Syslog File

Using the [**clab.binds** parameter](https://netlab.tools/labs/clab/#using-file-binds), you can map the container `/var/log/syslog` file to a host file and have a logging file that persists across lab runs, for example:

{{<printout caption="Mapping a local file to the Syslog server logging file" highlight="yes">}}
provider: clab
defaults.device: eos
services.syslog.server: srv

nodes:
  router:
    module: [ services ]
  srv:
    device: dnsmasq
    services.syslog: False
    clab.binds:
      <b>logging: /var/log/syslog</b>

links: [ router-srv ]
{{</printout>}}

{{<note warn>}}
The local file mentioned in the **clab.binds** parameter must exist before the lab starts and must be world-writable, or the container *rsyslog* daemon refuses to use it.

Start the lab with `touch logging && chmod a+rw logging && netlab up`.
{{</note>}}
