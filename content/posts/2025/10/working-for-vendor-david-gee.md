---
title: "Working for a Vendor with David Gee"
date: 2025-10-07 08:23:00
tags: [ Software Gone Wild, netlab, podcast ]
netlab_tag: podcast
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_201-Working_for_a_Vendor_with_David_Gee.mp3
---
When I first met David Gee, he worked for a large system integrator. A few years later, he moved to a networking vendor, worked for a few of them, then for a software vendor, and finally decided to start his own system integration business.

Obviously, I wanted to know what drove him to make those changes, what lessons he learned working in various parts of the networking industry, and what (looking back with perfect hindsight) he would have changed.
<!--more-->
We also managed to keep the "everything was better in the old days" routine to a minimum, but couldn't resist commenting on the "everyone should become a programmer" stupidity. The results are in [Episode 201](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_201-Working_for_a_Vendor_with_David_Gee.mp3) of the [Software Gone Wild podcast](https://www.ipspace.net/Podcast/Software_Gone_Wild/).

After recording the podcast, David sent me a long email with more details on some points he was making during the podcast. Enjoy!

---

Chatting with Ivan is always a challenge. There's some history and familiarity with each other, so it's all too easy to slip into "friend rant" mode whilst being recorded, also the second danger is talking about assumed knowledge and assuming that the audience is in on the experience, which invariably they might not be. I made some comments on the podcast which might get you shouting swear words in my general meta-direction and never finished off some of the commentary.

### Create, build experience, and accept you will get a lot wrong

Creating anything, is a wonderful experience. But, don't be fooled, some of your babies will be ugly, hairy deformed monstrosities that need to be Sparta kicked over a cliff. Great for learning from and scaring your enemies andI fear due to our socio-economic climate, calling out truth is mislabelled as an act of international terror. It isn't. Your code will be crap, non-idiomatic and will be full of performance and security issues. Get over it, laugh it off and do the next thing, but also save it. I promise, looking back on your creations will make you smile and give you some funny stories to share in the future. I'll give you just one of many to laugh at.

In the early 2000s, I wrote a simple control system for a solid fuel burning boiler system. These burners are in use across the UK and are quite efficient, burning waste food products to about 95% or higher burn efficiency, providing power and heat to buildings and businesses. In the early development work, the code was about 80% in C and 20% in assembly. I had learned C from the infamous K&R book for this project then applied it to some 8 bit MCUs, which talked to each other over UART over different interconnected PCBs, exchanging a very simple form of XML. These CPUs had single cores and I wrote the real-time OS that they ran, which was essentially a control loop with data acquisition and task scheduler. It worked like a charm! The machines ran gloriously well. One day, the phone rang, asking me to visit the development rig in the factory for a meeting. I went to site, to be met by the owner of the manufacturer of the machines and a control system electrical engineer. Turns out, the system had an issue. Under very specific circumstances, there was an odd state. The machine backfired and would turn the cold water head tank into a boiler; the result was it blew the lid off and nearly took the ceiling off. After everyone had stopped laughing, addressing the seriousness of the situation, the fix was one missing exclamation mark on a logical AND condition. Despite my best efforts, countless hours of testing and building, I still nearly managed to burn a factory down.

### Grounding background

Are you prepared not to be the smartest person in the room on a subject? The first time I brought a network online, it was a frame-relay point-to-multipoint system. It took me about three evenings of configuration work reading from a CCNA book. I was ecstatic. I was also living at home with my parents and you couldn't shut me up about it. I was beyond excited.

What I didn't really appreciate at the time was that joy and experience was for me and me alone. Can you imagine me walking into to an ISP and declaring "Stand aside! For I know the power of the DLCIs".

Learning anything is a journey through the quadrant of knowledge:

- You know what you know
- You know what you don't know
- You don't know you what you know
- You don't know what you don't know

Knowing what you know and being happy with it is the saddest state and thinking you know what you don't know is also called naivety. The other states are nice. Not knowing what you know is a smile maker. Sometimes you read something that doesn't make sense...until it does. The last phase is where all of the pain but beauty comes from in my opinion. This quadrant represents a curse; the knowledge curse. The more you know, the more you realise you don't know.

On the podcast, I rapidly called Synadia out for having uber skilled engineers, and I did that because it was a career highlight. Most companies are blessed with senior, experienced engineers. Another key lesson I picked up, was to spend time with the experienced engineers and opinionated people. Whilst they might have wonky controls, uncover their journey. I guarantee you'll find a source of knowledge, entertainment and it might build you a solid relationship with covert executors.

### The core rant

Something I've seen a lot is the expert beginner romantic honeymoon, where you're power drunk on new knowledge. I KNOW THE POWER OF FOR LOOPS! A sobering thought is that thousands of people have come before you and thousands will come after. Others have this knowledge and whilst it might be understood in different ways and exposed differently to the outside world, it's the same set of readily discoverable mechanics underneath. Two people can learn the same word and yet, pronounce it audibly uniquely and apply it differently in the written form.

When delivering workshops, I'm high on engagement and try hard to deliver concepts before digging into implementation detail. This is where fresh water meets salt water. The enthusiastic learner is convinced due to the lack of implementation detail at this point, they know more and are keen to lead the class *(ref, the knowledge quad)*. I had a memorable moment around loops and conditional logic, where an onlooker almost pushed me to once side to explain to a group of network engineers about different loop types in Python. Not long before, this gentleman had shown me an entire Python script as a single function call and was basking in new knowledge.

I wish I could say I haven't been a jerk, but at times, I've gone well and truly beyond that. Network automation is something I've been involved in for a long time, but I went through a phase where I assumed everyone knew what I knew and stopped talking about it. One day, someone sat me down to explain what network automation was, and asked lots of loaded questions for self-gratification. Ashamedly, I tore the guy to bits and vowed after this moment to be a better person. So, no, not everyone knows who are you, what you know and neither should they. This lead to a critical realisation that communication is the number one skill that requires development. There is a one to one relationship between  experience and communication skills. If one goes up so does the other.

Another sin I'm guilty of is assuming that everyone wants to learn the same way, the same content and sacrifice a social life in the pursuit of knowledge. It's not a crime to not want that and I'm thanks to a few people who reminded me that there is a thing called a life outside of networking and software. Who knew.

### Know your audience

Fortune has smiled down on me. I've been on sales training, marketing training, negotiation, marketing and all sorts of soft skill stuff. I'm a natural waffler (can't you tell?) and talk too much. Some other hard lessons include not hose piping a sales team to death with tech and also not setting up a VP with some terrible panel questions. The higher you go up in a business, the less guidance is provided by their stake holders. Looking up from the bottom, it might appear wishy washy, but the risk that senior leaders carry is significant. Just because they don't share the details it doesn't mean those leaders don't know. Some of the leaders I've worked for are some of the most capable and knowledgeable people I've ever met and that includes tech. They've been there, got the full wardrobe of tshirts and have dealt with an immense amount of risk. They also might be skilled at giving you enough rope to hang yourself with.

### The toolbox, house, town, city, and country

I vanished from networking for a few years and came back, surprised to learn that progress has been almost immeasurably slow. Not a whole lot changed in three years. The arguments on tooling is still alive and seems to get recycled with the increasing number of engineers joining the party.

Being more specific, learning a bit of a programming language and learning a bit of Git, is kind of like saying, I have two Torx bits for my screwdriver, but know nothing else about the mechanical world. I mention on the podcast it's achievable for most of us to get to an 80% network engineer and 80% software engineer, but what I didn't mention explicitly is that percentage measurement is against a seasoned engineer with a deep but narrow set of skill. When networking and software worlds collide, the 80% lands you at competent engineer, which is good enough. Experts are rare. The experts that can apply this knowledge properly, even rarer.

My old man rant and unpopular fact, is Git and a bit of agnostic Python is one of the earliest steps you can take in the software journey and some of the earliest tools you put in your apprentice bag, but if the first thing you learn is loop semantics from Python, you'll become blindly biased too early in your journey. In essence, you're concentrating on putting countersunk screws in a wardrobe door, not building a city. Another truth here is, this door might be from an Ikea set. Are you assembling or building from scratch? Putting a screw in an Ikea set or a custom build might be the same core skill, but building a wardrobe from your imagination to physical manifestation is a different journey to the Ikea assembly. Sure you get a wardrobe, but it's the difference between following instructions and being a creator.

So much history has come before us and it's worth following some computer science curriculum to widen your learning funnel. It's safe to say, you don't know what you don't know and that is a lot. Every day I feel like a moron for not knowing something. It's great. My book collection consists of lost knowledge, things I've found from the 1950s to the latest books on machine learning and eBPF. Every day is a learning day.

A lesson I hold dear is, whilst I’m being pedantic about making furniture, others are building cities. Being harmonious and doing the best job of where are you in your career still contributes to the bigger picture, whether you know it or not. I walk around London sometimes and smile, remembering what projects I was involved in, what I delivered and where I messed up. It’s great.

### Fin

With new skills and new knowledge comes the risky bit. Do you overcomplicate everything you touch, or use those powers for good and reduce complexity whilst meeting requirements? Not everything needs to be automated and not everything needs a schema. Not everything has to be clever. Sometimes and most of the time, the simplest answer means you understand the problem deeply and have found the best solution. Ask questions and listen more. What does your business do? Do other people share the same opinion? How does your business unit transact with that other business unit? The questions are never ending and telling the customer no is often an outcome of finding out rich information. Sometimes saying “No” is the best answer and helping folks to understand why is a skill.

No blog post would be complete without an AI section and I use and abuse AI agents to do menial tasks I can't be bothered to do, like updating documentation, writing unit tests and mending CI platforms. I know how to do those tasks, but don't want to spend the time. Vibe coding is fun when you know what to do and  AI is a great accelerator. When you don't know what you're doing, AI is only a delayed catastrophe and the rise of the “Vibe coding cleanup” consultant is already here.

We danced around a lot on the podcast and I hope the information above adds to the story! This feels like wrapping up a twenty year journey and opening up a new chapter. It's been a wild ride so far and I look forward to meeting you on the never ending journey of learning and making idiots out of ourselves.

---

More to explore:

* [Curvium Group](https://curvium.com/)
* [Max Headroom](https://en.wikipedia.org/wiki/Max_Headroom)
* [Four Yorkshiremen](https://en.wikipedia.org/wiki/Four_Yorkshiremen) (you can also [enjoy them on YouTube](https://www.youtube.com/watch?v=ue7wM0QC5LE))

{{<jump>}}[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_201-Working_for_a_Vendor_with_David_Gee.mp3){{</jump>}}