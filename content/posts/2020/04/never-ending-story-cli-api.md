---
title: The Never-Ending Story of CLI or API
date: 2020-04-06 07:47:00
tags: [ automation,SDN ]
---
Over the last weekend I almost got pulled into yet-another [CLI-or-automation Twitter spat](https://twitter.com/danieldibswe/status/1246412818196414464). The really sad part: I thought we were past that point. After all, I've been ranting about that topic for almost seven years... and yet I'm still hearing the same arguments I did in those days.

Just for the giggles I collected a few old blog posts on the topic (not that anyone evangelizing their opinions on Twitter would ever take the time to read them ;).
<!--more-->
The basics:

* [CLI and API Myths](/2013/06/cli-and-api-myths/) (2013)
* [What Is This API Thingy?](/2014/07/what-is-this-api-thingy/) (2014)
* [To API or Not To API](/2016/10/to-api-or-not-to-api/) (2016)

CLI-or-API dilemma:

* [Is CLI In My Way … or Is It Just a Symptom of a Bigger Problem?](/2014/02/is-cli-in-my-way-or-is-it-just-symptom/) (2014)
* [CLI or API? Wait … Do You Really Have to Ask?](/2014/02/cli-or-api-wait-do-you-really-have-to/) (2014)
* [We Have to Get Away from the Box-Focused Mentality](/2015/03/we-have-to-get-away-from-box-focused/) (2015)
* [CLI or API… Again (and Again and Again…)](/2017/10/cli-or-api-again-and-again-and-again/) (2017)
* [It’s Bash Scripts All the Way Down (more on CLI versus API)](/2017/11/its-bash-scripts-all-way-down-more-on/) (2017)
* [Don't Get Obsessed with REST API](/2018/04/dont-get-obsessed-with-rest-api/) (2018)

Real-life considerations:

* [Stop the Low-Level Configuration Manipulation](/2019/05/stop-low-level-configuration/) (2019)
* [Is Controller-Based Networking More Reliable than Traditional Networking?](/2015/01/is-controller-based-networking-more/) (2015)
* [Big Red Button for Network Automation](/2018/02/big-red-button-for-network-automation/) (2018)

Meanwhile on planet Earth:

* [Anti-Automation from the Antimatter Universe](/2018/02/anti-automation-from-antimatter-universe/)
* [Fat Fingers Strike Again…](/2018/01/fat-fingers-strike-again/)

Finally:

* You MUST listen to [Terry Slattery remembering the history of Cisco IOS CLI](/2019/04/must-watch-history-of-cisco-ios-cli/)
* You might also love what [David Barroso had to say on the topic](https://twitter.com/dbarrosop/status/1246551526581157889).

### For those of you still loving Bash CLI

Fun fact: It took me less than 10 minutes to put together the above list using Bash on OSX (including figuring out the pipelines to get it done). Maybe there's some value to using CLI after all ;)

Here's what I did:

A) Get a list of blog posts mentioning CLI (a piece of cake after [migrating the blog into a Git-backed directory tree](/2020/03/ipspace-blog-runs-on-hugo/)):

```
cd $DIRECTORY/content/posts 
ack -l CLI
```

B) Limit the list to blog posts published between 2016 and 2019:

```
ack -l CLI|ack '201[6-9]'
```

C) Open all those blog posts in a web browser to see what I wrote in each one:

```
ack -l CLI|ack '201[5-9]'| \
  sort| \
  xargs -n 1 -I % open /%
```

Of course I also wanted to automate generation of Markdown text pointing to each blog post.

D) Write a Bash script to extract title from a blog post and return a bulleted line in Markdown:

```
URL=$1
TITLE=$(wget -qO- $URL|\
  hxnormalize -x|\
  hxselect -c head title|\
  sed -e 's/ &#171;.*//')
echo '*' "[$TITLE]($URL)"
```

Short explanation:

* **wget** fetches the web page contents
* **hxnormalize** (installed with **brew install html-xml-utils**) normalizes HTML, **-x** option returns the document in XML format
* **hxselect** reads an XML document and returns elements matching a CSS selector (**head title**), or their content when used with **-c** option.
* **sed** strips the fixed part at the end of page title.

E) Use the Bash script together with paste/copy OSX utilities to transform URL (on clipboard) into Markdown text (on clipboard)

```
pbpaste|xargs get-title.sh|pbcopy
```

Final workflow:

* Find an interesting article
* Copy article URL
* Switch to Bash window, up-arrow, enter
* Switch to IA Writer, paste
* Lather, rinse, repeat.
