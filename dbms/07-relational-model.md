# Lecture 7: Relational Model

1. The **Relational Model (RM)** organises data as **relations (tables)**.
   1. **Data model:** RM is a data model, like the ER model. It describes data, relationships within the data, and data consistency constraints.
   2. **Table and relation:** They are the same thing. Do not get confused between the two.
   3. **Design steps:**
      - Step 1: build the ER model (ER diagram).
      - Step 2: convert the ER model into the relational model.
      - Step 3: an RDBMS implements the relational model (`CREATE TABLE` etc.).
   4. **Conversion from ER to RM:** Each entity becomes a table. Each attribute becomes a column. Multivalued and composite attributes, and relationships, come in the next lecture.
   5. **Example:** Entity Customer (cust_id, name, address, contact_no) becomes table Customer with those 4 columns.

      | cust_id | name | address | contact_no |
      |---|---|---|---|
      | 1 | Lakshya | ... | ... |
      | 2 | Raj | ... | ... |

   6. **Example:** The online delivery system ER model gives two tables.
      - Customer(cust_id, name, address, contact_no) with PK cust_id.
      - Order(order_id, timestamp, delivery_date) with PK order_id. Timestamp is the time the order was placed.
2. A relational DB is a **collection of tables**. Each table has a **unique name**.
3. A **row** in a table represents a relationship among a set of values. A table is a collection of such relationships.
   1. Here the 4 values of a row define one customer.
4. **Tuple:** A single row of the table. It is a single data point, a unique record.
   1. Each tuple of the Customer table represents one customer.
5. **Columns:** They represent the attributes of the relation. Each attribute has a permitted set of values, called the **domain of the attribute**.
6. **Relation schema:** It defines the design and structure of the relation. It contains the name of the relation and all its columns (attributes).
   1. It is a way of defining the table: relation name plus its attributes. Examples: the schema of Customer, the schema of Order.
7. **RDBMS:** Common RM-based DBMS systems are Oracle, IBM, **MySQL** and MS Access.
   1. An RDBMS is the software that implements the relational model.
8. **Degree of table:** The number of attributes (columns) in a table.
   1. A Customer table with 4 columns has degree 4.
9. **Cardinality:** The total number of tuples in a relation.
   1. In the ER model cardinality meant something else. Here it is the total number of rows.
   2. A Customer table with 2 rows has cardinality 2, so there are 2 unique customers.
10. **Relational key:** A set of attributes that can uniquely identify each tuple.
    1. It applies to a table and a relation alike.

## 11. Properties of a table in the relational model

| # | Property | Detail |
|---|----------|--------|
| 1 | **Unique relation name** | The name of a relation is distinct among all other relations. Each entity has a unique name in the ER model, and each entity becomes a table. So each table has a unique name in the database. |
| 2 | **Atomic values** | Values cannot be broken down further. A contact number cannot be split into two parts to get a meaning out of them. A name cannot be broken down further. |
| 3 | **Unique column names** | No two attributes in a relation have the same name. This is similar to the ER diagram. |
| 4 | **Unique tuples** | No redundant (extra) rows. A second row with cust_id 1 and name Lakshya, same as the existing one, is not wanted. The data of cust_id 1 is already stored, so do not store it again. |
| 5 | **Order does not matter** | The sequence of rows and columns has no significance. Name, address and contact can be written in any order. Only all attributes must be defined. |
| 6 | **Integrity constraints** | Tables must follow integrity constraints. They help maintain data consistency across tables. |

## 12. Relational model keys

1. **Super Key (SK):** Any permutation and combination (P&C) of attributes in a table that can uniquely identify each tuple.
   2. **Example:** In Customer, these are super keys: {cust_id}, {cust_id, email}, {contact, email}, {cust_id, name, contact, email}. Any such P&C that uniquely identifies each tuple is a super key.
2. **Candidate Key (CK):** The minimum subset of a super key that can uniquely identify each tuple. It contains no redundant attribute.
   1. Take the super key {cust_id, name, contact, email}. Two customers can have the same name, so name is redundant. Remove such attributes. What remains is a candidate key.
   2. **Example:** The candidate keys are {cust_id}, {contact}, {email}, {cust_id, contact} and {cust_id, email}. Name is removed from every super key since it can repeat.
   3. Every candidate key is a super key. The reverse is not true.
   4. **CK value must not be NULL.**
   5. A super key can be NULL. It is a superset, and in set maths a superset can include NULL entries. A candidate key cannot be NULL.
3. **Primary Key (PK):**
   1. It is selected out of the CK set. It has the least number of attributes.
   2. All candidate keys identify uniquely, but only one becomes the PK: the shortest one. For example, choose cust_id as PK.
4. **Alternate Key (AK):**
   1. All CKs except the PK.
   2. AK = set of CKs minus PK.
5. **Foreign Key (FK):**
   1. It creates a relation between two tables.
   2. A relation r1 may include among its attributes the PK of another relation r2. This attribute is called an FK from r1 referencing r2.
   3. r1 is the **Referencing (Child) relation** of the FK dependency. r2 is the **Referenced (Parent) relation** of the FK.
   4. An FK helps cross reference between two different relations.
   5. **Why needed:** The ER diagram has the relationship "Customer places Order" (the diamond). The tables must show it too. The FK does this.
   6. **How:** Add the PK of one table as an attribute in the other. Add cust_id to Order. cust_id is the PK of Customer, so in Order it is an FK.
   7. **Example Order table:** (order_id 21, cust_id 1), (22, 2), (23, 3). Customer 1 placed order 21, customer 2 placed order 22, customer 3 placed order 23.
   8. **Cross reference:** To find who placed order 21, take its FK value (1) and read customer 1 in the Customer table.
   9. The ER relationship diamond becomes the FK inside the Order table.
   10. **Naming:** Order (holds the FK) is the child (referencing) relation. Customer (its PK is used) is the parent (referenced) relation.
6. **Composite Key:** A PK formed using at least 2 attributes.
7. **Compound Key:** A PK formed using 2 FKs.
   1. **Example:** Two schools A and B each keep their own registration numbers (A: 101, 102, 103; B: B101, B102 and so on). The tables are independent. When merging them into one table, the registration number alone cannot be the PK.
8. **Surrogate Key:**
   1. It is a synthetic PK.
   2. The DB generates it automatically, usually as an integer.
   3. It may be used as the PK.
   4. In the merged school table, the DB gives each tuple a self-generated integer (1, 2, 3, 4, 5 ...), auto-incremented by 1. It identifies each tuple uniquely and is used as the PK.

## 13. Integrity constraints

1. **CRUD and consistency:** CRUD operations must follow some integrity policy so that the DB is always consistent.
   1. CRUD means Create (add an entry), Read (read without modifying), Update (for example, change the address of customer 1) and Delete (remove an entry).
   2. Every CRUD operation must follow some consistency checks. If not, the DB becomes inconsistent or corrupt.
2. **Purpose:** Constraints exist so that we do not accidentally corrupt the DB.
   1. **Example:** A Student table has roll no, name and contact. Adding roll no "abc" fails with an error if the domain of roll no is integer.
   2. Constraints are defined while designing the DB so that CRUD operations are validated.
3. **Domain constraints:**
   1. They restrict the value in an attribute of a relation. They specify the domain.
   2. They restrict the data type of every attribute. For example, roll no is integer, name is characters, contact is integer.
   3. **Example:** Enrolment is allowed only for candidates with birth year below 2002.
      - Similar example: admission to college is allowed only if age is at least 18.
4. **Entity constraints:**
   1. Every relation should have a PK. PK is not NULL.
   2. Without a non-null PK, tuples cannot be uniquely identified.

   > **Interview:** Entity constraints are very important from the interview perspective.

5. **Referential constraints:**
   1. They are specified between two relations. They help maintain consistency among tuples of the two relations.
   2. A value in the specified attributes of any tuple in the referencing relation must also appear in the specified attributes of at least one tuple in the referenced relation.
   3. If an FK in the referencing table refers to the PK of the referenced table, every FK value must be NULL or available in the referenced table.
   5. Order is the child (referencing) table. Customer is the parent (referenced) table.
   6. **Insert constraint:** A value cannot be inserted in the child table if it is not in the parent table.
      - **Example:** Add order 24 placed by cust_id 4. Customer has no customer 4, so the insert is not allowed. A forced SQL insert throws a foreign key constraint violation error.
   7. **Delete constraint:** A value cannot be deleted from the parent table if it is in the child table.
      - **Example:** Customer 3 requests account deletion. We cannot delete customer 3 (or 1 or 2) while Order has an entry for it.
      - **Reason:** Order 23 (placed by cust_id 3) would reference a customer that no longer exists. That is inconsistency.
   8. **ON DELETE CASCADE:** The value can be deleted from the parent table even if it is in the child table, without violating the delete constraint.
      - The DBMS also deletes the matching child entries. Delete customer 3 and its order is deleted too, so no inconsistency remains.
      - It is defined in SQL at table creation: `CREATE TABLE Order (... cust_id INT, FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE)`. Detailed syntax comes in the SQL lectures.
   9. **ON DELETE NULL (SET NULL):** Can a foreign key be NULL? Yes. When the value is deleted from the parent, the child's entry is not deleted. Instead, the FK value in the child is set to NULL.
      - Delete customer 3. The order row stays and its cust_id becomes NULL. NULL means no customer, because the customer has left the system.
      - The delete constraint is not violated.
      - So an FK is NULL when the parent tuple it referred to has gone from the system.
      > **Interview:** Explain this fully to the interviewer.
6. **Key constraints:** The DBMS has six types of key constraints.
   1. **NOT NULL:** It stops the user from leaving a value NULL. Every element in the database has a value.
      - Key constraints are applied when `CREATE TABLE` is called, that is, when the relation is defined. A column can be NULL by default.
      - **Example:** Customer(id INT NOT NULL, name VARCHAR(50) NOT NULL). VARCHAR(50) means at most 50 characters.
      - The id and name entries can then never be NULL. If a CRUD operation leaves them NULL, the DBMS checks, fails the operation and throws an error.
   2. **UNIQUE:** It ensures all the values in a column are different from each other.
      - Values of that column stay unique across the whole table.
      - It looks like a PK, but a table can have only one PK. It can have many UNIQUE constraints (many unique attributes, for example id unique and name unique).
      - UNIQUE can be applied on more than one column. A PK is applied on one key only.
      - **Example:** Unique usernames. If Ram enrols, no other Ram can enrol.
   3. **DEFAULT:** It sets the default value of a column. The default value is added if no value is specified.
      - **Example:** A column prime_status of a customer in an Amazon-like DB can default to a fixed value.
   4. **CHECK:** It is an integrity constraint. It checks that data integrity is maintained before and after the CRUD operation.
      - It limits the value range (domain) of a column.
      - **Example:** `CHECK (age >= 18)`. Creating a row with age 17 or 16 throws a check (consistency) error. Age 18 or more is allowed.
   5. **PRIMARY KEY:** An attribute or set of attributes that can uniquely identify each entity in the entity set. The PK must be unique and not null.
      - Only one PK per relation. It is defined in the table along with the other attributes, for example cust_id is the primary key.
   6. **FOREIGN KEY:** Whenever there is a relationship between two entities, they must have a common attribute. This common attribute is the primary key of one entity set and becomes the foreign key of the other. This key prevents every action that could break the connection between tables.
      - It keeps the relation between two tables.
      - It is defined in Order's `CREATE TABLE`: PK is order_id, and FK is cust_id REFERENCING Customer(cust_id).
      - **Example:** The common attribute cust_id is the PK in Customer and an FK in Order.
      - **Referential constraint (summary):** It is specified between two relations and helps maintain consistency among tuples of the two relations. When something is deleted from the parent, the child can be given an action: delete the entry, throw an error, or set the FK to NULL.

## 14. Implementation

- **RDBMS:** The relational model is implemented through software, an RDBMS: Oracle, IBM, MySQL, MS SQL Server and others.

## 15. ER and relational model

- **Interconvertible:** An ER model can be converted to tables, and a relational model designed from it (next lecture).
