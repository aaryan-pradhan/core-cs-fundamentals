# 9. Data Modelling and Choosing a Database

How you keep data matters. The data model is the backbone of the system.

- **Bad schema:** Slow queries, messy scaling and inconsistent data.
- **Type of data store matters:** Database, cache or blob store.
- **Type of database matters:** SQL, document, key-value, wide-column or graph.

## From requirements to schema

```mermaid
flowchart LR
    R["Requirements"] -->|"find the nouns"| E["Entities"]
    E -->|"give each a stable id"| K["Keys / IDs"]
    E -->|"how they connect"| REL["Relationships"]
    REL -->|"draw tables and fields"| S["Schema Sketch"]
    S -->|"for the hot queries"| I["Indexes and Scaling Notes"]
```

## The 3 drivers of schema decisions

| Driver | Question | What to check |
|--------|----------|---------------|
| Volume | How big? | Storage size, growth rate, partitioning |
| Access patterns | How is it queried? | Read endpoints, hot queries, write endpoints |
| Consistency | How strict? | Is eventual OK? Is auditability needed? Is ACID needed? |

- **ACID:** Atomicity (all or nothing), Consistency (rules always hold), Isolation (parallel transactions do not see each other's half work), Durability (a commit survives a crash).

## SQL vs NoSQL

| | SQL (relational) | NoSQL |
|---|------------------|-------|
| Structure | Fixed tables, columns and types | No fixed structure needed |
| Joins | Supported | Mostly not supported |
| Data integrity | Enforced by the DB with checks and foreign keys | Left to the app code |
| Horizontal scaling | Harder | Easy |
| Pick it when | You know the structure of the data | You have no predefined structure in mind yet |

**SQL example (maang.in):**

| Table | Columns |
|-------|---------|
| users | user_id, first_name, last_name, ... |
| problems | problem_id, problem_statement, constraints, ... |
| submissions | submission_id, problem_id, user_id, ... |

- **Data integrity:** A submission cannot be made if the user does not exist in the users table. The DB enforces this with checks. There are different types of checks.

**Switching later:**

- **SQL to NoSQL:** Switching is practically not possible.
- **NoSQL to SQL:** This makes more sense, once the structure is clear.

## Data models

| Model | How data is stored | Pros | Cons | Examples |
|-------|--------------------|------|------|----------|
| Relational | Tables of rows, linked by keys | Joins, transactions, integrity, mature tools | Fixed schema. Sharding is hard. | PostgreSQL, MySQL |
| Document | JSON-like documents, nested fields | Flexible schema. One read gets a whole object. | Weak joins. Data is often duplicated. | MongoDB, Firestore |
| Key-value | A key maps to a value | Fastest exact lookups. Scales easily. | Only lookup by key. No complex queries. | Redis, DynamoDB |
| Wide-column | Rows with many columns, spread by partition key | Huge write throughput. Good for time-series. | Queries must follow the partition key | Cassandra |
| Graph | Nodes and edges | Fast relationship traversal (friends of friends) | Hard to scale. Niche. | Neo4j |

## Choosing the DB

Rule of thumb for interviews: start with PostgreSQL. Use another DB only if the requirements demand it.

```mermaid
flowchart LR
    Q{"What do we need?"} -->|"transactions, joins, integrity"| PG[("PostgreSQL")]
    Q -->|"flexible schema, nested docs"| MG[("MongoDB / Firestore")]
    Q -->|"exact key lookup, caching, sessions"| RD[("Redis / DynamoDB")]
    Q -->|"huge writes, time-series"| CS[("Cassandra")]
    Q -->|"relationship traversal heavy"| GR[("Graph DB")]
```

- **Postgres scales far:** OpenAI scaled PostgreSQL to power 800 million ChatGPT users (openai.com/index/scaling-postgresql).

## Relational example: social media posts

Entities are users, posts, comments and likes.

| Relationship | Type |
|--------------|------|
| 1 user writes many posts | 1:N |
| 1 post has many comments | 1:N |
| Users like posts, via the likes table | N:M |

```mermaid
erDiagram
    USERS ||--o{ POSTS : writes
    USERS ||--o{ COMMENTS : writes
    USERS ||--o{ LIKES : gives
    POSTS ||--o{ COMMENTS : has
    POSTS ||--o{ LIKES : receives
    USERS {
        bigint id PK
        varchar username UK
        varchar email UK
        timestamp created_at
    }
    POSTS {
        bigint id PK
        bigint user_id FK
        text content
        timestamp created_at
    }
    COMMENTS {
        bigint id PK
        bigint post_id FK
        bigint user_id FK
        text content
        timestamp created_at
    }
    LIKES {
        bigint user_id FK
        bigint post_id FK
        timestamp created_at
    }
```

## Keys and relationships

- **System-generated IDs:** Use them. They are stable and never change.
- **Foreign keys:** They enforce integrity. At massive scale they are optional, because they slow writes and do not work across shards.
- **Composite key for likes:** Use `(user_id, post_id)` as the key. A user cannot like the same post twice.

## Normalization vs denormalization

| | Normalized | Denormalized |
|---|------------|--------------|
| Meaning | One source of truth. Each fact is stored once. | Fields are duplicated into other tables |
| Updates | Safe. Consistency is easy. | Hard. Every copy must change. |
| Reads | Need joins | Faster |
| Risk | Slow reads at scale | Inconsistency |

**Interview rule:**

1. Start normalized.
2. Denormalize only for a real read bottleneck.
3. Prefer a cache or a precomputed (materialized) view over duplicating the truth everywhere.

- **Materialized view:** A stored query result that the DB refreshes. Reads hit it directly.

## Scaling notes

SQL scales with read replicas, caching and sharding by access pattern. Topic 12 covers each one.

```mermaid
flowchart LR
    APP["App"] -->|"writes"| P[("Primary DB")]
    APP -->|"reads"| RR[("Read Replica")]
    APP -->|"hot reads"| C[("Cache")]
    P -->|"copies changes"| RR
    P -->|"too big?"| SH["Sharding"]
    SH -->|"user_id range 1"| S1[("Shard 1")]
    SH -->|"user_id range 2"| S2[("Shard 2")]
```

- **Sharding example:** With `user_id % 4`, a remainder of 0 sends the row to DB 1, 1 to DB 2, and so on. No single server scales forever. Many reasonable DB servers cost less than one huge one.
