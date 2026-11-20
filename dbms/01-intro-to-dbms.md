# Lecture 1: Introduction to DBMS

## LEC-1: Introduction to DBMS

1. **What is Data?**
   1. Data is a collection of raw, unorganized facts and details like text, observations, figures, symbols, and descriptions of things etc.
      In other words, **data does not carry any specific purpose and has no significance by itself.**
      Moreover, data is measured in terms of bits and bytes – which are basic units of information in the context of computer storage and processing.
      - Stored in memory as bits and bytes (integers, floats, text); at the lowest level everything is bits and bytes.
      - Example: a table of plain numbers (integers and floats) means nothing. Label the columns as weight, height and BMI and the same numbers suddenly mean something: each row is a person.
      - Unprocessed data gives no sense, so it cannot become information and is of no use.
      - Data is only a raw material: it has to be processed (interpreted) before it is useful.
   2. Data can be recorded and doesn't have any meaning unless processed.
2. **Types of Data**
   1. **Quantitative**
      1. Numerical form
      2. Weight, volume, cost of an item.
   2. **Qualitative**
      1. Descriptive, but not numerical.
      2. Name, gender, hair color of a person.
3. What is **Information**?
   1. Info. Is **processed, organized, and structured data.**
   2. It provides **context of the data and enables decision making.**
   3. Processed data that make **sense** to us.
   4. Information is extracted from the data, by **analyzing and interpreting** pieces of data.
   5. E.g., you have data of all the people living in your locality, its Data, when you analyze and interpret the data and come to some conclusion that:
      1. There are 100 senior citizens.
      2. The sex ratio is 1.1.
      3. Newborn babies are 100.

      These are information.
   - Flow: data -> processing (analyze/interpret) -> information -> decision making. The only difference between data and information is one processing step.
   - Census example: family members, age groups, gender are stored in tables (bits and bytes) = data. Conclusion "100 senior citizens in the area" = information; decisions follow from it.
   - Social media example: a business posts the same content on Facebook, Instagram and LinkedIn. Likes counts (integers) are data. Processing them shows, e.g., 800 likes on Instagram and 2 on LinkedIn, so focus on Instagram. That conclusion is information; the decision is where to promote.
   - Online shopping example: customer feedback is raw text stored as bytes = data. Sentiment analysis tells whether feedback on a product is positive or negative and which age group likes it; customer age, customer rating and recommendation level are information. Stakeholders decide which age group to target and where to run ads.
   - Restaurant example: person A and person B both open a restaurant with 10 dishes. A collects no feedback and keeps ordering the same raw material for all dishes. B collects feedback (data), finds only 5 dishes sell well, and orders less raw material for the other 5 (cost optimized). B also finds momos are very famous and markets them. B ends up with much higher profit and sales; A may fail.
   - "Data is the new oil": data is so important and powerful that businesses grow with it (what food or clothes an area likes). Companies even buy data from other companies for crores of rupees. Raw data is useless unless processed; data acts as a raw material.
4. **Data vs Information**
   1. Data is a collection of facts, while information puts those facts into context.
   2. While data is raw and unorganized, information is organized.
   3. Data points are individual and sometimes unrelated. Information maps out that data to provide a big-picture view of how it all fits together.
   4. Data, on its own, is meaningless. When it's analyzed and interpreted, it becomes meaningful information.
   5. Data does not depend on information; however, information depends on data.
   6. Data typically comes in the form of graphs, numbers, figures, or statistics. Information is typically presented through words, language, thoughts, and ideas.
   7. Data isn't sufficient for **decision-making**, but you can make decisions based on information.
5. What is **Database**?
   1. Database is an electronic place/system where data is stored in a way that it can be **easily accessed, managed, and updated.**
      - Easily accessed: not encrypted or made so complex that every access needs heavy decryption.
      - A database is just the location in the computer where the bits and bytes are stored; the real work on that data is done by the DBMS.
   2. To make real use Data, we need **Database management systems. (DBMS)**
      - Like an OS manages resources, a DBMS manages data.
6. What is **DBMS**?
   1. A database-management system (DBMS) is a collection of **interrelated data** and **a set of programs to access those data**. The collection of data, usually referred to as the **database**, contains information relevant to an enterprise. The primary goal of a DBMS is to provide a way to **store and retrieve database information** that is both convenient and efficient.
      - Two parts: the DB (where data is stored) and a set of programs (to access, add, update and delete data).
      - It also provides the method to create the database, i.e. how and where to store the data.
      - Example: 3001 students stored; adding a 3002nd student uses the addition method the DBMS provides.
      - A DBMS is a software that provides two things: (1) how to create the database / where to store data, (2) a set of programs to access it.
      - Efficient and convenient: storing or retrieving should not take hours.
      - The data lives on disk. The DBMS sits as an interface between the DB and the application programs/users that want the data.
      - In modern systems the database and the DBMS are one entity (e.g. MySQL, Oracle): they both create the database and give the methods to access it.
   2. A DBMS is the database itself, along with all the software and functionality. It is used to perform different operations, like **addition**, **access**, **updating**, and **deletion** of the data.
7. 

   ```
                          +-------+
                    API   |  App  |
                 +------->+-------+
   +----------+  |
   | Database |->| DBMS |--API-->+-------+
   +----------+  |              | User  |
                 |              +-------+
                 +--API-->+-------+
                          |  App  |
                          +-------+
   ```

   Diagram: Database feeds the DBMS; the DBMS talks through an API to Apps and Users.
8. **DBMS vs File Systems**
   - Why not just use a file system (txt files, etc.)? Earlier, data (names, courses, roll numbers, phone numbers) was kept in separate files or one combined file. Files are not extensible, and with data in billions, storing is possible but accessing efficiently is not.
   - Example: a bank with a savings-account system built on files. A programmer is hired to write programs for debit/credit, add a new account, find balance, generate monthly statements. Each kind of data goes into its own files. After 10 years the bank wants current accounts (no interest, different debit/credit rules, quarterly/yearly statements). This was not anticipated, so a new programmer writes new files and programs. Same as the OS idea: without a DBMS the individual programmer must write all of this.
   1. **File-processing systems** has major **disadvantages**.
      1. Data Redundancy and inconsistency
         - Redundancy: the same person (address etc.) now exists in the savings file and in the new current-account file, stored differently by two programmers. Same data at two places wastes disk.
         - Inconsistency: the person changes address in the savings file but it is forgotten in the current-account file, so the same person has two addresses. It can be fixed by writing programs that update both places, but that is complex and needs a program for every small thing.
      2. Difficulty in accessing data
         - Example: a government officer asks for all people living at a given pin code. The original programmer did not anticipate it, so a new program must be written (list all customers, sort, filter by pin code). Not quick or efficient.
         - In a DBMS a query is written with conditions and the answer comes back; with a file system every request needs a new program.
      3. Data isolation
         - Different programmers use different formats (.txt, .dat etc.) for the same kind of data in different places, so retrieving it is hard.
      4. Integrity problems
         - Consistency constraints, e.g. a current account balance must never fall below 10000, are enforced by checks in the debit programs.
         - If the rule changes (RBI says minimum 20000), the programmer must be called again to change the code.
      5. Atomicity problems
         - Transactions (covered later) must be atomic: either the whole thing happens or none of it. A debit must be matched by a credit; money must not be debited and lost without the credit.
         - A DBMS provides this functionality; in a file system it is very hard to maintain.
      6. Concurrent-access anomalies
         - Same as concurrency in OS. E.g. you withdraw from the phone while someone else withdraws with the debit card on the same account at the same time.
         - Locks are needed so one debit request completes before the next; in a file system this is manual, you write the programs and locks yourself.
      7. Security problems
         - Not everyone should access all data: public data visible to all, restricted/confidential data only to some people, some only to higher-level stakeholders.
         - Controlling access rights in a file system needs your own programs.
   2. Above 7 are also the **Advantages of DBMS** (answer to "**Why to use DBMS?**")
      - A file system can implement all of this, but with a lot of manual effort. As data and internet users grew (huge volume), a specific software (the DBMS) was built with these basics in-built and customizable.
      - A DBMS provides database creation methods and access/management of data, e.g. first 20 students, or students with above 90 percent marks, via conditions and constraints.
      - Interview: asked "why use a DBMS", say these 7 points; they may ask you to explain one or two.
