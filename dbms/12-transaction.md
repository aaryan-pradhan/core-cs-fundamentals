# Lecture 12: Transaction

> **The story:** Bank ABC has two accounts. A has Rs 1000 and B has Rs 2000. You send Rs 50 from A to B. The bank must never lose or create money.

## 1. One click, six steps

You press "Send Rs 50" once. The DB runs it as six steps in a fixed order. Together they form one transaction.

```mermaid
flowchart LR
  S1["1. Read(A)<br/>A = 1000"] --> S2["2. A = A - 50<br/>A = 950"] --> S3["3. Write(A)"] --> S4["4. Read(B)<br/>B = 2000"] --> S5["5. B = B + 50<br/>B = 2050"] --> S6["6. Write(B)"]
```

| Term | Meaning |
|---|---|
| Transaction | It is one logical unit of work made of one or more SQL statements. |
| Commit | All changes become permanent together. |
| Rollback | A failure undoes every change of the transaction. |
| SQL | The commands are `BEGIN TRANSACTION`, `COMMIT` and `END TRANSACTION`. |

> **Interview:** A transaction is complete only when all of its steps complete.

## 2. Where the work happens

The DB lives on disk. Read copies A into a RAM buffer. Write also changes only the buffer. Only COMMIT puts the change on disk.

```mermaid
flowchart LR
  D[("Disk<br/>A = 1000")] -->|"Read(A)"| B["RAM buffer<br/>A = 950 after A - 50"]
  B -->|"Write(A): still in buffer"| B
  B -->|"COMMIT"| D2[("Disk<br/>A = 950")]
```

## 3. ACID: four things that can go wrong

Each ACID property stops one disaster in the transfer.

```mermaid
flowchart TB
  ACID["ACID keeps the transfer safe"]
  ACID --> A["Atomicity<br/>all 6 steps or none"]
  ACID --> C["Consistency<br/>total stays Rs 3000"]
  ACID --> I["Isolation<br/>parallel transfers look sequential"]
  ACID --> D["Durability<br/>a committed transfer survives a crash"]
```

| Property | Rule | Who ensures it |
|---|---|---|
| Atomicity | All steps happen, or none happen. | The recovery system rolls back. |
| Consistency | Integrity constraints hold before and after. | Correct atomicity gives consistency. |
| Isolation | Concurrent transactions behave as if run one by one. | The DB uses locks. |
| Durability | Committed changes survive any failure. | The recovery manager uses logs. |

> **Interview:** "What are the ACID properties?" is a very famous question. Explain each one with the A to B transfer.

## 4. Atomicity: the crash in the middle

A is debited. Then the server crashes before B is credited. Rs 50 vanishes, so the DB rolls back to the old state.

```mermaid
flowchart LR
  O["Old state<br/>A = 1000, B = 2000<br/>total 3000"] --> M["Steps 1 to 3 done<br/>A = 950, B = 2000"]
  M -->|"crash before B"| X["Total 2950<br/>Rs 50 lost"]
  X -->|"never committed, so roll back"| O
```

The DB keeps the old state apart from the half-done state. That is how it can roll back.

## 5. Consistency: count the money

The total money in the bank must be the same before and after.

| Moment | A | B | Total | Consistent? |
|---|---|---|---|---|
| Before | 1000 | 2000 | 3000 | Yes. |
| After success | 950 | 2050 | 3000 | Yes. |
| After crash, no rollback | 950 | 2000 | 2950 | No. |

## 6. Isolation: two phones, one account

You send Rs 50 from your phone (T1). At the same moment, net banking (T2) also sends Rs 50. Both read the old value of A.

```mermaid
sequenceDiagram
  participant T1 as T1 (phone)
  participant DB as DB
  participant T2 as T2 (net banking)
  T1->>DB: Read(A) = 1000
  T2->>DB: Read(A) = 1000
  T1->>DB: Write(A) = 950
  T2->>DB: Write(A) = 950
  T1->>DB: B = 2000 + 50
  T2->>DB: B = 2050 + 50
  Note over DB: A = 950, B = 2100, total 3050. Rs 50 was created.
```

The fix is to make T2 wait until T1 ends. In reality both run together, but locks make the result look sequential.

## 7. Durability: the crash after "Success"

The app shows "Success". Then the server crashes before RAM reaches disk. The log on disk lets the DB redo the transfer.

```mermaid
flowchart LR
  T["Transfer done in RAM<br/>A = 950, B = 2050"] -->|"every operation"| L[("Log on disk")]
  T -->|"writing to DB file"| X["Crash<br/>RAM wiped"]
  X -->|"restart"| R["Recovery manager<br/>reads the log"]
  L --> R
  R -->|"redo changes"| D[("Disk<br/>A = 950, B = 2050")]
```

Checkpoints also help recovery. They are covered in the next lecture.

## 8. The life of a transaction

Every transfer moves through these states. It ends either committed or aborted.

```mermaid
stateDiagram-v2
  [*] --> Active
  Active --> PartiallyCommitted: all reads and writes done
  Active --> Failed: error
  PartiallyCommitted --> Committed: COMMIT saved to disk
  PartiallyCommitted --> Failed: error
  Failed --> Aborted: roll back
  Committed --> Terminated
  Aborted --> Terminated
  Terminated --> [*]
```

| State | What happens | Transfer example |
|---|---|---|
| Active | All reads and writes run here. | Steps 1 to 6 run. |
| Partially committed | The last step is done, but changes sit in the RAM buffer. | A = 950 and B = 2050 exist only in RAM. |
| Committed | Changes are permanent. Rollback is no longer possible. | The disk shows A = 950 and B = 2050. |
| Failed | A hardware, software, network or user error stops the transaction. | The server crashes at Write(A). |
| Aborted | Every buffered change is undone. The old state returns. | The disk still shows A = 1000 and B = 2000. |
| Terminated | The transaction has either committed or aborted. | The transfer is over. |

> **Interview:** A committed transaction can never be rolled back. A failed one always ends as aborted.
