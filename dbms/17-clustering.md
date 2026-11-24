# Lecture 17: Clustering in DBMS

> **The story:** Your shop goes global. Millions of users hit one DB server every day. The server cannot keep up, so you copy it.

## 1. One server is not enough

One DB on one machine serves the whole world. A bigger machine (vertical scaling) still hits a limit. If that machine dies, the website dies.

```mermaid
flowchart LR
  U["Millions of requests<br/>from all over the world"] --> S["One DB server<br/>all data, all requests"]
  S --> P1["Overloaded<br/>slow, may hang or crash"]
  S --> P2["Single point of failure<br/>server down, so site down"]
```

## 2. Make replicas: the cluster

You put the same data on three servers. This group of identical servers is one cluster, also called a replica set.

```mermaid
flowchart LR
  subgraph Cluster["One cluster (replica set)"]
    direction TB
    S1["S1: D1<br/>1000 users"]
    S2["S2: D2<br/>same 1000 users"]
    S3["S3: D3<br/>same 1000 users"]
  end
  S1 <-. "sync: D1 = D2 = D3" .-> S2
  S2 <-. "sync" .-> S3
```

| Term | Meaning |
|---|---|
| Database clustering | It is running more than one server that holds the same database. |
| Cluster | It is the group of servers (nodes) that hold the same data. |
| Replica | It is one copy of the full database on one server. |
| Node / server / host | It is a machine that stores data, takes requests and sends replies. |
| Used with | It is common in NoSQL (MongoDB replica sets) but works with SQL too. |

## 3. S1 crashes, the site stays up

A hacker attack takes S1 down. S2 still holds the same data, so it answers. The user never knows which server replied.

```mermaid
flowchart LR
  U["User asks for order 21"] --> S1["S1<br/>down"]
  S1 -. "no reply" .-> X["fails"]
  U --> S2["S2<br/>returns order 21"]
  S2 --> OK["Site stays up"]
```

> **Interview:** Is this redundancy bad? No. Bad redundancy repeats data inside one DB and causes anomalies. Clustering copies the whole DB across servers on purpose, which makes the system robust.

## 4. Traffic spikes: the load balancer

A sale starts and traffic triples. A load balancer sits in front. It sends each request to the least loaded server.

```mermaid
flowchart LR
  R["Requests 1, 2, 3, 4, 5, 6"] --> LB["Load balancer<br/>picks the least loaded server"]
  LB -->|"1, 4"| S1["S1"]
  LB -->|"2, 5"| S2["S2"]
  LB -->|"3, 6"| S3["S3"]
```

Without it, one server takes every request in sequence and may crash.

## 5. The three wins

```mermaid
flowchart TB
  C["Clustering"]
  C --> R["Data redundancy<br/>same data on every server"]
  C --> L["Load balancing<br/>work spread across servers"]
  C --> H["High availability<br/>some server always answers"]
  R --> H
  L --> H
```

| Advantage | What it gives |
|---|---|
| Data redundancy | If one server fails, the others still have the data. |
| Load balancing | No single server is overloaded, so requests run fast. |
| High availability | The database stays reachable even when a node dies. |
| Abstraction | The user does not know which server served the request. |

## 6. How it works, end to end

Each request goes to the load balancer, then to a healthy, lightly loaded node. If a node collapses, another node takes the request. Total failure is very unlikely.

```mermaid
flowchart LR
  U["User request"] --> LB["Load balancer"]
  LB --> Q{"S1 healthy<br/>and least loaded?"}
  Q -- "Yes" --> S1["S1 serves it"]
  Q -- "No" --> S2["S2 or S3 serves it"]
```
