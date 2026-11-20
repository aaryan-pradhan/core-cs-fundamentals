# Lecture 20: The Dining Philosophers problem

- Third and last classic synchronization problem (after producer-consumer and reader-writer).

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

1. We have **5 philosophers.**
2. They spend their life just being in **two states:**
   1. Thinking
   2. Eating
3. They sit on a circular table surrounded by 5 chairs (1 each), in the center of table is a bowl of noodles, and the table is laid with 5 single forks.
   - So: 5 philosophers (ph.), 1 bowl of noodles in the middle, only 5 forks.
4. **Thinking state**: When a ph. Thinks, he doesn't interact with others.
   - Philosophers never talk to each other; there is no interaction between them at all. They only think or eat.
5. **Eating state:** When a ph. Gets hungry, he tries to pick up the 2 forks adjacent to him (Left and Right). He can pick one fork at a time.
   - To eat, a ph. needs exactly 2 forks (at least and at most 2): the one on his left and the one on his right.
   - He picks them one by one: first one fork, then the other.
   - If all 5 want to eat at once, ideally 5 × 2 = 10 forks are needed, but only 5 exist. The problem: synchronise them so that whoever wants to eat gets 2 forks and eats, and the system is deadlock free.
   - OS mapping: philosophers = processes (threads), forks = resources. A classic problem about sharing limited resources among processes.
6. One can't pick up a fork if it is already taken.
   - If one ph. has picked up (locked) a fork, his neighbour cannot pick that same fork.
7. When ph. Has both forks at the same time, he eats without releasing forks.
8. Solution can be given using semaphores.
   1. Each fork is a binary semaphore.
   2. A ph. Calls wait() operation to acquire a fork.
      - If philosopher i calls `wait(fork[i])`, he has acquired fork i.
   3. Release fork by calling signal().
      - After `signal(fork[i])`, the fork is released and someone else can pick it up.
   4. **Semaphore fork[5]{1};**
      - An array of 5 semaphores (one per fork), each initialised to 1 (free).

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

   - Second fork is `(i + 1) % 5`: the table is circular. E.g. i = 1 → second fork is 2. For the last philosopher, i + 1 = 6, but there is no 6th fork, so the mod wraps it back to the first fork.
   - wait() is called on the two forks one by one (not in parallel). After acquiring both, he eats; after eating, he signals (releases) both and goes back to thinking.
9. Although the semaphore solution makes sure that no two neighbors are eating simultaneously but it could still create **Deadlock**.
   - Why neighbours can't eat together: if P1 has locked both his forks, P2 can lock his other fork but not the fork shared with P1, so P2 cannot eat until P1 releases it.
10. Suppose that all 5 ph. Become hungry at the same time and each picks up their left fork, then All fork semaphores would be 0.
11. When each ph. Tries to grab his right fork, he will be waiting for ever (Deadlock)
    - P1 holds his left fork and waits for his right one, which P2 holds; P2 holds his and waits for P3's, and so on around the table; the last one waits for the fork P1 holds. No one ever releases, so the system never comes out of this state (circular wait).
12. We must use **some methods to avoid Deadlock and make the solution work**
    - There is no hard and fast rule to remove deadlock here; we add small tweaks (rules) so that the deadlock situation never occurs in the first place (avoid it before it happens).
    1. Allow at most 4 ph. To be sitting simultaneously.
       - E.g. remove philosopher 5 from the table. Now P1, P2, P3, P4 each pick their left fork; because P5 is absent, the fork on P1's other side is still free, so P1 picks it and eats (at least one ph. is in the eating state; the rest wait).
       - When P1 finishes eating, he releases both forks; P2 gets the fork he was waiting for, eats, releases both; then P3 gets his, and so on. No deadlock.
       - Downside: the 5th philosopher is not allowed to sit at all.
    2. Allow a ph. To pick up his fork only if both forks are available and to do this, he must pick them up in a critical section (atomically).
       - Instead of picking one fork, then the other, the fork-picking section of code (the two wait() calls) is made a critical section, guarded by one more lock (a mutex): lock the mutex before picking, release it after.
       - The releasing section (the two signal() calls) is also made a critical section, so both forks are released together.
       - Now both are atomic: only one thread can execute the critical section at a time, so a ph. that enters it comes out holding both forks.

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

       an odd ph. Picks up first his left fork and then his right fork, whereas an even ph. Picks up his right fork then his left fork.
       - Odd philosophers: 1, 3, 5. Even philosophers: 2, 4.
       - Example: odd ones (1, 3, 5) pick their left fork; even ones (2, 4) try their right fork first. Ph. 4 cannot get his first fork, so he waits at that point without having picked anything.
       - Because 4 picked nothing, the fork between 4 and 5 stays free, so 5 picks it, has both forks, eats and moves on. Similarly the rest proceed; no circular wait arises, so deadlock is avoided.
13. Hence, only semaphores are not enough to solve this problem.
    We must add some enhancement rules to make deadlock free solution.
    - Removing deadlock permanently is very hard (here, impossible with semaphores alone), so we add small rules on how resources are taken.
    - Same in real-world programs: limited resources, some threads that must share them; we set an order among threads (e.g. using condition variables) or rules like these to keep the system deadlock free.
    - This sets the basis for the next topic: deadlocks (end of the concurrency module).
