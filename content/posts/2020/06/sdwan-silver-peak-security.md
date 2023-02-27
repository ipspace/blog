---
title: "SD-WAN Security: A Product Liability Insurance Law Would Certainly Help"
date: 2020-06-02 07:06:00
tags: [ SD-WAN, security ]
sd-wan_tag: security
---
On May 14th 2020, [Marcel Gamma](https://www.linkedin.com/in/marcel-gamma-61536127/), tech industry journalist, and editor-in-chief at inside-it.ch and inside-channels.ch, published an [article discussing several glaring security vulnerabilities in Silver Peak's SD-WAN products](https://www.inside-it.ch/de/post/eine-produkthaftpflicht-wuerde-sicher-helfen-20200514) on inside-it.ch. The original article was written in German; Marcel was kind enough to translate it into English and get permission from his publisher to have the English version published on ipSpace.net.
- - -
**Security researchers make serious accusations against SD-Wan manufacturer Silver Peak. The latter disagrees. Swiss experts are analyzing the case.**

By Marcel Gamma, 

Silver Peak is accused of laxity in dealing with security issues and in dealing with security researchers who act within the framework of _Responsible Disclosure_.
<!--more-->
The starting point of the research are three vulnerabilities the 9-member group of SD-Wan security researchers at Tomsk University published under the name "[SD-WAN New Hope](https://github.com/sdnewhop/sdwannewhope)" on Github in April 2020. The vulnerabilities concern Silver Peak, a Gartner-celebrated manufacturer of SD-WAN products, whose products are used by at least two Swiss telcos.

Vulnerability number one according to _SD-WAN New Hope_: [The IPsec UDP protocol implementation in the Silver Peak EdgeConnect product does not offer the claimed "Perfect Forward Secrecy" (PFS)](https://github.com/sdnewhop/sdwannewhope/blob/master/reports/SDWAN-New-Hop-2020-17-01.pdf). [Perfect Forward Secrecy](https://en.wikipedia.org/wiki/Forward_secrecy) means that the session keys used in an IPsec session cannot be reconstructed from the secret long-term keys after the session has ended.

A second vulnerability, which the researchers believe is just as significant, is that [there is no authentication between Orchestrator and EdgeConnect devices](https://github.com/sdnewhop/sdwannewhope/blob/master/reports/SDWAN-New-Hop-2020-30-01.pdf). "It is possible to establish a connection between EdgeConnect and Orchestrator devices belonging to different SD-WAN networks," the researchers say ([PDF](https://github.com/sdnewhop/sdwannewhope/blob/master/reports/SDWAN-New-Hop-2020-30-01.pdf)).

Thirdly, the researchers found that [there is no authentication between the Silver Peak Cloud portal on the Internet and customers' EdgeConnect devices](https://github.com/sdnewhop/sdwannewhope/blob/master/reports/SDWAN-New-Hop-2020-31-01.pdf). "EdgeConnect does not authenticate the portal. The portal can execute any command on EdgeConnect using the REST API," says the publication summary on Github ([PDF](https://github.com/sdnewhop/sdwannewhope/blob/master/reports/SDWAN-New-Hop-2020-31-01.pdf)).

According to the researchers, the vulnerabilities are severe: "In our view, these vulnerabilities completely compromise the current EdgeConnect software. The vulnerabilities show that the cryptographic layer of the product is broken; the quality of the security mechanisms is very low," says [Denis Kolegov](https://www.linkedin.com/in/dnkolegov/), Ph.D., for 14 years associate professor of computer security at Tomsk University.

## All you need is a hacker with script kiddy skills

And how hard was it to find the vulnerabilities? Denis Kolegov explains: "To be honest, some of the vulnerabilities we found are 'low hanging fruits' and it is very easy to find and exploit them. You don't need to hire people with skills like Google's Project Zero team. All you need is a hacker with script kiddy skills. Other vulnerabilities require cryptographic expertise. We spent about two weeks trying to find the vulnerability in the proprietary IPsec because we had to reverse-engineer some parts of the code and reconstruct the logic, but then found two more vulnerabilities within 2 or 3 hours".

Kolegov adds, "In my opinion, these vulnerabilities could completely compromise the security of any Silver Peak customer. Furthermore, the third vulnerability has shown that an attacker can compromise the Silver Peak network and its Silver Peak portal and then attack customers or provide a fake portal on the Internet (as we did), change the EdgeConnect configuration, and then route all customer network traffic through the attacker's network". This means "that Silver Peak does not understand or does want to understand how to develop secure software in 2020," writes the security researcher.

## There shouldn't be any vulnerabilities of this severity

[Martin Leuthold](https://www.linkedin.com/in/martinleuthold/), head of the "Security & Network" business unit at [Switch](https://www.switch.ch/about/foundation/), does not know the case in detail, but expresses his personal view: "If a manufacturer in software development really does work systematically 'secure' in the sense of DevSecOps, then there should not be any such serious vulnerabilities."

These gaps, which the researchers classified as critical, were published 90 days after being reported to the manufacturer according to the rules of _Responsible Disclosure_ because Silver Peak first reacted to their report with incomprehension and then assured them that there was a fix, according to Tomsk.

And Kolegov criticizes the company's communication with researchers in general: "In 2018 we found many vulnerabilities in the web interface of EdgeConnect and reported them to Silver Peak. We received no responses to our report."

With the new vulnerabilities, the researchers were no longer willing to accept this, and Kolegov also [tweeted to the manufacturer on January 17th](https://twitter.com/dnkolegov/status/1218203041234669568) that they had reported new vulnerabilities. He publicly stated that "Silver Peak has also completely ignored previous reports."

Only after several days did Silver Peak react. According to Kolegov, those responsible either did not understand the dimensions or did not take them seriously.

This would indicate a general communication problem Silver Peak has with security researchers. "This is not true," Kristian Thyregod, VP & GM, EMEA of the manufacturer, defends himself on request of inside-it.ch. "Silver Peak appreciates the ongoing efforts of the SD-WAN New Hop team to alert us to potential security vulnerabilities, and we have an established process for reviewing, fixing, and communicating such discoveries."

## Questionable vulnerabilities resolved

In the context of _Responsible Disclosure_, security researchers disclose a weakness or problem after a certain period of time, giving the manufacturer sufficient time to fix the problem or provide a patch. For example, Google Project Zero respects a 90-day disclosure period, which begins after the vendor is notified of the vulnerability. "Specifically for this investigation, Silver Peak has fixed the vulnerabilities in question in its latest software version," Silver Peak said on request without explaining when this was done.

The process for security vulnerabilities includes a vendor requesting a CVE number to publicly warn customers and potential customers that a problem has been identified.

When did Silver Peak respond by requesting CVE numbers? Apparently, not until three months after the warning from Tomsk, as evidenced by an email we received. Now, as of April 23rd, the vendor is a CVE Numbering Authority and can assign CVE numbers itself. "So there is no excuse for not having published a number for the first Security Advisory," a Swiss security expert tells us. He doesn't want to be named but has taken a detailed look at the three current Silver Peak vulnerabilities.

## When were customers informed?

Has the company informed all its customers about these deficiencies? Including all affected Swiss clients? At what exact time? Silver Peak replies that it "communicated directly with EdgeConnect customers, including service provider partners serving customers over managed SD-WAN services."

Silver Peak didn't say when the communication was made. In Switzerland, according to inside-it.ch, several customers were informed not by the company itself, but in mid-April by other means under "TLP AMBER" in a closed user group after a tip from an independent security expert, not the manufacturer.

Usually, manufacturers also create transparency by publishing all security advisories on their corporate website, where potential customers or journalists could see them. In the case of Silver Peak, inside-it.ch found a delta between the corporate website and cvedetails.com, with several known gaps not listed. 

The question to Kolegov: From an outsider's point of view, does Silver Peak give the impression of more security than is available? "From a security perspective, Silver Peak gives the impression of being an immature company that develops unsafe products," writes the security researcher from Tomsk University. "Silver Peak has published the latest security advisories in the support section of our website," manufacturer spokesman Thyregod answers our question concisely and without saying when that happened.

In fact, on May 4th, the day of our inquiry and several days after the Tomsk "SD-WAN New Hope" Silver Peak published the three advisories including CVE numbers. According to the manufacturer the gaps are not to be classified as critical, but at most as "medium" (base score 6.0). NIST's base score on the "National Vulnerability Database" is still to be assessed.

How does Leuthold assess this procedure? "I expect a different reaction: quick feedback to the researchers, a clear process for the treatment of responsible disclosure, and at the same time constructive cooperation with the researchers to mitigate these weaknesses and gaps. Added to this is transparency towards customers," he states as his personal opinion.

Thyregod says, "Silver Peak is fully committed to providing the highest levels of software quality and security to its Unity EdgeConnect SD-WAN edge platform customers. As a CVE-Numbering Authority, Silver Peak adheres to consistent and disciplined procedures to fully investigate and remediate vulnerabilities in our software whenever they may occur."

Leuthold is critical: "Due to the facts mentioned, Silver Peak is for me a bad example of how security researchers deal with _Responsible Disclosure_. Ten years ago, such behavior was normal for many manufacturers. Today, fortunately, it no longer is. But unfortunately, there are still manufacturers who act this way or even threaten researchers with legal action."

He cannot evaluate Silver Peak's general approach to security, he says, because he does not have the necessary information about the company's internal information security management. Kolegov sums up dryly: "The vulnerabilities speak for themselves." And he believes: "What we've found is the tip of the iceberg."

Security experts agree that many manufacturers have made significant progress in recent years: Leuthold cites Microsoft as one example, and Kolegov says Citrix is open to the community.

## Is the FIPS cryptography certification worthless?

Leuthold adds that "the longer the more" one can expect ICT manufacturers to proactively establish a bug bounty program. The SD-Wan-New Hope researchers did not even aim for a bug bounty, since Silver Peak, to their knowledge, does not have one.

The three vulnerabilities also question the value of FIPS certifications, which are supposed to certify secure cryptography. The vulnerable Unity EdgeConnect SD-WAN Edge Platform had received FIPS 140-2 certification for the quality of its encryption in March, after the discoveries of the security researchers in Tomsk.

A proven Swiss security specialist, who wants to remain anonymous, confirms what other experts say: Silver Peak is only one of many examples, and what we'd need to make things better is product liability for manufacturers. Leuthold specifies: "This would certainly help. At least in cases of gross negligence or even intent. I would classify the case here as 'gross negligence'. However, it would not be easy to formulate a legal framework for this in a sensible way. In addition, this would have to be done jointly in at least one large economic area (e.g. the EU) in order to have a real impact. A solo effort by Switzerland is unthinkable and would lead to disadvantages for our country". Presumably, certain manufacturers would no longer supply "solutions" to Switzerland.

Furthermore, according to Leuthold, product liability could lead to an increase in product pricing, or stifle the innovation in Switzerland, resulting in disadvantages for local hardware and software manufacturers.

Marcel Gamma, tech industry journalist, editor-in-chief at inside-it.ch/inside-channels.ch, Public Speaker, Discussion Moderator

This article was [first published on May, 14th 2020 on inside-it.ch](https://www.inside-it.ch/de/post/eine-produkthaftpflicht-wuerde-sicher-helfen-20200514) and has been translated into English. Published with permission of Marcel Gamma/Huron AG, Switzerland
