# Lecture 8: Transform - ER Model to Relational Model

1. Both ER-Model and Relational Model are abstract logical representation of real world enterprises. Because the two models implies the similar design principles, we can convert ER design into Relational design.
   - DB design order: first ER model (gives the ER diagram), then Relational model (gives the conceptual schema of the whole DB as tables).
   - Relations between tables are shown with FKs; referential constraints apply.
   - Questions answered by conversion: how many tables, which PKs, which FKs, how relationships are shown.
   - Running example: Banking System ER diagram (Lecture 5), which has strong entities, weak entity, weak relationship, generalisation, unary relationship.
2. Converting a DB representation from an ER diagram to a table format is the way we arrive at Relational DB-design from an ER diagram.
3. ER diagram notations to relations:
   1. **Strong Entity**
      1. Becomes an **individual table** with entity name, attributes becomes columns of the relation.
      2. Entity's Primary Key (PK) is used as Relation's PK.
      3. **FK** are added to establish relationships with other relations.
      - Table name = entity name.
      - Single-valued attributes become columns; multivalued, composite and derived attributes are handled separately (see below).
      - e.g., Loan is a strong entity: table `loan (loan-number, amount)`.
   2. **Weak Entity**
      1. A table is formed with all the attributes of the entity.
      2. PK of its corresponding Strong Entity will be added as **FK**.
      3. **PK** of the relation will be a composite PK, {FK + Partial discriminator Key}.
      - A weak entity has no existence of its own; it depends on (totally participates in) a strong entity.
      - e.g., Payment is a weak entity of Loan. Its table has its own 3 attributes plus a 4th column, loan-number (the PK of Loan).
      - loan-number is also an FK in the payment table.
      - PK = {loan-number, payment-number}. The discriminator (payment-number) alone cannot be a PK because the weak entity depends on the strong entity.
   3. **Single Values Attributes**
      1. Represented as **columns** directly in the tables/relations.
      - Simply adds one column to the relation.
   4. **Composite Attributes**
      1. Handled by **creating a separate attribute** itself in the original relation for each composite attribute.
      2. e.g., **Address**: {street-name, house-no}, is a composite attribute in customer relation, we add address-street-name & address-house-name as new columns in the attribute and ignore "address" as an attribute.
      - Break the composite attribute down into its components; each component becomes its own column.
      - e.g., Customer has Address (with street as itself composite): 5 components in total, so columns are address-city, address-state, address-pin-code, address-street-number, address-street-name, plus the other attributes of customer (customer-name etc.).
   5. **Multivalued Attributes**
      1. **New tables** (named as original attribute name) are created for each multivalued attribute.
      2. PK of the entity is used as column **FK** in the new table.
      3. Multivalued attribute's similar name is added as a column to define multiple values.
      4. **PK** of the new table would be {FK + multivalued name}.
      5. e.g., For Strong entity **Employee**, **dependent-name** is a multivalued attribute.
         1. New table named dependent-name will be formed with columns emp-id, and dname.
         2. PK: {emp-id, name}
         3. FK: {emp-id}
      - Why not add dependent-name as one more column in the employee table: one emp-id can have many dependents (father, mother, brother, wife; 3-4 entries), so that would repeat all the other attributes of the employee for every dependent.
      - So the multivalued attribute is moved to a new table; the new table has the same name as the attribute.
      - emp-id in the new table is an FK referencing the employee table's PK.
      - Both columns together form the PK.
      - Example data: emp-id 1 can have several rows, one per dependent name.
   6. **Derived Attributes**: Not considered in the tables.
      - Derived attributes are only a notation in the ER diagram.
      - They are not stored because they can be calculated directly (e.g. through an API or query).
      - e.g., age is calculated from DOB and the current date, so there is no place for it in the table.
   7. **Generalisation**
      1. **Method-1:** Create a table for the higher level entity set. For each lower-level entity set, create a table that includes a column for each of the attributes of that entity set plus a column for each attribute of the primary key of the higher-level entity set.
         For e.g., Banking System generalisation of Account - saving & current.
         1. Table 1: account (account-number, balance)
         2. Table 2: savings-account (account-number, interest-rate, daily-withdrawal-limit)
         3. Table 3: current-account (account-number, overdraft-amount, per-transaction-charges)
         - One table for the higher-level (generalised) entity and one table each for the lower-level entities.
         - The PK of the lower-level tables is the PK of the generalised entity (account-number).
      2. **Method-2:** An alternative representation is possible, if the generalisation is disjoint and complete—that is, if no entity is a member of two lower-level entity sets directly below a higher-level entity set, and if every entity in the higher level entity set is also a member of one of the lower-level entity sets. Here, do not create a table for the higher-level entity set. Instead, for each lower-level entity set, create a table that includes a column for each of the attributes of that entity set plus a column for each attribute of the higher-level entity sets.
         Tables would be:
         1. Table 1: savings-account (account-number, balance, interest-rate, daily-withdrawal-limit)
         2. Table 2: current-account (account-number, balance, overdraft-amount, per-transaction-charges)
         - The account table is dropped; its attributes (balance) are copied into both lower-level tables. account-number is still the PK in both.
      3. Drawbacks of Method-2: If the second method were used for an overlapping generalisation, some values such as balance would be stored twice unnecessarily. Similarly, if the generalisation were not complete—that is, if some accounts were neither savings nor current accounts—then such accounts could not be represented with the second method.
         - Overlapping generalisation: the same entity belongs to both savings and current, i.e. one account number provides both features (not two separate accounts). It needs an entry in both tables, and since it is the same account the balance is the same, so it is stored twice (redundancy). With Method-1 the balance is stored once, in the account table; the lower tables do not hold balance.
         - Incomplete generalisation: some accounts are neither savings nor current (a third account type not stored in the DB). There is no generalised entity table, so such an account has nowhere to be stored.
      - Which method to use depends on the use case. Method-2 looks better at a glance (only 2 tables, account table is not redundant) but Method-1 looks simpler and the requirement may force it. Think about whether a table can be dropped as redundant for your use case.
   8. **Aggregation**
      1. Table of the relationship set is made.
      2. Attributes includes primary keys of entity set and aggregation set's entities.
      3. Also, add descriptive attribute if any on the relationship.
      - Recall (Lecture 4): job, employee and branch form a ternary relationship; it is aggregated as "works-on", and a relationship between the works-on aggregation and the manager entity says the manager manages that combination (an employee with a particular job at a particular branch).
      - Make a table named after the relationship between the aggregated entity and the normal (strong) entity: manages.
      - Its columns are the PKs of all participants: manager-id (manager), emp-id (employee), job-id (job), branch-id (branch).
      - All of these together form a composite PK.
   9. **Unary Relationship**
      - One-to-many (e.g. employee managed by employee, mapping cardinality 1:N):
         1. The employee table already has emp-id; a manager is himself an employee.
         2. Add the manager's emp-id as one more column (manager-id) in the same employee table and treat it as an FK referencing the employee table's own PK.
         3. e.g., employees 201 and 202 are both managed by 205. One manager can manage many employees.
         4. The manager column can be NULL: a person may have no manager (e.g. the CEO).
      - One-to-one (e.g. Person married to Person, monogamy):
         1. Person table: id, name, spouse-id.
         2. spouse-id behaves like an FK; id is the PK.
      - Many-to-many (e.g. Course with prerequisite course; a course may need other courses first, e.g. computer needs physics and maths first):
         1. The entity table exists anyway: course (id, title); PK is id.
         2. Make a second table named after the relationship: prereq (id, prereq-course-id).
         3. Both columns are course ids, so both are FKs referencing the PK of course.
         4. Both together form the composite PK.

# Facebook ER Model to Relational Model

Converting the Facebook ER diagram (Lecture 6, social media website) with the rules above gives 9 tables (relations), which can then be implemented in an RDBMS with SQL commands (e.g. MySQL).

1. **user-profile** (strong entity): user-name (PK), password, dob. All single-valued attributes.
2. **user-profile-email**: email is multivalued, so a new table. user-name is an FK; email is one single-valued column. PK is {user-name, email} (composite).
3. **user-profile-contact**: contact is also multivalued, so a separate table made the same way.
4. **friendship**: a unary relationship between user-profile and user-profile, so a separate table with two columns, the profile that requested and the profile that accepted. Both are FKs referencing user-profile's PK (user-name). Both together form the PK (a compound key: a key made by combining two FKs).
5. **post-like** (strong entity): post-like-id (PK), time-stamp, plus two FKs.
   - post-id (FK) shows the "has" relationship with user-post; with it you can find which post has how many likes.
   - user-name (FK, PK of user-profile) shows the "can" relationship: a user can like a post.
6. **user-post**: post-id (PK), its other attributes, and user-name as FK (the "post" relationship) referencing user-profile. The link between user-post and user-profile is via user-name. The "has" relationship is shown in the other tables (post-like, post-comment) through post-id.
7. **user-post-image**: image is multivalued (a post can have many images), so a new table. post-id (FK, the PK of user-post) and image-url (each image has its own URL). Together they form the PK.
8. **user-post-video**: same as above for video (multivalued).
9. **post-comment**: post-comment-id (PK), text-content, time-stamp (its single-valued attributes).
   - Comment is made by a user profile, so user-name (PK of user-profile) is added as FK to handle the "comments" relationship.
   - post-id (PK of user-post) is added as FK to handle the "has" relationship.
   - So it has two FKs.
