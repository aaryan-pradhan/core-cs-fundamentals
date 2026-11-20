# Lecture 19: Reader writer problem

> **Interview:** The reader-writer problem is very famous and is asked in interviews.

- **Setup:** A database (or a file, or a page of paper) is a shared resource. Many reader threads want to read it. Many writer threads want to write to it.
- **Goal:** Only one writer writes at a time, but multiple readers can read at the same time.

## Reader writer problem

1. **Reader thread:** It reads.
   - It only reads the data.
2. **Writer thread:** It writes or updates.
   - It updates the data in the shared database or file.

```
   ┌──────────┐
   │          │
   │ Database │   (shared resource = C.S.)
   │          │
   └──────────┘
```

| Case | Result |
|------|--------|
| More than 1 reader reading | No issue. Readers do not change the data, so any number can read in parallel. |
| More than 1 writer, or 1 writer plus some other thread (reader or writer), in parallel | Race condition and inconsistent data. |

```
   W1 ──→ ┌────────┐ ←── R1
          │  page  │
          └────────┘
   abzf  ←──  R  ──Read──→  abcd
```

- **Two writers together:** W1 is already writing at a position. W2 starts writing at the same position. W1 writes "abcd" and W2 writes "efg". The characters get mixed and the data becomes inconsistent.
- **One writer and one reader together:** The writer has written "abcd". Reader R1 comes at that moment, reads "abcd" into its buffer and leaves. A little later the writer updates it to "abzf". The reader went away with "abcd". It read inconsistent (wrong) data, because the writer corrected the data shortly after.
- **Rule:** While a writer is updating the database, no other thread, reader or writer, may interfere.
- **Critical section:** The database (the page) is the critical section.
  - Writer threads must enter one at a time, in a mutually exclusive way.
  - Multiple reader threads may read together.
  - If a writer is already writing, no reader may enter either, because it would read inconsistent data.

## Semaphore sol<sup>n</sup> to R-W problems

1. **mutex:** a binary semaphore.
   - It ensures mutual exclusion when the read count (rc) is updated.
   - No two threads may modify rc at the same time.
   - Multiple readers are allowed, so we keep a count of them.
   - rc is itself a critical section. `rc++` is not atomic (it goes through a temp variable or register, as with `count++`). Two readers updating it together can give a wrong count.
2. **wrt:** a binary semaphore.
   - It is common for both readers and writers.
   - It makes access to the critical section (the database) synchronised and mutually exclusive between reader and writer threads.
3. **read count (rc):** an integer, initially 0.
   - It tracks how many readers are in the C.S. It is a plain integer, not a semaphore.

### Writer sol<sup>n</sup>

```c
do {
    wait(wrt);
    // do write operation
    signal(wrt);
} while (true);
```

- **Critical section:** The write operation. Only one writer gets access at a time.
- **`wait(wrt)`:** It locks the section, so no other thread (reader or writer) can enter. Then the write happens.
- **`signal(wrt)`:** It releases the section so another thread can enter.

### Reader sol<sup>n</sup>

```c
do {
    wait(mutex);    // to mutex readcount variable
    rc++;
    if (rc == 1)
        wait(wrt);  // ensures no writer can enter if there is
                    // even one reader
    signal(mutex);

    // C.S: Reader is reading

    wait(mutex)
    rc--;           // a reader leaves
    if (rc == 0)    // no reader is left in CS
        signal(wrt); // writer can enter
    signal(mutex);  // reader leaves
} while (1)
```

- **Conditions for a reader:** Multiple readers may read together. While a reader is reading, no writer may be in the C.S.
- **`rc++`:** It is done inside `wait(mutex)` and `signal(mutex)`, so the count is not corrupted.
- **`if (rc == 1)`:** Only the first reader calls `wait(wrt)`.
  - If a writer is already in the C.S., this first reader blocks right here. The readers after it block on `mutex`.
  - If no writer is inside, the first reader takes `wrt`. Any writer that arrives now is blocked and cannot enter the C.S.
  - Later readers (rc > 1) skip `wait(wrt)` and go straight in, so many readers read together.
- **`signal(mutex)` after the check:** It releases the lock on rc. Then the reader reads in the C.S. (along with any other readers).
- **On leaving:** The reader calls `wait(mutex)` again. Several readers (say 4) may leave at the same time, and `rc--` must also be mutually exclusive.
- **`if (rc == 0)`:** The last reader to leave (zero readers in the C.S.) calls `signal(wrt)`. A writer may have been waiting all the time the readers were reading. This signal lets it enter.
- **Then:** `signal(mutex)` runs and the reader leaves. Both reader and writer run in a loop.
- **Difficulty:** The writer solution is very easy. The reader solution is also easy, but a little tricky to understand.

## Sol<sup>n</sup>: implement

- **Homework:** Implement all the solutions given (reader-writer, bounded buffer).

> **Interview:** These problems are asked in interviews.
