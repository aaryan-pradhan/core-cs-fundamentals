# Lecture 20: CAP Theorem

1. Basic and one of the most important concept in Distributed Databases.
2. Useful to know this to design efficient distributed system for your given business logic.
   1. Needed when a database grows large and must serve many requests: scale up only to a level, then scale out (horizontal scaling, multiple nodes or replicas). This creates a cloud system or distributed storage.
3. Let's first breakdown CAP
   1. **Consistency**: In a consistent system, all nodes see the same data simultaneously. If we perform a read operation on a consistent system, it should return the value of the most recent write operation. The read should cause all nodes to return the same data. All users see the same data at the same time, regardless of the node they connect to. When data is written to a single node, it is then replicated across the other nodes in the system.
      1. Example: if x = 10 on node A, x must be 10 on node B too. Data across nodes must be consistent.
   2. **Availability**: When availability is present in a distributed system, it means that the system remains operational all of the time. Every request will get a response regardless of the individual state of the nodes. This means that the system will operate even if there are multiple nodes down. Unlike a consistent system, there's no guarantee that the response will be the most recent write operation.
      1. If some nodes fail, the system must still stay available. A little latency or delay is fine, but the system must respond.
   3. **Partition Tolerance**: When a distributed system encounters a partition, it means that there's a break in communication between nodes. If a system is partition-tolerant, the system does not fail, regardless of whether messages are dropped or delayed between nodes within the system. To have partition tolerance, the system must replicate records across combinations of nodes and networks.
      1. Say node A is the primary and node B is its replica. They must communicate to replicate data. A partition is the communication link between them breaking.
      2. Partition tolerant: the partition happens, the system does not fail and stays up. Some messages may be delayed or data may be inconsistent, but the system keeps running.
      3. When the node comes back up and the link is re-established, the data must be replicated again.
4. What does the CAP Theorem says,
   1. The CAP theorem states that a distributed system can only provide **two of three properties** simultaneously: consistency, availability, and partition tolerance. The theorem formalises the **tradeoff between consistency and availability when there's a partition.**
   2. When all three can exist: a single-node database (a small application on one computer) is not a distributed system. There is no partition, since data was never divided across nodes. So all three hold.
   3. In a distributed system, only two of the three can be established at a time. In other words: when there is a partition (communication or link break), you must trade off between consistency and availability. Either take consistency or take availability.
   4. Simple proof with two nodes:
      1. A single database grows large, gets scaled and distributed because requests are many and latency must stay low. Split into node A and node B, replicas of each other.
      2. Node A is the primary and handles all write operations. Node B is the secondary (replica) and handles all read operations.
      3. A partition happens (communication breaks). Now a write sets x = 10 on node A. The link is down, so it is not replicated to node B.
      4. Option 1: serve both reads and writes (keep the system available). A read on node B returns the previous value (say x = 20) instead of 10. The latest write is not read, so consistency is lost.
      5. Option 2: keep the system consistent. A read during the partition would return the stale value, so reject it and return a failed or bad request. Availability is lost.
      6. So during a partition either consistency is lost or availability is lost. One of the two happens. This is what the CAP theorem says.
   5. A single-node system has no problem, since partition never occurs there. Partition means a break in the link between two distributed nodes.
5. CAP Theorem NoSQL Databases: NoSQL databases are great for distributed networks. They allow for horizontal scaling, and they can quickly scale across multiple nodes. When deciding which NoSQL database to use, it's important to keep the CAP theorem in mind.

   ```
              Consistency
              /         \
           CA     .      CP
        Availability  AP  Partition Tolerance
   ```

   The three properties cannot all exist together. Only the intersection of two properties is possible: CA, CP or AP.
   1. **CA Databases:** CA databases enable consistency and availability across all nodes. Unfortunately, CA databases can't deliver fault tolerance. In any distributed system, partitions are bound to happen, which means this type of database isn't a very practical choice. That being said, you still can find a CA database if you need one. Some relational databases, such as MySQL or PostgreSQL, allow for consistency and availability. You can deploy them to nodes using replication.
      1. CA means consistency and availability together. We just saw they cannot both hold when a partition happens. So CA databases are databases that do not get partitioned, i.e. not distributed, on a single node.
      2. There is no "all the nodes" in such a case.
      3. If you build a distributed system with MySQL and link the nodes, a partition is bound to happen, because the link will break for some time. So you cannot claim both consistency and availability.
      4. The only ways out: make a system where partition never happens (hypothetical, near impossible, maybe possible at small scale, not at large scale) or keep the system on one node.
      5. Not a very practical choice in distributed systems. Use only on a single node.
   2. **CP Databases:** CP databases enable consistency and partition tolerance, but not availability. When a partition occurs, the system has to turn off inconsistent nodes until the partition can be fixed. MongoDB is an example of a CP database. It's a NoSQL database management system (DBMS) that uses documents for data storage. It's considered schema-less, which means that it doesn't require a defined database schema. It's commonly used in big data and applications running in different locations. The CP system is structured so that there's **only one primary node that receives all of the write requests in a given replica set.** Secondary nodes replicate the data in the primary nodes, so if the primary node fails, a secondary node can stand-in. In banking system Availability is not as important as consistency, so we can opt it (MongoDB).
      1. Partition tolerant means the system keeps working after a partition. So take either consistency or availability. CP picks consistency.
      2. When a partition occurs, node B (the inconsistent node) is turned off. Availability is lost. When the partition is fixed and communication is re-established between both, work continues.
      3. Banking example: availability is not that important. Banking systems go down at night for maintenance or at times, and that is fine. Consistency matters: one account must not show 1 lakh on one node and 2 lakh on another.
      4. So for a banking system use a CP type database. On a partition the secondary (inconsistent) nodes are turned off, and a read from them returns a bad request. The system loses availability, but availability is not the target.
   3. **AP Databases:** AP databases enable availability and partition tolerance, but not consistency. In the event of a partition, all nodes are available, but they're not all updated. For example, if a user tries to access data from a bad node, they won't receive the most up-to-date version of the data. When the partition is eventually resolved, most AP databases will sync the nodes to ensure consistency across them. Apache Cassandra is an example of an AP database. It's a NoSQL database with no primary node, meaning that all of the nodes remain available. Cassandra allows for eventual consistency because users can re-sync their data right after a partition is resolved. For apps like Facebook, we value availability more than consistency, we'd opt for AP Databases like Cassandra or Amazon DynamoDB.
      1. On a partition, do nothing. Let both nodes keep working, so both reads and writes execute.
      2. The system stays inconsistent for a while. This is fine if the business logic allows it. Example: x = 10 written on one node, the other node (still available) returns the old value x = 20. This does not matter in AP databases.
      3. When the link is re-established, replication syncs the nodes and both become consistent again.
      4. This is called eventual consistency, so AP databases are eventually consistent. It is important to know that AP databases are eventually consistent.
      5. Cassandra and DynamoDB are examples.
      6. Use case: social media, where availability is valued more than consistency.
6. Choosing a database type
   1. Banking system: CP (e.g. MongoDB).
   2. Social media website: AP (e.g. Cassandra, DynamoDB).
   3. CA databases are used only when you assume partition will never happen, i.e. a single node. They are not practical in a distributed system, since partition is certain there.
7. ACID vs BASE
   1. A banking system follows the ACID properties. Social networking systems follow the BASE properties. ACID vs BASE is a simple interview question.
   2. BASE stands for: Basically Available, Soft state, Eventual consistency.
