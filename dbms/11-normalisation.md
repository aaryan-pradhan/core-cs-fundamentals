# Lecture 11: Normalisation

1. **Normalisation** is a step towards DB optimisation.

## 2. Functional Dependency (FD)

1. An FD is a relationship between the attribute (usually the primary key) of a relation and another attribute of the relation.
   1. **Meaning:** If the value of A is given, the value of B can be found (`A -> B`). A can be a single attribute or a set of attributes. A composite primary key has more than one attribute.
   2. **Candidate keys:** They also count, since the primary key is chosen from the candidate keys.
   3. **Example:** Employee(id, name, department) with id as primary key. We have `id -> name` and `id -> department`. Given an id, the name and the department can be looked up in the table.
   4. It is only a mathematical way of saying which attribute depends on which.
2. In `X -> Y`, the left side is the **Determinant**. The right side is the **Dependent**.
   1. **Determinant:** The attribute whose value is given.
   2. **Dependent:** Its value depends on the determinant.
3. **Types of FD**

   | Type | Rule | Venn diagram |
   |------|------|--------------|
   | Trivial | `A -> B` is trivial if B is a subset of A. | B is drawn inside A. |
   | Non-trivial | `A -> B` is non-trivial if B is not a subset of A. A intersection B is NULL. | A and B are drawn separately, with nothing common. |

   1. **Trivial FD**
      1. `A -> A` and `B -> B` are also trivial FDs.
      2. **Example:** Employee(id, name, address). `(id, name) -> id` is trivial, because id is part of the left side. Anything in the determinant can be determined by it.
      3. `(A, B) -> A` and `(A, B) -> B` are trivial. Trivial means obvious.
   2. **Non-trivial FD**
      1. **Example:** `(id, name) -> address`. Address is not a subset of (id, name).
      2. **Example:** `id -> department`. Department is not a subset of id, so it is non-trivial.
4. **Rules of FD (Armstrong's axioms)**
   1. **Reflexive**
      1. If A is a set of attributes and B is a subset of A, then `A -> B` holds.
      2. In symbols: if A is a superset of B, then `A -> B`.
      3. This is like a trivial FD.
      4. **Example:** X = {A, B, C, D, E} and Y = {A, B, C} is a subset of X. Y is already inside X, so knowing X gives Y. `X -> Y` holds.
   2. **Augmentation**
      1. If B can be determined from A, then adding an attribute to this FD changes nothing.
      2. If `A -> B` holds, then `AX -> BX` holds too. X is a set of attributes.
      3. **Example:** Relation (X, Y, Z), and `X -> Y` is given. Adding Z on both sides, `XZ -> YZ` is also a valid FD.
      4. Any attribute or set of attributes can be added to both sides.
   3. **Transitivity**
      1. If A determines B and B determines C, then A determines C.
      2. In symbols: if `A -> B` and `B -> C`, then `A -> C`.
5. **Worked problems using the rules** (is the FD valid or illegal?)
   1. Relation (A, B, C, D, E). Given FDs: `A -> B`, `A -> C`, `CD -> E`, `B -> D`, `E -> A`.
      1. **Can `BC -> CD` be derived?** `B -> D` is given. Augment both sides with C to get `BC -> CD`. Valid.
      2. **Can `EC -> AC` be derived?** `E -> A` is given. Augment both sides with C to get `EC -> AC`. Valid.
      3. **Is `B -> C` derivable?** No FD given or derivable gives it. Illegal.
   2. Same relation: can CD determine AC (`CD -> AC`)?
      1. `CD -> E` is given and `E -> A` is given. By transitivity, `CD -> A`.
      2. `CD -> C` holds by reflexivity (C is a subset of CD).
      3. `CD -> A` and `CD -> C` together give `CD -> AC`. Valid.

## 3. Why Normalisation?

1. To avoid redundancy in the DB, so we do not store redundant data.

## 4. What happens if we have redundant data?

1. Insertion, deletion and updation anomalies arise.

## 5. Anomalies

1. Anomalies means abnormalities. Data redundancy introduces three types of anomalies.
   1. **Example table used below:** Student(id, name, age, branch code, branch name, branch HOD). Student and branch data are merged in one table. No normalisation is applied, so the data is redundant.
   2. Separate Student and Branch tables at ER model time would have avoided this.
2. **Insertion anomaly**
   1. Certain data (an attribute) cannot be inserted into the DB without the presence of other data.
      1. **Example:** A new student enrols but has not chosen a branch yet (counselling is going on). Either the student cannot be added, or the branch columns are set to NULL and updated later. This is double work.
      2. **Example:** A new IT department is started with branch code 4, but no student has enrolled in it. The IT branch cannot be added to the table, or it is added with NULL student values.
      3. A student and a branch exist independently, but were merged into one table.
3. **Deletion anomaly**
   1. Deleting data causes the unintended loss of some other important data.
      1. **Example:** The only Mechanical student passes out and his row is deleted. The Mechanical branch itself disappears from the DB, as if the university never offered Mechanical.
      2. Separate Student and Branch tables would avoid this.
4. **Updation anomaly (or modification anomaly)**
   1. An update of a single data value requires multiple rows of data to be updated.
      1. **Example:** The HOD of the CS department changes from X to a new person. Every CS student's row has to be changed. One small piece of information changes, but many places in the DB need a change.
   2. Updating many places can cause data inconsistency, if one forgets to update the data at all the intended places.
5. **Effect on size and speed:** Due to these anomalies, DB size increases and DB performance becomes very slow.
   1. The HOD of a department is stored again for every student, so the DB grows and queries slow down.
   2. A separate Department table (CS: X, IT: Y, EC: Z) would hold one entry per department.
6. **Fix:** To rectify these anomalies and their effect on the DB, we use a database optimisation technique called NORMALISATION.

## 6. What is Normalisation?

1. Normalisation minimises redundancy in relations. It also removes undesirable characteristics like insertion, update and deletion anomalies.
   1. **Solving the example:** Decompose into two tables.
      1. Table 1: Student(id, name, age, branch code).
      2. Table 2: Branch Info(branch code, branch name, HOD name).
      3. Now a new IT department can be added with its HOD without enrolling any student. A student deletion does not remove a branch. An HOD change is made in one row. There is no insertion, deletion or updation anomaly.
      4. The DB is easier to view and search.
2. Normalisation divides composite attributes into individual attributes, or divides a larger table into smaller ones and links them using relationships.
   1. **What we do:** Decompose a table into multiple tables.
   2. **SRP (Single Responsibility Principle):** Keep decomposing until SRP is achieved. One table should have one job. It should represent a single idea or a single thing. In the example the Student table also stored branch information, so it had two responsibilities.
3. The normal forms reduce redundancy in the database table.
   1. We move from one normal form to the next until every table honours SRP.

## 7. Types of normal forms

| Form | Needs | Rule |
|------|-------|------|
| 1NF | none | Atomic values, no multi-valued attributes. |
| 2NF | 1NF | No partial dependency. |
| 3NF | 2NF | No transitive dependency. |
| BCNF | 3NF | For `A -> B`, A must be a super key. |

1. **1NF**
   1. Every relation cell must have an atomic value.
      1. **Example:** A contact number cell must not be further divisible.
   2. The relation must not have multi-valued attributes.
      1. **Example:** Employee(id, name, phone). A row like (1, A, 88.. and 99..) with two numbers in one cell is not allowed. Phone must be atomic.
      2. **Converting to 1NF:** Repeat the row, one row per phone number: (1, A, 88..), (1, A, 99..). The data is repeated, so redundancy still exists here.
      3. 1NF only requires atomic values. Further forms handle the redundancy.
      4. **ER link:** Converting an ER diagram makes a multi-valued attribute a separate table, so normalisation is already applied by instinct.
2. **2NF**
   1. The relation must be in 1NF.
   2. There must not be any partial dependency.
      1. All non-prime attributes must be fully dependent on the PK.
         1. A **non-prime attribute** is any attribute that is not part of the candidate key or primary key. The primary key may be composite. Then the non-prime attribute must depend on the whole key.
      2. A non-prime attribute cannot depend on part of the PK.
         1. **Example:** Relation (A, B, C, D), primary key = {A, B}. Prime attributes: A, B. Non-prime: C, D.
         2. Given FD `B -> C`. This is a partial dependency. C is determined by B alone, a part of the primary key.
         3. **Problem:** A and B together form the primary key, so both cannot be NULL together, but one of them can be NULL. If B is NULL, then `B -> C` cannot hold, because NULL cannot determine a value. So a partial dependency cannot be kept.
         4. **Rule:** The whole primary key together must determine another attribute, not a part of it.
      3. **Converting to 2NF:** Decompose into R1(A, B, D) with primary key (A, B), and R2(B, C) with primary key B. Now `AB -> D` and `B -> C` are both full dependencies.
      4. **Real-life example:** StudentProject(student id, project id, student name, project name), primary key (student id, project id). It is in 1NF, since all values are atomic.
         1. Prime: student id, project id. Non-prime: student name, project name.
         2. FDs: `student id -> student name`, `project id -> project name`. Each non-prime attribute depends on part of the primary key, so there are partial dependencies.
         3. Decompose: Student(student id, student name) with student id as PK, and Project(project id, project name) with project id as PK.
         4. Now each non-prime attribute is fully dependent on its table's primary key.
         5. Keep project id in the table linking student and project, as a foreign key. This keeps the two tables linked (student id and project id are primary and foreign keys).
3. **3NF**
   1. The relation must be in 2NF.
   2. No transitive dependency exists.
      1. A non-prime attribute should not determine a non-prime attribute.
         1. **Example:** Relation (A, B, C), primary key A. FDs: `A -> B`, `B -> C`. By transitivity `A -> C`, so `B -> C` is a transitive dependency. A non-prime attribute B determines a non-prime attribute C.
         2. **Check 2NF first:** Values are atomic, and B and C are fully dependent on the primary key A, so there is no partial dependency. It is in 2NF.
         3. **Redundancy:** Wherever B has the same value, C repeats (every B = 1 has C = x, and so on).
      2. **Converting to 3NF:** Decompose into R1(A, B) with PK A and R2(B, C) with PK B. Now the repeated C values are stored once per B, and the redundancy is gone.
4. **BCNF (Boyce-Codd normal form)**
   1. The relation must be in 3NF.
      1. BCNF is a stronger version of 3NF.
   2. For an FD `A -> B`, A must be a super key.
      1. We must not derive a prime attribute from any prime or non-prime attribute.
         1. **2NF case:** a non-prime attribute derived from part of a prime attribute.
         2. **3NF case:** a non-prime attribute derived from a non-prime attribute.
         3. **BCNF:** It removes the case where a prime attribute is derived (B on the right side is a prime attribute).
         4. A prime attribute is already derivable by itself, so deriving it through another attribute is a problem.
         5. **Other way to say it:** For `A -> B`, A must be a super key.
      2. **Example:** Student id, subject, professor.
         1. A student can enrol in multiple subjects (Java, C++). For each subject, a professor is assigned. Multiple professors can teach the same subject (two Java professors PJ and PJ2). One professor teaches only one subject.
         2. The primary key is (student id, subject). Given both, the professor can be found.
         3. It is in 1NF, 2NF (no partial dependency) and 3NF.
         4. **FDs:** `(student id, subject) -> professor`, and `professor -> subject` (because a professor teaches only one subject).
         5. In `professor -> subject`, subject is a prime attribute and it is derived from a non-prime attribute (professor). Also, professor is not a super key. So it is not in BCNF.
      3. **Converting to BCNF:** Decompose into Student(student id, professor id) and Professor(professor id, professor name/subject) with professor id as the primary key.
         1. **Example data:** PJ gives Java, PC gives C++, PJ2 gives Java. Each has a separate professor id.
         2. Now the professor id (prime) finds all non-prime attributes, and no non-prime attribute finds a prime attribute. BCNF holds.
   3. **Summary of the forms using `alpha -> beta`:**

      | Form | Rule |
      |------|------|
      | 2NF | No partial dependency. Beta must not depend on a part of the primary key. |
      | 3NF | No transitivity. A non-prime alpha must not find a non-prime beta. |
      | BCNF | Alpha can be prime or non-prime, but must not find a prime attribute. The right side must never be a prime attribute. |

## 8. Advantages of Normalisation

1. **Less redundancy:** Normalisation helps minimise data redundancy.
2. **Organisation:** Greater overall database organisation.
3. **Consistency:** Data consistency is maintained in the DB.
4. **No anomalies:** The DB is well structured and optimised.
5. **Space and speed:** The DB takes less space and queries run faster.
