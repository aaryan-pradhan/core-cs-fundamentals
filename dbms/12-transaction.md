# Lecture 12: Transaction

1. Transaction
    1. A unit of work done against the DB in a logical sequence.
    2. Sequence is very important in transaction.
    3. It is a logical unit of work that contains one or more SQL statements. The result of all these statements in a transaction either gets completed successfully (all the changes made to the database are permanent) or if at any point any failure happens it gets rollbacked (all the changes being done are undone.)
    4. Example: bank ABC has two accounts, A (Rs 1000) and B (Rs 2000). Transfer Rs 50 from A to B. For the user it is one single operation (debit A, credit B). For the DB it is several steps.
    5. Transaction T1 for the transfer (6 logical steps, in this sequence):
        1. Read(A): read A's balance, check constraints (e.g. balance must not go negative).
        2. A = A - 50 (temporary change, A becomes 950).
        3. Write(A).
        4. Read(B).
        5. B = B + 50 (B becomes 2050).
        6. Write(B).
    6. These 6 steps together are one transaction because from the user's view it is one task. They must be atomic: treated as a single task. Either the whole transaction completes, or (error anywhere in between, e.g. cannot read B, server error, hardware failure, logical error) none of it happens.
    7. If failure comes after A was debited, the debited money is credited back (rolled back). Sometimes in real banks the rollback is not instant (money returns after hours or days) but it still gets rolled back.
    8. Why rollback matters: consistency. Money can neither be created nor destroyed. Total in the system is Rs 3000; if Rs 50 is deducted from A and the transaction is neither completed nor rolled back, the system has Rs 2950 and Rs 50 has vanished.
    9. Transaction = a unit of work made of many steps; only when all steps complete is the transaction complete.
    10. Read and Write inside a transaction:
        1. Read(A): the DB is on disk (still has 1000); read brings the value into a local buffer in main memory (RAM), where the program works.
        2. Write(A): conceptually writes the buffer value (950) into the DB on disk. (Simplification for understanding.)
        3. In real DB systems, write also goes only to a buffer in RAM (temporary). The change reaches the physical DB only when COMMIT is called at the end.
        4. SQL commands for a transaction: `BEGIN TRANSACTION`, `COMMIT`, `END TRANSACTION`.
2. ACID Properties
    1. To ensure integrity of the data, we require that the DB system maintain the following properties of the transaction.
        1. Very famous interview question: what are ACID properties?
        2. Integrity constraints (domain constraints, consistency constraints) were covered earlier. A transaction that does not follow these 4 properties brings inconsistency into the DB.
    2. Atomicity
        1. Either all operations of transaction are reflected properly in the DB, or none are.
        2. All 6 steps complete and reflect in the DB, or none do. Binary, 0 or 1, never fuzzy.
        3. Example: A = 1000, B = 2000. Read(A), A - 50 = 950, Write(A) done. Before B is updated the system crashes. Now A = 950, B = 2000, total 2950; Rs 50 is lost. This is an inconsistent state.
        4. So a transaction is either successful, or on failure it recovers to the old state. Here the old state is A = 1000, B = 2000; the transaction never reached the committed state, so roll back to the old state.
        5. The DB maintains the old state separately from the intermediate state to make this rollback possible.
    3. Consistency
        1. Integrity constraints must be maintained before and after transaction.
        2. DB must be consistent after transaction happens.
        3. Example: total money in the banking system is 3000 before the transaction, so it must be 3000 after it. One account is debited and another credited, so nothing is lost.
        4. If atomicity is implemented properly, consistency is maintained. The properties are closely related.
    4. Isolation
        1. Even though multiple transactions may execute concurrently, the system guarantees that, for every pair of transactions Ti and Tj, it appears to Ti that either Tj finished execution before Ti started, or Tj started execution after Ti finished. Thus, each transaction is unaware of other transactions executing concurrently in the system.
        2. Multiple transactions can happen in the system in isolation, without interfering each other.
        3. Example problem: T1 (you, from your phone) and T2 (net banking) both transfer Rs 50 from A to B at the same time. Both read A = 1000. T1 writes A = 950. T2 also computes 1000 - 50 = 950 and writes A = 950. Both credit B: B = 2000 + 50 + 50 = 2100. Result: A = 950, B = 2100, total 3050. Rs 50 was created, which is impossible.
        4. Solution: run transactions so that they look sequential. T2 does not start until T1 terminates (succeeds or fails).
        5. In reality both execute concurrently, but the DB implements locks so that the result is logically sequential. Total money stays consistent.
        6. Transaction A does not know transaction B is running and vice versa. They run independently and do not interfere.
        7. Isolation is a very important property: without it consistency breaks for the whole DB.
        8. Similar to OS: a decrement must be an atomic operation, so that another thread or transaction does not read the old value.
    5. Durability
        1. After transaction completes successfully, the changes it has made to the database persist, even if there are system failures.
        2. Problem case: the user is told the transaction completed, but due to a system failure at the end the change never got persisted in the DB, so the user's Rs 50 never arrived. This must never happen.
        3. In real DBs the work happens on a copy in main memory (A = 950, B = 2050). Writing it to the actual DB file on disk must succeed. If the system crashes during that write after the user was told it completed, the DB must be able to recover and re-execute the write, so A = 950 and B = 2050 end up in the DB.
        4. Main memory is wiped on a crash, so some mechanism is needed: generate logs of every operation (e.g. 50 subtracted, write to A, read B) and keep them on disk; or write to disk intermediately.
        5. On restart the system reads the logs, finds what happened and redoes the changes in the actual DB. Checkpoints can also be used (covered later).
        6. Ensuring durability is the responsibility of the recovery management component of the DB.
3. Transaction states
    1. Life cycle of a transaction.

    ```mermaid
    flowchart LR
        A[Active state] -- R/W operations --> P[Partially committed state]
        P -- Permanent store --> C[Committed state]
        A -- Failure --> F[Failed state]
        P -- Failure --> F
        F -- Roll back --> AB[Aborted state]
        C --> T[Terminated state]
        AB --> T
    ```

    2. Active state
        1. The very first state of the life cycle of the transaction, all the read and write operations are being performed. If they execute without any error the T comes to Partially committed state. Although if any error occurs then it leads to a Failed state.
        2. E.g. Read(A) and Read(B) succeed, then the T goes to partially committed. If any problem occurs even while reading from the DB, it goes straight to failed.
    3. Partially committed state
        1. After transaction is executed the changes are saved in the buffer in the main memory. If the changes made are permanent on the DB then the state will transfer to the committed state and if there is any failure, the T will go to Failed state.
        2. All the work happens in main memory because the CPU does the actual plus/minus work there; data is brought from the storage device (hard disk, SSD, a server or S3).
        3. When all 6 steps are done, COMMIT is called, making the changes permanent in the DB; the T moves to the committed state.
        4. An error at any step in this state (e.g. during Write(A)) sends the T straight to failed. Every state checks completion so that atomicity is kept and no inconsistency is introduced.
    4. Committed state
        1. When updates are made permanent on the DB. Then the T is said to be in the committed state. Rollback can't be done from the committed states. New consistent state is achieved at this stage.
        2. DB state before Active is State 1 (A = 1000, B = 2000). After commit the DB is in State 2 (A = 950, B = 2050): permanent changes, new values. The transaction was successful.
    5. Failed state
        1. When T is being executed and some failure occurs. Due to this it is impossible to continue the execution of the T.
        2. The failure can be hardware, software, a communication issue, or an interrupt by the user; any kind.
    6. Aborted state
        1. When T reaches the failed state, all the changes made in the buffer are reversed. After that the T rollback completely. T reaches abort state after rollback. DB's state prior to the T is achieved.
        2. After rollback all changes are undone, and the DB returns to State 1; it never reached State 2.
    7. Terminated state
        1. A transaction is said to have terminated if has either committed or aborted.
        2. In SQL terms: `BEGIN TRANSACTION` and `END TRANSACTION` are the two operators; the work in between is the partially committed work. If a problem comes in between, go to failed and roll back to a checkpoint or earlier state. On leaving the block the T is terminated, either through abort or through commit.
4. How to implement atomicity is discussed in the next lecture (Lecture 13).
