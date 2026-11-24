# Lecture 21: Master-Slave Database

> **The story:** Your shop goes viral. Millions of people browse products, but only a few place orders. One database cannot keep up, so you give it helpers.

## 1. One DB drowns

Three servers sit behind a load balancer, but all of them hit the same DB. If that DB crashes, the whole shop stops.

```mermaid
flowchart LR
  U["Millions of requests"] --> LB["Load balancer"]
  LB --> S1["Server 1"] & S2["Server 2"] & S3["Server 3"]
  S1 --> DB[("One DB<br/>overloaded<br/>single point of failure")]
  S2 --> DB
  S3 --> DB
```

## 2. Hire helpers: master and slaves

You copy the DB onto more machines. The master takes every write. The slaves copy from the master and serve every read.

```mermaid
flowchart LR
  App["App"] -- "write: place order" --> M[("Master<br/>latest data")]
  M -- "replicate" --> R1[("Slave 1")]
  M -- "replicate" --> R2[("Slave 2")]
  App -- "read: browse products" --> R1
  App -- "read: browse products" --> R2
```

| Role | Takes | Other names |
|---|---|---|
| Master | It takes only writes. It always holds the latest data. | It is also called the primary or owner DB. |
| Slave | It takes only reads. It copies new data from the master. | It is also called a replica. |

> **Interview:** "What is the master-slave model?" is asked directly. Today it is often called primary-replica. It is the CQRS pattern from Lecture 19.

The master and slaves can use different data models, such as a PostgreSQL master with MongoDB slaves. Then you must write code to translate the replicated data.

## 3. Replication, ending 1: asynchronous

A customer changes X from 20 to 10. The master says "done" at once. The slaves catch up a few seconds later, so an early read can be stale.

```mermaid
sequenceDiagram
  participant C as Client
  participant M as Master
  participant S1 as Slave 1
  participant S2 as Slave 2
  C->>M: t = 0, set X = 10
  M-->>C: success at once
  C->>S1: read X at t = 5
  S1-->>C: X = 20 (stale)
  M->>S1: t = 10, replicate X = 10
  M->>S2: t = 12, replicate X = 10
```

## 4. Replication, ending 2: synchronous

A UPI payment drops a balance from 10000 to 9000. A stale 10000 would be wrong, so the master waits for every slave before saying "done".

```mermaid
sequenceDiagram
  participant C as Client
  participant M as Master
  participant S as Slaves
  C->>M: X = X - 1000 (10000 to 9000)
  M->>S: same query
  S-->>M: success
  M-->>C: success, only now
```

| Type | Write returns | Read on slave | Use when |
|---|---|---|---|
| Asynchronous | It returns right after the master writes. | It may be stale for a few seconds. | A small delay is fine, as in cab booking. |
| Synchronous | It returns after all slaves also succeed. | It is always the latest. | No delay is allowed, as in banking or UPI. |

The async delay must stay in seconds, never hours.

## 5. A write lands on a slave

A buggy server sends an update to Slave 1. The rule says slaves never accept writes.

```mermaid
flowchart LR
  W["UPDATE sent to Slave 1"] --> Q{"Allow it?"}
  Q -- "No (best)" --> N["Rejected<br/>slaves are read-only"]
  Q -- "Yes" --> Y["Slave must push it to the master<br/>now it is master-master<br/>(multi-primary, Lecture 19)"]
```

## 6. The master dies

The master crashes during a sale. Customers can still browse, but nobody can order until the master returns.

```mermaid
flowchart LR
  W["Writes"] -. "fail for a while" .-> M[("Master: down")]
  R["Reads"] --> S1[("Slave 1: up")]
  R --> S2[("Slave 2: up")]
```

Only part of the system fails, not the whole system. For writes that survive a dead master, use multi-primary.

## 7. Why it pays off

| Advantage | Meaning |
|---|---|
| Backup | Reads still work when the master goes down. |
| Read scale-out | You add slaves instead of buying one huge machine. |
| Lower latency | Reads spread out, so responses come faster. |
| Availability | Reads no longer have a single point of failure. |
| Parallelism | Slaves serve read requests at the same time. |

It fits apps with few writes and many reads.
