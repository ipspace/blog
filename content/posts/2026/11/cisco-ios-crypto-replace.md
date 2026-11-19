---
title: "Cisco IOS XE 'configure replace' Breaks on 'crypto pki' Commands"
date: 2026-11-19 08:08:00+0100
tags: [ netsim ]
netsim_tag: quirks
---
In February 2007, I published a (long gone) article describing the drawbacks of the Cisco IOS **configure replace** command. It was pretty bad at the time, but has improved significantly since. Alas, after 20 years, it still can't cope with simple stuff that routers generate on their own.

I was reimplementing the _netlab_ "[reload configuration](https://netlab.tools/netlab/up/#reloading-saved-configurations)" functionality with Netmiko, and things seemed to work until I got random errors in the integration tests. Those tests are really trivial:
<!--more-->
1. Start the lab, configure OSPF on the tested device.
2. Collect and save the device configuration
3. Stop the lab
4. Start the lab with `--reload` parameter to reload the saved configuration
5. Check OSPF adjacency between the tested device and a probe to validate the configuration was properly reloaded.

For a non-trivial number of test runs, the **configure replace** command failed on *some* IOS XE devices (Catalyst 8000v and CSR, but not IOL or IOLL2). After chasing the gremlins for a while, this is what I found:

* It was a timing issue. _netlab_ got too fast now that it no longer uses Ansible to configure Cisco IOS devices.
* The running configuration _netlab_ collected from Cisco IOS XE sometimes did not include the licensing server PKI trustpoint (**crypto pki** commands like the ones below).

```
crypto pki trustpoint SLA-TrustPoint
 enrollment pkcs12
 revocation-check crl
 hash sha512
```

* In 75% of the potential scenarios, that doesn't matter, but when I tried to replace a configuration with **crypto pki trustpoint** with the saved configuration that did not have it, **configure replace** command failed miserably[^AYBBU]:

[^AYBBU]: Ignoring the *all your base are belong to us*-type blooper: "*The following commands are failed to apply to the IOS image*"

```
dut#configure replace nvram:replace-config force
The rollback configlet from the last pass is listed below:
********
!List of Rollback Commands:
crypto pki certificate chain SLA-TrustPoint
 certificate ca 01
  no 	quit
  no D697DF7F 28
  no 418616A9 4093E049 4D10AB75 27E86F73 932E35B5 8862FDAE 0275156F 719BB2F0
  no 80DDCD16 D6BACECA EEBC7CF9 8428787B 35202CDC 60E4616A B623CDBD 230E3AFB
  no 5FB0DA06 B92AFE7F 494E8A9E 07B85737 F3A58BE1 1A48A229 C37C1E69 39F08678
  no 7CA7B7E6 C1AF74F6 152E99B7 B1FCF9BB E973DE7F 5BDDEB86 C71E3B49 1765308B
  no 467A3DF4 4D565700 6ADF0F0D CF835015 3C04FF7C 21E878AC 11BA9CD2 55A9232C
  no D98987BF E40CBD9E 1AECA0C2 2189BB5C 8FA85686 CD98B646 5575B146 8DFC66A8
  no 604EDCDE FF4FED2B 77FC460E CD636FDB DD44681E 3A5673AB 9093D3B1 6C9E3D8B
  no 03820101 00507F24 D3932A66 86025D9F E838AE5C 6D4DF6B0 49631C78 240DA905
  no 4B3D31E5 1B3E6A17 606AF333 3D3B4C73 E8300D06 092A8648 86F70D01 010B0500
  no 06300F06 03551D13 0101FF04 05300301 01FF301D 0603551D 0E041604 1449DC85
  no DFC7C6CF 04DD7FD1 02030100 01A34230 40300E06 03551D0F 0101FF04 04030201
  no C55F0D76 61F9A4CD 3D992327 A8BB03BD 4E6D7069 7CBADF8B DF5F4368 95135E44
  no C7479096 B4CB2D62 EA2F505D C7B062A4 6811D95B E8250FC4 5D5D5FB8 8F27D191
  no 68E69491 20F320E7 948E71D7 AE3BCC84 F10684C7 4BC8E00F 539BA42B 42C68BB7
  no 7390A3EB 2B5436AD C847A2C5 DAB553EB 69A9A535 58E9F3E3 C0BD23CF 58BD7188
  no 4AA4E80D DB6FD1C9 60B1FD18 FFC69C96 6FA68957 A2617DE7 104FDC5F EA2956AC
  no 1C394D78 462EF239 C659F715 B98C0A59 5BBB5CBD 0CFEBEA3 700A8BF7 D8F256EE
  no CBB4C798 212AA147 C655D8D7 9471380D 8711441E 1AAF071A 9CAE6388 8A38E520
  no 82010A02 82010100 A6BCBD96 131E05F7 145EA72C 2CD686E6 17222EA1 F1EFF64D
  no 526F6F74 20434130 82012230 0D06092A 864886F7 0D010101 05000382 010F0030
  no 43697363 6F312030 1E060355 04031317 43697363 6F204C69 63656E73 696E6720
  no 3834375A 170D3338 30353330 31393438 34375A30 32310E30 0C060355 040A1305
  no 6F204C69 63656E73 696E6720 526F6F74 20434130 1E170D31 33303533 30313934
  no 32310E30 0C060355 040A1305 43697363 6F312030 1E060355 04031317 43697363
  no 30820321 30820209 A0030201 02020101 300D0609 2A864886 F70D0101 0B050030
 no certificate ca 01
no crypto pki certificate chain SLA-TrustPoint
crypto pki trustpoint SLA-TrustPoint
 no hash sha512
 no revocation-check crl
 no enrollment pkcs12
no crypto pki trustpoint SLA-TrustPoint
end
********


Rollback aborted after 5 passes
The following commands are failed to apply to the IOS image.
********
certificate ca 01
no 	quit
no D697DF7F 28
no 418616A9 4093E049 4D10AB75 27E86F73 932E35B5 8862FDAE 0275156F 719BB2F0
no 80DDCD16 D6BACECA EEBC7CF9 8428787B 35202CDC 60E4616A B623CDBD 230E3AFB
no 5FB0DA06 B92AFE7F 494E8A9E 07B85737 F3A58BE1 1A48A229 C37C1E69 39F08678
no 7CA7B7E6 C1AF74F6 152E99B7 B1FCF9BB E973DE7F 5BDDEB86 C71E3B49 1765308B
no 467A3DF4 4D565700 6ADF0F0D CF835015 3C04FF7C 21E878AC 11BA9CD2 55A9232C
no D98987BF E40CBD9E 1AECA0C2 2189BB5C 8FA85686 CD98B646 5575B146 8DFC66A8
no 604EDCDE FF4FED2B 77FC460E CD636FDB DD44681E 3A5673AB 9093D3B1 6C9E3D8B
no 03820101 00507F24 D3932A66 86025D9F E838AE5C 6D4DF6B0 49631C78 240DA905
no 4B3D31E5 1B3E6A17 606AF333 3D3B4C73 E8300D06 092A8648 86F70D01 010B0500
no 06300F06 03551D13 0101FF04 05300301 01FF301D 0603551D 0E041604 1449DC85
no DFC7C6CF 04DD7FD1 02030100 01A34230 40300E06 03551D0F 0101FF04 04030201
no C55F0D76 61F9A4CD 3D992327 A8BB03BD 4E6D7069 7CBADF8B DF5F4368 95135E44
no C7479096 B4CB2D62 EA2F505D C7B062A4 6811D95B E8250FC4 5D5D5FB8 8F27D191
no 68E69491 20F320E7 948E71D7 AE3BCC84 F10684C7 4BC8E00F 539BA42B 42C68BB7
no 7390A3EB 2B5436AD C847A2C5 DAB553EB 69A9A535 58E9F3E3 C0BD23CF 58BD7188
no 4AA4E80D DB6FD1C9 60B1FD18 FFC69C96 6FA68957 A2617DE7 104FDC5F EA2956AC
no 1C394D78 462EF239 C659F715 B98C0A59 5BBB5CBD 0CFEBEA3 700A8BF7 D8F256EE
no CBB4C798 212AA147 C655D8D7 9471380D 8711441E 1AAF071A 9CAE6388 8A38E520
no 82010A02 82010100 A6BCBD96 131E05F7 145EA72C 2CD686E6 17222EA1 F1EFF64D
no 526F6F74 20434130 82012230 0D06092A 864886F7 0D010101 05000382 010F0030
no 43697363 6F312030 1E060355 04031317 43697363 6F204C69 63656E73 696E6720
no 3834375A 170D3338 30353330 31393438 34375A30 32310E30 0C060355 040A1305
no 6F204C69 63656E73 696E6720 526F6F74 20434130 1E170D31 33303533 30313934
no 32310E30 0C060355 040A1305 43697363 6F312030 1E060355 04031317 43697363
no 30820321 30820209 A0030201 02020101 300D0609 2A864886 F70D0101 0B050030
no certificate ca 01
no hash sha512
no revocation-check crl
no enrollment pkcs12
********
```

It's obvious that the **configure replace** command has no idea what to do with the **crypto pki** commands. I completely understand why this never showed up in Cisco's internal tests (you wait a bit longer and there's no issue), but you could have your own PKI trustpoints, and it's ridiculous that we still don't have a *reliable* "replace configuration" functionality in Cisco IOS XE.
