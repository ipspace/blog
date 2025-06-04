---
title: "Interesting: Juniper MX and Jumbo Frames"
date: 2025-06-10 07:41:00+0200
tags: [ worth reading ]
---
Did you know that there's an Ethernet link between the Packet Forwarding Engine (PFE -- data plane) and Routing Engine (RE -- control plane) in every Juniper MX? That's why you have to run two VMs to emulate it (sometimes conveniently packed into one larger VM, proving RFC 1925 rule 6a).

That Ethernet link happens to have the MTU fixed at 1500 bytes. Guess what happens in the world where everyone uses jumbo frames? Did you say fragmentation? Bingo! And what do you think happens when one of those fragments gets dropped due to control-plane policing, and the rest of them are stuck in the reassembly queue? You'll find the gory details in a [lengthy blog post](https://www.oasis-tech.net/networks/how-troubleshooting-of-routing-flaps-ends-with-a-new-junos-command/) by Nitzan Tzelniker.
