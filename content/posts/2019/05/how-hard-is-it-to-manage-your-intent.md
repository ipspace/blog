---
date: 2019-05-23 09:20:00+02:00
tags:
- automation
- intent-based networking
title: How Hard Is It to Manage Your Intent?
url: /2019/05/how-hard-is-it-to-manage-your-intent.html
intent-based-networking_tag: drawback
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

Remember the "[*every device configuration is really an expression of our intent*](/2018/06/what-is-intent-based-networking.html)" discussion? Forgetting the wrong level of abstraction (we mostly don't want to deal with all the idiosyncratic stuff network devices want to see in their configurations) and box-oriented thinking caused by device-level intent for the moment, let's focus on another aspect: how hard is it to manage your intent?
<!--more-->
For example:

-   If you want to change your intent (in plain English: device configuration), how hard is it to get from current configuration to the new one?
-   How hard is it to see what intent has been passed to the system (in plain English: how is the device or system configured)?

In you're working with decent networking devices you're probably wondering why I'm even bringing up these topics. After all, the answer to the first one is *replace configuration* and the answer to the second one is *show configuration*.

Interestingly, not all network devices support *configuration replace* functionality (for example, **configure replace** was added to Nexus OS in April 2018), and even if a network device supports non-disruptive replacement of its configuration, it might not allow you to replace parts of the configuration without an interesting carefully-choreographed dance of configuration commands.

Note: the only exception I know of is Junos that treats device configuration as a data model that can be manipulated in any way you wish and implemented when you're satisfied with its state. Arista's **config sessions** might work the same way.

Now imagine you're evaluating an abstracted intent-based system with a beautiful GUI and a REST API. Don't forget to ask these questions (and don't back down until you get the answers):

-   Can you easily [replace your intent when you want to](/2018/04/dont-get-obsessed-with-rest-api.html) or do you have to [work through GUI (or API calls)](/2018/05/layers-of-single-pane-of-glass.html) to massage the current state of the system into what you want it to be?
-   Can you see all of your intent in a single place or do you have to [navigate through GUI screens and take notes of what's configured](/2018/06/automation-win-document-cisco-aci.html) (or execute a dozen of API calls to get it)?
-   Can you track a history of changes to your intent?
-   Can you track the changes to your intent with standard version-control tools like Git/GitLab/GitHub/... or do you have to use tools embedded into the system? Are there any such tools available in the system?
-   How easy is it to automate changes to your intent (like implementing the same fix to all tenants configured in the system)?
-   How easy is it to integrate the intent-based system into whatever application testing/deployment pipeline?

{{<note info>}}You might have noticed that the above questions describe *infrastructure-as-code* concepts ;){{</note>}}

Finally, for an overview of intent-based networking fundamentals watch [*Intent-Based Networking*](https://my.ipspace.net/bin/list?id=AutConcepts#INTENT) section of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar, and if want to know even more, register for the [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course (it has a [whole module dedicated to network infrastructure-as-code](https://my.ipspace.net/bin/list?id=NetAutSol&module=7)).
