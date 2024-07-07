---
kb_section: ELK
minimal_sidebar: true
title: What Is Elastic Stack?
url: /kb/ELK/015-elk-components/
---
Elastic Stack, formerly known as ELK stack, includes:

- Elasticsearch: the search engine where all your data is stored.
- Logstash: the tool to parse, enrich, and filter data before storing them into Elasticsearch.
- Kibana: the tool to visualize data stored in Elasticsearch.

Elastic Stack also includes Beats -  lightweight shippers (agents lighter than Logstash) to get, parse, and store data:

- Filebeat: used (mainly) to analyze Linux/Unix log files.
- Packetbeat: used to analyze network packets.
- Winlogbeat: used to analyze Windows events.

Elastic Stack includes many other tools, but they are out of the scope of this introductory post.

You can get Elastic Stack as:

- Opensource: downloadable from [GitHub](https://github.com/elastic "GitHub Elastic repository") but also from [Opendistro](https://opendistro.github.io/for-elasticsearch/ "Opendistro");
- Basic: free product with limited features;
- Licensed (Gold, Platinum, Enterprise): including features like auditing, LDAP authentication, alerting, machine learning... (see [subscription page](https://opendistro.github.io/for-elasticsearch/ "Elastic subscriptions") for more details).

## Elastic Common Schema (ECS)

Recently ELK users started to realize that injecting logs is not enough. Correlating logs requires to have in a standard form. ECS is the suggested (not mandatory) format to inject log: each log injected into Elastic Stack should be translated to adhere to ECS format.

If you start using ECS you'll be able to:

- correlate events from different sources
- share and reuse dashboards

ECS covers how documents inserted into Elastic Stack should be structured, but does not (currently) cover indexes. It's also not all-encompassing; for example, it's still missing a reference to email objects.

On the positive side, the ECS maintainers are willing to receive proposals, and are fast enough to discuss and integrate changes into official ECS releases.
