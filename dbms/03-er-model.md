# Lecture 3: Entity-Relationship Model

1. **Data Model**: Collection of conceptual tools for describing **data, data relationships, data semantics, and consistency constraints.**
   1. Works at the conceptual / logical level, the layer the DBA works on.
   2. Describes *what* the data is, the relations among the data, and the consistency constraints.
   3. Data models are used to visualize all of these.
   4. ER model is one high level data model.
2. **ER Model**
   1. It is a high level data model based on a perception of a **real** world that consists of a collection of basic objects, called **entities** and of **relationships** among these objects.
      1. Real world basic objects: student, professor, vehicle, customer. Similar to objects in object oriented technology.
      2. These objects are called entities; entities have attributes.
   2. Graphical representation of ER Model is **ER diagram**, which acts as a **blueprint** of DB.
      1. Rectangle box = entity, diamond = relationship, line = association.
      2. For any database design task: first find the entities, then their attributes, then establish the relationships among them, then draw the full ER diagram.
      3. The ER diagram can be converted into tables / the relational model (covered in later lectures); it directly helps in designing the actual tables.
      4. In an interview you may be asked to draw an ER model.
3. **Entity**: An Entity is a "**thing**" or "**object**" in the real world that is **distinguishable** from all other objects.
   1. It has **physical existence**.
   2. Each student in a college is an entity.
      1. A college can itself also be an entity.
   3. Entity can be **uniquely** identified. (By a primary attribute, aka Primary Key)
      1. A unique attribute is chosen or defined so that no two entities (e.g. students) have the same value.
      2. The unique attribute of an entity is called its primary key. E.g., Customer ID for Customer.
   4. **Strong Entity**: Can be uniquely identified.
      1. Independent existence in the system; recognised by its own primary key. E.g., Student identified by Student ID.
   5. **Weak Entity**: Can't be uniquely identified., depends on some other strong entity.
      1. It doesn't have sufficient attributes, to select a uniquely identifiable attribute.
         1. It has no primary key of its own.
      2. Loan -> Strong Entity, Payment -> Weak, as instalments are sequential number counter can be generated separate for each loan.
         1. A loan has a loan type and a loan ID that uniquely identifies it.
         2. A loan has a payment schedule, e.g. a 1 year car loan paid in 12 monthly EMIs, so 12 payments.
         3. Payment number is a sequential counter 1, 2, 3, 4... generated separately for each loan; a car loan has payments 1 to 12 and a home loan has payments 1, 2, 3... too.
         4. Payment number alone does not identify a payment (payment no. 1 of the car loan vs payment no. 1 of the home loan); it is a weak key (partial key).
         5. No loan means no payment schedule, so payment cannot exist without the loan.
      3. **Weak entity depends on strong entity for existence.**
4. **Entity set**
   1. It is a set of entities of the **same** type that share the **same** properties, or attributes.
      1. A database does not store just one student; it has a schema for Student with a set of attributes, and any one student in it is an entity.
      2. The whole collection of students is the entity set.
      3. In ER modelling, entity and entity set are used interchangeably (the two differ in strict language, but in an ER diagram both mean the same).
   2. E.g., Student is an entity set.
   3. E.g., Customer of a bank
5. **Attributes**
   1. An entity is represented by a set of attributes.
      1. Attributes describe the entity / define its data. "Student: Ram" alone tells nothing; the attributes tell about the student.
      2. Attributes are limited: define only the attributes needed for the database being built (e.g. a university DB), no useless attributes that waste space.
   2. Each entity has a value for each of its attributes.
   3. For each attribute, there is a set of permitted values, called the **domain**, or **value set**, of that attribute.
      1. Attributes carry consistency constraints. E.g., a customer's name cannot be NULL and cannot be numeric (a name like "2345" is illegal).
      2. E.g., a bank gives only car, home and education loans; the loan type domain is these three values, so a personal loan or business loan entry is not permitted.
      3. Constraints keep the database consistent; without them an illegal entry can get in and the data cannot be retrieved or interpreted properly.
   4. E.g., Student Entity has following attributes
      A. Student_ID
      B. Name
      C. Standard
      D. Course
      E. Batch
      F. Contact number
      G. Address
      1. E.g., Customer entity attributes: Customer ID, Contact number, Address, Date of birth, Email ID and so on.
   5. **Types of Attributes**
      1. **Simple**
         1. Attributes which can't be divided further.
            1. Cannot extract separate meaning from parts. E.g., a 10 digit account number: the first 5 digits or last 5 digits alone mean nothing, use it as a whole.
         2. E.g., Customer's account number in a bank, Student's Roll number etc.
      2. **Composite**
         1. Can be divided into subparts (that is, other attributes).
         2. E.g., Name of a person, can be divided into first-name, middle-name, last-name.
         3. If user wants to refer to an entire attribute or to only a component of the attribute.
            1. Benefit of dividing: the system can access only a part, e.g. all people whose last name is Mukherjee, or all citizens living in a particular PIN/zip code.
            2. With a file system this needed a special program (the police-zip-code example from lecture 1); in a DB, storing address as a composite attribute makes it easy.
            3. The same composite attribute can also be referred to as a whole.
         4. Address can also be divided, street, city, state, PIN code.
            1. Composites can be nested: street can be further divided into street name and street number.
            2. Interview tip: always store address as a composite attribute, as deeply divided as possible; the more composite, the better you can manage it.
      3. **Single-valued**
         1. Only one value attribute.
         2. e.g., Student ID, loan-number for a loan.
            1. A student with ID 737 has only that ID, not also 743.
      4. **Multi-valued**
         1. Attribute having more than one value.
            1. Multiple values in a single attribute / single entry, instead of storing e.g. an alternate number separately.
         2. e.g., phone-number, nominee-name on some insurance, dependent-name etc.
            1. E.g., a policy where you list both parents as dependents.
         3. Limit constraint may be applied, upper or lower limits.
            1. E.g., at most two nominees (upper bound), or at least one nominee (lower bound).
      5. **Derived**
         1. Value of this type of attribute can be derived from the value of other related attributes.
         2. e.g., Age, loan-age, membership-period etc.
            1. Age = current date - date of birth.
            2. Loan-age = current date - date the loan was disbursed.
   6. **NULL Value**
      1. An attribute takes a null value when an entity does not have a value for it.
      2. It may indicate "not applicable", value doesn't exist. e.g., person having no middle-name
         1. The database is not inconsistent here; the value is simply not needed.
      3. It may indicate "unknown".
         1. Unknown can indicate missing entry, e.g., name value of a customer is NULL, means it is missing as name must have some value.
            1. A constraint says name must exist, so a NULL here means the entry is missing; some inconsistency or problem.
         2. Not known, salary attribute value of an employee is null, means it is not known yet.
            1. E.g., the employee is still being on-boarded and the salary has not been agreed yet.
      4. What NULL means depends on the usage, the attribute and the constraints defined: not applicable, missing, or not known yet.
   7. Attribute notation in the ER diagram (example: Customer entity)
      1. Composite attributes (Name, Address) have their component attributes hanging off them; Address has street, city, state, zip code, and street is itself composite (street name, street number).
      2. Single-valued: Customer ID (simple, cannot be divided).
      3. Multi-valued: Phone number, drawn as two concentric ellipses, as there can be multiple phone numbers.
      4. Derived: Age, drawn as a dotted ellipse, as it can be derived from date of birth.
6. **Relationships**
   1. **Association** among two or more entities.
   2. e.g., Person has vehicle, Parent has Child, Customer borrow loan etc.
      1. A database stores many entities (e.g. bank: customers, loans, accounts; university: professors, courses, students). Entities are disjoint and each is uniquely identified; the relationships tie them together.
      2. Bank: Customer borrows Loan; Customer deposits / withdraws Account.
      3. Online ordering / food delivery: Customer places Order.
      4. University: Professor takes Course; Student enrolls Course.
      5. Citizen has Vehicle.
      6. Each is a simple English statement; the relationship name (borrow, enroll, takes, places) is written inside the diamond between the two entities.
   3. **Strong Relationship**, between two independent entities.
      1. E.g., Customer places Order: both have independent existence and their own primary keys (Customer ID, Order ID).
      2. E.g., Professor takes Course (Professor ID, Course ID).
   4. **Weak Relationship**, between weak entity and its owner/strong entity.
      1. e.g., Loan <instalment-payments> Payment.
         1. Drawn as a double diamond.
         2. Payment exists only if the loan exists.
   5. **Degree of Relationship**
      1. Number of entities participating in a relationship.
      2. **Unary**, Only one entity participates. e.g., Employee manages employee.
         1. Within the same set of employees, some employee is a manager who manages other employees.
      3. **Binary**, two entities participates. e.g., Student takes Course.
         1. Others: Customer borrow Loan, Customer deposits Account, Professor takes Course.
      4. **Ternary** relationship, three entities participates. E.g, Employee works-on branch, employee works-on job.
         1. Employee works on a Branch of a bank in a Job role; Job and Branch are also related to each other, and Employee to each of them.
      5. Binary are **common**.
         1. Ternary and unary are rare; focus on identifying binary relationships and their constraints.
7. **Relationships Constraints**
   1. **Mapping Cardinality / Cardinality Ratio**
      1. Number of entities to which another entity can be associated via a relationship.
         1. How many entities of one entity set an entity is associated with in the other entity set.
      2. **One to one,** Entity in A associates with at most one entity in B, where A & B are entity sets. And an entity of B is associated with at most one entity of A.
         1. E.g., Citizen has Aadhar Card.
            1. Draw two sets: citizens a1, a2, a3... and Aadhar cards b1, b2, b3...; mapping is a1-b1, a2-b2, a3-b3; each citizen has exactly one card.
      3. **One to many,** Entity in A associated with N entity in B. While entity in B is associated with at most one entity in A.
         1. e.g., Citizen has Vehicle.
            1. One citizen can own multiple vehicles; one vehicle is owned by only one citizen. Left to right it is 1:N, right to left it is N:1.
      4. **Many to one,** Entity in A associated with at most one entity in B. While entity in B can be associated with N entity in A.
         1. e.g., Course taken by Professor.
            1. Courses c1, c2, c3... and professors p1, p2...; c1 and c2 are both taught by p1. Left to right, a course is taught by one professor; right to left, one professor can teach multiple courses.
      5. **Many to many,** Entity in A associated with N entity in B. While entity in B also associated with N entity in A.
         1. Customer buys product.
            1. A customer can buy multiple products, and a product can be bought by multiple customers.
         2. Student attend course.
            1. A student can attend multiple courses, and a course can be attended by multiple students.
   2. **Participation Constraints**
      1. Aka, **Minimum cardinality constraint.**
      2. **Types**, Partial & Total Participation.
      3. **Partial Participation**, not all entities are involved in the relationship instance.
         1. Not necessary that every entity in the entity set takes part in the relationship instance.
      4. **Total Participation**, each entity must be involved in at least one relationship instance.
         1. Every entity in the entity set is involved in at least one relationship instance.
         2. Drawn as a double line from the entity to the relationship.
      5. e.g., Customer borrow loan, loan has total participation as it can't exist without customer entity. And customer has partial participation.
         1. Every loan in the loan entity set is borrowed by at least one customer; no orphan loan that no customer took.
         2. Some customers may never have taken a loan, so customer participates partially.
         3. Customer -> Loan is partial; Loan -> Customer is total.
      6. **Weak entity has total participation constraint, but strong may not have total.**
         1. A weak entity always comes with total participation (double line); a strong entity may have partial or total.
         2. E.g., in Loan-Payment, Payment has total participation: a payment schedule exists only if it is tied to some loan.
         3. In Customer-Loan, both are strong entities; customer is partial and loan is total.
8. **ER Notations**

   Symbols used in ER Diagram

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

   1. Next lecture: more ER notations, extended ER features (generalization, specialization), and practice drawing ER diagrams.
