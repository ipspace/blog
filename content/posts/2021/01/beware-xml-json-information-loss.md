---
date: 2021-01-14 07:20:00+00:00
series:
- xml-json
tags:
- automation
title: Beware XML-to-JSON Information Loss (Junos with Ansible)
---
When you want to transport a complex data structure between components of a distributed system you're usually using a platform-independent data encoding format like XML, YAML, or JSON.

XML was the hip encoding format in days when Junos and Cisco Nexus OS was designed and lost most of its popularity in the meantime due to its complexity (attributes, namespaces...) that makes it hard to deal with XML documents in most programming languages.

JSON is the new cool kid on the block. It's less complex than XML, maps better into data structures supported by modern programming languages, and has decently fast parser implementations.
<!--more-->
If you're using a recently developed automation platform to deal with network devices that were designed more than a decade ago you'll have to deal with both formats. For example, Junos has always used XML to encode its data structures when sending them over NETCONF (or when requested to do so with **display xml** CLI option) and Ansible relies heavily on JSON and Python data structures. 

Ansible Junos modules do a good job of abstracting the gap. A command executed on a Junos device returns XML document, and you get a Python data structure out of **junos_command** module. Unfortunately, the two data encoding formats are not equivalent, and [most abstractions tend to be leaky](/2019/01/more-on-leaky-abstractions/) biting you at a most inconvenient moment. The breaking point in this case is a list with a single element.

Imagine a Junos device with three IPv4 routes and a single IPv6 route:

{{<cc>}}Junos IPv4 and IPv6 route tables{{</cc>}}
```
vagrant@vsrx> show route

inet.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

0.0.0.0/0          *[Access-internal/12] 00:01:29, metric 0
                    >  to 192.168.121.1 via fxp0.0
192.168.121.0/24   *[Direct/0] 00:01:29
                    >  via fxp0.0
192.168.121.105/32 *[Local/0] 00:01:29
                       Local via fxp0.0

inet6.0: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

ff02::2/128        *[INET6/0] 00:01:44
                       MultiRecv
```

When using **display xml** to format that same information in XML format you get the following document:

{{<cc>}}Junos IPv4 and IPv6 route tables in an XML document{{</cc>}}
```
vagrant@vsrx> show route | display xml
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.3R0/junos">
    <route-information 
      xmlns="http://xml.juniper.net/junos/20.3R0/junos-routing">
        <!-- keepalive -->
        <route-table>
            <table-name>inet.0</table-name>
            <destination-count>3</destination-count>
            <total-route-count>3</total-route-count>
            <active-route-count>3</active-route-count>
            <holddown-route-count>0</holddown-route-count>
            <hidden-route-count>0</hidden-route-count>
            <rt junos:style="brief">
                <rt-destination>0.0.0.0/0</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>Access-internal</protocol-name>
                    <preference>12</preference>
                    <age junos:seconds="128">00:02:08</age>
                    <metric>0</metric>
                    <nh>
                        <selected-next-hop/>
                        <to>192.168.121.1</to>
                        <via>fxp0.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>192.168.121.0/24</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>Direct</protocol-name>
                    <preference>0</preference>
                    <age junos:seconds="128">00:02:08</age>
                    <nh>
                        <selected-next-hop/>
                        <via>fxp0.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>192.168.121.105/32</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>Local</protocol-name>
                    <preference>0</preference>
                    <age junos:seconds="128">00:02:08</age>
                    <nh-type>Local</nh-type>
                    <nh>
                        <nh-local-interface>fxp0.0</nh-local-interface>
                    </nh>
                </rt-entry>
            </rt>
        </route-table>
        <route-table>
            <table-name>inet6.0</table-name>
            <destination-count>1</destination-count>
            <total-route-count>1</total-route-count>
            <active-route-count>1</active-route-count>
            <holddown-route-count>0</holddown-route-count>
            <hidden-route-count>0</hidden-route-count>
            <rt junos:style="brief">
                <rt-destination>ff02::2/128</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>INET6</protocol-name>
                    <preference>0</preference>
                    <age junos:seconds="143">00:02:23</age>
                    <nh-type>MultiRecv</nh-type>
                </rt-entry>
            </rt>
        </route-table>
    </route-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
```

Looks good... but what happens when you're using **junos_command** module to fetch that information, for example with this trivial Ansible playbook?

{{<cc>}}An Ansible playbook that reads Junos route tables{{</cc>}}
```
- hosts: j_vsrx
  gather_facts: false
  tasks:
  - junipernetworks.junos.junos_command:
      commands: show route
      display: xml
```

Here's the data returned by **junos_command** module (using YAML stdout callback to format it into human-readable format):

{{<cc>}}Junos IPv4 and IPv6 route tables as returned by **junos_command** Ansible module{{</cc>}}
```
TASK [junipernetworks.junos.junos_command] *****************************
ok: [j_vsrx] => changed=false
  ansible_facts:
    discovered_interpreter_python: /usr/bin/python3
  output:
  - rpc-reply:
      route-information:
        route-table:
        - active-route-count: '3'
          destination-count: '3'
          hidden-route-count: '0'
          holddown-route-count: '0'
          rt:
          - rt-destination: 0.0.0.0/0
            rt-entry:
              active-tag: '*'
              age: 00:04:15
              current-active: ''
              last-active: ''
              metric: '0'
              nh:
                selected-next-hop: ''
                to: 192.168.121.1
                via: fxp0.0
              preference: '12'
              protocol-name: Access-internal
          - rt-destination: 192.168.121.0/24
            rt-entry:
              active-tag: '*'
              age: 00:04:15
              current-active: ''
              last-active: ''
              nh:
                selected-next-hop: ''
                via: fxp0.0
              preference: '0'
              protocol-name: Direct
          - rt-destination: 192.168.121.105/32
            rt-entry:
              active-tag: '*'
              age: 00:04:15
              current-active: ''
              last-active: ''
              nh:
                nh-local-interface: fxp0.0
              nh-type: Local
              preference: '0'
              protocol-name: Local
          table-name: inet.0
          total-route-count: '3'
        - active-route-count: '1'
          destination-count: '1'
          hidden-route-count: '0'
          holddown-route-count: '0'
          rt:
            rt-destination: ff02::2/128
            rt-entry:
              active-tag: '*'
              age: 00:04:30
              current-active: ''
              last-active: ''
              nh-type: MultiRecv
              preference: '0'
              protocol-name: INET6
          table-name: inet6.0
          total-route-count: '1'
```

Have you noticed anything weird? No? Let me help you...

* **route-table** element within the **rpc-reply.route-information** dictionary is a list of route tables.
* Each route table is a *dictionary* with a few counters and a **rt** element. The **rt** element contains route table entries.
* The IPv4 **rt** element is a *list* or route table entries, the IPv6 **rt** element is a *dictionary*... but only because there's a single IPv6 route. If I were to add another IPv6 route, it would immediately become a *list*. Have fun parsing such a data structure ;)

### What Happened?

Remember: there's no 1:1 mapping between XML and JSON. XML documents use nested *tags* to create complex data structures whereas JSON documents have *arrays* (Python: lists) and *objects* (Python: dictionaries)... and it's unclear when parsing a complex XML data structure whether to turn an XML tag into an array or an object.

Most XML parsers that try abstract the complexities of XML and convert an XML document into a data structure usable by a programming language like Python use a heuristic approach:

* Is a tag the only tag of its type within the parent tag? Use object (dictionary)
* Are there multiple tags of the same type within the parent tag? Use array (list).

The *only* challenge of this approach is that it breaks when something that should have been a list has a single element.

### Can We Fix It?

**TL&DR**: No

There's no perfect solution to this problem. In the ideal world you'd have an attribute attached to an XML tag saying *this is really a list*. In reality, there's no such thing.

An XML-to-JSON converter would thus have to understand the semantics of the underlying data structure, and I don't think anyone is working on that. The best we have (that I'm aware of) is Juniper's [jxmlease](https://jxmlease.readthedocs.io/en/stable/index.html) library used by **junos_command** module.

Also note that this is not a Junos-specific challenge. Cisco Nexus OS exhibits exactly the same behavior (more about that in another blog post).

### What Can We Do?

You could hope that you'll never encounter a list with a single element. Good luck with looking at VLANs on a newly provisioned switch ;)

You could also check whether a data structure that you expect to be a list is really a dictionary and turn it into a list with a single element. More about that in another upcoming blog post.

With recent Junos versions you could also use **display json** output filter to get JSON... but it turns out you can't win that way either. The "*this is really a table*" information is still missing, and to prevent loss of information the Junos XML-to-JSON converter uses an extremely conservative approach: let's turn everything into an array... including tags containing text that are converted into a single-element array containing an object with a **data** value. Have fun dealing with that data structure in your Jinja2 template ;))

{{<cc>}}Junos IPv4 and IPv6 route tables as Junos-generated JSON data structure{{</cc>}}
```
vagrant@vsrx> show route | display json
{
    "route-information" : [
    {
        "attributes" : {
          "xmlns" : "http://xml.juniper.net/junos/20.3R0/junos-routing"
        },
        "route-table" : [
        {
            "comment" : "keepalive",
            "table-name" : [
            {
                "data" : "inet.0"
            }
            ],
            "destination-count" : [
            {
                "data" : "3"
            }
            ],
            "total-route-count" : [
            {
                "data" : "3"
            }
            ],
            "active-route-count" : [
            {
                "data" : "3"
            }
            ],
            "holddown-route-count" : [
            {
                "data" : "0"
            }
            ],
            "hidden-route-count" : [
            {
                "data" : "0"
            }
            ],
            "rt" : [
            {
                "attributes" : {"junos:style" : "brief"},
                "rt-destination" : [
                {
                    "data" : "0.0.0.0/0"
                }
                ],
                "rt-entry" : [
                {
                    "active-tag" : [
                    {
                        "data" : "*"
                    }
                    ],
                    "current-active" : [
                    {
                        "data" : [null]
                    }
                    ],
                    "last-active" : [
                    {
                        "data" : [null]
                    }
                    ],
                    "protocol-name" : [
                    {
                        "data" : "Access-internal"
                    }
                    ],
                    "preference" : [
                    {
                        "data" : "12"
                    }
                    ],
                    "age" : [
                    {
                        "data" : "00:01:09",
                        "attributes" : {"junos:seconds" : "69"}
                    }
                    ],
                    "metric" : [
                    {
                        "data" : "0"
                    }
                    ],
                    "nh" : [
                    {
                        "selected-next-hop" : [
                        {
                            "data" : [null]
                        }
                        ],
                        "to" : [
                        {
                            "data" : "192.168.121.1"
                        }
                        ],
                        "via" : [
                        {
                            "data" : "fxp0.0"
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            {
                "attributes" : {"junos:style" : "brief"},
                "rt-destination" : [
                {
                    "data" : "192.168.121.0/24"
                }
                ],
                "rt-entry" : [
                {
                    "active-tag" : [
                    {
                        "data" : "*"
                    }
                    ],
                    "current-active" : [
                    {
                        "data" : [null]
                    }
                    ],
                    "last-active" : [
                    {
                        "data" : [null]
                    }
                    ],
                    "protocol-name" : [
                    {
                        "data" : "Direct"
                    }
                    ],
                    "preference" : [
                    {
                        "data" : "0"
                    }
                    ],
                    "age" : [
                    {
                        "data" : "00:01:09",
                        "attributes" : {"junos:seconds" : "69"}
                    }
                    ],
                    "nh" : [
                    {
                        "selected-next-hop" : [
                        {
                            "data" : [null]
                        }
                        ],
                        "via" : [
                        {
                            "data" : "fxp0.0"
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            {
                "attributes" : {"junos:style" : "brief"},
                "rt-destination" : [
                {
                    "data" : "192.168.121.102/32"
                }
                ],
                "rt-entry" : [
                {
                    "active-tag" : [
                    {
                        "data" : "*"
                    }
                    ],
                    "current-active" : [
                    {
                        "data" : [null]
                    }
                    ],
                    "last-active" : [
                    {
                        "data" : [null]
                    }
                    ],
                    "protocol-name" : [
                    {
                        "data" : "Local"
                    }
                    ],
                    "preference" : [
                    {
                        "data" : "0"
                    }
                    ],
                    "age" : [
                    {
                        "data" : "00:01:09",
                        "attributes" : {"junos:seconds" : "69"}
                    }
                    ],
                    "nh-type" : [
                    {
                        "data" : "Local"
                    }
                    ],
                    "nh" : [
                    {
                        "nh-local-interface" : [
                        {
                            "data" : "fxp0.0"
                        }
                        ]
                    }
                    ]
                }
                ]
            }
            ]
        },
        {
            "table-name" : [
            {
                "data" : "inet6.0"
            }
            ],
            "destination-count" : [
            {
                "data" : "1"
            }
            ],
            "total-route-count" : [
            {
                "data" : "1"
            }
            ],
            "active-route-count" : [
            {
                "data" : "1"
            }
            ],
            "holddown-route-count" : [
            {
                "data" : "0"
            }
            ],
            "hidden-route-count" : [
            {
                "data" : "0"
            }
            ],
            "rt" : [
            {
                "attributes" : {"junos:style" : "brief"},
                "rt-destination" : [
                {
                    "data" : "ff02::2/128"
                }
                ],
                "rt-entry" : [
                {
                    "active-tag" : [
                    {
                        "data" : "*"
                    }
                    ],
                    "current-active" : [
                    {
                        "data" : [null]
                    }
                    ],
                    "last-active" : [
                    {
                        "data" : [null]
                    }
                    ],
                    "protocol-name" : [
                    {
                        "data" : "INET6"
                    }
                    ],
                    "preference" : [
                    {
                        "data" : "0"
                    }
                    ],
                    "age" : [
                    {
                        "data" : "00:01:24",
                        "attributes" : {"junos:seconds" : "84"}
                    }
                    ],
                    "nh-type" : [
                    {
                        "data" : "MultiRecv"
                    }
                    ]
                }
                ]
            }
            ]
        }
        ]
    }
    ]
}
```

### Getting Your Hands Dirty

Want to reproduce what I described? You'll find the sources in my [netlab-examples](https://github.com/ipspace/netlab-examples/tree/master/Ansible/XML) repository (and might find it useful to use [netlab](https://github.com/ipspace/netlab) to generate Vagrantfile and Ansible inventory and configuration files).