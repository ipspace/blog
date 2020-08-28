---
title: "Example: Securing AWS Deployment"
date: 2020-09-02 07:44:00
tags: [ cloud, AWS ]
---
[Nadeem Lughmani](https://www.linkedin.com/in/nadeem-lughmani-38b4251/) created [an excellent solution](https://github.com/nadeemnet/NetworkingInPubClouds/tree/master/security) for the [_securing your cloud deployment_](https://my.ipspace.net/bin/list?id=PubCloud&module=6#HOMEWORK) hands-on exercise in our [public cloud online course](https://www.ipspace.net/PubCloud/). His Terraform-based solution includes:

* Security groups to restrict access to web server and SSH bastion host;
* An IAM policy and associated user that has read-only access to EC2 and VPC resources (used for monitoring)
* An IAM policy that has full access to as single S3 bucket (used to modify static content hosted on S3)
* An IAM role for AWS CloudWatch logs
* Logging SSH events from the SSH bastion host into CloudWatch logs.

{{<jump>}}[Explore the solution](https://github.com/nadeemnet/NetworkingInPubClouds/tree/master/security){{</jump>}}