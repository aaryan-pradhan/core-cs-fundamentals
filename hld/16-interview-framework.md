# 16. The Design Rules

Every design follows the same 7 steps, in the same order. An SDE-1 interview lasts 45 to 50 minutes, so keep each step basic. Say each step's name out loud as you start it.

| Step | What you produce |
|------|------------------|
| 1. FR | You write 3 "User should be able to ..." lines and list what is out of scope. |
| 2. NFR | You choose CAP and set a latency target. |
| 3. Estimates | You work out DAU, users per second, and read and write QPS. |
| 4. Entities | You list the nouns of the FRs with their key fields. |
| 5. APIs | You write one endpoint per FR. |
| 6. Basic diagram | You draw the gateway, the services and the DB, and say "with this design, FRs are satisfied". |
| 7. Problems | You fix 3 or 4 problems, one at a time. |

## Step 1: FR

- **Form:** Write each FR as "User should be able to ...". An FR never names a database or a server.
- **Count:** Write 3 core features. They cover only what the app basically does.
- **Out of scope:** Name the features you skip, such as payments, notifications or live tracking.

## Step 2: NFR

- **CAP:** Pick consistency or availability (topic 14). Money, bookings and game moves need consistency (CP). Feeds, chats and view counts can choose availability (AP).
- **Latency:** Give one number for the main action, for example "a ride is matched in under 2 minutes".

## Step 3: Estimates

Use the [estimation](15-estimation.md) steps: a day is about 10^5 seconds, and the peak is 5 times the average.

| Quantity | Formula | Example (Rapido) |
|----------|---------|------------------|
| Users per second | DAU / 10^5 | 10^8 / 10^5 = 1,000 |
| Read QPS at peak | users per second × reads per user × 5 | 1,000 × 5 × 5 = 25K |
| Write QPS at peak | users per second × writes per user × 5 | 1,000 × 2 × 5 = 10K |

Then say what the numbers mean:

- **Reads are much higher than writes:** The system is read heavy, so add a cache.
- **Writes are above about 5K per second:** One Postgres server cannot take this. Use Redis, or Cassandra, a NoSQL database built for heavy writes.

## Step 4: Entities

Underline the nouns in the FRs. Each important noun is an entity. List only the key fields, such as id, owner, status and time.

## Step 5: APIs

- **One endpoint per FR:** `POST` creates, `GET` reads, and `PATCH` updates.
- **Plural nouns:** Name resources with plural nouns, such as `/rides` or `/chats/{chatId}/messages`.

## Step 6: Basic diagram

Draw the client, the API gateway (topic 6), one service per FR, and the DB. Walk each FR along the arrows. Then say "with this design, FRs are satisfied".

## Step 7: Problems

Ask "what breaks at our numbers?". Fix that one problem, then ask again. Stop after 3 or 4 problems.

**Ways to push updates to the client:**

| Pattern | How it works | Use it for |
|---------|--------------|------------|
| Polling | The client asks the server every few seconds. This wastes calls when nothing is new. | Rare updates |
| SSE (Server-Sent Events) | The server keeps one response open and writes new data into it. Only the server sends. | AI answers, live scores |
| WebSocket | One connection stays open, and both sides can send at any time. | Chat, games, live location |

**Common problems and their fixes:**

| Problem | Standard fix |
|---------|--------------|
| One server cannot take the QPS. | Add stateless servers behind a load balancer (topic 4). |
| There are too many reads. | Cache the hot data in Redis (topic 10). |
| There are too many writes. | Use Redis or Cassandra, or shard the DB (topic 12). |
| The client needs live updates. | Use SSE if only the server pushes. Use WebSocket if both sides send. |
| A user's WebSocket is on another server. | Keep a registry in Redis. A registry maps each user to the server that holds their WebSocket. |
| Some work is slow. | Put the work on a queue, and let workers do it (topic 13). |
| Two users grab the same item. | Use a lock, so only one user can hold the item. Or update the row only if it is still free. |
| Users upload big files. | Store them in blob storage such as S3, and serve them through a CDN (topics 8 and 10). |

> **Interview:** Name the step you are on. Satisfy the FRs with a simple design first. Then fix the problems one by one.

## Likely questions

- **How do you start a design?** Write the FRs, then the NFRs, then the estimates. Agree on them with the interviewer before you draw.
- **How do you get QPS from DAU?** Divide DAU by 10^5 to get users per second. Multiply by requests per user, then by 5 for the peak.
- **SSE or WebSocket?** Use SSE if only the server pushes. Use WebSocket if both sides send.
- **How do you stop two users booking the same thing?** Use a lock, or update the row only if it is still free.
