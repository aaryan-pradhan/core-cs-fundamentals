# Lecture 17: Clustering in DBMS

1. **Database clustering** means making **replica sets**. It combines more than one server or instance that connect to a single database.
   - **Why:** Sometimes one server cannot handle the amount of data or the number of requests. Then a data cluster is needed.
   - **Related terms:** Database clustering, SQL server clustering and SQL clustering are closely associated. SQL is the language used to manage the database information.
   - **Cluster:** A bundle, collection or group of servers (nodes) holding the same database.
   - **Example problem:** One database holds all the info. Millions of customers send millions of requests daily from all over the world. One DB on one computer cannot serve worldwide requests easily, however much it is scaled vertically (super computer).
   - **Availability risk:** If that one database or computer goes down, availability is gone. The website is down and users shout.
   - **Popularity:** Clustering became popular with the internet. It is mostly used with NoSQL, where multiple servers and horizontal scaling are needed. It works with SQL too.
   - **Example:** MongoDB provides replica sets (replication), so you can make replicas of the database.

2. **Replicate the same dataset on different servers.**
   - Make servers S1, S2 and S3 holding databases D1, D2 and D3. D1 = D2 = D3, so the same data is stored on all three servers.
   - It is not the case that S1 holds more users and S2 fewer. Every server holds the same users' data (for example 1000 users on each).
   - This set of servers (replicas) is one cluster.

   ```mermaid
   flowchart LR
     subgraph Cluster["One cluster (replica set)"]
       direction TB
       S1["S1: D1"]
       S2["S2: D2"]
       S3["S3: D3"]
     end
     S1 <-. "sync: D1 = D2 = D3" .-> S2
     S2 <-. "sync" .-> S3
   ```
   - **Architecture:** Create the same instances, make replicas, and store them as a cluster.
   - **Server / node / host:** A capable computer connected to the internet. Its main job is to store data, take requests, process the data and send it back.

3. **Advantages**

   1. **Data redundancy:** The same data is stored on multiple servers. If any server fails for any reason, the data is available on the other servers.
      - **Not harmful:** This is not the repetition of data that leads to anomalies (the same student stored repeatedly inside one database). Here the same data is replicated across different servers. Within one database it is not duplicated.
      - **Required:** The redundancy that clustering offers is required. It is certain because of synchronisation. It is not always bad. Here it makes the system robust and highly available.
      - **Example:** S1 shuts down (hacker attack, illegal activity detected, regular maintenance, or any problem with the node). With a single server, the website would go down. With replicas, S2 returns the same data. The user never knows whether data came from S1 or S2. The website stays on.

      ```mermaid
      flowchart LR
        U["User"] --> S1["S1<br/>down"]
        U --> S2["S2<br/>returns the same data"]
        S1 -. "fails" .-> X["no reply"]
      ```
      - **Abstraction:** A layer of abstraction is added. The user does not know whether data comes from S1, S2 or S3. This is hidden from the user.

   2. **Load balancing:** Load balancing (scalability) does not come by default with a database. Clustering has to bring it. It also depends on the setup.
      - **What it does:** It allocates the workload among the different servers in the cluster. One machine does not get all the hits.
      - **Benefit:** More users can be supported. If traffic spikes, there is higher assurance that the new traffic is supported. Scaling is seamless.
      - **Link to availability:** This links directly to high availability. Without load balancing, one machine could get overworked and traffic would slow down. Then traffic would drop to zero.
      - **Single server:** With one server and millions of requests, the server handles all of them sequentially. It gets highly loaded and may hang or crash.
      - **With replicas:** Give some requests to S1, some to S2 and some to S3. The load is balanced and no system crashes.
      - **Why balance:** Requests execute fast (an overloaded server delays them). No single server crashes. Both point to availability.
      - **Load balancer:** This needs a layer, logic or interface called the load balancer. Requests arrive at the load balancer. It checks which server (S1, S2 or S3) is less loaded and passes the new request to it.

      ```mermaid
      flowchart LR
        R["Requests"] --> LB["Load balancer<br/>picks the least loaded"]
        LB --> S1["S1"]
        LB --> S2["S2"]
        LB --> S3["S3"]
      ```
      - **Architecture:** With replica sets, the architecture needs a load balancer.

   3. **High availability:** If you can access a database, it is available. High availability is the amount of time a database is considered available.
      - **How much:** The availability you need depends on the number of transactions you run and how often you run analytics on your data.
      - **How clustering helps:** Load balancing and extra machines give extremely high availability. If a server shuts down, the database is still available.
      - **Backup:** If S1 goes down, S2 and S3 are available as backup. At any point of time, some server will execute the request.
      - **Goal:** The website should always stay on.

4. **How does clustering work?**

   1. In cluster architecture, requests are split across many computers. One user request is executed and produced by a number of computer systems.
      - **Basis:** Clustering works because of load balancing and high availability.
      - **Failure:** If one node collapses, another node handles the request. So there are few or no chances of a total system failure.
      - **Routing:** The load balancer sends each incoming request to the less loaded server (node).
      - **Real life:** Big product-based companies use it for internet products. It ensures high availability and a seamless user experience. The website never goes down.
