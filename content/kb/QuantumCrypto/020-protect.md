---
kb_section: QuantumCrypto
minimal_sidebar: true
title: Protecting Against Future Quantum Computers
url: /kb/QuantumCrypto/020-protect/
---
There are four options you can use to protect your keys and encrypted data against successful attacks from both classical and quantum computers:

## Symmetric Key Exchange

You could avoid asymmetric key exchange algorithms by using fully symmetrical procedures. Those procedures require the prior distribution of a secret shared with the other participants, and come lack Perfect Forward Secrecy (another serious disadvantage). If the shared secret becomes known, all previously recorded communication can be decrypted.

## Symmetric Encryption of the Asymmetric Key Exchange

Symmetric encryption with sufficiently long keys is quantum safe. With a symmetric signature, an asymmetric key exchange procedure can be secured symmetrically. This is the most efficient method for network encryption, but is only practicable for static site-to-site networks.

## Quantum Key Distribution (QKD)

QKD transmits the keys as photons over an optical link. The maximum distance achieved in test labs is below 200km. QKD is also only practicable for static site networks as it requires a dedicated optical connection. 

The serious disadvantages of this technology (optical connection, short distance, and high costs) preclude its use in most real-life solutions. Since it does not work over packet networks like Ethernet or IP, its use is limited to optical layer 1 networks.

## Post-Quantum Cryptography (PQC)

A generally applicable solution offers the use of key exchange methods that are also resistant to attacks by quantum computers. Several such methods are available, but their resistance to attacks by quantum computers has not yet been proven. There are first systems that already implement PQC. One of the first was a Layer-3 (IP) encryptor developed by VDOM Research using Kyber. In the meantime, there are also established providers such as Atmedia, Secunet and Securosys, who optionally offer support for Frodo, a quantum-secure key exchange method. 

In general, however, it should be noted that the selected algorithms in their current form do not correspond to what will be widely used in a few years. Currently, the primitives are not yet fully developed and tested. Both in the USA (NIST) and in China, a competition is currently underway that should lead to the standardization of PQC algorithms.