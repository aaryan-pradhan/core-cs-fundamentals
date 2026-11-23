# 2. Requirements

## What a requirement is

Frame the requirements before you solve anything. A requirement is a statement. It defines one or more of these:

- **Behaviour:** What the system must do.
- **Quality constraints:** How well it must do it.
- **Conditions:** Under what conditions it must do it, such as scale, failures, security and compliance.

| Bad requirement | Good requirement |
|-----------------|------------------|
| "It should be fast" | "p95 latency < 200 ms at 5k QPS" |

- **p95 latency:** 95% of requests finish within this time. Only the slowest 5% take longer.
- **QPS:** Queries (requests) per second. RPS means the same thing.

> **Interview:** Always put a number and a load on a quality. "Fast" means nothing. "p95 < 200 ms at 5k QPS" can be tested.

## Main types of requirements

There are two types, functional and non-functional.

### A) Functional Requirements (FR)

An FR says what the system does. It is a feature the user can use.

| System | Functional requirements |
|--------|-------------------------|
| Live Counter | 1. `GET /counter` returns the current counter value. 2. `POST /increment` increases the counter by 1. |
| Other products | "User can upload PDFs". "Search returns the top 10 results". |

**How to write an FR:**

- **Form 1:** "User should be able to ... X ...".
- **Form 2:** "User should see ... X ... happening".
- **No implementation details:** An FR names the product behaviour only. It never names a database, queue or server.
- **Minimal flow:** Think of the smallest flow of the product that still works.
- **Below the line:** List the features you will not build as "out of scope". This keeps the design small and shows you thought of them.

### B) Non-Functional Requirements (NFR)

An NFR is a quality attribute. It says how good the system must be. Seniority starts to show here.

| No. | NFR | Meaning | Live Counter example |
|-----|-----|---------|----------------------|
| 1 | **Performance (Latency)** | How fast responses are | `GET /counter` p95 < 100 ms. `POST /increment` p95 < 150 ms. |
| 2 | **Throughput (Capacity / QPS)** | How many requests per second you can handle | Support 10k QPS of GET plus 2k QPS of increment. |
| 3 | **Scalability (Growth handling)** | Ability to grow smoothly as users and traffic grow | Problem: every `POST /increment` hits the same DB row. That row becomes a hotspot. |
| 4 | **Availability (Uptime)** | The system keeps answering requests | Keep serving the count even if the DB fails. |
| 5 | **Reliability (Correctness under failures)** | It works correctly even when things fail, such as timeouts and retries | Risk: the client retries `POST /increment`, so the count goes up twice. |
| 6 | **Consistency (Strong vs Eventual)** | Whether every reader sees the latest value | Do all users see the same count at the same moment? |
| 7 | **Durability (No data loss)** | An acknowledged write is never lost | An increment the user saw succeed must stay counted. |
| 8 | **Security (Auth + Abuse protection)** | Only allowed users do allowed things, and abuse is blocked | Stop one user from sending a million increments. |
| 9 | **Observability (Logs, Metrics, Tracing)** | You can see what the system is doing | Know the error rate and latency of `GET /counter`. |
| 10 | **Maintainability / Operability (Safe changes and deployment)** | You can change and deploy safely | Ship a new version without breaking the counter. |

Each NFR has a standard fix. Topics 4 to 6 solve all ten on the Live Counter.

## Why NFRs are hard

- **Harder than FRs:** FRs come from the product. NFRs need judgement.
- **Guesses on numbers:** You estimate users, traffic and sizes yourself.
- **No set standards:** No rule says "every app needs 99.9%".
- **Experiential:** The right numbers come from experience with real systems.

## Which NFRs to cover in an interview

Cover NFRs in this order, after the FRs.

1. **Start with C vs A (CAP):** Decide if the system prefers consistency or availability. See topic 14.
2. **Then estimate DAU:** DAU means daily active users.
3. **Then estimate throughput:** Discuss the read to write ratio.
4. **Then estimate latency.**
5. **Storage (if relevant):** Estimate storage if the system stores a lot.
6. **Bandwidth (if relevant):** Estimate network bandwidth if the system moves a lot of data.

- **Limit:** Never go beyond 3 or 4 NFRs.
- **The core three:** Performance (latency), Throughput (QPS) and Consistency (strong vs eventual).

## Latency targets by product type

| Product type | Latency target |
|--------------|----------------|
| Real-time product, such as a live game | 50 to 100 ms. Worst case below 200 ms, or it is no longer real-time. |
| Social media website | Below 200 ms |
| Normal API | Well under 1 second. Users give up after about 5 seconds. |
| Long task, such as finding a ride | 1 to 2 minutes, then cancel |

> **Interview:** Some systems need strong consistency, such as the board in a live game. A chat app like Slack can live with eventual consistency.
