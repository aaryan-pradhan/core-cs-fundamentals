# Lecture 22: Deadlock Part-2

- Last lecture: what a deadlock is, its necessary conditions, and deadlock prevention. This lecture: deadlock avoidance, deadlock detection and recovery.

1. **Deadlock Avoidance**: Idea is, the kernel be given in advance info concerning which resources will use in its lifetime.
   By this, system can decide for each request whether the process should wait.
   To decide whether the current request can be satisfied or delayed, the system must consider the resources currently available, resources currently allocated to each process in the system and the future requests and releases of each process.
   - In avoidance, the current state of the system is known in advance:
     - number of processes;
     - number of resources and the number of instances of each resource;
     - resources currently allocated to each process;
     - maximum need of each process (max instances of each resource it needs to finish).
   - Using all this, the goal is to schedule processes and allocate resources so that the system always stays in a safe state.
   1. Schedule process and its resources allocation in such a way that the DL never occur.
   2. Safe state: A state is safe if the system can allocate resources to each process (up to its max.) in some order and still avoid DL.
      A system is in safe state only if there exists a safe sequence.
      - Safe state, simply: with the current allocations, max needs and processes, there is some order of scheduling the processes (giving each process the resources it needs) such that all processes finish execution without any deadlock.
      - Safe sequence: that order. E.g. with P1, P2, P3, P4, scheduling P1 → P3 → P4 → P2 may cause no deadlock, while P1 → P2 → P3 → P4 may cause one. The first order is a safe sequence.
   3. In an Unsafe state, the operating system cannot prevent processes from requesting resources in such a way that any deadlock occurs. It is not necessary that all unsafe states are deadlocks; an unsafe state may lead to a deadlock.
      - Unsafe state is the opposite of safe: a configuration from which further allocations may lead to deadlock (all four necessary conditions may get fulfilled).
   4. The main key of the deadlock avoidance method is whenever the request is made for resources then the request must only be approved only in the case if the resulting state is a safe state.
   5. In a case, if the system is unable to fulfill the request of all processes, then the state of the system is called unsafe.
   6. Scheduling algorithm using which DL can be avoided by finding safe state. (Banker Algorithm)
      - Safe state needs a safe sequence; the Banker's algorithm is the algorithm used to find that safe sequence.

2. **Banker Algorithm**
   1. When a process requests a set of resources, the system must determine whether allocating these resources will leave the system in a safe state. If yes, then the resources may be allocated to the process. If not, then the process must wait till other processes release enough resources.

   **Example** (5 processes, 3 resource types A, B, C; a resource can be anything: memory, CPU, files, locks):

   - Total instances: A = 10, B = 5, C = 7.
   - Allocated = instances already given to each process. Max need = max instances it needs to execute.

   | Process | Allocated (A B C) | Max need (A B C) | Remaining need = Max − Allocated (A B C) |
   |---------|-------------------|------------------|------------------------------------------|
   | P1      | 0 1 0             | 7 5 3            | 7 4 3                                    |
   | P2      | 2 0 0             | 3 2 2            | 1 2 2                                    |
   | P3      | 3 0 2             | 9 0 2            | 6 0 0                                    |
   | P4      | 2 1 1             | 2 2 2            | 0 1 1                                    |
   | P5      | 0 0 2             | 4 3 3            | 4 3 1                                    |
   | Total   | 7 2 5             |                  |                                          |

   - Available = Total − Total allocated = (10−7, 5−2, 7−5) = **3 3 2**.
   - Finding a safe sequence: repeatedly pick a process whose remaining need ≤ available; let it run to completion; it then frees all its allocated resources, which are added to available.

   | Step | Check                                  | Runs? | Available after (A B C) |
   |------|----------------------------------------|-------|-------------------------|
   | 0    | start                                  |       | 3 3 2                   |
   | 1    | P1 needs 7 4 3 > 3 3 2                 | no    | 3 3 2                   |
   | 2    | P2 needs 1 2 2 ≤ 3 3 2                 | yes   | 3 3 2 + 2 0 0 = 5 3 2   |
   | 3    | P3 needs 6 0 0 > 5 3 2                 | no    | 5 3 2                   |
   | 4    | P4 needs 0 1 1 ≤ 5 3 2                 | yes   | 5 3 2 + 2 1 1 = 7 4 3   |
   | 5    | P5 needs 4 3 1 ≤ 7 4 3                 | yes   | 7 4 3 + 0 0 2 = 7 4 5   |
   | 6    | P1 needs 7 4 3 ≤ 7 4 5                 | yes   | 7 4 5 + 0 1 0 = 7 5 5   |
   | 7    | P3 needs 6 0 0 ≤ 7 5 5                 | yes   | 7 5 5 + 3 0 2 = 10 5 7  |

   - Safe sequence: **P2 → P4 → P5 → P1 → P3**. After all processes run, available = total (10 5 7), so the state is safe and deadlock can be avoided.
   - Unsafe case: if at the end P3 had needed 8 instances of A instead of 6, only 7 would be available, so P3 could never be scheduled. No safe sequence exists, so the state is unsafe (deadlock may occur).
   - In short: at each step, check whether available resources can fulfil some process's remaining need. If yes, schedule it and keep going. If you reach a point where no remaining need can be fulfilled, the system is in an unsafe state.
   - Interviews do not ask you to solve a Banker's algorithm numerical; that comes in university exams ("find the safe sequence"). Interviews ask: what is deadlock avoidance, what does it assume is known (allocated, max need, number of processes, instances of each resource), and which algorithm is used for it (Banker's).

3. **Deadlock Detection:** Systems haven't implemented deadlock-prevention or a deadlock avoidance technique, then they may employ DL detection then, recovery technique.
   - Deadlock handling order: prevention, avoidance, then detection & recovery. If an OS implements neither prevention nor avoidance, it lets the system go into deadlock, detects it with an algorithm, and then recovers.
   - The detection algorithm runs periodically (at some set interval):

   ```mermaid
   flowchart LR
       A[Run detection algorithm] --> B{System in deadlock?}
       B -- yes --> C[Recovery mechanism]
       B -- no --> D[Wait for interval]
       D --> A
   ```

   1. Single Instance of Each resource type **(wait-for graph method)**
      1. A deadlock exists in the system if and only if there is a cycle in the wait-for graph. In order to detect the deadlock, the system needs to maintain the wait-for graph and periodically system invokes an algorithm that searches for the cycle in the wait-for graph.
         - Wait-for graph is a version of the resource allocation graph (RAG): remove the resource vertices from the RAG and merge the edges, so only process vertices remain.
         - Edge Pi → Pj means Pi is waiting for a resource held by Pj.

         ```
         Resource allocation graph            Wait-for graph

            P1 ──request──> R1                  P1 ────> P2
            ^                |                  ^         |
            |            held by                └─────────┘
          held by            v
            R2 <──request── P2
         ```

         - Here P1 waits for a resource held by P2, and P2 waits for a resource held by P1: a cycle, so deadlock.
         - Cycle in the wait-for graph → deadlock; no cycle → no deadlock. Valid only for single instance of each resource.
   2. Multiple instances for each resource type
      1. Banker Algorithm
         - Run the Banker's algorithm: safe sequence found → no deadlock; no safe sequence → deadlock detected.

4. **Recovery from Deadlock**
   - Once detection finds a deadlock, the recovery mechanism is called.
   1. Process termination
      1. Abort all DL processes
         - E.g. forcefully kill both P1 and P2 from the example above. This surely removes the deadlock, but it is very harsh.
      2. Abort one process at a time until DL cycle is eliminated.
         - E.g. kill only the lower-priority process. If P2 has low priority, kill it; it frees R1, P1 gets R1, and the deadlock is removed. Gentler than killing all.
   2. Resource preemption
      1. To eliminate DL, we successively preempt some resources from processes and give these resources to other processes until DL cycle is broken.
         - Similar to process termination, but take away resources instead of killing. E.g. P2 has low priority, holds R1 and waits for R2: preempt R1 from P2, so R1 is free and P1 gets it.
