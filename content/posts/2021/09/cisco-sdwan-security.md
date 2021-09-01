---
title: "Another SD-WAN Security SNAFU: SQL Injections in Cisco SD-WAN Admin Interface"
date: 2021-09-21 06:43:00
tags: [ SD-WAN, security ]
---
[Christoph Jaggi](https://www.ipspace.net/Author:Christoph_Jaggi) sent me a link to an interesting article describing [security vulnerabilities pentesters found in Cisco SD-WAN admin/management code](https://www.sstic.org/media/SSTIC2021/SSTIC-actes/the_security_of_sd-wan_the_cisco_case/SSTIC2021-Article-the_security_of_sd-wan_the_cisco_case-legras.pdf). 

I'm positive the bugs have been fixed in the meantime, but what riled me most was the root cause: [Little Bobby Tables](https://xkcd.com/327/) (aka SQL injection) dropped by. Come on, it's 2021, SD-WAN is supposed to be about building secure replacements for MPLS/VPN networks, and they couldn't get someone who could write SQL-injection-safe code (the top [web application security risk](https://owasp.org/www-project-top-ten/))?
