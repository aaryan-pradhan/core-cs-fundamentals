# Lecture 3: Entity-Relationship Model

1. **Data Model:** A collection of conceptual tools for describing **data, data relationships, data semantics, and consistency constraints**.
   1. It works at the conceptual or logical level, the layer the DBA works on.
   2. It describes *what* the data is, the relations among the data, and the consistency constraints.
   3. Data models are used to visualize all of these.
   4. The ER model is one high level data model.

2. **ER Model**
   1. It is a high level data model based on a perception of a **real** world. This world consists of basic objects called **entities** and of **relationships** among them.
      1. **Real world basic objects:** Student, professor, vehicle, customer. They are similar to objects in object oriented technology.
      2. These objects are called entities. Entities have attributes.
   2. The graphical representation of the ER model is the **ER diagram**. It acts as a **blueprint** of the DB.
      1. **Symbols:** A rectangle is an entity. A diamond is a relationship. A line is an association.
      2. **Design steps:** Find the entities. Then find their attributes. Then establish the relationships. Then draw the full ER diagram.
      3. **To tables:** The ER diagram can be converted into tables (the relational model, covered later). It directly helps in designing the actual tables.
      4. **Interview:** You may be asked to draw an ER model.

3. **Entity:** An entity is a "**thing**" or "**object**" in the real world that is **distinguishable** from all other objects.
   1. It has **physical existence**.
   2. Each student in a college is an entity.
      1. A college can itself also be an entity.
   3. An entity can be **uniquely** identified, by a primary attribute (the primary key).
      1. A unique attribute is chosen or defined so that no two entities (for example students) have the same value.
      2. **Example:** Customer ID for Customer.
   4. **Strong entity:** It can be uniquely identified.
      1. It has independent existence and its own primary key. For example, Student is identified by Student ID.
   5. **Weak entity:** It cannot be uniquely identified. It depends on some other strong entity.
      1. It does not have enough attributes to select a uniquely identifiable attribute. It has no primary key of its own.
      2. **Example:** Loan is strong. Payment is weak. Instalments are sequential, so a number counter can be generated separately for each loan.
         1. **Loan:** A loan has a loan type and a loan ID that uniquely identifies it.
         2. **Payment schedule:** A loan has a payment schedule. A 1 year car loan paid in 12 monthly EMIs has 12 payments.
         3. **Payment number:** It is a sequential counter 1, 2, 3, 4... generated separately for each loan. A car loan has payments 1 to 12. A home loan has payments 1, 2, 3... too.
         4. **Weak key:** The payment number alone does not identify a payment. Payment no. 1 of the car loan differs from payment no. 1 of the home loan. So it is a weak key (partial key).
         5. **Dependence:** No loan means no payment schedule. A payment cannot exist without the loan.
      3. **A weak entity depends on a strong entity for its existence.**

4. **Entity set**
   1. It is a set of entities of the **same** type that share the **same** properties, or attributes.
      1. A database has a schema for Student with a set of attributes. Any one student is an entity. The whole collection of students is the entity set.
      2. In ER modelling, entity and entity set are used interchangeably. They differ in strict language, but in an ER diagram both mean the same.
   2. **Examples:** Student. Customer of a bank.

5. **Attributes**
   1. An entity is represented by a set of attributes.
      1. Attributes describe the entity and define its data. "Student: Ram" alone tells nothing.
      2. Define only the attributes needed for the database being built (for example a university DB). Useless attributes waste space.
   2. Each entity has a value for each of its attributes.
   3. For each attribute, there is a set of permitted values called the **domain**, or **value set**.
      1. **Constraints:** Attributes carry consistency constraints. For example, a customer's name cannot be NULL and cannot be numeric. A name like "2345" is illegal.
      2. **Loan type:** A bank gives only car, home and education loans. The domain is these three values. A personal loan or business loan is not permitted.
      3. Without constraints, an illegal entry can get in. Then the data cannot be retrieved or interpreted properly.
   4. **Student entity attributes:**
      A. Student_ID
      B. Name
      C. Standard
      D. Course
      E. Batch
      F. Contact number
      G. Address
      1. **Customer entity attributes:** Customer ID, Contact number, Address, Date of birth, Email ID and so on.
   5. **Types of Attributes**
      1. **Simple**
         1. It cannot be divided further.
            1. You cannot extract separate meaning from the parts. For example, in a 10 digit account number the first 5 or last 5 digits alone mean nothing.
         2. **Examples:** A customer's account number in a bank, a student's roll number.
      2. **Composite**
         1. It can be divided into subparts (other attributes).
         2. **Example:** Name divides into first-name, middle-name and last-name.
         3. The user can refer to the entire attribute or only a component.
            1. **Benefit:** The system can access only a part. For example, find all people whose last name is Mukherjee, or all citizens in a PIN or zip code.
            2. **Versus file system:** That needed a special program (the police zip code example from lecture 1). In a DB, a composite address makes it easy.
            3. The same composite attribute can also be referred to as a whole.
         4. Address divides into street, city, state and PIN code.
            1. **Nesting:** Composites can be nested. Street divides into street name and street number.
            2. **Interview tip:** Always store address as a composite attribute, divided as deeply as possible. The more composite, the better you can manage it.
      3. **Single-valued**
         1. It has only one value.
         2. **Examples:** Student ID, and loan-number for a loan. A student with ID 737 has only that ID, not also 743.
      4. **Multi-valued**
         1. It has more than one value, in a single attribute. You do not store, say, an alternate number separately.
         2. **Examples:** phone-number, nominee-name on some insurance, dependent-name (for example both parents).
         3. A limit constraint may apply, with upper or lower limits. For example, at most two nominees (upper bound), or at least one nominee (lower bound).
      5. **Derived**
         1. Its value can be derived from other related attributes.
         2. **Examples:** Age, loan-age, membership-period.
            1. Age is current date minus date of birth.
            2. Loan-age is current date minus the date the loan was disbursed.
   6. **NULL value**
      1. An attribute is null when an entity does not have a value for it.
      2. **Not applicable:** The value does not exist. For example, a person has no middle-name. The database is not inconsistent here.
      3. **Unknown:** NULL may also mean "unknown".
         1. **Missing entry:** A customer's name is NULL. A constraint says name must exist, so the entry is missing. This is an inconsistency or problem.
         2. **Not known yet:** An employee's salary is null. For example, the employee is still being on-boarded and the salary is not agreed yet.
      4. What NULL means depends on the usage, the attribute and the constraints defined: not applicable, missing, or not known yet.
   7. **Attribute notation in the ER diagram** (example: Customer entity)
      1. **Composite:** Name and Address have their components hanging off them. Address has street, city, state and zip code. Street is itself composite (street name, street number).
      2. **Single-valued:** Customer ID (simple, cannot be divided).
      3. **Multi-valued:** Phone number, drawn as two concentric ellipses, as there can be multiple phone numbers.
      4. **Derived:** Age, drawn as a dotted ellipse, as it can be derived from date of birth.

6. **Relationships**
   1. A relationship is an **association** among two or more entities.
   2. **Examples:** Person has vehicle, Parent has Child, Customer borrow loan.
      1. A database stores many entities. A bank has customers, loans and accounts. A university has professors, courses and students. Entities are disjoint and each is uniquely identified. Relationships tie them together.
      2. **Bank:** Customer borrows Loan. Customer deposits or withdraws Account.
      3. **Online ordering or food delivery:** Customer places Order.
      4. **University:** Professor takes Course. Student enrolls Course.
      5. **Citizen** has Vehicle.
      6. **Naming:** The relationship name (borrow, enroll, takes, places) is written inside the diamond between the two entities.
   3. **Strong relationship:** It is between two independent entities.
      1. **Example:** Customer places Order. Both have independent existence and their own primary keys (Customer ID, Order ID).
      2. **Example:** Professor takes Course (Professor ID, Course ID).
   4. **Weak relationship:** It is between a weak entity and its owner or strong entity.
      1. **Example:** Loan has instalment-payments Payment. It is drawn as a double diamond. Payment exists only if the loan exists.
   5. **Degree of Relationship**
      1. The degree is the number of entities participating in a relationship.

         | Degree | Entities | Example |
         |--------|----------|---------|
         | **Unary** | One | Employee manages employee. Within the same set of employees, some employee is a manager who manages others. |
         | **Binary** | Two | Student takes Course. Others: Customer borrow Loan, Customer deposits Account, Professor takes Course. |
         | **Ternary** | Three | Employee works-on branch, employee works-on job. An employee works on a Branch of a bank in a Job role. Job and Branch are also related to each other, and Employee to each of them. |

      2. Binary relationships are **common**. Ternary and unary are rare. Focus on identifying binary relationships and their constraints.

7. **Relationship Constraints**
   1. **Mapping Cardinality / Cardinality Ratio**
      1. It is the number of entities to which another entity can be associated via a relationship. It tells how many entities of one entity set an entity is associated with in the other entity set.

         | Type | Rule (A and B are entity sets) | Example |
         |------|--------------------------------|---------|
         | **One to one** | An entity in A associates with at most one entity in B, and an entity in B with at most one in A. | Citizen has Aadhar Card |
         | **One to many** | An entity in A associates with N entities in B. An entity in B associates with at most one in A. | Citizen has Vehicle |
         | **Many to one** | An entity in A associates with at most one entity in B. An entity in B can associate with N in A. | Course taken by Professor |
         | **Many to many** | An entity in A associates with N entities in B, and an entity in B with N in A. | Customer buys Product; Student attends Course |

      2. **One to one:** Draw citizens a1, a2, a3... and Aadhar cards b1, b2, b3... The mapping is a1-b1, a2-b2, a3-b3. Each citizen has exactly one card.
      3. **One to many:** One citizen can own multiple vehicles. One vehicle is owned by one citizen. Left to right it is 1:N. Right to left it is N:1.
      4. **Many to one:** Courses c1, c2, c3... and professors p1, p2... Courses c1 and c2 are both taught by p1. Left to right, a course has one professor. Right to left, one professor teaches multiple courses.
      5. **Many to many:** A customer can buy multiple products, and a product can be bought by multiple customers. A student can attend multiple courses, and a course can be attended by multiple students.
   2. **Participation Constraints**
      1. They are also called the **minimum cardinality constraint**.
      2. **Types:** Partial and total participation.
      3. **Partial participation:** Not all entities are involved in the relationship instance. It is not necessary that every entity in the set takes part.
      4. **Total participation:** Each entity must be involved in at least one relationship instance. It is drawn as a double line from the entity to the relationship.
      5. **Example:** Customer borrow loan. Loan has total participation, as it cannot exist without a customer. Customer has partial participation.
         1. Every loan is borrowed by at least one customer. There is no orphan loan.
         2. Some customers may never have taken a loan, so customer participates partially.
         3. Customer to Loan is partial. Loan to Customer is total.
      6. **A weak entity has a total participation constraint, but a strong entity may not have total.**
         1. A weak entity always has total participation (double line). A strong entity may have partial or total.
         2. **Loan-Payment:** Payment has total participation. A payment schedule exists only if tied to some loan.
         3. **Customer-Loan:** Both are strong entities. Customer is partial and loan is total.

8. **ER Notations**

   Symbols used in an ER diagram:

   | Symbol | Notation |
   |---|---|
   | Entity | Rectangle |
   | Weak Entity | Double rectangle |
   | Attribute | Ellipse |
   | Multi-valued Attribute | Double ellipse |
   | Primary Key Attribute | Ellipse with the attribute name underlined |
   | Weak Key Attribute | Ellipse with the attribute name underlined with a dotted line |
   | Derived Attribute | Dotted ellipse |
   | Relationship | Diamond |
   | Total Participation | Double line between the Relationship diamond and the Entity rectangle (labelled "Total Participation") |
   | Weak Relationship | Double diamond |

   1. **Next lecture:** More ER notations, extended ER features (generalization, specialization), and practice drawing ER diagrams.
