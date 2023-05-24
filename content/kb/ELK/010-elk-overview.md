index: yes
toc_title: Overview

In recent years network engineers turned from CLI jockeys into a hybrid between an application developer and a networking expert... what acronym-loving people call NetDevOps. In practice, a NetDevOps engineer should be able to:

- manage and troubleshoot networks;
- helps to troubleshoot any information system issue (including "slow" applications);
- automate networking tasks;
- monitor network and application performance;
- continue auditing the infrastructure, eventually using (partial) automation to make it less time-consuming;
- and do everything else not covered by other IT teams.

To get there, NetDevOps started to learn Linux, Python, and automation frameworks. In this article, we'll add **log management** to the mix.

Log management is the ability to collect any event from information systems and get them automatically analyzed to help NetDevOps react faster to information system issues.

There are many commercial or open-source log management platforms; I would mention:

- [Graylog](https://www.graylog.org/)
- [Elastic Stack](https://www.elastic.co/)
- [InfluxDB](https://www.influxdata.com/)

Each one of these has a different focus: Graylog was born as a log management solution, Elastic Stack is a Big Data solution, and InfluxDB is a time-series database.

We won't go into discussing the pros and cons of these products. There are already plenty of blog posts doing that.

I chose to work with Elastic Stack because of its:

- flexibility: I'm able to inject logs from almost any device I encountered;
- scalability: I can manage hundreds or thousands of log messages per seconds without any issue;
- integration: I'm able to build a very robust solution that includes other open-source components.
- vision: I honestly like where Elastic company is going, and I agree with its vision.
