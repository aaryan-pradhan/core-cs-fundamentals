# 4. Performance, Throughput and Load Balancing

One server breaks as users grow. A cache fixes slow responses (latency). More servers behind a load balancer fix too many requests (throughput).

## Key terms

| Term | Meaning |
|------|---------|
| Latency | Time for one request to get a response |
| Throughput (QPS) | Requests the system handles per second |
| Cache | Fast store in RAM (Redis) that holds copies of hot data |
| Vertical scaling | Make one server bigger (more CPU, RAM) |
| Horizontal scaling | Add more servers |
| Load balancer (LB) | Spreads requests across servers. Examples: AWS ELB, NGINX. |
| Stateless server | Keeps no client data. Any server can serve any request. |
| Stateful server | Keeps client data. That client must always reach the same server. |
| Sticky session | The LB sends one user to the same server every time |
| Data center | A building of servers. Big systems run several, in different regions. |

## How it works

Each fix creates the next problem:

1. **One server goes down:** Nobody is served. Fix: run many servers.
2. **Each server has its own data:** Data drifts apart. Fix: move data to one shared DB.
3. **Responses are slow:** Every request hits the DB. Fix: a cache. Look in Redis first. On a miss, read the DB and store the result in Redis (cache-aside, topic 11).
4. **Too many requests for one server:** Fix: add servers (horizontal) behind an LB.
5. **Servers keep state in RAM:** The LB cannot send any request anywhere. Fix: make servers stateless. Keep shared state in Redis or the DB.

```mermaid
flowchart LR
    C["Clients"] -->|"requests"| LB["Load Balancer"]
    LB -->|"any request"| S1["App Server 1<br/>(stateless)"]
    LB -->|"any request"| S2["App Server 2<br/>(stateless)"]
    S1 -->|"1. look in cache"| R[("Redis")]
    S2 -->|"1. look in cache"| R
    S1 -->|"2. on a miss"| D[("Database")]
    S2 -->|"2. on a miss"| D
```

## Trade-offs

| Option | Pick when | Cost |
|--------|-----------|------|
| Vertical scaling | Small load, quick fix | One machine has a ceiling. Big machines cost a lot. |
| Horizontal scaling | Load keeps growing | Needs an LB and stateless servers |
| Round robin LB | Requests cost about the same | A slow request or weak server still gets equal share |
| Weighted round robin | Servers have different power | Weights are fixed. They ignore live load. |
| Load-aware LB | Request costs vary a lot | LB needs live stats from each server |
| Stateless servers | Almost always | Shared state must live in Redis or the DB |
| Stateful servers | Speed needs in-memory state (chat sockets, games) | Hard to scale. Users must be routed to their server. |

## Numbers

| Thing | Rough value |
|-------|-------------|
| Redis operation | About 1 ms |
| One 2-vCPU server, no DB call | 1,000 to 10,000 QPS |
| One 2-vCPU server, one DB read per request | 200 to 1,500 QPS |
| One 2-vCPU server, one DB write per request | 100 to 800 QPS |

> **Interview:** Say "the app servers are stateless, so the LB can send any request anywhere". This is the base of horizontal scaling.

## Likely questions

- **Vertical or horizontal?** Horizontal. Vertical hits a ceiling and costs more.
- **What does a load balancer do?** It spreads requests across servers, so no server gets all the load.
- **Why stateless servers?** Any server can take any request. So you just add servers to scale.
- **Where does the state go then?** Shared state goes in Redis. Durable data goes in the DB.
- **Why add a cache?** RAM is about 1 ms. A DB read is much slower. Hot reads skip the DB.
