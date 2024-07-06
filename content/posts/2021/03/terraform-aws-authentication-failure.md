---
title: "Intermittent Terraform Authentication Failure Using AWS Provider in a Vagrant VM"
date: 2021-03-31 07:47:00
tags: [ cloud, automation, AWS ]
---
**TL&DR**: Client clock skew could result in AWS authentication failure when running **terraform apply**

When I wanted to [compare AWS and Azure orchestration speeds](/2021/03/public-cloud-orchestration-speed.html) I encountered a crazy Terraform error message when running **terraform apply**:

```
module.network.aws_vpc.My_VPC: Creating...

Error: Error creating VPC: AuthFailure: 
AWS was not able to validate the provided access credentials
	status code: 401, request id: ...
```

Obviously I did all the usual stuff before googling for a solution:
<!--more-->
* Changing my access keys (just in case, who knows)
* Checking whether the access keys work with AWS CLI (they did)
* Running **terraform plan** first (it worked)

And then something weird happened: when searching for the exact error message, I felt like I dropped straight into the [Wisdom of the Ancients](https://xkcd.com/979/).

I found a half-dozen Terraform support cases almost identical to my problem where the reporters did everything they could do to fix the problem (including switching the access keys), and collected all the necessary information, only to have their report closed with *It's not a good idea to publish your AWS access keys* (like that would be relevant) or *Looks like you can't use AWS IAM* or *Not a Terraform problem* or *Can't reproduce*.

{{<note>}}Now you know why it's sometimes more efficient to [publish a rant](/2020/12/ansible-config-sections.html) pointing out ([sometimes very well-known](/2017/04/lets-drop-some-random-commands-shall-we.html)) undesired behavior.{{</note>}}

Finally I [found one](https://github.com/hashicorp/terraform/issues/6566) where someone took the time to realize that HTTP error code 401 does *not* mean *Forbidden* but *Unauthorized*, and provided a [link to an AWS discussion](https://forums.aws.amazon.com/thread.jspa?threadID=175266) with an interesting conclusion: the real-time clock on your client might be out-of-sync.

Indeed I ran Terraform on a Vagrant/VirtualBox VM ([deployment recipe](https://github.com/ipspace/pubcloud/tree/master/install) in case you need it) that has been up for days, and it seems like its real-time clock drifted just enough for AWS authentication to fail. Restarting the VM (thus syncing its clock to the laptop clock) fixed the problem.
