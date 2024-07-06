---
date: 2008-02-13 07:04:00.003000+01:00
tags:
- BGP
title: AS-path Based Filter of Customer BGP Routes
url: /2008/02/as-path-based-filter-of-customer-bgp.html
---
Any serious (or at least security-aware) ISP should not blindly accept BGP routes from its customers but at the very minimum do some sanity checks on them. For example, if a multi-homed customer is clumsy enough to advertise BGP routes between service providers, it's nice if you still stop him from turning into a transit AS. The required filter is conceptually quite simple: all the BGP routes from the customer should contain only his AS number in the AS-path.

The initial non-scalable approach is obvious: accept only the AS paths that have exactly the customer's AS number in the AS path. For example, if your customer's AS number is 65001, you could use this filter: **ip as-path access-list 100 permit \^65001\$**.
<!--more-->

{{<note>}}The *caret sign* at the beginning of the string and the *dollar sign* at its end are mandatory; otherwise the **as-path access-list** will match any AS-path with the string 65001 in it.{{</note>}}

A more generic approach might recognize that the AS path received from the customer shall contain a single AS number, so the filter can be rewritten as **ip as-path access-list 100 permit \^\[0-9\]+\$**, where the expression **\[0-9\]+** matches *one or more digits* (also known as *a number*).

Both filters described above have a common problem: they fail if the customer is using [AS-path prepending](/2008/02/bgp-essentials-as-path-prepending.html). In those cases, you should accept all AS-paths that contain a single number (potentially repeating multiple times). The explicit filter is simple: **ip as-path access-list 100 permit \^65001(\_65001)\*\$**. This filter matches all AS paths that start with 65001 and contain zero or more occurrences of a delimiter (whitespace) followed by 65001.

Writing an implicit AS-path filter that recognizes AS-path prepending is trickier and requires the use of pattern recall -- part of regular expression could match a pattern recognized earlier in the regular expression. In our case, the first AS number recognized could be repeated many times over as expressed with this cryptic filter: **ip as-path access-list 100 permit \^(\[0-9\]+)(\_\\1)\*\$**. The **\\1** part of the filter is pattern recall and matches whatever was matched within the first parenthesis (the first AS number in the AS path).
