# 2. Requirements

Frame the requirements before you solve anything. A requirement is a statement. It defines what the system must do, how well it must do it, and under what conditions. Conditions include scale, failures, security and compliance.

## Key terms

| Term | Meaning |
|------|---------|
| FR (functional requirement) | An FR says what the system does. It is a feature the user can use, such as "`GET /counter` returns the current count". |
| NFR (non-functional requirement) | An NFR is a quality attribute. It says how good the system must be, such as how fast or how available. |

A good requirement always has a number and a load. "It should be fast" is bad. "p95 [latency](03-one-computer-and-latency.md) < 200 ms at 5k [QPS](04-performance-throughput-load-balancing.md)" is good. Latency is the time one request takes, and QPS is the number of requests per second. p95 means 95% of requests finish within that time.

## How it works

1. **Write the FRs first:** Use the form "User should be able to ..." or "User should see ... happening". Think of the smallest flow of the product that still works.
2. **Keep FRs free of implementation:** An FR names only product behaviour. It never names a database, queue or server.
3. **List what is out of scope:** Name the features you will not build, "below the line". This keeps the design small.
4. **Then pick the NFRs:** There are ten common NFRs, listed below. Seniority starts to show here.

| NFR | Meaning | Live Counter example |
|-----|---------|----------------------|
| Performance (latency) | Responses are fast. | `GET /counter` p95 < 100 ms, and `POST /increment` p95 < 150 ms. |
| [Throughput](04-performance-throughput-load-balancing.md) (QPS) | The system handles many requests per second. | It supports 10k QPS of GET plus 2k QPS of increment. |
| [Scalability](05-scalability-availability-consistency.md) | The system grows smoothly as users and traffic grow. | Every increment hits the same DB row, so that row becomes a bottleneck. |
| [Availability](05-scalability-availability-consistency.md) | The system keeps answering requests. | It keeps serving the count even if the DB fails. |
| Reliability | The system works correctly when things fail, such as timeouts and retries. | A client retries `POST /increment`, so the count goes up twice. |
| [Consistency](05-scalability-availability-consistency.md) | Every reader sees the latest value, which is strong consistency, or sees it after a short delay, which is eventual consistency. | All users should see the same count. |
| Durability | An acknowledged write is never lost. | An increment that succeeded stays counted. |
| Security | Only allowed users do allowed things, and abuse is blocked. | One user cannot send a million increments. |
| [Observability](06-gateway-observability-maintainability.md) | You can see what the system is doing through logs, metrics and tracing. | You know the error rate and latency of `GET /counter`. |
| [Maintainability](06-gateway-observability-maintainability.md) | You can change and deploy the system safely. | You ship a new version without breaking the counter. |

## Trade-offs

| | FR | NFR |
|---|----|-----|
| Comes from | It comes from the product. | It comes from judgement and experience. |
| Numbers | It needs none. | You guess users, traffic and sizes yourself. |
| Standards | The product defines it. | No set standard exists, such as "every app needs 99.9%". |

**Which NFRs to cover:** Cover them after the FRs, in this order.

1. **C vs A:** Decide if the system prefers consistency or availability. This choice is [CAP](14-cap-theorem.md), the rule that a system split by a network failure must give up one of the two.
2. **DAU:** Estimate the [DAU](15-estimation.md), the number of daily active users.
3. **Throughput:** Estimate the QPS and discuss the read to write ratio.
4. **Latency:** Set a latency target.
5. **Storage or bandwidth:** Estimate these only if the system stores or moves a lot of data.

Never cover more than 3 or 4 NFRs. The core three are latency, throughput and consistency.

**Numbers:** A real-time game needs 50 to 100 ms and never more than 200 ms. A social media site needs under 200 ms. A normal API can make a user wait 5 s at most. Finding a ride can take 1 to 2 minutes before it is cancelled.

> **Interview:** Always put a number and a load on a quality. "Fast" means nothing, but "p95 < 200 ms at 5k QPS" can be tested.

## Likely questions

- **What is the difference between an FR and an NFR?** An FR says what the system does. An NFR says how well it does it.
- **Can an FR name a database?** No, it cannot. An FR names only product behaviour.
- **How many NFRs should you cover?** Cover 3 or 4 at most. Start with CAP, then DAU, throughput and latency.
- **Which systems need strong consistency?** A live game board needs strong consistency. A chat app like Slack can live with eventual consistency.
- **Why are NFRs harder than FRs?** You must guess the numbers, no set standard exists, and the right values come from experience.
