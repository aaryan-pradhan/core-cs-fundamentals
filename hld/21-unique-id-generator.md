# 21. Unique ID Generator

Every new record, such as a message or an order, needs an ID. With many servers and a [sharded](12-scaling-databases.md) DB, making IDs that never repeat is hard. Twitter Snowflake is the usual answer.

## Key terms

| Term | Meaning |
|------|---------|
| Auto-increment | Auto-increment is a DB column that adds 1 to the last ID for each new row. |
| UUID | A UUID (Universally Unique Identifier) is a random 128-bit ID that any server makes on its own. |
| Ticket server | A ticket server is one central server whose only job is to hand out the next ID. |
| Snowflake ID | A Snowflake ID is a 64-bit ID built from a timestamp, a data center ID, a machine ID and a counter. Twitter made it. |
| Epoch | An epoch is a fixed start time. A timestamp counts the milliseconds since it. |
| Unix timestamp | A Unix timestamp counts the time since 1 January 1970. |
| NTP | NTP (Network Time Protocol) keeps the clocks of many servers in sync over the network. |

## How it works

First, agree on four requirements. The ID must be unique. It must be sorted by time, so a record made at 7:46 gets a bigger ID than one made at 7:45. It must fit in 64 bits. It must be numeric, because the character set decides the length.

1. **One server keeps a counter in RAM.** If it restarts, the counter goes back to 0, and old IDs repeat. The fix is to store the counter in the DB and read it back on restart.
2. **Many servers each keep a counter.** The counters drift apart, and syncing them is very hard. One DB with auto-increment works, but only while one DB holds all the data. Once the data is sharded, each shard starts from 1, and IDs repeat.
3. **Each of k DBs steps by k.** With 4 DBs, DB1 gives 1, 5, 9 and DB2 gives 2, 6, 10. The IDs are unique, numeric and 64-bit. They are not sorted by time: two requests to DB1 get 1 and 5, then a third request to DB2 gets 2. Adding a fifth DB changes every rule, so it is hard.
4. **A UUID needs no coordination.** Each server makes its own random ID. A repeat is very unlikely but still possible, so the rare case must be handled. A UUID is 128 bits, not sorted by time and not numeric.
5. **A ticket server meets all four requirements.** It runs the counter-in-DB loop from step 1, and every web server asks it for IDs. But it is a [single point of failure](05-scalability-availability-consistency.md), and a second ticket server brings back the sync problem.
6. **Snowflake splits the 64 bits.** Each machine builds IDs on its own, so no sync is needed. The timestamp sits in the highest bits, so a later millisecond gives a bigger ID. The data center ID, machine ID and sequence never repeat within one millisecond, so the ID is unique.

```mermaid
flowchart LR
    S["1 bit<br/>sign, always 0"] -->|"then"| T["41 bits<br/>ms since epoch"]
    T -->|"then"| D["5 bits<br/>data center ID"]
    D -->|"then"| M["5 bits<br/>machine ID"]
    M -->|"then"| Q["12 bits<br/>sequence per ms"]
```

## Trade-offs

| | Step by k | UUID | Ticket server | Snowflake |
|---|-----------|------|---------------|-----------|
| Unique | Yes | Very likely | Yes | Yes |
| Sorted by time | No | No | Yes | Yes, if clocks match |
| 64-bit and numeric | Yes | No, 128-bit | Yes | Yes |
| Weak point | Adding a DB is hard. | It is long and random. | It is a single point of failure. | It needs synced clocks. |

**Snowflake limits:**

- **Sequence:** One machine can make only 2^12 = 4096 IDs in one millisecond. Twitter chose 12 bits, but the split depends on the QPS.
- **Clocks:** IDs from different machines are sorted only if their clocks match. Servers use NTP to keep their clocks close.
- **Timestamp runs out:** 41 bits of milliseconds last about 69 years. Then you reset the epoch to 0, or use the spare sign bit.

**Numbers:** A Snowflake ID is 64 bits: 1 + 41 + 5 + 5 + 12. That gives 32 data centers, 32 machines in each, and 4096 IDs per millisecond per machine. A UUID is 128 bits.

> **Interview:** Ask the four requirements first. Then say "Snowflake gives unique, time-sorted 64-bit IDs with no sync between machines", and name each field.

## Likely questions

- **Why not auto-increment?** It works only on one DB. Once the data is sharded, each shard counts from 1, so IDs repeat.
- **Why not a UUID?** It is 128 bits, it is not numeric, and it is not sorted by time.
- **What is wrong with a ticket server?** It is a single point of failure, and adding a second one brings back the sync problem.
- **How is a Snowflake ID unique?** Each machine has its own data center and machine ID, and its 12-bit sequence never repeats within one millisecond.
- **What is Snowflake's weak point?** Order across machines needs synced clocks, so servers run NTP.
