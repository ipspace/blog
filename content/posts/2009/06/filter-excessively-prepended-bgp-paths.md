---
date: 2009-06-15 07:00:00.005000+02:00
tags:
- BGP
title: Filter Excessively Prepended BGP Paths
url: /2009/06/filter-excessively-prepended-bgp-paths/
---
A few months ago, a [small ISP was able to disrupt numerous BGP sessions in the Internet core by prepending over 250 copies of its AS number to the outbound BGP updates](/2009/02/root-cause-analysis-oversized-as-paths/). While you should use the **bgp maxas-limit** command to limit the absolute length of AS-path in the inbound updates, you might also want to drop all excessively prepended BGP paths.

For more details, read the [*Filter Excessively Prepended BGP Paths*](/kb/tag/BGP/Filter_Excessively_Prepended_BGP_Paths/) article.