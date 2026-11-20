# Lecture 14: MLQ | MLFQ

- The algorithms so far (FCFS, SJF, RR, priority) are simple algorithms. Real operating systems do not implement them directly; they combine them in an optimised way. MLQ and MLFQ are such real-life designs.

1. Multi-level queue scheduling (**MLQ**)
   a. Ready queue is divided into multiple queues depending upon priority.
      - Earlier algorithms treated all processes (P1, P2, P3, ...) the same. MLQ first divides processes by their nature into three types, then splits the single ready queue into three logical divisions, one ready queue per type.

   b. A process is permanently assigned to one of the queues (inflexible) based on some property of process, memory, size, process priority or process type.
      - When a new process arrives, the OS looks at its nature (memory size it needs, its priority, its type) and pushes it into one of the queues.
      - Once placed, it stays in that queue for its whole life and is scheduled there by that queue's algorithm. E.g., a system process always goes to, and stays in, the SP queue; it never moves to the IP queue.

   c. Each queue has its own scheduling algorithm. E.g., SP -> RR, IP -> RR & BP -> FCFS.
      - Each queue can use any of the algorithms studied so far.

   ```
   Highest priority  |
                     |  ---> [ System process (SP) queue ]      --->
                     |
                     |  ---> [ Interactive process (IP) queue ] --->
                     |
   Lowest priority   v  ---> [ Batch process (BP) queue ]       --->
   ```

   d. System process: Created by OS (Highest priority)
      - These are the processes important for the OS's own working.
      - Why highest priority: if the OS's own processes do not get priority, the OS cannot work properly.

   Interactive process (Foreground process): Needs user input (I/O).
   - E.g., Microsoft Word: it keeps waiting for user input (I/O).
   - Called foreground because it is visible at the front of the user space (in the GUI).
   - Placed after system processes; these are the user processes.

   Batch process (Background process): Runs silently, no user input required.
   - E.g., in a Unix terminal, `sleep 100 &` (the `&` used in the orphan/zombie process demo): the process runs in the background, needs no input and is not visible in front.
   - Kept at the lowest priority, even though some batch processes may also be important.

   e. Scheduling among different sub-queues is implemented as **fixed priority preemptive** scheduling. E.g., foreground queue has absolute priority over background queue.
      - The fixed priority order is: SP queue > IP queue > BP queue.
      - So MLQ has two levels of scheduling:
        - Within a queue (intra-queue): the queue's own algorithm.
        - Between queues (inter-queue): fixed priority preemptive scheduling.

   f. If an interactive process comes & batch process is currently executing. Then, batch process will be preempted.
      - E.g., P2 (a batch process) is running on the CPU. A new process P1 arrives and it is an interactive process. The BP queue has the lowest priority, so P2 is preempted and P1 is scheduled.
      - Similarly, if a system process arrives while an interactive process is running, the interactive process is preempted.

   g. Problem: Only after completion of all the processes from the top-level ready queue, the further level ready queues will be scheduled.
      This came starvation for lower priority process.
      - Until every process in the SP queue terminates or goes to wait, the IP and BP queues get no chance.
      - Same as priority scheduling: the highest priority gets most CPU time, the lowest may never get a chance (indefinite waiting).
      - Batch processes wait the most, so the overall average waiting time is high.
      - MLQ cannot use ageing to fix this, because there is no inter-queue movement.

   h. Convoy effect is present.
      - MLQ tries to optimise for the real-world mix of processes, but the fixed priority between queues is the weak point: the SP queue gets most CPU time and the BP queue is effectively forgotten.
      - MLQ is mostly a concept; it is hardly used today. MLFQ is its improved version.

2. Multi-level feedback queue scheduling (**MLFQ**)
   - Improved version of MLQ that tries to reduce MLQ's heavy convoy effect / starvation. It is used in OSes today (e.g., macOS uses MLFQ, with different types of priorities added on top).

   a. Multiple sub-queues are present.

   b. Allows the process to move between queues. The idea is to separate processes according to the characteristics of their BT. If a process uses too much CPU time, it will be moved to lower priority queue. This scheme leaves I/O bound and interactive processes in the higher-priority queue.
      - Key difference from MLQ: inter-queue movement is allowed.
      - Processes taking more time (higher BT) keep getting moved to lower queues.
      - I/O bound / interactive processes go to wait every little while, needing user input (user presses Enter, Next, etc.). They are kept in / moved to the higher queues.
      - Why interactive processes get high priority: you turn on the system and launch an application. If background or system processes got more CPU time and your application got none, the OS would not respond to the user. Nobody would want to work on such an OS.

   In addition, a process that waits too much in a lower-priority queue may be moved to a higher priority queue. This form of ageing prevents starvation.
   - Problem it solves: processes that keep moving to lower queues can starve, because upper queues get more time.
   - Ageing (same method as in priority scheduling): after a point, the priority of processes in lower queues is increased step by step, and they are moved up to higher queues.
   - MLQ could not use ageing since it had no inter-queue movement; MLFQ can.

   c. Less starvation then MLQ.

   d. It is flexible.

   e. Can be configured to match a specific system design requirement.
      - Things the designer can configure: when to send a process to a lower priority queue, at what interval to apply ageing (raise priority), whether interactive or system processes sit at the top, how much priority background processes get.

   Sample MLFQ design:

   ```
   new --->  [ TQ = 2 ]  ---> (done, exit)
                 |
                 v  (not done in TQ)
   new --->  [ TQ = 4 ]  ---> (done, exit)
                 |
                 v  (not done in TQ)
   new --->  [ TQ = 8 ]  ---> (done, exit)
                 |
                 v  (not done in TQ)
   new --->  [  FCFS  ]  ---> (done, exit)
   ```

   - Queues 1 to 3 use RR with time quantum 2, 4 and 8 respectively; queue 4 uses FCFS.
   - A new process first enters the top queue (TQ = 2).
     - If its BT is at most 2, it finishes there and exits.
     - If its BT is more than 2, it is moved to the next queue and gets TQ = 4; if still not done, TQ = 8; if still not done, it is scheduled FCFS.
   - Benefit: processes with low BT do not starve. E.g., a process needing 1 sec exits right in the first queue.
   - Each process gets multiple chances, with a growing time quantum, before being pushed to FCFS.
   - More queues can be added; this is just a small sample.
   - Ageing here: a process P1 with a large BT may fall through every queue to the FCFS queue and starve there. To prevent this, its priority is increased by ageing and it can be moved back up to a higher queue.

   Design of an MLFQ: the five things a designer decides (e.g., when building an OS):
   1. Number of queues, based on the OS's requirements.
   2. Scheduling algorithm for each queue.
   3. Method to upgrade a process to a higher queue.
      - E.g., ageing: if a process is stuck in the FCFS queue, its priority counter increases every 15 min (say), and it is moved to upper queues.
      - So between queues there is a flexible priority scheduling (unlike MLQ's fixed priority).
   4. Method to demote a process to a lower queue.
      - In the sample: if the process does not finish within the queue's TQ, it is demoted to the next queue.
   5. Which queue a process enters first.
      - E.g., new processes can be sent to the top queue first, or a process known to be very slow can be sent directly to the FCFS queue.

3. Comparison:

   | | FCFS | SJF | PSJF | Priority | P-Priority | RR | MLQ | MLFQ |
   |---|---|---|---|---|---|---|---|---|
   | Design | Simple | Complex | Complex | Complex | Complex | Simple | Complex | Complex |
   | Preemption | No | No | Yes | No | Yes | Yes | Yes | Yes |
   | Convoy effect | Yes | Yes | No | Yes | Yes | No | Yes | Yes |
   | Overhead | No | No | Yes | No | Yes | Yes | Yes | Yes |

   - Overhead = context switching, which only happens with preemption.
   - FCFS
     - Design simple: implemented as a plain queue.
     - No preemption. (Question: what is the preemptive version of FCFS? RR, from the previous lecture.)
     - Convoy effect is heavy; convoy effect was first defined using FCFS. If the first process has the largest BT, all others keep waiting.
     - No overhead: no preemption, so no context switching. Once P1 gets the CPU, it keeps it.
   - SJF
     - Design complex: calculating the correct BT of a process is nearly impossible.
     - No preemption.
     - Convoy effect: if a process with a large BT arrives at t = 0, it gets scheduled and runs to completion. A process P2 with smaller BT that arrives later cannot be scheduled.
     - No overhead, since no preemption.
   - PSJF
     - Design complex: BT still has to be estimated.
     - Preemption: when a job with a smaller BT arrives, the current one is preempted and the shorter one is scheduled.
     - No convoy effect (negligible): it gives the lowest average waiting time.
     - Overhead: yes, context switching due to preemption.
   - Priority
     - Design complex: deciding the right priority for a process is itself a hard decision.
     - No preemption (non-preemptive version).
     - Convoy effect is heavy (indefinite waiting).
     - No overhead, since non-preemptive.
   - P-Priority
     - Design complex: same problem of assigning priority.
     - Preemption: yes.
     - Convoy effect: yes. Higher priority jobs keep getting scheduled; low priority jobs keep waiting (starvation).
     - Overhead: yes, it is preemptive.
   - RR
     - Design simple: a simple block diagram (circular queue).
     - Its best quality: lowest response time. Every process gets the CPU at least once quickly.
     - Preemption: yes. If the process does not finish within the time quantum, it is preempted and the next job is taken.
     - No convoy effect: no starvation, every process gets the CPU after a little while.
     - Overhead: yes, context switching.
   - MLQ
     - Design complex: queues have to be built, and each process has to be assigned to the right queue.
     - Preemption: yes. A high priority job (e.g. interactive) preempts a batch process.
     - Convoy effect: yes. Low priority processes may never get CPU time (starvation).
     - Overhead: yes, context switching.
   - MLFQ
     - Design complex.
     - Preemption: yes.
     - Convoy effect: yes, but reduced by ageing, not eliminated. Like deadlock avoidance/prevention later: no implementation is perfect, and a computer still hangs sometimes, whatever its specifications.
     - Overhead: yes, context switching.
   - Implement all these algorithms yourself; then in an interview you can explain what happens in each one.
   - This completes CPU scheduling. Next topic: concurrency.
