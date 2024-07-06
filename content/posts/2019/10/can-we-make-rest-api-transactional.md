---
cli_tag: api-challenge
date: 2019-10-22 08:27:00+02:00
niac_tag: rest
series:
- niac
- cli
tags:
- automation
- SDN
title: Can We Make REST API Transactional Across Multiple Calls?
url: /2019/10/can-we-make-rest-api-transactional.html
---
I got interesting feedback from one of my readers after publishing my [REST API Is Not Transactional](/2019/04/rest-api-is-not-transactional.html) blog post:

> One would think a transactional REST interface wouldn't be too difficult to implement. Using HTTP1/1, it is possible to multiplex several REST calls into one connection to a specific server. The first call then is a request for start a transaction, returning a transaction ID, to be used in subsequent calls. Since we're not primarily interested in the massive scalability of stateless REST calls, all the REST calls will be handled by the same frontend. Obviously the last call would be a commit.

I wouldn't count on HTTP pipelining to keep all requests in one HTTP session (mixing too many layers in a stack never ends well) but we wouldn't need it anyway the moment we'd have a transaction ID which would be identical to session ID (or session cookie) traditional web apps use.
<!--more-->
However, the real problem lies in the way REST API servers are usually implemented.

Let's evict the obvious elephant from the room before you rush to point out that *every single REST API call* is transactional. I hope that's true, but I don't care about that. What I'd like to have is:

-   The ability to roll back five independent changes to the system if one of my changes fails;
-   Ideally the ability to make changes that are not visible to the outside world until the **commit** REST API call.

Implementing such a system is trivial if the REST API calls do nothing more than [modify the data model which is then instantiated once we execute the **commit** call](/2018/09/adjusting-system-state-with.html).

Unfortunately most systems (or network devices) don't work that way because it's much simpler to [execute a function call within the system and modify system state the moment a REST API call is received](/2018/09/infrastructure-as-code-netconf-and-rest.html) or a command is typed in the CLI.

Even worse, the execute-changes-immediately paradigm is so widely accepted that it's totally unrealistic to expect that we'll get transactional configuration consistency we have with Junos, IOS-XR or Arista EOS in SDN controllers, orchestration systems or intent-based products (isn't it great to have three marketing names for the same stuff?) with rare exceptions like Cisco APIC.

Like they say, sometimes you're too busy to yammer to realize what you had until you lose it... Welcome to the brave new RESTful world.
