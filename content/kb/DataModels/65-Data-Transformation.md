---
kb_section: DataModels
minimal_sidebar: true
title: Data Model Transformation Concepts
url: /kb/DataModels/65-Data-Transformation/
---
Our journey took us from the [initial simplistic data model full of duplicate data](index.html) to [highly optimized data model with automatic IP address allocation](40-Link%20Prefixes.html). However, as we kept simplifying the data model and squeezing out redundancies, the complexity of our templates increased dramatically &ndash; we replaced explicit (data) complexity with hidden (template) complexity.

While it's hard to reduce overall system complexity, sometimes we can at least control where we want to have it. It doesn't make sense to push the complexity onto system operators; after all, we use network automation to make changes to the network more reliable, and burdening operators with a complex data model will not get us there. 

It also doesn't make sense to intertwine complex logic with device configuration templates, in particular if we plan to use multiple device types or even network operating systems. In that  case, we would have to have the same logic repeated in every device template or use complex Jinja2 constructs like macros and includes.

Many successful network automation platforms like Cisco NSO or Apstra AOS use multiple data models &ndash; a high-level data model that is easy to work with, a low-level data model that can be directly transformed into device configurations, and a transformation engine that dynamically converts data from high-level data model into low-level data model(s).

**Notes:**

* This approach is commonly called *data model transformation*, but we're not *transforming data models* ([abstract formalizations of the objects and relationships found in a particular application domain](https://en.wikipedia.org/wiki/Data_model)) but *converting data* organized according to one data model into a format described by another data model.
* This approach is sometimes called *intent-based networking* because that sounds much better than *data model transformation*.

## Data Transformation Implementation Options

Your network automation solution could transform data from abstract (high-level) data model into device-level data on the fly (ever time it is needed), on every change to the high-level data model, a combination of both (first time the data is needed after the high-level model has been changed), or periodically. The best approach depends on how complex and time-consuming the transformation is, and whether it's possible to detect a change in the high-level model.

For example, it's extremely easy to detect changed data if your high-level model is a set of YAML text files controlled with Git &ndash; the data transformation is performed every time a commit is merged into the master branch. On the other hand, it's hard to detect changes in relational databases unless the application making the changes implements some logging logic.

{{<note note>}}You could use UPDATE triggers to detect changes to database tables, but you probably don't want to go down that path.{{</note>}}

Complex data transformation or transformation involving numerous lookups into external data sources is best performed in a dedicated transformation program... but if all you need is something simple you might be able to get it done with a Jinja2 template transforming internal data structures into YAML-formatted text.

If you're using Ansible to generate and deploy device configurations, you could store the resulting YAML document as **host_vars** file, and Ansible would automatically use it the next time you'd run an Ansible playbook. You could also do the transformation on-the-fly within an Ansible playbook using **template** lookup to perform the transformation, and **from_yaml** filter to parse the results back into an internal data structure.

{{<note warn>}}Using a Jinja2 template to perform data transformation might result in [write-only code](https://blog.ipspace.net/2018/04/avoid-write-only-code.html). Even [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/complex_data_manipulation.html) agrees that *Ansible is not recommended as a data processing/manipulation tool*.{{</note>}}

<!-- need a comment -->
