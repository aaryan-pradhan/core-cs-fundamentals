# Lecture 7: Relational Model

1. Relational Model (RM) organises the data in the form of **relations (tables)**.
    1. RM is a data model, like the ER model. It describes data, relationships within the data, and data consistency constraints.
    2. A table and a relation are the same thing. Do not get confused between the two.
    3. Database design is done in steps. Step 1: build the ER model (ER diagram). Step 2: convert the ER model into the relational model. Step 3: an RDBMS implements the relational model (`CREATE TABLE` etc.).
    4. Conversion ER to RM: each entity becomes a separate table, each attribute of the entity becomes a column of that table. (Multivalued and composite attributes, and relationships, are covered in the next lecture.)
    5. Example: entity Customer (cust_id, name, address, contact_no) becomes table Customer with those 4 columns.

        | cust_id | name | address | contact_no |
        |---|---|---|---|
        | 1 | Lakshya | ... | ... |
        | 2 | Raj | ... | ... |

    6. Example: online delivery system ER model gives two tables. Customer(cust_id, name, address, contact_no) with PK cust_id. Order(order_id, timestamp, delivery_date) with PK order_id. Timestamp is the time the order was placed.
2. A relational DB consists of **collection of tables**, each of which is assigned a **unique name.**
3. A **row** in a table represents a relationship among a set of values, and table is collection of such relationships.
    1. Each row is a set of values that together define one customer (here the 4 values define one customer).
4. **Tuple**: A single row of the table representing a single data point / a unique record.
    1. Each tuple of the Customer table represents one customer.
5. **Columns**: represents the attributes of the relation. Each attribute, there is a permitted value, called **domain of the attribute.**
6. **Relation Schema**: defines the design and structure of the relation, contains the name of the relation and all the columns/attributes.
    1. Way of defining the table: relation name plus its attributes. Example: schema of Customer, schema of Order.
7. Common RM based DBMS systems, aka RDBMS: Oracle, IBM, **MySQL**, MS Access.
    1. RDBMS is the software that implements the relational model.
8. **Degree of table:** number of attributes/columns in a given table/relation.
    1. Customer table with 4 columns has degree 4.
9. **Cardinality**: Total no. of tuples in a given relation.
    1. In the ER model cardinality meant something else; here it is the total number of rows.
    2. Customer table with 2 rows has cardinality 2, i.e. 2 unique customers.
10. **Relational Key**: Set of attributes which can uniquely identify an each tuple.
    1. Applies to table and relation alike.
11. Important **properties** of a **Table** in Relational Model
    1. The name of relation is distinct among all other relation.
        1. Each entity becomes a table, and each entity has a unique name in the ER model, so each table has a unique name in the database.
    2. The values have to be atomic. Can't be broken down further.
        1. E.g., a contact number cannot be split into two parts to get a meaning out of them. A name cannot be broken down further.
    3. The name of each attribute/column must be unique.
        1. Similar to the ER diagram: no two attributes with the same name in a relation.
    4. Each tuple must be unique in a table.
        1. No redundant (extra) rows. E.g., a second row with cust_id 1 and name Lakshya, same as the existing one, is not wanted: the data of cust_id 1 is already stored, so do not store it again.
    5. The sequence of row and column has no significance.
        1. Name, address, contact can be written in any order; only all attributes must be defined.
    6. Tables must follow integrity constraints - it helps to maintain data consistency across the tables.
12. **Relational Model Keys**
    1. **Super Key** (**SK**): Any P&C of attributes present in a table which can uniquely identify each tuple.
        1. P&C = any permutation and combination of attributes, which together uniquely identify every tuple.
        2. E.g., in Customer: {cust_id}, {cust_id, email}, {contact, email}, {cust_id, name, contact, email}. Any such P&C that uniquely identifies each tuple is a super key.
    2. **Candidate Key** (**CK**): minimum subset of super keys, which can uniquely identify each tuple. It contains no redundant attribute.
        1. Take a super key like {cust_id, name, contact, email}. Name cannot identify uniquely (two customers can have the same name), so name is a redundant attribute here. Remove such attributes; what remains is a candidate key.
        2. E.g., candidate keys: {cust_id}, {contact}, {email}, {cust_id, contact} and {cust_id, email} as listed in the lecture (name is removed from every super key since it can repeat).
        3. Every candidate key is a super key, not the other way round.
        4. **CK value shouldn't be NULL.**
        5. A super key can be NULL (it is a superset, and in set maths a superset can include NULL entries); a candidate key cannot.
    3. **Primary Key** (**PK**):
        1. Selected out of CK set, has the least no. of attributes.
        2. Candidate keys can all identify uniquely, but only one is given the chance to be PK: the shortest one, with the minimum number of attributes. E.g., choose cust_id as PK.
    4. **Alternate Key** (**AK**)
        1. All CK except PK.
        2. AK = set of CK minus PK.
    5. **Foreign Key** (**FK**)
        1. It creates relation between two tables.
        2. A relation, say r1, may include among its attributes the PK of an other relation, say r2. This attribute is called FK from r1 referencing r2.
        3. The relation r1 is aka **Referencing (Child) relation** of the FK dependency, and r2 is called **Referenced (Parent) relation** of the FK.
        4. FK helps to cross reference between two different relations.
        5. Why needed: the ER diagram has the relationship "Customer places Order" (the diamond). In the tables Customer and Order, the relationship must also be shown. RM provides FK for this.
        6. How: take the PK of one table and add it as an attribute in the other table. Add cust_id to Order. cust_id is the PK of Customer, so in Order it is a foreign key.
        7. Example Order table: (order_id 21, cust_id 1), (22, 2), (23, 3). Customer 1 placed order 21, customer 2 placed order 22, customer 3 placed order 23.
        8. Cross reference: to find who placed order 21, look at its FK value (1), go to the Customer table and read all the details of customer 1.
        9. The ER relationship diamond is converted into the FK inside the Order table.
        10. The table in which the FK is added (Order) is the child / referencing relation. The table whose PK is used as FK (Customer) is the parent / referenced relation. This nomenclature is used later.
    6. **Composite** Key: PK formed using at least 2 attributes.
    7. **Compound** Key: PK which is formed using 2 FK.
        1. Example: two schools A and B each keep their own registration numbers (A: 101, 102, 103; B: B101, B102 and so on). The tables are independent. When merging them into one table, the registration number alone cannot be used as PK.
    8. **Surrogate** Key:
        1. Synthetic PK.
        2. Generated automatically by DB, usually an integer value.
        3. May be used as PK.
        4. In the merged school table, the DB assigns each tuple a self-generated integer (1, 2, 3, 4, 5 ...), auto-incremented by 1. It identifies each tuple uniquely and is used as the PK.
13. **Integrity Constraints**
    1. CRUD Operations must be done with some integrity policy so that DB is always consistent.
        1. CRUD = Create (add an entry), Read (read without modifying), Update (e.g. change the address of customer 1), Delete (remove an entry).
        2. Every CRUD operation must follow some consistency checks. If not, the DB becomes inconsistent / corrupt.
    2. Introduced so that we do not accidentally corrupt the DB.
        1. Example: a Student table with roll no, name, contact. A create request adds a student with roll no "abc" (not an integer). If the domain of roll no is defined as integer, the DB checks, the operation fails and throws an error.
        2. Constraints are defined while designing the DB so that CRUD operations are validated.
    3. **Domain Constraints**
        1. Restricts the value in the attribute of relation, specifies the Domain.
        2. Restrict the Data types of every attribute.
            1. E.g., roll no is integer, name is characters, contact is integer.
        3. E.g., We want to specify that the enrolment should happen for candidate birth year < 2002.
            1. Similar example: age >= 18, only then admission to college is allowed.
    4. **Entity Constraints**
        1. Every relation should have PK. PK != NULL.
        2. Without a non-null PK, tuples cannot be uniquely identified.
        3. Very important from the interview perspective.
5.   **Referential Constraints**
     1. Specified between two relations & helps maintain consistency among tuples of two relations.
     2. It requires that the value appearing in specified attributes of any tuple in referencing relation also appear in the specified attributes of at least one tuple in the referenced relation.
     3. If FK in referencing table refers to PK of referenced table then every value of the FK in referencing table must be NULL or available in referenced table.
     4. FK must have the matching PK for its each value in the parent table or it must be NULL.
     5. Order is the child / referencing table, Customer is the parent / referenced table.
     6. Insert constraint: a value cannot be inserted in the child table if the value is not lying in the parent table.
         1. Example: add order 24 (timestamp, delivery date) placed by cust_id 4. The Customer table has no customer 4. The insert is not allowed. If forced with an SQL insert, the DBMS throws a foreign key constraint violation error.
     7. Delete constraint: a value cannot be deleted from the parent table if the value is lying in the child table.
         1. Example: customer 3 requests account deletion. Cannot delete customer 3 from Customer while Order has an entry for it. Same for customers 1 and 2.
         2. Reason: if customer 3 were deleted, fetching order 23 (placed by cust_id 3) would reference a customer that no longer exists. That is inconsistency.
     8. **ON DELETE CASCADE**: the value can be deleted from the parent table even if it lies in the child table, without violating the delete constraint.
         1. When a tuple is deleted from the parent, the DBMS also deletes the corresponding entries in the child table. Delete customer 3: its order in Order is deleted too. Both are gone, so no inconsistency remains.
         2. Defined in SQL at table creation: `CREATE TABLE Order (... cust_id INT, FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE)`. Detailed syntax comes in the SQL lectures.
     9. Can a foreign key be NULL? Yes. **ON DELETE NULL** (SET NULL): when the value is deleted from the parent, instead of deleting the child's corresponding entry, the FK value in the child is set to NULL.
         1. Delete customer 3: the order row stays, its cust_id becomes NULL. It no longer points to a customer that does not exist; NULL means it does not specify any customer (customer has left the system).
         2. The delete constraint is not violated.
         3. So FK is NULL when the parent tuple it referred to has gone from the system. Explain this fully to the interviewer.
6.   **Key Constraints:** The six types of key constraints present in the Database management system are:-
     1. NOT NULL:  This constraint will restrict the user from not having a NULL value. It ensures that every element in the database has a value.
         1. Key constraints are applied when `CREATE TABLE` is called, i.e. when the relation is defined. A column can be NULL by default.
         2. Example: Customer(id INT NOT NULL, name VARCHAR(50) NOT NULL). VARCHAR(50) means at most 50 characters.
         3. The id and name entries can then never be NULL. If a CRUD operation leaves them NULL, the DBMS checks, fails the operation and throws an error.
     2. UNIQUE: It helps us to ensure that all the values consisting in a column are different from each other.
         1. Values of that column stay unique across the whole table.
         2. Looks like PK, but a table can have only one PK, while it can have many UNIQUE constraints (many unique attributes, e.g. id unique, name unique).
         3. UNIQUE can be applied on more than one column; PK is applied on one key only.
         4. Example: usernames made unique, so if someone named Ram enrolls, no other Ram can enroll.
     3. DEFAULT: it is used to set the default value to the column. The default value is added to the columns if no value is specified for them.
         1. Example: a column prime_status of a customer in an Amazon-like DB can default to a fixed value.
     4. CHECK: It is one of the integrity constraints in DBMS. It keeps the check that integrity of data is maintained before and after the completion of the CRUD.
         1. Limits the value range / domain of a column.
         2. Example: `CHECK (age >= 18)`. On a create operation with age 17 or 16, the DB checks before inserting; if age >= 18 the entry is allowed, otherwise it throws a check (consistency) error.
     5. PRIMARY KEY: This is an attribute or set of attributes that can uniquely identify each entity in the entity set. The primary key must contain unique as well as not null values.
         1. Only one PK per relation. Defined in the table along with the other attributes, e.g. cust_id is the primary key.
     6. FOREIGN KEY: Whenever there is some relationship between two entities, there must be some common attribute between them. This common attribute must be the primary key of an entity set and will become the foreign key of another entity set. This key will prevent every action which can result in loss of connection between tables.
         1. Keeps the relation between two tables.
         2. Defined in Order's `CREATE TABLE`: PK is order_id, and FK is cust_id REFERENCING Customer(cust_id).
         3. Example: the common attribute cust_id is the PK in Customer and an FK in Order.
         4. Referential constraint (summary): specified between two relations, helps maintain consistency among tuples of the two relations. When something is deleted from the parent, the child can be given an action: delete the entry, throw an error, or set the FK to NULL.
7. The relational model is implemented through software, an RDBMS: Oracle, IBM, MySQL, MS SQL Server and others.
8. ER model and relational model are interconvertible: an ER model can be converted to tables and a relational model designed from it (next lecture).
