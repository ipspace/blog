---
date: 2018-02-19 11:15:00+01:00
tags:
- automation
series: [ niac ]
niac_tag: principles
title: Automation Isn’t About Building a Button to Press
url: /2018/02/automation-isnt-about-building-button/
---
*This is a guest blog post by* [*Carl Buchmann*](https://www.linkedin.com/in/carl-buchmann-6b436727/)*, Managing Solution Consultant at TeraMach. Carl attended the* [*Building Network Automation Solutions*](http://www.ipspace.net/Building_Network_Automation_Solutions) *online course in 2017.*

There is one thing I regret not doing sooner during my automation journey, and that is adopting Git and a proper IDE/text editor that has built-in source control management. I personally use Microsoft Visual Studio Code, as it has Git built in and has many great extensions to validate code syntax.
<!--more-->
At the time, I was a little overwhelmed with all the technology I had to learn or re-learn. Git took the wayside, unfortunately\... but once I adopted Git in my daily practice, I realized the benefits of treating Infrastructure as Code, as did the clients I worked with.

{{<note info>}}Mastering automation concepts, making a consulting practice out of deploying them, and sharing them with the customers seems to be a pretty common theme. [Mark Prior](http://www.ipspace.net/Author:Mark_Prior) talked [about a similar approach](http://my.ipspace.net/bin/list?id=xNetAut181#INFRA_AS_CODE) during [his presentation](http://automation.ipspace.net/Public:1-Getting_Started#Guest_speakers) in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.{{</note>}}

Without leveraging Git, the Ansible playbooks I developed were just another scripting language the teams had to learn (although a very powerful one), but once I started demonstrating Software Development Lifecycle (SDLC) techniques to the infrastructure teams that was the real game changer! It actually made us faster at developing new scripts/code and enhanced the collaboration between us.

I've been focusing a lot lately on applying SDLC techniques to manage Infrastructure as Code and using the Agile framework and branching strategies to achieve change as opposed to traditional RFCs. Because automation isn\'t about building a button to press when it\'s time. It\'s about creating an automation framework that automatically adjusts the infrastructure to your definition of it!
