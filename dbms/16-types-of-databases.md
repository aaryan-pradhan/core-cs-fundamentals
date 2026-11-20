# Lecture 16: Types of Databases

## 1. Relational databases

They are based on the relational model.

- **Tables:** Data is defined in tables, and tables are related to each other (tables are also called relations).
- **Relations:** They are established through foreign keys. Referential integrity and many constraints apply.
- **Popular:** Relational databases are quite **popular**, even though the system was designed in the 1970s. They are also known as relational database management systems (RDBMS). They commonly use **Structured Query Language (SQL)** to **create**, **read**, **update**, and **delete** data.
- **Discrete tables:** Information is stored in tables that can be **JOIN**ed by fields known as **foreign** keys. For example, a User table joins to a Purchases table of all purchases the users made. Meaningful data is pulled out by establishing relations with joins.
- **Examples:** MySQL, Microsoft SQL Server, Oracle.

**Advantages:**

- **Ubiquitous:** They have had a steady user base since the 1970s. This is the most mature database. It suits almost all use cases, except where horizontal scalability is needed. Community support is very good: courses and Stack Overflow are easy to find.
- **Structured data:** They are highly optimised for structured data. Data fed in must be structured.
- **Normalisation:** They give a stronger guarantee of normalisation. Normalisation and redundancy removal are required before inserting data. The design flow is: visualise data, draw an ER diagram, convert it to tables, and apply normalisation step by step. So data is almost normalised, with no redundancy.
- **SQL:** They use a well-known query language. Data is retrieved with SQL.

**Disadvantages:**

- **Scalability issues (horizontal scaling):** This is the biggest disadvantage, the one problem of an otherwise most mature DB.
- **Complexity:** As data becomes huge, the system becomes more complex. It is hard to track which data is related to which, so it gets messy. A very large relational model for one application is difficult for the DBA to manage.

> **Interview:** Which problem of the relational model makes it a poor fit for cloud systems, and why is it not called the best DBMS? It cannot fulfil today's cloud requirements well because of the horizontal scalability issue.

## 2. Object-oriented databases

The object-oriented data model is based on the **object-oriented-programming paradigm**, which is now in wide use. **Inheritance**, **object-identity**, and **encapsulation** (information hiding), with methods as an interface to objects, are key OOP concepts that apply in data modelling. The model also supports a rich type system, including structured and collection types.

- **Versus the E-R model:** Inheritance and, to some extent, complex types are also in the E-R model. Encapsulation and object-identity distinguish the object-oriented model from it.
- **Prior knowledge:** It needs OOPs knowledge (classes, objects, encapsulation, inheritance, polymorphism). That is why it is typical to understand and not very popular. You must design the whole system in an object-oriented way.
- **Class:** A class is a blueprint. An object is an instance of a class.
- **Class attributes:** The characteristics, meaning the data types that together define the class.
- **Class methods:** They define the behaviour of the object, meaning what it can do.
- **Everything is an object:** Data is not stored directly as, for example, strings. It is encapsulated in a class, bundled into an object, and the object is stored directly on disk or in the database. Whatever is retrieved comes back as an object.
- **Contents:** Objects can hold tables and executable code. The executable code lives in the methods.
- **Communication:** Objects communicate with each other via methods.
- **Handle:** The object ID, like the primary key in relational terms.
- **Example:** A Student class has name, roll number and so on as attributes. It has methods like "can study" or "is passed" (for example, passed the 2021 exam). Create an object per student, set name, roll number and address, and store it as an object. Retrieve it as an object and call methods, such as `student.isPassed()`.
- **No tables:** It is not a table blueprint with data stored row by row. A class instance is created and stored as a whole bunch.
- **All OOPs concepts apply:**
  - **Inheritance:** A Person class (name, gender, age). Student and Professor inherit from Person, each with its own extra attributes.
  - **Object identity:** Each object represents itself. A Student object represents that it is a student.
  - **Encapsulation:** Hide some attributes of an object and expose others.
  - **Methods:** They provide the interface to the object.
- **Structured:** The object model stores a collection of structured data. A structure is needed (a student must have a name and so on) before the data is stored.

**When to move to it:** A relational database can be very complex, with multiple relations, and maintaining them can be tedious. The relational model's problem arises exactly when establishing and maintaining relations becomes hard. Then one can shift to an object-oriented database.

- **One package:** Data is treated as an object. All bits of information come in one instantly available object, instead of multiple tables. No joins are needed.

**Example:**

1. A Person class (name, phone number, email, address) is the blueprint. Person objects are stored.
2. Student (roll number, marks, relevant information) is a Person, and Professor is also a Person. Inheritance applies, and the Person attributes apply to both.
3. Suppose `isPassed` is exposed to the Professor but average marks is not. The professor calls `isPassed` on a particular Student object.
4. `isPassed` may hold an algorithm that checks the student's past records in the DB (passed in 2021 or 2010, how many subjects failed). It can also give the dates a student took leave.
5. Personal information the university knows but the professor should not see can be hidden.
6. A Person lives somewhere. The address is stored as another object, and the Person calls a method such as `getAddress`. Objects interact with other objects through methods.

### a. Advantages

- **Easy and quick:** Data arrives in object form, so all information comes at once and no joins are needed. It is somewhat like NoSQL, but not completely.
- **Complex data:** It handles complex relations and more data types than standard relational databases. Relations are not written the relational way. There is no rule that everything must be a table, no redundancy rule, no strict normalisation.
- **Real-world modelling:** It is relatively friendly for modelling advanced real-world problems. OOP came because real-world problems are easier to model that way.
- **OOP fit:** It works with OOPs and object-oriented languages. Software written in C++ or Java interacts easily with an object-oriented DB, since both use the same paradigm.

### b. Disadvantages

- **Performance:** High complexity slows read, write, update and delete. Sometimes too much complexity is put into method calls.
- **Community:** It has little community support, as it is not widely adopted like relational databases.
- **Views:** It does not support views like relational databases. In a relational DB, a view can show a professor only a trimmed-down Student. Here, views can be implemented using encapsulation.

**Examples:** ObjectDB, GemStone etc.

## 3. NoSQL databases

NoSQL databases (also called "not only SQL") are non-tabular databases. They store data differently than relational tables. The main types are document, key-value, wide-column, and graph. They provide flexible schemas and scale easily with large data and high user loads.

- **Schema free:** There are no tables at all.
- **Flexible structures:** Data structures are not tabular and adjust dynamically.
- **Big data:** They handle huge amounts of data.
- **Open source:** Most are open source and scale horizontally.
- **Format:** They just store data in some format other than relational. Redundancy can exist, meaning repeated data.
- **More:** Refer to the **LEC-15** notes.
- **Maturity:** NoSQL is modern. Relational databases are old and very mature. In cloud systems NoSQL is almost mature now. MongoDB is the prime, very famous example.

## 4. Hierarchical databases

The hierarchical model suits use cases built on a **concrete hierarchy**, such as several employees reporting to a single department.

- **Real-world examples:** A family tree (grandparents, parents, children, starting from a root). A file system (directories such as Movies and Music with children inside).
- **Biggest use case:** Information is needed from top to bottom, traversing down the tree.
- **Organisation example:** CEO, then VPs, presidents, CTO, then senior directors, directors, managers. Or a company, then Marketing, HR and other departments, divided further. Store who reports to whom and which department is under which.
- **Software engineering example:** Many employees work under the department, under an employee more employees, under a lead more leads, and so on.
- **Choice:** For data of this kind, do not use NoSQL or the relational model. The relational model is built for M:N relations, a different use case, and only adds complexity. Use a hierarchical DB directly, because it is simple and fits.

The schema is defined by its **tree-like** organisation. A **root** "parent" directory of records links to subdirectory branches, and each branch, or child record, may link to further branches.

- **One parent:** A parent record can have several child records. Each child record can have only **one parent**.
- **Fields:** Data within records is stored as fields, and each field holds one value.
- **Retrieval:** It requires traversing the tree, starting at the root node.
- **Electronics shop example:** Table Electronics holds Phones, TVs, Washing Machines. Phones hold, for example, Samsung phones. To list all types of TV, traverse from the root down to TVs, then LCD and LED, and print their records. Retrieving top-down like this is the use case.

**Physical model:** The **disk storage system** is also inherently hierarchical, so these models can be used as physical models.

- **Schemas:** The conceptual (logical) schema says how data is related and what it is. The physical schema says how it is stored on disk. There is also the view schema.
- **Reuse:** The logical schema is tree-like and the file system is tree-like, so the logical schema can be copied as is to disk.

**Advantage:** Ease of use. The one-to-many organisation makes traversal simple and fast. It is ideal for website drop-down menus or folders in Microsoft Windows.

- **Easy changes:** The tables are separate from physical storage structures, so information can be added or deleted without affecting the whole database.
- **Language support:** Most major programming languages can read tree structures. Trees are important in DSA.
- **Example:** Stop selling TVs. Drop the TV node, and all its children are deleted automatically.

**Disadvantage:** Inflexibility.

- **Single parent:** The one-to-many structure cannot describe relationships where a child has multiple parents. Siblings (same level) with a relation among themselves cannot be related.
- **Slow search:** Searching is top-to-bottom and sequential, always starting from the root. With a very big tree, maintenance and traversal become very costly in time complexity.
- **Redundancy:** It requires repetitive storage of data in multiple entities.

**Example:** IBM IMS. IMS stands for Information Management System. A node cannot have multiple parents. Where a node must have multiple parents, use a network database.

## 5. Network databases

A network database is an **extension** of the hierarchical database. It is still tree-like, but multiple parents are allowed.

- **Multiple parents:** A child record can link to multiple parent records, so complex relations can be handled. The hierarchical DB insists on one parent per child.
- **Graph:** Multiple parents make it a **graph** structure.
- **Complex relations:** It can handle them.
- **Maintenance:** It is tedious.
- **M:N links:** They may cause slow retrieval. The tree-like hierarchical DB was already slow with lots of data. Here there is lots of data plus M:N links, so graph traversal becomes very costly.
- **Community:** There is little web community support. Hierarchical, network and object-oriented databases all have very specific use cases and little support. They are not used much and will not be in future. The most famous are relational and NoSQL databases.
- **Examples:** Integrated Data Store (IDS), IDMS (Integrated Database Management System), Raima Database Manager, TurboIMAGE etc. These are old and rarely used today. Only some legacy systems use them.
- **University example:** University is the root, with Department and Admin under it. Department has Student, Faculty and Sports. There are also Clubs. Students and Faculty can be in clubs, and Sports are also in clubs. So a Student's parents are Department and Club, and a Faculty's parents are Department and Club. This needs multiple parents, so use a network DB.

![Network database diagram](img/lec-16-network-db.png)

## 6. Which databases to focus on

- **Market:** Relational and NoSQL databases are the ones used. Cloud-heavy companies use NoSQL (such as MongoDB) a lot.
- **Know every type:** When the use case comes, its advantages and disadvantages, which has better market support, and what you would pick for your own software.
- **Rule:** If the structure is only tree-like and siblings have no relation, use a hierarchical DB. If there are multiple parents (graph-like structure), use a network DB.

> **Interview:** You may be asked what relational and NoSQL databases are, and what other databases exist. Have at least a rough idea of the rest.
