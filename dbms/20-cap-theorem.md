# Lecture 20: CAP Theorem

> **The story:** Your app's database grew too big for one machine. You split it into Node A (primary, takes writes) and Node B (replica, takes reads). One day the network link between them breaks.

## 1. Why there are two nodes at all

One node could not handle the load. You scaled up as far as you could, then scaled out.

```mermaid
flowchart LR
  S[("One node<br/>too many requests")] -->|"scale out"| A[("Node A<br/>primary: writes")]
  S -->|"scale out"| B[("Node B<br/>replica: reads")]
  A -->|"replicate x = 20"| B
```

## 2. The three properties

Each letter of CAP is one promise the system can make.

```mermaid
flowchart TB
  CAP["CAP"]
  CAP --> C["Consistency<br/>every node returns the latest write<br/>x = 10 on A, so x = 10 on B"]
  CAP --> AV["Availability<br/>every request gets a response<br/>even if some nodes are down"]
  CAP --> P["Partition tolerance<br/>the system keeps running<br/>when the link between nodes breaks"]
```

| Property | Promise |
|---|---|
| Consistency | Every read returns the most recent write, on every node. |
| Availability | Every request gets a response. The response may be stale. |
| Partition tolerance | The system survives dropped or delayed messages between nodes. |
| Partition | A partition is a break in communication between nodes. |

## 3. The link breaks

A writer sets x = 10 on Node A. The link is down, so Node B still holds x = 20. A reader now asks Node B for x.

```mermaid
sequenceDiagram
  participant W as Writer
  participant A as Node A (primary)
  participant B as Node B (x = 20)
  participant R as Reader
  Note over A,B: Partition: link A to B is down
  W->>A: write x = 10
  A--xB: replicate (fails)
  R->>B: read x
  alt Ending 1: stay available (AP)
    B-->>R: x = 20 (stale, consistency lost)
  else Ending 2: stay consistent (CP)
    B-->>R: error (availability lost)
  end
```

The CAP theorem says this: during a partition, you must give up either consistency or availability. A distributed system gets only two of the three.

## 4. Pick two

Partitions always happen in a distributed system. So the real choice is CP or AP.

```mermaid
flowchart TB
  C(("Consistency"))
  A(("Availability"))
  P(("Partition<br/>tolerance"))
  C --- CA["CA: MySQL, PostgreSQL<br/>single node only"] --- A
  C --- CP["CP: MongoDB"] --- P
  A --- AP["AP: Cassandra, DynamoDB"] --- P
```

| Type | Gives | Gives up | Examples |
|---|---|---|---|
| CA | It gives consistency and availability. | It gives up partition tolerance. | MySQL, PostgreSQL on one node |
| CP | It gives consistency and partition tolerance. | It gives up availability. | MongoDB |
| AP | It gives availability and partition tolerance. | It gives up consistency. | Cassandra, DynamoDB |

## 5. CA: the single-node ending

CA works only when a partition can never happen. That means one node, which is not distributed.

```mermaid
flowchart LR
  O[("One MySQL node<br/>no link to break")] --> OK["No partition<br/>so C and A both hold"]
  D[("MySQL on 2 linked nodes")] --> BR["The link will break someday<br/>so C and A cannot both hold"]
```

## 6. CP: the bank's ending

A bank cannot show 1 lakh on one node and 2 lakh on another. It switches off the stale node until the link is fixed.

```mermaid
flowchart LR
  P["Partition"] --> OFF["Node B (stale) is turned off<br/>reads on B return an error"]
  OFF --> FIX["Link fixed"] --> ON["Node B syncs and comes back"]
```

| CP fact | Detail |
|---|---|
| Writes | Only one primary node takes all writes in a replica set. |
| Failover | A secondary takes over if the primary fails. |
| Example | MongoDB is a schema-less document DB and is CP. |
| Use case | Banking uses CP. Downtime is acceptable, wrong balances are not. |

## 7. AP: the social media ending

A feed must never go down. Both nodes keep serving, and they agree again later.

```mermaid
flowchart LR
  P["Partition"] --> I["Both nodes serve reads and writes<br/>A: x = 10, B: x = 20"]
  I --> L["Link re-established"]
  L --> S["Replication syncs<br/>A = B, x = 10"]
```

This is **eventual consistency**: the nodes become consistent once the partition heals.

| AP fact | Detail |
|---|---|
| Primary | Cassandra has no primary node, so every node stays available. |
| Stale reads | A user on a stale node may see old data for a while. |
| Recovery | The nodes sync after the partition is resolved. |
| Use case | Social media uses AP. A slightly old feed is acceptable, downtime is not. |

## 8. Which database do you choose?

The business decides what matters more during a partition.

```mermaid
flowchart TB
  Q{"What matters more during a partition?"}
  Q -- "consistency (banking)" --> CP["CP: MongoDB<br/>follows ACID"]
  Q -- "availability (social media)" --> AP["AP: Cassandra, DynamoDB<br/>follows BASE"]
  Q -- "no partition (single node)" --> CA["CA: MySQL, PostgreSQL"]
```

## 9. ACID vs BASE

> **Interview:** ACID vs BASE is a common interview question.

| | ACID | BASE |
|---|---|---|
| Stands for | It stands for Atomicity, Consistency, Isolation, Durability. | It stands for Basically Available, Soft state, Eventual consistency. |
| Priority | It puts correctness first. | It puts availability first. |
| Consistency | Data is consistent after every transaction. | Data becomes consistent eventually. |
| Fits | It fits CP systems such as banking. | It fits AP systems such as social media. |
