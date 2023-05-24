title: Data Validation
publish: 2020-10-19

Optimizing a data model and removing duplicate data is great... but how do we know that we're working with a _valid_ data model? 

That question is easy to answer in a traditional IPAM/CMDB implementation using a back-end database and a custom data handling logic offering a REST API, a GUI, or both. The custom data handling logic validates data before it's entered in the database, and the database thus contains syntactically and semantically valid data.

In a simpler solution that relies on text files to store the network data model (also known as _source-of-truth_) it's hard to do a rigorous per-transaction validation, more so if you're using a text editor to modify those files. In these cases you have to write your own validation pipeline using tools that check:

* Text file syntax;
* Conformance with a data model schema;
* Referential integrity.

Using our [latest data model with per-link prefixes](40-Link%20Prefixes.html) that is stored as a bunch of Ansible **host_vars** files and a **network.yml** file, the validation pipeline should check whether:

* All files conform to YAML syntax (you can use tools like **yamllint** to do that);
* Host facts for each host include **hostname** and **bgp_as** values;
* Network data model contains **links** value which is an array of _core_ and _edge_ links;
* Core links contain a **prefix** and at least two other values;
* Edge links contain a single value which is a dictionary (or object if you prefer JSON terminology) with a single value.

You could write a simple program in any programming language to perform those tests, or use data modeling languages (also called _schemas_) like YANG, JSON Schema, or XML Schema to check most of the constraints. As it's easy to transform YAML files into JSON, we'll use **jsonschema**.

NOTE: It's often hard to check referential integrity using a data modeling language. You might have to write your own program to do that, but at least you can offload the boring task of checking data structures and data format to a third-party solution.

## Validating Host Data

As the first step in our data model validation logic we'll validate Ansible host facts. These facts are often spread over a number of files and directories, or generated on-the-fly with an external script or Ansible plugin. The best way to fetch them is thus to delegate the task to **ansible-inventory** program that produces a JSON data structure as required by an external inventory script.

```
$ ansible-inventory -i ../hosts --list
{
    "_meta": {
        "hostvars": {
            "S1": {
                "bgp_as": 65001,
                "description": "Unexpected",
                "hostname": "S1"
            },
            "S2": {
                "bgp_as": 65002,
                "hostname": "S2"
            }
        }
    },
    "all": {
        "children": [
            "ungrouped"
        ]
    },
...
```

We need to extract just the host variables from the resulting JSON data structure, and **jq** seems to be a perfect fit for the job:

```
$ ansible-inventory -i ../hosts --list|jq ._meta.hostvars
{
  "S1": {
    "bgp_as": 65001,
    "description": "Unexpected",
    "hostname": "S1"
  },
  "S2": {
    "bgp_as": 65002,
    "hostname": "S2"
  }
}
```

If we want to use the **jsonschema** command-line utility we have to store the results in a text file and then invoke the **jsonschema** utility with the name of the text file and the JSON Schema file the data should be checked against.

```
$ jsonschema -i /tmp/hosts.json hosts.schema.json
{'bgp_as': 65001, 'description': 'Unexpected', 'hostname': 'S1'}: 
Additional properties are not allowed ('description' was unexpected)
```

## Validating Network Data Model

We'll use a similar approach to validate the **network.yml** file:

* Convert YAML file into JSON format with **yq**
* Run **jsonschema** on the resulting JSON file

```
yq <network.yml . >/tmp/$$.network.json
jsonschema -i /tmp/$$.network.json network.schema.json
```

As mentioned above, the JSON Schema enables us to validate the data model grammar, but not the referential integrity. For example:

* We cannot check if the host names specified for core or edge links are valid.
* While we can validate the interface name format, we have no means of checking whether the devices have the interfaces we want to use without connecting to the network devices or fetching data from a network management system.

## A Word on JSON Schema

Data modeling languages are not for the faint-hearted, and JSON Schema is no exception. The cryptic way the specifications are written doesn't help either (I had more fun reading ISO or IEEE standards). Fortunately, the [Understanding JSON Schema](http://json-schema.org/understanding-json-schema/index.html) online book does a pretty good job explaining the intricacies.

Just to give you a taste of how JSON schema works: here's the JSON document describing the expected data structure of host variables derived from Ansible inventory:

```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://www.ipSpace.net/hosts.schema.json",
  "title": "Ansible inventory data",
  "definitions": {
    ...
  },
  "type": "object",
  "patternProperties": {
    ".*" : { "$ref" : "#/definitions/router" }
  },
  "minProperties": 1
}
```

This is what the schema description is saying:

* It's describing Ansible inventory data;
* It contains definitions of additional schemas (see below)
* The top-level element is an object (dictionary) with some properties (we know they are inventory host names), and each property should conform to the _router_ schema
* The minimum number of properties is one (at least one host in the inventory file).

The definition of the _router_ schema is within the **definitions** property:

```
"router" : {
  "type" : "object",
  "properties": {
    "bgp_as": {
      "type": "number",
      "minimum": 1,
      "maximum": 65535
    },
    "hostname": {
      "type": "string"
    }
  },
  "required": [ "bgp_as","hostname" ],
  "additionalProperties": false
}
```

According to this schema, a router (more precisely, Ansible host facts describing a router) is an object with:

* A number **bgp_as** property which must be between 1 and 65535;
* A string **hostname** property
* Both properties are required, and there should be no other properties in the object.

## Getting Your Hands Dirty

The hosts- and network JSON schemas as well as the source code for the validation script are available on GitHub. Please feel free to clone the repository, change the **host_vars** files or the network data model, and rerun the validation script.

You might also want to explore JSON Schema and:

* Figure out what **network** JSON schema does;
* Add an optional **description** property to the router data model;
* Change the validation of **bgp_as** property to allow 4-byte AS numbers in dot notation.

You will need these tools:

* [jq](https://stedolan.github.io/jq/)
* [yq](https://kislyuk.github.io/yq/)
* [jsonschema](https://pypi.org/project/jsonschema/)

## More on Data Validation

We covered data validation and CI/CD pipelines extensively in *[Validation, Error Handling and Unit Tests](https://my.ipspace.net/bin/list?id=NetAutSol&module=5)* part of *[Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions)* online course.