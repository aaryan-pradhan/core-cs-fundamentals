# Lecture 21: Deadlock Part-1

- **Synchronization:** Locks on a critical section make threads access it in a mutually exclusive way. If T1 locks it, T2 cannot enter and has to wait.
- **The problem:** This mutual exclusion gives rise to a bug in the system called **deadlock**.
- **Terms:** Process and thread are used interchangeably here, because a thread is just a part of a process.

1. In a multi-programming environment, several processes compete for a finite number of resources.
   - **Setup:** The system has finite resources R1, R2, R3, ... and many processes P1, P2, P3, ... (or threads, in a multithreaded environment) that need them to execute.
   - **Goal:** Keep the system running. A process may wait a while for a resource, but it eventually gets it. There should be no blockage.
   - **Example of a blockage:** The system has only two resources R1, R2 and only two processes P1, P2. Each process needs **both** R1 and R2 to complete execution.
     - P1 locks R1, so R1 is busy with P1. P2 locks R2.
     - P1 cannot proceed until it gets R2. P2 cannot proceed until it gets R1.
     - Both go to waiting, and the waiting continues for infinite time. Neither process can advance its program counter, so no progress happens. The system hangs. It is in deadlock.
     - Some work should always progress (the PC should not hang). In deadlock nothing does.
2. A process requests a **resource (R)**. If R is not available (taken by another process), the process enters a waiting state. Sometimes that waiting process can never change its state, because the resource it requested stays busy forever. This is called **DEADLOCK (DL)**.
   - **In the example:** R1 is with P1, which waits for R2. R2 is with P2, which waits for R1. The circular dependency makes the wait infinite.
3. Two or more processes wait on a resource that will never become available, because it is busy with some other process. These processes are said to be in **Deadlock.**
4. DL is a bug in the process/thread synchronization method.
5. In DL, processes never finish executing. The system resources are tied up, which prevents other jobs from starting.
6. **Examples of resources:** Memory space, CPU cycles, files, locks, sockets, IO devices etc.
7. A single resource can have multiple instances. E.g., CPU is a resource, and a system can have 2 CPUs.
   - "CPU" is the abstract name. A quad-core CPU has 4 cores, i.e., 4 instances of the CPU resource.
   - Two monitors (extended display) are 2 instances of monitor. Two hard disks are 2 instances of disk.
8. How does a process/thread use a resource?
   1. **Request:** Request R. If R is free, lock it. Otherwise wait till it is available.
      - Availability is checked through the resource's lock. Once the lock succeeds, R is allocated to the process (drawn as an edge R → P). No other process can then use R.
   2. **Use**
   3. **Release:** Release the resource instance and make it available for other processes.
      - The process releases R when its code says so, by unlocking the lock. Then another process can use R.

   ```mermaid
   flowchart LR
       R1[R1] -- allocated --> T1((T1))
       T1 -- Req. --> R2[R2]
       R2 -- allocated --> T2((T2))
       T2 -- Req. --> R1
   ```

9. **Deadlock Necessary Conditions:** **4** conditions must hold simultaneously.
   - All four must be true together. Only then is there a deadlock.

   > **Interview:** "What are the necessary conditions for deadlock to occur in a system?" This is asked directly.

   1. **Mutual Exclusion**
      1. Only 1 process at a time can use the resource. If another process requests that resource, the requesting process must wait until the resource has been released.
         - E.g. R is allocated to P1. If P2 requests R, the request cannot be fulfilled until P1 releases R (after use).
   2. **Hold & Wait**
      1. A process must be holding at least one resource and waiting to acquire additional resources that are currently held by other processes.
         - **Hold:** The process already got a resource and has a lock on it (P1 is holding R1).
         - **Wait:** It waits for another resource that is allocated elsewhere (P1 is waiting for R2, because R2 is already allocated to P2).
   3. **No-preemption**
      1. A resource must be voluntarily released by the process after completion of execution. (No resource preemption)
         - Once R is allocated to P1, it cannot be deallocated from P1 until P1's code itself releases it.
         - Another process (P2) cannot forcefully get R allocated to itself, and the OS cannot forcefully take R back.
   4. **Circular wait**
      1. A set {P0, P1, … ,Pn} of waiting processes must exist such that P0 is waiting for a resource held by P1, P1 is waiting for a resource held by P2, and so on.
         - It is hold & wait in a circular fashion.
         - E.g. R1 is with P1, which waits for R2. R2 is with P2, which waits for R1. Without the resource nodes, P1 → P2 → P1.

   Checking all four on the T1/T2 diagram above:

   - **Mutual exclusion:** Once a thread locks a resource, no other thread can use it.
   - **Hold & wait:** T1 holds R1 and waits for R2. T2 holds R2 and waits for R1.
   - **No preemption:** Nothing makes T1 give up R1 before it is done (e.g. R1 is a memory space).
   - **Circular wait:** R1 → T1 → R2 → T2 → R1.

   All four hold, so the system is in deadlock.

## Resource Allocation Graph (RAG)

- **What it is:** The graph-type drawings used so far (boxes for resources, circles for processes) are the Resource Allocation Graph.
- **Vertices** are of two types:

  | Vertex | Drawn as |
  |--------|----------|
  | Process | Circle (P) |
  | Resource | Box (R) |

- **Edges** are of two types:

  | Edge | Direction | Meaning |
  |------|-----------|---------|
  | Assign edge | R → P | R is allocated to P. |
  | Request edge | P → R | P is requesting R. |

- **Multiple instances:** They are shown as dots inside the resource box (e.g. a quad-core CPU R drawn with 4 dots). A box with no dots means a single instance.
- **Use:** It is a pictorial representation of the system's state. From it we can see whether there is a cycle (a circular-wait-like condition) and hence whether there may be a deadlock.
- **Rule** (inspired by the circular wait condition):
  - No cycle in RAG means no deadlock (definitely).
  - Cycle in RAG means maybe deadlock. It must be double-checked against the necessary conditions.
- **Example 1 (cycle and deadlock):** R1 and R3 have a single instance. R2 has 2 instances.

  ```mermaid
  flowchart LR
      P1((P1)) --> R1[R1]
      R1 --> P2((P2))
      P2 --> R3[R3]
      R3 --> P3((P3))
      P3 --> R2["R2 (2 instances)"]
      R2 --> P1
      R2 --> P2
  ```

  - A cycle exists, so maybe deadlock. Validate with the cycle P2 → R3 → P3 → R2 → P2:
    - P2 requests R3, but R3 is already allocated to P3.
    - P3 requests an instance of R2, but one instance is busy with P1 and the other is assigned to P2.
    - **Mutual exclusion:** holds.
    - **Hold & wait:** holds. P2 holds R2 and waits for R3. P3 holds R3 and waits for R2.
    - **No preemption:** holds. A process releases a resource only voluntarily. The OS cannot forcibly preempt it.
    - **Circular wait:** holds.
    - So deadlock is actually present.
- **Example 2 (cycle but no deadlock):** R1 and R2 have 2 instances each.

  ```mermaid
  flowchart LR
      P1((P1)) --> R1["R1 (2 instances)"]
      R1 --> P2((P2))
      R1 --> P3((P3))
      P3 --> R2["R2 (2 instances)"]
      R2 --> P1
      R2 --> P4((P4))
  ```

  - The cycle P1 → R1 → P3 → R2 → P1 exists. A normal graph cycle-detection algorithm would return true.
  - But there is no deadlock, because of multiple instances. At t = 0:
    - P4 holds an instance of R2 and is not waiting. It finishes and releases R2 (P4 leaves).
    - R2 goes to P3. P3 has R1 and R2, so it executes and frees its resources.
    - When P2 completes, its instance of R1 is freed and P1 gets R1.
  - A cycle was present, but deadlock was not. Hence "cycle means maybe deadlock".

> **Interview:** RAG examples are not usually asked directly. The definition, the rules (no cycle means no DL, cycle means maybe DL) and why RAG is used can be asked.

10. **Methods for handling Deadlocks:**
    1. Use a protocol to **prevent** or **avoid** deadlocks, so the system never enters a deadlocked state.
    2. Allow the system to enter a deadlocked state, **detect it, and recover.**
       - A separate algorithm runs in parallel and detects whether the system is in deadlock. If it is, the system is recovered.
    3. Ignore the problem altogether and pretend that deadlocks never occur in the system. This is the Ostrich algorithm, also called **Deadlock ignorance.**
       - The system assumes deadlock can never happen and does not implement any handling.
       - The whole responsibility is left to the application programmer (the one writing the apps/processes). They must write the code to detect and handle deadlock themselves.
       - **Name:** When danger comes, an ostrich hides its head in the soil and thinks the problem has gone away. This method likewise ignores the problem and pretends it does not exist.
       - It is not discussed further. Only prevention/avoidance and detection/recovery are covered.
11. To ensure that deadlocks never occur, the system can use either a **deadlock prevention or deadlock avoidance scheme**.
12. **Deadlock Prevention:** ensure that at least one of the necessary conditions cannot hold.
    - Deadlock needs all 4 conditions simultaneously. If the system implements logic so that any one condition never holds, the system never enters deadlock. Deadlock is prevented.

    1. **Mutual exclusion**
       1. Use locks (mutual exclusion) only for non-sharable resources.
          - Keep mutual exclusion to as few places as possible. Do not make every resource non-sharable needlessly.
          - **Non-sharable resources:** critical sections, a memory space that only one process should use at a time, a printer (handles one process at a time). These are locked or made critical.
       2. Sharable resources like read-only files can be accessed by multiple processes/threads.
          - Nobody writes to a read-only file, so no inconsistency can occur. It need not be a critical section and no lock is used. Many processes can request it and it gets assigned to all of them.
       3. However, we cannot prevent DLs by denying the mutual-exclusion condition, because some resources are intrinsically non-sharable.
          - Some resources and memory areas will always be critical sections. So mutual exclusion cannot be removed entirely. It can only be reduced (no locks on sharable resources).
    2. **Hold & Wait**
       1. To ensure the H&W condition never occurs, we must guarantee that whenever a process requests a resource, it does not hold any other resource.
       2. **Protocol (A):** Each process requests and is allocated all its resources before its execution.
          - Every resource needed over the process's whole life cycle is allocated at the start, before execution.
          - **Example:** Process P copies from a DVD drive to a file, sorts the file (CPU work), then sends it to the printer. With protocol A, P gets the DVD drive, the file and the printer at the start.
            - **Drawback:** While copying DVD to file (say 1 hour), P holds the printer too. Another process could have used it. This is poor resource utilization.
       3. **Protocol (B):** A process may request resources only when it has none. It can request additional resources only after it has released all the resources it currently holds.
          - Same example with protocol B:
            1. At the start, P requests only the DVD drive and the file (both needed to copy).
            2. It copies, then sorts.
            3. Before requesting the printer, it releases the DVD drive and the file.
            4. Then it requests the file and the printer together, gets both, and gives the print command.
          - P needs two resources at each point (DVD and file to copy, file and printer to print). It never holds the printer needlessly, and holds nothing when it makes a new request.
    3. **No preemption**
       1. If a process holds some resources and requests another resource that cannot be immediately allocated to it, then all the resources it currently holds are preempted. The process restarts only when it can regain its old resources as well as the new one it is requesting. (Live Lock may occur.)
          - **Example:** P1 holds R1 and requests R2, but R2 is busy (allocated elsewhere).
            - P1 gets a trigger: R2 is unavailable, so release everything held. P1 releases R1.
            - When R1 and R2 are both available, it requests both together. Once allocated, it proceeds.
          - **Live lock:** When a process acquires both locks (R1, R2) at the same time, the attempts can collide (kernel side). It retries after a delay. If the retries collide again, it retries again, and so on.
            - The code keeps revolving on the same line, wasting CPU cycles without progress.
            - **Fix:** Put a small delay, e.g. a sleep of a few nanoseconds or 1 ms, between acquiring lock 1 and lock 2. This overcomes the live lock condition.
       2. If a process requests some resources, we first check whether they are available. If yes, we allocate them. If not, we check whether they are allocated to some other process that is waiting for additional resources. If so, we preempt the desired resource from the waiting process and allocate it to the requesting process.
          - **Example:** R1 is with P1, which waits for R2. R2 is with P2, which waits for R3. Assume P1 has higher priority.
            - P2 is itself waiting, so preempt R2 from P2 and give it to P1.
            - When P1 completes and R2 is free, P2 can request R2 again.
          - With such options, the no-preemption condition is broken, so deadlock is prevented.
    4. **Circular wait**
       1. To ensure this condition never holds, impose a proper ordering of resource allocation.
          - **Problem case:** P1 and P2 both need R1 and R2. P1 gets R1, P2 has already acquired R2. Now each waits for the other. This is circular wait.
       2. P1 and P2 both require R1 and R2. Locking should be ordered so that both try to lock R1 first, then R2. This way, whichever process locks R1 first will get R2.
          - **Fixed order:** Both first try to lock R1. Only after getting R1 does a process go for R2.
          - **Example:** P2 gets R1 first. P1 keeps waiting on R1. P2 then gets R2 and runs.
          - Circular wait cannot form, because P1 never grabs R2 while P2 holds R1.

          ```mermaid
          flowchart LR
              R1[R1] -- allocated --> P2((P2))
              P1((P1)) -- waits --> R1
              P2 -- Req. --> R2[R2]
          ```

- **Coverage:** Of the handling methods, prevention is covered here. Avoidance comes in the next lecture, then detection and recovery. Deadlock ignorance (ostrich algorithm) needs no further discussion.
