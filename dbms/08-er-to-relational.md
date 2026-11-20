# Lecture 8: Transform - ER Model to Relational Model

1. Both the ER model and the relational model are abstract logical representations of real-world enterprises. They follow similar design principles, so we can convert an ER design into a relational design.
   - **DB design order:** First the ER model, which gives the ER diagram. Then the relational model, which gives the conceptual schema of the whole DB as tables.
   - **Relations between tables:** They are shown with FKs. Referential constraints apply.
   - **Conversion decides:** How many tables, which PKs, which FKs, and how relationships are shown.
   - **Running example:** The Banking System ER diagram (Lecture 5). It has strong entities, a weak entity, a weak relationship, a generalisation and a unary relationship.
2. Converting a DB representation from an ER diagram to a table format is how we reach a relational DB design from an ER diagram.
3. ER diagram notations to relations:

   1. **Strong Entity**
      1. It becomes an **individual table** with the entity name. Its attributes become columns of the relation.
      2. The entity's Primary Key (PK) is used as the relation's PK.
      3. **FKs** are added to establish relationships with other relations.
      - **Table name:** the entity name.
      - **Columns:** Single-valued attributes become columns. Multivalued, composite and derived attributes are handled separately (see below).
      - **Example:** Loan is a strong entity. Its table is `loan (loan-number, amount)`.

   2. **Weak Entity**
      1. A table is formed with all the attributes of the entity.
      2. The PK of its corresponding strong entity is added as an **FK**.
      3. The **PK** of the relation is a composite PK: {FK + partial discriminator key}.
      - A weak entity has no existence of its own. It totally participates in a strong entity.
      - **Example:** Payment is a weak entity of Loan. Its table has its own 3 attributes plus a 4th column, loan-number (the PK of Loan).
      - loan-number is also an FK in the payment table.
      - **PK:** {loan-number, payment-number}. The discriminator (payment-number) alone cannot be a PK, because the weak entity depends on the strong entity.

   3. **Single Values Attributes**
      1. They are represented directly as **columns** in the tables (relations).
      - Each one simply adds one column to the relation.

   4. **Composite Attributes**
      1. Create a separate column in the original relation for each component of the composite attribute.
      2. **Example:** **Address** {street-name, house-no} is a composite attribute in the customer relation. We add address-street-name and address-house-name as new columns and ignore "address" as an attribute.
      - **Rule:** Break the composite attribute into its components. Each component becomes its own column.
      - **Example:** Customer has Address, and street is itself composite. That gives 5 components, so the columns are address-city, address-state, address-pin-code, address-street-number and address-street-name. Other attributes (customer-name etc.) stay.

   5. **Multivalued Attributes**
      1. Create a **new table** for each multivalued attribute. It is named after the original attribute.
      2. The PK of the entity is used as an **FK** column in the new table.
      3. The multivalued attribute's name is added as a column to hold the multiple values.
      4. The **PK** of the new table is {FK + multivalued name}.
      5. **Example:** In the strong entity **Employee**, **dependent-name** is a multivalued attribute.
         1. A new table named dependent-name is formed with columns emp-id and dname.
         2. PK: {emp-id, name}
         3. FK: {emp-id}
      - **Why not a column in the employee table:** One emp-id can have many dependents (father, mother, brother, wife; 3-4 entries). That would repeat all other employee attributes for every dependent.
      - emp-id in the new table is an FK referencing the employee table's PK.
      - Both columns together form the PK.
      - **Example data:** emp-id 1 can have several rows, one per dependent name.

   6. **Derived Attributes:** They are not considered in the tables.
      - They are only an ER diagram notation. They are not stored, because they can be calculated directly (for example, through an API or query).
      - **Example:** Age is calculated from DOB and the current date, so there is no place for it in the table.

   7. **Generalisation**
      1. **Method-1:** Create a table for the higher-level entity set. For each lower-level entity set, create a table with a column for each of its own attributes, plus a column for each attribute of the primary key of the higher-level entity set.

         Example: the Banking System generalisation of Account into savings and current.
         1. Table 1: account (account-number, balance)
         2. Table 2: savings-account (account-number, interest-rate, daily-withdrawal-limit)
         3. Table 3: current-account (account-number, overdraft-amount, per-transaction-charges)
         - There is one table for the higher-level (generalised) entity and one table each for the lower-level entities.
         - The PK of the lower-level tables is the PK of the generalised entity (account-number).
      2. **Method-2:** This is an alternative. It works only if the generalisation is disjoint and complete.
         - **Disjoint:** No entity is a member of two lower-level entity sets directly below a higher-level entity set.
         - **Complete:** Every entity in the higher-level entity set is also a member of one of the lower-level entity sets.
         - **Rule:** Do not create a table for the higher-level entity set. For each lower-level entity set, create a table with a column for each of its own attributes, plus a column for each attribute of the higher-level entity set.

         Tables would be:
         1. Table 1: savings-account (account-number, balance, interest-rate, daily-withdrawal-limit)
         2. Table 2: current-account (account-number, balance, overdraft-amount, per-transaction-charges)
         - The account table is dropped. Its attributes (balance) are copied into both lower-level tables. account-number is still the PK in both.
      3. **Drawbacks of Method-2:**
         - **Overlapping generalisation:** Some values, such as balance, are stored twice.
         - **Incomplete generalisation:** Accounts that are neither savings nor current cannot be represented.
         - **Overlapping, in detail:** One account number provides both savings and current features (not two accounts). It needs an entry in both tables, so the same balance is stored twice. With Method-1 the balance is stored once, in the account table.
         - **Incomplete, in detail:** A third account type not stored in the DB has no table, so it has nowhere to be stored.
      - **Choosing:** It depends on the use case. Method-2 looks better at a glance (only 2 tables). But Method-1 is simpler, and the requirement may force it.

   8. **Aggregation**
      1. Make a table for the relationship set.
      2. Its attributes include the primary keys of the entity set and of the aggregation set's entities.
      3. Also add a descriptive attribute, if any, on the relationship.
      - **Recall (Lecture 4):** Job, employee and branch form a ternary relationship. It is aggregated as "works-on". A relationship between the works-on aggregation and the manager entity says the manager manages that combination (an employee with a particular job at a particular branch).
      - **Table:** Make a table named after the relationship between the aggregated entity and the normal (strong) entity: manages.
      - **Columns:** The PKs of all participants: manager-id (manager), emp-id (employee), job-id (job), branch-id (branch).
      - **PK:** All of these together form a composite PK.

   9. **Unary Relationship**
      - **One-to-many** (for example, employee managed by employee, mapping cardinality 1:N):
         1. The employee table already has emp-id. A manager is himself an employee.
         2. Add the manager's emp-id as one more column (manager-id) in the same employee table. Treat it as an FK referencing the employee table's own PK.
         3. **Example:** Employees 201 and 202 are both managed by 205. One manager can manage many employees.
         4. The manager column can be NULL. A person may have no manager (for example, the CEO).
      - **One-to-one** (for example, Person married to Person, monogamy):
         1. The Person table has id, name, spouse-id.
         2. spouse-id behaves like an FK. id is the PK.
      - **Many-to-many** (for example, Course with prerequisite course; a course may need other courses first, such as computer needing physics and maths first):
         1. The entity table exists anyway: course (id, title). PK is id.
         2. Make a second table named after the relationship: prereq (id, prereq-course-id).
         3. Both columns are course ids, so both are FKs referencing the PK of course.
         4. Both together form the composite PK.

# Facebook ER Model to Relational Model

Converting the Facebook ER diagram (Lecture 6, social media website) with the rules above gives 9 tables (relations). They can then be implemented in an RDBMS with SQL commands (for example, MySQL).

1. **user-profile** (strong entity): user-name (PK), password, dob. All attributes are single-valued.
2. **user-profile-email:** Email is multivalued, so it gets a new table.
   - user-name is an FK. Email is one single-valued column.
   - PK is {user-name, email} (composite).
3. **user-profile-contact:** Contact is also multivalued, so it gets a separate table made the same way.
4. **friendship:** It is a unary relationship between user-profile and user-profile, so it gets a separate table.
   - **Columns:** the profile that requested and the profile that accepted.
   - Both are FKs referencing user-profile's PK (user-name).
   - Both together form the PK (a compound key: a key made by combining two FKs).
5. **post-like** (strong entity): post-like-id (PK), time-stamp, plus two FKs.
   - **post-id (FK):** It shows the "has" relationship with user-post. With it you can find which post has how many likes.
   - **user-name (FK, PK of user-profile):** It shows the "can" relationship: a user can like a post.
6. **user-post:** post-id (PK), its other attributes, and user-name as FK (the "post" relationship) referencing user-profile.
   - The link between user-post and user-profile is via user-name.
   - The "has" relationship is shown in the other tables (post-like, post-comment) through post-id.
7. **user-post-image:** Image is multivalued (a post can have many images), so it gets a new table.
   - **Columns:** post-id (FK, the PK of user-post) and image-url (each image has its own URL).
   - Together they form the PK.
8. **user-post-video:** Same as above, for video (multivalued).
9. **post-comment:** post-comment-id (PK), text-content, time-stamp (its single-valued attributes).
   - A comment is made by a user profile. So user-name (PK of user-profile) is added as an FK to handle the "comments" relationship.
   - post-id (PK of user-post) is added as an FK to handle the "has" relationship.
   - So it has two FKs.
