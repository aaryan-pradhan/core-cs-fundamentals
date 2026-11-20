# Lecture 21: Deadlock Part-1

- Synchronization (e.g. locks on a critical section) makes threads access a critical section in a mutually exclusive way: if T1 locks it, T2 cannot enter and has to wait.
- This mutual exclusion gives rise to a problem (a bug) in the system called **deadlock**.
- The terms process and thread are used interchangeably here: everything said for processes holds for threads too (a thread is just a part of a process).

1. In Multi-programming environment, we have several processes competing for finite number of resources
   - The system has finite resources R1, R2, R3, ... and many processes P1, P2, P3, ... (or threads, in a multithreaded environment) that need them to execute.
   - Goal: use these finite resources so the whole system keeps running. A process that wants a resource may wait a while, but eventually gets it; there should be no blockage.
   - Example of a blockage: system has only two resources R1, R2 and only two processes P1, P2. Each process needs **both** R1 and R2 to complete execution.
     - P1 locks R1 (R1 is busy with P1). P2 locks R2.
     - P1 cannot proceed until it gets R2; P2 cannot proceed until it gets R1.
     - Both go to waiting, and the waiting continues for infinite time. Neither process can advance its program counter, so no progress happens. The system hangs: it is in deadlock.
     - From the user's perspective some work should always be progressing (the PC should not hang); in deadlock nothing progresses, which is why it is so dangerous.
2. Process requests a **resource (R)**, if R is not available (taken by other process), process enters in a waiting state. Sometimes that waiting process is never able to change its state because the resource, it has requested is busy (forever), called **DEADLOCK (DL)**
   - In the example: R1 is allocated to P1, but P1 waits for R2. R2 is with P2, and P2 waits for R1. A circular dependency forms, so the waiting goes on forever.
3. Two or more processes are waiting on some resource's availability, which will never be available as it is also busy with some other process. The Processes are said to be in **Deadlock.**
4. DL is a bug present in the process/thread synchronization method.
   - Both processes and threads request resources, so deadlock applies to both.
5. In DL, processes never finish executing, and the system resources are tied up, preventing other jobs from starting.
6. **Example of resources**: Memory space, CPU cycles, files, locks, sockets, IO devices etc.
7. Single resource can have multiple instances of that. E.g., CPU is a resource, and a system can have 2 CPUs.
   - "CPU" is the abstract name; a quad-core CPU has 4 cores, i.e., 4 instances of the CPU resource.
   - Similarly, two monitors (extended display) = 2 instances of monitor; two hard disks = 2 instances of disk.
8. How a process/thread utilize a resource?
   1. Request: Request the R, if R is free Lock it, else wait till it is available.
      - Availability is checked through the resource's lock: if the lock is free, the process locks the resource. Once the lock succeeds, R is allocated to the process (drawn as an edge R → P).
      - Locking means no other process can use R.
   2. Use
   3. Release: Release resource instance and make it available for other processes
      - The process releases R when it decides it is done (when its code says so), by unlocking/releasing the lock. After that, some other process can use R.

   ```mermaid
   flowchart LR
       R1[R1] -- allocated --> T1((T1))
       T1 -- Req. --> R2[R2]
       R2 -- allocated --> T2((T2))
       T2 -- Req. --> R1
   ```

9. **Deadlock Necessary Condition**: **4** Condition should hold simultaneously.
   - All four must be true together; only then is there a deadlock, otherwise not.
   - Interview question asked directly: "What are the necessary conditions for deadlock to occur in a system?"
   1. **Mutual Exclusion**
      1. Only 1 process at a time can use the resource, if another process requests that resource, the requesting process must wait until the resource has been released.
         - E.g. R is allocated to P1. If P2 requests R, the request cannot be fulfilled until P1 releases R (after use).
   2. **Hold & Wait**
      1. A process must be holding at least one resource & waiting to acquire additional resources that are currently being held by other processes.
         - Hold: the process already got a resource and has a lock on it (P1 is holding R1).
         - Wait: it is waiting for another resource that is allocated elsewhere (P1 is waiting for R2, because R2 is already allocated to P2).
   3. **No-preemption**
      1. Resource must be voluntarily released by the process after completion of execution. (No resource preemption)
         - Once R is allocated to P1, it cannot be deallocated from P1 until P1's code itself releases it.
         - Another process (P2) cannot forcefully get R allocated to itself, and the OS cannot forcefully take R back.
   4. **Circular wait**
      1. A set {P0, P1, … ,Pn} of waiting processes must exist such that P0 is waiting for a resource held by P1, P1 is waiting for a resource held by P2, and so on.
         - It is an extended version of hold & wait, where the waiting happens in a circular fashion.
         - E.g. R1 allocated to P1, P1 waits for R2; R2 allocated to P2, P2 waits for R1. Removing the resource nodes: P1 waits for something P2 holds, and P2 waits for something P1 holds, i.e., P1 → P2 → P1.
   - Checking all four on the T1/T2 diagram above:
     - Mutual exclusion: the resource allocation code is written so that once a thread locks a resource, no other thread can use it.
     - Hold & wait: T1 holds R1 and waits for R2; T2 holds R2 and waits for R1.
     - No preemption: nothing makes T1 give up R1 before its work is done (e.g. R1 is a memory space; T1 keeps it until T1 itself releases it).
     - Circular wait: R1 → T1 → R2 → T2 → R1 forms a circular dependency.
     - All four hold, so the system is in deadlock.

## Resource Allocation Graph (RAG)

- The graph-type drawings used so far (boxes for resources, circles for processes) are the Resource Allocation Graph.
- Vertices are of two types:
  1. Process vertex: drawn as a circle (P).
  2. Resource vertex: drawn as a box (R).
- Edges are of two types:
  1. Assign edge: R → P, i.e., R is allocated to P.
  2. Request edge: P → R, i.e., P is requesting R.
- Multiple instances of a resource are shown as dots inside the resource box (e.g. a quad-core CPU R drawn with 4 dots). A box with no dots means a single instance.
- Use: a pictorial representation of the system's state, from which we can see whether there is a cycle (circular-wait-like condition) and hence whether there may be a deadlock.
- Rule (inspired by the circular wait condition):
  - No cycle in RAG → no deadlock (definitely).
  - Cycle in RAG → maybe deadlock. It must be double-checked against the necessary conditions.
- Example 1 (cycle and deadlock): R1 and R3 have a single instance; R2 has 2 instances.

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

  - Cycle exists, so maybe deadlock. Validate with the cycle P2 → R3 → P3 → R2 → P2:
    - P2 requests R3, but R3 is already allocated to P3.
    - P3 requests an instance of R2, but one instance is busy with P1 and the other is assigned to P2.
    - Mutual exclusion holds. Hold & wait holds: P2 holds R2 and waits for R3; P3 holds R3 and waits for R2. No preemption holds (a process releases a resource only voluntarily; the OS cannot forcibly preempt it). Circular wait holds.
    - So deadlock is actually present.
- Example 2 (cycle but no deadlock): R1 and R2 have 2 instances each.

  ```mermaid
  flowchart LR
      P1((P1)) --> R1["R1 (2 instances)"]
      R1 --> P2((P2))
      R1 --> P3((P3))
      P3 --> R2["R2 (2 instances)"]
      R2 --> P1
      R2 --> P4((P4))
  ```

  - Cycle P1 → R1 → P3 → R2 → P1 exists; a normal graph cycle-detection algorithm would return true.
  - But there is no deadlock, because of multiple instances. At t = 0:
    - P4 holds an instance of R2 and is not waiting, so after some time it finishes and releases R2 (P4 leaves the system).
    - R2 then gets assigned to P3. P3 now has both R1 and R2, so it executes successfully and frees its resources.
    - Similarly, when P2 completes, its instance of R1 becomes free and P1 gets R1.
  - Cycle was present, but deadlock was not. Hence "cycle → maybe deadlock".
- RAG examples are not usually asked directly in interviews, but the definition and the conditions (no cycle → no DL, cycle → maybe DL) and why RAG is used can be asked.

10. **Methods for handling Deadlocks:**
    1. Use a protocol to **prevent** or **avoid** deadlocks, ensuring that the system will never enter a deadlocked state.
    2. Allow the system to enter a deadlocked state, **detect it, and recover.**
       - A separate algorithm runs in parallel and detects whether the system is in deadlock; if it is, the system is recovered.
    3. Ignore the problem altogether and pretend that deadlocks never occur in system. (Ostrich algorithm) aka, **Deadlock ignorance.**
       - The system assumes deadlock can never happen and does not implement any handling.
       - The whole responsibility is left to the application programmer (the one writing the apps/processes): they must write the code to detect and handle deadlock themselves.
       - Name: when danger comes, an ostrich hides its head in the soil and thinks the problem has gone away. Similarly, this method ignores the problem and pretends it does not exist.
       - Not discussed further; only prevention/avoidance and detection/recovery are covered.
11. To ensure that deadlocks never occur, the system can use either a **deadlock prevention or deadlock avoidance scheme**.
12. **Deadlock Prevention**: by ensuring at least one of the necessary conditions cannot hold.
    - Deadlock needs all 4 conditions simultaneously. If the system implements logic so that any one condition never holds, the system never enters deadlock, i.e., deadlock is prevented.
    1. **Mutual exclusion**
       1. Use locks (mutual exclusion) only for non-sharable resource.
          - Keep mutual exclusion to as few places as possible; do not make every resource non-sharable needlessly.
          - Non-sharable resources: critical sections, a memory space that only one process should use at a time, a printer (handles one process at a time). These are locked/made critical.
       2. Sharable resources like Read-Only files can be accessed by multiple processes/threads.
          - Nobody writes to a read-only file, so no inconsistency can occur. So it need not be a critical section and no lock is used: many processes can request it and it gets assigned to all of them.
       3. However, we can't prevent DLs by denying the mutual-exclusion condition, because some resources are intrinsically non-sharable.
          - Some resources/memory areas will always be critical sections, so mutual exclusion cannot be removed entirely; it can only be reduced (no locks on sharable resources).
    2. **Hold & Wait**
       1. To ensure H&W condition never occurs in the system, we must guarantee that, whenever a process requests a resource, it doesn't hold any other resource.
       2. Protocol (A) can be, each process has to request and be allocated all its resources before its execution.
          - Every resource needed over the process's whole life cycle is allocated at the start, before execution.
          - Example: process P copies data from a DVD drive to a file, sorts the file (CPU work), then sends it to the printer.
            - With protocol A, P gets the DVD drive, the file and the printer allocated at the start, then does copy → sort → print.
            - Drawback: while copying DVD → file (say it takes 1 hour), P is holding the printer too. Another process could have used the printer for useful work in that time (poor resource utilization).
       3. Protocol (B) can be, allow a process to request resources only when it has none. It can request any additional resources after it must have released all the resources that it is currently allocated.
          - Same example with protocol B:
            1. At the start, P requests only the DVD drive and the file (both needed to copy).
            2. It copies, then sorts.
            3. Before requesting the printer, it releases the DVD drive and the file.
            4. Then it requests the file and the printer together, gets both, and gives the print command.
          - P still needs two resources at each point (DVD + file to copy, file + printer to print), but it never holds the printer when it does not need it, and it holds nothing when it makes a new request.
    3. **No preemption**
       1. If a process is holding some resources and request another resource that cannot be immediately allocated to it, then all the resources the process is currently holding are preempted. The process will restart only when it can regain its old resources, as well as the new one that it is requesting. (Live Lock may occur).
          - Example: P1 holds R1 and requests R2, but R2 is busy (allocated elsewhere).
            - P1 gets an interrupt/trigger: since R2 is not available, release everything currently held. P1 releases R1.
            - P1 waits until R2 is free. When R1 and R2 are both available, it requests both together and wants both allocated at once; once allocated, it proceeds.
          - Live lock: when a process tries to acquire both locks (R1, R2) at the same time, the lock attempts can collide (on the kernel side). After a collision, it retries after some delay; if the retries collide again, it retries again, and so on.
            - The code keeps revolving on the same line (where both locks are taken together), wasting CPU cycles without progress.
            - Fix: put a small delay, e.g. a sleep of a few nanoseconds or 1 ms between acquiring lock 1 and lock 2. This overcomes the live lock condition.
       2. If a process requests some resources, we first check whether they are available. If yes, we allocate them. If not, we check whether they are allocated to some other process that is waiting for additional resources. If so, preempt the desired resource from waiting process and allocate them to the requesting process.
          - Example: R1 is allocated to P1, and P1 waits for R2. R2 is allocated to P2, and P2 waits for R3. Assume P1 has higher priority.
            - P2 is itself waiting (for R3), so its hold on R2 can be removed: preempt R2 from P2 and give it to P1.
            - P1 can now execute. When P1 completes and R2 is free again, P2 can request R2 again.
          - With such options, the no-preemption condition is broken, and so deadlock is prevented.
    4. **Circular wait**
       1. To ensure that this condition never holds is to impose a proper ordering of resource allocation.
          - Problem case: P1 and P2 both need R1 and R2. P1 requests R1 and gets it; meanwhile P2 has already acquired R2. Now P1 waits for R2 and P2 waits for R1: circular wait.
       2. P1 and P2 both require R1 and R2, locking on these resources should be like, both try to lock R1 then R2. By this way which ever process first locks R1 will get R2.
          - Fixed order: both first try to lock R1. Only after getting R1 does a process go for R2; otherwise it keeps waiting on R1.
          - E.g. P2 gets R1 first. P1 does not go and request R2; it keeps waiting on R1. P2 then requests R2, gets it too, and runs.
          - Circular wait can never form, because P1 never grabs R2 while P2 holds R1.

          ```mermaid
          flowchart LR
              R1[R1] -- allocated --> P2((P2))
              P1((P1)) -- waits --> R1
              P2 -- Req. --> R2[R2]
          ```

- Of the handling methods, this lecture covers prevention. Avoidance comes in the next lecture, then detection & recovery. Deadlock ignorance (ostrich algorithm) needs no further discussion.
