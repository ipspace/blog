---
kb_section: ELK
minimal_sidebar: true
pre_scroll: true
title: Using Elastic Stack in Networking and Security
toc_title: Using Elastic Stack
url: /kb/ELK/020-elk-for-network-engineers/
---
Any information system gets through many incidents every year. Most of them are light, but (hopefully) very few can be very serious. The key to resolve incidents fast enough, additionally resulting in a valuable "lesson learned," is visibility.

I would define visibility as the ability to have a clear view of what's going in information systems. I also would point out that using a _single pane of glass_ helps more than having multiple dashboards; specialized dashboards help to drill down into details during an investigation, but a _single pane of glass_ is usually the best starting point for initial analysis.

We commonly use SIEM (Security Information and Event Management) systems to help us collect logs and get them automatically analyzed. SIEMs are also the preferred solution to sort security logs and to analyze security incidents.

However, if you want to manage information systems successfully, you need more: ELK is the perfect bucket to store and analyze all logs (analysis could be manual or automatic). You could also use ELK as a log management platform with advanced features like machine learning.

To give you a few examples - you can do all these things (and many more) with Elastic Stack:

* Real-time traffic analysis: ELK can receive, store and visualize Netflow/IPFIX flows, helping you to figure out average utilization, bottlenecks, and anomalies.
* Network device events: SNMP traps and Syslog messages can be parsed and analyzed in real-time.
* Security logs: firewall, IPS, DNS, VPN concentrator, user authentication logs can be ingested and correlated with each other to find malicious activities, lateral movements, or privilege escalation.
* Application anomalies and performance: ELK can also help to troubleshoot application problems in terms of availability, anomalies, and performance.


## A Simple ELK(B) Architecture

Enterprise-level scalable and resilient ELK architectures will be discussed in the future. We'll start with a simple ELK configuration useful as a learning lab:

{{<figure src="../elk-1.png" caption="A simple ELK(B) architecture">}}

- Logstash is the first log receiver you'll focus on to ingest Syslog and NetFlow logs. Logstash parses and enriches logs before storing them to Elasticsearch.
- Beats are agents installed into Linux or Windows systems to collect logs. Beats can write directly to Elasticsearch, but I usually prefer to pass them trough Logstash for enrichment.
- Elasticsearch receives structured logs in JSON format from Logstash, Beats, or directly from other sources (i.e. Python scripts).
- Kibana calls Elasticsearch and visualizes data in customizable dashboards and reports.

## Starting with ELK

ELK is not a "plug and play" solution. ELK is an extensible, flexible, and scalable big data solution. Take that into account.

I suggest you start your Elastic Stack journey with these steps:

- build a monolithic Linux-based environment with Elasticsearch, Logstash, and Kibana;
- acquire logs from network devices using syslog protocol (Logstash);
- learn how to parse logs into a structured format (Logstash)
- learn how to create some visualizations (Kibana)
- acquire Netflow logs. You can use Logstash to collect them, even if the performance is not very good.
