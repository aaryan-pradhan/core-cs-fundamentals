# Lecture 13: How to implement Atomicity and Durability in Transactions

1. **Recovery Mechanism Component** of DBMS supports **atomicity and durability.**
   1. Shadow-copy scheme and the other schemes below are implemented inside this component.
   2. Recap: atomicity = T is all-or-nothing, never left half done (money deducted but not credited is not allowed; on failure it rolls back).
   3. Recap: durability = once T is committed and the user is notified, the updates in the DB must persist.
2. **Shadow-copy scheme**
   1. Based on making copies of DB (aka, **shadow copies**).
      1. Simplest, naive method.
   2. Assumption only one Transaction (T) is active at a time.
      1. Transactions must run serially; concurrent transactions do not work with this scheme.
   3. A pointer called **db-pointer** is maintained on the **disk**; which at any instant points to current copy of DB.
      1. Example: db-pointer holds address 0x01, pointing to the old DB copy on disk.
   4. T, that wants to update DB first creates a complete copy of DB.
      1. The copy is made in RAM; it is written to disk later.
   5. All further updates are done on new DB copy leaving the original copy (shadow copy) untouched.
   6. If at any point the T **has to be aborted** the system deletes the new copy. And the old copy is not affected.
      1. The db-pointer was pointing to the old copy all along, so nothing needs to be undone.
   7. If T success, it is committed as,
      1. OS makes sure all the pages of the new copy of DB written on the disk.
         1. Pages sit in RAM; the OS writes them back to disk.
      2. DB system updates the db-pointer to point to the new copy of DB.
         1. Example: db-pointer changes from 0x01 to 0x02.
      3. New copy is now the current copy of DB.
      4. The old copy is deleted.
      5. The T is said to have been **COMMITTED** at the point where the updated db-pointer is written to disk.
         1. Writing the new copy to disk is not enough; the user is told "committed" only after db-pointer shows the new location.
   8. **Atomicity**
      1. If T fails at any time before db-pointer is updated, the old content of DB are not affected.
      2. T abort can be done by just deleting the new copy of DB.
         1. The new copy is deleted from RAM.
      3. Hence, either all updates are reflected or none.
   9. **Durability**
      1. Suppose, system fails are any time before the updated db-pointer is written to disk.
         1. New copy may already be saved on disk, but db-pointer still says 0x01.
      2. When the system restarts, it will read db-pointer & will thus, see the original content of DB and none of the effects of T will be visible.
      3. T is assumed to be successful only when db-pointer is updated.
      4. If **system fails after** db-pointer has been updated. Before that all the pages of the new copy were written to disk. Hence, when system restarts, it will read new DB copy.
         1. db-pointer already says 0x02, so the changes persist; the old copy is already deleted.
   10. The implementation is dependent on write to the db-pointer being atomic. Luckily, disk system provide atomic updates to entire block or at least a disk sector. So, we make sure db-pointer lies entirely in a single sector. By storing db-pointer at the beginning of a block.
       1. Question: what if the system fails in the middle of changing 0x01 to 0x02? It cannot: a single-sector write is either done or not done.
   11. **Inefficient**, as entire DB is copied for every Transaction.
       1. DB can be terabytes in size; copying it for every T is very costly.
3. **Log-based recovery methods**
   1. The log is a sequence of records. Log of each transaction is maintained in some **stable storage** so that if any failure occurs, then it can be recovered from there.
      1. No copy of DB is needed in this method.
      2. Log records are written as T executes: T started, each value changed, T committed.
   2. If any operation is performed on the database, then it will be recorded in the log.
   3. But the process of storing the logs should be done **before** the actual transaction is applied in the database.
      1. First record what is to be done, then do it in the DB. A log written after the operation would not tell what was happening if the system failed in between.
   4. **Stable storage** is a classification of computer data storage technology that guarantees atomicity for any given write operation and allows software to be written that is robust against some hardware and power failures.
      1. Logs are kept separate from the DB storage: if the DB storage fails, the logs would be lost with it.
      2. Stable storage is expensive and robust.
   5. Example for log records: A = 1000 and B = 2000 initially. T0 sends 50 from A to B: read(A), A = A - 50, write(A), read(B), B = B + 50, write(B).
      1. Log records: `<T0 start>`, `<T0, A, 950>`, `<T0, B, 2050>`, `<T0 commit>`.
         1. Each update record has the transaction id, the variable and its new value.
   6. Deferred DB Modifications
      1. Ensuring **atomicity** by recording all the DB modifications in the log but deferring the execution of all the write operations until the final action of the T has been executed.
         1. Until T commits only log records are written; the actual DB is not modified.
      2. Log information is used to execute deferred writes when T is completed.
         1. After `<T0 commit>` is written, A = 950 and B = 2050 are written to the DB using the log.
      3. If system crashed before the T completes, or if T is aborted, the information in the logs are ignored.
         1. No commit record in the log means T never committed; the DB was never touched, so atomicity holds.
      4. If T completes, the records associated to it in the log file are used in executing the deferred writes.
      5. If failure occur while this updating is taking place, we preform redo.
         1. Durability: T0 is committed and the user is told, then A = 950 is written and the system crashes before B = 2050 is written.
         2. On restart, read the log from stable storage; `<T0 commit>` is there, so T0 did commit.
         3. Re-execute the writes from the log (redo) and finish T0.
         4. Failure during commit/deferred writes is handled the same way: the commit record in the log proves T0 completed.
   7. Immediate DB Modifications
      1. DB modifications to be output to the DB while the T is still in active state.
         1. In deferred mode a write is only logged and applied after commit; here each write is logged first and written to the DB right after being logged, so the DB is updated again and again while T runs.
      2. DB modifications written by active T are called uncommitted modifications.
         1. Uncommitted because T may fail midway and then these changes must be rolled back, using the log.
      3. In the event of crash or T failure, system uses old value field of the log records to restore modified values.
         1. Log records here have an extra field: `<T0, A, 1000, 950>` = transaction id, item, old value, new value; so `<T0 start>`, `<T0, A, 1000, 950>`, `<T0, B, 2000, 2050>`, `<T0 commit>`.
         2. Old value is needed because the DB already holds 950; to roll back, the old value 1000 must be known.
         3. Example: T0 wrote A = 950 in the DB and then fails or the user aborts; read the log, find A's old value 1000 and write it back.
      4. Update takes place only after log records in a stable storage.
         1. Always log first. If the DB were updated first and the system failed before the log was written, recovery would be impossible.
      5. Failure handling
         1. System failure before T completes, or if T aborted, then old value field is used to undo the T.
            1. Example: crash before commit; write 1000 back to A and 2000 back to B using old values.
         2. If T completes and system crashes, then new value field is used to redo T having commit logs in the logs.
            1. Example: T0 completed and the user was told, but the DB crashed while applying the commit; on restart the log shows T0 committed, so redo by writing new values (950, 2050) again.
            2. Redo only if `<T0 commit>` is in the log; if that line is absent, assume T0 failed and undo it.
   8. Checkpoints (improved log-based method)
      1. Logs keep growing with thousands or lakhs of transactions; stable storage fills up and keeping all old information is costly.
      2. A checkpoint is made at a point where the DB is consistent: all transactions before it (C1, C2, ...) are in committed state.
      3. If a transaction fails after a checkpoint, recovery needs only the log after the last checkpoint.
4. Interview
   1. Answer with the shadow-copy method first, then log-based recovery (deferred and immediate), which is better than shadow copy; checkpoints improve it further.
   2. Cross-question: what if the system fails while changing db-pointer from 0x01 to 0x02? It cannot: the disk writes a block/sector atomically and db-pointer sits in a single sector.
