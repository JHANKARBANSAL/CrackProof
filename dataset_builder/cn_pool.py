"""
Computer Networks Question Pool: 8 Questions x 3 Samples = 24 Samples.
Coverage:
CN_01: TCP vs UDP & 3-Way Handshake
CN_02: Transport Layer vs Network Layer in OSI
CN_03: OSI 7-Layer vs TCP/IP 4-Layer Model
CN_04: HTTP vs HTTPS & SSL/TLS Encryption
CN_05: DNS Resolution Workflow
CN_06: IPv4 vs IPv6 & CIDR Subnetting
CN_07: TCP Flow Control vs Congestion Control
CN_08: Lifecycle of a Web Request (URL to Page Render)
"""

CN_POOL = [
    {
        "question_id": "CN_01",
        "subject": "CN",
        "question": "What is the difference between TCP and UDP, and how does the TCP 3-way handshake establish a connection?",
        "reference": "[1] TCP is a connection-oriented, reliable transport protocol providing ordered delivery, error checking, retransmissions, flow control, and congestion control with higher header overhead (20 bytes). UDP is connectionless, unreliable (best-effort), and low-latency without delivery guarantees or retransmissions (8-byte header). The TCP 3-way handshake establishes synchronization: Client sends SYN (seq=x), Server responds with SYN-ACK (seq=y, ack=x+1), and Client sends ACK (ack=y+1).",
        "samples": [
            {
                "answer": "TCP is connection-oriented and reliable, guaranteeing in-order delivery through packet sequence numbers, ACKs, retransmissions, and flow/congestion control, at the cost of higher header overhead (20 bytes). UDP is connectionless and lightweight (8-byte header), sending packets without connection setup or retransmission guarantees, making it ideal for real-time applications like DNS, gaming, and streaming. The TCP 3-way handshake establishes a session: 1. Client sends SYN with initial sequence number x; 2. Server responds with SYN-ACK with its own sequence number y and ACK=x+1; 3. Client sends ACK=y+1, establishing the connection.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["TCP is connection-oriented, reliable, and ordered with error-correction and flow control", "UDP is connectionless, best-effort, and low-latency for real-time data", "Handshake Step 1: SYN (client seq=x)", "Handshake Step 2: SYN-ACK (server seq=y, ack=x+1)", "Handshake Step 3: ACK (client ack=y+1)"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["TCP 4-way FIN teardown", "SYN flood denial-of-service attack and SYN cookies"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted reliability and overhead between TCP and UDP."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Detailed sequence and acknowledgment arithmetic of the 3-way handshake."}
                    ],
                    "citations": [{"claim": "TCP is connection-oriented, reliable... UDP is connectionless, unreliable... 3-way handshake: SYN... SYN-ACK... ACK", "source_number": 1}],
                    "reasoning": "Clear, technically thorough explanation covering both protocol characteristics and precise handshake sequence number mechanics."
                }
            },
            {
                "answer": "TCP reliable hota hai aur UDP fast hota hai. Handshake me client server ko pehle hi/hello bolte hain fir connection ban jata hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["TCP is reliable", "UDP is faster"],
                    "missing_core_concepts": ["Specific 3-way handshake packets: SYN, SYN-ACK, ACK", "Sequence numbers and acknowledgment numbers", "Why TCP is reliable (retransmissions, ordering, flow control)"],
                    "deeper_concepts_to_probe": ["SYN, SYN-ACK, ACK packets"],
                    "misconceptions": ["Vague conversational description ('hi/hello') rather than technical packet flags and sequence synchronization"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Knew the high-level trade-off but gave superficial 'hi/hello' description for handshake."}
                    ],
                    "citations": [{"claim": "The TCP 3-way handshake establishes synchronization: Client sends SYN (seq=x), Server responds with SYN-ACK (seq=y, ack=x+1), and Client sends ACK", "source_number": 1}],
                    "reasoning": "High-level intuition on speed vs reliability is present, but handshake description lacks technical rigor and packet names."
                }
            },
            {
                "answer": "TCP is a wireless protocol for Wi-Fi routers, while UDP is a physical Ethernet cable plugged into the wall.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Both TCP and UDP are Layer 4 transport protocols operating over any physical medium"],
                    "deeper_concepts_to_probe": ["OSI transport layer protocols"],
                    "misconceptions": ["Confusing transport layer protocols with physical cables and wireless hardware"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Confused transport layer protocols with physical media."}
                    ],
                    "citations": [{"claim": "TCP is a connection-oriented, reliable transport protocol... UDP is connectionless", "source_number": 1}],
                    "reasoning": "Complete confusion between transport layer software protocols and physical networking hardware."
                }
            }
        ]
    },
    {
        "question_id": "CN_02",
        "subject": "CN",
        "question": "What is the primary function of the Transport Layer in the OSI model, and how does it differ from the Network Layer?",
        "reference": "[1] In the OSI model: The Network Layer (Layer 3, e.g. IP) is responsible for host-to-host packet routing across intermediate routers using logical IP addresses. The Transport Layer (Layer 4, e.g. TCP, UDP) is responsible for end-to-end (process-to-process) communication between applications using port numbers, providing segmentation, multiplexing, flow control, and optional reliability.",
        "samples": [
            {
                "answer": "The Network Layer (Layer 3) handles host-to-host delivery, routing packets across diverse intermediate networks using IP addresses. The Transport Layer (Layer 4) handles process-to-process (end-to-end) communication between specific software applications on those hosts using port numbers. While Layer 3 gets packets from Machine A to Machine B, Layer 4 delivers data directly to the specific application process (e.g. web browser on port 80/443), managing segmentation, reassembly, and optional reliability.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Network layer provides host-to-host delivery using IP addressing and routing", "Transport layer provides process-to-process / end-to-end delivery using port numbers", "Transport layer manages segmentation, reassembly, multiplexing, and optional flow control"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Port numbers and socket abstraction", "Role of routers (operating at L3) vs end hosts (processing L4)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Precisely contrasted host-to-host (L3) with process-to-process (L4)."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly linked IP addresses to L3 and port numbers to L4."}
                    ],
                    "citations": [{"claim": "Network Layer... is responsible for host-to-host packet routing... Transport Layer... is responsible for end-to-end (process-to-process) communication between applications using port numbers", "source_number": 1}],
                    "reasoning": "Clear, precise distinction between host-to-host routing and process-to-process application multiplexing."
                }
            },
            {
                "answer": "Transport layer data transport karta hai jaise TCP aur UDP. Network layer internet connection banata hai routers ke through. Dono data transfer karte hain bas alag alag speed pe.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["Transport layer includes TCP and UDP", "Network layer involves routers"],
                    "missing_core_concepts": ["Host-to-host (L3 / IP) vs process-to-process (L4 / Port numbers) distinction", "Port addressing and multiplexing"],
                    "deeper_concepts_to_probe": ["Process-to-process addressing via ports"],
                    "misconceptions": ["Believing layers differ primarily by transfer speed rather than addressing and functional scope"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Named protocols and hardware but failed to articulate addressing and scoping differences."}
                    ],
                    "citations": [{"claim": "Network Layer (Layer 3, e.g. IP)... host-to-host... Transport Layer (Layer 4, e.g. TCP, UDP)... process-to-process... using port numbers", "source_number": 1}],
                    "reasoning": "Vague understanding naming protocols, but lacked the core host-to-host vs process-to-process distinction."
                }
            },
            {
                "answer": "Transport layer is for physical fiber optic cables and Network layer is for satellite Wi-Fi.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Physical media is Layer 1 (Physical layer); L3 is Network Layer (IP) and L4 is Transport Layer (TCP/UDP)"],
                    "deeper_concepts_to_probe": ["OSI layer stack"],
                    "misconceptions": ["Mapping layers 3 and 4 to physical transmission media"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total confusion with physical layer media."}
                    ],
                    "citations": [{"claim": "In the OSI model: The Network Layer (Layer 3...)... The Transport Layer (Layer 4...)", "source_number": 1}],
                    "reasoning": "Completely incorrect answer confusing higher-level software layers with physical cables and satellites."
                }
            }
        ]
    },
    {
        "question_id": "CN_03",
        "subject": "CN",
        "question": "What are the seven layers of the OSI model, and how do they map to the four layers of the TCP/IP model?",
        "reference": "[1] The 7 layers of the OSI model (from bottom to top) are: Physical (L1), Data Link (L2), Network (L3), Transport (L4), Session (L5), Presentation (L6), and Application (L7). In the 4-layer TCP/IP model: OSI L1 and L2 map to the Network Access / Link layer; OSI L3 maps to the Internet layer (IP); OSI L4 maps to the Transport layer (TCP/UDP); and OSI L5, L6, and L7 are collapsed into a single Application layer (HTTP, DNS, FTP).",
        "samples": [
            {
                "answer": "The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application. The TCP/IP model simplifies this into 4 layers: 1. Network Access (combines OSI Physical and Data Link), 2. Internet layer (corresponds to OSI Network layer / IP), 3. Transport layer (corresponds directly to OSI Transport layer / TCP/UDP), and 4. Application layer (merges OSI Session, Presentation, and Application layers together).",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Accurately listed all 7 OSI layers in order", "Mapped OSI L1/L2 to TCP/IP Network Access / Link layer", "Mapped OSI L3 to TCP/IP Internet layer", "Mapped OSI L4 to TCP/IP Transport layer", "Mapped OSI L5/L6/L7 to TCP/IP Application layer"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Encapsulation and header addition across layers (PDU names: Bits, Frames, Packets, Segments)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately recited the complete 7-layer stack."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Provided the exact 7-to-4 mapping between OSI and TCP/IP."}
                    ],
                    "citations": [{"claim": "Physical (L1), Data Link (L2), Network (L3), Transport (L4), Session (L5), Presentation (L6), and Application (L7)... mapped to 4-layer TCP/IP", "source_number": 1}],
                    "reasoning": "Flawless, comprehensive recall of the 7 OSI layers and their exact mapping to the 4 TCP/IP layers."
                }
            },
            {
                "answer": "OSI me 7 layers hoti hain: Physical, Data Link, Network, Transport, aur upar Application layer. TCP/IP chhota model hota hai jisme 4 layers hoti hain.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["OSI has 7 layers and named Physical, Data Link, Network, Transport, Application", "TCP/IP has 4 layers"],
                    "missing_core_concepts": ["Session and Presentation layers in OSI", "Explicit mapping from the 7 layers to the 4 TCP/IP layers"],
                    "deeper_concepts_to_probe": ["Session and Presentation layers"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Omitted Session and Presentation layers and gave no mapping details."}
                    ],
                    "citations": [{"claim": "Session (L5), Presentation (L6)... OSI L5, L6, and L7 are collapsed into a single Application layer", "source_number": 1}],
                    "reasoning": "Omitted Session and Presentation layers and did not explain how the layers map between the two models."
                }
            },
            {
                "answer": "OSI model has 10 layers and TCP/IP has 8 layers, designed by Microsoft for Windows 95.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["OSI has strictly 7 layers; TCP/IP has 4 layers (or 5 in updated models), designed by ISO and DARPA"],
                    "deeper_concepts_to_probe": ["Networking reference models"],
                    "misconceptions": ["Inventing non-existent layer counts and attributing them to Microsoft Windows 95"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Gross factual errors regarding layer counts and origins."}
                    ],
                    "citations": [{"claim": "The 7 layers of the OSI model... In the 4-layer TCP/IP model", "source_number": 1}],
                    "reasoning": "Completely inaccurate layer counts and historical origin."
                }
            }
        ]
    },
    {
        "question_id": "CN_04",
        "subject": "CN",
        "question": "What is the difference between HTTP and HTTPS, and how does SSL/TLS encryption protect data in transit?",
        "reference": "[1] HTTP (Hypertext Transfer Protocol, port 80) transmits plaintext data, leaving traffic vulnerable to packet sniffing, eavesdropping, and man-in-the-middle (MITM) attacks. HTTPS (HTTP Secure, port 443) runs HTTP over TLS/SSL encryption. During the TLS handshake, the server authenticates its identity via a digital certificate issued by a trusted Certificate Authority (CA), asymmetric public-key cryptography is used to securely exchange/derive a symmetric session key, and subsequent payload data is encrypted using high-speed symmetric encryption (e.g. AES-GCM), guaranteeing confidentiality, integrity, and authenticity.",
        "samples": [
            {
                "answer": "HTTP transmits data in plaintext over port 80, making it vulnerable to eavesdropping and man-in-the-middle attacks. HTTPS runs over port 443 and secures HTTP using TLS/SSL encryption. During the TLS handshake, the client verifies the server's identity through an SSL certificate signed by a Certificate Authority. They use asymmetric encryption (like RSA or Diffie-Hellman) to safely negotiate a shared symmetric session key, and all subsequent application data is encrypted using fast symmetric encryption (like AES), ensuring confidentiality, data integrity, and authentication.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["HTTP transmits plaintext over port 80; vulnerable to MITM/sniffing", "HTTPS encrypts traffic using TLS/SSL over port 443", "Server authenticates via CA-signed digital certificate", "Asymmetric crypto negotiates symmetric session key", "Symmetric encryption secures subsequent application payload for confidentiality and integrity"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Diffie-Hellman Ephemeral (DHE/ECDHE) for Perfect Forward Secrecy", "TLS 1.3 1-RTT handshake improvements"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted port numbers, plaintext vulnerabilities, and TLS protection."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained the hybrid cryptography model (asymmetric handshake + symmetric payload)."}
                    ],
                    "citations": [{"claim": "HTTP transmits plaintext data... HTTPS runs HTTP over TLS/SSL encryption... asymmetric public-key cryptography... symmetric session key", "source_number": 1}],
                    "reasoning": "Clear, precise explanation detailing ports, vulnerabilities, certificates, and the hybrid encryption handshake."
                }
            },
            {
                "answer": "HTTP me data plaintext me jata hai jise koi bhi hack kar sakta hai. HTTPS me green lock icon aata hai aur data encrypt ho jata hai SSL se taaki secure rahe.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["HTTP transmits plaintext data vulnerably", "HTTPS encrypts data using SSL/TLS"],
                    "missing_core_concepts": ["Ports: 80 vs 443", "How TLS encryption works: CA certificates and asymmetric/symmetric hybrid key exchange", "Integrity and authentication benefits"],
                    "deeper_concepts_to_probe": ["TLS handshake key exchange"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood the security difference but described it casually using browser icons without cryptographic mechanics."}
                    ],
                    "citations": [{"claim": "HTTPS... runs HTTP over TLS/SSL encryption... authenticates its identity via a digital certificate... symmetric session key", "source_number": 1}],
                    "reasoning": "High-level understanding is correct, but lacks technical depth regarding ports, certificates, and asymmetric/symmetric encryption."
                }
            },
            {
                "answer": "HTTPS means the website is owned by the government, whereas HTTP is for personal blogs.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["HTTPS is standard TLS encryption for any website, unrelated to government ownership"],
                    "deeper_concepts_to_probe": ["Web security protocols"],
                    "misconceptions": ["Believing HTTPS indicates government ownership"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Bizarre social misconception."}
                    ],
                    "citations": [{"claim": "A primary use of TLS is to secure World Wide Web traffic between a website and a web browser encoded with the HTTP protocol", "source_number": 1}],
                    "reasoning": "Completely inaccurate and non-technical claim."
                }
            }
        ]
    },
    {
        "question_id": "CN_05",
        "subject": "CN",
        "question": "How does DNS resolution work step-by-step when translating a domain name to an IP address?",
        "reference": "[1] DNS (Domain Name System, port 53 UDP/TCP) translates human-readable domain names into machine-routable IP addresses. Resolution workflow: 1. Browser/OS checks local DNS cache. 2. If missed, queries the Local DNS Recursive Resolver (ISP or 8.8.8.8). 3. Resolver queries the Root DNS Server ('.'), which returns the Top-Level Domain (TLD) server (e.g. '.com'). 4. Resolver queries the TLD server, which returns the Authoritative Name Server for the domain. 5. Resolver queries the Authoritative Name Server, which returns the target A/AAAA IP record. 6. Resolver caches the IP based on TTL and returns it to the client.",
        "samples": [
            {
                "answer": "When a domain name like example.com is requested: 1. The client checks local browser cache and OS hosts file/cache. 2. If missed, it queries the local Recursive Resolver (e.g. ISP or 1.1.1.1). 3. The recursive resolver queries a Root DNS server, which directs it to the TLD server (like .com). 4. The resolver queries the .com TLD server, which returns the Authoritative Name Server for example.com. 5. The resolver queries the Authoritative Name Server, which returns the actual IP address (A/AAAA record). 6. The resolver caches the IP based on the TTL (Time to Live) and returns it to the client.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Checks local browser and OS DNS cache first", "Queries Recursive Resolver", "Recursive resolver queries Root Server ('.')", "Root directs to TLD Server (e.g. '.com')", "TLD directs to Authoritative Name Server", "Authoritative server returns IP record (A/AAAA)", "Caches result according to TTL"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Iterative vs Recursive queries", "DNS record types (CNAME, MX, NS, TXT)", "DNS over HTTPS (DoH)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately laid out the hierarchical server querying structure."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Specified caching and TTL mechanics."}
                    ],
                    "citations": [{"claim": "Resolution workflow: 1. Browser/OS checks local DNS cache... 2. Recursive Resolver... 3. Root DNS Server... 4. TLD server... 5. Authoritative Name Server... 6. TTL caching", "source_number": 1}],
                    "reasoning": "Clear, comprehensive, and accurate step-by-step description of DNS hierarchical resolution."
                }
            },
            {
                "answer": "Jab hum website ka naam likhte hain to DNS usko IP me convert karta hai. Pehle computer apne cache me dekhta hai fir Google ke server 8.8.8.8 se IP le aata hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["DNS converts domain name to IP", "Checks local cache first", "Queries recursive resolver (like 8.8.8.8)"],
                    "missing_core_concepts": ["Hierarchical resolution steps: Root Servers, TLD Servers, Authoritative Nameservers", "TTL caching concept"],
                    "deeper_concepts_to_probe": ["Root and TLD nameserver roles"],
                    "misconceptions": ["Assuming Google's resolver holds all IPs directly without performing recursive hierarchical lookups"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Captured the end result but omitted the internal hierarchical DNS tree resolution."}
                    ],
                    "citations": [{"claim": "Resolver queries the Root DNS Server... TLD server... Authoritative Name Server", "source_number": 1}],
                    "reasoning": "Understood the basic goal and caching, but omitted the entire hierarchical structure (Root, TLD, Authoritative servers)."
                }
            },
            {
                "answer": "DNS resolution is done by searching Google's web crawler index to see if the website is popular.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["DNS is an address translation directory protocol, completely separate from search engine web crawlers"],
                    "deeper_concepts_to_probe": ["DNS directory service"],
                    "misconceptions": ["Confusing domain name resolution with search engine web indexing"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Confused DNS with search engine indexing."}
                    ],
                    "citations": [{"claim": "DNS translates human-readable domain names into machine-routable IP addresses", "source_number": 1}],
                    "reasoning": "Total confusion between DNS networking infrastructure and search engine indexing."
                }
            }
        ]
    },
    {
        "question_id": "CN_06",
        "subject": "CN",
        "question": "What is the difference between IPv4 and IPv6 addressing, and why is Classless Inter-Domain Routing (CIDR) used in subnetting?",
        "reference": "[1] IPv4 uses 32-bit addresses written in dotted-decimal format (yielding ~4.3 billion unique addresses, now depleted). IPv6 uses 128-bit addresses written in hexadecimal format (yielding ~3.4 x 10^38 addresses, solving exhaustion while eliminating NAT and improving header routing efficiency). Classless Inter-Domain Routing (CIDR) replaces rigid legacy classful addressing (Class A, B, C) using variable-length subnet masking (/prefix notation, e.g. /24), reducing IP address wastage and shrinking global router routing tables through route aggregation (supernetting).",
        "samples": [
            {
                "answer": "IPv4 uses 32-bit addresses in dotted decimal notation, supporting about 4.3 billion addresses which are exhausted. IPv6 uses 128-bit addresses in hexadecimal notation, providing an enormous address space (3.4x10^38) to eliminate address exhaustion and remove the need for NAT. CIDR (Classless Inter-Domain Routing) replaced rigid classful networking (Class A, B, C) with prefix notation (like /24). CIDR prevents massive IP address wastage by allocating variable block sizes and reduces router routing table sizes through route aggregation (supernetting).",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["IPv4 is 32-bit (dotted decimal) with ~4.3 billion addresses (exhausted)", "IPv6 is 128-bit (hexadecimal) with vast address space", "CIDR replaced rigid classful networking (Class A, B, C) using prefix notation", "CIDR minimizes IP address wastage through variable-length allocation", "CIDR shrinks routing tables via route aggregation / supernetting"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Subnet mask bit calculation (network vs host bits)", "IPv6 header simplifications"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted 32-bit vs 128-bit address spaces."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained CIDR's dual benefits of reducing IP waste and aggregating routing tables."}
                    ],
                    "citations": [{"claim": "IPv4 uses 32-bit addresses... IPv6 uses 128-bit addresses... Classless Inter-Domain Routing (CIDR) replaces rigid legacy classful addressing... reducing IP address wastage and shrinking global router routing tables", "source_number": 1}],
                    "reasoning": "Clear, precise differentiation covering address bit lengths, exhaustion reasons, and CIDR route aggregation benefits."
                }
            },
            {
                "answer": "IPv4 32 bit ka hota hai aur IPv6 128 bit ka hota hai. IPv4 khatam ho gaya tha isliye IPv6 banaya gaya. CIDR subnetting ke liye slash notation use karta hai jaise /24.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["IPv4 is 32-bit and IPv6 is 128-bit", "IPv6 addresses address exhaustion", "CIDR uses slash notation like /24 for subnetting"],
                    "missing_core_concepts": ["Why CIDR was needed over classful networking (Class A, B, C waste)", "Route aggregation / supernetting in router tables"],
                    "deeper_concepts_to_probe": ["Route aggregation / supernetting"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Stated bits and slash notation accurately but omitted routing table aggregation and classful comparison."}
                    ],
                    "citations": [{"claim": "CIDR replaces rigid legacy classful addressing... shrinking global router routing tables through route aggregation", "source_number": 1}],
                    "reasoning": "Accurate on bit sizes and notation, but lacked depth on why CIDR replaced classful networking and routing table aggregation."
                }
            },
            {
                "answer": "IPv4 is for version 4 of the internet and IPv6 is for version 6, and CIDR is an antivirus program installed on routers.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["IPv4 and IPv6 are IP addressing specifications; CIDR is an IP routing and subnet allocation method, not antivirus"],
                    "deeper_concepts_to_probe": ["IP addressing schemes"],
                    "misconceptions": ["Believing CIDR is antivirus software"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete misunderstanding of CIDR."}
                    ],
                    "citations": [{"claim": "Classless Inter-Domain Routing (CIDR) replaces rigid legacy classful addressing... in subnetting", "source_number": 1}],
                    "reasoning": "Factually erroneous claim that CIDR is antivirus software."
                }
            }
        ]
    },
    {
        "question_id": "CN_07",
        "subject": "CN",
        "question": "What is the difference between Flow Control and Congestion Control in TCP, and how does the Sliding Window mechanism work?",
        "reference": "[1] In TCP: Flow Control prevents the sender from overwhelming the single receiver (end-to-end mechanism; receiver advertises its available buffer space via the Receive Window 'rwnd' in TCP headers, and the sender's Sliding Window advances only as ACKs arrive). Congestion Control prevents senders from overwhelming the intermediate network routers (global network mechanism; sender maintains a Congestion Window 'cwnd' dynamically tuned via algorithms like Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery). The effective transmission window is min(rwnd, cwnd).",
        "samples": [
            {
                "answer": "Flow control protects the receiver from being overwhelmed by a fast sender. The receiver advertises its available buffer capacity in the TCP header as the Receive Window (rwnd), and the sender uses a sliding window to send data without exceeding rwnd. Congestion control protects the intermediate network infrastructure from being saturated by all traffic; the sender maintains a Congestion Window (cwnd) adjusted dynamically via algorithms like Slow Start and AIMD. The sender's actual allowed transmission window is the minimum of rwnd and cwnd.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Flow control protects single receiver buffer overflow", "Congestion control protects intermediate network routers from saturation", "Flow control uses receive window (rwnd) and sliding window mechanism", "Congestion control dynamically adjusts congestion window (cwnd) via Slow Start / AIMD", "Effective window is min(rwnd, cwnd)"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["TCP Tahoe vs Reno vs BBR congestion algorithms", "Silly Window Syndrome and Nagle's algorithm"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted end-to-end receiver protection vs intermediate network protection."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Identified the governing formula: min(rwnd, cwnd)."}
                    ],
                    "citations": [{"claim": "Flow Control prevents the sender from overwhelming the single receiver... Congestion Control prevents senders from overwhelming the intermediate network routers... effective transmission window is min(rwnd, cwnd)", "source_number": 1}],
                    "reasoning": "Clear, technically precise distinction between flow control and congestion control mechanisms and variables."
                }
            },
            {
                "answer": "Flow control data ke flow ko control karta hai aur congestion control network me traffic jam ko rokta hai. Sliding window me ek window aage slide hoti rehti hai jab packet deliver hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["Flow control regulates data rate to receiver", "Congestion control prevents network traffic jams", "Sliding window advances as packets are acknowledged"],
                    "missing_core_concepts": ["Specific parameters: rwnd (receiver window) vs cwnd (congestion window)", "min(rwnd, cwnd) relationship", "Slow Start / Congestion Avoidance algorithms"],
                    "deeper_concepts_to_probe": ["rwnd vs cwnd"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Intuitive understanding present but lacked formal protocol parameters and algorithms."}
                    ],
                    "citations": [{"claim": "receiver advertises its available buffer space via the Receive Window 'rwnd'... sender maintains a Congestion Window 'cwnd'", "source_number": 1}],
                    "reasoning": "Good basic intuition, but lacked technical specifics on rwnd, cwnd, and congestion avoidance phases."
                }
            },
            {
                "answer": "Flow control is used in water pipes and sliding window is a GUI feature in Windows 11 operating system.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Flow control and sliding window are core transport layer algorithms in TCP networking"],
                    "deeper_concepts_to_probe": ["TCP protocol architecture"],
                    "misconceptions": ["Confusing networking algorithms with plumbing and OS desktop interfaces"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete non-technical mockery."}
                    ],
                    "citations": [{"claim": "In TCP: Flow Control prevents the sender from overwhelming the single receiver... sender's Sliding Window advances", "source_number": 1}],
                    "reasoning": "Non-technical joke answer."
                }
            }
        ]
    },
    {
        "question_id": "CN_08",
        "subject": "CN",
        "question": "What happens at the networking level from typing https://www.google.com into a browser until the web page renders?",
        "reference": "[1] The web request lifecycle entails: 1. URL Parsing & HSTS check. 2. DNS Resolution: browser/OS cache checked, followed by recursive resolver to obtain IP. 3. TCP 3-Way Handshake: SYN, SYN-ACK, ACK establishing Layer 4 connection on port 443. 4. TLS Handshake: certificate validation, key exchange, establishing symmetric encrypted session. 5. HTTP GET Request: sent over encrypted TLS channel. 6. Server Processing & HTTP 200 Response: HTML/CSS/JS transmitted. 7. Browser Rendering: DOM & CSSOM trees constructed, layout computed, and page painted.",
        "samples": [
            {
                "answer": "1. The browser parses the URL and checks local/OS DNS cache. 2. If missed, DNS resolution queries Root, TLD, and Authoritative servers to get Google's IP address. 3. The browser initiates a TCP 3-way handshake (SYN, SYN-ACK, ACK) on port 443 with the server. 4. A TLS handshake establishes encrypted communication via certificate authentication and symmetric session key negotiation. 5. The browser sends an encrypted HTTP GET request. 6. Google's server processes the request and returns an HTTP 200 OK response with HTML payload. 7. The browser parses HTML to construct the DOM tree, fetches CSS/JS, builds the render tree, and paints the page.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["DNS resolution to translate domain to IP", "TCP 3-way handshake on port 443", "TLS handshake for encrypted session establishment", "HTTP GET request over TLS", "Server HTTP 200 response with payload", "Browser DOM/CSSOM parsing, layout, and rendering"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["HTTP/2 or HTTP/3 multiplexing over QUIC (UDP)", "CDN edge caching and reverse proxy load balancing"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Covered DNS, TCP, TLS, HTTP, and browser rendering in exact chronological sequence."}
                    ],
                    "citations": [{"claim": "DNS Resolution... TCP 3-Way Handshake... TLS Handshake... HTTP GET Request... Server Processing & HTTP 200 Response... Browser Rendering", "source_number": 1}],
                    "reasoning": "Comprehensive, chronological, and technically accurate end-to-end breakdown across all networking and application phases."
                }
            },
            {
                "answer": "Browser Google ke server ko call karta hai, DNS se IP dhoondhta hai, fir HTTP request bhejta hai aur Google web page bhej deta hai jo screen pe show ho jata hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["DNS resolution to find IP", "Sends request to server", "Server returns web page to display"],
                    "missing_core_concepts": ["TCP 3-way handshake on port 443", "TLS/SSL cryptographic handshake for HTTPS", "Browser rendering pipeline (DOM/CSSOM/paint)"],
                    "deeper_concepts_to_probe": ["TCP and TLS handshakes"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Captured general workflow but completely skipped TCP and TLS handshake layers."}
                    ],
                    "citations": [{"claim": "TCP 3-Way Handshake: SYN, SYN-ACK, ACK... TLS Handshake: certificate validation, key exchange", "source_number": 1}],
                    "reasoning": "Omitted the two most important networking phases: the TCP 3-way handshake and the TLS security handshake."
                }
            },
            {
                "answer": "The browser contacts your local electricity power plant to turn on the Wi-Fi signal directly to satellite.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["URL navigation triggers DNS resolution, TCP handshake, TLS handshake, HTTP request/response, and browser rendering"],
                    "deeper_concepts_to_probe": ["Internet protocol architecture"],
                    "misconceptions": ["Confusing web browsing with electricity power plants"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete technological absurdity."}
                    ],
                    "citations": [{"claim": "The web request lifecycle entails: 1. URL Parsing... 2. DNS Resolution... 3. TCP 3-Way Handshake", "source_number": 1}],
                    "reasoning": "Nonsensical answer with zero technical validity."
                }
            }
        ]
    }
]
