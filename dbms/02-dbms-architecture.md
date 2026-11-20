# Lecture 2: DBMS Architecture

## 1. View of Data (Three Schema Architecture)

- a. The major purpose of DBMS is to provide users with an abstract view of the data. That is, the system hides certain details of how the data is stored and maintained.
  - Abstraction = simplify the system for users: expose only what the user needs, hide the complicated internal working.
  - Car example: driver uses accelerator, brake, clutch, steering; does not need to know how axle, tyres, gearbox work. Driving licence needs only that.
  - Tally (business software) example: user clicks add/delete/calculate GST, exports balance sheet as PDF; does not know the data structures, where or how the file is saved, which encoding, encryption or compression is used.
  - In a DBMS: user does not care whether data is hashed, in which data structures, in bits and bytes or tables. User only needs to see the data.
  - E.g., school administration only wants to see how many students enrolled this year; not how data is stored or which server it comes from.
- b. To simplify user interaction with the system, abstraction is applied through several levels of abstraction.
- c. The main objective of three level architecture is to enable multiple users to access the same data with a personalized view while storing the underlying data only once
  - Example: an online store's DB holds each customer's likes/dislikes, reviews, products bought, most-used credit card, debit card, UPI, age, name, phone number, address.
  - Logistics department needs only name, phone number and address. It must not see card details, UPI, past purchases, likes/dislikes.
  - Customer service department needs name, phone number, address plus the products the customer ordered (for refund/replace of a faulty product).
  - So the DB is stored once (underlying data stored once), but each department gets its own view of the same data.
  - Abstraction is the end goal; the three schema architecture is how it is achieved: the DBMS is divided into three abstract levels.
  - Schema = design (how the thing looks, how it is built). The word "schema" can be replaced by "design".
- d. **Physical level / Internal level**
  - i. The lowest level of abstraction describes how the data are stored.
  - ii. Low-level data structures used.
  - iii. It has **Physical schema** which describes physical storage structure of DB.
  - iv. Talks about: Storage allocation (N-ary tree etc), Data compression & encryption etc.
  - v. **Goal**: We must define algorithms that allow efficient access to data.
  - Example: a profile picture stored in the DB is shown as a picture to the user, but physically it is a collection of bytes (pixels) on disk/SSD. A 100x100 image can be stored with compression such as run-length encoding (say 1 MB becomes 50 KB).
  - Physical schema is a blueprint, like the architect's map of a house before building it (bedroom here, gallery there). It is not the actual thing.
  - Physical schema decides: how data is stored on disk, which compression, which encryption, storage location, small or big blocks, whether hashing is used.
  - Goal is fast access to data. E.g., a compression whose decompression needs a lot of CPU makes access slow, so it is a bad choice. Use data structures that give fast access: binary tree, red-black tree, N-ary tree, tries, dictionary-like structures.
- e. **Logical level / Conceptual level:**
  - i. The **conceptual schema** describes the design of a database at the conceptual level, describes *what* data are stored in DB, and what *relationships* exist among those data.
  - ii. User at logical level does not need to be aware about physical-level structures.
  - iii. **DBA**, who must decide what information to keep in the DB use the logical level of abstraction.
  - iv. **Goal**: ease to use.
  - Logical level = how the data looks logically (not bits and bytes): which data is stored (student, employee) and how it looks, plus relationships.
  - Example, student data:
    - Physical level: a file holding name, phone number, address, batch number of student 1, then the same four of student 2, and so on (e.g. `Ram, 8812..., ..., 201`). Opening the file you cannot tell it is student data; it is only bytes and strings with commas.
    - Logical level: the file is transformed into a table with columns Name, Phone number, Address, Batch number and one row per student. Now it is visibly student data with four attributes.
  - This is the physical level to logical level mapping. The mapping is defined by the logical (conceptual) schema.
  - A second table, Course (course id, name, duration). Each student enrolls in some courses every semester, so the student data also holds a course id.
  - Relationship between the two tables: Student applies for a Course / Courses are applied by Student.
  - At the physical level both are just files of strings and integers (name = string, phone = integer, course id = integer); you cannot tell which is student or course or how they are related. At the logical level you can.
  - Physical data independence: if the physical schema changes, the logical level is unaffected.
    - E.g., move the file from disk to SSD for faster access: the user at the logical level is not affected.
    - E.g., split the file into four files (all names, all phone numbers, all addresses, all batches). Only the mapping changes (first string of file 1 is the name, first integer of file 2 is the phone number, and so on). Student still looks the same at the logical level: name, phone number, address, batch.
    - The change is handled entirely at the physical level.
- f. **View level / External level:**
  - i. Highest level of abstraction aims to simplify users’ interaction with the system by providing different view to different **end**-user.
  - ii. Each **view schema** describes the database part that a particular user group is interested and hides the remaining database from that user group.
  - iii. At the external level, a database contains several schemas that sometimes called as **subschema**. The subschema is used to describe the different view of the database.
  - iv. At views also provide a **security** mechanism to prevent users from accessing certain parts of DB.
  - The user at view level is the end user; does not care about conceptual or physical levels.
  - Example: view schema of Logistics department = (name, address, phone number). View schema of Customer service department = (name, address, phone number, products ordered). Same customer DB, different sub schemas, so different views. This is "view of data".
  - Security: some information (security codes, OTP, secret codes) should not be shown to some user groups, e.g. logistics has no use for it. This is applied at the external level.
- g. (Diagram: three schema architecture)

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

- a. The collection of information stored in the DB at a particular moment is called an **instance** of DB.
  - Example: student table is empty when created. First student enrolls, then a second: at that moment the instance is 2 rows. Next day with a third student, the instance has 3 rows; a year later, thousands. If some students withdraw, the instance shrinks. The table (schema) stays the same; the instance is the data at that point in time.
- b. The overall design of the DB is called the DB **schema**.
- c. Schema is **structural** description of data. Schema **doesn’t change frequently**. Data may change frequently.
  - Physical-level things may change (how data is stored), but the student still looks the same logically.
- d. **DB schema** corresponds to the variable declarations (along with type) in a program.
- e. We have 3 types of **Schemas**: **Physical, Logical**, several **view schemas** called subschemas.
  - The term "DB schema" normally means the logical (conceptual) schema, used as plain jargon.
  - A DB schema contains: attributes of each table (e.g. Student: name, address, batch...), consistency constraints (e.g. name cannot be null, so no student without a name; phone number or address rules), a unique identifier such as student id (primary key, must not be null, else a student cannot be identified), and relationships between tables (Student applies for Course).
- f. Logical schema is most **important** in terms of its effect on application programs, as programmers construct apps by using logical schema.
  - Example: an app that gives loans to students uses the student database. The Student class in the app has name, address, phone number, student id as members, taken from the logical schema. If the class leaves out name, it is wrong.
- g. **Physical data independence**, physical schema change should not affect logical schema/application programs.

## 3. Data Models:

- a. Provides a way to describe the **design** of a DB at **logical level.**
  - Needed when building e.g. a banking system: customers, credit/debit card info, employees, payroll, transactions. You need to design how the data looks logically and what relationships exist between them (employee and payroll, customer and transaction).
- b. Underlying the structure of the DB is the Data Model; a collection of conceptual tools for describing **data, data relationships, data semantics & consistency constraints**.
  - Data: how a student is described (the five or so attributes).
  - Data relationships: e.g. Course and Student.
  - Data semantics: meaning of the data.
  - Consistency constraints: e.g. bank balance must not go below 0.
- c. E.g., **ER** model, **Relational** model, **object-oriented** model, **object-relational** data model etc.
  - Object-relational model = object-oriented model and relational model mixed.
  - Covered in detail in the coming lectures. The data model concept is built on the conceptual (logical) schema.

## 4. Database Languages:

- a. **Data definition language (DDL)** to specify the database schema.
- b. **Data manipulation language (DML)** to express database queries and updates.
- c. **Practically**, both language features are present in a single DB language, e.g., SQL language.
  - A language is needed to interact with the DBMS, like a compiler needs a programming language to convert to machine code.
  - A single language provides both, unlike C++/Java/Python being separate languages. SQL (Structured Query Language) is the example.
  - DDL and DML together form the DB language; queries are a part of it. A query is sent to the DBMS, which understands it, runs it and returns the result.
- d. DDL
  - i. We specify consistency constraints, which must be checked, every time DB is updated.
  - DDL defines the schema (student table with student id, name, address, phone number) and its constraints. E.g. student id and name not null, phone number 10 digits.
  - Constraints keep the DB consistent and uncorrupted after every modification. E.g. a student giving a 5 digit mobile number cannot be entered; an error comes.
  - Example (SQL): `CREATE TABLE Student (` student id INT, name VARCHAR(50), address VARCHAR(50), phone INT `)`. Name limited to 50 characters is a consistency constraint.
- e. DML
  - i. Data manipulation involves
    1. **Retrieval** of information stored in DB.
    2. **Insertion** of new information into DB.
    3. **Deletion** of information from the DB.
    4. **Updating** existing information stored in DB.
  - ii. **Query language**, a part of DML to specify statement requesting the retrieval of information.
  - E.g. a student leaves: delete; address changes: update; principal asks for all students living at a particular address or pin code: retrieve.
  - Example (SQL): `SELECT * FROM Student;` (`*` means everything) retrieves all students.

## 5. How is Database accessed from Application programs?

- a. Apps (written in host languages, C/C++, Java) interacts with DB.
  - The DBMS understands SQL (DB language), but the app is in a host language (JavaScript, C++, Python, Java). Two incompatible entities need an interface.
- b. E.g., Banking system’s module generating payrolls access DB by executing DML statements from the host language.
- c. API is provided to send DML/DDL statements to DB and retrieve the results.
  - The API/package converts the host language's statements/packets into actual SQL queries, sends them to the DBMS, and converts the returned data back into a data structure of the host language.
  - i. Open Database Connectivity (**ODBC**), Microsoft “C”.
  - ii. Java Database Connectivity (**JDBC**), Java.
  - Example: a Java Spring Boot backend uses JDBC; SQL like `INSERT INTO candidate (name, phone...)` is written as strings/templates in Java and sent via JDBC to the SQL server (the DBMS); the result comes back through JDBC into Java data structures.
  - Interview point: know how a host language app communicates with SQL (JDBC for Java, ODBC for C/C++).

## 6. Database Administrator (DBA)

- a. A person who has **central control** of both the data and the programs that access those data.
  - Example: the Aadhaar DB is used by Income Tax, EPF, Home Ministry etc. Each has its own view schema; the DBA knows which programs/APIs access the data and has central control of it.
  - DBA mostly works at the logical level; end users work at the view level.
- b. **Functions** of DBA
  - i. Schema Definition
    - Defining the schema: what attributes a student has, storage structure.
  - ii. Storage structure and access methods.
  - iii. Schema and physical organization modifications.
    - Any change to the physical or logical schema is the DBA's job. E.g. the school committee wants Aadhaar stored with each student: add a new attribute (column), change the organization, and possibly relationships with course/professor data.
  - iv. Authorization control.
    - Who can access which data and what each sees.
  - v. Routine maintenance
    1. Periodic backups.
       - Keep copies on multiple servers; losing one DB server must not delete the data, which is collected over years.
    2. Security patches.
       - Apply latest patches for vulnerabilities (e.g. hackers reaching Aadhaar or NIC data).
    3. Any upgrades.
       - E.g. physical schema/design changes to make access faster.
  - Interview question: who is a DBA and what are its functions.

## 7. DBMS Application Architectures: Client machines, on which remote DB users work, and server machines on which DB system runs.

- Client machine: where the end user works. Server machine: where the DB system actually runs. The architecture defines how these are arranged.
- a. **T1** Architecture
  - i. The client, server & DB all present on the same machine.
  - E.g. a localhost server while developing a web app, or learning SQL: you are the client, the DBMS server runs on your own PC and the DB is stored as files on it.
  - Use it for an app you alone use on your own computer.
- b. **T2** Architecture
  - i. App is partitioned into 2-components.
  - ii. Client machine, which invokes DB system functionality at server end through query language statements.
  - iii. API standards like **ODBC** & **JDBC** are used to interact between client and server.
  - Client app (host application) sends SQL query statements directly over the network to a remote server where the DBMS runs; the DBMS runs them and returns output.
  - Use it e.g. on a home local area network (family devices), where security is not a big issue.
- c. **T3** Architecture
  - i. App is partitioned into 3 logical components.
  - ii. Client machine is just a frontend and doesn’t contain any direct DB calls.
  - iii. Client machine communicates with App server, and App server communicated with DB system to access data.
  - iv. **Business** logic, what action to take at that condition is in App server itself.
  - v. T3 architecture are best for **WWW** Applications.
  - vi. **Advantages**:
    1. **Scalability** due to distributed application servers.
       - Many clients and many application servers can be used to serve billions of people.
    2. **Data integrity**, App server acts as a middle layer between client and DB, which minimize the chances of data corruption.
       - A malicious or buggy user query that could corrupt the DB is filtered out at the app server layer.
    3. **Security**, client can’t directly access DB, hence it is more secure.
       - The app server is a guard in between. Used by large applications, since users can be anywhere in the world. The Spring Boot JDBC code shown earlier was app server code of a WWW application.
  - Flow: client -> app server -> DB; the DB returns data to the app server, which processes it and sends it to the client.

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
