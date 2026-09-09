"""
Which concepts the knowledge base should cover.

This is the ONLY file you edit to add a new topic. Add the Wikipedia
article title to the right subject and re-run corpus_fetcher.py.

The interview topic the candidate types is matched against these
subject names, so keep the keys close to what people actually type
("OOP", "DBMS", "Java").
"""

TOPICS = {

    "OOP": [
        "Object-oriented programming",
        "Class (computer programming)",
        "Object (computer science)",
        "Inheritance (object-oriented programming)",
        "Polymorphism (computer science)",
        "Encapsulation (computer programming)",
        "Abstraction (computer science)",
        "Method overriding",
        "Constructor (object-oriented programming)",
        "Interface (object-oriented programming)",
        "Composition over inheritance",
        "SOLID",
    ],

    "JAVA": [
        "Java (programming language)",
        "Java virtual machine",
        "Java Class Library",
        "Garbage collection (computer science)",
        "String interning",
        "Java syntax",
        "Exception handling",
        "Java collections framework",
        "Autoboxing",
        "Immutable object",
    ],

    "DBMS": [
        "Database",
        "Relational database",
        "Database normalization",
        "SQL",
        "Database index",
        "Database transaction",
        "ACID",
        "Isolation (database systems)",
        "Foreign key",
        "Join (SQL)",
        "Database schema",
        "Query optimization",
    ],

    "OS": [
        "Operating system",
        "Process (computing)",
        "Thread (computing)",
        "Scheduling (computing)",
        "Deadlock",
        "Virtual memory",
        "Paging",
        "Semaphore (programming)",
        "Mutual exclusion",
        "Context switch",
        "File system",
        "Interrupt",
    ],

    "CN": [
        "Computer network",
        "OSI model",
        "Internet protocol suite",
        "Transmission Control Protocol",
        "User Datagram Protocol",
        "Domain Name System",
        "Hypertext Transfer Protocol",
        "IP address",
        "Routing",
        "Network switch",
        "Transport Layer Security",
        "Subnetwork",
    ],

    "DSA": [
        "Data structure",
        "Algorithm",
        "Array (data structure)",
        "Linked list",
        "Stack (abstract data type)",
        "Queue (abstract data type)",
        "Hash table",
        "Binary search tree",
        "Graph (abstract data type)",
        "Sorting algorithm",
        "Big O notation",
        "Dynamic programming",
        "Recursion (computer science)",
    ],
}


def all_articles():
    """Every (subject, article) pair, flattened."""

    pairs = []

    for subject, articles in TOPICS.items():
        for article in articles:
            pairs.append((subject, article))

    return pairs
