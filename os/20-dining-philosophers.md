# Lecture 20: The Dining Philosophers problem

This is the third and last classic synchronization problem (after producer-consumer and reader-writer).

```
                 Philosopher 1
          ┌──────────────────────────┐
          │        ψ        ψ        │
Philosopher 5    ψ   [noodles]   ψ    Philosopher 2
          │            ψ             │
          └──────────────────────────┘
       Philosopher 4          Philosopher 3

   circular table, bowl of noodles in the center, 5 forks (ψ),
   one fork between each pair of neighbouring philosophers
```

1. There are **5 philosophers.**
2. They spend their life in just **two states:**
   1. Thinking
   2. Eating
3. They sit at a circular table with 5 chairs (1 each). In the center of the table is a bowl of noodles. The table is laid with 5 single forks.
   - So there are 5 philosophers (ph.), 1 bowl of noodles in the middle, and only 5 forks.
4. **Thinking state:** When a ph. thinks, he does not interact with others.
5. **Eating state:** When a ph. gets hungry, he tries to pick up the 2 forks adjacent to him (left and right). He can pick one fork at a time.
   - **Forks needed:** A ph. needs exactly 2 forks (at least and at most 2): the one on his left and the one on his right.
   - He picks them one by one.
   - **The problem:** If all 5 want to eat at once, ideally 5 × 2 = 10 forks are needed, but only 5 exist. We must synchronise them so that whoever wants to eat gets 2 forks and eats, and the system is deadlock free.
   - **OS mapping:** Philosophers are processes (threads). Forks are resources. It is a classic problem about sharing limited resources among processes.
6. One cannot pick up a fork that is already taken.
   - If one ph. has picked up (locked) a fork, his neighbour cannot pick that same fork.
7. When a ph. has both forks at the same time, he eats without releasing the forks.
8. The solution can be given using semaphores.
   1. Each fork is a binary semaphore.
   2. A ph. calls the wait() operation to acquire a fork.
      - If philosopher i calls `wait(fork[i])`, he has acquired fork i.
   3. A ph. releases a fork by calling signal().
      - After `signal(fork[i])`, the fork is released and someone else can pick it up.
   4. **Semaphore fork[5]{1};**
      - It is an array of 5 semaphores (one per fork), each initialised to 1 (free).

   Philosopher i:

   ```c
   do {
       wait(fork[i]);              // pick first fork
       wait(fork[(i + 1) % 5]);    // pick second (adjacent) fork

       // eat

       signal(fork[i]);            // release both forks
       signal(fork[(i + 1) % 5]);

       // think
   } while (1);
   ```

   - **Second fork:** It is `(i + 1) % 5`, because the table is circular. E.g. i = 1 gives second fork 2. For the last philosopher, i + 1 = 6, but there is no 6th fork, so the mod wraps it back to the first fork.
   - **Order of calls:** wait() is called on the two forks one by one, not in parallel. After acquiring both, he eats. After eating, he signals (releases) both and goes back to thinking.
9. The semaphore solution makes sure that no two neighbors eat simultaneously. But it could still create **Deadlock**.
   - **Why neighbours cannot eat together:** If P1 has locked both his forks, P2 cannot get the fork shared with P1.
10. Suppose all 5 ph. become hungry at the same time and each picks up his left fork. Then all fork semaphores are 0.
11. When each ph. tries to grab his right fork, he waits forever (Deadlock).
    - P1 holds his left fork and waits for his right one, which P2 holds. P2 waits for P3's, and so on around the table. The last waits for the fork P1 holds.
    - No one ever releases. This is circular wait.
12. We must use **some methods to avoid Deadlock and make the solution work.**
    - There is no hard and fast rule to remove deadlock here. We add small tweaks (rules) so that the deadlock never occurs in the first place (avoid it before it happens).

    1. Allow at most 4 ph. to sit simultaneously.
       - **Example:** Remove philosopher 5 from the table. P1, P2, P3, P4 each pick their left fork. P5 is absent, so the fork on P1's other side is still free. P1 picks it and eats (at least one ph. is in the eating state, the rest wait).
       - **Then:** P1 eats and releases both forks. P2 gets his fork, eats, releases. Then P3, and so on. No deadlock.
       - **Downside:** The 5th philosopher is not allowed to sit at all.

    2. Allow a ph. to pick up his forks only if both are available. To do this, he must pick them up in a critical section (atomically).
       - **Pick section:** The two wait() calls form a critical section guarded by one more lock (a mutex). Lock before picking, unlock after.
       - **Release section:** The two signal() calls are also a critical section, so both forks are released together.
       - **Result:** Both are atomic, so a ph. that enters comes out holding both forks.

       ```c
       do {
           lock(mutex);
           wait(fork[i]);
           wait(fork[(i + 1) % 5]);
           unlock(mutex);

           // eat

           lock(mutex);
           signal(fork[i]);
           signal(fork[(i + 1) % 5]);
           unlock(mutex);

           // think
       } while (1);
       ```

    3. **Odd-even rule.**
       - An odd ph. picks up his left fork first, then his right fork. An even ph. picks up his right fork first, then his left fork.
       - **Odd philosophers:** 1, 3, 5. **Even philosophers:** 2, 4.
       - **Example:** Odd ones (1, 3, 5) pick their left fork. Even ones (2, 4) try their right fork first. Ph. 4 cannot get his first fork, so he waits at that point without having picked anything.
       - **Then:** The fork between 4 and 5 stays free, so 5 picks it, eats and moves on. The rest proceed. No circular wait arises.
13. Hence, only semaphores are not enough to solve this problem. We must add enhancement rules to make the solution deadlock free.
    - Removing deadlock permanently is very hard (here, impossible with semaphores alone). So we add small rules on how resources are taken.
    - Real-world programs are the same: limited resources, threads that must share them. We set an order among threads (e.g. using condition variables) or rules like these.
    - This sets the basis for the next topic: deadlocks (end of the concurrency module).
