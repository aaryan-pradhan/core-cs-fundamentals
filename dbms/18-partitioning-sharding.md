# Lecture 18: Partitioning & Sharding in DBMS (DB Optimisation)

## LEC-18: Partitioning & Sharding in DBMS (DB Optimisation)

Context (why DB optimisation techniques are needed)

- A DBMS makes storing data easy, but a very large system has two problems: huge data and a huge number of requests.
- Huge data (an application serving masses, e.g. a website hosted on the cloud with a live event): hard to manage and deal with on a single node, so manageability suffers.
- Huge number of requests (millions): a single node cannot serve them properly. At some point the system may crash, or its response time becomes very high.
- Fix: distribute the data. The result is a distributed database.
- DB optimisation techniques make data easily manageable and reduce response time.
- Option 1: Scale up (vertical scaling, increase hardware).
    1. E.g. 1 TB disk to 2 TB, CPU doubled, RAM doubled.
    2. In practice response time does not become half when everything is doubled.
    3. Cost increases a lot (disk, CPU, RAM). It is an expensive bet and not logical in terms of money.
- Option 2: Clustering (replica set).
    1. Copies of the same DB instance are made, so all data is replicated (redundancy).
    2. There is a master node and replicas. Updates always come to the master, and the master propagates them to the replicas.
    3. Propagation causes delay, and it has to be managed.
    4. Problem: one replica may be updated while another is not yet updated.
- A level above clustering, and a better way, is partitioning.
- Partitioning is a scale-out (horizontal scaling) technique. The capacity of a single node is not increased. Data is split and new nodes are added.
- Clustering is also horizontal scaling (new nodes are added), but there the whole data is copied. In partitioning the data is divided between servers.

1.   A big problem can be solved easily when it is chopped into several smaller sub-problems. That is what the partitioning technique does. It divides a big database containing data metrics and indexes into smaller and handy slices of data called partitions. The partitioned tables are directly used by SQL queries without any alteration. Once the database is partitioned, the data definition language can easily work on the smaller partitioned slices, instead of handling the giant database altogether. This is how partitioning cuts down the problems in managing large database tables.
2.   Partitioning is the technique used to divide stored database objects into separate servers. Due to this, there is an increase in performance, controllability of the data. We can manage huge chunks of data optimally. When we horizontally scale our machines/servers, we know that it gives us a challenging time dealing with relational databases as it's quite tough to maintain the relations. But if we apply partitioning to the database that is already scaled out i.e. equipped with multiple servers, we can partition our database among those servers and handle the big data easily.
    - Partitioning is applied when response time has increased because data is huge and traversing it takes a lot of time.
    - Example: Student table (name, id, class, address, phone number) with a huge number of students.
3.   **Vertical Partitioning**
      1. Slicing relation vertically / column-wise.
          - E.g. the first two columns go to server S1 and the other two columns go to server S2.
      2. Need to access different servers to get complete tuples.
          - To get the complete information of one tuple, both servers must be accessed.
4.   **Horizontal Partitioning**
      1. Slicing relation horizontally / row-wise.
          - E.g. roll no 1 to 25K on S1 and roll no 25K to 100K on S2.
      2. Independent chunks of data tuples are stored in different servers.
          - Students 1 to 10000 are fetched from S1 only, so S1 is independent of S2.
5.   **When Partitioning is Applied?**
      1. Dataset become much huge that managing and dealing with it become a tedious task.
      2. The number of requests are enough larger that the single DB server access is taking huge time and hence the system's response time become high.
          - This is the more important and better reason to apply partitioning. Tables are then divided horizontally or vertically.
6.   **Advantages of Partitioning**
      1. Parallelism
          - Chunk 1 is on S1 and chunk 2 is on S2. Multiple incoming requests are filtered by the key (e.g. id 1 to 10000 on S1, the rest on S2) and each request is sent to the server holding its data, so requests are served in parallel.
      2. Availability
          - All DB optimisation techniques increase availability (as in clustering). If node S1 crashes, only the requests for S1's data are affected, not all of them.
      3. Performance
          - Each server is less loaded. If all the data were on one system it would be more loaded and processing would take more time. Requests are also divided between servers, so response time decreases.
      4. Manageability
          - A DBA who has to change something for students 1 to 10000 goes to S1 only, and it is quicker. Likewise for S2. It gives a bird's-eye view: this half of the data is here, so work on it here.
      5. Reduce Cost, as scaling-up or vertical scaling might be costly.
          - Instead of one big costly machine, use more machines of smaller capacity. Each machine only gets part of the requests.
7.   **Distributed Database**
      1. A single logical database that is, spread across multiple locations (servers) and logically interconnected by network.
          - After partitioning, data sits on different servers, but logically it is still the same database (e.g. the Student table, or a university database).
      2. This is the product of applying DB optimisation techniques like **Clustering, Partitioning and Sharding.**
      3. Why this is needed? READ Point **5**.
          - Requests have increased and data has become huge, so DB optimisation techniques are applied.
8.   **Sharding**
      1. Technique to implement Horizontal Partitioning.
          - It is an extension of partitioning.
      2. The **fundamental idea** of Sharding is the idea that instead of having all the data sit on one DB instance, we split it up and introduce a Routing layer so that we can forward the request to the right instances that actually contain the data.
          - Example: Student data. Roll no 1 to 10K is stored on S1 and the rest to 100K on S2. It is a horizontal partition (tuple-wise: the full tuple goes to one node). Each part is called a shard: Shard 1 holds roll no 1 to 10K, Shard 2 holds roll no above 10K to 100K.
          - Shards are independent. A request for roll no 1 to 10K goes to S1, other requests go to S2.
          - Routing layer: a layer written in the application layer / software that decides which shard a request goes to (S1 or S2). It is additional logic / a lookup (an intermediate layer). It is needed whenever sharding is applied.
          - Example: Invoice table, with the data split between Database Shard 1 and Database Shard 2 (one colour of rows on each). The split is made on a custom id (customer id), not on the primary key (invoice id).
          - The column on which the split is made is called the shard key (partition key). In the Student table it was student/roll no. In the Invoice table the primary key is invoice id, but the shard key can be something else (customer id).
          - Each shard is stored on its own server. Shard is just a name.
          - In system design interviews and in industry, partitioning and sharding are used as the same thing (vertical sharding, horizontal sharding). They are not exactly synonyms. By theory, sharding is a way of horizontal partitioning.
      3. **Pros**
          1. Scalability
              - It is a technique to increase scalability (scale out). Parallelism, availability, manageability and lower cost also follow, as listed above.
          2. Availability
      4. **Cons**
          1. Complexity, making partition mapping, Routing layer to be implemented in the system, Non-uniformity that creates the necessity of Re-Sharding
              - Mapping: it must be identified which shard a particular request belongs to, based on the partition key. This needs an additional routing layer which you write yourself.
              - Non-uniformity: the shard key should divide the data uniformly (e.g. 3 rows to each node out of 6). But if the shard key is not the primary key, one key value can have far more rows (e.g. customer id 2 has placed 10,000 orders), so that shard gets much more data than the other. The division becomes non-uniform and the original problem comes back.
              - Handling it is your responsibility: Re-Shard from time to time, i.e. change the partition key and shard again.
          2. Not well suited for Analytical type of queries, as the data is spread across different DB instances. (Scatter-Gather problem)
              - Example: Invoice table with an amount column, and the query is the total amount ordered by each customer. On a single node, one aggregation function (SUM) in SQL would answer it. With sharding, the data is on multiple nodes, so the query goes to the first node and finds its sum, goes to the second node and finds its sum, then combines both sums. Another layer / the DBMS has to handle this. This adds complexity.
- You have to give up something to gain something: pros come with cons. Sharding and partitioning are still used a lot.
- Interview question: you have a large number of requests on one system and must reduce response time. Answer: shard the data across different nodes, write a routing layer that sends each request to its particular shard. This gives manageability, scale out, scalability, availability, parallelism and performance, and avoids scaling up (vertical scaling is costly).
- Clustering (replica set), partitioning and sharding are all very important. Know the core idea of each for system design interview questions on how to optimise a system.
