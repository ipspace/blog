---
ai_tag: kick
date: 2023-04-06 07:39:00+00:00
tags:
- AI
title: Kicking the Tires of GitHub Copilot
---
A friend sent me a video demo of his *AI-driven network device configuration* proof-of-concept. Before commenting on that idea, I wanted to see how well AI works as an assistant. Once [Kristian Larsson mentioned](https://twitter.com/plajjan/status/1640088978228408326) he was using [GitHub Copilot](https://github.com/features/copilot), it was obvious what to do next: try it out while working on the next *[netlab](https://netsim-tools.readthedocs.io/en/latest/)* release.

**TL&DR:**

-   It works.
-   Some Copilot suggestions are uncannily accurate; others are fishing expeditions.
-   It's bland.
<!--more-->
### Setting It Up

Getting GitHub Copilot to work was a breeze:

-   Sublime Text has an unofficial Copilot plugin with too many dependencies, so I installed Visual Studio Code (VSC).
-   I installed Python, Copilot, and SFTP (don't ask) plugins for VSC and registered for a trial Copilot account on GitHub.

The next moment I started getting suggestions, from single lines of code (or comments) to whole code blocks.

**The scary side effect:** I'm back to a Microsoft-dominated development ecosystem now that Microsoft has invested in OpenAI.

### First Impressions

-   Some of the code suggestions are **uncannily good**. I was writing a function and realized I needed to handle some edge cases first. Copilot figured out precisely what edge cases to test for and how to react. 
-   I could write a lengthy comment describing what I want a function to do, and Copilot would **offer the whole code block** doing something along those lines. Sometimes it was accurate, and sometimes it was way off.
-   The suggestions were good as long as I stayed within the context of the current text file. When I used functions from other modules (even if I had used them in different places before), the suggestions turned into a **fishing expedition** along the lines of *this is how I would expect you to name those functions.*
-   The code suggestions were **safely boring**. For example, it suggested using a long block of `if/elif/else` conditions to execute a function selected by a string value instead of using a more concise lookup table.
-   I try to write code comments explaining the reasons I'm doing things. Copilot offered comment suggestions, but while they were better than "*increase x by adding 1 to it"* for `x = x + 1`, they **mostly rephrased the current line of code**. That's good enough if your coding standard requires (useless) comments, but not if you want to help your future self or others looking at your code.
-   Suggested error messages were **equally bland**. While they matched the challenges the code encountered, they did not provide enough context or offer suggestions. We shouldn't judge Copilot too harshly on this one; useless error messages are par for the course.

To recap:

-   Using GitHub Copilot is like working with a decent programmer that hasn't seen much of your codebase and would like to offer suggestions based on limited information and some safe guesses.
-   Is it useful? Definitely, and even more so if you have to write a lot of boilerplate code[^BP].
-   Will I keep using it? Most probably.
-   Would I trust it to write working code? Absolutely not.

[^BP]: Whenever faced with the boredom of writing boilerplate code, I'd usually write a tool generating it, but that's a different story.

### The Inevitable Hype

AI cheerleaders often [turn around that last argument](https://about.sourcegraph.com/blog/cheating-is-all-you-need) claiming that _since Copilot writes code that's 80% correct, you'll code five times faster_. That's one of the biggest piles of [Déjà-Moo](https://idioms.thefreedictionary.com/d%C3%A9j%C3%A0+moo) I've seen in a long while.

It might be true if your main challenge is your typing speed (in which case I'd suggest you take a typing course), assuming you spend all your time typing code without thinking about it. From a senior networking engineer's perspective: how much time do you spend typing configuration commands into network devices compared to all other things you have to do?

I'm sure you get performance improvement using GitHub Copilot in real-world scenarios, but it often takes longer to fix code that is 80% correct than writing your own. As always, YMMV.

### Back to Networking

Want to know whether AI/ML makes sense in networking and how you could use these technologies? You'll love the [AI/ML in Networking: the Good, the Bad, and the Ugly](https://www.ipspace.net/AI_and_ML_in_Networking) webinar by Javier Antich (available with the [free ipSpace.net subscription](https://www.ipspace.net/Subscription/Free)). He also [wrote a book on the topic](https://blog.ipspace.net/2023/02/machine-learning-network-cloud.html) that's definitely worth buying.
