# Lecture 18: Partitioning and Sharding

> **The story:** You built a photo app. It went viral. Its User table now has 100K users and millions of requests. One DB server can no longer cope.

## 1. One server is drowning

The single server faces two problems at once. Huge data makes it hard to manage. Huge request volume makes it slow or makes it crash.

```mermaid
flowchart LR
  U["Millions of requests"] --> S["One DB server<br/>User table: 100K rows"]
  S --> P1["Problem 1: huge data<br/>hard to manage"]
  S --> P2["Problem 2: huge requests<br/>slow response, may crash"]
  P1 --> F["Fix: distribute the data<br/>= distributed database"]
  P2 --> F
```

## 2. Three ways out

You weigh three options. Partitioning wins because it splits the data instead of copying it.

```mermaid
flowchart TB
  Q["How to handle more load?"]
  Q --> A["Scale up<br/>1 TB to 2 TB, double CPU and RAM<br/>costly, time does not halve"]
  Q --> B["Clustering<br/>copy ALL data to replicas<br/>master propagates updates, lag"]
  Q --> C["Partitioning<br/>SPLIT data across servers<br/>scale out, cheap machines"]
```

| Option | Scaling type | What happens to data | Catch |
|---|---|---|---|
| Scale up | Vertical | One bigger machine holds it all. | It is costly, and time does not halve. |
| Clustering | Horizontal | Every node holds a full copy. | Replicas lag behind the master. |
| Partitioning | Horizontal | Each node holds only a part. | Relations across servers are harder. |

## 3. Cut by columns: vertical partitioning

You first slice the table by columns. Small, hot columns go to S1, and heavy columns go to S2.

| user_id | name | bio | photo |
|---|---|---|---|
| 1 | Asha | loves cats | a.jpg |
| 2 | Ben | runner | b.jpg |

```mermaid
flowchart LR
  T["User(user_id, name, bio, photo)"] -- "split columns" --> S1["S1<br/>user_id, name<br/>1 Asha / 2 Ben"]
  T -- "split columns" --> S2["S2<br/>user_id, bio, photo<br/>1 cats a.jpg / 2 runner b.jpg"]
  S1 --> J["Full row of Asha?<br/>read S1 AND S2"]
  S2 --> J
```

## 4. Cut by rows: horizontal partitioning

You then slice the table by rows instead. Each server holds full rows for one range of user_id.

```mermaid
flowchart LR
  T["User table<br/>100K rows"] -- "user_id 1 to 10K" --> S1["S1<br/>1 Asha ... 10000 Zoe<br/>full rows"]
  T -- "user_id 10K to 100K" --> S2["S2<br/>10001 Amit ... 100000 Yuki<br/>full rows"]
  S1 --> I["Full row of Asha?<br/>read S1 only"]
```

| Type | Slices by | Example | Full row needs |
|---|---|---|---|
| Vertical | Columns | Name on S1, photo on S2 | It needs both servers. |
| Horizontal | Rows | Users 1–10K on S1, the rest on S2 | It needs one server. |

## 5. Why partitioning pays off

Requests now spread across servers. Each server holds less and serves less.

```mermaid
flowchart LR
  R1["Request user 42"] --> S1["S1: users 1 to 10K"]
  R2["Request user 50000"] --> S2["S2: users 10K to 100K"]
  S1 -. "S1 crashes?" .-> X["Only users 1 to 10K are affected"]
```

| Advantage | What it means |
|---|---|
| Parallelism | Different servers answer different requests at the same time. |
| Availability | A crash on one server affects only its part of the data. |
| Performance | Each server is less loaded, so response time drops. |
| Manageability | A DBA fixes users 1–10K on S1 only. |
| Reduced cost | Many small machines are cheaper than one huge one. |

Apply partitioning when the data is too big to manage or when requests make a single server slow. Heavy request load is the stronger reason.

## 6. Still one database: distributed database

The data now lives on many servers. To the app, it is still one logical database.

```mermaid
flowchart TB
  L["One logical DB<br/>User table"] --- N1["Server S1"]
  L --- N2["Server S2"]
  L --- N3["Server S3"]
  N1 -. "network" .- N2
  N2 -. "network" .- N3
```

A distributed database is the result of clustering, partitioning and sharding.

## 7. Sharding: add a routing layer

Sharding is how you implement horizontal partitioning. Each part is a shard, and a routing layer in your app sends each request to the right shard.

```mermaid
flowchart LR
  A["Request: user 42"] --> RL{"Routing layer<br/>(app code)<br/>look up shard key"}
  RL -- "user_id 1 to 10K" --> SH1["Shard 1 on S1"]
  RL -- "user_id above 10K" --> SH2["Shard 2 on S2"]
```

The shard key need not be the PK. An Invoice table has PK invoice_id, but you can shard it by customer_id.

| Term | Meaning |
|---|---|
| Shard | A shard is one horizontal part of the table, on its own server. |
| Shard key | The shard key is the column used to split rows. It is also called the partition key. |
| Routing layer | The routing layer is app code that maps each request to its shard. |
| Re-sharding | Re-sharding means choosing a new shard key and splitting the data again. |

> **Interview:** People use "partitioning" and "sharding" as the same word. Strictly, sharding is a way to do horizontal partitioning.

## 8. Trouble 1: one shard gets too hot

You shard invoices by customer_id. Then customer 2 places 10,000 orders, and shard 1 overloads.

```mermaid
flowchart LR
  K["Shard key: customer_id"] --> A["Shard 1<br/>customer 2: 10,000 orders<br/>overloaded"]
  K --> B["Shard 2<br/>other customers: few orders"]
  A -. "non-uniform, so re-shard" .-> K
```

A good shard key spreads rows evenly. A bad one recreates the original problem, so you must re-shard from time to time.

## 9. Trouble 2: analytics need scatter-gather

The finance team asks for the total amount per customer. On one server, a single `SUM` would do. With shards, the query must visit every shard and combine the parts.

```mermaid
flowchart LR
  Q["SUM(amount) per customer"] -- "scatter" --> N1["Shard 1: partial sum"]
  Q -- "scatter" --> N2["Shard 2: partial sum"]
  N1 -- "gather" --> G["Combine the sums"]
  N2 -- "gather" --> G
```

| Pros of sharding | Cons of sharding |
|---|---|
| It scales out to more servers. | You must build the mapping and the routing layer. |
| It keeps the other shards available when one fails. | A skewed shard key forces re-sharding. |
| It serves requests in parallel. | Analytical queries need scatter-gather. |

## 10. The interview answer

The interviewer says: "One system gets a huge number of requests. Reduce the response time."

```mermaid
flowchart LR
  P["Huge requests on one DB"] --> S["Shard the data<br/>across nodes"] --> R["Write a routing layer<br/>that sends each request<br/>to its shard"]
  R --> G["You gain scale out, parallelism,<br/>availability, performance,<br/>manageability, lower cost"]
  R --> X["You avoid scale up<br/>which is costly"]
```
