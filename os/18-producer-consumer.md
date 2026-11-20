# Lecture 18: Producer-consumer problem

- Classic problems of synchronization: so far we saw race conditions, the critical section problem, and the methods to synchronise threads (locks, Peterson's solution, condition variables, semaphores). Now we apply those methods to classic synchronization problems.
- Asked directly in interviews: "What is the producer-consumer problem? How do you solve it?" (and the reader-writer problem, next lecture).

## Producer-consumer problem (Bounded Buffer problem)

1. Producer thread
2. Consumer thread

```
Producer
   ↓
┌──────┬──────┬──────┬──────┬──────┐
│      │      │      │      │      │
└──────┴──────┴──────┴──────┴──────┘
              n slots                └──→ Consumer pick
```

- Producer produces data (e.g. bottles) and puts it into the buffer.
- Consumer picks (consumes) data from the buffer, only when data is available in some slot.
- Buffer has n slots; at the start all slots are empty.
- Producer puts data into the empty slots; consumer picks from the filled slots.
- The buffer is the critical section: while the producer is putting data, the consumer must not interfere (come to pick), and while the consumer is picking, the producer must not be putting.
- Why "bounded buffer": the buffer is finite (n slots), i.e. the buffer is bounded, and the producer and consumer accessing it must be synchronised.

## Problem???

- C.S. (Buffer) → Sync. b/w Producer & Consumer.
  - The buffer is a shared resource; unsynchronised access produces inconsistency (race condition). So access to it must be mutually exclusive.
- Producer must not insert data when the buffer is full.
  - If all n slots are full, trying to put (checking again and again) only wastes CPU cycles. The whole game is saving CPU cycles.
- Consumer must not pick/remove data when the buffer is empty.

## Sol<sup>n</sup>: Semaphores

Both types of semaphores are used: binary and counting.

1. m, mutex → Binary sema. used to acquire lock on buffer.
   - Internally a mutex is a binary semaphore.
   - Lock is taken before accessing the buffer (critical section).
2. empty → a counting sem. Initial value is n.
   - ↳ tracks empty slots.
   - Initial value n because at the start the buffer is empty, so all n slots are empty.
3. full → tracks filled slots.
   - initial = 0.
   - At t = 0 the buffer is completely empty, so 0 slots are filled.

Producer

```c
do {
    wait(empty);  // wait until empty > 0
                  // then, empty-- (value)
    wait(mutex);
    // C.S, add data to buffer
    signal(mutex);
    signal(full); // increment full (value)
} while (1)
```

Consumer

```c
do {
    wait(full);   // wait until full > 0,
                  // then full--;
    wait(mutex);
    // remove data from Buffer
    signal(mutex);
    signal(empty); // increment empty
} while (1)
```

### How the solution works

- Mutual exclusion on the C.S. (the "add data" / "remove data" parts):
  - mutex is a binary semaphore with value 1. `wait(mutex)` decrements it to 0 and the thread enters.
  - Any other thread that now calls `wait(mutex)` is blocked (put to wait), not busy waiting, until `signal(mutex)`.
- Case 1: buffer empty (start).
  - Consumer calls `wait(full)`. full is 0, so it cannot be decremented; the value goes negative and the consumer thread blocks.
  - Producer calls `wait(empty)`. empty = n > 0, so it decrements and moves on, takes mutex, and enters the C.S.
  - So at the start only the producer can enter; the consumer cannot.
  - Producer fills one slot, `signal(mutex)`, then `signal(full)`: full++ (value goes from -1 to 0), and signal calls wakeup on the blocked consumer.
  - Consumer unblocks and enters the C.S. So the consumer enters only once the producer has filled at least one slot.
- Case 2: buffer full.
  - Consumer can consume: `wait(full)` passes.
  - empty = 0, so the producer's `wait(empty)` blocks (wait until empty > 0). No slot is empty, so the producer is not given access to the C.S.
- Result:
  - Producer produces only when at least one slot is empty.
  - Consumer picks only when at least one slot has data.

### Extension

- Used in many places inside the OS, and in thread design.
- Extends to multiple producers and multiple consumers sharing the buffer.
