---
date: 2008-12-02 07:06:00.002000+01:00
tags: []
title: I’m Too Old … I Prefer CLI over GUI
url: /2008/12/im-too-old-i-prefer-cli-over-gui/
---
I was delighted when I got access to **Cisco's Application Control Engine (ACE) XML Gateway/Web Application Firewall (WAF) box**. This box is the perfect intersection of three fields that really interest me: networking, security and Web programming. To my huge disappointment, though, all the real configuration can only be done through the Web interface. I understand that casual users of a device prefer a graphical user interface (GUI) over text commands (and Generation Z has never seen a terminal window, DOS prompt or, God forbid, an actual terminal), **but you can achieve so much more with a simple text-based configuration approach:**
<!--more-->
**Working is more efficient.** Unless you use only one index finger (positioned on the mouse) to work with your computer, you work faster in text-only mode once you become proficient with the device. If you know the configuration commands, you just type them; there's no need to navigate a complex hierarchy of menus, forms and drop-down options. Just imagine the mental pain you would experience if you had to configure the BGP routing on a Cisco router through a menu interface.

**Troubleshooting is easier.** If you're faced with a dire network-down situation, you can quickly adapt the configuration of an actual device by using the command line. With the GUI and distributed Manager/Gateway architecture, you have to log into the Web interface of the Manager device, work your way through the menus while the ringing phone is jumping up and down on your desk, make the changes you think might solve the problem and deploy the changes to the actual Gateway devices.

**Configuration backup is easy.** Once you configure a device that uses text-based configuration, you can store the configuration in a text file, having an almost perfect backup of the state of the working device (private keys might be an exception). I haven't found a good way to back up the whole configuration of an ACE XML Gateway that would allow me to drop a replacement box in the network with a simple copy/paste operation from the console terminal.

**You can identify the changes.** Given two text-form device configuration files (a working one and a broken one), it's feasible to use simple text-comparison tools to spot major differences and use your common sense to work from there. GUI interfaces have no such highly adaptable tool. The GUI solutions might give you reporting and configuration-comparison tools, but you never know whether they really consider all configuration parameters in the reports.

**You can develop a library of "configlets."** Numerous blogs describe various aspects of Cisco IOS configuration, and you have probably built your own private library of useful configuration bits and pieces. These tools are useful because they can present the relevant information in highly condensed form: text configuration commands that you can immediately test and use. If I want to give you a useful tip about WAF configuration, I can describe the menu paths to get to the setting you need to change and post some screenshots. It might get the job done, but it will never be as fast and efficient as posting a few lines of text.

Don't get me wrong; I understand that some people need GUIs and that the vendors need to implement a GUI to retain (or increase) market share. But the **minimum we should get is a dual-interface solution**, like the Cisco IOS/Secure Device Manager (SDM) or Wide Area Application Services (WAAS) configuration.

{{<note>}}This blog post has earned me another affectionate nickname from *Red Pineapple*. On top of *holy cow* (not to mention *Pineapple Certified Religious Bovine Professional*) I became *telnet jockey*. Unfortunately his blog posts are long gone, so I had to remove the original links when updating this one.

On a more serious note, I agree with him on the need of visualization, but most GUIs I've seen look more like [eye candy](http://www.merriam-webster.com/dictionary/eye+candy) than a useful visualization tool.{{</note>}}
