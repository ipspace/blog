Why industry/ietf never invested into OAM for OSPF/ Link State protocols (though pardon my ignorance if they did). But idea here is that there should be intelligence built into the system and inform operator about:
 
Database size has reached on higher side from HW resources and SW accuracy standpoint
Too many frequent SPF runs … so network is unstable for whatever reasons
Alert….Hey Admin, are you sure you want to redistribute BGP routes into OSPF, another one – Hey Admin, why on earth you would want to redistribute iBGP routes into OSPF
A particular x device is causing convergence delays because it doesn’t have enough resources to process updates fast enough (essentially the weakest link theory)
SPF is taking often too long now for potentially x,y,z reasons
X node/link in network has no backup path available to trigger FRR due so it’s not protected
Hey Admin, since the path driven from SPT is now congested for A to B conversation, Do you want to turn on backup path and use UCMP (assuming we now support UCMP)