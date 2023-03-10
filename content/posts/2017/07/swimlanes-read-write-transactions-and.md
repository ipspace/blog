---
date: 2017-07-04 08:12:00+02:00
high-availability_tag: app
tags:
- design
- data center
- WAN
- high availability
title: Swimlanes, Read-Write Transactions and Session State
url: /2017/07/swimlanes-read-write-transactions-and.html
---
Another question from someone watching my [*Designing Active-Active and Disaster Recovery Data Centers*](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar (you know, the one where I tell people how to avoid the world-spanning-layer-2 madness):

> In the video about parallel application stacks (swimlanes) you mentioned that one of the options for using the R/W database in Datacenter A if the user traffic landed in Datacenter B in which the replica of the database is read-only was to redirect the user browser with the purpose that the follow up HTTP POST land in Datacenter A.

Here's the diagram he's referring to:
<!--more-->
{{<figure src="/2017/07/s1600-AA-Redirects.jpg">}}

Just in case you're wondering why someone would go for an architecture that seems complex: several people running e-commerce sites told me that they see more than 99% of read-only transactions. Also, expecting to get transactional consistency across multiple active-active data centers is a recipe for disaster (see also: [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)).

{{<note info>}}A major difference between an application-layer solution and stretched VLANs is that in one case you own the complexity and can thus manage it.{{</note>}}

Continuing with the question...

> In that case wouldn\'t the Web/App servers in Datacenter A need to know the session already created for the user in Datacenter B Web/App servers?

Absolutely. They would need to:

-   Recognize the session cookie (so the user doesn't have to log in again) or use some other mechanism to authenticate user based just on user-supplied information (see [Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol)));
-   Have access to the data needed for R/W transaction.

I would probably use an eventually consistent database (MongoDB, for example) to solve the second challenge, and assume that the user data (for example, shopping cart) arrives to DC-A before the user clicks the \"Purchase\" button. I would also put some simple checksum (or calculate a hash) of the data to verify it got there, or start the checkout process (*review your shopping cart* phase) in DC-A. Alternatively, you could process all "add to basket" transactions in DC-A so the data is already there (shipping a copy to DC-B in case DC-A fails).

{{<note>}}In any case, if the user arrives into DC-A before the data does, you have a serious communication problem between DC-B and DC-A, and it's time to admit the failure.{{</note>}}

Long story short:

-   Try to make your solution [*as simple as possible, but not simpler*](http://quoteinvestigator.com/2011/05/13/einstein-simple/);
-   Solve the complexity on the application layer considering all potential failure scenarios (including *user can see DC-A and DC-B, but they can't see each other*)
-   Recognize that distributed systems always involve [byzantine failures](https://en.wikipedia.org/wiki/Byzantine_fault_tolerance) (see also [this NASA document](https://c3.nasa.gov/dashlink/static/media/other/ObservedFailures1.html)) and that sometimes the best thing you can do is to admit the failure to the user and ask her to recover instead of failing in obscure and undocumented ways.

Have you learned something new? Guess how much more you'd learn in [Building Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course ;)
