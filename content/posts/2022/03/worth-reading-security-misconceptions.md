---
title: "Worth Reading: Misconceptions about Route Origin Validation"
date: 2022-03-06 08:44:00
tags: [ worth reading, security ]
---
Use the [email sent by Randy Bush to RIPE routing WG mailing list](https://www.ripe.net/ripe/mail/archives/routing-wg/2022-February/004542.html) every time a security researcher claims a technology with no built-in security mechanism is insecure (slightly reworded to make it more generic).

---

Lately, I am getting flak about $SomeTechnology not providing protection from this or that malicious attack. Indeed it does not.
<!--more-->
In the $SomeTechnology design, we DELIBERATELY did NOT try to cover malicious attacks. We also did not try to solve world hunger.

Repeat 20 times: "$SomeTechnology is not a security mechanism.  It is only meant to reach $SomeOtherGoal."

Yes, a screwdriver sucks as a hammer.

We do seem to see that $SomeOtherGoal is being reached, and presume this is due to $SomeTechnology. This is good.

And once more for good luck: "$SomeTechnology is not a security mechanism. It is only meant to reach $SomeOtherGoal."

---

Bonus points if the [description of $SomeTechnology clearly describes its security shortcomings](/2018/11/omg-vxlan-is-still-insecure/) that are then "discovered" by a publicity-hungry security researcher.
