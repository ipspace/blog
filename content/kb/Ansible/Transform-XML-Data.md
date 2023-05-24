title: Transforming XML Data in Ansible

A netwoking engineer attending the Building Network Automation Solutions online course wanted to transform Junos interface configuration (in XML format) into a concise data structure that could be used in an Ansible playbook.

## Example

Junos represents interface configuration in a data structure similar to the following XML document:

```
<configuration>
  <interfaces>
    <interface>
      <name>ge-0/0/0</name>
      <mac>00:00:00:00:00:01</mac>
      <unit>
        <name>0</name>
        <family>
          <inet>
            <address>
              <name>192.168.1.101/24</name>
            </address>
          </inet>
        </family>
      </unit>
    </interface>
    <interface>
      <name>ge-0/0/3</name>
      <flexible-vlan-tagging/>
      <encapsulation>flexible-ethernet-services</encapsulation>
      <mac>00:00:00:00:00:01</mac>
      <unit>
        <name>112</name>
        <vlan-id>112</vlan-id>
        <family>
            <inet>
                <address>
                    <name>172.16.112.1/24</name>
                </address>
            </inet>
            <iso>
            </iso>
            <mpls>
            </mpls>
        </family>
      </unit>
      <unit>
        <name>114</name>
        <vlan-id>114</vlan-id>
        <family>
          <inet>
            <address>
              <name>172.16.114.1/24</name>
            </address>
          </inet>
        </family>
      </unit>
    </interface>
  </interfaces>
</configuration>
```

The data structure we would like to get out of that XML document should look like this:

```
ge-0/0/0.0:
 address: 192.168.1.101/24
ge-0/0/3.112:
 address: 172.16.112.1/24
ge-0/0/3.114:
 address: 172.16.114.1/24
 ```
## XML-to-JSON Data Transformation

To transform XML document into target data structure using Ansible Jinja2 filters (or equivalent Python code), you have to solve two challenges:

* How do you parse Junos XML data into an Ansible (= Python) data structure
* How do you convert that data structure into the target data structure.

Traditionally you could use **junos_command** module to get XML data straight into Ansible data structure as I explained in the [_Executing Commands on Network Devices_](https://my.ipspace.net/bin/get/Ansible/N2.1%20-%20Executing%20Commands%20on%20Network%20Devices.mp4?doccode=Ansible) video in the [_Ansible Networking Modules_](https://my.ipspace.net/bin/list?id=Ansible#NET_CMD) part of [Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers) webinar. Recent versions of Junos could also return JSON-formatted data which would be immediately usable in Ansible (but see caveats below).

NOTE: In earlier Ansible versions the **junos_command** module returned parsed XML data no matter how it was invoked... but it seems that in Ansible 2.8 it started returning XML data as a text string when you decided to use **network_cli** connection plugin.

When the data returned by a network device is parsed and resides in an Ansible variable (fact), you could use **json_query** filter to extract the bits you need. You could also use one of the tricks I described in [_Transforming Data Models with Ansible_](https://my.ipspace.net/bin/list?id=NetAutSol&module=3#M3S4B), for example using a Jinja2 template with **lookup** filter. Finally, you could write a small Python data manipulation filter yourself.

## One-Step Transformation

Recent versions of Ansible provide an alternate option which can be used with any device that returns XML data (for example, XML parser is built into **junos_command** module but not in **nxos_command** module): **parse_xml** Jinja2 filter. That filter uses XPath expressions to identify bits of XML document you're interested in, and Jinja2-augmented YAML to create the target data structure. With **parse_xml** filter you can parse any XML data into (almost) any desired target data structure in one step.

Finally, if you plan to do extensive transformations of XML documents, it might be worthwhile to learn XSLT and use XSLT transformation in a custom Python Jinja2 filter (or move to Nornir and use the same Python code directly).

## Caveats

XML is a richer presentation language than JSON; XML-to-JSON transformations that are not aware of the source data structure could return inconsistent data based on the number of elements in an XML document. For example, if you generate a JSON printout of a list of VLANs on Nexus OS you could get a list (when there's more than one VLAN) or a dictionary (if there's a single VLAN configured on the switch).

[Damien Garros](https://www.ipspace.net/Author:Damien_Garros) experienced similar behavior with Junos. This is what he sent me on this topic:

---

I would be cautious about using JSON output in Junos. As you probably know, JSON and XML are not compatible so you are exposed to the risk that Junos will return a different data structure for the same command if the number of elements in the response is different.

Juniper wrote [jxmlease library](https://github.com/Juniper/jxmlease) to help with that, but at the end of the day you can only mitigate that because these two formats don’t translate 100%. Also when moving to Json you are losing the attributes in XML.

Also, as part of [PyEZ](https://www.juniper.net/documentation/en_US/junos-pyez/information-products/pathway-pages/junos-pyez-developer-guide.html) there is a nice tool to convert XML into JSON structure called the Table and Views. It let you define a table in YAML based on XPath. You can use that directly in ansible by using the [Juniper-supplied module **juniper_junos_table**](https://github.com/Juniper/ansible-junos-stdlib).

---

## Getting It Right

The only way to get a precise XML-to-JSON transformation is to understand the semantics of the XML data structure, and one of the
popular ways of describing a (network-related) data model is YANG. With a YANG data model describing the XML data structure you could
use **yanglint** tool to perform accurate XML-to-JSON transformation - for more details read the
[Convert XML to JSON](https://plajjan.github.io/2020-01-29-convert-xml-to-json-and-yaml.html) article by
[Kristian Larsson](https://www.ipspace.net/Author:Kristian_Larsson).
