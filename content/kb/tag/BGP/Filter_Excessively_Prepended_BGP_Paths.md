---
kb_section: BGP
minimal_sidebar: true
pre_scroll: true
title: Filter Excessively Prepended BGP Paths
url: /kb/tag/BGP/Filter_Excessively_Prepended_BGP_Paths.html
---
**Short description**: BGP AS-path prepending is commonly used to influence BGP path selection in upstream autonomous systems, forcing the upstream networks to use one of the advertised paths as a primary path and another one as a backup path based on the AS path length.

Excessive AS-path prepending (more than five or six copies of the same AS in the AS-path) very rarely solves the path selection issues, pollutes the BGP routing tables and adversely impacts routers throughout the Internet. As an ISP cannot rely on its customers’ ability to advertise acceptable BGP prefixes, AS path access lists should be used to filter inbound BGP updates and drop excessively prepended prefixes.

**Solution**: Use the following statement in an AS-path access list to block all AS-paths where the same AS number appears more than five times consecutively (change the number of *\1* expressions to tailor the filter to your needs).

```
ip as-path access-list 100 deny *([0-9]+)*\1_\1_\1_\1_<
```

**Short explanation**: **\\1** Cisco IOS regular expression pattern allows you to match a previously matched string. This pattern can be used to match prepended AS-paths.

## Detailed Description

The following features of Cisco IOS regular expressions were used in this solution:

-   The **\[0-9\]** pattern matches any digit.
-   The **\[0-9\]+** pattern matches a sequence of digits.
-   The **\_\[0-9\]+\_** pattern matches a complete number (the \_ characters match separators, including beginning or end of string).
-   The **\_(\[0-9\]+)\_** pattern matches a complete number and saves it for further reference.
-   The **\\1** pattern matches a previously saved match.

The regular expression **\_(\[0-9\]+)\_\\1\_\\1\_\\1\_\\1\_ **therefore matches any AS path where a single AS number appears five or more times in a sequence.

## Test Bed

A simple test network was set up using a single Cisco IOS router (10.17.0.1) and a Linux host (10.17.0.2) running a BGP daemon (see the *Initial configurations* section for details). The Linux BGP daemon advertised numerous BGP routes with various lengths of prepended AS paths to the Cisco IOS router (note that prepending happens at various points in the AS path, not just at the beginning of it).

```
Rtr#show ip bgp | begin Network
   Network      Next Hop    Metric Loc Weight Path
*> 10.2.1.0/24  10.17.0.2        0          0 65000 1 2 3 4 i
*> 10.2.2.0/24  10.17.0.2        0          0 65000 1 2 2 3 4 i
*> 10.2.3.0/24  10.17.0.2        0          0 65000 1 2 3 3 3 4 i
*> 10.2.4.0/24  10.17.0.2        0          0 65000 1 2 3 4 4 4 4 i
*> 10.2.5.0/24  10.17.0.2        0          0 65000 1 2 2 2 2 2 3 4 i
*> 10.2.6.0/24  10.17.0.2        0          0 65000 1 1 1 1 1 1 2 3 4 i
```

## Test Results

You can use the **show ip bgp regexp** command to test a regular expression on the actual data stored in the BGP table. When used on the test router, the regular expression matched all IP prefixes where a single AS number was prepended four or more times, verifying the correctness of the regular expression.

The **show ip bgp quote-regexp** command was used to combine the regexp match with additional **show** filters.

```
R2#show ip bgp quote-regexp "_([0-9]+)_\1_\1_\1_\1_" | begin Network
   Network      Next Hop    Metric Loc Weight Path
*> 10.2.5.0/24  10.17.0.2        0          0 65000 1 2 2 2 2 2 3 4 i
*> 10.2.6.0/24  10.17.0.2        0          0 65000 1 1 1 1 1 1 2 3 4 i
```

The following changes were made to the router configuration to filter excessively prepended BGP prefixes:

```
router bgp 65100
 neighbor 10.17.0.2 filter-list 100 in
!
ip as-path access-list 100 deny _([0-9]+)_\1_\1_\1_\1_
ip as-path access-list 100 permit .*
```

After a soft reset of the BGP session, the printout of the resulting BGP table verified that the router has filtered all inbound BGP updates with excessively prepended AS paths.

{{<cc>}}Final BGP table on the router{{</cc>}}
```
R2#show ip bgp ¦ begin Network
   Network      Next Hop    Metric Loc Weight Path
*> 10.2.1.0/24  10.17.0.2        0          0 65000 1 2 3 4 i
*> 10.2.2.0/24  10.17.0.2        0          0 65000 1 2 2 3 4 i
*> 10.2.3.0/24  10.17.0.2        0          0 65000 1 2 3 3 3 4 i
*> 10.2.4.0/24  10.17.0.2        0          0 65000 1 2 3 4 4 4 4 i 
```

## Device Configurations

{{<cc>}}Initial router configuration{{</cc>}}
```
hostname Rtr
!
ip cef
!
interface Loopback0
 ip address 10.0.1.2 255.255.255.255
!
interface FastEthernet0/0
 ip address 10.17.0.1 255.255.255.0
!
router bgp 65100
 no synchronization
 bgp log-neighbor-changes
 neighbor 10.17.0.2 remote-as 65000
 no auto-summary
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 transport preferred none
 stopbits 1
!
ntp logging
end 
```

{{<cc>}}BGP daemon configuration{{</cc>}}
```
hostname BGP_prepend
!
router bgp 65000
 bgp router-id 10.17.0.2
 network 10.2.1.0/24 route-map P1
 network 10.2.2.0/24 route-map P2
 network 10.2.3.0/24 route-map P3
 network 10.2.4.0/24 route-map P4
 network 10.2.5.0/24 route-map P5
 network 10.2.6.0/24 route-map P6
 neighbor 10.17.0.1 remote-as 65100
!
route-map P1 permit 10
 set as-path prepend 1 2 3 4
!
route-map P2 permit 10
 set as-path prepend 1 2 2 3 4
!
route-map P3 permit 10
 set as-path prepend 1 2 3 3 3 4
!
route-map P4 permit 10
 set as-path prepend 1 2 3 4 4 4 4
!
route-map P5 permit 10
 set as-path prepend 1 2 2 2 2 2 3 4
!
route-map P6 permit 10
 set as-path prepend 1 1 1 1 1 1 2 3 4
!
line vty
 no login 
```

{{<cc>}}Final router configuration{{</cc>}}
```
hostname R2
!
ip cef
!
interface Loopback0
 ip address 10.0.1.2 255.255.255.255
!
interface FastEthernet0/1
 ip address 10.17.0.1 255.255.255.0
 speed auto
 duplex auto
!
router bgp 65100
 no synchronization
 bgp log-neighbor-changes
 neighbor 10.17.0.2 remote-as 65000
 neighbor 10.17.0.2 filter-list 100 in
 no auto-summary
!
ip classless
!
ip as-path access-list 100 deny _([0-9]+)_\1_\1_\1_\1_
ip as-path access-list 100 permit .*
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 transport preferred none
 stopbits 1
!
ntp logging
end
```

<!-- end -->