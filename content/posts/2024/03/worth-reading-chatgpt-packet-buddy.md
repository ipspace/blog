---
title: "Worth Exploring: PCAP Analysis with Generative AI"
series_title: "PCAP Analysis with Generative AI"
date: 2024-03-09 08:16:00+0100
tags: [ worth reading, AI ]
---
[John Capobianco](https://www.linkedin.com/in/john-capobianco-644a1515/) published the source code of his 
[Packet Buddy](https://github.com/automateyournetwork/packet_buddy) application on GitHub. It's a Python UI that takes a PCAP file, converts it to JSON, and includes that JSON as part of the ChatGPT chat, allowing you to discuss the captured packets with ChatGPT.

His idea is one of the best uses of generative AI in networking I've seen so far, as long as you remember that you're dealing with an overconfident intern who has no problem making up an answer just to sound smart. Have fun!

Finally, if you don't want to use ChatGPT (I wouldn't blame you) or send captured data into The Cloud, someone already [adapted his idea to use local LLMs](https://github.com/kspviswa/local-packet-whisperer).