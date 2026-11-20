# Lecture 15: NoSQL

## LEC-15: NoSQL

1. NoSQL databases (aka "not only SQL") are non-tabular databases and store data differently than relational tables. NoSQL databases come in a variety of types based on their data model. The main types are document, key-value, wide-column, and graph. They provide flexible schemas and scale easily with large amounts of data and high user loads.
   1. They are schema free.
   2. Data structures used are not tabular, they are more flexible, has the ability to adjust dynamically.
   3. Can handle huge amount of data (big data).
   4. Most of the NoSQL are open sources and has the capability of horizontal scaling.
   5. It just stores data in some format other than relational.
   6. "Not only SQL" does not mean queries cannot run; MongoDB is an example and it has queries. It means something beyond SQL.
   7. Data is stored in non-tabular form; tables are not related to each other. Everything about an entity is stored together (e.g. no separate hobbies table and person table).
   8. SQL needs structured data, i.e. a fixed schema plus integrity constraints (e.g. Student(name, age, address, roll no) with roll no as primary key; admit only if age > 13 must hold before an entry is allowed).
   9. NoSQL can store structured, unstructured and semi-structured data.
       1. Unstructured data: text files, social media chats, CCTV/survey/scientific data dumped for many days.
       2. Semi-structured data: email (the "to"/"from" header is structured, the body is unstructured; every bank/sender writes in its own structure).
       3. Structured data: student table, employee database (fixed schema).
   10. SQL cannot store unstructured data as-is: you must process it into structure first. Structured data is the primary requirement of SQL.
   11. Flexible schema means not all information has to be present (e.g. only some columns of a student are available).
   12. Because it is non-tabular, flexible schema comes automatically: there is no rule that every column must be filled.
   13. This lecture is only a brief introduction to get a feel; it is not meant to teach every NoSQL type. Learn the relational model first, then every other model is easy. For depth, study MongoDB separately.
2. History behind NoSQL
   1. NoSQL databases emerged in the late 2000s as the cost of storage dramatically decreased. Gone were the days of needing to create a complex, difficult-to-manage data model in order to avoid data duplication. Developers (rather than storage) were becoming the primary cost of software development, so NoSQL databases optimised for developer productivity.
      1. Early on, disk/storage was very expensive (memory cards cost thousands, floppy disks were costly), so SQL emerged: structure the data, normalise it, no redundancy, store the minimum data in an optimised way.
      2. To retrieve, tables are linked by foreign keys and joins (inner join, outer join) are applied; this needs processing, so SQL is not that fast.
      3. As storage cost fell, databases emerged focused on fast access: data may be redundant or repeated, storage is not a problem (terabytes available), but data must be served within seconds.
      4. Example of redundancy NoSQL accepts: storing branch/HOD information inside the student's data (the normalisation example), repeated for every student.
   2. Data becoming unstructured more, hence structuring (defining schema in advance) them had becoming costly.
      1. For emails, scientific data and survey data, structuring means pre-processing first and then storing, and the data would also be split across multiple tables (this goes to table A, that to table B, that to table C) because of normalisation.
   3. NoSQL databases allow developers to store huge amounts of unstructured data, giving them a lot of flexibility.
   4. Recognising the need to rapidly adapt to changing requirements in a software system. Developers needed the ability to iterate quickly and make changes throughout their software stack — all the way down to the database. NoSQL databases gave them this flexibility.
   5. Cloud computing also rose in popularity, and developers began using public clouds to host their applications and data. They wanted the ability to distribute data across multiple servers and regions to make their applications resilient, to scale out instead of scale up, and to intelligently geo-place their data. Some NoSQL databases like MongoDB provide these capabilities.
      1. Many servers, serving many people, data within seconds: this business use case grew with cloud computing and faster internet (4G/5G), so servers and databases had to retrieve/read data quickly. Necessity is the mother of invention.
3. NoSQL Databases Advantages
   A. Flexible Schema
      1. RDBMS has pre-defined schema, which become an issue when we do not have all the data with us or we need to change the schema. It's a huge task to change schema on the go.
         1. Data modelling example. SQL: a user table (id, first name, last name, cell, city) and, after normalisation, a separate hobbies table (user id, hobby) because hobby is a multi-valued attribute.
         2. NoSQL (JSON / JavaScript object): one object `{ id: 1, firstName, lastName, cell, city, hobbies: [ ... ] }` with hobbies stored as an array. Same data, different storage: everything comes together and no join across two tables is needed.
         3. Drawback: for even a small piece of information you must pick up the whole object from the DB to the application and then work on it, whereas in SQL you could fetch just the needed column/table.
         4. If an entry has no hobbies, no city and no cell number, SQL stores null null null (some space is wasted). In NoSQL you simply create another object without those fields; nothing is stored for them. That is flexible schema, the biggest advantage.
   B. Horizontal Scaling
      1. Horizontal scaling, also known as scale-out, refers to bringing on additional nodes to share the load. This is difficult with relational databases due to the difficulty in spreading out related data across nodes. With non-relational databases, this is made simpler since collections are self-contained and not coupled relationally. This allows them to be distributed across nodes more simply, as queries do not have to "join" them together across nodes.
         1. Scaling: when you keep storing data, the hardware eventually exhausts (disk full) or data becomes so large that processing takes too long; you must upgrade the system to serve more users, store more data and retrieve faster. Scaling is of two types.
         2. Vertical scaling (scale-up): upgrade the hardware of the single system: RAM, CPU, disk (1 TB disk to 10 TB). SQL generally scales this way, within a single node/unit. Vertical scaling is always costly; many small cheap systems (e.g. 1 GB RAM each) are more cost efficient.
         3. Horizontal scaling (scale-out): add additional nodes (another similar DB system); some data is stored on the old node, new data on the new nodes, so the load is shared/balanced.
         4. Interview question: why can't SQL do horizontal scaling? It is possible but not practical.
            1. SQL is a collection of tables. Say T1, T2, T3 sit on System 1, System 2, System 3 (possibly different servers or even different countries as an extreme example).
            2. Retrieving meaningful data needs joins on T1, T2, T3; the three tables are logically one storage, so all three must first be brought to one node (say System 4) over the network. A join cannot run on half the data.
            3. Moving tables over the network is slow, then the join itself takes time, so retrieval becomes extremely slow.
            4. Such business cases (opening a WhatsApp chat and wanting the last two days of chats instantly) cannot use SQL: data scattered across places, structured data must be fetched, un-structured, spread over the message, then shown. Very costly in time complexity.
            5. NoSQL says: store the data as a document, redundancy is fine, no normalisation load, put related data in one bunch (student, department and branch info together).
         5. In NoSQL all information is in one self-contained object, not coupled relationally, so it can be distributed across nodes; there is no join, no separate JSON object linked by relation.
      2. Scaling horizontally is achieved through Sharding OR Replica-sets.
         1. Replica sets: multiple servers hold copies of the same data (e.g. your Aadhaar data on server 1 and server 3 though stored across 10 servers). If server 1 goes down, the data is read from server 3.
   C. High Availability
      1. NoSQL databases are highly available due to its auto replication feature i.e. whenever any kind of failure happens data replicates itself to the preceding consistent state.
      2. If a server fails, we can access that data from another server as well, as in NoSQL database data is stored at multiple servers.
         1. Because data is replicated on different nodes, if one server is down another is up; this gives reliability.
   D. Easy insert and read operations.
      1. Queries in NoSQL databases can be faster than SQL databases. Why? Data in SQL databases is typically normalised, so queries for a single object or entity require you to join data from multiple tables. As your tables grow in size, the joins can become expensive. However, data in NoSQL databases is typically stored in a way that is optimised for queries. The rule of thumb when you use MongoDB is data that is accessed together should be stored together. Queries typically do not require joins, so the queries are very fast.
         1. With a large amount of data, join is very costly in time complexity; NoSQL read operations are very fast compared to SQL.
         2. All related data is stored at the same location, so it can be accessed in one go without a join.
         3. Rule of thumb in MongoDB: data that is accessed together should be stored together (e.g. if user and hobbies are always accessed together, store them together instead of normalising into tables).
      2. But difficult delete or update operations.
         1. In SQL, to change/add/delete a hobby you go only to the hobbies table and edit it, which is easy.
         2. In NoSQL you must load the whole object into memory, go into hobbies, edit (e.g. delete bike hobby, add a hobby), so add/update/delete is costly in time.
         3. Choice depends on the business use case: if you do not mind slow insert/update/delete but need fast reads (e.g. chats opened often), NoSQL fits.
   E. Caching mechanism.
      1. e.g. chats you talk to most are readily available when you open the app; no heavy load is needed, and they are cached in the system and the database.
   F. NoSQL use case is more for Cloud applications.
      1. Cloud has multiple servers with spread-out data and users want fast data (5G); you do not want normalised data stored separately and joined to fetch it, because joins are slow.
4. When to use NoSQL?
   1. Fast-paced Agile development
      1. Example: when TikTok was banned, Instagram had no Reels yet and had to build it quickly. With SQL development is slower: you design the model, avoid redundancy, create separate tables for multi-valued and composite attributes. With NoSQL there is no worry about duplication or redundancy, so development is fast.
      2. Interview: if given a cloud application, which DB would you use? Say NoSQL.
   2. Storage of structured and semi-structured data
      1. Structured, semi-structured and unstructured data can all be stored in NoSQL.
      2. Where NoSQL is not used: a banking system (credit card etc.) has structured data, usually on a single server not on multiple servers, so SQL is used.
      3. Most normal development today is done with NoSQL databases.
   3. Huge volumes of data
      1. Web applications have lots of data that must be stored, processed and retrieved quickly; retrieval is fast in NoSQL.
   4. Requirements for scale-out architecture
      1. When business requirement is horizontal scaling with multiple servers: in SQL the tables would be spread out and joins become hard.
   5. Modern application paradigms like micro-services and real-time streaming.
      1. Micro-services and real-time streaming operations are fast and need fast access, so NoSQL is used.
5. NoSQL DB Misconceptions
   1. Relationship data is best suited for relational databases.
      1. A common misconception is that NoSQL databases or non-relational databases don't store relationship data well. NoSQL databases can store relationship data — they just store it differently than relational databases do. In fact, when compared with relational databases, many find modelling relationship data in NoSQL databases to be easier than in relational databases, because related data doesn't have to be split between tables. NoSQL data models allow related data to be nested within a single data structure.
         1. Example: user and hobby are related; they are stored together in one JSON object.
         2. A relation between two documents can also be made: put an entry in one JSON object (an id key) whose value is the id of another JSON object. This is like a foreign key. Normally you try to store all related data together, but if needed you can relate two objects this way.
         3. Relationships are easier to model since you do not have to visualise and create tables.
   2. NoSQL databases don't support ACID transactions.
      1. Another common misconception is that NoSQL databases don't support ACID transactions. Some NoSQL databases like MongoDB do, in fact, support ACID transactions.
         1. In general NoSQL databases were not made to support transactions/ACID (that is why banking systems mostly still use SQL), because early NoSQL paradigm development did not focus on ACID. But some, like MongoDB, support them.
6. Types of NoSQL Data Models
   1. Key-Value Stores
      1. The simplest type of NoSQL database is a key-value store. Every data element in the database is stored as a key value pair consisting of an attribute name (or "key") and a value. In a sense, a key-value store is like a relational database with only two columns: the key or attribute name (such as "state") and the value (such as "Alaska").
         1. Only one key and one value; no multiple fields or objects (no name etc.). A single value is found for a key, like a binary lookup.
      2. Use cases include shopping carts, user preferences, and user profiles.
         1. Shopping cart: one hash key per cart item (key = card/item id, value = mobile; second key value = cream; third = monitor).
      3. e.g., Oracle NoSQL, Amazon DynamoDB, MongoDB also supports Key-Value store, Redis.
      4. A key-value database associates a value (which can be anything from a number or simple string to a complex object) with a key, which is used to keep track of the object. In its simplest form, a key-value store is like a dictionary/array/map object as it exists in most programming paradigms, but which is stored in a persistent way and managed by a Database Management System (DBMS).
         1. Key can be a string or integer; value can be anything: JSON, binary object, string, array.
      5. Key-value databases use compact, efficient index structures to be able to quickly and reliably locate a value by its key, making them ideal for systems that need to be able to find and retrieve data in constant time.
      6. There are several use-cases where choosing a key value store approach is an optimal solution:
         a) Real time random data access, e.g., user session attributes in an online application such as gaming or finance.
         b) Caching mechanism for frequently accessed data or configuration based on keys.
         c) Application is designed on simple key-based queries.
   2. Column-Oriented / Columnar / C-Store / Wide-Column
      1. The data is stored such that each row of a column will be next to other rows from that same column.
         1. SQL stores data row-wise (row optimised): all data of a row (e.g. Matt, Delhi, 27) sits together in memory; good when you want the whole row for a key. Reads are fast, but insert needs changes in the middle, so write/update/delete is slow (like appending to a linked list vs editing in the middle).
         2. Column store: all names together, all cities together, all ages together. Adding a new tuple (Rahul) means adding to each column's place.
         3. Reads are fast but insert is slow in column stores too.
      2. While a relational database stores data in rows and reads data row by row, a column store is organised as a set of columns. This means that when you want to run analytics on a small number of columns, you can read those columns directly without consuming memory with the unwanted data. Columns are often of the same type and benefit from more efficient compression, making reads even faster. Columnar databases can quickly aggregate the value of a given column (adding up the total sales for the year, for example). Use cases include analytics.
         1. Example: average age. Row-wise, memory is read by jumping (e.g. every third location) to pick up ages. Column-wise, all ages are together, so go to the first age and read all of it in one go; fast.
         2. Use when analytics and aggregation functions are applied again and again (e.g. industrial machine data shown in analytics, average, peak time).
      3. e.g., Cassandra, RedShift, Snowflake.
   3. Document Based Stores
      1. This DB store data in documents similar to JSON (JavaScript Object Notation) objects. Each document contains pairs of fields and values. The values can typically be a variety of types including things like strings, numbers, booleans, arrays, or objects.
         1. Key-value had one field and one value; a document has multiple fields. A document in the DB is like a JSON object (JSON is widely used on the web to transmit data).
         2. One document can relate to another: e.g. a user document (with id) and a contact/access document that also has the user id (e.g. 1). That is like a foreign key, so relations can be applied.
      2. Use cases include e-commerce platforms, trading platforms, and mobile app development across industries.
      3. Supports ACID properties hence, suitable for Transactions.
      4. e.g., MongoDB, CouchDB.
         1. MongoDB is used in most use cases and is the first choice for anyone learning a NoSQL DB for cloud systems.
   4. Graph Based Stores
      1. A graph database focuses on the relationship between data elements. Each element is stored as a node (such as a person in a social media graph). The connections between elements are called links or relationships. In a graph database, connections are first-class elements of the database, stored directly. In relational databases, links are implied, using data to express the relationships.
         1. Data is visualised as a graph: nodes (vertices) and edges; edges are the relations.
         2. Example: Facebook friends, friends of friends. Profiles A, B, C, D, E are stored, and relations are stored as edges: A related to B, B friend of C, and so on. Mostly used in social media (who follows whom).
         3. The directly related relations are stored, so no join is needed to establish the relation.
         4. In SQL you would keep user profile tables plus a separate table with two foreign keys noting who is friend of whom, then join to get the relation; graph DBs avoid this overhead.
      2. A graph database is optimised to capture and search the connections between data elements, overcoming the overhead associated with JOINing multiple tables in SQL.
      3. Very few real-world business systems can survive solely on graph queries. As a result graph databases are usually run alongside other more traditional databases.
      4. Use cases include fraud detection, social networks, and knowledge graphs.
         1. Fraud detection example: a card used at this ATM then at that ATM; connections are built between them.
         2. e.g., Neo4j, ArangoDB.
7. NoSQL Databases Dis-advantages
   1. Data Redundancy
      1. Since data models in NoSQL databases are typically optimised for queries and not for reducing data duplication, NoSQL databases can be larger than SQL databases. Storage is currently so cheap that most consider this a minor drawback, and some NoSQL databases also support compression to reduce the storage footprint.
         1. Same data for the same use case takes more storage than in SQL, because SQL reduces redundancy by normalisation.
         2. Given the trade-off between storage cost and fast access, storage is cheap today, so this point can be ignored.
   2. Update & Delete operations are costly.
      1. Because related data is stored all together, as in the earlier example.
   3. All type of NoSQL Data model doesn't fulfil all of your application needs
      1. Depending on the NoSQL database type you select, you may not be able to achieve all of your use cases in a single database. For example, graph databases are excellent for analysing relationships in your data but may not provide what you need for everyday retrieval of the data such as range queries. When selecting a NoSQL database, consider what your use cases will be and if a general purpose database like MongoDB would be a better option.
         1. SQL mostly fulfils all application needs (leaving aside scalability / horizontal scaling). In NoSQL one data model fulfils one need and another does not.
         2. MongoDB leveraged its document model and modified it so it can also work as a key-value store.
   4. Doesn't support ACID properties in general.
      1. MongoDB has implemented it, but it is not supported in all.
   5. Doesn't support data entry with consistency constraints.
      1. The database has no consistency constraints of its own; you can add checks in your application before entering data (e.g. if age < 13, do not enter), but the DB itself does not enforce them.
8. SQL vs NoSQL

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

   1. Data storage model: if a column has no entry for a tuple in SQL, null is stored; in NoSQL there are JSON documents, key-value pairs, columnar tables with rows and dynamic columns, and graph nodes and edges.
   2. Development history: SQL storage was expensive so the aim was minimum duplication; NoSQL focused on scaling, fast access, and rapid application change (agile practices).
   3. Examples: Oracle/MySQL are SQL; MongoDB (document), Redis (key-value), HBase (columnar), Neo4j (graph).
   4. Primary purpose: SQL is used generally for everything. Document stores are used for general purpose (MongoDB is the most famous, more related to SQL); key-value for large amounts of data with simple queries; wide-column for large amounts of data with fast queries and analysis; graph for retrieving relationships.
   5. Scaling: SQL can scale vertically; horizontal scaling gives join problems. NoSQL can scale out (and also up), but making one node more powerful is costly, so data is divided across multiple nodes.
   6. ACID: the primary goal of SQL is to support ACID; in NoSQL it is generally not supported but some, like MongoDB, support it.
   7. Joins: needed in SQL because related data is stored in separate tables and meaningful data comes only after a join; not required in NoSQL because related data is stored together in one JSON object.
   8. Data to object mapping:
      1. A server/client retrieves a student's name, age, course id, address from a SQL DB; the front-end application has a Student class, so the retrieved fields must be mapped one by one into an instance (student.name = value from server). This is data-to-object mapping (ORM) and is required.
      2. In Java this is done with the DAO (Data Access Object) design pattern; read about the DAO pattern as homework.
      3. In MongoDB, a document maps directly to the data structure (e.g. a Python class) in the language, so student = whatever came from the server fills the fields automatically; no explicit mapping is needed.
