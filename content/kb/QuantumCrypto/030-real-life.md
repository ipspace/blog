---
kb_section: QuantumCrypto
minimal_sidebar: true
title: Real-Life Solutions Explained
url: /kb/QuantumCrypto/030-real-life/
---
The two approaches to post-quantum cryptography that are the most practical and efficient for packet networks are:

* Symmetric encryption of the asymmetric key exchange
* Post-quantum cryptography (using cryptographic methods that are not affected by Grover's or Shor's algorithms).

## Symmetric Encryption of Asymmetric Key Exchange

This is the approach selected by a leading developer of high-assurance network encryption devices, the German company Atmedia. Co-founder and co-CEO Jörg Friedrich explains why and how they do it:

---

Starting the development of our high-speed encryption products 20 years ago, we decided to offer a robust and largely future proof encryption solution to customers. Since Perfect Forward Secrecy (PFS) and an overall key strength of 256 bit were required, we decided to use an asymmetric key agreement scheme based on Elliptic Curve Cryptography (ECDH). The device authentication (protection against Man-in-the-Middle attacks) has been realized with symmetric AES encryption based on pre-shared secrets. A key derivation function uses these components to generate the SA (security association) keys which are used to exchange master keys.

The resulting system is a hybrid approach, where the customer can select if ECDH is used at all and which curves are used (Brainpool, NIST or other custom curves). An operation of the encryptors with symmetric cryptography only is possible, enabling external (grey box) testing of the main encryption functionality by the customer.The pre-shared keys are distributed via Smartcards or can be internally generated by an ad-hoc authentication function. The above scheme is resistant against known quantum based attacks because of the AES256 encryption. It is also highly resistant against side channel and timing attacks on ECDH, which could break PFS in the worst case only.

We are currently evaluating post quantum cryptography (PQC) candidates from the BSI and NIST. At least one of these algorithms will be included as an additional component in the key derivation function for the SA keys in upcoming firmware releases of our encryption products supporting the existing hybrid model together with PQC.

## Post-Quantum Cryptography

The second approach is to use post-quantum cryptography (PQC), explained by Denis Kolegov, associate professor of computer security at Tomsk State University and former research engineer at VDOM Research (Denis participated in two different projects that used PQC)

---

The first project we did with PQC was in 2017/2018 and was the development of a high-assurance quantum-safe IP network encryptor. We did not invent our own post-quantum cryptographic primitives for key establishment; as there was a choice of existing primitives available, such as NewHope, Kyber, Frodo, etc. The main goal was to develop a new VPN protocol combining post-quantum and pre-quantum (classic) cryptography algorithms. The protocol was based on WireGuard state machine and Noise protocol framework, but we did not use Noise's Hybrid Forward Secrecy extension. Instead we developed a new protocol to meet the product security requirements. We chose Kyber for the following two main reasons: 

* When we prototyped the system, we wanted to know whether the encryptor is capable to process packets in modern networks with the highest throughput. There are several variants of Kyber with different public key and cipher text lengths and different security levels
* Kyber can be used in authenticated key exchange by design.

At the same time NewHope, for example, is a passively secure KEM (key encapsulation mechanism) that provides post-quantum confidentiality but pre-quantum authenticity (See https://pq-crystals.org/kyber/data/kyber-specification-round2.pdf, section 1.5). This means that you can't use NewHope if you want to authenticate a peer by its means. You have to use post-quantum signatures or something else (cf. https://cryptojedi.org/papers/newhope-20190710.pdf, section 2.3). 

The promising results of the project: The VPN protocol worked well within the encryptor platform and was formally verified later. Kyber can and will be replaced by a new standardized primitive.

The second project was a small joint project with the CloudFlare crypto team. The goal was to implement Noise Hybrid Forward Secrecy (IKhfs) pattern on nQUIC for several post-quantum KEMs and then measure connection parameters. 

nQUIC is a variant of QUIC-TLS that uses the Noise protocol framework for its key exchange. nQUIC can be used as alternative to the standard TLS layer in QUIC. We measured Kyber512 and SIKE-P434 performance. The measurements showed that post-quantum nQUIC with the selected primitives can be used in the QUIC protocol. The handshake time increased by several milliseconds only and CPU load increased only marginally.

The results are  described in the "The TLS Post-Quantum Experiment" (https://blog.cloudflare.com/the-tls-post-quantum-experiment/) and nQUIC (https://eprint.iacr.org/2019/028.pdf) papers. 
