# Lecture 20: CAP Theorem

1. CAP is a basic and one of the most important concepts in distributed databases.
2. It helps you design an efficient distributed system for your business logic.
   1. **Why distributed:** A database grows large and must serve many requests. You scale up only to a level, then scale out (horizontal scaling with multiple nodes or replicas). This creates a cloud system or distributed storage.
3. **Breaking down CAP**
   1. **Consistency:** In a consistent system, all nodes see the same data simultaneously.
      - A read returns the value of the most recent write.
      - A read makes all nodes return the same data.
      - All users see the same data at the same time, whichever node they connect to.
      - When data is written to a single node, it is then replicated across the other nodes.
      1. **Example:** If x = 10 on node A, x must be 10 on node B too. Data across nodes must be consistent.
   2. **Availability:** The system remains operational all of the time.
      - Every request gets a response, whatever the state of the individual nodes.
      - The system operates even if multiple nodes are down.
      - Unlike a consistent system, there is no guarantee that the response is the most recent write.
      1. If some nodes fail, the system must still stay available. A little latency or delay is fine, but the system must respond.
   3. **Partition tolerance:** A partition is a break in communication between nodes.
      - A partition-tolerant system does not fail, whether messages are dropped or delayed between nodes.
      - To have partition tolerance, the system must replicate records across combinations of nodes and networks.
      1. **Example:** Node A is the primary and node B is its replica. They must communicate to replicate data. A partition is the communication link between them breaking.

         ```mermaid
         flowchart LR
           A[("Node A<br/>primary")] -- "replicate" --x B[("Node B<br/>replica")]
           X["partition: link broken"] -.- A
         ```
      2. **Tolerant:** The partition happens, but the system does not fail and stays up. Some messages may be delayed or data may be inconsistent, but the system keeps running.
      3. **Recovery:** When the node comes back up and the link is re-established, the data must be replicated again.

4. **What does the CAP theorem say?**
   1. A distributed system can provide only **two of three properties** at the same time: consistency, availability and partition tolerance.
      - The theorem formalises the **tradeoff between consistency and availability when there is a partition.**
   2. **When all three can exist:** A single-node database (a small application on one computer) is not a distributed system. There is no partition, since data was never divided across nodes. So all three hold.
   3. **Distributed system:** Only two of the three can be established at a time. When there is a partition (a communication or link break), you must trade off between consistency and availability. Take either consistency or availability.
   4. **Simple proof with two nodes**
      1. A single database grows large. It gets scaled and distributed because requests are many and latency must stay low. It is split into node A and node B, replicas of each other.
      2. Node A is the primary and handles all write operations. Node B is the secondary (replica) and handles all read operations.
      3. A partition happens (communication breaks). Now a write sets x = 10 on node A. The link is down, so it is not replicated to node B.
      4. **Option 1: stay available.** Serve both reads and writes. A read on node B returns the previous value (say x = 20) instead of 10. The latest write is not read, so consistency is lost.
      5. **Option 2: stay consistent.** A read during the partition would return the stale value. So reject it and return a failed or bad request. Availability is lost.
      6. **Conclusion:** During a partition, either consistency is lost or availability is lost. One of the two happens. This is what the CAP theorem says.

         ```mermaid
         sequenceDiagram
           participant W as Writer
           participant A as Node A (primary)
           participant B as Node B (replica, x = 20)
           participant R as Reader
           Note over A,B: Partition: link A to B is down
           W->>A: write x = 10
           A--xB: replicate (fails)
           R->>B: read x
           alt Option 1: stay available (AP)
             B-->>R: x = 20 (stale, consistency lost)
           else Option 2: stay consistent (CP)
             B-->>R: failed / bad request (availability lost)
           end
         ```
   5. A single-node system has no problem, since a partition never occurs there. A partition means a break in the link between two distributed nodes.

5. **CAP theorem and NoSQL databases**
   - NoSQL databases are great for distributed networks. They allow horizontal scaling, and they can quickly scale across multiple nodes.
   - When deciding which NoSQL database to use, keep the CAP theorem in mind.

   ```mermaid
   flowchart TB
     C(("Consistency"))
     A(("Availability"))
     P(("Partition<br/>tolerance"))
     C --- CA["CA: MySQL, PostgreSQL<br/>(single node)"] --- A
     C --- CP["CP: MongoDB"] --- P
     A --- AP["AP: Cassandra, DynamoDB"] --- P
   ```

   The three properties cannot all exist together. Only the intersection of two properties is possible: CA, CP or AP.

   | Type | Gives | Gives up | Examples |
   |------|-------|----------|----------|
   | CA | Consistency, availability | Partition tolerance | MySQL, PostgreSQL (single node) |
   | CP | Consistency, partition tolerance | Availability | MongoDB |
   | AP | Availability, partition tolerance | Consistency | Cassandra, DynamoDB |

   1. **CA databases:** They enable consistency and availability across all nodes. They cannot deliver fault tolerance.
      - In any distributed system, partitions are bound to happen. So this type of database is not a very practical choice.
      - You can still find a CA database if you need one. Some relational databases, such as MySQL or PostgreSQL, allow consistency and availability. You can deploy them to nodes using replication.
      1. CA means consistency and availability together. We saw they cannot both hold when a partition happens. So CA databases are databases that do not get partitioned. They are not distributed. They run on a single node.
      2. There is no "all the nodes" in such a case.
      3. If you build a distributed system with MySQL and link the nodes, a partition is bound to happen, because the link will break for some time. So you cannot claim both consistency and availability.
      4. **Only ways out:** Make a system where a partition never happens (hypothetical, near impossible, maybe possible at small scale, not at large scale). Or keep the system on one node.
      5. CA is not a very practical choice in distributed systems. Use it only on a single node.

   2. **CP databases:** They enable consistency and partition tolerance, but not availability.
      - When a partition occurs, the system has to turn off inconsistent nodes until the partition is fixed.
      - **MongoDB** is an example of a CP database. It is a NoSQL database management system (DBMS) that uses documents for data storage. It is schema-less, which means it does not require a defined database schema. It is commonly used in big data and in applications running in different locations.
      - **Structure:** A CP system has **only one primary node that receives all the write requests in a given replica set.** Secondary nodes replicate the data from the primary node. If the primary node fails, a secondary node can stand in.
      - **Banking:** Availability is not as important as consistency, so we can opt for MongoDB.
      1. Partition tolerant means the system keeps working after a partition. So take either consistency or availability. CP picks consistency.
      2. When a partition occurs, node B (the inconsistent node) is turned off. Availability is lost. When the partition is fixed and communication is re-established between both, work continues.
      3. **Banking example:** Availability is not that important. Banking systems go down at night for maintenance or at other times, and that is fine. Consistency matters. One account must not show 1 lakh on one node and 2 lakh on another.
      4. So for a banking system, use a CP type database. On a partition, the secondary (inconsistent) nodes are turned off, and a read from them returns a bad request. The system loses availability, but availability is not the target.

   3. **AP databases:** They enable availability and partition tolerance, but not consistency.
      - In the event of a partition, all nodes are available, but they are not all updated.
      - **Example:** If a user accesses data from a bad node, they do not receive the most up-to-date version of the data.
      - When the partition is eventually resolved, most AP databases sync the nodes to ensure consistency across them.
      - **Apache Cassandra** is an example of an AP database. It is a NoSQL database with no primary node, so all nodes remain available.
      - Cassandra allows for **eventual consistency**, because users can re-sync their data right after a partition is resolved.
      - **Facebook-like apps:** We value availability more than consistency. We opt for AP databases like Cassandra or Amazon DynamoDB.
      1. On a partition, do nothing. Let both nodes keep working, so both reads and writes execute.
      2. The system stays inconsistent for a while. This is fine if the business logic allows it. Example: x = 10 is written on one node, and the other node (still available) returns the old value x = 20. This does not matter in AP databases.
      3. When the link is re-established, replication syncs the nodes and both become consistent again.
      4. This is called **eventual consistency.** AP databases are eventually consistent. It is important to know this.

         ```mermaid
         flowchart LR
           P["Partition"] --> I["Both nodes serve reads and writes<br/>A: x = 10, B: x = 20"]
           I --> L["Link re-established"]
           L --> S["Replication syncs: A = B, x = 10<br/>(eventually consistent)"]
         ```
      5. Cassandra and DynamoDB are examples.
      6. **Use case:** Social media, where availability is valued more than consistency.

6. **Choosing a database type**
   1. **Banking system:** CP (for example MongoDB).
   2. **Social media website:** AP (for example Cassandra, DynamoDB).
   3. **CA databases:** Use them only when you assume a partition will never happen, that is, on a single node. They are not practical in a distributed system, since a partition is certain there.

   ```mermaid
   flowchart TB
     Q{"What matters more during a partition?"}
     Q -- "consistency (banking)" --> CP["CP: MongoDB<br/>ACID"]
     Q -- "availability (social media)" --> AP["AP: Cassandra, DynamoDB<br/>BASE"]
     Q -- "no partition: single node" --> CA["CA: MySQL, PostgreSQL"]
   ```

7. **ACID vs BASE**
   1. A banking system follows the ACID properties. Social networking systems follow the BASE properties.
   2. **BASE** stands for Basically Available, Soft state, Eventual consistency.

   > **Interview:** ACID vs BASE is a simple interview question.
