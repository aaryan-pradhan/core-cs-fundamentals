# Lecture 17: Clustering in DBMS

1. **Database Clustering** (making **Replica-sets**) is the process of combining more than one servers or instances connecting a single database. Sometimes one server may not be adequate to manage the amount of data or the number of requests, that is when a Data Cluster is needed. Database clustering, SQL server clustering, and SQL clustering are closely associated with SQL is the language used to manage the database information.
   - Cluster = bundle / collection / group of servers (nodes) holding the same database.
   - Example problem: one database holds all info, millions of customers send millions of requests daily from all over the world. One DB on one computer, however much it is scaled vertically (super computer), cannot serve worldwide requests easily.
   - If that one database/computer goes down, availability is gone: website down, users shout.
   - Clustering became popular with the internet; mostly used with NoSQL, where multiple servers and horizontal scaling are needed. Works with SQL too.
   - MongoDB is a good example: it provides replica sets (replication) so you can make replicas of the database.
2. Replicate the same dataset on different servers.
   - Make servers S1, S2, S3 holding databases D1, D2, D3 where D1 = D2 = D3: same data stored on all three servers.
   - Not that S1 holds more users and S2 fewer. Every server holds the same users' data (e.g. 1000 users on each).
   - This set of servers / replicas is one cluster. Architecture: create same instances, make replicas, store them as a cluster.
   - Server / node / host = a capable computer connected to the internet whose main job is to store data, take requests, process the data and send it back.
3. **Advantages**
   1. **Data Redundancy:** Clustering of databases helps with data redundancy, as we store the same data at multiple servers. Don't confuse this data redundancy as repetition of the same data that might lead to some anomalies. The redundancy that clustering offers is required and is quite certain due to the synchronisation. In case any of the servers had to face a failure due to any possible reason, the data is available at other servers to access.
      - Not the redundancy that causes anomalies (same student stored repeatedly inside one database). Here the same data is replicated across different servers; within the same database it is not duplicated.
      - Redundancy is not always bad; here it makes the system robust and highly available.
      - Example: S1 shuts down (hacker attack, illegal activity detected, regular maintenance, any problem with the node). With a single server the website would go down. With replicas, the user never knows whether data came from S1 or S2; S2 returns the same data. Website stays on.
      - A layer of abstraction is added: the user does not know whether data comes from S1, S2 or S3. This is hidden from the user.
   2. **Load balancing:** or scalability doesn't come by default with the database. It has to be brought by clustering regularly. It also depends on the setup. Basically, what load balancing does is allocating the workload among the different servers that are part of the cluster. This indicates that more users can be supported and if for some reasons if a huge spike in the traffic appears, there is a higher assurance that it will be able to support the new traffic. One machine is not going to get all of the hits. This can provide scaling seamlessly as required. This **links directly to high availability.** Without load balancing, a particular machine could get overworked and traffic would slow down, leading to decrement of the traffic to zero.
      - With one server and millions of requests, all are handled sequentially by it: it gets highly loaded, may hang or crash.
      - With replicas, give some requests to S1, some to S2, some to S3. Load is balanced and no system crashes.
      - Load balancing is done so that requests execute fast (an overloaded server delays) and so that no single server crashes. Both point to availability.
      - Needs a layer / logic / interface: the load balancer. Requests arrive at the load balancer; it checks which server (S1, S2, S3) is less loaded and passes the new request to it.
      - So with replica sets the architecture needs a load balancer.
   3. **High availability:** When you can access a database, it implies that it is available. High availability refers the amount of time a database is considered available. The amount of availability you need greatly depends on the number of transactions you are running on your database and how often you are running any kind of analytics on your data. With database clustering, we can reach extremely high levels of availability due to load balancing and have extra machines. In case a server got shut down the database will, however, be available.
      - If S1 goes down, S2 and S3 are available as backup, so at any point of time some server will execute the request.
      - Website should always stay on.
4. **How does Clustering Work?**
   1. In cluster architecture, all requests are split with many computers so that an individual user request is executed and produced by a number of computer systems. The clustering is serviceable definitely by the ability of load balancing and high-availability. If one node collapses, the request is handled by another node. Consequently, there are few or no possibilities of absolute system failures.
      - The load balancer sends each incoming request to the less loaded server / node.
      - Used in real life by big product-based companies for internet products, to ensure high availability and a seamless user experience: website never goes down.
