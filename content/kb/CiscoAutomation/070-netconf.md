# NETCONF and RESTCONF

Network Configuration Protocol (NETCONF - all uppercase according to IETF docs, although it's not an acronym) is an IETF standard (RFC 6241) developed to manage network devices. SNMP was also developed by IETF for the same purpose. In fact, NETCONF and SNMP have many similarities, and there are people referring to NETCONF as SNMPv4. Explaining NETCONF details is beyond the scope of this short blog post, but let's introduce a couple of essential characterstics:

INFO: If you're looking for a deep dive into NETCONF and YANG, please check out the *[NETCONF and YANG](https://www.ipspace.net/NETCONF_and_YANG)* webinar

* NETCONF provides mechanisms to install, manipulate, and delete the configuration of network devices.
* YANG describes the data structures exchanged in NETCONF message (like SMIv2 describes SNMP MIBs).
* RESTCONF (RFC 8040) provides a subset of NETCONF functionality implemented on top of HTTP/HTTPS.
* Both NETCONF and RESTCONF were developed to manages devices in a standard way.

## NETCONF

NETCONF protocol is based on XML messages exchanged via SSH protocol using TCP port 830 (default). Network devices running a NETCONF agent can be managed through five operations:

* **get**: This operation retrieves the running configuration and device state information.
* **get-config**: This operation retrieves all or part of a specified configuration.
* **edit-config**: This operation loads all or part of a specified configuration to the specified device.
* **copy-config**: This operation creates or replaces an entire configuration with specified contents.
* **delete-config**: This operation deletes a configuration. The running configuration cannot be deleted.

## RESTCONF

RESTCONF is another IETF standard implementing some NETCONF functionality on top of RESTful interface.

Network devices running a RESTCONF agent can be managed through five HTTP operations:

* **GET**: This method retrieves data and metadata for a resource. It is supported for all resource types, except operation resources.
* **PATCH**: This method partially modifies a resource (the equivalent of the NETCONF **merge** operation).
* **PUT**: This method creates or replaces the target resource.
* **POST**: This method creates a data resource or invokes an operations resource.
* **DELETE**: This method deletes the target resource.

It seems like RESTCONF is NETCONF via HTTP/HTTPS using XML or JSON messages, but it's missing several crucial NETCONF components, including multiple datastores, commits or rollbacks, and configuration locking.

## Caveats

SNMP was developed to standardize network device management. Ideally, network administrator should be able to use SNMP to:

* read status information from any device in a standard way;
* modify (configure) devices in a standard way.

In practice:

* vendors show a subset of data available on a device through standard SNMP MIBs;
* vendors show data specific to a particular platform using custom format (calling private tree `iso.org.dod.internet.private.enterprises`);
* SNMP is rarely used to modify configurations because it lacks atomic configuration changes.

In other words, SNMP is useful to retrieve information, even if some of it is stored in a custom format, but it's not the best tool to configure devices.

NETCONF and RESTCONF have been developed to fix the caveats of SNMP but, in my opinion, they fail for the same reasons:

* even where standard YANG schema exists, each vendor implements a custom schema (like the private tree of SNMP);
* different models from same vendors use different schema (the same REST call cannot be used for Cisco IOS-XE, IOS-XR, and NXOS);
* vendor-specific schemas change over time, sometimes with little regard to backward compatibility (we already experienced that with Cisco IOS-XE);
* documentation is incomplete if it exists.

I'm confident that NETCONF and RESTCONF will eventually follow the same path as SNMP, and will be used in the same way: to get statistics and other operational data, but not to update device configurations.
