# Lecture 1: Introduction to DBMS

## LEC-1: Introduction to DBMS

1. **What is Data?**

   1. Data is a collection of raw, unorganized facts and details. It includes text, observations, figures, symbols, and descriptions of things.
      - **No purpose:** Data has no specific purpose and no significance by itself.
      - **Units:** Data is measured in bits and bytes. At the lowest level, everything is bits and bytes (integers, floats, text).
      - **Example:** A table of plain numbers means nothing. Label the columns weight, height and BMI. Now each row is a person.
      - **Unprocessed data:** It gives no sense, so it is of no use. It is raw material. It must be processed (interpreted) first.

   2. Data can be recorded. It has no meaning unless it is processed.

2. **Types of Data**

   | Type | Form | Examples |
   |------|------|----------|
   | **Quantitative** | Numerical | Weight, volume, cost of an item |
   | **Qualitative** | Descriptive, not numerical | Name, gender, hair color of a person |

3. What is **Information**?

   1. Information is **processed, organized, and structured data**.
   2. It gives **context to the data** and enables decision making.
   3. It is processed data that makes **sense** to us.
   4. Information is extracted from data by **analyzing and interpreting** it.
   5. **Example:** You have data on all people in your locality. After analysis you conclude:
      1. There are 100 senior citizens.
      2. The sex ratio is 1.1.
      3. There are 100 newborn babies.

      These conclusions are information.

   - **Flow:** data, then processing, then information, then decision making. The only difference between data and information is one processing step.

     ```mermaid
     flowchart LR
       D["Data<br/>(raw facts, 800 and 2 likes)"] --> P["Processing<br/>(analyze, interpret)"] --> I["Information<br/>(Instagram works best)"] --> X["Decision<br/>(promote on Instagram)"]
     ```
   - **Census:** Family members, age groups and gender in tables are data. "100 senior citizens in the area" is information.
   - **Social media:** A business posts on Facebook, Instagram and LinkedIn. Like counts are data. Processing shows 800 likes on Instagram and 2 on LinkedIn. That is information. The decision is to promote on Instagram.
   - **Online shopping:** Feedback text stored as bytes is data. Sentiment analysis shows positive or negative feedback and which age group likes the product. Customer age, rating and recommendation level are information. Stakeholders decide which age group to target and where to run ads.
   - **Restaurant:** Person A and person B both open a restaurant with 10 dishes. A collects no feedback and orders the same raw material for all dishes. B collects feedback (data). B finds only 5 dishes sell well, so B orders less for the other 5 (cost optimized). B finds momos are famous and markets them. B gets much higher profit and sales. A may fail.
   - **"Data is the new oil":** Businesses grow with data, for example by learning what food or clothes an area likes. Companies buy data from other companies for crores of rupees.

4. **Data vs Information**

   | Point | Data | Information |
   |-------|------|-------------|
   | Meaning | A collection of facts | Puts those facts into context |
   | Structure | Raw and unorganized | Organized |
   | Relation | Individual points, sometimes unrelated | Maps the data to give a big-picture view |
   | Value | Meaningless on its own | Meaningful once analyzed and interpreted |
   | Dependency | Does not depend on information | Depends on data |
   | Form | Graphs, numbers, figures, statistics | Words, language, thoughts, ideas |
   | Decisions | Not sufficient for **decision making** | You can decide based on it |

5. What is **Database**?

   1. A database is an electronic place or system where data is stored. The data can be **easily accessed, managed, and updated**.
      - **Easily accessed:** The data is not encrypted or made so complex that every access needs heavy decryption.
      - **Just a location:** A database is only the place where the bits and bytes are stored. The DBMS does the real work on that data.
   2. To make real use of data, we need a **Database Management System (DBMS)**.
      - **Analogy:** An OS manages resources. A DBMS manages data.

6. What is **DBMS**?

   1. A DBMS is a collection of **interrelated data** and **a set of programs to access that data**.
      - **Database:** The collection of data. It contains information relevant to an enterprise.
      - **Goal:** To **store and retrieve database information** conveniently and efficiently. Storing or retrieving should not take hours.
      - **Two parts:** The DB (where data is stored) and a set of programs (to access, add, update and delete data).
      - **Creation:** A DBMS also gives the method to create the database. That means how and where to store data.
      - **Example:** 3001 students are stored. To add a 3002nd student, you use the addition method the DBMS provides.
      - **Position:** The data lives on disk. The DBMS is the interface between the DB and the applications or users.
      - **Modern systems:** The database and DBMS are one entity (for example MySQL and Oracle).
   2. A DBMS is the database along with all the software and functionality. It performs **addition**, **access**, **updating**, and **deletion** of data.

7. Diagram of a DBMS:

   ```mermaid
   flowchart LR
     DB[("Database<br/>(data on disk)")] <--> DBMS["DBMS<br/>(set of programs:<br/>add, access, update, delete)"]
     DBMS <-- API --> App1["App"]
     DBMS <-- API --> User["User"]
     DBMS <-- API --> App2["App"]
   ```

8. **DBMS vs File Systems**

   - **Why not files?** Earlier, data (names, courses, roll numbers, phone numbers) was kept in separate files or one combined file. Files are not extensible. With billions of records, storing is possible but accessing efficiently is not.
   - **Bank example:** A bank builds a savings-account system on files. A programmer writes programs for debit and credit, new accounts, balance, and monthly statements. After 10 years, the bank wants current accounts. They have no interest, different debit and credit rules, and quarterly or yearly statements. This was not anticipated, so a new programmer writes new files and programs. **Analogy:** same as the OS idea. Without a DBMS, each programmer writes all of this.

     ```mermaid
     flowchart TB
       subgraph FS["File system: every need gets its own programs and files"]
         P1["Savings programs<br/>(debit, credit, statement)"] --> F1[("savings file")]
         P2["Current account programs<br/>(written 10 years later)"] --> F2[("current file")]
         P3["Pin code report program"] --> F1
         P3 --> F2
       end
       subgraph DS["DBMS: one system, queries for new needs"]
         Q["Apps and queries"] --> M["DBMS"] --> D[("one database")]
       end
     ```

   1. **File-processing systems** have major **disadvantages**.

      1. **Data redundancy and inconsistency**
         - **Redundancy:** The same person (address and so on) exists in the savings file and the current-account file. Two programmers stored it differently. Same data in two places wastes disk.
         - **Inconsistency:** A person changes address in the savings file. It is forgotten in the current-account file. Now the person has two addresses.

           ```mermaid
           flowchart LR
             subgraph S["savings file"]
               A1["Person: new address"]
             end
             subgraph C["current-account file"]
               A2["Person: old address"]
             end
             A1 -. "same person stored twice<br/>(redundancy)" .- A2
             A2 -. "update missed, two addresses<br/>(inconsistency)" .- A1
           ```
         - **Fix:** Programs that update both places. This is complex and needs a program for every small thing.

      2. **Difficulty in accessing data**
         - **Example:** A government officer wants all people at a given pin code. The original programmer did not anticipate it. A new program must list all customers, sort and filter by pin code.
         - **Versus DBMS:** A DBMS needs only a query with conditions. A file system needs a new program for every request.

      3. **Data isolation**
         - Different programmers use different formats (.txt, .dat and so on) for the same kind of data in different places. Retrieving it is hard.

      4. **Integrity problems**
         - **Consistency constraints:** For example, a current account balance must never fall below 10000. The debit programs enforce this with checks.
         - **Rule change:** RBI says the minimum is now 20000. The programmer must be called to change the code.

      5. **Atomicity problems**
         - **Atomic:** Transactions (covered later) must be atomic. Either the whole thing happens or none of it. A debit must be matched by a credit. Money must not be debited and lost.
         - **Support:** A DBMS provides this. In a file system it is very hard.

      6. **Concurrent-access anomalies**
         - **Same as OS concurrency:** You withdraw from your phone while someone withdraws with the debit card on the same account at the same time.
         - **Locks:** Locks make one debit finish before the next. In a file system you write the programs and locks yourself.

      7. **Security problems**
         - **Access levels:** Public data is visible to all. Restricted or confidential data is visible to some people. Some data is for higher-level stakeholders only.
         - **File system:** Controlling access rights needs your own programs.

   2. The 7 problems above are also the **advantages of DBMS**. They answer "**Why use a DBMS?**"
      - **Manual effort:** A file system can do all of this, but with a lot of manual effort. As data and internet users grew, specific software (the DBMS) was built with these basics built in and customizable.
      - **Access:** A DBMS gives database creation methods and access and management of data. For example, you can get the first 20 students, or students with above 90 percent marks, using conditions and constraints.

      > **Interview:** If asked "why use a DBMS", give these 7 points. You may be asked to explain one or two.
