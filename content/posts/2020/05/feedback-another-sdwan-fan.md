---
title: "Feedback from Another SD-WAN Fan"
date: 2020-05-14 06:21:00
tags: [ SD-WAN ]
sd-wan_tag: reality
---
I don't know what's wrong with me, but I rarely get emails along the lines of "_I deployed SD-WAN and it was the best thing we did in the last decade_" (trust me, I would publish those if they'd come from a semi-trusted source). 

What I usually get are sad experiences from people being exposed to vendor brainwashing or deployments that failed to meet expectations (but according to Systems Engineering Director working for an aggressive SD-WAN vendor that's just because they didn't do their research, and thus did everything wrong).

Here's another story coming from [Adrian Giacometti](https://www.linkedin.com/in/adrian-giacometti/).
<!--more-->
- - -
This was my first encounter with SDWAN a couple of years ago and I realized that there was no magic, it’s just a Linux with some coding, and if all the traffic has to go trough it, bingo, you can do whatever you want.
 
At that moment I used to ask simple question to the vendors.
 
Me: “How does your device decide which link to use?”
 
Vendor: “They measure the quality and packet loss but you don’t have to worry about it, look at this demo is magic”
 
And it was like magic… but still. For the second time I asked
 
Me: “The question remains, is it a ping? What is it? And how I can influence that decision? The logic? How i can be sure the it will not screw up things with flapping links?”
 
I never had a good answer. Ok let’s continue with the questions
 
Me: “How is the deployment?”
 
Vendor: “It’s easy, one per-site, in the middle of the way of your current devices”
 
Me: “Ok, it’s a little bit disruptive. Does it have a fall back? What happens if your device hangs up. Because I trust my routers? Make me trust in your device…”
 
Vendor: “Eeeh …. Mmmmm”
 
Ok, let’s move on…
 
Me: “I have to deploy them at all the sites or just on the main sites?”
 
Vendor: “It’s not necessary but we recommend that you deploy them at all sites.”
 
Ok, you are just trying to sell boxes. Fair answer.
 
Me: “How my current routing scheme will work if I don’t deploy SD-WAN at all sites?”
 
Vendor: “If traffic will go through SD-WAN devices, no problem”
 
Ok, another thing inserted in my working routing scheme. I assume it might work, but…
 
Me: “Ok then, how much does it cost because I might need a lot of boxes?”
 
Crazy expensive… for a Linux server.
 
Ok… I believe in progress, but you are trying to sell me something that is not as magical as you say, it’s just a nice compilation of old and very basic techniques with a beautiful GUI. And I say “very basic techniques” mainly because it seems to use only ICMP for calculations, it works as-is, and I can’t modify or check it further. Or at least you are not willing to give me more low-level details.
 
So, I like the concept, but I have to go back to [your premise](/2019/03/lock-in-and-sd-wan-match-made-in-heaven/), this is a lock-in and nothing so new, it’s just the ability to code faster than some big players.
 
Or like when I started to study OpenStack and VMWare-NSX… what? They all use the concept of the old fellow Linux-bridge and tunnel interfaces!

And I hit my forehead… of course… remarketed old concepts just that with some additional coding you can scale easily.