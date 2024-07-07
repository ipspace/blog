---
date: 2009-10-05 07:11:00.002000+02:00
tags:
- security
- SSH
title: SSH RSA authentication works in IOS release 15.0M
url: /2009/10/ssh-rsa-authentication-works-in-ios/
---
The feature we've begged, prayed, sobbed, yelled, screamed for has finally been implemented in Cisco IOS: public key SSH authentication works in IOS release 15.0M (and is surprisingly easy to use).

After [configuring SSH server on IOS](/2008/08/ssh-works-without-aaa/) (see also [comments to this post](/2008/08/identifying-tacacs-failure/)), you have to configure the **ssh pubkey-chain**, where you can enter the key string (from your SSH public key file) or the key's hash (which is displayed by the **ssh-keygen** command).
<!--more-->
It's probably easier to copy/paste the public key from your *id_rsa.pub* file into the terminal window ...

``` {.code}
R2#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#ip ssh pubkey-chain
R2(conf-ssh-pubkey)#username pipi
R2(conf-ssh-pubkey-user)#key-string
R2(conf-ssh-pubkey-data)#$AAQEA6jYlf9MBskhkWov+ZOUDKun0ExQIRj1zfWA/YciO02VS  
R2(conf-ssh-pubkey-data)#$XsxM7SqNkRSQOR7y7HBMoxTHV7o+R/uS6A8/mF0A3P/ScRjct  
R2(conf-ssh-pubkey-data)#$JrNGACGaFy1njD9PrrvrU4o4hx6XDr6xVXF4sP4OCSXIn+Cp8  
R2(conf-ssh-pubkey-data)#$bCnZLmv908AeDb1Ac4nPdsn1OhCPIg6fxZjB7DvAMB8Dbr+7Y  
R2(conf-ssh-pubkey-data)#$apEbGE94luIqnBc61HsMd6JCWbQ== user@host.example.com
R2(conf-ssh-pubkey-data)#exit
R2(conf-ssh-pubkey-user)#^Z
```

... and let the router convert it into the key hash, which is stored in the configuration:

``` {.code}
R2#show run | section ssh
ip ssh rsa keypair-name SSH
ip ssh version 2
ip ssh pubkey-chain
 username pipi
  key-hash ssh-rsa C20B739F2645D6850C591C6A11780CB5 user@host.example.com
```

After this simple step, you can log into your router without typing the password. Finally we have a manageable way of secure remote command execution.
