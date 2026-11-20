# Lecture 21: The Master-Slave Database Concept

```
                Replicate        +-----------------+      Read
          +--------------------> | Slave Database  | <-----------------+
          |                      | (MongoDB)       |                   |
          |                      +-----------------+                   v
+-----------------+                                              +-------------+
| Master Database |                                              | App Service |
| (PostgreSQL)    |                                              +-------------+
+-----------------+              +-----------------+                   ^   ^
   ^      |        Replicate     | Slave Database  |      Read         |   |
   |      +--------------------> | (MongoDB)       | <-----------------+   |
   |                             +-----------------+                       |
   |                                                                       |
   +------------------------------- Write ---------------------------------+
```

1. **Master-slave** is a general way to optimise IO in a system. It is used when the number of requests goes so high that a single DB server cannot handle it efficiently.
   - **Normal setup:** Servers S1, S2 and S3 sit behind a load balancer. Millions of requests reach the load balancer. It sends each one to the least busy server.
   - **One DB:** Every request from every server goes to that one DB. It serves all servers as the database server.
   - **Single point of failure:** If that DB crashes or gets hacked, the whole system blocks. Availability becomes zero. Requests are not served (they return bad requests or failures).
   - **Solution:** Add another DB as a copy (replica). Requests are divided between the DBs, so some go to one and some to the other.
   - **Name:** This architecture is called master-slave architecture. One DB is the master. The other is the slave.
   - **Usage:** Master-slave is very widely used in computer science (also seen as master-slave flip-flop in circuits).
   - **Naming:** The name is falling out of use for ethical reasons (the master dictates, the slave obeys). Some places say primary and replica. Similarly, Git's `master` branch is renamed `main`. The concept is the same.
   - **Different data models:** The master DB may be SQL while the slaves are MongoDB. So the data model of the primary and the replicas can differ. Then interfaces must be written to replicate between them so the application works properly.

   > **Interview:** Interviewers ask directly "what is the master-slave model".

2. **Link to Lecture 19:** This is Pattern 3 in LEC-19 (Database Scaling Patterns), Command Query Responsibility Segregation.
   - Lecture 19 covered it practically (cab booking app). This lecture covers it formally.
   - Revise Lecture 19 for a real-life example of DB scaling.

3. **Writes and reads**
   - **Master:** The true, latest data is kept in the master DB. So write operations are directed there. The master is the original DB. It is also called the latest DB, owner DB or primary DB. Whatever it holds is the latest information.
   - **Writes:** All writes go to the master only, so it always has the latest data. Slaves never take write operations.
   - **Slaves:** They replicate from the master to get new updates. They handle only read operations.
   - **Purpose:** This architecture safeguards site reliability and availability, and reduces latency.
   - **Without it:** If a site gets a lot of traffic and the only database is one master, it is overloaded with read and write requests. This makes the entire system slow for everyone on the site.
   - **Single point of failure:** Master-slave removes the single point of failure for reads.
   - **Scale out:** Reads are scaled out (traffic is scaled out) instead of scaling up. Scale up is very costly and not a practical choice.
   - **Fit:** It suits applications with few writes and many reads.

4. **Replication**
   - DB replication distributes data from the master machine to the slave machines. It can be *synchronous or asynchronous*, depending on the system's need.
   - All writes go to the master. Slaves replicate from it from time to time. Reads go to the slaves.

   | Type | Write returns | Read on slave | Use when |
   |------|---------------|---------------|----------|
   | Asynchronous | Right after master write | May be stale for a short time | A small delay is acceptable (cab booking) |
   | Synchronous | After slaves also succeed | Always latest | No delay is acceptable (banking, UPI) |

   - **Asynchronous replication**
     - **Example:** At t = 0, a write "set X = 10" reaches the master. The slaves get updated later, for example one at t = 10 and another at t = 12.
     - **Stale read:** Any read on a slave between t = 0 and its update time returns the old value of X (say 20).
     - **Fit:** It is fine when the application accepts a small delay in reads, as in the cab booking system.
     - **Limit:** The delay must not be large. It should be seconds, not hours or days. Updates should reach the replicas shortly after.
   - **Synchronous replication**
     - **Example:** Banking or UPI (GPay). The balance is 10000. A client pays 1000, so it must become 9000. If the client reads from a replica with a 10 second delay, it still shows the old balance 10000, which is wrong.
     - **How:** Replicate synchronously. When the write `X = X - 1000` arrives, do not return success until it has been replicated. Apply it on the master. Send the same query to each slave. Only after the slaves return success, return success for the write.
     - **Use:** When no delay at all is acceptable.
   - **Choice:** Which one to use depends on the system being built.
   - **What if an update query reaches a slave?**
     - **Best option:** Never allow it. The slave is designed for read only and never accepts write queries.
     - **If you allow it:** You must propagate it to the master (for example through application-layer code on your server). Then it is no longer a master-slave model. It becomes a master-master model.
     - **Master-master:** This is Pattern 4 of Lecture 19 (multi-primary configuration). Many masters are arranged in a circular way, and each propagates writes to the others. You must work out master-to-master propagation.
     - **Original rule:** In master-slave architecture, the master takes only writes and the slave takes only reads.

## Advantages

1. **Backup:** If the primary (master) goes down, read requests can still be sent to the slaves.
   - Writes are ignored for a while, but reads keep working. So the system does not fail completely. Only a portion fails.
   - **For multiple masters:** Go to the multi-primary configuration (Pattern 4).
2. **Read scale out:** Read operations are scaled out. This is good where reads are far more than writes. Latency is reduced and responses come faster.
3. **Availability:** Availability increases and the site becomes reliable.
4. **Parallelism:** Read requests are split across the slaves and execute in parallel.
