---
cli_tag: api-use
date: 2019-06-18 08:07:00+02:00
series:
- ssot
- cli
ssot_tag: details
tags:
- automation
- data models
title: Read Network Device Information with REST API and Store It Into a Database
url: /2019/06/read-network-device-information-with/
---
One of my readers sent me this question:

> How can I learn more about reading REST API information from network devices and storing the data into tables?

Long story short: it's like learning how to drive (well) - you have to master multiple seemingly-unrelated tasks to get the job done.
<!--more-->
**Starting with the big picture**: Don't get over-excited. REST API (on network devices) is usually a subset of what you can do with CLI, most commonly mapping a single CLI command into a single REST API request.

While there are some emerging standards like RESTCONF, most often REST API is device-specific (apart from riding on top of HTTPS and using JSON or XML encoding), so you'd have to read the developer documentation for the platform you're interested in (hoping the \$vendor managed to create somewhat-decent documentation).

Next, **the mechanics of getting it done**. You have to:

-   Figure out what devices you want to work with (inventory)
-   Authenticate to the device(s) - usually using username+password, sometimes executing a sequence of calls to log in and dealing with custom HTTP headers to pass authentication token to the device
-   Execute REST API calls to collect data
-   Store the data into some data store.

After we know what needs to be done, it's time to **select the best tool for the job**. You could execute REST API calls through Ansible networking modules (assuming the device is supported by Ansible, has REST API, and the Ansible team implemented REST API access to the device) or from any programming language (Python being the most popular these days).

I covered the general principles of [selecting the optimal tool](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S4A) in [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course, and [information retrieval with Ansible](https://my.ipspace.net/bin/list?id=Ansible#NET_CMD) in [Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers) webinar and online course. If you prefer using a programming language, check out "Learning \$SomeLanguage" or "Programming \$SomeLanguage" books - executing HTTP calls is a very common programming task these days and should be covered in details in any decent programming language material.

Successfully executing REST API calls is not the end of the story. My reader wanted to **store the retrieved information**. REST API calls usually return structured data (example: VRF -\> interface -\> ARP entry) that you cannot simply push into a database table. You could either:

-   Save structured data directly into a database or into text files. Easy to implement, but you're just pushing complexity into the future (aka "Technical Debt"). Searching for specific bit of information (like "when did the ARP mapping for this IP address change") would be great fun unless you use something like ElasticSearch
-   Create multiple records (example: VRF,Interface,MAC,IP) from returned data and insert them into one or more relational database tables. MySQL would be a typical database to use, and the books I mentioned above should cover working with relational databases as well.

Finally, while "*retrieving ARP table periodically and store changes in a database*" might be a fun science project, keep in mind that your true value isn't being a stumbling Python beginner but being a high-quality networking engineer. When creating a production-grade system you have to know *what information to collect* and *how to make it relevant* and offload the implementation details to someone who spent years becoming an excellent programmer.
