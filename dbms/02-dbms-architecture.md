# Lecture 2: DBMS Architecture

## 1. View of Data (Three Schema Architecture)

- a. The major purpose of a DBMS is to give users an abstract view of the data. The system hides details of how data is stored and maintained.
  - **Abstraction:** Expose only what the user needs. Hide the complicated internal working.
  - **Car:** The driver uses accelerator, brake, clutch and steering. The driver does not need to know the axle, tyres or gearbox.
  - **Tally:** The user clicks add, delete or calculate GST, and exports a balance sheet as PDF. The user does not know the data structures, file location, encoding, encryption or compression.
  - **In a DBMS:** The user does not care whether data is hashed, in which data structures, or in bits and bytes or tables. The user only sees the data. For example, a school administration only wants to see how many students enrolled this year.
- b. To simplify user interaction, abstraction is applied through several levels.
- c. The main objective of the three level architecture is to let multiple users access the same data with a personalized view. The underlying data is stored only once.
  - **Online store:** The DB holds each customer's likes and dislikes, reviews, products bought, most-used credit card, debit card, UPI, age, name, phone number and address.
  - **Logistics department:** It needs only name, phone number and address. It must not see card details, UPI, past purchases, or likes and dislikes.
  - **Customer service department:** It needs name, phone number, address and the products ordered, to refund or replace a faulty product.
  - **Result:** The DB is stored once. Each department gets its own view.
  - **Goal and method:** Abstraction is the goal. The three schema architecture achieves it by dividing the DBMS into three abstract levels.
  - **Schema:** A schema is a design. You can read "schema" as "design".
- d. **Physical level / Internal level**
  - i. It is the lowest level of abstraction. It describes how the data is stored.
  - ii. It uses low-level data structures.
  - iii. It has the **physical schema**. This describes the physical storage structure of the DB.
  - iv. It covers storage allocation (N-ary tree and so on), data compression and encryption.
  - v. **Goal:** We must define algorithms that allow efficient access to data.
  - **Picture example:** A profile picture is shown as a picture. Physically it is bytes (pixels) on disk or SSD. A 100x100 image can be compressed with run-length encoding, for example 1 MB to 50 KB.
  - **Analogy:** The physical schema is the architect's blueprint of a house. It is not the house.
  - **What it decides:** How data is stored on disk, compression, encryption, storage location, small or big blocks, and whether hashing is used.
  - **Fast access:** A compression whose decompression needs a lot of CPU makes access slow, so it is a bad choice. Use fast data structures: binary tree, red-black tree, N-ary tree, tries, and dictionary-like structures.
- e. **Logical level / Conceptual level**
  - i. The **conceptual schema** describes the design of a database at the conceptual level. It describes *what* data is stored and what *relationships* exist among it.
  - ii. A user at the logical level does not need to know the physical-level structures.
  - iii. The **DBA** uses the logical level. The DBA decides what information to keep in the DB.
  - iv. **Goal:** ease of use.
  - **Meaning:** The logical level shows how data looks logically (not bits and bytes): which data is stored (student, employee), how it looks, and the relationships.
  - **Student data example:**
    - **Physical level:** A file holds name, phone number, address and batch number of student 1, then the same four for student 2, and so on (for example `Ram, 8812..., ..., 201`). You cannot tell it is student data. It is only bytes and strings with commas.
    - **Logical level:** The file becomes a table with columns Name, Phone number, Address and Batch number, one row per student. Now it is visibly student data with four attributes.
  - **Mapping:** This is the physical to logical mapping. The logical (conceptual) schema defines it.
  - **Second table:** Course has course id, name and duration. Each student enrolls in some courses every semester, so student data also holds a course id.
  - **Relationship:** Student applies for a Course. Courses are applied by Student.
  - **Physical versus logical view:** At the physical level, both tables are files of strings and integers. You cannot tell which is student or course, or how they relate. At the logical level you can.
  - **Physical data independence:** If the physical schema changes, the logical level is unaffected.
    - **Disk to SSD:** You move the file from disk to SSD for faster access. The logical user is not affected.
    - **Split file:** You split the file into four files (all names, all phone numbers, all addresses, all batches). Only the mapping changes. The first string of file 1 is the name, the first integer of file 2 is the phone number, and so on. The student still looks the same logically.
    - **Where handled:** Entirely at the physical level.
- f. **View level / External level**
  - i. It is the highest level of abstraction. It simplifies users' interaction by giving a different view to each **end** user.
  - ii. Each **view schema** describes the part of the database a particular user group is interested in. It hides the rest from that group.
  - iii. At the external level, a database contains several schemas, sometimes called **subschemas**. A subschema describes a different view of the database.
  - iv. Views also give a **security** mechanism. They stop users from accessing certain parts of the DB.
  - **End user:** The user at the view level does not care about the conceptual or physical levels.
  - **Example:** The Logistics view schema is (name, address, phone number). The Customer service view schema is (name, address, phone number, products ordered). It is the same customer DB with different subschemas. This is the "view of data".
  - **Security:** Some information (security codes, OTP, secret codes) should not be shown to some groups, for example Logistics. This is applied at the external level.
- g. Diagram: three schema architecture

```
 External Schema     +----------------+    +----------------+
                     | External Level |    | External Level |
                     +----------------+    +----------------+
                               ^   \           /   ^
                               |    v         v    |
                                +----------------+      External / Conceptual
 Conceptual Schema              |Conceptual Level|      Mapping
                                +----------------+
                                        ^
                                        |                Conceptual / Internal
                                        v                Mapping
 Internal Schema                +----------------+
                                | Internal Level |
                                +----------------+
                                        |
                                        v
                                    (Database)
```

## 2. Instances and Schemas

- a. The collection of information stored in the DB at a particular moment is called an **instance** of the DB.
  - **Example:** The student table is empty when created. With 2 students, the instance is 2 rows. A day later with a third, it is 3 rows. A year later, thousands. If students withdraw, it shrinks.
  - **Schema versus instance:** The table (schema) stays the same. The instance is the data at that point in time.
- b. The overall design of the DB is called the DB **schema**.
- c. A schema is a **structural** description of data. A schema **does not change frequently**. Data may change frequently.
  - Physical-level things may change. The student still looks the same logically.
- d. A **DB schema** corresponds to the variable declarations (along with type) in a program.
- e. There are 3 types of **schemas**: **physical**, **logical**, and several **view schemas** called subschemas.
  - **Jargon:** "DB schema" normally means the logical (conceptual) schema.
  - **A DB schema contains:**
    - **Attributes:** The attributes of each table (for example Student: name, address, batch).
    - **Consistency constraints:** For example, name cannot be null, so no student exists without a name. Phone number or address rules also count.
    - **Unique identifier:** For example, student id (the primary key). It must not be null. Otherwise a student cannot be identified.
    - **Relationships:** The relationships between tables (Student applies for Course).
- f. The logical schema is most **important** in its effect on application programs. Programmers build apps from the logical schema.
  - **Example:** An app gives loans to students. Its Student class has name, address, phone number and student id, taken from the logical schema. If the class leaves out name, it is wrong.
- g. **Physical data independence:** A change in the physical schema should not affect the logical schema or application programs.

## 3. Data Models

- a. A data model gives a way to describe the **design** of a DB at the **logical level**.
  - **Example:** A banking system has customers, credit and debit card info, employees, payroll, and transactions. You design how the data looks logically and the relationships (employee and payroll, customer and transaction).
- b. Underlying the structure of the DB is the data model. It is a collection of conceptual tools for describing **data, data relationships, data semantics and consistency constraints**.
  - **Data:** How a student is described (the five or so attributes).
  - **Data relationships:** For example, Course and Student.
  - **Data semantics:** The meaning of the data.
  - **Consistency constraints:** For example, a bank balance must not go below 0.
- c. Examples are the **ER** model, **relational** model, **object-oriented** model, and **object-relational** data model.
  - **Object-relational model:** It mixes the object-oriented and relational models.
  - **Later:** These are covered in the coming lectures. The data model concept is built on the conceptual (logical) schema.

## 4. Database Languages

- a. **Data definition language (DDL)** specifies the database schema.
- b. **Data manipulation language (DML)** expresses database queries and updates.
- c. **In practice**, both are in a single DB language, for example SQL (Structured Query Language).
  - **Why a language:** You need a language to interact with the DBMS, like a compiler needs a programming language.
  - **Single language:** One language provides both. C++, Java and Python are separate languages, but DDL and DML are not.
  - **Queries:** A query is part of the DB language. It is sent to the DBMS, which understands it, runs it and returns the result.
- d. DDL
  - i. We specify consistency constraints. They must be checked every time the DB is updated.
  - **Role:** DDL defines the schema (a student table with student id, name, address, phone number) and its constraints. For example, student id and name are not null, and phone number is 10 digits.
  - **Purpose of constraints:** They keep the DB consistent and uncorrupted after every modification. For example, a 5 digit mobile number cannot be entered. An error comes.
  - **Example (SQL):** `CREATE TABLE Student (` student id INT, name VARCHAR(50), address VARCHAR(50), phone INT `)`. Limiting name to 50 characters is a consistency constraint.
- e. DML
  - i. Data manipulation involves:
    1. **Retrieval** of information stored in the DB.
    2. **Insertion** of new information into the DB.
    3. **Deletion** of information from the DB.
    4. **Updating** existing information stored in the DB.
  - ii. A **query language** is a part of DML. It specifies a statement that requests retrieval of information.
  - **Examples:** A student leaves, so you delete. An address changes, so you update. The principal asks for all students at an address or pin code, so you retrieve.
  - **Example (SQL):** `SELECT * FROM Student;` retrieves all students. The `*` means everything.

## 5. How is Database accessed from Application programs?

- a. Apps (written in host languages such as C/C++ and Java) interact with the DB.
  - **Mismatch:** The DBMS understands SQL. The app is in a host language (JavaScript, C++, Python, Java). Two incompatible entities need an interface.
- b. **Example:** A banking system's payroll module accesses the DB by executing DML statements from the host language.
- c. An API sends DML and DDL statements to the DB and retrieves the results.
  - **What the API does:** It converts the host language's statements or packets into SQL queries and sends them to the DBMS. It converts the returned data into a host language data structure.
  - i. Open Database Connectivity (**ODBC**), Microsoft "C".
  - ii. Java Database Connectivity (**JDBC**), Java.
  - **Spring Boot:** A Java Spring Boot backend writes SQL like `INSERT INTO candidate (name, phone...)` as strings or templates in Java. JDBC sends it to the SQL server (the DBMS). The result comes back through JDBC into Java data structures.

  > **Interview:** Know how a host language app communicates with SQL. Use JDBC for Java and ODBC for C/C++.

## 6. Database Administrator (DBA)

- a. The DBA is a person who has **central control** of both the data and the programs that access that data.
  - **Aadhaar:** The Aadhaar DB is used by Income Tax, EPF, Home Ministry and others. Each has its own view schema. The DBA knows which programs and APIs access the data.
  - **Levels:** The DBA mostly works at the logical level. End users work at the view level.
- b. **Functions** of the DBA
  - i. **Schema definition:** Define what attributes a student has, and the storage structure.
  - ii. **Storage structure and access methods**
  - iii. **Schema and physical organization modifications:** Any change to the physical or logical schema is the DBA's job.
    - **Example:** The school committee wants Aadhaar stored with each student. The DBA adds a new attribute (column) and changes the organization. Relationships with course or professor data may change.
  - iv. **Authorization control:** Who can access which data and what each user sees.
  - v. **Routine maintenance**
    1. **Periodic backups:** Keep copies on multiple servers. Losing one DB server must not delete data collected over years.
    2. **Security patches:** Apply the latest patches for vulnerabilities. For example, hackers may reach Aadhaar or NIC data.
    3. **Any upgrades:** For example, physical schema or design changes to make access faster.

  > **Interview:** Who is a DBA, and what are its functions?

## 7. DBMS Application Architectures

Client machines are where remote DB users work. Server machines are where the DB system runs. The architecture defines how these are arranged.

- a. **T1** Architecture
  - i. The client, server and DB are all on the same machine.
  - **Example:** A localhost server while developing a web app or learning SQL. You are the client. The DBMS server runs on your PC. The DB is stored as files on it.
  - **Use:** An app that only you use on your own computer.
- b. **T2** Architecture
  - i. The app is partitioned into 2 components.
  - ii. The client machine invokes DB system functionality at the server end through query language statements.
  - iii. API standards like **ODBC** and **JDBC** are used between client and server.
  - **Flow:** The client app (host application) sends SQL statements directly over the network to a remote server where the DBMS runs. The DBMS runs them and returns the output.
  - **Use:** For example, a home local area network (family devices), where security is not a big issue.
- c. **T3** Architecture
  - i. The app is partitioned into 3 logical components.
  - ii. The client machine is just a frontend. It has no direct DB calls.
  - iii. The client machine communicates with the app server. The app server communicates with the DB system.
  - iv. **Business** logic (what action to take under which condition) is in the app server.
  - v. T3 is best for **WWW** applications.
  - vi. **Advantages:**
    1. **Scalability:** Application servers are distributed. Many clients and app servers can serve billions of people.
    2. **Data integrity:** The app server is a middle layer between client and DB. It filters out a malicious or buggy query that could corrupt the DB.
    3. **Security:** The client cannot directly access the DB. The app server is a guard in between. Large applications use it, since users can be anywhere in the world.
  - **Spring Boot link:** The Spring Boot JDBC code shown earlier was app server code of a WWW application.
  - **Flow:** The client calls the app server. The app server calls the DB. The DB returns data to the app server, which processes it and sends it to the client.

```
 a. two-tier architecture          b. three-tier architecture

 +-----------------+               +---------------------+
 |      user       |               |        user         |
 | +-------------+ |               | +-----------------+ |
 | | application | |   client      | | application     | |
 | +-------------+ |               | | client          | |
 +-------|---------+               | +-----------------+ |
         |                         +----------|----------+
      network                               network
         |                         +----------|----------+
 +-------|---------+               | +-----------------+ |
 | +-------------+ |   server      | | application     | |
 | | database    | |               | | server          | |
 | | system      | |               | +-----------------+ |
 | +-------------+ |               | | database system | |
 +-----------------+               | +-----------------+ |
                                   +---------------------+
```
