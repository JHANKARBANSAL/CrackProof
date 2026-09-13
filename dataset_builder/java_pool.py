"""
Java Question Pool: 8 Questions x 3 Samples = 24 Samples.
Coverage:
JAVA_01: == vs .equals() and null semantics
JAVA_02: String vs StringBuilder vs StringBuffer
JAVA_03: hashCode() and equals() contract
JAVA_04: JDK vs JRE vs JVM architecture
JAVA_05: Checked vs Unchecked Exceptions
JAVA_06: final vs finally vs finalize()
JAVA_07: Java Garbage Collection (Generational Heap)
JAVA_08: Interface Default Methods vs Abstract Classes
"""

JAVA_POOL = [
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
            }
        ]
    },
    {
        "question_id": "JAVA_02",
        "subject": "Java",
        "question": "What is the difference between String, StringBuilder, and StringBuffer in Java?",
        "reference": "[1] In Java: String is immutable; any modification creates a new object in the String Constant Pool or heap. StringBuilder is mutable and not synchronized, designed for high performance in single-threaded environments. StringBuffer is mutable and synchronized, making all public methods thread-safe at the cost of synchronization overhead.",
        "samples": [
            {
                "answer": "String is immutable in Java, so any change creates a new object. StringBuilder and StringBuffer are both mutable, but StringBuffer has synchronized methods making it thread-safe with overhead, whereas StringBuilder is unsynchronized and faster for single-threaded code.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["String is immutable", "StringBuilder is mutable and unsynchronized", "StringBuffer is mutable and synchronized / thread-safe"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["String constant pool interning", "Compiler optimization replacing + with StringBuilder"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly stated immutability and mutability across all three classes."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained synchronization trade-off between StringBuffer and StringBuilder."}
                    ],
                    "citations": [{"claim": "StringBuffer is mutable and synchronized... StringBuilder is mutable and not synchronized", "source_number": 1}],
                    "reasoning": "Clear and comprehensive explanation of mutability and thread safety."
                }
            },
            {
                "answer": "String immutable hota hai jabki StringBuilder aur StringBuffer mutable hote hain. Dono me bas performance ka thoda farq hota hai kyunki StringBuffer purana class hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["String is immutable while StringBuilder and StringBuffer are mutable", "StringBuilder is faster than StringBuffer"],
                    "missing_core_concepts": ["Synchronization and thread-safety mechanism in StringBuffer"],
                    "deeper_concepts_to_probe": ["Thread safety and locking overhead"],
                    "misconceptions": ["Attributing performance difference solely to age rather than synchronization"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Captured mutability difference correctly."},
                        {"evidence_type": "REASONING", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Missed synchronization as the cause of the performance difference."}
                    ],
                    "citations": [{"claim": "StringBuffer is mutable and synchronized, making all public methods thread-safe at the cost of synchronization overhead", "source_number": 1}],
                    "reasoning": "Understood mutability but failed to identify synchronization as the core distinction."
                }
            },
            {
                "answer": "String is mutable and thread-safe. StringBuilder is for numbers and StringBuffer is for characters.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["String is immutable", "Both StringBuilder and StringBuffer manipulate character sequences"],
                    "deeper_concepts_to_probe": ["Object immutability in Java"],
                    "misconceptions": ["Believing String is mutable", "Believing StringBuilder is for numbers"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Gross misunderstanding of String mutability and buffer purposes."}
                    ],
                    "citations": [{"claim": "String is immutable; any modification creates a new object", "source_number": 1}],
                    "reasoning": "Completely inaccurate description of all three classes."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_03",
        "subject": "Java",
        "question": "Why is it mandatory to override hashCode() whenever you override equals() in Java?",
        "reference": "[1] The contract between equals() and hashCode() specifies that if two objects are equal according to the equals(Object) method, then calling hashCode() on each of the two objects must produce the same integer result. If violated, hash-based collections such as HashMap and HashSet will fail to locate or retrieve stored elements.",
        "samples": [
            {
                "answer": "The contract states that if two objects are equal according to equals(), they must return the same hashCode(). If you override equals without hashCode, two logically equal objects will hash to different buckets in a HashMap, making it impossible to retrieve the stored value.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Equal objects must return identical hash codes", "Failure results in bucket lookup failures in hash-based collections"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Hash collision resolution (chaining vs open addressing)", "Unequal objects returning the same hash code (valid collision)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately cited the equals and hashCode contract."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly linked hash codes to HashMap bucket placement."}
                    ],
                    "citations": [{"claim": "if two objects are equal according to the equals(Object) method, then calling hashCode()... must produce the same integer result", "source_number": 1}],
                    "reasoning": "Direct and technically sound articulation of the contract and hash table mechanics."
                }
            },
            {
                "answer": "Agar equals override kiya toh hashCode bhi karna padta hai taaki Java ko pata chale dono alag hain. Warna memory leak ho jata hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["Understands that overriding equals requires overriding hashCode"],
                    "missing_core_concepts": ["Contract: equal objects must produce equal hash codes", "Impact on hash-based collection lookup"],
                    "deeper_concepts_to_probe": ["HashMap internal bucket lookup"],
                    "misconceptions": ["Believing a hashCode mismatch causes a memory leak instead of collection lookup failure"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Recalled the rule but hallucinated memory leak consequences."}
                    ],
                    "citations": [{"claim": "hash-based collections such as HashMap and HashSet will fail to locate or retrieve stored elements", "source_number": 1}],
                    "reasoning": "Recognized rule existence but confused the mechanical consequences on hash tables with memory leaks."
                }
            },
            {
                "answer": "hashCode override karna zaroori nahi hai, compiler bas warning deta hai. equals se hi comparison hota hai hashCode bas printing ke liye hota hai.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["The hashCode contract is vital for hash collections", "hashCode determines bucket index, not just printing"],
                    "deeper_concepts_to_probe": ["Hash-based data structures"],
                    "misconceptions": ["Believing hashCode is only used for printing", "Believing the contract is optional"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Dismissed hashCode as cosmetic."}
                    ],
                    "citations": [{"claim": "calling hashCode() on each of the two objects must produce the same integer result. If violated, hash-based collections such as HashMap... fail", "source_number": 1}],
                    "reasoning": "Fundamental misunderstanding of hashing in the Java Collections Framework."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_04",
        "subject": "Java",
        "question": "What is the fundamental difference between JDK, JRE, and JVM in the Java ecosystem?",
        "reference": "[1] JDK (Java Development Kit) is the full developer environment containing the JRE, compiler (javac), debugger, and development tools. JRE (Java Runtime Environment) provides the libraries, Java ClassLoader, and JVM needed to run compiled Java bytecode. JVM (Java Virtual Machine) is the abstract execution engine that executes bytecode on the host OS, managing memory, JIT compilation, and garbage collection.",
        "samples": [
            {
                "answer": "JDK is the complete development toolkit containing javac compiler and tools plus JRE. JRE is the runtime environment containing libraries plus JVM. JVM is the virtual machine that actually executes compiled bytecode into machine code using JIT compilation.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["JDK contains JRE and development tools like javac", "JRE contains JVM and runtime class libraries", "JVM executes bytecode on the target machine"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["JIT compiler (C1/C2) optimization", "Platform independence: write once run anywhere through JVM abstraction"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clear nested hierarchy: JDK includes JRE, which includes JVM."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Distinguished compilation role (javac) from execution role (JVM)."}
                    ],
                    "citations": [{"claim": "JDK is the full developer environment... JRE provides the libraries... JVM executes bytecode on the host OS", "source_number": 1}],
                    "reasoning": "Accurate and structural breakdown of the three Java execution layers."
                }
            },
            {
                "answer": "JDK compile karta hai, JRE run karta hai, aur JVM Java files ko seedha machine code me save karta hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["JDK is for compiling", "JRE is for running"],
                    "missing_core_concepts": ["JVM executes intermediate bytecode via JIT/interpreter, not direct saving to machine code", "Hierarchy: JDK contains JRE contains JVM"],
                    "deeper_concepts_to_probe": ["Bytecode intermediate representation"],
                    "misconceptions": ["Believing JVM saves Java files directly to machine code"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood high-level purpose but inaccurate on JVM execution."}
                    ],
                    "citations": [{"claim": "JVM is the abstract execution engine that executes bytecode on the host OS", "source_number": 1}],
                    "reasoning": "Captured high-level responsibilities but lacked precision on bytecode interpretation."
                }
            },
            {
                "answer": "JVM is for writing code, JRE is for testing code, and JDK is the server where Java runs in production.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["JDK is the developer kit", "JRE is runtime", "JVM is virtual execution machine"],
                    "deeper_concepts_to_probe": ["Java compilation pipeline"],
                    "misconceptions": ["Claiming JDK is a server and JVM is for writing code"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total confusion of terms and execution environments."}
                    ],
                    "citations": [{"claim": "JDK is the full developer environment... JRE provides the libraries... JVM executes bytecode", "source_number": 1}],
                    "reasoning": "Arbitrary and incorrect associations for all three components."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_05",
        "subject": "Java",
        "question": "What is the difference between Checked and Unchecked Exceptions in Java, and how does the compiler treat them?",
        "reference": "[1] In Java: Checked exceptions (subclasses of Exception excluding RuntimeException) are checked at compile-time; the compiler forces the code to handle them with try-catch or declare them with throws. Unchecked exceptions (subclasses of RuntimeException and Error) represent programming bugs or system failures; the compiler does not enforce handling.",
        "samples": [
            {
                "answer": "Checked exceptions extend Exception (excluding RuntimeException) and are enforced by the compiler at compile-time; you must either catch them or declare them with throws, like IOException. Unchecked exceptions extend RuntimeException, like NullPointerException or ArithmeticException; the compiler does not enforce handling because they typically represent logic bugs.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Checked exceptions are verified at compile time", "Compiler enforces handle-or-declare for checked exceptions", "Unchecked exceptions inherit from RuntimeException or Error", "Unchecked exceptions represent runtime programming bugs"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Custom checked exception design", "try-with-resources and AutoCloseable"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clear distinction of inheritance hierarchy under Throwable."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained why compiler enforces checked exceptions vs unchecked bugs."}
                    ],
                    "citations": [{"claim": "Checked exceptions are checked at compile-time; the compiler forces the code to handle them... Unchecked exceptions represent programming bugs", "source_number": 1}],
                    "reasoning": "Accurate, well-reasoned distinction between compile-time enforcement and runtime logic failures."
                }
            },
            {
                "answer": "Checked exceptions compiler check karta hai jaise syntax error, aur unchecked exceptions runtime pe aate hain jaise divide by zero. Dono try-catch me pakad sakte hain.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["Checked exceptions checked at compile time", "Unchecked exceptions occur at runtime like divide by zero", "Both can be handled in try-catch"],
                    "missing_core_concepts": ["Checked exceptions are not syntax errors; they represent recoverable external failures (e.g. FileNotFoundException)", "Class hierarchy: RuntimeException vs Exception"],
                    "deeper_concepts_to_probe": ["Throws clause in method signature"],
                    "misconceptions": ["Equating checked exceptions with syntax errors"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Confused checked exceptions with syntax compile errors."}
                    ],
                    "citations": [{"claim": "Checked exceptions are checked at compile-time; the compiler forces the code to handle them with try-catch or declare them with throws", "source_number": 1}],
                    "reasoning": "Candidate confused checked exceptions with compile-time syntax errors, though recognized runtime exception behavior."
                }
            },
            {
                "answer": "Checked exceptions are those that have a catch block, and unchecked exceptions are those where you forget to write a catch block and program crashes.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 2,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Checked vs unchecked is a compile-time type classification under Throwable, not whether a catch block is written"],
                    "deeper_concepts_to_probe": ["Java exception hierarchy"],
                    "misconceptions": ["Believing checked/unchecked depends on whether a try-catch block was typed by the developer"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Fundamentally confused static type classification with developer handling."}
                    ],
                    "citations": [{"claim": "Checked exceptions (subclasses of Exception excluding RuntimeException) are checked at compile-time", "source_number": 1}],
                    "reasoning": "Candidate incorrectly defined exception categories based on whether user code caught them."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_06",
        "subject": "Java",
        "question": "What is the difference between final, finally, and finalize() in Java?",
        "reference": "[1] final is a keyword/modifier: a final variable cannot be reassigned, a final method cannot be overridden, and a final class cannot be subclassed. finally is a block associated with try-catch that executes regardless of whether an exception is thrown. finalize() is a method on Object invoked by the Garbage Collector before reclaiming memory (deprecated in Java 9+).",
        "samples": [
            {
                "answer": "final is a keyword that makes variables constant, prevents method overriding, and stops class inheritance. finally is a block in exception handling that always executes for cleanup. finalize() is an Object method called by the garbage collector before reclaiming an object, though it is deprecated in modern Java.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["final modifier restricts reassignment, overriding, and inheritance", "finally block guarantees execution for resource cleanup", "finalize() is GC cleanup method on Object (deprecated)"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Cases where finally does not run (System.exit)", "Cleaner / PhantomReference replacing finalize()"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Cleanly distinguished modifier, block, and method."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately identified finalize() deprecation."}
                    ],
                    "citations": [{"claim": "final is a keyword/modifier... finally is a block... finalize() is a method on Object invoked by the Garbage Collector", "source_number": 1}],
                    "reasoning": "Clear, accurate, and covers all three components with proper contextual detail."
                }
            },
            {
                "answer": "final variable ko change nahi kar sakte. finally try-catch ke baad hamesha chalta hai. finalize() bhi finally jaisa hota hai bas functions ke liye hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["final prevents variable reassignment", "finally always executes after try-catch"],
                    "missing_core_concepts": ["final for methods and classes", "finalize() is a GC hook method on Object, not a function cleanup block"],
                    "deeper_concepts_to_probe": ["Garbage collection hooks"],
                    "misconceptions": ["Believing finalize() is a cleanup block for functions"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Accurate on final variable and finally block, but confused finalize()."}
                    ],
                    "citations": [{"claim": "finalize() is a method on Object invoked by the Garbage Collector before reclaiming memory", "source_number": 1}],
                    "reasoning": "Understood final variable and finally block, but completely misunderstood finalize()."
                }
            },
            {
                "answer": "final, finally, aur finalize teeno same hain, bas alag alag versions of Java me syntax change hua tha to confuse programmers.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["final is modifier, finally is control flow block, finalize is Object method"],
                    "deeper_concepts_to_probe": ["Java language keywords and lifecycle"],
                    "misconceptions": ["Believing the three are syntax variations of the same concept"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "No technical comprehension shown."}
                    ],
                    "citations": [{"claim": "final is a keyword/modifier... finally is a block... finalize() is a method on Object", "source_number": 1}],
                    "reasoning": "Purely dismissive and factually incorrect answer."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_07",
        "subject": "Java",
        "question": "How does Java Garbage Collection work, and what is the difference between the Young Generation and Old Generation in heap memory?",
        "reference": "[1] Java Garbage Collection automatically manages heap memory by identifying and deleting unreachable objects using GC roots. Based on the Weak Generational Hypothesis, the heap is split into: Young Generation (Eden and Survivor spaces where new objects are allocated and collected via frequent Minor GCs) and Old Generation (Tenured space where objects surviving multiple collections are promoted, collected via less frequent Major/Full GCs).",
        "samples": [
            {
                "answer": "Java GC automatically reclaims memory of unreachable objects using GC root tracing. Under the generational hypothesis, most objects die young, so heap is split: Young Gen (Eden + Survivor spaces) where new objects are created and cleaned with fast Minor GCs, and Old Gen where long-lived objects are promoted after surviving cycles, cleaned by Major GCs.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["GC traces reachable objects from GC roots", "Generational hypothesis: most objects have short lifespans", "Young Gen has Eden and Survivor spaces for Minor GC", "Old Gen stores long-lived objects promoted after surviving threshold"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Stop-the-World pauses", "Modern GC algorithms: G1, ZGC"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clear articulation of heap generations and reachability."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Connected the generational hypothesis to minor vs major GC frequency."}
                    ],
                    "citations": [{"claim": "Young Generation (Eden and Survivor spaces... collected via frequent Minor GCs) and Old Generation (Tenured space where objects surviving... promoted)", "source_number": 1}],
                    "reasoning": "Thorough and accurate description of Java generational garbage collection."
                }
            },
            {
                "answer": "Garbage collector memory saaf karta hai jab heap bhar jata hai. Young generation me naye objects bante hain aur Old generation me purane objects rehte hain.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["GC cleans heap memory", "Young gen holds new objects and Old gen holds old objects"],
                    "missing_core_concepts": ["Eden and Survivor spaces within Young Gen", "Minor GC vs Major GC distinctions", "Reachability from GC roots"],
                    "deeper_concepts_to_probe": ["Promotion threshold (tenuring)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Captured high-level concept but missed internal heap structure and collection mechanics."}
                    ],
                    "citations": [{"claim": "Young Generation (Eden and Survivor spaces... and Old Generation (Tenured space where objects surviving multiple collections are promoted)", "source_number": 1}],
                    "reasoning": "High-level understanding present, but lacks technical depth regarding spaces and collection phases."
                }
            },
            {
                "answer": "Java does not have automatic garbage collection; developers must manually call delete or free like in C++ or else memory overflows.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Java has automatic garbage collection", "Explicit memory deallocation is not permitted in Java"],
                    "deeper_concepts_to_probe": ["JVM memory model"],
                    "misconceptions": ["Believing Java requires manual free/delete"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Fundamental falsehood regarding Java's memory model."}
                    ],
                    "citations": [{"claim": "Java Garbage Collection automatically manages heap memory by identifying and deleting unreachable objects", "source_number": 1}],
                    "reasoning": "Blatantly incorrect claim about manual memory management in Java."
                }
            }
        ]
    },
    {
        "question_id": "JAVA_08",
        "subject": "Java",
        "question": "How do interface default and static methods in Java 8 differ from methods in abstract classes?",
        "reference": "[1] Java 8 introduced default and static methods in interfaces to enable interface evolution with backward compatibility. Key differences: An interface cannot hold instance state (no instance fields; all variables are public static final), while an abstract class can maintain mutable instance state via instance variables and constructors. A class can implement multiple interfaces, but can extend only one abstract class.",
        "samples": [
            {
                "answer": "Interface default methods allow adding method implementations without breaking existing implementers. The key difference is state: interfaces cannot have instance fields (all fields are public static final) or constructors, while abstract classes can maintain mutable instance state with constructors. Also, a class can implement multiple interfaces but extend only one abstract class.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Default methods allow interface evolution with backward compatibility", "Interfaces cannot have instance state or constructors", "Abstract classes maintain mutable instance fields and constructors", "Multiple inheritance of interfaces vs single inheritance of abstract classes"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Diamond conflict resolution rules in interface default methods", "When to choose abstract class vs interface"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly identified instance state and constructor differences."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Highlighted multiple vs single inheritance trade-off."}
                    ],
                    "citations": [{"claim": "An interface cannot hold instance state (no instance fields... while an abstract class can maintain mutable instance state via instance variables and constructors", "source_number": 1}],
                    "reasoning": "Clear, precise explanation of state, constructors, and multiple inheritance."
                }
            },
            {
                "answer": "Java 8 me default methods aane ke baad interface aur abstract class bilkul same ban gaye hain, bas interface me multiple inheritance allow hoti hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Interfaces allow multiple inheritance", "Default methods provide implementation in interfaces"],
                    "missing_core_concepts": ["Interfaces cannot hold mutable instance state or constructors", "Abstract classes can have stateful fields and constructors"],
                    "deeper_concepts_to_probe": ["Instance variables in abstract class vs constants in interface"],
                    "misconceptions": ["Believing interfaces and abstract classes became completely identical"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Captured method implementation and multiple inheritance, but failed on instance state."}
                    ],
                    "citations": [{"claim": "An interface cannot hold instance state (no instance fields... while an abstract class can maintain mutable instance state", "source_number": 1}],
                    "reasoning": "Missed the crucial distinction of instance state and constructors."
                }
            },
            {
                "answer": "Default methods are private methods that can only be called inside the interface itself, so outside classes cannot access them.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Default methods are public by default and designed to be inherited and called by implementing classes"],
                    "deeper_concepts_to_probe": ["Interface method access modifiers in Java 8 and 9"],
                    "misconceptions": ["Believing default methods are private and inaccessible"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Inverted the access visibility of default methods."}
                    ],
                    "citations": [{"claim": "default methods to interfaces which allows developers to add new methods to existing interfaces without breaking compatibility", "source_number": 1}],
                    "reasoning": "Completely incorrect definition of default method accessibility."
                }
            }
        ]
    }
]
