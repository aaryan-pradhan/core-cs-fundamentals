# Lecture 19: Reader writer problem

- Next classic synchronization problem after producer-consumer. Very famous; asked in interviews.
- Setup: a database (or a file / a page of paper) is a shared resource. Many reader threads want to read it, many writer threads want to write to it.
- Goal of the synchronization: only one writer writes at a time, but multiple readers can read at the same time.

## Reader writer problem

1. Reader thread → Read
   - Only reads the data.
2. writer threads → write / update
   - Updates the data in the shared database / file.

```
   ┌──────────┐
   │          │
   │ Database │   (shared resource = C.S.)
   │          │
   └──────────┘
```

1. if >1 Readers are reading → No issue ✗.
   - Readers do not change the data, so any number of them can read in parallel.
2. >1 writers OR 1 writer && some other thread (R/W), parallely,
   → Race condition & data inconsistent

```
   W1 ──→ ┌────────┐ ←── R1
          │  page  │
          └────────┘
   abzf  ←──  R  ──Read──→  abcd
```

- Two writers together: W1 is already writing at a position; W2 starts writing at the same position. W1 writes "abcd", W2 writes "efg" → characters get mixed, data becomes inconsistent.
- One writer + one reader together: writer has written "abcd"; reader R1 comes at that moment and reads "abcd" into its buffer and leaves. A little later the writer updates it to "abzf". The reader went away with "abcd", i.e. it read inconsistent (wrong) data, while the writer had corrected the data shortly after.
- So while a writer is working on the data (updating the database), no other thread, reader or writer, may interfere.
- The database (the page) is the critical section:
  - Writer threads must enter one at a time, in a mutually exclusive way.
  - Multiple reader threads may read together.
  - If a writer is already writing, no reader may enter either (it would read inconsistent data).

## Semaphore sol<sup>n</sup> to R-W problems

1. mutex → Binary semaphore
   - to ensure mutual exclusion, when read count (rc) is updated.
   - No. two threads modify R.C at same time.
   - Multiple readers are allowed, so we must keep a count of how many readers there are. rc itself becomes a critical section: `rc++` is not an atomic operation (it goes through a temp variable / register, as seen with `count++`), so two readers updating it together can cause a race condition and a wrong count.
   - Same mutex (binary semaphore) idea as in the previous lectures.
2. wrt → Binary semaphore.
   - common for both reader, writer.
   - Used to make access to the critical section (the database) synchronised and mutually exclusive between reader and writer threads.
3. read count (rc) → integer {0},
   tracks how many readers are reading in C.S.
   - rc is a plain integer, not a semaphore. Initialised to 0.

### Writer sol<sup>n</sup>

```c
do {
    wait(wrt);
    // do write operation
    signal(wrt);
} while (true);
```

- The write operation is the critical section; only one writer gets access at a time.
- `wait(wrt)` locks it, so no other thread (reader or writer) can enter; the write happens; `signal(wrt)` releases it so another thread can enter.

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

- Conditions for a reader: multiple readers may read together, and while reading, no writer may be in the critical section (equivalently: if a reader is reading, the writer must not be let in).
- `rc++` is done inside `wait(mutex)` / `signal(mutex)` so that several readers arriving together do not corrupt the count.
- `if (rc == 1)`: only the first reader calls `wait(wrt)`.
  - If a writer is already in the C.S., this first reader blocks right here (and the readers after it block on `mutex`).
  - If no writer is inside, the first reader takes `wrt`, so any writer that arrives now is blocked and cannot enter the C.S.
  - Later readers (rc > 1) skip `wait(wrt)` and go straight in, so many readers read together.
- `signal(mutex)` after the check releases the lock on rc; then the reader reads in the C.S. (along with any other readers).
- On leaving: `wait(mutex)` again, because several readers (say 4) may leave at the same time and `rc--` must also be mutually exclusive.
- `if (rc == 0)`: the last reader to leave (zero readers in the C.S.) calls `signal(wrt)`. A writer may have been waiting all the time the readers were reading; this signal lets it enter.
- Then `signal(mutex)` and the reader leaves. Both reader and writer run in a loop.
- Writer solution is very easy; reader solution is also easy but a little tricky to understand.

## Sol<sup>n</sup> → implement ✓

- Homework: after reading all the classic problems, implement all the solutions given (reader-writer, bounded buffer). Implementing them gives confidence that you have understood the problems.
- These are asked in interviews.
