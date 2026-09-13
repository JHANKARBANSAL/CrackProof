"""
DBMS Question Pool: 8 Questions x 3 Samples = 24 Samples.
Coverage:
DBMS_01: ACID properties in database transactions
DBMS_02: Primary Key vs Unique Key vs Foreign Key
DBMS_03: Clustered Index vs Non-Clustered Index
DBMS_04: Database Normalization (1NF, 2NF, 3NF)
DBMS_05: SQL vs NoSQL architectural trade-offs
DBMS_06: Transaction Isolation Levels & Concurrency Anomalies
DBMS_07: INNER JOIN vs LEFT JOIN vs FULL OUTER JOIN
DBMS_08: WHERE clause vs HAVING clause execution
"""

DBMS_POOL = [
    {
        "question_id": "DBMS_01",
        "subject": "DBMS",
        "question": "What are the ACID properties in database transactions, and why is each property essential?",
        "reference": "[1] In relational databases, ACID guarantees reliable transaction processing: Atomicity ('all or nothing' execution via write-ahead logging/rollback), Consistency (transactions transition database from one valid state to another satisfying all schema constraints), Isolation (concurrent transactions execute independently without interference, controlled by isolation levels), and Durability (committed changes persist permanently even through power failure or system crash, backed by non-volatile storage logs).",
        "samples": [
            {
                "answer": "ACID stands for Atomicity, Consistency, Isolation, and Durability. Atomicity means all operations in a transaction succeed or all rollback ('all-or-nothing'). Consistency ensures the database transitions between valid states adhering to constraints. Isolation prevents concurrent transactions from interfering with each other's uncommitted data. Durability guarantees that once committed, data is permanently recorded on disk and survives crashes.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Atomicity ensures all-or-nothing execution with rollback", "Consistency enforces transition between valid states satisfying constraints", "Isolation prevents concurrent transaction anomalies", "Durability guarantees committed data survives crashes via non-volatile storage"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Write-Ahead Logging (WAL) for durability and atomicity", "Trade-off between high isolation levels and concurrency throughput"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately defined all four ACID properties."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Articulated why each property is necessary for reliable data transactions."}
                    ],
                    "citations": [{"claim": "Atomicity ('all or nothing')... Consistency (valid state)... Isolation (concurrent transactions)... Durability (persist permanently)", "source_number": 1}],
                    "reasoning": "Clear, precise explanation of all four ACID properties and their roles in transactional reliability."
                }
            },
            {
                "answer": "ACID properties transactions ke liye hoti hain. Atomicity ka matlab transaction complete ho ya bilkul na ho. Consistency matlab data consistent rahe. Durability matlab data jaldi delete na ho. Isolation ka exact idea nahi hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["Atomicity is all-or-nothing execution", "Durability ensures data persists"],
                    "missing_core_concepts": ["Isolation prevents concurrent transaction interference", "Consistency specifically enforces schema and integrity constraints"],
                    "deeper_concepts_to_probe": ["Concurrency control and isolation levels"],
                    "misconceptions": ["Vague definition of durability as 'not quickly deleted' rather than crash resilience"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood atomicity, but missed isolation and gave superficial definition for durability."}
                    ],
                    "citations": [{"claim": "Isolation (concurrent transactions execute independently without interference)... Durability (committed changes persist permanently even through power failure)", "source_number": 1}],
                    "reasoning": "Understood atomicity well, but omitted isolation and lacked technical precision on durability."
                }
            },
            {
                "answer": "ACID stands for Accuracy, Completeness, Integration, and Data. It means the database must have fast search and no duplicate primary keys.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["ACID stands for Atomicity, Consistency, Isolation, Durability"],
                    "deeper_concepts_to_probe": ["Database transaction fundamentals"],
                    "misconceptions": ["Fabricated incorrect terms for the ACID acronym"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Completely invented terms for the acronym."}
                    ],
                    "citations": [{"claim": "ACID guarantees reliable transaction processing: Atomicity... Consistency... Isolation... and Durability", "source_number": 1}],
                    "reasoning": "Completely incorrect acronym expansion and explanation."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_02",
        "subject": "DBMS",
        "question": "What is the difference between a Primary Key, Unique Key, and Foreign Key in relational databases?",
        "reference": "[1] In relational databases: A Primary Key uniquely identifies each row in a table, disallowing NULL values (strictly one primary key per table, typically default clustered index). A Unique Key also enforces uniqueness across columns but permits one or more NULL values (depending on SQL dialect), and multiple unique keys can exist on a table. A Foreign Key is a referential constraint pointing to a primary or unique key in another table, ensuring referential integrity.",
        "samples": [
            {
                "answer": "A Primary Key uniquely identifies each record in a table and cannot contain NULL values; each table can only have one primary key. A Unique Key also guarantees uniqueness, but it allows NULL values (one NULL in standard SQL), and a table can have multiple unique keys. A Foreign Key creates a relationship by referencing the primary or unique key of another table, ensuring referential integrity across related data.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Primary key enforces uniqueness and forbids NULL values", "Only one primary key per table", "Unique key enforces uniqueness, permits NULLs, and multiple can exist per table", "Foreign key references primary/unique key in parent table for referential integrity"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["ON DELETE CASCADE and ON UPDATE CASCADE behaviors in foreign keys", "Clustered index default on primary key"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted NULL constraints, quantity limits, and relational linking."}
                    ],
                    "citations": [{"claim": "Primary Key uniquely identifies each row... disallowing NULL values... Unique Key... permits NULL values... Foreign Key is a referential constraint", "source_number": 1}],
                    "reasoning": "Clear, precise differentiation between all three key types and their integrity roles."
                }
            },
            {
                "answer": "Primary key unique hoti hai aur null nahi ho sakti. Unique key bhi unique hoti hai par usme null aa sakta hai. Foreign key doosri table se data copy karne ke liye hoti hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Primary key is unique and cannot be null", "Unique key allows null"],
                    "missing_core_concepts": ["Quantity limit: exactly one primary key vs multiple unique keys", "Foreign key enforces referential integrity, not data copying"],
                    "deeper_concepts_to_probe": ["Referential integrity constraints"],
                    "misconceptions": ["Believing foreign key copies data rather than establishing referential constraint"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Accurately defined Primary and Unique keys, but misunderstood foreign key as data copying."}
                    ],
                    "citations": [{"claim": "Foreign Key is a referential constraint pointing to a primary or unique key in another table, ensuring referential integrity", "source_number": 1}],
                    "reasoning": "Primary and unique keys described well, but foreign key was misrepresented as data copying rather than referential integrity constraint."
                }
            },
            {
                "answer": "Primary key and unique key are identical with no difference, and foreign key is used when the database is hosted in another country.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Primary key forbids NULLs, unique key allows NULLs", "Foreign key enforces relational integrity between tables, not geographic location"],
                    "deeper_concepts_to_probe": ["Relational key constraints"],
                    "misconceptions": ["Believing primary and unique keys are identical", "Believing foreign key refers to geographical hosting"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Humorous but completely incorrect misconception regarding foreign keys."}
                    ],
                    "citations": [{"claim": "A Primary Key uniquely identifies... A Unique Key... permits one or more NULL values... A Foreign Key is a referential constraint", "source_number": 1}],
                    "reasoning": "Factually erroneous and demonstrates no understanding of relational keys."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_03",
        "subject": "DBMS",
        "question": "What is the difference between a Clustered Index and a Non-Clustered Index in a relational database?",
        "reference": "[1] In relational databases: A Clustered Index dictates the actual physical order of data rows on disk; the leaf nodes contain the actual data pages (table can have only ONE clustered index). A Non-Clustered Index is a separate B-tree structure whose leaf nodes contain index keys and row pointers (clustering key or RID) that point to the physical data rows, allowing multiple non-clustered indexes per table.",
        "samples": [
            {
                "answer": "A clustered index determines the physical order of data stored on disk; because data can only be physically sorted one way, a table can have only one clustered index, and its leaf nodes are the actual data pages. A non-clustered index is a separate structure where leaf nodes store the index keys and row locators (pointers to the actual data). You can have multiple non-clustered indexes on a single table.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Clustered index physically sorts data rows on disk", "Only one clustered index per table", "Leaf nodes of clustered index contain actual table data pages", "Non-clustered index is a separate structure with pointers to rows", "Multiple non-clustered indexes per table"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Index lookup overhead (bookmark lookup / key lookup)", "Covering index to avoid row lookups"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clearly articulated physical storage versus separate pointer B-tree."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained why only one clustered index can exist (data can only be sorted one way on disk)."}
                    ],
                    "citations": [{"claim": "Clustered Index dictates the actual physical order... leaf nodes contain the actual data pages... Non-Clustered Index is a separate B-tree structure whose leaf nodes contain index keys and row pointers", "source_number": 1}],
                    "reasoning": "Comprehensive, technically precise explanation of physical storage and index structures."
                }
            },
            {
                "answer": "Clustered index table me ek hi ho sakta hai kyunki wo primary key pe banta hai. Non-clustered index kitne bhi bana sakte hain. Clustered index fast hota hai aur non-clustered thoda slow hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Only one clustered index per table", "Multiple non-clustered indexes allowed", "Clustered index avoids pointer lookups making it faster for ranges"],
                    "missing_core_concepts": ["Physical storage ordering on disk", "Leaf nodes contain data pages vs leaf nodes contain row pointers"],
                    "deeper_concepts_to_probe": ["Physical data layout on storage pages"],
                    "misconceptions": ["Assuming clustered index must always be on primary key (it defaults to PK, but can be on any column)"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Captured count limitation and general performance but missed physical disk layout."}
                    ],
                    "citations": [{"claim": "A Clustered Index dictates the actual physical order of data rows on disk... leaf nodes contain index keys and row pointers", "source_number": 1}],
                    "reasoning": "Understood the count constraint and performance difference, but missed physical disk organization."
                }
            },
            {
                "answer": "Clustered index means all tables in the database are merged into a cluster, while non-clustered means tables are kept in separate folders on the computer.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Clustered and non-clustered indexes are B-tree structures within a single table for fast row retrieval"],
                    "deeper_concepts_to_probe": ["Database indexing"],
                    "misconceptions": ["Confusing database index types with distributed server clusters and folders"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total confusion with server clusters and file systems."}
                    ],
                    "citations": [{"claim": "In relational databases: A Clustered Index dictates the actual physical order of data rows on disk", "source_number": 1}],
                    "reasoning": "Complete failure to comprehend database indexing."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_04",
        "subject": "DBMS",
        "question": "What is Database Normalization, and what are the primary differences between 1NF, 2NF, and 3NF?",
        "reference": "[1] Database Normalization is the process of structuring relational tables to reduce data redundancy and eliminate insert, update, and delete anomalies. 1NF requires atomic values and no repeating groups. 2NF requires 1NF plus the removal of partial dependencies (every non-prime attribute must depend on the whole candidate key). 3NF requires 2NF plus the removal of transitive dependencies (no non-prime attribute depends on another non-prime attribute).",
        "samples": [
            {
                "answer": "Normalization organizes relational tables to minimize data redundancy and prevent insertion, update, and deletion anomalies. 1NF requires atomic column values (no multi-valued attributes or repeating groups). 2NF satisfies 1NF and eliminates partial dependencies, meaning every non-key attribute must depend on the complete primary key, not a subset of a composite key. 3NF satisfies 2NF and eliminates transitive dependencies, meaning non-key attributes cannot depend on other non-key attributes.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Normalization reduces redundancy and eliminates anomalies", "1NF enforces atomic values and no repeating groups", "2NF eliminates partial dependencies on composite keys", "3NF eliminates transitive dependencies between non-key attributes"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Boyce-Codd Normal Form (BCNF)", "Denormalization trade-offs for read-heavy OLAP systems"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately defined 1NF, 2NF, and 3NF conditions."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Explained dependency types (partial vs transitive) clearly."}
                    ],
                    "citations": [{"claim": "1NF requires atomic values... 2NF requires 1NF plus the removal of partial dependencies... 3NF requires 2NF plus the removal of transitive dependencies", "source_number": 1}],
                    "reasoning": "Clear, precise explanation of functional dependencies across 1NF, 2NF, and 3NF."
                }
            },
            {
                "answer": "Normalization data duplicate hone se bachata hai. 1NF me har column me ek hi value hoti hai. 2NF aur 3NF tables ko divide karke primary key jodte hain taaki query fast chale.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["Normalization reduces data duplication", "1NF requires atomic single values per column"],
                    "missing_core_concepts": ["2NF specifically removes partial dependencies on composite keys", "3NF specifically removes transitive dependencies", "Normalization actually increases joins, which can slow reads"],
                    "deeper_concepts_to_probe": ["Functional dependencies (partial and transitive)"],
                    "misconceptions": ["Believing normalization is primarily done to make queries run faster"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood 1NF atomicity but gave vague generic descriptions for 2NF and 3NF."}
                    ],
                    "citations": [{"claim": "2NF requires 1NF plus the removal of partial dependencies... 3NF requires 2NF plus the removal of transitive dependencies", "source_number": 1}],
                    "reasoning": "Got 1NF correct, but completely skipped the definitions of partial and transitive dependencies for 2NF and 3NF."
                }
            },
            {
                "answer": "Normalization means converting a relational SQL database into a JSON format so that Node.js can read it without tables.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Normalization is relational schema design to eliminate redundancy and update anomalies via functional dependencies"],
                    "deeper_concepts_to_probe": ["Relational database theory"],
                    "misconceptions": ["Confusing database normalization with JSON serialization"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total confusion with JSON format."}
                    ],
                    "citations": [{"claim": "Database Normalization is the process of structuring relational tables to reduce data redundancy and eliminate... anomalies", "source_number": 1}],
                    "reasoning": "Incorrectly mapped normalization to JSON serialization."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_05",
        "subject": "DBMS",
        "question": "What are the core architectural differences and trade-offs between SQL (Relational) and NoSQL databases?",
        "reference": "[1] SQL databases (e.g. PostgreSQL, MySQL) are relational, use structured schemas with ACID guarantees, rely on SQL for complex joins, and scale vertically (scale-up). NoSQL databases (Document like MongoDB, Key-Value like Redis, Columnar like Cassandra) are non-relational with dynamic schemas, optimize for horizontal scaling (scale-out distributed clustering), prioritize the CAP theorem (often sacrificing immediate consistency for availability/partition tolerance via BASE), but lack standard multi-table ACID joins.",
        "samples": [
            {
                "answer": "SQL databases are relational, table-based systems with predefined schemas that guarantee strict ACID transactions and support complex multi-table joins; they primarily scale vertically. NoSQL databases are non-relational (document, key-value, graph, columnar) with dynamic schemas that scale horizontally across distributed commodity clusters; they follow the BASE model prioritizing availability and partition tolerance under the CAP theorem, at the expense of complex cross-entity joins.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["SQL is relational with fixed schema and strict ACID transactions", "SQL relies on vertical scaling and supports complex joins", "NoSQL is non-relational with dynamic schema and horizontal scaling", "NoSQL optimizes for distributed clustering and CAP theorem trade-offs (BASE)"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["CAP theorem (Consistency, Availability, Partition Tolerance)", "Eventual consistency vs strong consistency"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Clear differentiation between schema, scaling, transactions, and data models."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Compared ACID vs BASE and vertical vs horizontal scaling trade-offs."}
                    ],
                    "citations": [{"claim": "SQL databases... structured schemas with ACID guarantees... scale vertically... NoSQL databases... dynamic schemas... horizontal scaling", "source_number": 1}],
                    "reasoning": "Well-balanced and technically comprehensive comparison of relational and non-relational paradigms."
                }
            },
            {
                "answer": "SQL me tables aur rows hote hain jaise MySQL, aur NoSQL me JSON files hoti hain jaise MongoDB. NoSQL naya hai isliye har jagah SQL se better hota hai aur fast hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 5,
                    "depth_score": 4,
                    "correct_points": ["SQL uses tables and rows (MySQL)", "NoSQL document stores use JSON-like documents (MongoDB)"],
                    "missing_core_concepts": ["ACID transactions vs eventual consistency (BASE)", "Vertical vs horizontal scaling models", "Complex joins and relational integrity"],
                    "deeper_concepts_to_probe": ["When to choose SQL over NoSQL"],
                    "misconceptions": ["Believing NoSQL is universally superior and replaces SQL in all use cases"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Identified data structures and examples but held naive view that NoSQL is always better."}
                    ],
                    "citations": [{"claim": "SQL databases... structured schemas with ACID guarantees... NoSQL databases... lack standard multi-table ACID joins", "source_number": 1}],
                    "reasoning": "Identified the data modeling difference, but showed an immature bias claiming NoSQL is universally superior."
                }
            },
            {
                "answer": "SQL is for software that costs money, and NoSQL means 'No SQL' meaning you write Python code without any database at all.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["NoSQL stands for 'Not Only SQL', referring to non-relational distributed database systems"],
                    "deeper_concepts_to_probe": ["NoSQL data stores"],
                    "misconceptions": ["Believing NoSQL means having no database", "Believing SQL is defined by software cost"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "False etymology and complete absence of technical concepts."}
                    ],
                    "citations": [{"claim": "NoSQL databases (Document like MongoDB, Key-Value like Redis, Columnar like Cassandra) are non-relational", "source_number": 1}],
                    "reasoning": "Completely inaccurate and non-technical assertion."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_06",
        "subject": "DBMS",
        "question": "What are Transaction Isolation Levels in DBMS, and what concurrency anomalies like Dirty Read and Phantom Read do they prevent?",
        "reference": "[1] SQL standard defines four transaction isolation levels to balance concurrency against anomalies: Read Uncommitted (permits Dirty Reads, Non-repeatable Reads, Phantoms), Read Committed (prevents Dirty Reads by reading only committed data), Repeatable Read (prevents Dirty and Non-Repeatable Reads via shared locks/MVCC snapshots), and Serializable (highest level; prevents all anomalies including Phantom Reads by simulating serial execution, often via range locks or strict 2PL).",
        "samples": [
            {
                "answer": "There are four standard isolation levels: Read Uncommitted, Read Committed, Repeatable Read, and Serializable. A Dirty Read occurs when a transaction reads uncommitted changes from another transaction that later roll back; Read Committed prevents this. A Non-Repeatable Read occurs when re-reading a row returns altered data because another transaction updated it; Repeatable Read prevents this. A Phantom Read occurs when re-executing a range query returns newly inserted rows; Serializable prevents this by locking ranges or using strict snapshot isolation.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["Four isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable", "Dirty Read: reading uncommitted rollback data (prevented by Read Committed)", "Non-Repeatable Read: row values change between reads (prevented by Repeatable Read)", "Phantom Read: new rows appear in range queries (prevented by Serializable)"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Multi-Version Concurrency Control (MVCC) in PostgreSQL/MySQL", "Performance cost of Serializable isolation"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately listed all four levels in ascending order."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Mapped each specific anomaly to the level that eliminates it."}
                    ],
                    "citations": [{"claim": "Read Uncommitted... Read Committed (prevents Dirty Reads)... Repeatable Read (prevents Dirty and Non-Repeatable Reads)... Serializable... prevents all anomalies including Phantom Reads", "source_number": 1}],
                    "reasoning": "Flawless, structured explanation of all four isolation levels and their corresponding concurrency anomalies."
                }
            },
            {
                "answer": "Isolation levels decide karte hain ki do transactions ek doosre ko disturb na karein. Dirty read me galat data read hota hai. Highest level Serializable hota hai jo sabse safe hota hai par slow hota hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["Isolation manages transaction interference", "Dirty read involves reading uncommitted/wrong data", "Serializable is the safest and slowest level"],
                    "missing_core_concepts": ["Exact four levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable", "Exact definitions of Non-Repeatable Read and Phantom Read"],
                    "deeper_concepts_to_probe": ["Range locking vs row locking in Serializable"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood the general goal and named Serializable, but omitted the intermediate levels and Phantom Read."}
                    ],
                    "citations": [{"claim": "four transaction isolation levels: Read Uncommitted... Read Committed... Repeatable Read... Serializable", "source_number": 1}],
                    "reasoning": "High-level understanding is correct, but missed the full taxonomy of levels and specific anomaly definitions."
                }
            },
            {
                "answer": "Dirty read means reading from a corrupted hard drive, and phantom read means reading data that was deleted 10 years ago.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Dirty read and phantom read are transactional concurrency anomalies in multi-user DBMS"],
                    "deeper_concepts_to_probe": ["Concurrency control anomalies"],
                    "misconceptions": ["Confusing concurrency anomalies with physical storage corruption and historical archives"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Absurd literal interpretation of terminology."}
                    ],
                    "citations": [{"claim": "Dirty Reads, Non-repeatable Reads, Phantoms... are concurrency anomalies", "source_number": 1}],
                    "reasoning": "Literal, non-technical guessing with zero understanding of database concurrency."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_07",
        "subject": "DBMS",
        "question": "What is the difference between an INNER JOIN, LEFT OUTER JOIN, and FULL OUTER JOIN in SQL queries?",
        "reference": "[1] In SQL relational algebra: An INNER JOIN returns only records that have matching values in both joined tables based on the join predicate. A LEFT OUTER JOIN returns all records from the left table, along with matching records from the right table; if no match exists, NULL values are populated for right-table columns. A FULL OUTER JOIN returns all records when there is a match in either table, filling missing matches with NULLs on either side.",
        "samples": [
            {
                "answer": "An INNER JOIN returns only the rows where there is a matching key in both tables. A LEFT OUTER JOIN returns all rows from the left table plus matching rows from the right table; if a left row has no match, the right columns are filled with NULLs. A FULL OUTER JOIN returns all rows from both tables, pairing matching rows where possible and inserting NULLs on either side whenever a match is absent.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["INNER JOIN returns only records matching in both tables", "LEFT JOIN returns all left rows, filling unmatched right columns with NULL", "FULL OUTER JOIN returns all rows from both tables, filling missing matches with NULL on either side"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["CROSS JOIN (Cartesian product)", "Join optimization using hash joins vs merge joins"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Cleanly distinguished match requirements and NULL padding behavior across all three joins."}
                    ],
                    "citations": [{"claim": "INNER JOIN returns only records that have matching values... LEFT OUTER JOIN returns all records from the left table... FULL OUTER JOIN returns all records when there is a match in either table", "source_number": 1}],
                    "reasoning": "Direct, accurate, and completely sound explanation of SQL join semantics."
                }
            },
            {
                "answer": "Inner join me common data aata hai. Left join me left table ka saara data aata hai aur right table ka common data aata hai. Full join me sab kuch duplicate ho jata hai.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 4,
                    "correct_points": ["Inner join returns common matching data", "Left join returns all left table data plus matching right data"],
                    "missing_core_concepts": ["NULL padding for unmatched columns", "Full join pairs matching records and fills missing sides with NULLs (it does not duplicate everything)"],
                    "deeper_concepts_to_probe": ["NULL handling in outer joins"],
                    "misconceptions": ["Claiming full outer join 'duplicates everything' (confusing with Cartesian CROSS JOIN)"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Accurate on Inner and Left joins, but confused Full Outer Join with Cartesian Product."}
                    ],
                    "citations": [{"claim": "FULL OUTER JOIN returns all records when there is a match in either table, filling missing matches with NULLs", "source_number": 1}],
                    "reasoning": "Inner and Left join definitions are sound, but confused Full Outer Join with Cartesian duplicate product."
                }
            },
            {
                "answer": "Inner join is for primary keys, Left join is for foreign keys, and Full join is only used when copying an entire database to an external backup drive.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["Joins are relational operators combining rows based on predicates, independent of physical backups"],
                    "deeper_concepts_to_probe": ["Relational algebra joins"],
                    "misconceptions": ["Restricting joins to specific key types and associating full joins with backup utilities"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Total misunderstanding of relational query joins."}
                    ],
                    "citations": [{"claim": "In SQL relational algebra: An INNER JOIN returns only records that have matching values... Outer joins subdivide", "source_number": 1}],
                    "reasoning": "Complete failure to understand SQL join operations."
                }
            }
        ]
    },
    {
        "question_id": "DBMS_08",
        "subject": "DBMS",
        "question": "What is the difference between the WHERE clause and the HAVING clause in SQL queries?",
        "reference": "[1] In SQL execution order: The WHERE clause filters individual rows before any grouping or aggregation takes place (cannot contain aggregate functions like SUM, AVG, COUNT). The HAVING clause filters grouped summary rows after the GROUP BY clause has executed and aggregates have been calculated (specifically designed to filter aggregate conditions).",
        "samples": [
            {
                "answer": "The WHERE clause filters individual records before aggregation and grouping occurs, and it cannot contain aggregate functions like COUNT() or AVG(). The HAVING clause filters groups after the GROUP BY clause has executed, specifically designed to filter on aggregate function results (e.g., HAVING COUNT(*) > 5). In query execution order, WHERE runs before GROUP BY, while HAVING runs after.",
                "evaluation": {
                    "verdict": "CORRECT",
                    "correctness_score": 10,
                    "depth_score": 9,
                    "correct_points": ["WHERE filters rows before grouping/aggregation", "WHERE cannot contain aggregate functions", "HAVING filters groups after GROUP BY execution", "HAVING can evaluate aggregate conditions", "Clearly stated the execution order difference"],
                    "missing_core_concepts": [],
                    "deeper_concepts_to_probe": ["Performance impact: filtering early with WHERE reduces rows processed by GROUP BY", "SQL query logical execution phase order"],
                    "misconceptions": [],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "DEMONSTRATED", "evidence_from_answer": "Accurately contrasted row-level vs group-level filtering."},
                        {"evidence_type": "REASONING", "status": "DEMONSTRATED", "evidence_from_answer": "Specified execution order and aggregate function restrictions."}
                    ],
                    "citations": [{"claim": "WHERE clause filters individual rows before any grouping... HAVING clause filters grouped summary rows after the GROUP BY clause", "source_number": 1}],
                    "reasoning": "Clear, precise distinction detailing scope, aggregate function usage, and query execution order."
                }
            },
            {
                "answer": "WHERE clause normal filtering ke liye hota hai aur HAVING clause GROUP BY ke sath use hota hai. Agar GROUP BY nahi hai to HAVING use nahi kar sakte.",
                "evaluation": {
                    "verdict": "PARTIALLY_CORRECT",
                    "correctness_score": 6,
                    "depth_score": 5,
                    "correct_points": ["WHERE is for normal row filtering", "HAVING is used with GROUP BY to filter groups"],
                    "missing_core_concepts": ["WHERE runs before grouping; HAVING runs after aggregation", "Aggregate functions (SUM, COUNT) are forbidden in WHERE and evaluated in HAVING"],
                    "deeper_concepts_to_probe": ["Execution order in SQL"],
                    "misconceptions": ["Strict claim that HAVING can never be used without GROUP BY (HAVING can technically filter an entire table as a single aggregate group in ANSI SQL)"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "PARTIALLY_DEMONSTRATED", "evidence_from_answer": "Understood the general context of GROUP BY but did not mention aggregate function restrictions or execution phases."}
                    ],
                    "citations": [{"claim": "WHERE clause filters individual rows before any grouping... cannot contain aggregate functions", "source_number": 1}],
                    "reasoning": "Correct basic distinction regarding GROUP BY, but missed the underlying execution order and aggregate restrictions."
                }
            },
            {
                "answer": "WHERE and HAVING are exact synonyms in SQL; you can swap them anywhere in a query and the database will produce the same result.",
                "evaluation": {
                    "verdict": "INCORRECT",
                    "correctness_score": 1,
                    "depth_score": 1,
                    "correct_points": [],
                    "missing_core_concepts": ["WHERE filters rows before aggregation; HAVING filters groups after aggregation; swapping them causes syntax and logical errors"],
                    "deeper_concepts_to_probe": ["SQL syntax and clauses"],
                    "misconceptions": ["Believing WHERE and HAVING are interchangeable synonyms"],
                    "evidence": [
                        {"evidence_type": "FUNDAMENTAL", "status": "NOT_DEMONSTRATED", "evidence_from_answer": "Claimed two distinct filtering clauses are completely interchangeable."}
                    ],
                    "citations": [{"claim": "WHERE clause filters individual rows before any grouping... The HAVING clause filters grouped summary rows after the GROUP BY", "source_number": 1}],
                    "reasoning": "Blatantly incorrect claim of equivalence."
                }
            }
        ]
    }
]
