"""
Operating Systems Question Pool: 8 Questions x 3 Samples = 24 Samples.
Coverage:
OS_01: Process vs Thread
OS_02: Deadlock & 4 Coffman Conditions
OS_03: Deadlock Prevention vs Avoidance (Banker's Algorithm)
OS_04: Virtual Memory: Paging vs Segmentation
OS_05: Page Fault & LRU Page Replacement
OS_06: CPU Scheduling Algorithms (Round Robin, FCFS, SJF)
OS_07: Mutex vs Semaphore
OS_08: Critical Section & Race Conditions
"""

OS_POOL = [
    {
        "question_id": "OS_01",
        "subject": "OS",
        "question": "What is the fundamental difference between a Process and a Thread, and how does the OS handle memory for each?",
        "reference": "[1] In operating systems: A Process is an independent execution unit with its own private virtual address space (including code, data, heap, and open file descriptors), providing strong memory isolation managed via Page Tables. A Thread is a lightweight dispatch unit within a process; threads share the parent process's address space, heap, and global variables, but each maintains its own private Program Counter, CPU registers, and call stack.",
        "samples": [
            {
                "answer": "A process is an independent program in execution with its own dedicated virtual address space (code, data, heap), isolated by the OS page tables. A thread is a lightweight execution unit inside a process. Multiple threads of the same process share the heap, global memory, and open file descriptors, but each thread has its own private stack, registers, and program counter. Because threads share memory, context switching between threads is faster than between processes.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Process has isolated private virtual address space", "Threads share parent process address space, heap, and file descriptors", "Threads maintain private stack, registers, and program counter", "Thread context switching is faster due to shared memory and no MMU TLB flush"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["TLB invalidation on process context switch", "Inter-Process Communication (IPC) vs shared memory synchronization"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately delineated private vs shared memory segments."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Connected shared address space to lighter context switching overhead."}
                    ],
                    "citations": [{"claim": "Process is an independent execution unit with its own private virtual address space... Thread is a lightweight dispatch unit... share the parent process's address space", "source_number": 1}],
                    "reasoning": "Comprehensive and technically precise differentiation of memory layouts, context switching, and isolation."
                }
            },
            {
                "answer": "Process ek bada program hota hai aur thread uska chhota part hota hai. Process me alag memory hoti hai aur thread me alag memory hoti hai dono safe rehte hain.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["Process is a program in execution", "Thread is a unit within a process"],
                    "missing_core_concepts": ["Threads share address space and heap; they do NOT have isolated private memory spaces (except stack/registers)", "Process memory isolation via virtual address space"],
                    "deeper_concepts_to_probe": ["Thread stack vs process heap"],
                    "misconceptions": ["Believing threads have completely separate isolated memory like processes"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood the hierarchy but erred on memory sharing."}
                    ],
                    "citations": [{"claim": "threads share the parent process's address space, heap, and global variables", "source_number": 1}],
                    "reasoning": "Understood basic parent-child hierarchy, but incorrectly asserted that threads have separate isolated memory like processes."
                }
            },
            {
                "answer": "Processes run exclusively on Intel CPUs, while threads run exclusively on AMD CPUs.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Processes and threads are OS software abstractions, completely independent of CPU brand"],
                    "deeper_concepts_to_probe": ["OS process model"],
                    "misconceptions": ["Associating OS execution abstractions with hardware brands"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete hardware misconception."}
                    ],
                    "citations": [{"claim": "In operating systems: A Process is an independent execution unit... A Thread is a lightweight dispatch unit", "source_number": 1}],
                    "reasoning": "Absurd hardware brand attribution."
                }
            }
        ]
    },
    {
        "question_id": "OS_02",
        "subject": "OS",
        "question": "What is a Deadlock in an operating system, and what are the four necessary Coffman conditions for a deadlock to occur?",
        "reference": "[1] A Deadlock is a state where a set of processes are permanently blocked because each process holds a resource and waits for another resource held by another process in the set. The four necessary Coffman conditions are: 1. Mutual Exclusion (at least one non-shareable resource), 2. Hold and Wait (a process holding resources can request new ones), 3. No Preemption (resources cannot be forcibly confiscated), and 4. Circular Wait (a closed chain of processes exists where each waits for a resource held by the next).",
        "samples": [
            {
                "answer": "A deadlock occurs when two or more processes are blocked indefinitely, each waiting for a resource held by another process in the group. The four Coffman conditions that must all hold simultaneously are: Mutual Exclusion (resources cannot be shared concurrently), Hold and Wait (processes holding resources can request additional ones), No Preemption (resources can only be released voluntarily), and Circular Wait (a closed cycle of processes where each waits for a resource held by the next in the loop).",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Deadlock definition: mutual indefinite blocking over held resources", "Mutual Exclusion: non-shareable resources", "Hold and Wait: holding resources while requesting more", "No Preemption: resources cannot be forcibly seized", "Circular Wait: circular dependency chain between processes"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Resource Allocation Graph (RAG) cycle detection", "Breaking any single Coffman condition to prevent deadlocks"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately named and defined all four Coffman conditions."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Emphasized that all four conditions must hold simultaneously for deadlock."}
                    ],
                    "citations": [{"claim": "The four necessary Coffman conditions are: 1. Mutual Exclusion... 2. Hold and Wait... 3. No Preemption... and 4. Circular Wait", "source_number": 1}],
                    "reasoning": "Flawless, comprehensive explanation of deadlock definition and Coffman conditions."
                }
            },
            {
                "answer": "Deadlock tab hota hai jab system hang ho jata hai aur do process aapas me wait karte rehte hain. Iske conditions me Circular Wait hota hai aur Mutual Exclusion hota hai, baaki do yaad nahi aa rahe.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Deadlock is mutual indefinite waiting between processes", "Mutual Exclusion condition", "Circular Wait condition"],
                    "missing_core_concepts": ["Hold and Wait condition", "No Preemption condition", "Requirement that all four conditions must hold concurrently"],
                    "deeper_concepts_to_probe": ["Hold and wait vs no preemption"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood the core concept and named two of four Coffman conditions."}
                    ],
                    "citations": [{"claim": "Hold and Wait (a process holding resources can request new ones), 3. No Preemption (resources cannot be forcibly confiscated)", "source_number": 1}],
                    "reasoning": "Accurate definition and named two conditions, but omitted Hold and Wait and No Preemption."
                }
            },
            {
                "answer": "Deadlock means CPU is overheating and the operating system turns off power to avoid fire.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Deadlock is a concurrency resource-wait state, not thermal throttling or power shutdown"],
                    "deeper_concepts_to_probe": ["Deadlock concepts"],
                    "misconceptions": ["Confusing concurrency deadlocks with hardware overheating"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete hardware thermal confusion."}
                    ],
                    "citations": [{"claim": "A Deadlock is a state where a set of processes are permanently blocked because each process holds a resource", "source_number": 1}],
                    "reasoning": "Completely incorrect answer confusing software deadlock with thermal power shutdown."
                }
            }
        ]
    },
    {
        "question_id": "OS_03",
        "subject": "OS",
        "question": "What is the difference between Deadlock Prevention and Deadlock Avoidance, and how does Banker's Algorithm work?",
        "reference": "[1] Deadlock Prevention ensures deadlock is mathematically impossible by strictly designing the system to eliminate at least one of the four Coffman conditions (e.g., ordering resources globally to prevent circular wait). Deadlock Avoidance allows all four conditions but makes dynamic runtime decisions based on resource claims (Banker's Algorithm): before granting an allocation, it verifies whether the resulting state is 'safe' (a safe sequence exists where every process can eventually terminate).",
        "samples": [
            {
                "answer": "Deadlock Prevention statically invalidates at least one of the four Coffman conditions (for example, imposing a global numerical ordering on resources to break Circular Wait). Deadlock Avoidance dynamically inspects resource requests at runtime using advance knowledge of maximum claims. Banker's Algorithm simulates allocating the requested resources and checks if the system remains in a 'safe state'—meaning there exists a safe execution sequence where every process can acquire its max needs, finish, and return resources. If unsafe, the request is delayed.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Prevention statically invalidates at least one Coffman condition", "Avoidance makes dynamic runtime decisions based on maximum resource claims", "Banker's Algorithm checks for a 'safe state' / safe sequence before granting allocation", "If allocating leads to an unsafe state, the process is made to wait"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Difference between an unsafe state and an actual deadlock", "Banker's Algorithm time complexity and impracticality in general OS"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clear static vs dynamic distinction between prevention and avoidance."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Explained the safe sequence simulation mechanism of Banker's Algorithm."}
                    ],
                    "citations": [{"claim": "Deadlock Prevention ensures deadlock is mathematically impossible by... eliminating at least one of the four Coffman conditions... Deadlock Avoidance... Banker's Algorithm... verifies whether the resulting state is 'safe'", "source_number": 1}],
                    "reasoning": "Clear, precise explanation distinguishing static constraint imposition from dynamic safe-state evaluation."
                }
            },
            {
                "answer": "Prevention me hum pehle hi resource check karte hain taaki deadlock na ho. Avoidance me Banker's algorithm use hota hai jo bank jaisa loan deta hai processes ko. Dono deadlock rokne ke tareeqe hain.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["Both are deadlock mitigation strategies", "Banker's algorithm is used in avoidance"],
                    "missing_core_concepts": ["Prevention breaks one of the four Coffman conditions statically", "Avoidance uses safe state / safe sequence simulation dynamically", "Distinction between static design rules and dynamic runtime checks"],
                    "deeper_concepts_to_probe": ["Coffman condition breaking in prevention"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Vague intuition about bank loans without formal safe-state definition."}
                    ],
                    "citations": [{"claim": "Deadlock Prevention... eliminate at least one of the four Coffman conditions... Deadlock Avoidance... verifies whether the resulting state is 'safe'", "source_number": 1}],
                    "reasoning": "High-level intuition present, but lacked rigorous technical definitions of Coffman invalidation and safe sequences."
                }
            },
            {
                "answer": "Banker's algorithm is a cryptographic payment gateway used by financial banks to encrypt credit card transactions.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Banker's algorithm is an OS resource allocation and deadlock avoidance algorithm"],
                    "deeper_concepts_to_probe": ["Operating system resource scheduling"],
                    "misconceptions": ["Taking the name 'Banker' literally to mean banking cryptography"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Literal name misinterpretation."}
                    ],
                    "citations": [{"claim": "Banker's Algorithm: before granting an allocation, it verifies whether the resulting state is 'safe'", "source_number": 1}],
                    "reasoning": "Literal guessing based on the word 'Banker'."
                }
            }
        ]
    },
    {
        "question_id": "OS_04",
        "subject": "OS",
        "question": "What is Virtual Memory, and how does Paging differ from Segmentation in memory management?",
        "reference": "[1] Virtual Memory creates an illusion of large contiguous memory for each process by mapping virtual addresses to physical RAM or secondary storage via the MMU. Paging divides memory into fixed-size blocks (virtual pages mapped to physical page frames); it is transparent to programmer and causes internal fragmentation, not external. Segmentation divides memory into variable-sized logical units reflecting program structure (code, stack, heap, functions); it is visible to programmer and causes external fragmentation.",
        "samples": [
            {
                "answer": "Virtual memory abstracts physical RAM, giving each process the illusion of a large contiguous address space using the MMU and disk backing. Paging divides virtual memory into fixed-size blocks called pages, mapped to physical frames; it eliminates external fragmentation but suffers from internal fragmentation. Segmentation divides memory into variable-sized logical segments based on program components (code, stack, heap, modules); it is user-visible and eliminates internal fragmentation, but causes external fragmentation.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Virtual memory abstracts physical RAM via MMU mapping", "Paging uses fixed-size pages and frames", "Paging causes internal fragmentation (no external fragmentation)", "Segmentation uses variable-sized logical sections (code, heap, stack)", "Segmentation causes external fragmentation"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Translation Lookaside Buffer (TLB)", "Segmented Paging architectures (e.g. x86)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted fixed vs variable sizes and internal vs external fragmentation."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Connected segmentation to logical program structure."}
                    ],
                    "citations": [{"claim": "Paging divides memory into fixed-size blocks... causes internal fragmentation... Segmentation divides memory into variable-sized logical units... causes external fragmentation", "source_number": 1}],
                    "reasoning": "Clear, precise explanation of memory abstractions and the fragmentation trade-offs of paging vs segmentation."
                }
            },
            {
                "answer": "Virtual memory hard disk ko RAM ki tarah use karti hai. Paging me data pages me divide hota hai aur segmentation me data segments me hota hai. Paging modern OS me use hoti hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Virtual memory uses disk storage as backing store for RAM", "Paging uses pages and segmentation uses segments", "Paging is dominant in modern OS"],
                    "missing_core_concepts": ["Fixed-size pages vs variable-sized logical segments", "Internal fragmentation in paging vs external fragmentation in segmentation", "MMU address translation"],
                    "deeper_concepts_to_probe": ["Fragmentation differences"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Gave basic high-level summary but lacked technical differences in sizes and fragmentation."}
                    ],
                    "citations": [{"claim": "Paging divides memory into fixed-size blocks... Segmentation divides memory into variable-sized logical units", "source_number": 1}],
                    "reasoning": "High-level understanding present, but lacked depth regarding block sizes and fragmentation types."
                }
            },
            {
                "answer": "Virtual memory is a GPU graphics feature for running 4K monitors, and paging is sending SMS messages between CPUs.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Virtual memory and paging are OS memory management abstractions"],
                    "deeper_concepts_to_probe": ["Memory hierarchy"],
                    "misconceptions": ["Associating virtual memory with GPU displays and paging with telecommunication"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total disconnect from computer architecture."}
                    ],
                    "citations": [{"claim": "Virtual Memory creates an illusion of large contiguous memory for each process by mapping virtual addresses to physical RAM", "source_number": 1}],
                    "reasoning": "Nonsensical definition with no connection to operating system memory management."
                }
            }
        ]
    },
    {
        "question_id": "OS_05",
        "subject": "OS",
        "question": "What is a Page Fault in an operating system, and how does the Least Recently Used (LRU) page replacement algorithm handle it?",
        "reference": "[1] A Page Fault is a hardware trap raised by the Memory Management Unit (MMU) when a process accesses a virtual memory page marked not-present in physical RAM (valid bit = 0). The OS traps to kernel mode, selects a physical frame (invoking a page replacement algorithm like LRU if RAM is full), loads the required page from swap disk into RAM, updates page table, and restarts the instruction. LRU replaces the page that has not been accessed for the longest period of time.",
        "samples": [
            {
                "answer": "A page fault is an MMU hardware trap triggered when a process references a virtual page not currently present in physical RAM (valid bit is 0 in the page table). The OS kernel catches the trap, reads the page from swap space on disk into a free physical frame, updates the page table, and resumes the instruction. If RAM is full, the Least Recently Used (LRU) algorithm identifies and evicts the page that has remained unreferenced for the longest duration of past time.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Page fault is a trap raised by MMU when page is not present in RAM", "OS fetches missing page from swap/secondary storage", "Page table is updated and faulting instruction is restarted", "LRU evicts the page that has not been accessed for the longest time"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Belady's Anomaly (why LRU is immune as a stack algorithm)", "Approximating LRU using the Clock / Second-Chance algorithm"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately described the page fault trap and swap fetch sequence."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Defined the LRU replacement heuristic clearly."}
                    ],
                    "citations": [{"claim": "Page Fault is a hardware trap raised by the Memory Management Unit (MMU) when a process accesses a virtual memory page marked not-present... LRU replaces the page that has not been accessed for the longest period", "source_number": 1}],
                    "reasoning": "Accurate, step-by-step technical explanation of page fault handling and LRU eviction."
                }
            },
            {
                "answer": "Page fault tab hota hai jab required page RAM me nahi milta. OS disk se page load karta hai. LRU sabse purane page ko nikal deta hai jo sabse pehle aaya tha.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Page fault occurs when required page is missing from RAM", "OS retrieves missing page from disk"],
                    "missing_core_concepts": ["LRU replaces the page not used for the longest time, NOT the page that arrived first (confused with FIFO)", "Trap to OS and instruction restart"],
                    "deeper_concepts_to_probe": ["FIFO vs LRU replacement algorithms"],
                    "misconceptions": ["Describing FIFO ('jo sabse pehle aaya tha') while calling it LRU"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Defined page fault accurately, but defined FIFO replacement instead of LRU."}
                    ],
                    "citations": [{"claim": "LRU replaces the page that has not been accessed for the longest period of time", "source_number": 1}],
                    "reasoning": "Correctly explained page fault, but described FIFO replacement instead of Least Recently Used."
                }
            },
            {
                "answer": "Page fault tab hota hai jab website open nahi hoti aur 404 error aata hai. LRU purani files ko delete karke nayi files download karta hai.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Page fault is an OS memory management trap, not an HTTP web error", "LRU is an OS page eviction algorithm swapping pages between RAM and disk"],
                    "deeper_concepts_to_probe": ["Virtual memory paging"],
                    "misconceptions": ["Confusing OS virtual memory page fault with HTTP 404 web error"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Confused operating system virtual memory with web browsing."}
                    ],
                    "citations": [{"claim": "A Page Fault is a hardware trap raised by the Memory Management Unit (MMU)", "source_number": 1}],
                    "reasoning": "Complete confusion between OS memory page faults and web browser 404 errors."
                }
            }
        ]
    },
    {
        "question_id": "OS_06",
        "subject": "OS",
        "question": "What is the difference between Preemptive and Non-Preemptive CPU Scheduling, and how does Round Robin scheduling function?",
        "reference": "[1] In CPU scheduling: Non-Preemptive scheduling allows a process to retain the CPU until it voluntarily terminates or yields for I/O (e.g., standard FCFS, SJF). Preemptive scheduling allows the OS kernel to forcibly interrupt a running process via timer interrupts and move it back to the ready queue (e.g., Round Robin, SRTF). Round Robin allocates each process a fixed time slice (quantum); when the quantum expires, the process is preempted and placed at the tail of the ready queue.",
        "samples": [
            {
                "answer": "Non-preemptive scheduling means once a process gets the CPU, it holds it until it finishes or waits for I/O (like FCFS). Preemptive scheduling allows the OS timer interrupt to forcibly take the CPU away from a running process and return it to the ready queue. Round Robin is a preemptive scheduling algorithm that assigns each ready process a fixed time quantum; if the process does not finish within that quantum, the OS preempts it and appends it to the end of the ready queue, ensuring fair CPU distribution.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Non-preemptive retains CPU until completion or I/O block", "Preemptive allows OS timer interrupts to interrupt running processes", "Round Robin assigns a fixed time quantum", "Preempted processes are placed at the tail of the ready queue for fairness"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Impact of quantum size: too large approaches FCFS, too small causes excessive context switch overhead"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately distinguished preemption criteria."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Explained Round Robin time quantum mechanics and queue rotation."}
                    ],
                    "citations": [{"claim": "Non-Preemptive scheduling allows a process to retain the CPU... Preemptive scheduling allows the OS kernel to forcibly interrupt... Round Robin allocates each process a fixed time slice (quantum)", "source_number": 1}],
                    "reasoning": "Clear, precise explanation of scheduling preemption and Round Robin mechanics."
                }
            },
            {
                "answer": "Preemptive me process ko beech me rok sakte hain aur non-preemptive me nahi rok sakte. Round Robin me processes round-circle me ghumte hain jab tak CPU unko baari baari execute nahi kar leta.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["Preemptive allows interrupting processes mid-execution", "Non-preemptive does not allow interruption", "Round Robin executes processes turn by turn"],
                    "missing_core_concepts": ["Specific concept of time quantum / time slice in Round Robin", "Timer interrupts and ready queue tail insertion"],
                    "deeper_concepts_to_probe": ["Time quantum tuning"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood the high-level concept but missed the core concept of time quantum."}
                    ],
                    "citations": [{"claim": "Round Robin allocates each process a fixed time slice (quantum); when the quantum expires, the process is preempted", "source_number": 1}],
                    "reasoning": "Basic preemption distinction is correct, but omitted the critical concept of time quantum in Round Robin."
                }
            },
            {
                "answer": "Non-preemptive means CPU only runs during daytime, and preemptive means it works 24/7 overnight.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Preemption refers to OS process interruption mechanisms, not operating hours"],
                    "deeper_concepts_to_probe": ["CPU scheduling"],
                    "misconceptions": ["Confusing preemption with operating schedule"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total misconception."}
                    ],
                    "citations": [{"claim": "In CPU scheduling: Non-Preemptive scheduling... Preemptive scheduling allows the OS kernel to forcibly interrupt", "source_number": 1}],
                    "reasoning": "Non-technical guess with no validity."
                }
            }
        ]
    },
    {
        "question_id": "OS_07",
        "subject": "OS",
        "question": "What is the difference between a Mutex and a Semaphore in inter-process synchronization?",
        "reference": "[1] In synchronization: A Mutex (Mutual Exclusion object) is a locking mechanism with ownership semantics; only the specific thread that acquired/locked the mutex can release/unlock it (binary state: locked/unlocked). A Semaphore is a signaling mechanism without ownership; any thread can signal/release a semaphore. A Counting Semaphore maintains an integer counter allowing up to N concurrent threads access to a finite pool of resources.",
        "samples": [
            {
                "answer": "A Mutex is a mutual exclusion locking mechanism with ownership semantics—only the thread that locked the mutex is allowed to unlock it, enforcing strict single-thread access to a critical section. A Semaphore is a signaling mechanism without ownership, where any thread can signal/post to unblock a waiting thread. Furthermore, a counting semaphore maintains an integer count, allowing a specified number of concurrent threads (N) to access a shared resource pool.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Mutex has ownership semantics (only owner can unlock)", "Semaphore is a signaling mechanism without ownership", "Counting semaphore allows up to N concurrent threads to access shared resources", "Mutex is strictly binary for critical section mutual exclusion"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Priority Inversion and Priority Inheritance protocols with Mutexes", "Binary semaphore vs Mutex differences"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted locking/ownership with signaling mechanisms."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained counting semaphore counter allowing N threads."}
                    ],
                    "citations": [{"claim": "A Mutex... is a locking mechanism with ownership semantics; only the specific thread that acquired/locked the mutex can release/unlock it... Semaphore is a signaling mechanism without ownership", "source_number": 1}],
                    "reasoning": "Clear, accurate, and highlights the crucial architectural distinction of thread ownership."
                }
            },
            {
                "answer": "Mutex ek lock hota hai jo ek time pe ek hi thread ko allow karta hai. Semaphore ek counter hota hai jo multiple threads ko allow kar sakta hai. Dono me bas counter ka farq hota hai, baki sab same hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Mutex allows only one thread at a time", "Counting semaphore allows multiple threads via a counter"],
                    "missing_core_concepts": ["Ownership semantics: Mutex must be unlocked by the locking thread, whereas Semaphore is an ownership-less signaling mechanism"],
                    "deeper_concepts_to_probe": ["Thread ownership in mutexes"],
                    "misconceptions": ["Believing a mutex is simply a binary semaphore without ownership semantics"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood the thread count difference but missed the fundamental ownership difference."}
                    ],
                    "citations": [{"claim": "A Mutex... is a locking mechanism with ownership semantics; only the specific thread that acquired/locked the mutex can release/unlock it", "source_number": 1}],
                    "reasoning": "Understood capacity difference, but missed the essential ownership/signaling distinction."
                }
            },
            {
                "answer": "Mutex is used in frontend React apps, and Semaphore is a hardware chip on the motherboard.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Both Mutex and Semaphore are OS/concurrency synchronization primitives"],
                    "deeper_concepts_to_probe": ["Concurrency primitives"],
                    "misconceptions": ["Believing semaphore is a physical motherboard chip"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Completely disconnected from synchronization."}
                    ],
                    "citations": [{"claim": "In synchronization: A Mutex... is a locking mechanism... A Semaphore is a signaling mechanism", "source_number": 1}],
                    "reasoning": "Fabricated association having nothing to do with concurrent synchronization."
                }
            }
        ]
    },
    {
        "question_id": "OS_08",
        "subject": "OS",
        "question": "What is the Critical Section problem in operating systems, and how do Race Conditions occur?",
        "reference": "[1] The Critical Section is a segment of code where multiple concurrent threads/processes access shared resources (such as global memory or files). A Race Condition occurs when the outcome of concurrent execution depends unpredictably on the non-deterministic interleaving or timing of thread execution. A valid solution to the critical section problem must satisfy three requirements: Mutual Exclusion, Progress, and Bounded Waiting.",
        "samples": [
            {
                "answer": "A critical section is a piece of code that accesses shared mutable resources (like shared memory, global variables, or files). A race condition occurs when multiple threads concurrently read and write to this shared data, causing the final output to depend on the non-deterministic scheduling order of thread execution. To properly solve the critical section problem, any synchronization algorithm must satisfy three mandatory criteria: Mutual Exclusion (only one thread in critical section), Progress (threads not in critical section don't block others), and Bounded Waiting (no thread starves indefinitely).",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Critical section is code accessing shared mutable resources", "Race condition occurs when output depends on arbitrary thread scheduling timing", "Three requirements for valid solution: Mutual Exclusion, Progress, and Bounded Waiting"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Peterson's Algorithm", "Hardware atomic instructions like Test-and-Set and Compare-And-Swap (CAS)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately defined critical section and race conditions."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Listed the three formal criteria for critical section solutions."}
                    ],
                    "citations": [{"claim": "Critical Section is a segment of code where multiple concurrent threads/processes access shared resources... Race Condition occurs when the outcome... depends unpredictably on... timing... Mutual Exclusion, Progress, and Bounded Waiting", "source_number": 1}],
                    "reasoning": "Clear, comprehensive explanation of critical section, race condition, and the three formal solution requirements."
                }
            },
            {
                "answer": "Critical section matlab wo code jahan shared variable update hota hai. Race condition tab aati hai jab do threads ek hi variable ko update karne ki race lagate hain aur galat value save ho jati hai. Isko lock lagake fix karte hain.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 7,
                    "depth_score": 5,
                    "correct_points": ["Critical section is where shared variables are updated", "Race condition happens when concurrent threads interleave updates causing corrupted values", "Locking is a solution"],
                    "missing_core_concepts": ["Formal three requirements: Mutual Exclusion, Progress, Bounded Waiting"],
                    "deeper_concepts_to_probe": ["Bounded waiting and starvation"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Understood the practical programming issue and race condition mechanics."},
                        {"evidence_type": "REASONING", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Did not cite the theoretical solution criteria (Progress, Bounded Waiting)."}
                    ],
                    "citations": [{"claim": "A valid solution to the critical section problem must satisfy three requirements: Mutual Exclusion, Progress, and Bounded Waiting", "source_number": 1}],
                    "reasoning": "Good practical understanding of race conditions, but missed the formal three criteria (Mutual Exclusion, Progress, Bounded Waiting)."
                }
            },
            {
                "answer": "Critical section is an emergency error screen when Windows crashes, and race condition is when RAM speed is faster than CPU speed.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Critical section and race conditions are multi-threaded concurrency synchronization concepts"],
                    "deeper_concepts_to_probe": ["Concurrency fundamentals"],
                    "misconceptions": ["Confusing critical section with blue screen crash and race conditions with clock frequencies"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total confusion with crash screens and hardware bus speeds."}
                    ],
                    "citations": [{"claim": "Critical Section is a segment of code where multiple concurrent threads/processes access shared resources", "source_number": 1}],
                    "reasoning": "Complete failure to understand concurrency synchronization."
                }
            }
        ]
    }
]
