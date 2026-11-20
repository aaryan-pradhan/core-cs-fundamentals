# Lecture 14: MLQ | MLFQ

- **Simple algorithms:** FCFS, SJF, RR and priority are simple. Real operating systems combine them in an optimised way. MLQ and MLFQ are such real-life designs.

1. Multi-level queue scheduling (**MLQ**)

   a. The ready queue is divided into multiple queues depending on priority.
      - MLQ divides processes by their nature into three types. Each type gets its own logical ready queue.

   b. A process is permanently assigned to one queue (inflexible). The assignment is based on memory, size, process priority or process type.
      - The process stays in that queue for its whole life. That queue's algorithm schedules it.
      - **Example:** A system process always stays in the SP queue. It never moves to the IP queue.

   c. Each queue has its own scheduling algorithm. For example, SP uses RR, IP uses RR and BP uses FCFS.

   ```
   Highest priority  |
                     |  ---> [ System process (SP) queue ]      --->
                     |
                     |  ---> [ Interactive process (IP) queue ] --->
                     |
   Lowest priority   v  ---> [ Batch process (BP) queue ]       --->
   ```

   d. The three process types:

   | Type | Also called | Priority | Notes |
   |---|---|---|---|
   | System process | | Highest | Created by the OS. |
   | Interactive process | Foreground process | Middle | Needs user input (I/O). |
   | Batch process | Background process | Lowest | Runs silently. Needs no user input. |

   - **System process:** It is important for the OS's own working. Without priority, the OS cannot work properly.
   - **Interactive process:** It is a user process. It is visible at the front of the user space (in the GUI).
     - **Example:** Microsoft Word keeps waiting for user input (I/O).
   - **Batch process:** It is not visible in front.
     - **Example:** In a Unix terminal, `sleep 100 &` (the `&` used in the orphan/zombie process demo).
     - It is kept at the lowest priority, even though some batch processes may also be important.

   e. Scheduling among sub-queues is **fixed priority preemptive**. For example, the foreground queue has absolute priority over the background queue.
      - **Fixed priority order:** SP queue, then IP queue, then BP queue.
      - **Intra-queue (within a queue):** The queue's own algorithm.
      - **Inter-queue (between queues):** Fixed priority preemptive scheduling.

   f. If an interactive process comes while a batch process is executing, the batch process is preempted.
      - **Example:** P2 (batch) is running. Interactive P1 arrives. P2 is preempted and P1 is scheduled.
      - **Similarly:** A system process arriving preempts a running interactive process.

   g. **Problem:** Lower-level queues are scheduled only after all processes in the top-level queue complete. This causes starvation for lower priority processes.
      - The IP and BP queues get no chance until the SP queue terminates or waits.
      - **Same as priority scheduling:** The lowest may never get a chance (indefinite waiting).
      - **High average waiting time:** Batch processes wait the most.
      - **No ageing:** MLQ cannot use ageing, because there is no inter-queue movement.

   h. The convoy effect is present.
      - The fixed priority between queues is the weak point. The SP queue gets most CPU time and the BP queue is effectively forgotten.
      - **Mostly a concept:** MLQ is hardly used today. MLFQ is its improved version.

2. Multi-level feedback queue scheduling (**MLFQ**)
   - It is an improved version of MLQ. It reduces MLQ's heavy convoy effect and starvation.
   - **Used today:** For example, macOS uses MLFQ, with different types of priorities added on top.

   a. Multiple sub-queues are present.

   b. A process can move between queues. Processes are separated by the characteristics of their BT. A process that uses too much CPU time moves to a lower priority queue. I/O bound and interactive processes stay in the higher-priority queue.
      - **Key difference from MLQ:** Inter-queue movement is allowed.
      - **I/O bound and interactive processes:** They go to wait every little while, needing user input (user presses Enter, Next, and so on). They stay in the higher queues.
      - **Why interactive processes get high priority:** If background or system processes got more CPU time and your application got none, the OS would not respond to the user.

   - **Ageing:** A process that waits too much in a lower-priority queue may be moved to a higher priority queue. This prevents starvation.
     - **Problem it solves:** Processes that keep moving to lower queues can starve, because upper queues get more time.
     - **Method (same as in priority scheduling):** The priority of processes in lower queues is increased step by step. They move up to higher queues.
     - MLQ could not use ageing since it had no inter-queue movement. MLFQ can.

   c. Starvation is less than in MLQ.

   d. It is flexible.

   e. It can be configured to match a specific system design requirement.
      - **Configurable:** when to send a process to a lower queue, the interval for ageing (raising priority), whether interactive or system processes sit at the top, and how much priority background processes get.

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

   - **Queues:** Queues 1 to 3 use RR with time quantum 2, 4 and 8. Queue 4 uses FCFS.
   - **Entry:** A new process first enters the top queue (TQ = 2).
     - If its BT is at most 2, it finishes there and exits.
     - If its BT is more than 2, it moves to the next queue with TQ = 4. If still not done, TQ = 8. If still not done, it is scheduled FCFS.
   - **Benefit:** Processes with low BT do not starve. For example, a process needing 1 sec exits in the first queue.
   - **Multiple chances:** Each process gets multiple chances, with a growing time quantum, before FCFS.
   - **More queues:** More queues can be added. This is just a small sample.
   - **Ageing here:** A process P1 with a large BT may fall to the FCFS queue and starve there. Ageing raises its priority and moves it back up.

   **Design of an MLFQ:** the five things a designer decides.

   1. **Number of queues,** based on the OS's requirements.
   2. **Scheduling algorithm for each queue.**
   3. **Method to upgrade a process to a higher queue.**
      - **Example (ageing):** A process stuck in the FCFS queue gets its priority counter increased every 15 min (say) and moves to upper queues.
      - So between queues there is flexible priority scheduling (unlike MLQ's fixed priority).
   4. **Method to demote a process to a lower queue.**
      - In the sample, a process that does not finish within the queue's TQ is demoted.
   5. **Which queue a process enters first.**
      - **Example:** New processes go to the top queue first. A process known to be very slow can go directly to the FCFS queue.

3. Comparison:

   | | FCFS | SJF | PSJF | Priority | P-Priority | RR | MLQ | MLFQ |
   |---|---|---|---|---|---|---|---|---|
   | Design | Simple | Complex | Complex | Complex | Complex | Simple | Complex | Complex |
   | Preemption | No | No | Yes | No | Yes | Yes | Yes | Yes |
   | Convoy effect | Yes | Yes | No | Yes | Yes | No | Yes | Yes |
   | Overhead | No | No | Yes | No | Yes | Yes | Yes | Yes |

   - **Overhead:** It means context switching, which only happens with preemption.

   - **FCFS**
     - **Design simple:** It is a plain queue.
     - **No preemption.** The preemptive version of FCFS is RR.
     - **Convoy effect is heavy:** The convoy effect was first defined using FCFS. If the first process has the largest BT, all others keep waiting.
     - **No overhead:** Once P1 gets the CPU, it keeps it.

   - **SJF**
     - **Design complex:** Calculating the correct BT of a process is nearly impossible.
     - **Convoy effect:** A process with a large BT arrives at t = 0 and runs to completion. A later process P2 with smaller BT cannot be scheduled.

   - **PSJF**
     - **Design complex:** BT still has to be estimated.
     - **Preemption:** A smaller-BT job preempts the current one.
     - **No convoy effect (negligible):** It gives the lowest average waiting time.
     - **Overhead:** Preemption causes context switching.

   - **Priority**
     - **Design complex:** Deciding the right priority is itself a hard decision.
     - **Convoy effect is heavy** (indefinite waiting).
     - **No overhead,** since it is non-preemptive.

   - **P-Priority**
     - **Design complex:** Same problem of assigning priority.
     - **Convoy effect:** Higher priority jobs keep getting scheduled. Low priority jobs keep waiting (starvation).
     - **Overhead:** Yes, because it is preemptive.

   - **RR**
     - **Design simple:** A circular queue.
     - **Best quality:** Lowest response time. Every process gets the CPU at least once quickly.
     - **Preemption:** A process that does not finish within the time quantum is preempted.
     - **No convoy effect:** Every process gets the CPU after a little while.
     - **Overhead:** Yes, context switching.

   - **MLQ**
     - **Design complex:** Queues have to be built. Each process has to be assigned to the right queue.
     - **Preemption:** A high priority job (for example interactive) preempts a batch process.
     - **Convoy effect:** Low priority processes may never get CPU time (starvation).

   - **MLFQ**
     - **Design complex.**
     - **Convoy effect:** Yes, but reduced by ageing, not eliminated. This is like deadlock avoidance and prevention later. No implementation is perfect. A computer still hangs sometimes, whatever its specifications.

   - **Practice:** Implement all these algorithms yourself. Then in an interview you can explain what happens in each one.
   - **Next topic:** Concurrency.
