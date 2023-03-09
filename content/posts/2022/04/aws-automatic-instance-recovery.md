---
date: 2022-04-13 06:42:00+00:00
ha-cloud_tag: design
high-availability_tag: cloud
series:
- ha-cloud
tags:
- AWS
- virtualization
- high availability
title: AWS Automatic EC2 Instance Recovery
---
On March 30th 2022, AWS [announced](https://aws.amazon.com/about-aws/whats-new/2022/03/amazon-ec2-default-automatic-recovery/) automatic recovery of EC2 instances. Does that mean that AWS got feature-parity with VMware High Availability, or that VMware got it right from the very start? No and No.

### Automatic Instance Recover Is Not High Availability

Reading the [AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html) (as opposed to the feature announcement) quickly reveals a caveat or two. The automatic recovery is performed _if an instance becomes impaired because of an underlying hardware failure or a problem that requires AWS involvement to repair_.
<!--more-->
In simpler terms:

* If AWS experiences a (hypervisor) server failure or NIC failure, they'll recover your instance.
* If your instance crashes, or if an application server process hangs in your instance, they'll do nothing. It's still your responsibility.

VMware HA does all that, but it also includes [VM and Application Monitoring](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.avail.doc/GUID-62B80D7A-C764-40CB-AE59-752DA6AD78E7.html) that uses VMware Tools to detect  VM operating system failures. You can even use VMware SDK to generate application-specific heartbeats and have VMware HA restart the virtual machine if the application stops responding.

AWS EC2 does something similar to what VMware Tools are doing with [instance status checks](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html), but you have to [define an Amazon CloudWatch alarm action](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/UsingAlarmActions.html#AddingRecoverActions) to [reboot your instance](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/UsingAlarmActions.html)[^DOC].

[^DOC]: Did you notice I had to use three links in a single sentence to describe what's going on? I love AWS documentation, but sometimes the granularity/nesting level goes through the roof.

### VMware HA Clusters Still Don't Scale

How could AWS implement something similar to VMware HA clusters (which are limited to 64-96 hosts per cluster) in a region with (supposedly) millions of servers. Hint: they used a scalable architecture ;)

For decades, VMware treated vCenter as a GUI add-on that you could turn off when you go home. The high availability clusters and DRS were thus implemented as a standalone peer-to-peer mechanism independent of vCenter. The end result: a nasty conglomerate of byzantine failure scenarios (tons of blog posts and whole books were written about them) and "interesting" synchronization challenges when VMware started adding layers of network abstractions with VMware NSX[^LDP] on top of that pile of complexity.

AWS won't tell you how they implemented automatic recovery, but as they already had [server monitoring and instance status checks for a decade](https://aws.amazon.com/blogs/aws/ec2-instance-status-metrics/), all they had to do was to add a behind-the-scenes CloudWatch action to restart an instance when `StatusCheckFailed_System` changes to one. Instance recovery is thus not a byzantine system with its own mindset and opinions but a simple add-on to the existing thoroughly tested orchestration system. One does have to wonder why it took a decade to implement though ;)

[^LDP]: LDP-IGP synchronization issues are a kindergarten-level topic compared to HA/DRS-NSX ones. For example, in early versions of VMware NSX you could lose connectivity to your VMs if DRS moved them while the vCenter SOAP service was broken.
