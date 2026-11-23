# 9. Data Modelling and Choosing a Database

How you keep data matters, because the data model is the backbone of the system. A bad schema gives slow queries, messy scaling and inconsistent data. The type of store and the type of database both matter.

## Key terms

| Term | Meaning |
|------|---------|
| Schema | A schema is the plan of the data: the tables, their fields and how they link. |
| Entity | An entity is a thing the system stores, such as a user or a post. Each entity usually becomes one table. |
| Relation | A relation is how two entities link. 1:N means one user writes many posts. N:M means many users like many posts, through a middle table such as likes. |
| Primary key (PK) | A primary key is the field that names exactly one row, such as `id`. |
| Foreign key (FK) | A foreign key is a field that points to a primary key in another table, such as `posts.user_id`. The database rejects a row that points to nothing. |
| Index | An index is a separate structure that points to rows, so the database finds a row without reading every [page](07-storing-data-and-redis.md). The index is also stored as pages, so reading it costs [IO](07-storing-data-and-redis.md). |
| Transaction (ACID) | A transaction is a group of writes that succeed or fail together. ACID means it is all or nothing, it keeps the rules, it hides half-done work, and it survives a crash. |
| Normalization | Normalization stores each fact once, so there is one source of truth. |
| Denormalization | Denormalization copies fields into other tables, so reads need fewer joins. A join is a query that combines rows from two tables. |
| Materialized view | A materialized view is a stored query result that reads can hit directly. |

## How it works

Three questions drive every schema decision. **Volume** asks how big the data is and how fast it grows. **Access patterns** ask which reads, writes and hot queries the system runs. **[Consistency](05-scalability-availability-consistency.md)** asks how strict the data must be, for example whether ACID is needed.

1. **Find the entities.** Take the nouns from the requirements. A social media app has users, posts, comments and likes.
2. **Give each entity a stable id.** Use system-generated IDs, because they never change.
3. **Find the relations.** One user writes many posts (1:N). One post has many comments (1:N). Users like posts through the likes table (N:M).
4. **Sketch the schema.** Write each table with its fields and keys. Foreign keys enforce integrity, which means every link points to a real row. They are optional at massive scale. For likes, make `(user_id, post_id)` the primary key, so a user cannot like the same post twice.
5. **Add indexes and scaling notes.** Add an index for each hot query. SQL then scales with read [replicas](05-scalability-availability-consistency.md), a [cache](04-performance-throughput-load-balancing.md) and [sharding](12-scaling-databases.md), which splits the data across many databases.

| Table | Key fields |
|-------|------------|
| users | `id` (PK), `username`, `created_at` |
| posts | `id` (PK), `user_id` (FK), `content` |
| comments | `id` (PK), `post_id` (FK), `user_id` (FK), `content` |
| likes | `user_id` and `post_id` together form the PK. Each is also an FK. |

## Trade-offs

**Choosing the database:** Start with PostgreSQL. Use another database only if the requirements demand it.

| What you need | Data model | Pick |
|---------------|------------|------|
| You need transactions, joins and integrity. | Relational | PostgreSQL |
| You need a flexible schema with nested documents. | Document | MongoDB, Firestore |
| You need exact key lookups, caching or sessions. | [Key-value](07-storing-data-and-redis.md) | Redis, DynamoDB |
| You need huge writes or time-series data. | Wide-column | Cassandra |
| You mostly walk relationships, such as friends of friends. | Graph | Graph DB |

| | [SQL](07-storing-data-and-redis.md) | [NoSQL](07-storing-data-and-redis.md) |
|---|-----|-------|
| Structure | Tables have a fixed structure. | No fixed structure is needed. |
| Joins | Joins are supported. | Joins are mostly not supported. |
| Integrity | The database checks it, for example that a submission's user exists. | The app code must check it. |
| Horizontal scaling | It is harder. | It is easy. |
| Pick it when | You know the structure of the data. | You have no fixed structure in mind yet. |

Moving from SQL to NoSQL later is very hard. Moving from NoSQL to SQL makes more sense once the structure is clear.

| | Normalized | Denormalized |
|---|------------|--------------|
| Updates | Updates are safe, so consistency is easy. | Every copy must change. |
| Reads | Reads need joins. | Reads are faster. |
| Risk | Reads get slow at scale. | The copies can disagree. |

**Numbers:** OpenAI scaled PostgreSQL to power 800 million ChatGPT users.

> **Interview:** Say "I start with PostgreSQL and a normalized schema". Pick another database only when the access pattern demands it. Denormalize only for a real read bottleneck, and prefer a cache or a materialized view first.

## Likely questions

- **SQL or NoSQL?** Start with PostgreSQL for transactions, joins and integrity. Choose NoSQL when the structure is not fixed or the writes are huge.
- **What drives schema decisions?** Volume, access patterns and consistency drive them.
- **Why is the likes key `(user_id, post_id)`?** A composite primary key stops a user from liking the same post twice.
- **When do you denormalize?** Denormalize only for a real read bottleneck. Try a cache or a materialized view first.
- **Which database takes huge writes?** Cassandra, a wide-column database, is built for huge writes and time-series data.
