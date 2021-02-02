---
title: "Demonstrate Small Automation Wins"
date: 2021-02-09 07:10:00
tags: [ automation ]
---
Long long time ago in a country far far away when traveling was still a thing I led an interesting data center fabric design workshop. We covered tons of interesting topics, including automating network services deployments (starting with VLAN self-service for server admins).

As was often the case in my workshops, we had representatives from multiple IT teams sitting in the room, and when I started explaining how I'd automate VLAN deployments, the server administrator participating in the workshop quickly chimed in: "*that's exactly how I implemented self-service for some of our customers, it makes perfect sense to use the same approach for server port and VLAN provisioning*", and everyone else in the room agreed... apart from the networking engineer, who used a counter-argument along the lines of "*we only provision a new VLAN or server port every few days, we can do it by hand*" and no amount of persuasion would move him.
<!--more-->
I don't know how that particular story ended (sometimes I'm positively amazed by results shared by workshop attendees a year or two later, so there's still hope ;), but it's evident we need simple sample solutions to demonstrate the value of network automation through small wins.

You can find plenty of good "small wins" examples in our [Network Automation Solutions Showcase](https://www.ipspace.net/NetAutSol/Solutions)), but they mostly rely on running Ansible playbooks -- not exactly the most user-friendly environment. Even if you add AWX/Tower in front of them the user interface is still heavily tool-focused.

Hans Verkerk decided to go a step further and solve the UI challenge with a Python script, and created a demo VLAN provisioning demo with a [Tk-driven](https://docs.python.org/3/library/tk.html) graphical user interface. He [published the source code on GitHub](https://github.com/hans-vvv/VLAN-configuration-builder); if you feel like a similar solution might come handy browse the code to get some inspiration ;)