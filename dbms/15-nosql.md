# Lecture 15: NoSQL

## 1. What NoSQL is

NoSQL databases (also called "not only SQL") are non-tabular databases. They store data differently than relational tables. The main types are document, key-value, wide-column, and graph. They provide flexible schemas and scale easily with large data and high user loads.

- **Schema free:** There is no fixed schema.
- **Flexible structures:** Data structures are not tabular and adjust dynamically.
- **Big data:** It handles huge amounts of data.
- **Open source:** Most NoSQL databases are open source and scale horizontally.
- **Storage format:** It just stores data in some format other than relational.
- **Meaning of the name:** "Not only SQL" does not mean queries cannot run. MongoDB has queries. The name means something beyond SQL.
- **Non-tabular:** Tables are not related to each other. Everything about an entity is stored together. For example, there is no separate hobbies table and person table.
- **SQL needs structure:** A fixed schema plus integrity constraints. For example, Student(name, age, address, roll no) has roll no as the primary key. A rule such as "admit only if age > 13" must hold before an entry is allowed.
- **NoSQL stores:** Structured, unstructured and semi-structured data.

| Data type | Examples |
|-----------|----------|
| Unstructured | Text files, social media chats, CCTV, survey and scientific data dumped for many days. |
| Semi-structured | Email. The "to" and "from" header is structured, and the body is unstructured. Every bank or sender writes in its own structure. |
| Structured | A student table, an employee database (fixed schema). |

- **SQL and unstructured data:** SQL cannot store it as-is. You must process it into structure first. Structured data is the primary requirement of SQL.
- **Flexible schema:** Not all information has to be present. For example, only some columns of a student may be available. Being non-tabular, no rule says every column must be filled.
- **Scope:** This is only a brief introduction. Learn the relational model first, and then every other model is easy. For depth, study MongoDB separately.

## 2. History behind NoSQL

NoSQL databases emerged in the late 2000s, as the cost of storage dropped dramatically. Developers, not storage, became the primary cost of software development. So NoSQL databases optimised for developer productivity. Building a complex, hard-to-manage data model just to avoid duplication was no longer needed.

**Why SQL emerged first:**

- **Expensive storage:** Memory cards cost thousands, and floppy disks were costly.
- **SQL answer:** Structure the data, normalise it, keep no redundancy, and store the minimum data in an optimised way.
- **Retrieval:** Tables are linked by foreign keys, and joins (inner join, outer join) are applied. This needs processing, so SQL is not that fast.

**Why NoSQL emerged:**

- **Cheaper storage:** Databases emerged that focus on fast access. Data may be redundant, since terabytes are available, but it must be served within seconds.
- **Redundancy NoSQL accepts:** Storing branch and HOD information inside each student's data (the normalisation example), repeated for every student.
- **More unstructured data:** Defining a schema in advance became costly. Emails, scientific data and survey data need pre-processing, and normalisation splits them across tables (this goes to table A, that to table B, that to table C).
- **Flexibility:** Developers can store huge amounts of unstructured data.
- **Rapid change:** Software needs to adapt quickly to changing requirements. Developers needed to iterate and change things all the way down to the database.
- **Cloud computing:** Developers began hosting applications and data on public clouds. They wanted to distribute data across multiple servers and regions for resilience, scale out instead of scale up, and geo-place their data. Some NoSQL databases, such as MongoDB, provide these.
- **Business use case:** Many servers serve many people, and data must arrive within seconds. This grew with cloud computing and faster internet (4G/5G). Necessity is the mother of invention.

## 3. NoSQL databases: advantages

### A. Flexible schema

An RDBMS has a pre-defined schema. This is an issue when we lack some data or need to change the schema. Changing it on the go is a huge task.

**Data modelling example:**

| | SQL | NoSQL (JSON / JavaScript object) |
|---|-----|------|
| Layout | A user table (id, first name, last name, cell, city), plus a separate hobbies table (user id, hobby) after normalisation. Hobby is a multi-valued attribute. | One object `{ id: 1, firstName, lastName, cell, city, hobbies: [ ... ] }`. Hobbies are stored as an array. |
| Result | Data is split across two tables and needs a join. | Everything comes together, so no join is needed. |

- **Drawback:** For even a small piece of information, you must load the whole object into the application. In SQL you could fetch just the needed column or table.
- **Missing fields:** If an entry has no hobbies, no city and no cell number, SQL stores null null null and wastes some space. In NoSQL you create another object without those fields, and nothing is stored for them. This is flexible schema, the biggest advantage.

### B. Horizontal scaling

**Horizontal scaling** (also called scale-out) means bringing on additional nodes to share the load.

- **Relational databases:** This is difficult, because related data is hard to spread across nodes.
- **Non-relational databases:** This is simpler. Collections are self-contained and not coupled relationally, so queries do not have to "join" them across nodes.

**Scaling:** Eventually the disk fills up, or the data grows so large that processing takes too long. Then you must upgrade the system to serve more users, store more data and retrieve faster. There are two types.

| | Vertical scaling (scale-up) | Horizontal scaling (scale-out) |
|---|---|---|
| What | Upgrade the hardware of the single system: RAM, CPU, disk (1 TB disk to 10 TB). | Add additional nodes (another similar DB system). |
| Data | Stays in one node. | Some data stays on the old node. New data goes to new nodes, so the load is balanced. |
| Used by | SQL generally scales this way. | NoSQL. |
| Cost | Always costly. | Many small cheap systems (such as 1 GB RAM each) are more cost efficient. |

> **Interview:** Why can't SQL do horizontal scaling? It is possible but not practical.

- **Tables on separate systems:** T1, T2, T3 sit on System 1, 2, 3. In an extreme case they are in different countries.
- **Join problem:** Meaningful data needs joins on T1, T2, T3. The tables are logically one storage, so all three must first be brought to one node (say System 4) over the network. A join cannot run on half the data.
- **Slow:** Moving tables over the network is slow, and then the join takes time.
- **Unsuitable cases:** Opening a WhatsApp chat and wanting the last two days of chats instantly cannot use SQL. The data is scattered. Structured data must be fetched, un-structured, spread over the message, and then shown. That is very costly in time complexity.
- **NoSQL answer:** Store the data as a document. Redundancy is fine, with no normalisation load. Put related data in one bunch (student, department and branch info together).
- **Self-contained object:** All information is in one object, not coupled relationally, so it can be distributed across nodes. There is no join and no separate JSON object linked by relation.

Scaling horizontally is achieved through **sharding** or **replica sets**.

- **Replica sets:** Multiple servers hold copies of the same data. For example, your Aadhaar data is on server 1 and server 3 of 10. If server 1 goes down, it is read from server 3.

### C. High availability

NoSQL databases are highly available because of auto replication. Whenever any failure happens, data replicates itself to the preceding consistent state.

- **Multiple servers:** Data is replicated on different nodes. If a server fails, another is up, so the data is still accessible. This gives reliability.

### D. Easy insert and read operations

Queries in NoSQL can be faster than in SQL.

- **SQL:** Data is normalised, so a query for one entity needs joins across tables. As tables grow, joins become very costly in time complexity.
- **NoSQL:** Data is stored in a way optimised for queries. All related data sits at one location, so it is read in one go without a join.
- **MongoDB rule of thumb:** Data that is accessed together should be stored together. For example, if user and hobbies are always accessed together, store them together instead of normalising into tables.

**But delete and update operations are difficult:**

- **SQL:** To change, add or delete a hobby, you edit only the hobbies table. That is easy.
- **NoSQL:** You must load the whole object into memory, go into hobbies, and edit (such as delete the bike hobby, add a hobby). So add, update and delete are costly in time.
- **Choice:** If slow writes are fine but you need fast reads (such as chats opened often), NoSQL fits.

### E. Caching mechanism

The chats you talk to most are readily available when you open the app. They are cached in the system and the database, so no heavy load is needed.

### F. Cloud applications

NoSQL fits cloud applications more.

- **Why:** The cloud has multiple servers with spread-out data, and users want fast data (5G). Joining separately stored normalised data is slow.

## 4. When to use NoSQL

1. **Fast-paced agile development.**
   - **Example:** When TikTok was banned, Instagram had no Reels yet and had to build it quickly.
   - **SQL:** Slower. You design the model, avoid redundancy, and create separate tables for multi-valued and composite attributes.
   - **NoSQL:** No worry about duplication or redundancy, so development is fast.

   > **Interview:** If given a cloud application, which DB would you use? Say NoSQL.

2. **Storage of structured and semi-structured data.**
   - **Any type:** Structured, semi-structured and unstructured data can all be stored in NoSQL.
   - **Where NoSQL is not used:** A banking system (credit card and so on) has structured data, usually on a single server. So SQL is used.
   - **Today:** Most normal development is done with NoSQL databases.

3. **Huge volumes of data.**
   - **Web applications:** They have lots of data that must be stored, processed and retrieved quickly. Retrieval is fast in NoSQL.

4. **Requirements for scale-out architecture.**
   - **Horizontal scaling:** When the business needs horizontal scaling with multiple servers, SQL tables would be spread out and joins become hard.

5. **Modern application paradigms like micro-services and real-time streaming.**
   - **Speed:** These operations are fast and need fast access, so NoSQL is used.

## 5. NoSQL DB misconceptions

### a. "Relationship data is best suited for relational databases."

This is a common misconception. NoSQL databases can store relationship data. They just store it differently than relational databases do.

- **Easier modelling:** Related data does not have to be split between tables. It can be nested within a single data structure. You also do not have to visualise and create tables.
- **Example:** User and hobby are related, so they are stored together in one JSON object.
- **Relating documents:** Put an id key in one JSON object whose value is the id of another JSON object. This is like a foreign key. Normally you store related data together, but if needed you can relate two objects this way.

### b. "NoSQL databases don't support ACID transactions."

This is another common misconception. Some NoSQL databases, like MongoDB, do support ACID transactions.

- **In general:** Early NoSQL development did not focus on ACID. That is why banking systems mostly still use SQL. But some, like MongoDB, support it.

## 6. Types of NoSQL data models

### a. Key-value stores

The simplest type of NoSQL database is a key-value store. Every data element is stored as a key-value pair. It has an attribute name (the "key") and a value. A key-value store is like a relational database with only two columns: the key or attribute name (such as "state") and the value (such as "Alaska").

- **One key, one value:** There are no multiple fields or objects (no name and so on). A single value is found for a key, like a binary lookup.
- **Use cases:** Shopping carts, user preferences and user profiles.
  - **Shopping cart:** One hash key per cart item. The first key is the item id with value mobile, the second has value cream, and the third has value monitor.
- **Examples:** Oracle NoSQL, Amazon DynamoDB, Redis. MongoDB also supports key-value.
- **Definition:** A key-value database associates a value with a key. The value can be anything from a number or simple string to a complex object. The key keeps track of the object.
  - **Like a map:** In its simplest form, it is like a dictionary, array or map object in most programming paradigms. But it is stored persistently and managed by a Database Management System (DBMS).
  - **Types:** The key can be a string or integer. The value can be anything: JSON, binary object, string, array.
- **Fast lookup:** Key-value databases use compact, efficient index structures to locate a value by its key quickly and reliably. They are ideal for systems that need to find and retrieve data in constant time.

Use cases where a key-value store is an optimal choice:

- **Real-time random data access:** For example, user session attributes in an online application such as gaming or finance.
- **Caching:** For frequently accessed data or configuration based on keys.
- **Simple queries:** The application is designed on simple key-based queries.

### b. Column-oriented / columnar / C-store / wide-column

The data is stored so that each row of a column sits next to other rows from that same column.

- **SQL is row-wise (row optimised):** All data of a row (such as Matt, Delhi, 27) sits together in memory.
  - This is good when you want the whole row for a key. Reads are fast.
  - Insert needs changes in the middle, so write, update and delete are slow. It is like appending to a linked list versus editing in the middle.
- **Column store:** All names sit together, all cities together, all ages together. Adding a new tuple (Rahul) means adding to each column's place.
  - Reads are fast, but insert is slow in column stores too.
- **Analytics:** A relational database reads data row by row. A column store is organised as a set of columns. So for analytics on a few columns, you read those columns directly without loading unwanted data.
- **Compression:** Columns are often of the same type and compress more efficiently. That makes reads even faster.
- **Aggregation:** Columnar databases quickly aggregate the value of a given column, such as the total sales for the year.
- **Use case:** Analytics.
- **Example:** Average age. Row-wise, memory is read by jumping (such as every third location) to pick up ages. Column-wise, all ages are together. Go to the first age and read all of it in one go. That is fast.
- **When to use:** When analytics and aggregation functions are applied again and again. For example, industrial machine data shown in analytics, average and peak time.
- **Examples:** Cassandra, RedShift, Snowflake.

### c. Document-based stores

This DB stores data in documents similar to JSON (JavaScript Object Notation) objects. Each document contains pairs of fields and values. The values can typically be strings, numbers, booleans, arrays or objects.

- **Versus key-value:** Key-value had one field and one value. A document has multiple fields. A document in the DB is like a JSON object. JSON is widely used on the web to transmit data.
- **Relating documents:** One document can relate to another. For example, a user document (with id) and a contact or access document also have the user id (such as 1). That is like a foreign key, so relations can be applied.
- **Use cases:** E-commerce platforms, trading platforms and mobile app development across industries.
- **ACID:** It supports ACID properties, so it suits transactions.
- **Examples:** MongoDB, CouchDB.
  - MongoDB is used in most use cases. It is the first choice for anyone learning a NoSQL DB for cloud systems.

### d. Graph-based stores

A graph database focuses on the relationship between data elements. Each element is stored as a node (such as a person in a social media graph). The connections between elements are called links or relationships.

- **First-class links:** In a graph database, connections are stored directly. In relational databases, links are implied, using data to express the relationships.
- **Visualised as a graph:** Nodes (vertices) and edges. The edges are the relations.
- **Example:** Facebook friends, and friends of friends. Profiles A, B, C, D, E are stored. Relations are stored as edges: A related to B, B friend of C, and so on. It is mostly used in social media (who follows whom).
- **No join:** The directly related relations are stored, so no join is needed to establish the relation.
- **Versus SQL:** SQL keeps user profile tables plus a separate table with two foreign keys noting who is friend of whom. Then it joins to get the relation. Graph DBs avoid this overhead.
- **Optimised:** A graph database is optimised to capture and search the connections between data elements. It overcomes the overhead of JOINing multiple tables in SQL.
- **Limit:** Very few real-world business systems can survive solely on graph queries. So graph databases usually run alongside other more traditional databases.
- **Use cases:** Fraud detection, social networks and knowledge graphs.
  - **Fraud detection example:** A card is used at this ATM, then at that ATM. Connections are built between them.
- **Examples:** Neo4j, ArangoDB.

## 7. NoSQL databases: disadvantages

### a. Data redundancy

Data models in NoSQL are typically optimised for queries, not for reducing duplication. So NoSQL databases can be larger than SQL databases.

- **Minor drawback:** Storage is so cheap now that most consider this minor. Some NoSQL databases also support compression to reduce the storage footprint.
- **More storage:** The same data for the same use case takes more storage than in SQL, because SQL reduces redundancy by normalisation.
- **Trade-off:** Storage cost versus fast access. Storage is cheap today, so this point can be ignored.

### b. Update and delete operations are costly

Related data is stored all together, as in the earlier example.

### c. No single data model fits all application needs

Depending on the NoSQL type you select, you may not achieve all your use cases in a single database. For example, graph databases are excellent for analysing relationships but may not give what you need for everyday retrieval such as range queries. When selecting a NoSQL database, consider your use cases. Consider whether a general purpose database like MongoDB would be a better option.

- **SQL:** It mostly fulfils all application needs (leaving aside scalability and horizontal scaling).
- **NoSQL:** One data model fulfils one need, and another does not.
- **MongoDB:** It leveraged its document model and modified it so it can also work as a key-value store.

### d. No ACID in general

- **Exception:** MongoDB has implemented it, but it is not supported in all.

### e. No data entry with consistency constraints

- **No constraints:** The database has no consistency constraints of its own.
- **Workaround:** You can add checks in your application before entering data (such as "if age < 13, do not enter"). But the DB itself does not enforce them.

## 8. SQL vs NoSQL

| | SQL Databases | NoSQL Databases |
|---|---|---|
| Data Storage Model | Tables with fixed rows and columns | Document: JSON documents, Key-value: key-value pairs, Wide-column: tables with rows and dynamic columns, Graph: nodes and edges |
| Development History | Developed in the 1970s with a focus on reducing data duplication | Developed in the late 2000s with a focus on scaling and allowing for rapid application change driven by agile and DevOps practices. |
| Examples | Oracle, MySQL, Microsoft SQL Server, and PostgreSQL | Document: MongoDB and CouchDB, Key-value: Redis and DynamoDB, Wide-column: Cassandra and HBase, Graph: Neo4j and Amazon Neptune |
| Primary Purpose | General Purpose | Document: general purpose, Key-value: large amounts of data with simple lookup queries, Wide-column: large amounts of data with predictable query patterns, Graph: analyzing and traversing relationships between connected data |
| Schemas | Fixed | Flexible |
| Scaling | Vertical (Scale-up) | Horizontal (scale-out across commodity servers) |
| ACID Properties | Supported | Not Supported, except in DB like MongoDB etc. |
| JOINS | Typically Required | Typically not required |
| Data to object mapping | Required object-relational mapping | Many do not require ORMs. MongoDB documents map directly to data structures in most popular programming languages. |

Notes on each row:

1. **Data storage model:** If a column has no entry for a tuple in SQL, null is stored. NoSQL has JSON documents, key-value pairs, columnar tables with rows and dynamic columns, and graph nodes and edges.
2. **Development history:** SQL storage was expensive, so the aim was minimum duplication. NoSQL focused on scaling, fast access, and rapid application change (agile practices).
3. **Examples:** Oracle and MySQL are SQL. MongoDB (document), Redis (key-value), HBase (columnar) and Neo4j (graph) are NoSQL.
4. **Primary purpose:**
   - **SQL:** Used generally for everything.
   - **Document:** General purpose. MongoDB is the most famous and is more related to SQL.
   - **Key-value:** Large amounts of data with simple queries.
   - **Wide-column:** Large amounts of data with fast queries and analysis.
   - **Graph:** Retrieving relationships.
5. **Scaling:** SQL can scale vertically. Horizontal scaling gives join problems. NoSQL can scale out (and also up). But making one node more powerful is costly, so data is divided across multiple nodes.
6. **ACID:** The primary goal of SQL is to support ACID. NoSQL generally does not support it, but some, like MongoDB, do.
7. **Joins:** SQL needs them, because related data is stored in separate tables and meaningful data comes only after a join. NoSQL does not, because related data is stored together in one JSON object.
8. **Data to object mapping:**
   - **SQL:** A server or client retrieves a student's name, age, course id and address from a SQL DB. The front-end application has a Student class. So the retrieved fields must be mapped one by one into an instance (student.name = value from server). This is data-to-object mapping (ORM), and it is required.
   - **Java:** This is done with the DAO (Data Access Object) design pattern. Read about the DAO pattern as homework.
   - **MongoDB:** A document maps directly to the data structure (such as a Python class) in the language. So student = whatever came from the server fills the fields automatically. No explicit mapping is needed.
