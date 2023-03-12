---
title: High Availability in Private and Public Clouds
layout: custom
minimal_sidebar: true
sidebar_box: HA
---
Migrating your applications into a private or public cloud won't solve it's high availability challenges. Public cloud infrastructure is usually designed for application developers that know what they're doing; to make the most out of a public cloud deployment your applications have to be well-designed. For more details read:

{{<series-listing tag="intro" year="yes">}}

{{<plushy magic>}}Typical enterprise software development organizations disagree with that gloomy view, and virtualization vendors are more than happy to build an alternate-reality world for them in which stretching subnets and migrating live virtual machines into a public cloud makes sense. Unfortunately, the laws of physics don't care about vendor marketing.

{{<series-listing tag="stretch" weight="yeah" year="yes">}}

{{<plushy master>}}When your application developers figure out they have to respect the laws of physics your work has just started -- you have to design your virtual networking environment before the applications are deployed, carefully considering failure domains usually known as *availability zones* and *regions*:

{{<series-listing tag="design" weight="need it" year="yes">}}

{{<plushy happy>}}Finally, if you plan to build a private cloud infrastructure, you might find these blog posts useful:

{{<series-listing tag="private" year="yes">}}

Want to know more? Explore the [cloud networking webinars](https://www.ipspace.net/Cloud), in particular:

* [Networking in Private and Public Clouds](https://www.ipspace.net/Networking_in_Private_and_Public_Clouds)
* [Amazon Web Services Networking](https://www.ipspace.net/Amazon_Web_Services_Networking)
* [Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking)
* [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers)
