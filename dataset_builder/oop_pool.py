"""
OOP Question Pool: 8 Questions x 3 Samples = 24 Samples.
Coverage:
OOP_01: 4 Pillars of OOP
OOP_02: Inheritance vs Composition
OOP_03: Abstract Class vs Interface
OOP_04: Method Overloading vs Method Overriding
OOP_05: Coupling vs Cohesion
OOP_06: The Diamond Problem in Multiple Inheritance
OOP_07: Static Binding vs Dynamic Binding
OOP_08: Liskov Substitution Principle (LSP)
"""

OOP_POOL = [
    {
        "question_id": "OOP_01",
        "subject": "OOP",
        "question": "What are the four main principles of object-oriented programming, and can you briefly describe each one?",
        "reference": "[1] The four core principles of OOP are: Encapsulation (bundling data and methods into a single unit and restricting direct access using access modifiers), Abstraction (hiding internal implementation details and exposing only essential interface features), Inheritance (enabling a class to derive state and behavior from a base class), and Polymorphism (the ability of a single interface to represent different underlying forms/implementations).",
        "samples": [
            {
                "answer": "The four main pillars are Encapsulation, Abstraction, Inheritance, and Polymorphism. Encapsulation bundles data and methods while restricting direct field access via private variables and getters/setters. Abstraction hides complexity and reveals only essential behavior via interfaces or abstract classes. Inheritance allows a subclass to reuse properties and methods of a parent class. Polymorphism allows a method to take many forms, either via compile-time overloading or runtime overriding.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Encapsulation bundles data/methods and restricts direct access", "Abstraction hides internal implementation details", "Inheritance allows code reuse from base to derived class", "Polymorphism enables one interface to have multiple implementations"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Difference between abstraction (design level) and encapsulation (implementation level)", "Dynamic dispatch vtable mechanics"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately defined all four OOP pillars with appropriate programming mechanisms."}
                    ],
                    "citations": [{"claim": "Encapsulation... Abstraction... Inheritance... and Polymorphism", "source_number": 1}],
                    "reasoning": "Comprehensive, textbook-accurate explanation of all four OOP pillars."
                }
            },
            {
                "answer": "Char pillars hote hain: Encapsulation, Abstraction, Inheritance, Polymorphism. Inheritance se code reuse hota hai aur Polymorphism se functions ke alag forms bante hain. Encapsulation aur Abstraction dono ka matlab data hide karna hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Named all four pillars correctly", "Inheritance enables code reuse", "Polymorphism enables multiple forms"],
                    "missing_core_concepts": ["Distinction between Abstraction (hiding implementation complexity) and Encapsulation (data hiding & bundling)"],
                    "deeper_concepts_to_probe": ["Abstraction vs Encapsulation distinction"],
                    "misconceptions": ["Conflating Encapsulation and Abstraction as identical concepts of data hiding"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Listed all four pillars but merged encapsulation and abstraction definitions."}
                    ],
                    "citations": [{"claim": "Encapsulation (bundling data and methods... restricting direct access)... Abstraction (hiding internal implementation details)", "source_number": 1}],
                    "reasoning": "Good recall of four pillars, but conflated encapsulation with abstraction."
                }
            },
            {
                "answer": "The four pillars are Compilation, Interpretation, Garbage Collection, and Object creation.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["The four pillars are Encapsulation, Abstraction, Inheritance, Polymorphism"],
                    "deeper_concepts_to_probe": ["Core OOP paradigms"],
                    "misconceptions": ["Confusing runtime execution concepts with object-oriented paradigms"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Did not name a single OOP pillar."}
                    ],
                    "citations": [{"claim": "The four core principles of OOP are: Encapsulation... Abstraction... Inheritance... and Polymorphism", "source_number": 1}],
                    "reasoning": "Completely incorrect answer listing JVM lifecycle concepts instead of OOP principles."
                }
            }
        ]
    },
    {
        "question_id": "OOP_02",
        "subject": "OOP",
        "question": "What is the difference between Inheritance and Composition in object-oriented design, and why is composition often favored?",
        "reference": "[1] Inheritance represents an 'is-a' relationship where a subclass tightly couples to its superclass implementation, creating a fragile base class problem where changes in parent break children. Composition represents a 'has-a' relationship where an object contains instances of other classes to delegate behavior, enabling loose coupling, runtime flexibility (polymorphic swapping), and easier unit testing ('Favor composition over inheritance').",
        "samples": [
            {
                "answer": "Inheritance is an 'is-a' relationship that tightly couples a subclass to its parent class, which can lead to fragile base classes. Composition is a 'has-a' relationship where a class holds references to other objects and delegates tasks to them. Composition is favored because it achieves loose coupling, allows changing behavior at runtime, and prevents exposing internal superclass methods unnecessarily.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Inheritance is 'is-a' and creates tight coupling", "Composition is 'has-a' and delegates behavior", "Composition avoids the fragile base class problem", "Composition allows dynamic runtime swapping and loose coupling"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Dependency Injection as an application of composition", "Design patterns based on composition (Strategy, Decorator)"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly differentiated 'is-a' from 'has-a'."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Articulated tight coupling and fragile base class risks of inheritance."}
                    ],
                    "citations": [{"claim": "Inheritance represents an 'is-a' relationship... Composition represents a 'has-a' relationship... enabling loose coupling, runtime flexibility", "source_number": 1}],
                    "reasoning": "Clear, precise explanation of coupling, design relationships, and runtime flexibility."
                }
            },
            {
                "answer": "Inheritance me child class parent class ko extend karti hai. Composition me class ke andar doosri class ka object banate hain. Composition isliye acchi hai kyunki multiple inheritance allow karti hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Inheritance extends parent class", "Composition embeds another class's object"],
                    "missing_core_concepts": ["Tight coupling vs loose coupling", "Fragile base class problem"],
                    "deeper_concepts_to_probe": ["Behavior delegation at runtime"],
                    "misconceptions": ["Framing composition merely as a workaround for multiple inheritance rather than an architectural coupling choice"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Understood the structural implementation difference."},
                        {"evidence_type": "REASONING", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Did not articulate coupling issues."}
                    ],
                    "citations": [{"claim": "Composition represents a 'has-a' relationship... enabling loose coupling, runtime flexibility", "source_number": 1}],
                    "reasoning": "Understood basic syntax difference but lacked architectural depth on coupling and delegation."
                }
            },
            {
                "answer": "Inheritance is always faster and better than composition because composition wastes memory by creating duplicate pointers, so inheritance is always preferred.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["'Favor composition over inheritance' is a core OOP guideline", "Inheritance introduces tight coupling and rigid hierarchies"],
                    "deeper_concepts_to_probe": ["Coupling and cohesion"],
                    "misconceptions": ["Believing inheritance is universally superior to composition", "Claiming composition is avoided due to pointer overhead"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Inverted standard design principles."}
                    ],
                    "citations": [{"claim": "Favor composition over inheritance", "source_number": 1}],
                    "reasoning": "Contradicts established software design principles."
                }
            }
        ]
    },
    {
        "question_id": "OOP_03",
        "subject": "OOP",
        "question": "What is the difference between an Abstract Class and an Interface in object-oriented design?",
        "reference": "[1] In object-oriented design: An abstract class defines a common base identity ('is-a') that can hold mutable instance state, constructors, and partial method implementations. An interface defines a contractual capability or behavior ('can-do') without instance state. A class can extend only one abstract class but can implement multiple interfaces.",
        "samples": [
            {
                "answer": "An abstract class represents an 'is-a' hierarchy and can have instance variables, constructors, and default concrete methods. An interface represents a 'can-do' contract that defines capabilities without maintaining instance state. In single-inheritance languages like Java or C#, a class can only extend one abstract class but can implement multiple interfaces.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Abstract class represents 'is-a' identity with instance state and constructors", "Interface represents 'can-do' behavioral contract without state", "Multiple interfaces can be implemented whereas only one abstract class can be extended"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["When to choose an abstract class vs an interface", "Interface evolution with default methods"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clearly articulated state, constructor, and inheritance distinctions."}
                    ],
                    "citations": [{"claim": "An abstract class defines a common base identity... can hold mutable instance state... An interface defines a contractual capability", "source_number": 1}],
                    "reasoning": "Thorough, technically accurate comparison of abstract classes and interfaces."
                }
            },
            {
                "answer": "Abstract class me abstract aur concrete dono methods ho sakte hain, interface me pehle sirf abstract hote the. Abstract class me constructor hota hai interface me nahi hota.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 7,
                    "depth_score": 5,
                    "correct_points": ["Abstract class can have both abstract and concrete methods", "Abstract class has constructors while interface does not"],
                    "missing_core_concepts": ["'is-a' identity vs 'can-do' capability contract", "Single vs multiple inheritance limitations"],
                    "deeper_concepts_to_probe": ["Statefulness: instance variables in abstract class"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurate on method types and constructors."},
                        {"evidence_type": "REASONING", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Missed design level is-a vs can-do intent."}
                    ],
                    "citations": [{"claim": "An abstract class defines a common base identity... An interface defines a contractual capability", "source_number": 1}],
                    "reasoning": "Good technical recall of syntax differences, but lacked higher-level architectural design rationale."
                }
            },
            {
                "answer": "Abstract class can be instantiated directly using new keyword, but Interface cannot be instantiated.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": ["Interface cannot be instantiated directly"],
                    "missing_core_concepts": ["Neither abstract classes nor interfaces can be instantiated directly"],
                    "deeper_concepts_to_probe": ["Abstract types instantiation rules"],
                    "misconceptions": ["Believing an abstract class can be directly instantiated with 'new'"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Directly violated abstract class definition."}
                    ],
                    "citations": [{"claim": "An abstract class defines a common base identity... cannot be instantiated directly", "source_number": 1}],
                    "reasoning": "Claiming abstract classes can be directly instantiated is a fundamental error."
                }
            }
        ]
    },
    {
        "question_id": "OOP_04",
        "subject": "OOP",
        "question": "What is the difference between Method Overloading and Method Overriding in OOP, and when is each resolved?",
        "reference": "[1] Method Overloading occurs when multiple methods in the same class share the same name but differ in parameter list (count, types, or order); it is resolved at compile-time (static polymorphism / early binding). Method Overriding occurs when a subclass redefines a method inherited from a superclass with identical signature and return type; it is resolved at runtime (dynamic polymorphism / late binding via virtual method table dispatch).",
        "samples": [
            {
                "answer": "Method overloading happens within the same class when methods share the same name but have different parameter lists; it is resolved at compile time based on reference types. Method overriding happens between a parent and child class where the child redefines an inherited method with identical signature; it is resolved at runtime based on the actual object instance via dynamic dispatch.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Overloading: same name, different parameters in same class, compile-time resolution", "Overriding: identical signature between superclass and subclass, runtime resolution via dynamic dispatch", "Overloading is static polymorphism; overriding is dynamic polymorphism"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Covariant return types in overriding", "vtable / virtual dispatch mechanism"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Precisely distinguished compile-time vs runtime binding."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Specified parameter requirements vs identical signature requirements."}
                    ],
                    "citations": [{"claim": "Method Overloading... resolved at compile-time... Method Overriding... resolved at runtime (dynamic polymorphism)", "source_number": 1}],
                    "reasoning": "Clear, precise explanation of polymorphism, signatures, and resolution timing."
                }
            },
            {
                "answer": "Overloading me same function name hota hai alag parameters ke sath. Overriding me child class parent ke method ko replace karti hai. Dono runtime pe check hote hain.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Overloading has same name and different parameters", "Overriding redefines parent method in child class"],
                    "missing_core_concepts": ["Overloading is resolved at compile time, not runtime"],
                    "deeper_concepts_to_probe": ["Early vs late binding"],
                    "misconceptions": ["Believing method overloading is resolved at runtime"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Correct on definitions, but wrong on binding time for overloading."}
                    ],
                    "citations": [{"claim": "Method Overloading... is resolved at compile-time (static polymorphism)", "source_number": 1}],
                    "reasoning": "Understood the syntactic definition but incorrectly claimed both are checked at runtime."
                }
            },
            {
                "answer": "Overloading and Overriding are identical, only in C++ it is called Overloading and in Java it is called Overriding.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Overloading is static compile-time polymorphism; Overriding is dynamic runtime polymorphism; both exist in both C++ and Java"],
                    "deeper_concepts_to_probe": ["Object-oriented polymorphism"],
                    "misconceptions": ["Believing overloading and overriding are just language-specific synonyms"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete failure to distinguish two fundamental concepts."}
                    ],
                    "citations": [{"claim": "Method Overloading occurs when multiple methods... differ in parameter list... Method Overriding occurs when a subclass redefines", "source_number": 1}],
                    "reasoning": "Bizarre misconception equating two entirely different OOP concepts as language aliases."
                }
            }
        ]
    },
    {
        "question_id": "OOP_05",
        "subject": "OOP",
        "question": "What is the difference between Coupling and Cohesion in software design, and why do we aim for loose coupling and high cohesion?",
        "reference": "[1] In software engineering: Cohesion measures how strongly related and focused the responsibilities of a single module or class are (High Cohesion = class does one thing well, adhering to Single Responsibility). Coupling measures the degree of interdependence between different modules (Loose Coupling = modules interact through clean, minimal interfaces). Good software aims for high cohesion and loose coupling to maximize maintainability, testability, and code reusability.",
        "samples": [
            {
                "answer": "Cohesion refers to how focused a single module's responsibilities are; high cohesion means a class has one well-defined purpose, aligning with the Single Responsibility Principle. Coupling refers to the degree of dependency between different classes; loose coupling means changes in one class don't break others because they interact via interfaces. We aim for high cohesion and loose coupling to make systems maintainable, reusable, and easy to test.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Cohesion is internal focus of a module's responsibilities", "Coupling is external interdependence between modules", "High cohesion satisfies Single Responsibility Principle", "Loose coupling isolates changes, improving testability and maintainability"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Dependency Inversion as a tool for loose coupling", "Law of Demeter"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately distinguished intra-module cohesion from inter-module coupling."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained maintainability and testing benefits."}
                    ],
                    "citations": [{"claim": "Cohesion measures how strongly related and focused... Coupling measures the degree of interdependence between different modules", "source_number": 1}],
                    "reasoning": "Flawless technical distinction and clear rationale for modular software design."
                }
            },
            {
                "answer": "Coupling matlab do classes ke beech connection, jo kam hona chahiye. Cohesion matlab code kitna chhota hai. Agar code chhota hai to cohesion high hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["Coupling is the connection between classes and should be minimized"],
                    "missing_core_concepts": ["Cohesion is the functional relatedness of responsibilities, not line count or code size"],
                    "deeper_concepts_to_probe": ["Single Responsibility Principle"],
                    "misconceptions": ["Equating cohesion with lines of code or brevity"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood loose coupling but misunderstood cohesion as code brevity."}
                    ],
                    "citations": [{"claim": "Cohesion measures how strongly related and focused the responsibilities of a single module or class are", "source_number": 1}],
                    "reasoning": "Correct understanding of coupling, but completely misunderstood cohesion as brevity instead of focused responsibility."
                }
            },
            {
                "answer": "Coupling means functions inside the class are grouped together, and cohesion means the database is connected to the backend.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Coupling is inter-module dependency; Cohesion is intra-module responsibility focus"],
                    "deeper_concepts_to_probe": ["Software architectural metrics"],
                    "misconceptions": ["Confusing cohesion with database connectivity and swapping coupling definitions"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Inaccurate definitions with arbitrary database associations."}
                    ],
                    "citations": [{"claim": "Cohesion measures how strongly related... Coupling measures the degree of interdependence", "source_number": 1}],
                    "reasoning": "Inverted and inaccurate definitions."
                }
            }
        ]
    },
    {
        "question_id": "OOP_06",
        "subject": "OOP",
        "question": "What is the Diamond Problem in multiple inheritance, and how do languages like C++ or Java handle or avoid it?",
        "reference": "[1] The Diamond Problem arises in multiple inheritance when a class D inherits from two classes B and C, which both inherit from a common base class A. If A has a method overridden by both B and C, ambiguity arises over which implementation D inherits. C++ resolves this using virtual inheritance (virtual base classes) so only one instance of A is shared. Java avoids it entirely by disallowing multiple class inheritance, and resolves interface default method diamond conflicts by forcing class D to explicitly override and disambiguate.",
        "samples": [
            {
                "answer": "The Diamond Problem occurs when class D inherits from B and C, which both inherit from A. If B and C override a method from A, D faces ambiguity on which version to call. C++ solves this using 'virtual inheritance' so only one subobject of A exists. Java avoids it by disallowing multiple inheritance of classes; for interface default methods with diamond conflicts, Java forces the implementing class to explicitly override the method and specify the desired parent with SuperInterface.super.method().",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Describes diamond inheritance hierarchy A->B,C->D", "Ambiguity occurs when B and C override methods from base A", "C++ resolves via virtual inheritance", "Java disallows multiple class inheritance and forces explicit override for interface default method conflicts"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["vtable layout with virtual base pointers in C++", "Python C3 linearization MRO"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately sketched the diamond ambiguity scenario."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Correctly detailed both C++ virtual base classes and Java interface disambiguation."}
                    ],
                    "citations": [{"claim": "The Diamond Problem arises in multiple inheritance... C++ resolves this using virtual inheritance... Java avoids it entirely by disallowing multiple class inheritance", "source_number": 1}],
                    "reasoning": "Accurate, well-structured explanation of ambiguity and language-specific resolution strategies."
                }
            },
            {
                "answer": "Diamond problem multiple inheritance me hota hai jab do parents ka same method hota hai aur child confuse ho jata hai kaunsa call kare. Java me multiple inheritance nahi hoti isliye ye problem kabhi nahi aati.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Understands ambiguity in multiple inheritance when two parents have the same method", "Java avoids multiple class inheritance"],
                    "missing_core_concepts": ["Hierarchy specifically involves a shared base class A (diamond shape)", "How Java 8 handles interface default method diamond conflicts", "How C++ resolves it with virtual inheritance"],
                    "deeper_concepts_to_probe": ["Interface default method diamond conflict"],
                    "misconceptions": ["Believing diamond problem is impossible in Java (ignoring interface default methods)"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Captured general multiple inheritance collision but missed diamond hierarchy specifics and modern Java default methods."}
                    ],
                    "citations": [{"claim": "Java avoids it entirely by disallowing multiple class inheritance, and resolves interface default method diamond conflicts by forcing class D to explicitly override", "source_number": 1}],
                    "reasoning": "Understood the basic conflict, but lacked depth on shared root class A, C++ virtual inheritance, and Java interface default method conflicts."
                }
            },
            {
                "answer": "The diamond problem is a database deadlock issue where 4 tables lock each other in a diamond shape.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Diamond problem is an OOP multiple inheritance ambiguity problem, not a database deadlock"],
                    "deeper_concepts_to_probe": ["Multiple inheritance in OOP"],
                    "misconceptions": ["Confusing OOP inheritance with database locking"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Complete subject category mismatch."}
                    ],
                    "citations": [{"claim": "The Diamond Problem arises in multiple inheritance when a class D inherits from two classes B and C", "source_number": 1}],
                    "reasoning": "Incorrectly mapped an OOP inheritance concept to database deadlocks."
                }
            }
        ]
    },
    {
        "question_id": "OOP_07",
        "subject": "OOP",
        "question": "What is the difference between Static Binding (Early Binding) and Dynamic Binding (Late Binding) in OOP?",
        "reference": "[1] Static Binding (Early Binding) occurs at compile-time when the compiler binds the method call directly to the bytecode address based on the reference type; in Java/C++, this applies to private, static, final methods, and overloaded methods. Dynamic Binding (Late Binding) occurs at runtime when the call is resolved based on the actual runtime object instance using a virtual method table (vtable), which enables method overriding and runtime polymorphism.",
        "samples": [
            {
                "answer": "Static binding (early binding) occurs at compile-time where the method to execute is determined based on the variable's reference type. It applies to static, private, and final methods, as well as overloaded methods. Dynamic binding (late binding) occurs at runtime where the method call is resolved based on the actual runtime object instance using a virtual method table (vtable), which enables method overriding.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Static binding occurs at compile-time based on reference type", "Applies to static, private, final, and overloaded methods", "Dynamic binding occurs at runtime based on actual object instance", "Uses virtual method table (vtable) to support overriding"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Performance difference between direct jump and vtable dereferencing", "JIT inlining of monomorphic call sites"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clearly articulated compile-time vs runtime binding mechanics."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Associated static binding with final/static/private and dynamic binding with vtable overriding."}
                    ],
                    "citations": [{"claim": "Static Binding (Early Binding) occurs at compile-time... Dynamic Binding (Late Binding) occurs at runtime... using a virtual method table (vtable)", "source_number": 1}],
                    "reasoning": "Flawless, comprehensive explanation of binding mechanisms in OOP."
                }
            },
            {
                "answer": "Static binding compile time pe hoti hai aur dynamic binding runtime pe hoti hai. Static binding me static keyword lagana padta hai har function pe.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["Static binding happens at compile time", "Dynamic binding happens at runtime"],
                    "missing_core_concepts": ["Static binding also applies to private, final, and overloaded methods without static keyword", "Dynamic binding relies on vtable for overridden methods"],
                    "deeper_concepts_to_probe": ["Virtual method dispatch"],
                    "misconceptions": ["Believing static binding requires the static keyword on every method"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Got timing right but confused method modifiers."}
                    ],
                    "citations": [{"claim": "this applies to private, static, final methods, and overloaded methods", "source_number": 1}],
                    "reasoning": "Correctly identified timing, but mistakenly claimed all statically bound methods must be declared with 'static'."
                }
            },
            {
                "answer": "Static binding is used for frontend HTML and dynamic binding is used when connecting with Python backend.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Static vs dynamic binding refers to compile-time vs runtime method resolution in OOP"],
                    "deeper_concepts_to_probe": ["OOP method invocation"],
                    "misconceptions": ["Confusing method binding with full-stack web integration"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Completely irrelevant web dev analogy."}
                    ],
                    "citations": [{"claim": "Static Binding (Early Binding) occurs at compile-time... Dynamic Binding (Late Binding) occurs at runtime", "source_number": 1}],
                    "reasoning": "Totally incorrect mapping to web architecture."
                }
            }
        ]
    },
    {
        "question_id": "OOP_08",
        "subject": "OOP",
        "question": "What is the Liskov Substitution Principle (LSP) in SOLID design, and what is an example of a design violation?",
        "reference": "[1] The Liskov Substitution Principle (LSP) states that objects of a superclass should be replaceable with objects of its subclasses without altering the correctness or desirable properties of the program. A classic violation is the Square-Rectangle problem: a Square inherits from Rectangle, but overriding setWidth() to modify height violates the caller's expectation that changing width leaves height unchanged, breaking behavioral subtyping.",
        "samples": [
            {
                "answer": "LSP states that any subclass should be substitutable for its superclass without breaking client expectations or program correctness. A classic violation is the Rectangle and Square problem: if Square extends Rectangle, setting the width will also change the height to keep it square. Any code expecting a standard Rectangle will fail when changing width unexpectedly alters height, violating behavioral subtyping.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Subclasses must be substitutable for superclasses without breaking correctness", "Preserves behavioral subtyping and contracts", "Accurately illustrated with the classic Square-Rectangle violation"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Preconditions cannot be strengthened and postconditions cannot be weakened", "Design by Contract"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately stated the substitutability definition."},
                        {"evidence_type": "APPLICATION", "status": "DEMONSTRATED", "evidence_from_answer": "Provided the classic Square-Rectangle violation showing how contract assumptions fail."}
                    ],
                    "citations": [{"claim": "objects of a superclass should be replaceable with objects of its subclasses without altering the correctness... Square-Rectangle problem", "source_number": 1}],
                    "reasoning": "Clear, precise understanding of behavioral subtyping with an exemplary classic scenario."
                }
            },
            {
                "answer": "LSP matlab child class me parent ke saare methods hone chahiye taaki code compile ho sake. Agar child class me parent ka ek method miss ho gaya to LSP violate hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["Recognizes that child classes inherit parent methods"],
                    "missing_core_concepts": ["LSP is about behavioral contract preservation, not just syntax compilation", "Subclass must satisfy caller invariants without throwing unexpected exceptions"],
                    "deeper_concepts_to_probe": ["Behavioral subtyping vs syntactic inheritance"],
                    "misconceptions": ["Believing LSP is just about compiler method inheritance rather than behavioral semantics"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Confused syntactic method presence with semantic behavioral substitutability."}
                    ],
                    "citations": [{"claim": "objects of a superclass should be replaceable with objects of its subclasses without altering the correctness or desirable properties", "source_number": 1}],
                    "reasoning": "Confused compile-time signature inheritance with behavioral subtyping contracts."
                }
            },
            {
                "answer": "Liskov principle says that every class must have a main method and private constructor so no one can create objects.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["LSP governs substitutability of derived classes for base classes"],
                    "deeper_concepts_to_probe": ["SOLID principles"],
                    "misconceptions": ["Believing LSP is about singleton private constructors"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Completely detached from SOLID principles."}
                    ],
                    "citations": [{"claim": "The Liskov Substitution Principle (LSP) states that objects of a superclass should be replaceable", "source_number": 1}],
                    "reasoning": "Purely nonsensical claim unrelated to LSP."
                }
            }
        ]
    }
]
