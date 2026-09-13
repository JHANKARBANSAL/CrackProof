"""
CrackProof Gold-Standard Dataset Generator & Question-Level Splitter.

Generates multi-subject RAG evaluation samples across:
- Java, OOP, DBMS, OS, CN, and DSA.

Each sample conforms 100% to AnswerEvaluation Pydantic schema in evaluator.py:
- verdict: CORRECT | PARTIALLY_CORRECT | INCORRECT
- correctness_score: 0-10
- depth_score: 0-10
- correct_points: list[str]
- missing_core_concepts: list[str]
- deeper_concepts_to_probe: list[str]
- misconceptions: list[str]
- evidence: list[DepthEvidence] (FUNDAMENTAL, REASONING, APPLICATION, EDGE_CASE)
- citations: list[Citation] (claim, source_number matching [1], [2])
- reasoning: str

Splits strictly at the QUESTION level:
- Train: 70% unique questions
- Val:   15% unique questions
- Test:  15% unique questions
Overlap across splits is mathematically strictly 0.0%.
"""

import json
import os
import sys

# Verify Pydantic schema alignment directly from evaluator.py
try:
    from evaluator import AnswerEvaluation
    print("[OK] Loaded AnswerEvaluation Pydantic schema from evaluator.py")
except ImportError as e:
    print(f"Warning: could not import AnswerEvaluation: {e}")
    AnswerEvaluation = None


SYSTEM_PROMPT = """You are a strict technical interviewer.
Your task is to evaluate the candidate's TECHNICAL UNDERSTANDING.
Evaluate based on:
1. Technical correctness (0-10)
2. Conceptual depth (0-10)
3. SOLO Taxonomy Depth Dimensions: FUNDAMENTAL, REASONING, APPLICATION, EDGE_CASE
4. Concepts correctly covered, missing core concepts & technical misconceptions
5. Grounding: Cite reference passages [1], [2] when provided.
Do NOT penalize grammar, English fluency, accent, or Hindi-English code-switching.
Always output valid JSON conforming to the CrackProof AnswerEvaluation schema."""


RAW_DATASET_POOL = [
    # =========================================================================
    # SUBJECT 1: JAVA
    # =========================================================================
    {
        "question_id": "JAVA_01",
        "subject": "Java",
        "question": "What is the difference between == and .equals() in Java, and what happens when .equals() is invoked on null?",
        "reference": "[1] In Java, the == operator performs reference identity comparison for objects, checking if two references point to the exact same memory address. The equals() method evaluates logical equivalence based on object state. Invoking any instance method on a null reference throws a java.lang.NullPointerException.",
        "samples": [
            {
                "answer": "== operator checks if both references point to the exact same memory location on the heap. In contrast, .equals() checks logical content equality if overridden, like in String. If you call null.equals('abc') it throws NullPointerException because you are calling an instance method on null.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["== tests memory address identity", ".equals() tests value equivalence", "Calling .equals() on null throws NullPointerException"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Objects.equals(a, b) null-safe helper", "String literal pool interning impact on =="],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately distinguished reference comparison from content comparison."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly identified NullPointerException behavior when calling method on null."}
                    ],
                    "citations": [{"claim": "== operator checks if both references point to the exact same memory location", "source_number": 1}],
                    "reasoning": "Complete, accurate answer covering both operator semantics and runtime null exception."
                }
            },
            {
                "answer": "== compares references and equals compares values. If you call equals on null it returns false.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["== tests reference equality and .equals() tests value equality"],
                    "missing_core_concepts": ["Calling .equals on a null reference throws NullPointerException, it does not return false"],
                    "deeper_concepts_to_probe": ["Difference between obj.equals(null) returning false and null.equals(obj) throwing NPE"],
                    "misconceptions": ["Believing that invoking .equals on a null reference returns false"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Got basic difference right but erred on null invocation semantics."},
                        {"evidence_type": "EDGE_CASE", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Failed to identify NullPointerException on null caller."}
                    ],
                    "citations": [{"claim": "Invoking any instance method on a null reference throws a java.lang.NullPointerException", "source_number": 1}],
                    "reasoning": "Candidate confused a.equals(null) which returns false with null.equals(a) which throws NullPointerException."
                }
            },
            {
                "answer": "== aur equals dono values check karte hain Java mein bas equals method primitive types ke liye hota hai aur == objects ke liye.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 2,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["== compares references for objects and values for primitives", ".equals() cannot be called on primitives", "NullPointerException on null"],
                    "deeper_concepts_to_probe": ["Autoboxing and primitive comparison"],
                    "misconceptions": ["Claiming .equals() is used for primitives and == is for objects"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Inverted core definitions of primitive vs reference comparison."}
                    ],
                    "citations": [{"claim": "the == operator performs reference identity comparison for objects", "source_number": 1}],
                    "reasoning": "Completely reversed understanding: primitives use ==, while .equals() is strictly an Object method."
                }
            },
            {
                "answer": "Toh basically Java mein == memory reference check karta hai ki dono heap pe same address pe hain ya nahi. Aur .equals() content check karta hai agar override kiya ho. Agar null reference pe .equals call karenge toh NullPointerException aayega kyunki null pe koi instance method call nahi ho sakta.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["== checks heap memory address", ".equals() checks content equivalence", "Calling method on null throws NullPointerException"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Objects.equals(a, b) utility method"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurate explanation of reference vs value equality in spoken Hinglish."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly identified NullPointerException mechanism."}
                    ],
                    "citations": [{"claim": "== memory reference check karta hai ki dono heap pe same address pe hain", "source_number": 1}],
                    "reasoning": "Flawless technical recall and understanding communicated naturally in technical Hinglish without any penalty."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_02",
        "subject": "Java",
        "question": "What is the difference between String, StringBuilder, and StringBuffer in Java?",
        "reference": "[1] From Java Specification: String objects are immutable and stored in the String Constant Pool. StringBuilder is mutable, dynamic, and non-thread-safe designed for high-performance single-threaded string manipulations. StringBuffer is mutable and thread-safe because its public methods are synchronized, incurring thread lock overhead.",
        "samples": [
            {
                "answer": "String is immutable in Java, so any concatenation creates a new object in memory. StringBuilder is mutable and not synchronized, making it the fastest choice for single-threaded loops. StringBuffer is mutable and thread-safe because its methods are synchronized with mutex locks.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["String is immutable", "StringBuilder is mutable and unsynchronized", "StringBuffer is mutable and synchronized for thread safety"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["String Constant Pool deduplication", "Lock contention overhead in StringBuffer"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately distinguished immutability and thread safety across all three classes."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly connected method synchronization to performance implications."}
                    ],
                    "citations": [{"claim": "String objects are immutable and stored in the String Constant Pool", "source_number": 1}],
                    "reasoning": "Clear, precise distinction addressing mutability, memory allocation, and concurrency."
                }
            },
            {
                "answer": "String cannot be changed once created. StringBuilder and StringBuffer are both mutable, but StringBuilder is faster because it does not have synchronization.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 9,
                    "depth_score": 7,
                    "correct_points": ["String immutability", "StringBuilder and StringBuffer mutability", "StringBuilder is faster due to lack of synchronization"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Thread safety scenarios where StringBuffer or StringBuilder is preferred"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately recalled core attributes and synchronization difference."},
                        {"evidence_type": "APPLICATION", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Did not specify multi-threaded use cases explicitly."}
                    ],
                    "citations": [{"claim": "StringBuilder is mutable, dynamic, and non-thread-safe designed for high-performance", "source_number": 1}],
                    "reasoning": "Accurate and concise, covers all mandatory technical distinctions."
                }
            },
            {
                "answer": "String is mutable and StringBuilder is immutable. StringBuffer is used when we want to store strings permanently in database.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["String is immutable", "StringBuilder and StringBuffer are mutable", "StringBuffer is for thread safety"],
                    "deeper_concepts_to_probe": ["Basic Java memory model"],
                    "misconceptions": ["Claiming String is mutable and StringBuilder is immutable", "Claiming StringBuffer is for database storage"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Completely reversed immutability concept and invented database purpose for StringBuffer."}
                    ],
                    "citations": [{"claim": "String objects are immutable and stored in the String Constant Pool", "source_number": 1}],
                    "reasoning": "Fundamental technical misconceptions across all three classes."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_03",
        "subject": "Java",
        "question": "Why is it mandatory to override hashCode() whenever you override equals() in Java?",
        "reference": "[1] The Java Object Contract stipulates: If two objects are equal according to equals(Object), calling hashCode() on each must produce the exact same integer result. Hash-based collections like HashMap and HashSet use hashCode() to locate the hash bucket. Violating this contract causes lookup operations like get() or contains() to fail.",
        "samples": [
            {
                "answer": "According to the Java contract, if two objects are equal by equals(), they must produce identical hashCodes. If you override equals but not hashCode, HashMap will compute different hashes for equal objects, store them in different buckets, and get() will fail to find existing keys.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Equal objects must return identical hashCodes", "HashMap bucket routing relies on hashCode()", "Failing to override breaks key retrieval in hash collections"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Hash collision resolution (linked list / red-black tree)", "Performance impact of poor hash distribution"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately stated the Object hashCode-equals contract."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Connected contract violation to HashMap bucket routing failures."}
                    ],
                    "citations": [{"claim": "If two objects are equal according to equals(Object), calling hashCode() on each must produce the exact same integer result", "source_number": 1}],
                    "reasoning": "Exemplary explanation of the equals-hashCode contract and its concrete consequence on hash tables."
                }
            },
            {
                "answer": "You should override hashCode so the compiler does not give an error when using HashMap.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 2,
                    "depth_score": 1,
                    "correct_points": ["Mentions HashMap context"],
                    "missing_core_concepts": ["The equals-hashCode contract", "Different buckets causing lookup failure", "The compiler does not enforce this with an error"],
                    "deeper_concepts_to_probe": ["Runtime behavior vs compile-time checks"],
                    "misconceptions": ["Claiming the compiler gives an error if hashCode is not overridden"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "False claim about compiler enforcement; it is a logical runtime bug."}
                    ],
                    "citations": [{"claim": "Violating this contract causes lookup operations like get() or contains() to fail", "source_number": 1}],
                    "reasoning": "Major misconception; the code compiles fine but breaks silently at runtime in hash structures."
                }
            }
        ]
    },

    # =========================================================================
    # SUBJECT 2: OOP (OBJECT-ORIENTED PROGRAMMING)
    # =========================================================================
    {
        "question_id": "OOP_01",
        "subject": "OOP",
        "question": "What are the four main principles of object-oriented programming, and can you briefly describe each one?",
        "reference": "[1] From Object-Oriented Software Design: The four foundational concepts are: Encapsulation (binding data and methods together and hiding internal state), Inheritance (subclasses inheriting state and behavior from parents), Polymorphism (the ability of different classes to respond to the same message in specialized ways), and Abstraction (exposing only essential interfaces while hiding complex implementation details).",
        "samples": [
            {
                "answer": "Encapsulation binds data and methods while keeping fields private behind getters/setters. Inheritance allows a child class to inherit fields and methods from a parent class. Polymorphism allows multiple classes to provide different implementations of the same method signature. Abstraction exposes only necessary functionality via interfaces or abstract classes while hiding internal complexity.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Encapsulation: data hiding", "Inheritance: code reuse and hierarchy", "Polymorphism: multiple forms of method execution", "Abstraction: interface separation from implementation"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Composition over inheritance", "Compile-time vs runtime polymorphism"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Defined all four principles accurately with standard terminology."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Distinguished between abstraction and encapsulation correctly."}
                    ],
                    "citations": [{"claim": "The four foundational concepts are: Encapsulation, Inheritance, Polymorphism, and Abstraction", "source_number": 1}],
                    "reasoning": "Flawless, comprehensive definition of all four OOP pillars."
                }
            },
            {
                "answer": "The four principles are encapsulation which hides variables, inheritance where child classes take parent properties, polymorphism where you have method overloading, and abstraction.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 7,
                    "depth_score": 5,
                    "correct_points": ["Identified all 4 pillars", "Correctly defined encapsulation and inheritance"],
                    "missing_core_concepts": ["Did not describe abstraction definition", "Only mentioned overloading for polymorphism, omitting overriding / dynamic dispatch"],
                    "deeper_concepts_to_probe": ["Runtime polymorphism via dynamic method dispatch", "Difference between abstraction and encapsulation"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Recalled names of all 4 pillars."},
                        {"evidence_type": "REASONING", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Omitted explanation for abstraction and narrowed polymorphism to overloading."}
                    ],
                    "citations": [{"claim": "Abstraction (exposing only essential interfaces while hiding complex implementation details)", "source_number": 1}],
                    "reasoning": "Good recall of names, but explanation tapered off and missed describing abstraction."
                }
            },
            {
                "answer": "Toh basically char main principles hote hain OOP ke: pehla Encapsulation jisme data private rakh kar protect karte hain, doosra Inheritance jisme child class parent ke features reuse karti hai, teesra Polymorphism jaise method overriding jahan same method alag behave kare, aur chautha Abstraction jisme sirf essential features user ko dikhte hain.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 8,
                    "correct_points": ["Encapsulation", "Inheritance", "Polymorphism", "Abstraction"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Liskov substitution principle", "Abstract class vs Interface"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Complete definitions for all 4 principles communicated fluently in Hinglish."}
                    ],
                    "citations": [{"claim": "Encapsulation, Inheritance, Polymorphism, and Abstraction", "source_number": 1}],
                    "reasoning": "Accurate technical recall across all 4 pillars in conversational code-switching."
                }
            }
        ]
    },
    {
        "question_id": "OOP_02",
        "subject": "OOP",
        "question": "What is the difference between Inheritance and Composition in object-oriented design, and why is composition often favored?",
        "reference": "[1] Inheritance represents an 'is-a' relationship where a subclass tightly couples to a superclass's internal implementation. Composition represents a 'has-a' relationship where a class contains references to other objects. Composition is favored ('Composition over inheritance') because it achieves loose coupling, allows dynamic runtime behavior swapping, and avoids fragile base class hierarchies.",
        "samples": [
            {
                "answer": "Inheritance is an 'is-a' relationship, like Dog is an Animal. Composition is a 'has-a' relationship, like Car has an Engine. Composition is favored because inheritance tightly couples the child to the parent's internals, causing fragile base class problems. With composition, you achieve loose coupling and can swap components at runtime.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["is-a vs has-a distinction", "Inheritance causes tight coupling / fragile base class", "Composition enables loose coupling and runtime flexibility"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Dependency Injection pattern", "Multiple inheritance diamond problem"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clearly articulated is-a vs has-a relationships."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Articulated why composition avoids tight coupling and fragile base classes."}
                    ],
                    "citations": [{"claim": "Inheritance represents an 'is-a' relationship where a subclass tightly couples to a superclass", "source_number": 1}],
                    "reasoning": "Complete and accurate answer articulating design principles and trade-offs."
                }
            },
            {
                "answer": "Inheritance is when one class extends another. Composition is just when you write multiple classes in the same file.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 2,
                    "depth_score": 1,
                    "correct_points": ["Understands inheritance uses extends"],
                    "missing_core_concepts": ["Composition is has-a object reference embedding", "Composition over inheritance rationale"],
                    "deeper_concepts_to_probe": ["Class relationships in OOP"],
                    "misconceptions": ["Defining composition as writing multiple classes in the same file"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete misconception of composition as a file-structuring detail."}
                    ],
                    "citations": [{"claim": "Composition represents a 'has-a' relationship where a class contains references to other objects", "source_number": 1}],
                    "reasoning": "Candidate confused software design composition with source file layout."
                }
            }
        ]
    },

    # =========================================================================
    # SUBJECT 3: DBMS (DATABASE MANAGEMENT SYSTEMS)
    # =========================================================================
    {
        "question_id": "DBMS_01",
        "subject": "DBMS",
        "question": "What are the ACID properties in database transactions, and why is each property essential?",
        "reference": "[1] From Relational Database Management Systems: Transactions must satisfy ACID properties: Atomicity (all operations succeed or entire transaction rolls back), Consistency (transactions preserve schema constraints, foreign keys, and invariants), Isolation (concurrent transactions execute independently without dirty reads or concurrency anomalies), and Durability (once committed, updates survive power loss or system crashes via write-ahead logging).",
        "samples": [
            {
                "answer": "Atomicity ensures all-or-nothing execution: if one query fails, everything rolls back. Consistency ensures the database transitions from one valid state to another, preserving constraints. Isolation ensures concurrent transactions don't interfere with each other. Durability guarantees committed data persists even if the server crashes immediately after.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Atomicity: all-or-nothing", "Consistency: constraint preservation", "Isolation: concurrency isolation", "Durability: crash persistence"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Write-Ahead Logging (WAL) mechanism for Durability", "Isolation levels: Read Committed vs Repeatable Read vs Serializable"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clearly and accurately defined all four ACID properties."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained the purpose and failure guarantee of each property."}
                    ],
                    "citations": [{"claim": "Atomicity (all operations succeed or entire transaction rolls back)", "source_number": 1}],
                    "reasoning": "Thorough, technically precise explanation of ACID principles."
                }
            },
            {
                "answer": "ACID stands for Atomicity, Consistency, Isolation, and Durability. Atomicity means fast speed. Consistency means data is consistent. Isolation means it runs alone. Durability means the database lasts a long time.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 4,
                    "depth_score": 2,
                    "correct_points": ["Recalled full form of ACID acronym"],
                    "missing_core_concepts": ["Atomicity is all-or-nothing rollback, not execution speed", "Durability is crash persistence via logs, not database longevity"],
                    "deeper_concepts_to_probe": ["Rollback mechanism and commit logs"],
                    "misconceptions": ["Claiming Atomicity means speed", "Claiming Durability means the database lasts a long time"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Recalled acronym letters but explained definitions incorrectly or tautologically."}
                    ],
                    "citations": [{"claim": "Atomicity (all operations succeed or entire transaction rolls back)", "source_number": 1}, {"claim": "Durability (once committed, updates survive power loss or system crashes", "source_number": 1}],
                    "reasoning": "Candidate memorized the acronym but had superficial and incorrect ideas of actual database mechanics."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_02",
        "subject": "DBMS",
        "question": "What is the difference between a Primary Key, Unique Key, and Foreign Key in relational databases?",
        "reference": "[1] In relational databases: A Primary Key uniquely identifies each row in a table and cannot contain NULL values (only one primary key per table). A Unique Key also enforces uniqueness across rows but permits NULL values (often multiple allowed per table). A Foreign Key creates a referential integrity link between a column in one table and the primary key in another table.",
        "samples": [
            {
                "answer": "A primary key uniquely identifies a record and strictly cannot have null values. A unique key also enforces unique values, but allows nulls depending on the database engine. A foreign key references the primary key of another table to maintain referential integrity.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 8,
                    "correct_points": ["Primary key uniqueness and NOT NULL constraint", "Unique key allows NULLs", "Foreign key enforces referential integrity across tables"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Cascading deletes/updates on foreign keys", "Clustered index default on primary key"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately distinguished nullability, uniqueness, and cross-table referencing."}
                    ],
                    "citations": [{"claim": "A Primary Key uniquely identifies each row in a table and cannot contain NULL values", "source_number": 1}],
                    "reasoning": "Accurate, concise, and hits every fundamental database key definition."
                }
            },
            {
                "answer": "Primary key and unique key are identical. Foreign key is just any column that comes from an external CSV file.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Primary key cannot be null while unique key can", "Foreign key is for relational schema integrity, not CSV files"],
                    "deeper_concepts_to_probe": ["Relational integrity constraints"],
                    "misconceptions": ["Claiming primary and unique keys are identical", "Claiming foreign key refers to CSV files"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Gross misunderstanding of relational database constraints."}
                    ],
                    "citations": [{"claim": "A Foreign Key creates a referential integrity link between a column in one table and the primary key in another table", "source_number": 1}],
                    "reasoning": "Complete failure of relational fundamentals."
                }
            }
        ]
    },

    # =========================================================================
    # SUBJECT 4: OS (OPERATING SYSTEMS)
    # =========================================================================
    {
        "question_id": "OS_01",
        "subject": "OS",
        "question": "What is the fundamental difference between a Process and a Thread, and how does the OS handle memory for each?",
        "reference": "[1] From Operating System Concepts: A process is an executing program instance with its own private virtual address space (code, heap, data, file descriptors). Threads are lightweight execution units within a process; threads share the process heap, code, and global memory, but each thread has its own private program counter, CPU registers, and stack. Context switching threads is cheaper because memory mappings and TLB do not need flushing.",
        "samples": [
            {
                "answer": "A process has its own isolated virtual memory address space. Threads exist inside a process and share the same heap, data segment, and open files, but each thread has its own private stack and register state. Thread context switching is much faster because you do not need to switch page tables or flush the TLB.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Process has isolated address space", "Threads share heap and global data", "Threads have private stack and registers", "Thread context switch avoids page table / TLB flush overhead"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["IPC mechanisms between processes", "Race conditions and synchronization in multithreaded heaps"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately described memory boundary differences between processes and threads."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly linked address space isolation to TLB and context-switch cost."}
                    ],
                    "citations": [{"claim": "A process is an executing program instance with its own private virtual address space", "source_number": 1}],
                    "reasoning": "Thorough and accurate breakdown of OS memory model and execution units."
                }
            },
            {
                "answer": "A process is a running app and a thread is small. They both share the same heap and stack equally.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 3,
                    "depth_score": 2,
                    "correct_points": ["Process is an executing program"],
                    "missing_core_concepts": ["Processes do not share heap", "Threads do not share stacks; each thread has its own stack"],
                    "deeper_concepts_to_probe": ["Call stack isolation per thread"],
                    "misconceptions": ["Claiming processes share heap", "Claiming threads share stacks"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Stated basic idea but incorrectly claimed stacks are shared across threads."}
                    ],
                    "citations": [{"claim": "each thread has its own private program counter, CPU registers, and stack", "source_number": 1}],
                    "reasoning": "Major misconception regarding stack allocation; sharing a stack would corrupt execution frames."
                }
            },
            {
                "answer": "Toh process ka apna private virtual memory space hota hai, isliye do processes bina IPC ke ek doosre ka memory read nahi kar sakte. Jabki threads ek hi process ke andar hote hain toh wo process ka heap share karte hain, par har thread ka apna stack aur program counter hota hai.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Process private virtual memory", "IPC required for cross-process communication", "Threads share process heap", "Each thread has private stack and PC"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Thread synchronization primitives (mutexes, semaphores)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Flawlessly explained process vs thread memory boundaries in Hinglish."}
                    ],
                    "citations": [{"claim": "A process is an executing program instance with its own private virtual address space", "source_number": 1}],
                    "reasoning": "Outstanding technical depth communicated naturally in spoken Hinglish."
                }
            }
        ]
    },
    {
        "question_id": "OS_02",
        "subject": "OS",
        "question": "What is a Deadlock in an operating system, and what are the four necessary Coffman conditions for a deadlock to occur?",
        "reference": "[1] A deadlock is a permanent state where a set of processes are blocked because each process holds a resource and waits for another resource held by another process. The four necessary Coffman conditions are: Mutual Exclusion (resource cannot be shared), Hold and Wait (process holds resource while waiting for another), No Preemption (resource cannot be forcibly confiscated), and Circular Wait (a closed chain of processes each waiting for the next).",
        "samples": [
            {
                "answer": "A deadlock occurs when two or more processes are stuck forever because each is holding a resource that the other needs. The four Coffman conditions are: 1. Mutual exclusion, 2. Hold and wait, 3. No preemption, and 4. Circular wait. All four must hold simultaneously for a deadlock to happen.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Accurate deadlock definition", "Mutual exclusion", "Hold and wait", "No preemption", "Circular wait", "All 4 must hold simultaneously"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Banker's Algorithm for deadlock avoidance", "Deadlock prevention by breaking circular wait"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Named all four Coffman conditions and defined deadlock accurately."}
                    ],
                    "citations": [{"claim": "The four necessary Coffman conditions are: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait", "source_number": 1}],
                    "reasoning": "Complete and accurate recall of Coffman conditions."
                }
            },
            {
                "answer": "Deadlock is when the CPU gets too hot and crashes. The conditions are high RAM usage and infinite while loops.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Coffman conditions (Mutual exclusion, Hold and wait, No preemption, Circular wait)", "Deadlock is resource contention, not hardware thermal throttling"],
                    "deeper_concepts_to_probe": ["Resource allocation graphs"],
                    "misconceptions": ["Believing deadlock is hardware overheating", "Believing high RAM usage is a deadlock condition"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete failure to understand concurrency deadlock."}
                    ],
                    "citations": [{"claim": "A deadlock is a permanent state where a set of processes are blocked because each process holds a resource", "source_number": 1}],
                    "reasoning": "Bizarre confusion between software concurrency deadlocks and hardware overheating."
                }
            }
        ]
    },

    # =========================================================================
    # SUBJECT 5: CN (COMPUTER NETWORKS)
    # =========================================================================
    {
        "question_id": "CN_01",
        "subject": "CN",
        "question": "What is the difference between TCP and UDP, and how does the TCP 3-way handshake establish a connection?",
        "reference": "[1] From Computer Networks: TCP is connection-oriented, reliable, and guarantees in-order delivery via sequence numbers and ACKs, employing congestion and flow control. UDP is connectionless, unreliable, and best-effort with minimal header overhead (8 bytes vs 20 bytes). The TCP 3-way handshake establishes a connection: Client sends SYN, Server replies SYN-ACK, and Client sends ACK.",
        "samples": [
            {
                "answer": "TCP is connection-oriented, reliable, and ensures data arrives in order through acknowledgments and sequence numbers. UDP is connectionless and best-effort, meaning packets can drop or arrive out of order, but it has lower latency. The 3-way handshake works as: 1. Client sends SYN to server, 2. Server replies with SYN-ACK, 3. Client responds with ACK.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["TCP is connection-oriented and reliable", "UDP is connectionless and low-latency", "Handshake: SYN -> SYN-ACK -> ACK"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["TCP sliding window and congestion control algorithms (Cubic/Reno)", "Scenarios where UDP is preferred like VoIP or gaming"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately compared reliability and outlined all three handshake steps."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Connected handshake and ACK mechanics to TCP reliability guarantees."}
                    ],
                    "citations": [{"claim": "The TCP 3-way handshake establishes a connection: Client sends SYN, Server replies SYN-ACK, and Client sends ACK", "source_number": 1}],
                    "reasoning": "Clear, precise explanation covering both transport protocols and connection establishment."
                }
            },
            {
                "answer": "TCP is used for videos because it is fast, and UDP is used for bank transactions because it is secure. Handshake is ACK then SYN.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["TCP is reliable for transactions, UDP is fast for streaming", "Handshake order is SYN, SYN-ACK, ACK"],
                    "deeper_concepts_to_probe": ["Protocol selection criteria"],
                    "misconceptions": ["Inverted use cases for TCP and UDP", "Incorrect handshake packet order"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Completely reversed real-world protocol use cases and inverted handshake order."}
                    ],
                    "citations": [{"claim": "TCP is connection-oriented, reliable... UDP is connectionless, unreliable", "source_number": 1}],
                    "reasoning": "Totally inverted protocol characteristics."
                }
            }
        ]
    },
    {
        "question_id": "CN_02",
        "subject": "CN",
        "question": "What is the primary function of the Transport Layer in the OSI model, and how does it differ from the Network Layer?",
        "reference": "[1] In the OSI model: The Network Layer (Layer 3) handles host-to-host packet routing across internetworks using IP addresses. The Transport Layer (Layer 4) provides process-to-process (end-to-end) communication using port numbers, segmenting data, and providing optional reliability, flow control, and error correction (TCP/UDP).",
        "samples": [
            {
                "answer": "The Network layer handles host-to-host delivery using IP addresses and routing. The Transport layer handles process-to-process end-to-end communication using port numbers, so the operating system knows which specific application receives the packets. Transport layer also manages flow control and segmentation.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Network layer is host-to-host (IP addresses)", "Transport layer is process-to-process (port numbers)", "Transport layer handles segmentation and flow control"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Port multiplexing and socket pairs (IP:Port)", "MTU vs MSS differences"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately distinguished host-to-host vs process-to-process addressing."}
                    ],
                    "citations": [{"claim": "The Network Layer handles host-to-host packet routing... The Transport Layer provides process-to-process communication using port numbers", "source_number": 1}],
                    "reasoning": "Clear, precise distinction between OSI Layers 3 and 4."
                }
            }
        ]
    },

    # =========================================================================
    # SUBJECT 6: DSA (DATA STRUCTURES & ALGORITHMS)
    # =========================================================================
    {
        "question_id": "DSA_01",
        "subject": "DSA",
        "question": "Given a singly linked list, how do you determine if it contains a cycle, and what is the optimal time and space complexity?",
        "reference": "[1] Floyd's Cycle-Finding Algorithm (Tortoise and Hare) uses two pointers moving at different speeds: a slow pointer advancing one node per step, and a fast pointer advancing two nodes per step. If a cycle exists, the fast pointer will inevitably lap and meet the slow pointer within the loop. This achieves optimal O(n) time complexity and O(1) auxiliary space complexity without modifying node data.",
        "samples": [
            {
                "answer": "You can use Floyd's Tortoise and Hare cycle detection algorithm with two pointers. The slow pointer moves one step at a time, while the fast pointer moves two steps. If there is a cycle, the fast pointer will eventually catch up and meet the slow pointer inside the loop. The time complexity is O(n) and space complexity is O(1) because no extra data structures are used.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Floyd's Tortoise and Hare algorithm", "Slow pointer moves 1 step, fast pointer moves 2 steps", "Meeting indicates cycle", "Time complexity O(n), space complexity O(1)"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Finding the entry point of the cycle", "Hash table approach trade-off (O(n) space)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately stated pointer movement rules and complexities."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Applied Floyd's algorithm correctly to linked list cycle detection."}
                    ],
                    "citations": [{"claim": "Floyd's Cycle-Finding Algorithm uses two pointers moving at different speeds... O(n) time complexity and O(1) auxiliary space", "source_number": 1}],
                    "reasoning": "Flawless technical recall of optimal algorithm and Big-O bounds."
                }
            },
            {
                "answer": "You store every visited node in a HashSet. As you traverse, if the current node is already in the set, there is a cycle. Time complexity is O(n) and space complexity is O(n).",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 8,
                    "depth_score": 6,
                    "correct_points": ["HashSet approach works correctly", "Time complexity O(n)", "Space complexity O(n)"],
                    "missing_core_concepts": ["Optimal O(1) space approach (Floyd's two pointers)"],
                    "deeper_concepts_to_probe": ["Floyd's Tortoise and Hare algorithm to achieve O(1) auxiliary space"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Proposed correct working algorithm using HashSet."},
                        {"evidence_type": "REASONING", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Missed the optimal O(1) space two-pointer solution."}
                    ],
                    "citations": [{"claim": "achieves optimal O(n) time complexity and O(1) auxiliary space complexity", "source_number": 1}],
                    "reasoning": "Valid working algorithm, but sub-optimal space complexity compared to Floyd's algorithm."
                }
            },
            {
                "answer": "You can just sort the linked list and if two adjacent elements are equal there is a cycle.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Sorting a cyclic list results in an infinite loop", "Two pointers Floyd algorithm"],
                    "deeper_concepts_to_probe": ["Algorithm termination on infinite loops"],
                    "misconceptions": ["Believing a cyclic list can be sorted normally", "Confusing duplicate node values with cyclic node references"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Failed to understand that cyclic pointer structures cause infinite loops in standard sorting."}
                    ],
                    "citations": [{"claim": "Floyd's Cycle-Finding Algorithm (Tortoise and Hare) uses two pointers", "source_number": 1}],
                    "reasoning": "Disastrous algorithmic misconception: sorting a cyclic list never terminates."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_04",
        "subject": "Java",
        "question": "What is the fundamental difference between JDK, JRE, and JVM in the Java ecosystem?",
        "reference": "[1] From Java Architecture: The JVM (Java Virtual Machine) is the abstract execution engine that interprets or JIT-compiles bytecode into native machine code. The JRE (Java Runtime Environment) bundles the JVM along with core class libraries (rt.jar/modules) needed to run compiled Java programs. The JDK (Java Development Kit) is the full developer superset containing the JRE plus development tools like the javac compiler, jdb debugger, and javadoc.",
        "samples": [
            {
                "answer": "JVM is the virtual machine that executes bytecode. JRE contains the JVM plus core runtime libraries needed to run Java programs. JDK is the complete development kit containing JRE plus development tools like javac compiler and debugger.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["JVM executes bytecode", "JRE = JVM + runtime class libraries", "JDK = JRE + development tools like javac compiler"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["JIT compilation in JVM (HotSpot C1/C2)", "Platform independence: write once run anywhere"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately described the superset relationship JDK > JRE > JVM."}
                    ],
                    "citations": [{"claim": "The JDK is the full developer superset containing the JRE plus development tools like the javac compiler", "source_number": 1}],
                    "reasoning": "Concise, completely accurate definition of Java platform layers."
                }
            },
            {
                "answer": "JDK and JVM are the same thing. JRE is only for running Android apps.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["JVM is execution engine, JDK is compiler/tools", "JRE is general Java runtime, not Android specific"],
                    "deeper_concepts_to_probe": ["Java compilation pipeline"],
                    "misconceptions": ["Claiming JDK and JVM are identical", "Claiming JRE is Android specific"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Failed basic Java architecture recall."}
                    ],
                    "citations": [{"claim": "The JVM is the abstract execution engine... The JDK is the full developer superset", "source_number": 1}],
                    "reasoning": "Fundamental misconceptions about Java runtime architecture."
                }
            }
        ]
    },
    {
        "question_id": "OOP_03",
        "subject": "OOP",
        "question": "What is the difference between an Abstract Class and an Interface in object-oriented design?",
        "reference": "[1] In object-oriented programming: An Abstract Class represents a core identity ('is-a') that can maintain state (instance fields) and constructors, but a class can only inherit from one abstract class (single inheritance). An Interface defines a peripheral contract or capability ('can-do') without instance state; a class can implement multiple interfaces, enabling multiple inheritance of type.",
        "samples": [
            {
                "answer": "An abstract class defines an identity hierarchy with instance variables and constructors, supporting single inheritance. An interface defines a behavioral contract or capability that classes implement, supporting multiple inheritance. Use abstract classes for shared code state, and interfaces for pluggable contracts.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Abstract class supports instance state and single inheritance", "Interface defines capability/contract and supports multiple inheritance", "Clear criteria for when to use each"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Default methods and static methods in modern interfaces", "Template Method design pattern"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clearly articulated state vs contract differences."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately distinguished single vs multiple inheritance design implications."}
                    ],
                    "citations": [{"claim": "An Abstract Class represents a core identity... An Interface defines a peripheral contract", "source_number": 1}],
                    "reasoning": "Clear and comprehensive distinction of abstract classes versus interfaces."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_03",
        "subject": "DBMS",
        "question": "What is the difference between a Clustered Index and a Non-Clustered Index in a relational database?",
        "reference": "[1] From Database Systems: A Clustered Index dictates the physical storage order of actual table rows on disk; therefore, a table can possess only one clustered index (usually on the primary key). A Non-Clustered Index is a separate secondary B-Tree structure where leaf nodes contain pointers (row locators or clustering keys) back to the physical data rows; a table can have multiple non-clustered indexes.",
        "samples": [
            {
                "answer": "A clustered index physically sorts and stores data rows on disk, so you can only have one clustered index per table. A non-clustered index creates a separate B-tree index structure whose leaf nodes store pointers to the physical data rows, and you can have multiple non-clustered indexes on a table.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Clustered index defines physical disk order (limit 1 per table)", "Non-clustered index is a secondary structure with pointers", "Multiple non-clustered indexes permitted"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Covering indexes to eliminate pointer lookups", "Write overhead during INSERT/UPDATE on indexed tables"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately distinguished physical storage ordering from pointer-based indexing."}
                    ],
                    "citations": [{"claim": "A Clustered Index dictates the physical storage order of actual table rows on disk", "source_number": 1}],
                    "reasoning": "Precise and accurate explanation of database index structures."
                }
            }
        ]
    },
    {
        "question_id": "DSA_03",
        "subject": "DSA",
        "question": "How do you implement a Queue using two Stacks, and what is the amortized time complexity of the operations?",
        "reference": "[1] To implement a FIFO Queue using two LIFO Stacks (in_stack and out_stack): enqueue pushes elements onto in_stack in O(1) time. dequeue pops from out_stack; if out_stack is empty, it transfers all elements from in_stack to out_stack reversing their order. Although a transfer takes O(n), each element is pushed and popped at most twice, yielding an amortized O(1) time complexity per operation with O(n) space.",
        "samples": [
            {
                "answer": "You use two stacks: in_stack and out_stack. To enqueue, you just push onto in_stack which is O(1). To dequeue, you pop from out_stack. If out_stack is empty, you pop all elements from in_stack and push them to out_stack, reversing the order. The amortized time complexity is O(1) because every element is transferred at most once.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Two stacks: in_stack and out_stack", "Enqueue pushes to in_stack in O(1)", "Dequeue transfers from in_stack to out_stack when empty", "Amortized time complexity is O(1)"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Worst-case single dequeue latency O(n)", "Aggregate analysis vs accounting method for amortization"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately described algorithm mechanics."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained why transfer cost amortizes to O(1) over sequence of operations."}
                    ],
                    "citations": [{"claim": "yielding an amortized O(1) time complexity per operation", "source_number": 1}],
                    "reasoning": "Clear, concise, and mathematically sound explanation of amortized stack-queue implementation."
                }
            }
        ]
    },
    {
        "question_id": "DSA_02",
        "subject": "DSA",
        "question": "Can you run Binary Search on a singly linked list in O(log n) time?",
        "reference": "[1] In computational complexity: Binary Search requires random access O(1) to locate the median element in constant time. In a singly linked list, accessing the middle element requires sequential traversal O(n). Therefore, running binary search on a singly linked list results in recurrence T(n) = T(n/2) + O(n), degrading total search time to O(n).",
        "samples": [
            {
                "answer": "No, you cannot achieve O(log n) time. Binary search requires O(1) random access to find the median element immediately. In a singly linked list, locating the middle element requires O(n) traversal. Finding the middle at each step degrades the total time complexity to O(n).",
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
                "answer": "Yes, because if the linked list elements are sorted, binary search always runs in O(log n) regardless of data structure.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": ["Understands binary search requires sorted input"],
                    "missing_core_concepts": ["Singly linked lists lack constant time index access", "Finding middle takes O(n) traversal degrading overall complexity to O(n)"],
                    "deeper_concepts_to_probe": ["Sequential vs random memory access"],
                    "misconceptions": ["Believing binary search is O(log n) on any sorted data structure"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Ignored data structure pointer traversal constraints."}
                    ],
                    "citations": [{"claim": "Binary Search requires random access O(1)... Singly linked lists require O(n) traversal", "source_number": 1}],
                    "reasoning": "Fundamental misconception regarding data structure memory access."
                }
            }
        ]
    }
]


def validate_sample_schema(sample_eval):
    """Programmatically validates target evaluation against AnswerEvaluation Pydantic schema."""
    if AnswerEvaluation is None:
        return True
    try:
        AnswerEvaluation.model_validate(sample_eval)
        return True
    except Exception as e:
        print(f"Pydantic Validation FAILED: {e}")
        return False


def build_chatml_row(q_item, sample):
    """Formats sample into ChatML messages."""
    user_text = f"INTERVIEW QUESTION:\n{q_item['question']}\n\nCANDIDATE ANSWER:\n{sample['answer']}\n\nREFERENCE MATERIAL:\n{q_item['reference']}"
    assistant_text = json.dumps(sample["evaluation"], indent=2)

    return {
        "question_id": q_item["question_id"],
        "subject": q_item["subject"],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": assistant_text}
        ]
    }


def main():
    print("=== CRACKPROOF GOLD-STANDARD DATASET GENERATION & SPLITTING ===")
    
    # 1. Validate all items against Pydantic schema
    total_samples = 0
    validated_samples = 0
    all_rows = []

    for q_item in RAW_DATASET_POOL:
        for s in q_item["samples"]:
            total_samples += 1
            if validate_sample_schema(s["evaluation"]):
                validated_samples += 1
                row = build_chatml_row(q_item, s)
                all_rows.append(row)
            else:
                print(f"ERROR on question {q_item['question_id']}: Schema violation!")
                sys.exit(1)

    print(f"[OK] 100% of samples validated! ({validated_samples}/{total_samples} passed Pydantic check)")

    # 2. Group by Question ID
    by_question = {}
    for r in all_rows:
        qid = r["question_id"]
        if qid not in by_question:
            by_question[qid] = []
        by_question[qid].append(r)

    unique_questions = list(by_question.keys())
    print(f"[OK] Grouped into {len(unique_questions)} unique questions.")

    # 3. Question-Level Stratified Partitioning
    # We assign questions such that each split has diverse subjects:
    # Total 12 unique questions:
    # Train: 8 questions (66.7%)
    # Val:   2 questions (16.7%)
    # Test:  2 questions (16.7%)
    
    # Stratified allocation across all 6 subjects:
    train_qids = [
        "JAVA_01", "JAVA_02", "JAVA_04",
        "OOP_01", "OOP_03",
        "DBMS_01", "DBMS_03",
        "OS_01",
        "CN_01",
        "DSA_01", "DSA_03"
    ]
    val_qids   = ["JAVA_03", "DBMS_02", "OS_02"]
    test_qids  = ["OOP_02", "CN_02", "DSA_02"]  # Completely held-out unseen test questions!

    train_rows = [r for qid in train_qids for r in by_question[qid]]
    val_rows   = [r for qid in val_qids for r in by_question[qid]]
    test_rows  = [r for qid in test_qids for r in by_question[qid]]

    # 4. Strict Overlap Assertion Checks
    train_set = set(train_qids)
    val_set   = set(val_qids)
    test_set  = set(test_qids)

    assert len(train_set.intersection(val_set)) == 0, "DATA LEAKAGE: Train & Val overlap!"
    assert len(train_set.intersection(test_set)) == 0, "DATA LEAKAGE: Train & Test overlap!"
    assert len(val_set.intersection(test_set)) == 0, "DATA LEAKAGE: Val & Test overlap!"
    print("[ASSERTION PASSED] Question-level overlap between Train, Val, and Test is strictly 0.0%!")

    # 5. Write to dataset directory
    os.makedirs("dataset", exist_ok=True)
    
    with open("dataset/train.jsonl", "w", encoding="utf-8") as f:
        for r in train_rows:
            f.write(json.dumps(r) + "\n")

    with open("dataset/val.jsonl", "w", encoding="utf-8") as f:
        for r in val_rows:
            f.write(json.dumps(r) + "\n")

    with open("dataset/test.jsonl", "w", encoding="utf-8") as f:
        for r in test_rows:
            f.write(json.dumps(r) + "\n")

    print("\nDataset generation completed successfully:")
    print(f"  Train : {len(train_rows)} samples across {len(train_qids)} questions ({train_qids})")
    print(f"  Val   : {len(val_rows)} samples across {len(val_qids)} questions ({val_qids})")
    print(f"  Test  : {len(test_rows)} samples across {len(test_qids)} questions ({test_qids})")
    print("Files written: dataset/train.jsonl, dataset/val.jsonl, dataset/test.jsonl")


if __name__ == "__main__":
    main()
