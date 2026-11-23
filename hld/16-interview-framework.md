# 16. The Design Rules

Every design follows the same 7 steps, in the same order. Keep it basic: an SDE-1 interview is 45 minutes. Say each step's name out loud.

| Step | Output |
|------|--------|
| 1. FR | 3 "User should be able to ..." lines, plus out of scope |
| 2. NFR | CAP and latency |
| 3. Estimates | DAU, users per second, read and write QPS |
| 4. Entities | Nouns of the FRs, with key fields |
| 5. APIs | One endpoint per FR |
| 6. Basic diagram | Gateway, services, DB. "With this design, FRs are satisfied." |
| 7. Problems | 3 or 4 problems, one at a time, each with one fix |

## Step 1: FR

- **Form:** "User should be able to ...". No databases or servers in an FR.
- **Count:** 3 core features. Only what the app basically does.
- **Out of scope:** Name what you skip (payments, notifications, live tracking...).

## Step 2: NFR

- **CAP:** Pick one (topic 14). Money, booking, game moves: consistency (CP). Feeds, chat, views: availability (AP).
- **Latency:** One number for the main action. Example: "a ride in under 2 minutes".

## Step 3: Estimates

1 day = 3600 × 24 ≈ 10^5 seconds.

| Quantity | Formula | Example (Rapido) |
|----------|---------|------------------|
| Users per second | DAU / 10^5 | 10^8 / 10^5 = 1,000 |
| Read QPS (peak) | users/s × reads per user × 5 | 1,000 × 5 × 5 = 25K |
| Write QPS (peak) | users/s × writes per user × 5 | 1,000 × 2 × 5 = 10K |

Then say what it means:

- **Many more reads than writes:** Read heavy. Add a cache.
- **Writes over about 5K per second:** One Postgres cannot take it. Use Redis or a NoSQL DB like Cassandra.

## Step 4: Entities

Underline the nouns in the FRs. Each one is an entity. List key fields only: id, owner, status, time.

## Step 5: APIs

- **One endpoint per FR:** `POST` creates, `GET` reads, `PATCH` updates.
- **Plural nouns:** `/rides`, `/chats/{chatId}/messages`.

## Step 6: Basic diagram

Client, API gateway (auth, rate limit), one service per FR, DB. Walk each FR along the arrows. Say "with this design, FRs are satisfied".

## Step 7: Problems

Ask: "what breaks at our numbers?" Fix it. Ask again. Stop after 3 or 4.

| Problem | Standard fix |
|---------|--------------|
| One server cannot take the QPS | More stateless servers behind a load balancer (topic 4) |
| Too many reads | Cache in Redis (topic 10) |
| Too many writes | Redis, a NoSQL DB, or sharding (topic 12) |
| Client needs live updates | Server only pushes: SSE. Both sides send: WebSocket. |
| User's WebSocket is on another server | Registry in Redis: `user: server` |
| Slow work | Queue + workers (topic 13) |
| Two users grab the same thing | Lock, or update only if still free |
| Big files | Blob storage (S3) and a CDN (topics 8, 10) |

## Pushing updates to the client

| Pattern | How | Use |
|---------|-----|-----|
| Polling | Client asks every few seconds | Rare updates. Wastes calls. |
| SSE | Server keeps one response open and writes into it | Server pushes only: AI tokens, live scores |
| WebSocket | One open connection, both sides send any time | Chat, games, live location |

> **Interview:** Name the step you are on. Satisfy the FRs with a simple design first. Then fix problems one by one.

## Likely questions

- **How do you start?** FRs, then NFRs, then estimates. Agree on them before drawing.
- **How do you get QPS from DAU?** DAU / 10^5 gives users per second. Multiply by requests per user, then by 5 for peak.
- **SSE or WebSocket?** SSE if only the server pushes. WebSocket if both sides send.
- **How do you stop two users booking the same thing?** A lock, or update the row only if it is still free.
