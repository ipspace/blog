---
kb_section: QuantumCrypto
minimal_sidebar: true
title: Hype and Reality
url: /kb/QuantumCrypto/040-hype.html
---
Not surprisingly, vendor marketing teams don't always get it right when talking about Quantum Key Distribution (QKD) or Quantum Random Number Generators (QRNG).

## Why a Quantum Random Number Generator Doesn't Help

Random number generators generate random numbers. For this you need a good entropy source and this is definitely available in a QRNG. But the random number with good entropy does not protect at all against attacks by quantum computers and is therefore not quantum safe. There are also many alternatives for a good entropy source.

## Too Complicated for Self-Proclaimed Security Experts

If one happens to read announcements and marketing materials from security vendors after understanding the basics of post-quantum cryptography, one comes to an inevitable conclusion that "security experts" such as Fortinet or Thales have understood neither QKD nor QRNG correctly, but are using it in marketing anyway. 

Neither Fortinet nor Thales have Layer-1 encryptors, which would the most reasonable solution for the combination of optical networks and short distances. QKD does not work over longer distances. And operating an optical network just to be able to implement the key exchange via photons does not make sense. The symmetric encryption of the asymmetric key exchange is cheaper, works also with packet networks and is quantum safe.

The low level of practical thinking and knowledge is also shown by the efforts for a quantum internet. The Internet is a packet network and QKD needs an optical network. A large amount of research money is wasted, which would be better used elsewhere.

## More Information

Powerful quantum computers seem to be inevitable, and we should evaluate the risks and get prepared. BSI has published [recommendations for action](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Krypto/Post-Quanten-Kryptografie.pdf?\_\_blob=publicationFile&v=2) based on the current state of technology art and logical reasoning, offering a good overview of existing possibilities, and showing how a migration to PQC is possible. 

The recommendations are currently available only in German, but we can hope that an English version will be available soon.
