index: yes
toc_title: Overview

Theoretically, quantum computers can break common key establishment methods such as RSA, Diffie-Hellman and ECC (Elliptic Curve Cryptography) in no time at all. How real and how big is the risk really? Let’s have a look at the threat and the countermeasures.

### Quantum computers as threat

François Weissbaum, cryptographer at the Swiss Federal Department of Defense, provided an excellent introduction of this topic at an event organized by the [Security Interest Group Switzerland](https://www.sig-switzerland.ch/) in February 2017. Here is a short summary of his talk.

Traditional computers are based on bits. Each bit has either a value of O or 1. The system is deterministic; only definable and reproducible states occur. Quantum computers are based on qubits. Each qubit can have a value of 0, 1 or a quantum superposition of these two qubit states. A pair of qubits can be in any quantum superposition of four states, while three qubits can be in any superposition of eight states. A quantum register contains significantly more values than a classical binary register. Qubits are two-state systems that can be visually represented by a Bloch sphere.

Quantum computers provide the basis for new algorithms. Thus, the question arises which problems can be solved if universal quantum computers are available. With regard to breaking encryptions, two algorithms currently exist which could be effectively used if a universal quantum computer with at least 64 qubits is available: Shor's algorithm and Grover's algorithm. The first one reduces the time needed for integer factorization and the calculation of discrete logarithms. The fast integer factorization can crack the RSA method. Diffie-Hellman, DSA (Digital Signature Algorithm), ElGamal signature methods and Elliptic Curve Cryptography (ECC) are based on the problem of the discrete logarithm and are therefore also affected. All affected procedures are exclusively asymmetric cryptosystems. In contrast, Grover's algorithm can crack symmetric keys by means of brute force. For a 128-bit key, however, 2 to the power of 64 (18'446'744'073'709'551'616) iterations are required.

The effects of quantum computers on cryptography are currently extremely limited. To assess the future impact, you have to ask the hypothetical question of the security implications in the event that a universal quantum computer would be available. For the attack on symmetric keys, only Grover's algorithm is currently available. To avert the danger, it is sufficient to double the key lengths to maintain the same level of security. Even when using Grove's algorithm with a universal quantum computer, an AES key with a length of 256 bits still offers the level of security that an AES key with a length of 128 bits offers today when using classical computers. 

The only known algorithm to break hash functions is also Grover's algorithm. Lengths of 384 bits are theoretically safe even when universal quantum computers are available. This concerns SHA-384, SHA-512, SHA3-384 and SHA3-512. Even practicable attacks on SHA-256 and SHA3-256 are not possible in the foreseeable future.

The situation is different for asymmetric crypto systems. Shor's algorithm can solve problems like factorization and discrete logarithm quickly and efficiently. If a universal quantum computer existed, all of today's traditional asymmetric procedures would be unsafe.

INFO: Public Key Infrastructure needs two algorithms: one for hash functions and one for the digital signature. Only the digital signature algorithms use an asymmetric crypto system and are vulnerable.

For more information, please read a [study on quantum computing](https://www.bsi.bund.de/EN/Topics/Crypto/Cryptography/QuantumComputing/quantum_computing_node.html) released by the German Federal Office for Information Security (BSI).
