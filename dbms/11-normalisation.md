# Lecture 11: Normalisation

1. Normalisation is a step towards DB optimisation.
2. Functional Dependency (FD)
   1. It's a relationship between the primary key attribute (usually) of the relation to that of the other attribute of the relation.
      1. FD means: if the value of A is given, the value of B can be found (A -> B). A can be a single attribute or a set of attributes (a composite primary key has more than one attribute).
      2. Candidate keys also count, since the primary key is chosen from the candidate keys.
      3. Example: Employee(id, name, department) with id as primary key. `id -> name` and `id -> department`: given an id, the name and the department can be looked up in the table.
      4. It is only a mathematical way of saying which attribute depends on which.
   2. X -> Y, the left side of FD is known as a Determinant, the right side of the production is known as a Dependent.
      1. Determinant: the attribute whose value is given, it can determine the other.
      2. Dependent: its value depends on the determinant.
   3. Types of FD
      1. Trivial FD
         1. A → B has trivial functional dependency if B is a subset of A. A->A, B->B are also Trivial FD.
            1. Example: Employee(id, name, address). `(id, name) -> id` is trivial, because id is part of the left side. Anything in the determinant can be determined by it.
            2. `(A, B) -> A` and `(A, B) -> B` are trivial. Trivial means obvious.
            3. Venn diagram: B is drawn inside A.
      2. Non-trivial FD
         1. A → B has a non-trivial functional dependency if B is not a subset of A. [A intersection B is NULL].
            1. Example: `(id, name) -> address`. Address is not a subset of (id, name).
            2. Example: `id -> department`. Department is not a subset of id, so it is non-trivial.
            3. Venn diagram: A and B are drawn separately, with nothing common.
   4. Rules of FD (Armstrong’s axioms)
      1. Reflexive
         1. If ‘A’ is a set of attributes and ‘B’ is a subset of ‘A’. Then, A→ B holds.
         2. If A ⊇ B then A → B.
            1. This is like a trivial FD.
            2. Example: X = {A, B, C, D, E} and Y = {A, B, C} is a subset of X. Y is already inside X, so knowing X gives Y. X -> Y holds.
      2. Augmentation
         1. If B can be determined from A, then adding an attribute to this functional dependency won’t change anything.
         2. If A→ B holds, then AX→ BX holds too. ‘X’ being a set of attributes.
            1. Example: relation (X, Y, Z), X -> Y is given. Adding Z on both sides, XZ -> YZ is also a valid FD.
            2. Any attribute or set of attributes can be added to both sides.
      3. Transitivity
         1. If A determines B and B determines C, we can say that A determines C.
         2. if A→ B and B→ C then A→ C.
   5. Worked problems using the rules (is the FD valid or illegal?)
      1. Relation (A, B, C, D, E). Given FDs: A -> B, A -> C, CD -> E, B -> D, E -> A.
         1. Can BC -> CD be derived? B -> D is given, so augment both sides with C: BC -> CD. Valid.
         2. Can EC -> AC be derived? E -> A is given, so augment both sides with C: EC -> AC. Valid.
         3. Is B -> C derivable? No FD given or derivable gives it. Illegal.
      2. Same relation: can CD determine AC (CD -> AC)?
         1. CD -> E is given and E -> A is given. By transitivity, CD -> A.
         2. CD -> C holds by reflexivity (C is a subset of CD).
         3. CD -> A and CD -> C together give CD -> AC. Valid.
3. Why Normalisation?
   1. To avoid redundancy in the DB, not to store redundant data.
      1. A DB with redundant data is optimised using normalisation, so it ends up with minimum or no redundant values.
4. What happen if we have redundant data?
   1. Insertion, deletion and updation anomalies arises.
5. Anomalies
   1. Anomalies means abnormalities, there are three types of anomalies introduced by data redundancy.
      1. Example table used below: Student(id, name, age, branch code, branch name, branch HOD), with student and branch data merged in one table (no normalisation applied, redundant data).
      2. This could have been avoided by making a separate Student table and Branch table at ER model time. Here the DB is assumed to be built without thinking about it.
   2. Insertion anomaly
      1. When certain data (attribute) can not be inserted into the DB without the presence of other data.
         1. Example: a new student enrols but has not chosen a branch yet (counselling is going on). Either the student cannot be added, or the branch columns are set to NULL and updated later. This is double work.
         2. Example: a new IT department is started with branch code 4, but no student has enrolled in it. The IT branch cannot be added to the table, or it is added with NULL student values.
         3. The existence of a student and the existence of a branch are independent, but they were merged into one table.
   3. Deletion anomaly
      1. The delete anomaly refers to the situation where the deletion of data results in the unintended loss of some other important data.
         1. Example: the only Mechanical student passes out and his row is deleted. The Mechanical branch itself disappears from the DB, as if the university never offered Mechanical.
         2. Important data (the branch) is lost because of the redundant merged table. With separate Student and Branch tables this would not happen.
   4. Updation anomaly (or modification anomaly)
      1. The update anomaly is when an update of a single data value requires multiple rows of data to be updated.
         1. Example: the HOD of the CS department changes from X to a new person. Every CS student's row has to be changed. One small piece of information changes, but many places in the DB need a change.
      2. Due to updation to many places, may be Data inconsistency arises, if one forgets to update the data at all the intended places.
         1. With many rows or many tables, some rows may be missed, so inconsistent data is left behind.
   5. Due to these anomalies, DB size increases and DB performance become very slow.
      1. The same information (e.g. the HOD of a department) is stored again and again for every student, so the DB grows. Queries on a bigger DB are slower.
      2. A separate Department table (CS -> X, IT -> Y, EC -> Z) would hold one entry per department instead.
   6. To rectify these anomalies and the effect of these of DB, we use Database optimisation technique called NORMALISATION.
6. What is Normalisation?
   1. Normalisation is used to minimise the redundancy from a relations. It is also used to eliminate undesirable characteristics like Insertion, Update, and Deletion Anomalies.
      1. Solving the example: decompose into two tables.
         1. Table 1: Student(id, name, age, branch code).
         2. Table 2: Branch Info(branch code, branch name, HOD name).
         3. Now a new IT department can be added with its HOD without enrolling any student, a student deletion does not remove a branch, and an HOD change is made in one row. No insertion, deletion or updation anomaly.
         4. The DB is easier to view and search, and the inconsistency is removed.
   2. Normalisation divides the composite attributes into individual attributes OR larger table into smaller and links them using relationships.
      1. What we do in normalisation: decompose a table into multiple tables.
      2. Keep decomposing until SRP (Single Responsibility Principle) is achieved: one table should have one job, it should represent a single idea or a single thing. In the example the Student table was also storing branch information, so it had two responsibilities.
   3. The normal form is used to reduce redundancy from the database table.
      1. We move from one normal form to the next, optimising the DB further each time, until every table honours SRP.
7. Types of Normal forms
   1. 1NF
      1. Every relation cell must have atomic value.
         1. Example: a contact number cell must not be further divisible.
      2. Relation must not have multi-valued attributes.
         1. Example: Employee(id, name, phone). A row like (1, A, 88.. and 99..) with two numbers in one cell is not allowed. Phone must be atomic.
         2. To convert to 1NF, the row is repeated, one row per phone number: (1, A, 88..), (1, A, 99..). The data is repeated, so redundancy still exists here.
         3. 1NF does not care much about this repetition, it only requires atomic values. Further forms handle the redundancy.
         4. This is what happens when converting an ER diagram to a relation: a multi-valued attribute is made into a separate table, so the normalisation is already applied by instinct at that time.
   2. 2NF
      1. Relation must be in 1NF.
      2. There should not be any partial dependency.
         1. All non-prime attributes must be fully dependent on PK.
            1. A non-prime attribute is any attribute that is not part of the candidate key or primary key. The primary key may be composite, and then the non-prime attribute must depend on the whole key.
         2. Non prime attribute can not depend on the part of the PK.
            1. Example: relation (A, B, C, D), primary key = {A, B}. Prime attributes: A, B. Non-prime: C, D.
            2. Given FD `B -> C`. This is a partial dependency: C is determined by B alone, a part of the primary key.
            3. Problem: A and B together form the primary key, so both cannot be NULL together, but one of them can be NULL. If B is NULL, then `B -> C` cannot hold, NULL cannot determine a value. So a partial dependency cannot be kept.
            4. Rule: the whole primary key together must determine another attribute, not a part of it.
         3. Converting to 2NF: decompose into R1(A, B, D) with primary key (A, B), and R2(B, C) with primary key B. Now `AB -> D` and `B -> C` are both full dependencies.
         4. Real-life example: StudentProject(student id, project id, student name, project name), primary key (student id, project id). It is in 1NF (all values atomic).
            1. Prime: student id, project id. Non-prime: student name, project name.
            2. FDs: `student id -> student name`, `project id -> project name`. Each non-prime attribute depends on part of the primary key, so there are partial dependencies.
            3. Decompose: Student(student id, student name) with student id as PK, Project(project id, project name) with project id as PK.
            4. Now each non-prime attribute is fully dependent on its table's primary key.
            5. Keep project id in the table linking student and project, as a foreign key, so the two tables stay linked (student id and project id are primary and foreign keys).
   3. 3NF
      1. Relation must be in 2NF.
      2. No transitivity dependency exists.
         1. Non-prime attribute should not find a non-prime attribute.
            1. Example: relation (A, B, C), primary key A. FDs: `A -> B`, `B -> C`. By transitivity A -> C, so B -> C is a transitive dependency. A non-prime attribute B finds a non-prime attribute C.
            2. First check 2NF: atomic values, and B and C are fully dependent on the primary key A, no partial dependency. So it is in 2NF.
            3. Redundancy shows up in the data: wherever B has the same value, C repeats the same value (every B = 1 has C = x, and so on). C is repeated per B.
         2. Converting to 3NF: decompose into R1(A, B) with PK A and R2(B, C) with PK B. Now the repeated C values are stored once per B, and the redundancy is gone.
   4. BCNF (Boyce-Codd normal form)
      1. Relation must be in 3NF.
         1. BCNF is a stronger version of 3NF.
      2. FD: A -> B, A must be a super key.
         1. We must not derive prime attribute from any prime or non-prime attribute.
            1. 2NF case: non-prime derived from part of prime. 3NF case: non-prime derived from non-prime. BCNF removes the case where a prime attribute is derived (B on the right side is a prime attribute).
            2. A prime attribute is already derivable by itself, so deriving it with the help of another attribute is a problem.
            3. Other way to say it: for `A -> B`, A must be a super key.
         2. Example: Student id, subject, professor.
            1. A student can enrol in multiple subjects (Java, C++). For each subject, a professor is assigned. Multiple professors can teach the same subject (two Java professors PJ and PJ2). One professor teaches only one subject.
            2. The primary key is (student id, subject): given both, the professor can be found.
            3. It is in 1NF, 2NF (no partial dependency), and 3NF.
            4. FDs: `(student id, subject) -> professor`, and `professor -> subject` (because a professor teaches only one subject).
            5. In `professor -> subject`, subject is a prime attribute and it is derived from a non-prime attribute (professor). Also professor is not a super key. So it is not in BCNF.
         3. Converting to BCNF: decompose into Student(student id, professor id) and Professor(professor id, professor name/subject) with professor id as the primary key.
            1. Example data: PJ -> Java, PC -> C++, PJ2 -> Java, each with a separate professor id.
            2. Now the professor id (prime) finds all non-prime attributes, and no non-prime attribute finds a prime attribute. BCNF holds.
      3. Summary of the forms using `alpha -> beta`:
         1. 2NF: no partial dependency, beta must not depend on a part of the primary key.
         2. 3NF: no transitivity, a non-prime alpha must not find a non-prime beta.
         3. BCNF: alpha can be prime or non-prime but must not find a prime attribute, the right side must never be a prime attribute.
8. Advantages of Normalisation
   1. Normalisation helps to minimise data redundancy.
   2. Greater overall database organisation.
   3. Data consistency is maintained in DB.
   4. No anomalies, the DB is well structured and optimised.
   5. The DB takes less space and queries run faster.
