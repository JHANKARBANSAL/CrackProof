"""
Data Structures & Algorithms Question Pool: 8 Questions x 3 Samples = 24 Samples.
Coverage:
DSA_01: Floyd's Cycle Detection in Singly Linked List
DSA_02: Queue Implementation using Two Stacks
DSA_03: Binary Search on Singly Linked List
DSA_04: Array vs Linked List: Memory Layout & Cache Locality
DSA_05: HashMap Internal Mechanics & Collision Handling
DSA_06: Stack vs Heap Memory Allocation
DSA_07: BFS vs DFS Graph Traversals
DSA_08: Balanced BST vs Hash Table Trade-offs
"""

DSA_POOL = [
    {
        "question_id": "DSA_01",
        "subject": "DSA",
        "question": "Given a singly linked list, how do you determine if it contains a cycle, and what is the optimal time and space complexity?",
        "reference": "[1] Floyd's Cycle-Finding Algorithm (Tortoise and Hare) uses two pointers moving at different speeds: slow moves 1 node per step, fast moves 2 nodes per step. If a cycle exists, fast will eventually lap slow and they will collide at the same node. If fast reaches NULL, no cycle exists. Time complexity is O(n) and auxiliary space complexity is O(1).",
        "samples": [
            {
                "answer": "We use Floyd's Tortoise and Hare algorithm with two pointers initialized at the head. The slow pointer moves one step at a time while the fast pointer moves two steps. If there is a cycle, the fast pointer will catch up and meet the slow pointer inside the loop. If the fast pointer reaches null, there is no cycle. This achieves optimal O(n) time complexity and O(1) auxiliary space complexity.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Uses Floyd's two-pointer algorithm (slow and fast)", "Slow advances 1 step, fast advances 2 steps", "Meeting indicates a cycle; fast reaching null indicates no cycle", "Time complexity is O(n)", "Space complexity is O(1) auxiliary space"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Finding the entry point of the cycle (resetting one pointer to head and moving both at 1 step)", "Calculating cycle length"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately detailed slow and fast pointer increments."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Provided the optimal O(n) time and O(1) space bounds."}
                    ],
                    "citations": [{"claim": "Floyd's Cycle-Finding Algorithm (Tortoise and Hare) uses two pointers... slow moves 1 node... fast moves 2 nodes... Time complexity is O(n) and auxiliary space complexity is O(1)", "source_number": 1}],
                    "reasoning": "Flawless technical recall of Floyd's cycle detection algorithm with exact optimal complexity bounds."
                }
            },
            {
                "answer": "Aap ek HashSet banao aur traverse karte waqt har node ka reference set me daalte jao. Agar node pehle se set me mil jaye to cycle hai. Isme time O(n) lagta hai aur space O(n) lagti hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 7,
                    "depth_score": 6,
                    "correct_points": ["Valid working approach using a HashSet of visited nodes", "Correctly identified O(n) time and O(n) space for the hash set solution"],
                    "missing_core_concepts": ["Optimal O(1) space solution using Floyd's Tortoise and Hare algorithm"],
                    "deeper_concepts_to_probe": ["How to optimize space from O(n) down to O(1)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Proposed a correct hashing approach with accurate O(n) space complexity."},
                        {"evidence_type": "APPLICATION", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Failed to provide the optimal O(1) space two-pointer approach asked in the question."}
                    ],
                    "citations": [{"claim": "Floyd's Cycle-Finding Algorithm... auxiliary space complexity is O(1)", "source_number": 1}],
                    "reasoning": "The HashSet approach is correct and works in O(n) time, but the question asked for optimal space complexity which is O(1) via Floyd's algorithm."
                }
            },
            {
                "answer": "Count the number of nodes in the list using a while loop; if the count is greater than 10,000, then it is a cycle.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["A cycle creates an infinite loop that will hang the program and never terminate", "Must use Floyd's two-pointer algorithm or visited tracking"],
                    "deeper_concepts_to_probe": ["Cycle detection in linked structures"],
                    "misconceptions": ["Believing an arbitrary counter threshold detects cycles (infinite loops never break naturally)"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Flawed naive counting approach that hangs infinitely on cycles."}
                    ],
                    "citations": [{"claim": "If a cycle exists, fast will eventually lap slow and they will collide at the same node", "source_number": 1}],
                    "reasoning": "Naively counting nodes in a cyclic list results in an infinite loop that never terminates."
                }
            }
        ]
    },
    {
        "question_id": "DSA_02",
        "subject": "DSA",
        "question": "How do you implement a Queue using two Stacks, and what is the amortized time complexity of the operations?",
        "reference": "[1] A Queue (FIFO) can be implemented using two Stacks (LIFO): stack_in for enqueuing and stack_out for dequeuing. Enqueue pushes directly to stack_in (O(1)). Dequeue pops from stack_out; if stack_out is empty, all elements from stack_in are popped and pushed to stack_out (reversing their order to FIFO). Because each element is pushed and popped across the stacks exactly twice over its lifetime, the amortized time complexity per operation is O(1).",
        "samples": [
            {
                "answer": "We use two stacks: stack_in and stack_out. For enqueue, we simply push the element onto stack_in in O(1) time. For dequeue, if stack_out is not empty, we pop from it. If stack_out is empty, we transfer all elements from stack_in to stack_out (which reverses them into FIFO order) and then pop. While an individual transfer takes O(n) in the worst case, each element is moved at most once from in to out, yielding an amortized time complexity of O(1) per operation.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Uses two stacks: stack_in for enqueue and stack_out for dequeue", "Enqueue pushes to stack_in in O(1)", "Dequeue pops from stack_out, transferring from in to out only when out is empty", "Transfer reverses LIFO order to FIFO order", "Amortized time complexity is O(1) per operation"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Accounting/Potential method for formal amortized proof", "Thread-safe implementation with dual locks"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately explained the dual-stack enqueue/dequeue transfer logic."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Clearly articulated amortized O(1) analysis based on element lifetime moves."}
                    ],
                    "citations": [{"claim": "stack_in for enqueuing and stack_out for dequeuing... each element is pushed and popped... amortized time complexity per operation is O(1)", "source_number": 1}],
                    "reasoning": "Clear, accurate, and provides both the operational mechanics and the amortized analysis."
                }
            },
            {
                "answer": "Hum do stacks use karenge. Har baar jab naya element enqueue karna ho to pehle stack 1 se saare elements stack 2 me daalo, naya element stack 1 me dalo, fir stack 2 se wapas stack 1 me dalo. Isse enqueue O(n) ho jata hai aur dequeue O(1) ho jata hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 7,
                    "depth_score": 6,
                    "correct_points": ["Valid alternative implementation (making enqueue costly)", "Correctly analyzed O(n) enqueue and O(1) dequeue for this specific approach"],
                    "missing_core_concepts": ["Optimal lazy transfer approach achieving amortized O(1) for both enqueue and dequeue"],
                    "deeper_concepts_to_probe": ["Lazy evaluation for amortized O(1) dequeue"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Proposed a valid working queue using two stacks."},
                        {"evidence_type": "APPLICATION", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Eager transfer on every enqueue is less optimal than lazy amortized O(1) transfer."}
                    ],
                    "citations": [{"claim": "Because each element is pushed and popped across the stacks exactly twice over its lifetime, the amortized time complexity per operation is O(1)", "source_number": 1}],
                    "reasoning": "Proposed the eager-enqueue approach which works, but is less optimal than the lazy amortized O(1) dual-stack approach."
                }
            },
            {
                "answer": "It is impossible to implement a queue using stacks because stacks are LIFO and queues are FIFO, and their mathematical properties cancel each other out.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Two successive LIFO reversals produce a FIFO ordering, making queue implementation entirely possible"],
                    "deeper_concepts_to_probe": ["Stack and queue fundamentals"],
                    "misconceptions": ["Believing LIFO structures cannot simulate FIFO order through double reversal"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Failed to recognize that double reversal inverts LIFO into FIFO."}
                    ],
                    "citations": [{"claim": "A Queue (FIFO) can be implemented using two Stacks (LIFO)", "source_number": 1}],
                    "reasoning": "Demonstrates a fundamental failure to grasp that reversing a stack twice yields FIFO ordering."
                }
            }
        ]
    },
    {
        "question_id": "DSA_03",
        "subject": "DSA",
        "question": "Can you run Binary Search on a singly linked list in O(log n) time?",
        "reference": "[1] In computational complexity: Binary Search requires random access O(1) to locate the median element in constant time. In a singly linked list, accessing the middle element requires sequential traversal O(n). Therefore, running binary search on a singly linked list results in recurrence T(n) = T(n/2) + O(n), degrading total search time to O(n).",
        "samples": [
            {
                "answer": "No, you cannot achieve O(log n) time. Binary search requires O(1) random access to find the median element immediately. In a singly linked list, locating the middle element requires O(n) sequential traversal. Finding the middle at each step degrades the total time complexity recurrence to T(n) = T(n/2) + O(n), which resolves to O(n) total time.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Cannot run in O(log n) time", "Binary search requires O(1) random access", "Finding middle element in linked list takes O(n) sequential traversal", "Total time degrades to O(n)"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Skip Lists or Balanced BSTs for O(log n) search with pointers"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Identified random access requirement."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Derived recurrence degradation to O(n) due to linear traversal."}
                    ],
                    "citations": [{"claim": "Binary search requires random access O(1) to locate the median element... degrading total search time to O(n)", "source_number": 1}],
                    "reasoning": "Clear, precise understanding of data structure access characteristics vs algorithmic prerequisites."
                }
            },
            {
                "answer": "Nahi, binary search linked list me O(log n) me nahi chal sakta kyunki index access direct nahi hota. Par agar hum pehle list ka size nikal lein to binary search chal sakta hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["Correctly stated that binary search cannot achieve O(log n)", "Identified lack of direct index access in linked lists"],
                    "missing_core_concepts": ["Even knowing the size, traversing to index n/2 takes O(n) steps, degrading the recurrence to O(n) overall"],
                    "deeper_concepts_to_probe": ["Recurrence relation T(n) = T(n/2) + O(n)"],
                    "misconceptions": ["Implying that knowing the list size somehow solves the linear traversal bottleneck"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Correct answer on impossibility of O(log n), but fuzzy on traversal overhead."}
                    ],
                    "citations": [{"claim": "In a singly linked list, accessing the middle element requires sequential traversal O(n)", "source_number": 1}],
                    "reasoning": "Answered correctly that O(log n) is impossible, but suggested that knowing the size resolves the issue, missing the O(n) pointer walk constraint."
                }
            },
            {
                "answer": "Yes, because if the linked list elements are sorted, binary search always runs in O(log n) regardless of data structure.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": ["Understands binary search requires sorted input"],
                    "missing_core_concepts": ["Singly linked lists lack constant time index access", "Finding middle takes O(n) traversal degrading overall complexity to O(n)"],
                    "deeper_concepts_to_probe": ["Sequential vs random memory access"],
                    "misconceptions": ["Believing binary search is O(log n) on any sorted data structure regardless of memory layout"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Ignored data structure pointer traversal constraints."}
                    ],
                    "citations": [{"claim": "Binary Search requires random access O(1) to locate the median element in constant time", "source_number": 1}],
                    "reasoning": "Fundamental misconception regarding data structure memory access and algorithmic prerequisites."
                }
            }
        ]
    },
    {
        "question_id": "DSA_04",
        "subject": "DSA",
        "question": "What are the fundamental memory layout and CPU cache locality differences between an Array and a Singly Linked List?",
        "reference": "[1] Arrays allocate memory contiguously in physical RAM, providing O(1) random access via base + index * size address calculation and exploiting CPU spatial locality (when an element is read, the CPU hardware prefetcher loads the adjacent cache line into L1/L2 cache, resulting in fast cache hits). Singly Linked Lists allocate discrete nodes non-contiguously on the heap connected by pointers, requiring O(n) sequential traversal and causing frequent CPU cache misses due to scattered memory locations.",
        "samples": [
            {
                "answer": "Arrays store elements in contiguous physical memory, enabling O(1) random access via arithmetic indexing. Crucially, contiguous layout takes full advantage of CPU spatial cache locality: loading one array element pulls the entire 64-byte cache line into L1/L2 cache, making sequential iterations extremely fast. In contrast, singly linked lists allocate nodes non-contiguously on the heap linked by pointers. This causes frequent CPU cache misses because the CPU prefetcher cannot predict scattered heap addresses, resulting in memory latency penalties.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Arrays are stored in contiguous memory; linked lists are scattered on heap", "Arrays have O(1) indexing; linked lists have O(n) sequential traversal", "Arrays maximize CPU spatial locality by prefetching adjacent elements into cache lines", "Linked lists suffer from cache misses and pointer storage overhead"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Cache line size (typically 64 bytes)", "Pointer overhead on 64-bit systems (8 bytes per pointer)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Contrasted contiguous memory indexing with heap pointer traversal."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained CPU cache lines and spatial locality prefetching advantages."}
                    ],
                    "citations": [{"claim": "Arrays allocate memory contiguously... exploiting CPU spatial locality... Singly Linked Lists allocate discrete nodes non-contiguously on the heap... causing frequent CPU cache misses", "source_number": 1}],
                    "reasoning": "Thorough, technically deep explanation connecting memory layout directly to CPU hardware cache architecture."
                }
            },
            {
                "answer": "Array me size fixed hota hai aur contiguous memory hoti hai. Linked list me dynamic size hota hai aur nodes pointers se jude hote hain. Array fast hota hai aur linked list me insertion easy hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["Array uses contiguous memory", "Linked list uses dynamic nodes connected by pointers", "Array is faster for lookups"],
                    "missing_core_concepts": ["CPU cache lines and spatial locality", "Why contiguous memory results in cache hits while pointer chasing results in cache misses"],
                    "deeper_concepts_to_probe": ["CPU cache locality"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Covered textbook definition but omitted the core CPU cache locality asked in the question."}
                    ],
                    "citations": [{"claim": "exploiting CPU spatial locality (when an element is read, the CPU hardware prefetcher loads the adjacent cache line into L1/L2 cache)", "source_number": 1}],
                    "reasoning": "Recalled textbook array vs linked list characteristics, but completely missed the CPU hardware cache locality aspect."
                }
            },
            {
                "answer": "Linked lists are always cached in CPU L1 cache because pointers are very small, while arrays are stored on hard disk because they are too large.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Both arrays and linked lists reside in RAM", "Arrays enjoy cache locality due to contiguous memory, whereas linked lists suffer cache misses"],
                    "deeper_concepts_to_probe": ["Memory hierarchy and hardware caching"],
                    "misconceptions": ["Believing arrays live on hard disks and linked lists live in L1 cache"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete inversion of computer architecture principles."}
                    ],
                    "citations": [{"claim": "Arrays allocate memory contiguously in physical RAM... Singly Linked Lists allocate discrete nodes non-contiguously on the heap", "source_number": 1}],
                    "reasoning": "Blatantly incorrect assertions regarding hardware caching and storage locations."
                }
            }
        ]
    },
    {
        "question_id": "DSA_05",
        "subject": "DSA",
        "question": "How does a HashMap work internally, how are hash collisions resolved, and what is the significance of the load factor?",
        "reference": "[1] A HashMap implements an associative array using an underlying array of buckets. When a key-value pair is inserted, hash(key) calculates a hash code, which is mapped to an array bucket index via (n - 1) & hash. Collisions (different keys mapping to same bucket) are resolved via Separate Chaining (linked lists or balanced trees) or Open Addressing (probing). The Load Factor (default 0.75) is the threshold ratio (size / capacity); when exceeded, the map dynamically resizes (doubles capacity) and rehashes all entries to maintain average O(1) lookup time.",
        "samples": [
            {
                "answer": "A HashMap uses an internal bucket array. It computes hash(key) and maps it to a bucket index using modulo or bitwise masking (hash & (n-1)). When multiple keys produce the same bucket index (a hash collision), it uses Separate Chaining, storing entries in a linked list or converting to a Red-Black Tree when a bucket exceeds 8 entries (like in Java 8). The load factor (default 0.75) represents the threshold of fullness; when the number of entries exceeds load_factor * capacity, the array doubles its capacity and rehashes all entries to preserve O(1) average lookup performance.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Uses internal array of buckets with bitwise index calculation (hash & (n-1))", "Collisions resolved via separate chaining (linked list / treeification)", "Load factor (default 0.75) defines the resize threshold (capacity * load_factor)", "Rehashing doubles bucket capacity to maintain O(1) amortized lookup"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Worst case O(n) degradation under malicious hash attacks", "Treeify threshold (8) and untreeify threshold (6) in Java"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately detailed hash-to-bucket mapping and collision chaining."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained how load factor triggers capacity doubling and rehashing."}
                    ],
                    "citations": [{"claim": "hash(key) calculates a hash code, which is mapped to an array bucket index... Collisions... resolved via Separate Chaining... Load Factor... threshold ratio... doubles capacity", "source_number": 1}],
                    "reasoning": "Clear, technically thorough explanation covering bucket indexing, separate chaining collision resolution, and load factor resizing."
                }
            },
            {
                "answer": "HashMap me key ka hash nikalte hain aur array index pe value store karte hain. Collision hone pe linked list me daal dete hain. Load factor matlab table kitna bhara hua hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Computes hash from key to get array index", "Resolves collisions using linked list chaining", "Load factor measures fullness of table"],
                    "missing_core_concepts": ["Load factor threshold triggering rehashing and doubling array capacity", "Treeification under heavy collisions (Red-Black tree)"],
                    "deeper_concepts_to_probe": ["Rehashing process"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Got the basics of hashing and chaining, but omitted resizing mechanics."}
                    ],
                    "citations": [{"claim": "The Load Factor (default 0.75) is the threshold ratio (size / capacity); when exceeded, the map dynamically resizes (doubles capacity) and rehashes", "source_number": 1}],
                    "reasoning": "Accurate on hashing and basic chaining, but did not explain how load factor triggers resizing and rehashing."
                }
            },
            {
                "answer": "HashMap sorts all keys alphabetically in an array, and if two keys start with the same letter it creates a collision error and throws an exception.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["HashMaps are unordered associative structures using hash codes, not alphabetical sorting", "Collisions are normal and handled via chaining, not exception errors"],
                    "deeper_concepts_to_probe": ["Hash functions and collision handling"],
                    "misconceptions": ["Believing HashMap sorts keys alphabetically", "Believing collisions throw exceptions"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Gross misunderstanding of hashing."}
                    ],
                    "citations": [{"claim": "HashMap implements an associative array... hash(key) calculates a hash code", "source_number": 1}],
                    "reasoning": "Complete failure to understand hash table data structures."
                }
            }
        ]
    },
    {
        "question_id": "DSA_06",
        "subject": "DSA",
        "question": "What is the difference between Stack memory and Heap memory in runtime data structures and variable allocation?",
        "reference": "[1] In runtime memory architecture: Stack memory is used for static memory allocation, storing active function call frames, local primitive variables, and object references; it operates in strict LIFO order managed automatically by CPU stack pointer manipulation (extremely fast, fixed size, causes StackOverflowError if exceeded). Heap memory is used for dynamic memory allocation, storing all objects and instances at runtime; it is managed by the Garbage Collector or manual allocation (slower, fragmented, causes OutOfMemoryError when exhausted).",
        "samples": [
            {
                "answer": "Stack memory stores local primitive variables, references, and active function call frames. It follows strict LIFO order, managed automatically by CPU hardware via the stack pointer, making allocation and deallocation instantaneous, but has a fixed size and throws StackOverflowError on infinite recursion. Heap memory is used for dynamic object allocation at runtime, storing all class instances. It is managed by garbage collection, is much larger and globally accessible across threads, but suffers from fragmentation and overhead, throwing OutOfMemoryError when exhausted.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Stack stores call frames, local primitives, and object references in LIFO order", "Stack is fast, managed automatically by CPU, and throws StackOverflowError", "Heap stores dynamic object instances globally across threads", "Heap is managed by Garbage Collection and throws OutOfMemoryError"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Escape Analysis and stack allocation of non-escaping objects", "Thread safety: stack is thread-private while heap is shared"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Cleanly distinguished stack frames from dynamic heap objects."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately cited respective runtime errors (StackOverflowError vs OutOfMemoryError)."}
                    ],
                    "citations": [{"claim": "Stack memory is used for static memory allocation... function call frames... Heap memory is used for dynamic memory allocation... storing all objects", "source_number": 1}],
                    "reasoning": "Clear, precise differentiation covering lifetimes, speeds, contents, and error types."
                }
            },
            {
                "answer": "Stack memory functions ke liye hoti hai jo jaldi delete ho jati hai. Heap memory bade objects ke liye hoti hai jo garbage collector delete karta hai. Stack fast hoti hai aur heap slow hoti hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Stack is for functions and is quickly reclaimed", "Heap is for objects cleaned by garbage collector", "Stack is faster than heap"],
                    "missing_core_concepts": ["Stack stores call frames, local variables, and object references", "LIFO stack pointer hardware mechanism", "Respective error types: StackOverflowError vs OutOfMemoryError"],
                    "deeper_concepts_to_probe": ["Thread-local stack vs shared heap"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Accurate high-level summary but lacked technical detail on allocation mechanisms and error conditions."}
                    ],
                    "citations": [{"claim": "Stack memory... local primitive variables, and object references... Heap memory is used for dynamic memory allocation", "source_number": 1}],
                    "reasoning": "Good basic intuition, but lacked depth on stack frames, references, and memory error bounds."
                }
            },
            {
                "answer": "Stack memory is on your graphics card and heap memory is on your SSD drive.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Both stack and heap are logical regions within system RAM allocated to a process"],
                    "deeper_concepts_to_probe": ["Process memory layout"],
                    "misconceptions": ["Mapping stack to GPU and heap to secondary storage"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total hardware confusion."}
                    ],
                    "citations": [{"claim": "In runtime memory architecture: Stack memory... Heap memory... in physical RAM", "source_number": 1}],
                    "reasoning": "Factually incorrect mapping of runtime process memory to discrete hardware components."
                }
            }
        ]
    },
    {
        "question_id": "DSA_07",
        "subject": "DSA",
        "question": "What is the difference between Breadth-First Search (BFS) and Depth-First Search (DFS) in graph traversal, and what are their time and space complexities?",
        "reference": "[1] Graph traversals explore vertices and edges: BFS explores level-by-level using a Queue (FIFO), ideal for finding the shortest path on unweighted graphs; space complexity is O(V) or O(W) (maximum width of the graph). DFS explores as deep as possible along each branch before backtracking using a Stack (LIFO or recursion), ideal for topological sort, cycle detection, and maze solving; space complexity is O(V) or O(H) (maximum depth of the recursion tree). Both algorithms run in O(V + E) time using an adjacency list.",
        "samples": [
            {
                "answer": "BFS traverses the graph level-by-level using a Queue (FIFO), making it the optimal choice for finding the shortest path in unweighted graphs. Its space complexity is O(V) to store the maximum width of the graph in the queue. DFS traverses as deeply as possible down each path before backtracking, using a Stack or recursion. It is ideal for topological sorting, cycle detection, and finding connected components. Its space complexity is O(V), bounded by the maximum height of the recursion tree. Both have a time complexity of O(V + E) using an adjacency list.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["BFS traverses level-by-level using a Queue (FIFO)", "BFS finds shortest path on unweighted graphs with O(V) queue space", "DFS explores deeply before backtracking using Stack/recursion", "DFS is used for topological sort and cycle detection with O(V) stack space", "Both run in O(V + E) time complexity"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Dijkstra as generalized BFS with priority queue for weighted graphs", "Tarjan's strongly connected components using DFS"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted Queue/level-order vs Stack/backtracking traversal."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Associated BFS with shortest path and DFS with topological sort, citing O(V+E) time."}
                    ],
                    "citations": [{"claim": "BFS explores level-by-level using a Queue... DFS explores as deep as possible along each branch before backtracking... Both algorithms run in O(V + E) time", "source_number": 1}],
                    "reasoning": "Clear, technically precise comparison of data structures, search mechanics, use cases, and complexity bounds."
                }
            },
            {
                "answer": "BFS breadth-wise search karta hai queue use karke, aur DFS depth-wise search karta hai recursion use karke. Dono ka time complexity O(N) hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["BFS uses a queue", "DFS uses recursion", "BFS is breadth-wise and DFS is depth-wise"],
                    "missing_core_concepts": ["Precise graph time complexity O(V + E) rather than generic O(N)", "Space complexity differences: O(Width) vs O(Height)", "Applications: shortest path for BFS vs topological sort/cycles for DFS"],
                    "deeper_concepts_to_probe": ["Graph time complexity parameters (Vertices and Edges)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Knew the basic queue/recursion difference but gave incomplete O(N) complexity."}
                    ],
                    "citations": [{"claim": "Both algorithms run in O(V + E) time using an adjacency list", "source_number": 1}],
                    "reasoning": "Correct basic intuition on queue vs recursion, but lacked formal O(V + E) complexity and specific problem applications."
                }
            },
            {
                "answer": "BFS is for searching binary files and DFS is for searching deleted files on hard disk.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["BFS and DFS are fundamental graph and tree traversal algorithms"],
                    "deeper_concepts_to_probe": ["Graph traversal algorithms"],
                    "misconceptions": ["Confusing algorithmic graph searches with file system file recovery"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete disconnect from graph algorithms."}
                    ],
                    "citations": [{"claim": "Graph traversals explore vertices and edges: BFS explores level-by-level... DFS explores as deep as possible", "source_number": 1}],
                    "reasoning": "Invented file system analogies having zero relation to graph traversals."
                }
            }
        ]
    },
    {
        "question_id": "DSA_08",
        "subject": "DSA",
        "question": "What are the performance and trade-off differences between a Balanced Binary Search Tree (such as Red-Black Tree) and a Hash Table?",
        "reference": "[1] Hash Tables provide O(1) average-time insertion, deletion, and search, but degrade to O(n) under heavy hash collisions (unless treeified) and do not maintain sorted order (cannot perform range queries or find min/max efficiently). Balanced Binary Search Trees (e.g. Red-Black Tree, AVL Tree) provide strict O(log n) worst-case guarantees for insertion, deletion, and search, while maintaining elements in sorted in-order traversal, enabling efficient range queries, floor/ceiling lookups, and order statistics.",
        "samples": [
            {
                "answer": "Hash Tables provide O(1) average time complexity for insert, delete, and search, but they do not maintain any order and have an O(n) worst-case degradation under adversarial hash collisions. Furthermore, they cannot efficiently support range queries or min/max lookups. Balanced BSTs (like Red-Black Trees or AVL trees) guarantee strict O(log n) worst-case time for all basic operations and maintain elements in sorted order, enabling efficient range scans, predecessor/successor queries, and ordered iteration.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Hash table provides O(1) average lookup/insert but lacks order", "Hash table degrades under hash collisions and cannot do range queries", "Balanced BST guarantees strict O(log n) worst-case bounds", "Balanced BST maintains elements in sorted order enabling range queries and predecessor/successor lookups"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Memory overhead: Tree node pointers (left, right, parent, color) vs Hash table array capacity", "Java TreeMap (Red-Black) vs HashMap"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted O(1) average vs O(log n) worst-case guarantees."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Identified range queries and ordered traversal as the decisive trade-off."}
                    ],
                    "citations": [{"claim": "Hash Tables provide O(1) average-time... do not maintain sorted order... Balanced Binary Search Trees... provide strict O(log n) worst-case guarantees... while maintaining elements in sorted in-order traversal", "source_number": 1}],
                    "reasoning": "Clear, precise explanation covering average vs worst-case time bounds and ordered traversal trade-offs."
                }
            },
            {
                "answer": "Hash table O(1) hota hai aur binary tree O(log n) hota hai. Isliye hash table hamesha better hota hai har situation me.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["Hash table is O(1) average", "Binary search tree is O(log n)"],
                    "missing_core_concepts": ["Balanced BST guarantees worst-case O(log n) whereas hash table can degrade", "BST maintains sorted order allowing range queries, min/max, and predecessor/successor lookups", "Naive belief that O(1) makes hash tables universally superior"],
                    "deeper_concepts_to_probe": ["Range queries and ordered data"],
                    "misconceptions": ["Believing hash table is universally superior for all scenarios"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Recalled average Big-O, but held the misconception that hash tables are always superior."}
                    ],
                    "citations": [{"claim": "Balanced Binary Search Trees... maintain elements in sorted in-order traversal, enabling efficient range queries", "source_number": 1}],
                    "reasoning": "Recalled asymptotic average numbers, but completely overlooked ordered operations and worst-case guarantees, naively assuming hash table is always better."
                }
            },
            {
                "answer": "Binary search tree is used for growing real trees in agriculture, and hash table is a dining table for dinner.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Both are fundamental data structures in computer science"],
                    "deeper_concepts_to_probe": ["Data structures"],
                    "misconceptions": ["Literal wordplay with no technical content"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Literal joke response."}
                    ],
                    "citations": [{"claim": "Balanced Binary Search Trees (e.g. Red-Black Tree...)... Hash Tables provide", "source_number": 1}],
                    "reasoning": "Flippant joke answer with zero technical merit."
                }
            }
        ]
    }
]
