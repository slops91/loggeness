The Coordinated Set Identification Profile (CSIP) defines how Bluetooth devices can identify and operate as part of a Coordinated Set—a group of devices configured to act together in a specific use case. Common examples include a pair of earbuds, stereo speakers, or even medical sensors like EKG leads that perform synchronized operations. CSIP itself is agnostic to the actual functionality of these devices; its role is to define how they can be discovered, identified, and managed as part of a set. Importantly, it also provides a mechanism to grant exclusive access to the Coordinated Set to prevent race conditions when multiple clients attempt to control the same devices simultaneously.

This profile depends on the Generic Attribute Profile (GATT) defined in the Bluetooth Core Specification and is compatible with Bluetooth version 4.2 or later. Any device claiming conformance to CSIP must fully support all mandatory features as defined in the specification.

The document also outlines language conventions used across Bluetooth specifications. For instance, the word shall indicates a strict requirement, should expresses a recommendation, and may denotes permission or an optional behavior. Fields marked as “Reserved for Future Use (RFU)” must be set to zero and ignored on reception, while fields marked as “Prohibited” must never be used.

Three key terms are essential for understanding CSIP:

A Coordinated Set is a group of devices configured to support a shared scenario.

A Set Coordinator is the device responsible for discovering and managing these devices.

Set Members are the devices that belong to the Coordinated Set and follow the Coordinator’s control.

⚙️ Section 2: Configuration

CSIP defines two distinct roles — the Set Coordinator and the Set Member. The Set Coordinator acts as a GATT client responsible for discovering Coordinated Sets and their members. Each Coordinated Set can include one or more Set Members. The Set Member, in turn, functions as a GATT server that provides the Coordinated Set Identification Service (CSIS), which enables identification and coordination with the Coordinator.

Regarding topology, when CSIP is used over Bluetooth Low Energy (LE) transport, the Set Coordinator must operate in the GAP Central role, and the Set Member in the GAP Peripheral role. For BR/EDR transport, the Set Coordinator acts as the GAP A-party (inquirer) while the Set Member acts as the GAP B-party (scanner) during discovery procedures. There are no specific restrictions on concurrency or transport for this profile, though higher-layer specifications may impose additional requirements.

Each Set Member must include one instance of CSIS per Coordinated Set it belongs to. If a device participates in multiple sets, it must instantiate multiple CSIS instances, each with a unique Set Identity Resolving Key (SIRK). These instances help identify and differentiate among different coordinated sets that a single device may belong to.

The RSI (Resolvable Set Identifier) is included in the advertising or scan response data in LE or in the extended inquiry response data in BR/EDR. This RSI allows a Set Coordinator to identify which devices belong to a specific Coordinated Set. If a device participates in multiple sets, it can advertise multiple RSIs, one for each set. The Coordinated Set Size characteristic must remain consistent across all devices within the same set, ensuring synchronization among all members.

🔐 Section 3: Coordinator Role, Procedures & Security

The Set Coordinator plays a central role in managing the Coordinated Set through a sequence of discovery and control procedures. It uses GATT sub-procedures such as service discovery, characteristic discovery, and read/write operations to identify and interact with Set Members. The Coordinator must discover services like CSIS, read key characteristics such as SIRK, Coordinated Set Size, and Set Member Rank, and use these values to verify membership within a Coordinated Set.

The specification defines several key procedures. The Coordinated Set Discovery Procedure allows the Coordinator to identify a set’s identity by reading the SIRK from a Set Member. Once the SIRK is obtained, the Set Members Discovery Procedure helps find all devices that share this SIRK, confirming them as part of the same Coordinated Set. The Lock Request and Release Procedures are used to ensure exclusive access to the set. By locking, the Coordinator prevents simultaneous access by other clients, avoiding conflicts. If multiple Coordinators exist, they must wait until the lock is released before performing operations. When bonding is not supported, the Ordered Access Procedure can be used to sequence operations safely without full locking.

In terms of security, CSIP requires encryption and authentication consistent with Bluetooth Security Mode 1 Level 2 or higher. Both Coordinators and Members should support Bondable mode, and 128-bit key entropy is required for encrypted access to CSIS characteristics. Cross-Transport Key Derivation (CTKD) is recommended to allow seamless transitions between BR/EDR and LE transports without re-pairing. Privacy mechanisms such as periodically changing private addresses and RSI values should be used to prevent tracking. When privacy is enabled, devices should advertise RSI values derived only from encrypted SIRKs and operate primarily in Limited Discoverable Mode.

Finally, the Generic Access Profile (GAP) for BR/EDR requires that both Coordinators and Members support either Limited or General Discoverable modes, along with optional Bondable mode. The Set Coordinator should implement the General Inquiry procedure to discover Set Members, while both roles may optionally support the General Bonding procedure to maintain secure connections.

Would you like me to continue this into two more OneNote sections (e.g., “Procedures in Detail” and “Acronyms & References”) with a similar paragraph format — so the entire CSIP spec is covered neatly for your notes?

You said:
yes
ChatGPT said:

Perfect 👍 — here’s the continuation, completing your OneNote notebook for Bluetooth CSIP v1.0.1, in the same clear paragraph-based format, so you can directly copy-paste into your OneNote as 2 more titled sections:

⚙️ Section 4: Procedures in Detail

The Coordinated Set Identification Service (CSIS) defines a structured set of procedures that enable device discovery, membership verification, and safe coordination across all devices in a set. The first is the Coordinated Set Discovery Procedure, which allows a Set Coordinator to identify the unique identity of a Coordinated Set. The identity is represented by a Set Identity Resolving Key (SIRK), a value that may be stored in encrypted form or plain text. The Set Coordinator begins by identifying at least one Set Member using advertising data or other discovery mechanisms. Once found, it reads the SIRK from the device’s CSIS characteristics. If the SIRK is encrypted, the Coordinator must decrypt it using the specified decryption function from the CSIS specification. Upon successfully retrieving the SIRK and other related values such as Set Member Rank and Coordinated Set Size, the discovery procedure is considered complete.

After obtaining the SIRK, the Coordinator initiates the Set Members Discovery Procedure, which aims to find all members of the Coordinated Set. The Coordinator uses the SIRK to resolve the Resolvable Set Identifiers (RSIs) broadcasted by other devices. If an RSI is successfully resolved using the SIRK, that device is confirmed to be a member of the same Coordinated Set. The Coordinator then connects to each discovered Set Member, verifies its SIRK, and establishes a secure bond. The procedure continues until all members are discovered, or until a timer expires—typically set to 10 seconds unless defined otherwise by higher-layer specifications.

The Lock Request Procedure is an essential mechanism for preventing race conditions. It allows a Coordinator to acquire exclusive access to a Coordinated Set, ensuring that no other Coordinators can modify or control it simultaneously. This is particularly important in scenarios such as synchronized playback or configuration updates. The Coordinator locks Set Members one by one in ascending order of their rank. If any Set Member denies the lock request (for example, because another Coordinator already holds the lock), the procedure is aborted, and the Coordinator performs a Lock Release Procedure to revert the locks it has already obtained. Once the Set is unlocked, Coordinators waiting for access can retry.

The Lock Release Procedure reverses the locking operation. It is initiated when a Coordinator completes its tasks and wishes to release control so that other Coordinators may access the set. During this procedure, the Coordinator writes the “Unlocked” value to the Lock characteristic of each Set Member, proceeding in decreasing order of rank. The specification also describes the Ordered Access Procedure, a lightweight alternative used when devices are not bonded. It does not require full locking but instead ensures ordered execution by reading each Set Member’s lock state and performing actions sequentially. This reduces the likelihood of conflicts without establishing full exclusivity.

Finally, the Connection Establishment Procedure defines how a Coordinator and Set Member connect to each other. If a higher-layer specification does not impose additional requirements, the connection should be established using standard Bluetooth GAP connection modes. The Coordinator typically initiates the connection using General Discovery procedures, while the Set Member remains in discoverable and connectable states until paired.

🔒 Section 5: Security, GAP Modes & References

Security is a critical component of the CSIP specification. It ensures that only authorized Coordinators and Set Members can access or control the Coordinated Set. For Bluetooth Low Energy (LE) transport, all CSIS characteristics must meet Security Mode 1, Level 2 (SM1 L2) or higher, which enforces authenticated pairing and encryption. Both Coordinators and Members must support 128-bit encryption keys, derived from either LE Secure Connections, BR/EDR Secure Connections with Cross-Transport Key Derivation (CTKD), or out-of-band (OOB) methods. Privacy mechanisms, as defined in the Bluetooth Core Specification, should also be employed.

The Set Coordinator should operate in Bondable mode, allowing secure bonding with Set Members for persistent security keys. It should accept the security level requested by the Set Member and support CTKD to prevent the need for multiple pairing processes across transports. When privacy is used, the Coordinator must distribute its Identity Address (IA) and Identity Resolving Key (IRK), allowing trusted members to resolve its private address.

The Set Member must enforce similar security standards. It accepts only security levels that meet its requirements and must regenerate new Resolvable Set Identifiers (RSIs) whenever its private address changes, preventing devices from being tracked over time. A privacy-enabled Set Member should advertise RSIs only when in Limited Discoverable Mode, using SIRKs that are stored in encrypted form. If privacy is disabled, RSI refresh periods or renewals can be governed by higher-layer rules.

For BR/EDR transport, CSIP specifies Security Mode 4, Level 2 (SM4 L2), ensuring encryption and authentication. Both Coordinator and Member devices should use 128-bit keys derived from Secure Connections or CTKD. BR/EDR devices using CTKD can share keys between LE and BR/EDR connections to enhance user experience and reduce re-pairing needs. Devices supporting both transports must distribute their IA and IRK when privacy is active.

Additional considerations apply when using both BR/EDR and LE transports simultaneously. Devices using the Just Works pairing model should notify the user when pairing starts and succeeds—through an LED, sound, or vibration. A user action, such as pressing a button, should initiate pairing in such devices to ensure intentional connections. Importantly, if one Set Member uses an encrypted SIRK, all others in the same set must not expose that SIRK in plain text, maintaining the security of the Coordinated Set’s shared identity.

Finally, the Generic Access Profile (GAP) defines required and optional operational modes for BR/EDR devices. Both the Set Member and the Set Coordinator must support either the Limited Discoverable Mode or the General Discoverable Mode, with Bondable mode recommended for persistent pairing. The Coordinator must implement the General Inquiry Procedure to detect discoverable devices and may optionally use the Limited Inquiry Procedure for restricted searches. Both roles can support General Bonding to establish secure, reusable connections.

In summary, the Acronyms and References section of the CSIP specification defines key terms and supporting documents. Abbreviations such as BR/EDR (Basic Rate/Enhanced Data Rate), CSIS (Coordinated Set Identification Service), RSI (Resolvable Set Identifier), and SIRK (Set Identity Resolving Key) are frequently used throughout the document. The specification directly references two key standards: the Coordinated Set Identification Service Specification (v1.0) and the Bluetooth Core Specification (v4.2 or later), which together provide the foundational definitions and behaviors upon which CSIP operates.
