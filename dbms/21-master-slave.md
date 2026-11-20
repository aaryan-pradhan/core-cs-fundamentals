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

1. Master-Slave is a general way to optimise IO in a system where number of requests goes way high that a single DB server is not able to handle it efficiently.
   - A normal setup: servers S1, S2, S3 behind a load balancer. Millions of requests reach the load balancer, which sends each one to the least busy server.
   - If there is only one DB, every request from every server goes to that one DB. It serves all servers as the database server.
   - This is a single point of failure: if that DB crashes or gets hacked, the whole system blocks, availability becomes zero, and requests are not served (they return bad requests / failures).
   - Solution: add another DB as a copy (replica). Requests are divided between the DBs, so some go to one and some to the other.
   - This architecture is called Master-Slave architecture: one DB is the master, the other is the slave.
   - Master-Slave is very widely used in computer science (also seen as master-slave flip-flop in circuits). Interviewers ask directly "what is the master-slave model".
   - The name is falling out of use for ethical reasons (master dictates, slave obeys). Some places say primary/replica. Similarly Git's `master` branch is renamed `main`. The concept is the same.
   - The master DB may be SQL while the slaves are MongoDB, i.e. the data model of the primary and the replicas can differ. But then interfaces must be written to replicate between them so the application works properly.
2. Its a Pattern 3 in LEC-19 (Database Scaling Pattern). (Command Query Responsibility Segregation)
   - Lecture 19 covered this practically (cab booking app); this lecture covers it formally. Revise lecture 19 for a real-life example of DB scaling.
3. The true or latest data is kept in the Master DB thus write operations are directed there. Reading ops are done only from slaves. This architecture serves the purpose of safeguarding site reliability, availability, reduce latency etc . If a site receives a lot of traffic and the only available database is one master, it will be overloaded with reading and writing requests. Making the entire system slow for everyone on the site.
   - Master is the original DB; also called the latest DB, owner DB or primary DB. Whatever it holds is the latest information.
   - All writes go to the master only, so that it always has the latest data. Slaves never take write operations.
   - Slaves replicate from the master to get the new updates, and handle only read operations.
   - Master-slave removes the single point of failure for reads.
   - Reads are scaled out, i.e. traffic is scaled out, instead of scaling up (scale up is very costly and not a practical choice).
   - Fits applications with few writes and many reads.
4. DB *replication* will take care of distributing data from Master machine to Slaves machines. This can be *synchronous or asynchronous* depending upon the system's need.
   - All writes go to the master; slaves replicate from it from time to time. Reads are given to the slaves.
   - Asynchronous replication:
     - Example: at t = 0 a write "set X = 10" reaches the master. The slaves get updated later, e.g. one at t = 10 and another at t = 12.
     - Any read on a slave between t = 0 and its update time returns the old value of X (say 20).
     - Fine when the application accepts a small delay in reads, as in the cab booking system. The delay must not be large: seconds, not hours or days. Updates should reach the replicas shortly after.
   - Synchronous replication:
     - Example: banking / UPI (GPay). Balance is 10000, a client pays 1000, so it must become 9000. If the client reads from a replica with a 10 second delay, it still shows the old balance 10000, which is wrong.
     - So replicate synchronously: when the write `X = X - 1000` arrives, do not return success until it has been replicated. Apply it on the master, send the same query to each slave, and only after the slaves return success return success for the write.
     - Used when no delay at all is acceptable.
   - Which one to use depends on the system being built.
   - What if an update query reaches a slave:
     - Best option: never allow it. The slave is designed for read only and never accepts write queries.
     - If you allow it, you must propagate it to the master (e.g. through application-layer code on your server). Then it is no longer a master-slave model; it becomes a master-master model.
     - That is Pattern 4 of Lecture 19 (multi-primary configuration): many masters arranged in a circular way, each propagating writes to the others. You must work out master-to-master propagation.
     - Original master-slave architecture says the master only takes writes and the slave only takes reads.

## Advantages

1. Backup: if the primary/master goes down, read requests can still be sent to the slaves. Writes are ignored for a while, but reads keep working, so the system does not fail completely. Only a portion fails. It acts as a backup. For multiple masters, go to the multi-primary configuration (Pattern 4).
2. Read operations are scaled out. Good where reads are far more than writes. Latency is reduced, responses come faster.
3. Availability increases and the site becomes reliable.
4. Parallelism: read requests are split across the slaves and execute in parallel.
