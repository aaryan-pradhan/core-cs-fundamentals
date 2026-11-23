# 16. The Design Rules

Every design follows the same 7 steps, in the same order. Say each step's name out loud. Get the interviewer to agree on steps 1 to 3 before you draw.

| Step | Output |
|------|--------|
| 1. FR | 3 to 4 "User should be able to ..." lines, plus out of scope |
| 2. NFR | CAP per flow, latency target |
| 3. Estimates | Users per second, read and write QPS at peak, connections if real-time |
| 4. Entities | Nouns of the FRs, with key fields |
| 5. APIs | One endpoint per FR action |
| 6. Basic diagram | Gateway, one service per FR, DB. "With this design, FRs are satisfied." |
| 7. Problems | One problem at a time. Each fix exposes the next one. |

## Step 1: FR

- **Form:** "User should be able to ...". No implementation details.
- **Count:** 3 to 4 core lines.
- **Out of scope:** List what you will not design (payments, notifications, search...).

## Step 2: NFR

- **CAP:** Pick per flow (topic 14). Money, booking, game state: consistency. Feeds, chat, views: availability.
- **Latency:** One number for the main action. Example: "first token under 500 ms".
- **Count:** 3 to 4 NFRs at most.

## Step 3: Estimates

Use 1 day = 3600 × 24 ≈ 10^5 seconds.

| Quantity | Formula | Example (Rapido) |
|----------|---------|------------------|
| Users per second | DAU / 10^5 | 10^8 / 10^5 = 1,000 |
| Read QPS | users/s × reads per user × peak (5×) | 1,000 × 5 × 5 = 25K |
| Write QPS | users/s × writes per user × peak (5×) | 1,000 × 2 × 5 = 10K |
| Connections (real-time only) | concurrent users | chess: 500K games × 2 = 1M |

Then say what the numbers mean:

- **Reads much more than writes:** Read heavy. Cache and read replicas.
- **Writes over about 5K per second:** One Postgres cannot take it. Use Redis, or shard.
- **Many open connections:** Many stateful servers. Routing becomes a problem.

## Step 4: Entities

- **Rule:** Underline the nouns in the FRs. Each important noun is an entity.
- **Fields:** Key fields only: id, owner, status, time.

## Step 5: APIs

- **One endpoint per FR action:** `POST` creates, `GET` reads, `PATCH` updates.
- **Nouns, plural:** `/rides`, `/chats/{chatId}/messages`.
- **User from the token:** Never put `userId` in the body. The gateway reads it from the JWT.
- **Real-time apps:** Also list WebSocket messages, for example `sendMove {from, to}`.

## Step 6: Basic diagram

- **Boxes:** Client, API gateway (auth, rate limit, TLS), one service per FR, DB.
- **Walk it:** Trace each FR along the arrows.
- **Close:** Say "with this design, FRs are satisfied". Keep it simple. Scaling is step 7.

## Step 7: Problems, one by one

Ask of each box: "what breaks at our numbers?" Fix it. Then ask again.

| Problem | Standard fix |
|---------|--------------|
| One server cannot take the QPS | Stateless servers behind an LB (topic 4) |
| Too many reads | Cache in Redis, read replicas (topics 10, 12) |
| Too many writes or too much data | Shard the DB, with consistent hashing (topic 12) |
| Client needs live updates | Polling, then SSE (server only pushes), then WebSocket (both ways) |
| WebSocket servers are stateful | Registry of user to server, or pub/sub (topic 26) |
| Slow or bursty work | Queue + worker pool. Queue full: return `429` (back pressure). |
| Two users grab the same thing | Distributed lock, or a conditional update in the DB |
| Hot cache key expires, everyone recomputes | Lock: one request recomputes, the rest wait (thundering herd, topic 11) |
| Big files | Blob store, pre-signed URL, CDN (topics 8, 10) |
| Server crashes and loses data | Write to the DB or a log before you reply |

End with a table: each part, and how it scales.

## Pushing updates to the client

| Pattern | How | Direction | Use |
|---------|-----|-----------|-----|
| Short polling | Client calls `GET` every few seconds | Client asks | Rare updates. Wastes calls. |
| SSE | One HTTP response stays open. Server writes events into it. | Server to client | Streaming tokens, live scores |
| WebSocket | One connection, both sides send any time | Both ways | Chat, games, live location |

- **Polling cost:** A 30 s answer with 3 s polling needs 10 API calls.
- **WebSocket cost:** The connection is stateful. Messages must be routed to the user's server.

> **Interview:** Name the step you are on. Satisfy the FRs first with a simple design. Spend the rest of the time on the problems.

## Likely questions

- **How do you start a design?** FRs, then NFRs, then estimates. Agree on them before drawing.
- **How do you get QPS from DAU?** DAU / 10^5 gives users per second. Multiply by requests per user, then by 5 for peak.
- **When do you need WebSockets?** When both sides send at any time (chat, games). If only the server pushes, use SSE.
- **When do you add a queue?** When work is slow or bursty. Workers pull at their own rate.
- **How do you stop two users booking the same thing?** A lock, or `UPDATE ... WHERE status = 'available'` and check the row count.
