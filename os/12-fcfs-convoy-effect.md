# Lecture 12: Intro to Process Scheduling | FCFS | Convoy Effect

These terms are used by every scheduling algorithm.

1. **Process Scheduling**

   a. It is the basis of a multi-programming OS.

   b. The OS switches the CPU among processes. This makes the computer more productive.

   c. Many processes are kept in memory. When a process must wait or its time quantum expires, the OS takes the CPU away and gives it to another process. This repeats.

   - **Flow:**
     - The LTS (long-term scheduler) brings processes (P1, P2, P3, ...) into the ready queue.
     - The OS picks one process. The STS (short-term scheduler) dispatches it to the CPU (running state).
     - After its time quantum it goes back to the ready queue. It goes to the wait state on I/O. It exits when done.
   - **CPU scheduling:** The process scheduling algorithm decides which process is picked from the ready queue. This selection is also called CPU scheduling.
   - **Dispatcher:** This module gives control of the CPU to the selected process.

   ```
            LTS                     STS / dispatcher
   New ─────────► Ready queue ─────────────────────► CPU (Running) ──► Exit
                  [P1 P2 P3 ...]                       │
                       ▲                               │
                       └── time quantum expires / ─────┘
                           back from I/O wait
   ```

2. **CPU Scheduler**

   a. Whenever the CPU becomes idle, the OS must select one process from the ready queue.

   b. The STS does this.

   - **Two types (paradigms):** non-preemptive and preemptive.

3. **Non-Preemptive scheduling**

   a. A process keeps the CPU until it terminates or switches to the wait state (I/O).
      - There is no time sharing. The time quantum idea is missing.

   b. Starvation can happen. A process with a long burst time may starve processes with a short burst time.
      - **Starvation:** A process does not get the CPU at all, because another job (high-priority, or holding the CPU long) keeps running.
      - **Example:** A CPU-intensive job runs 20-30 minutes with no I/O. Every other process in the ready queue starves until it terminates.

   c. CPU utilization is low.

4. **Preemptive scheduling**

   a. The CPU is taken away when the time quantum expires, and also on termination or wait. The process then goes back to the ready queue.

   b. Starvation is less.
      - **Not zero:** Every process gets some chance after a while, since the running process's time quantum must expire.

   c. CPU utilization is high.
      - The CPU works on a larger number of processes at any time.

   d. Overhead is more.
      - **Extra cost:** The process is switched every time quantum.
      - **Example:** With a 1 second time quantum, the STS picks a new process each second (10 switches in 10 seconds).

   | | Non-preemptive | Preemptive |
   |---|---|---|
   | CPU released on | terminate, wait (I/O) | terminate, wait (I/O), time quantum expiry |
   | Starvation | more | less |
   | CPU utilization | low | high |
   | Overhead | less | more |

5. **Goals of CPU scheduling**

   - An OS designer keeps these parameters in mind when choosing a CPU scheduling algorithm.

   a. Maximum CPU utilization.
      - The CPU is the most important resource. It should not sit idle even for a few seconds.

   b. Minimum turnaround time (TAT).
      - A process in the ready queue should finish and exit as fast as possible.

   c. Minimum wait time.
      - A process should wait for the CPU as little as possible, for example after being preempted. Too much waiting leads to starvation.

   d. Minimum response time.
      - A process in the ready queue should get the CPU at least once as soon as possible, so its program starts executing.

   e. Maximum throughput of the system.
      - Throughput measures a CPU scheduling algorithm. The system should complete the most processes per unit time.

   - **Main aim:** All these goals aim at maximum CPU utilization, that is, a fast and efficient system.

6. **Throughput:** The number of processes completed per unit time.

7. **Arrival time (AT):** The time when the process arrives at the ready queue.
   - The system clock starts at t = 0 when the system is switched on. AT is the point on this clock at which the process entered the ready queue.

8. **Burst time (BT):** The time the process needs for its execution.
   - BT is the time the process would take if it were the only process in the system, the single owner of the CPU.

9. **Turnaround time (TAT):** The time from when the process first enters the ready state until it terminates. TAT = CT - AT.
   - In between, the process may go to the wait state or be preempted many times. TAT covers all of it.

10. **Wait time (WT):** The time the process spends waiting for the CPU. WT = TAT - BT.
    - TAT is the time actually taken. BT is the ideal time (alone in the system). The difference is the waiting.

11. **Response time:** The time between the process getting into the ready queue and getting the CPU for the first time.

12. **Completion time (CT):** The time taken until the process terminates.
    - On the timeline, CT is the clock time at which the process exits.
    - **Do not confuse CT with TAT:** TAT = CT - AT.

13. **FCFS (First Come First Serve):**
    - It is the simplest CPU scheduling algorithm.

    a. Whichever process comes first in the ready queue gets the CPU first.
       - If P1, P2, P3 arrive in that order, P1 runs first, then P2, then P3.
       - **Gantt chart:** Values are computed with it. It is a bar showing the full timeline of which process runs when.
       - **Example 1 (long job first),** all values in time units:

         | Process | AT | BT | CT | TAT = CT − AT | WT = TAT − BT |
         |---|---|---|---|---|---|
         | P1 | 0 | 20 | 20 | 20 | 0 |
         | P2 | 1 | 2 | 22 | 21 | 19 |
         | P3 | 2 | 2 | 24 | 22 | 20 |

         ```
         Gantt chart
         |          P1          | P2 | P3 |
         0                      20   22   24
         ```

         - P1 waits 0, since it executes as soon as it arrives.
         - **Average WT:** (0 + 19 + 20) / 3 = 13.
       - **Example 2 (same jobs, long job moved to the end of the ready queue):**

         | Process | AT | BT | CT | TAT = CT − AT | WT = TAT − BT |
         |---|---|---|---|---|---|
         | P2 | 0 | 2 | 2 | 2 | 0 |
         | P3 | 1 | 2 | 4 | 3 | 1 |
         | P1 | 2 | 20 | 24 | 22 | 2 |

         ```
         Gantt chart
         | P2 | P3 |          P1          |
         0    2    4                      24
         ```

         - **Average WT:** (0 + 1 + 2) / 3 = 1.
       - Only the order changed, yet average WT dropped from 13 to 1. This is the convoy effect.

    b. If one process has a longer BT, it has a major effect on the average WT of the other processes. This is called the **Convoy effect.**
       - A heavy job (largest BT) comes first. All other jobs (P2, P3) wait behind it. This raises the average WT of the whole ready queue.

    c. **Convoy effect:** Many processes need a resource for a short time. One process holds that resource for a long time and blocks them all.
       i. This causes poor resource management.
       - **Not limited to the CPU:** It applies to any resource, not only scheduling or FCFS.
       - **No partiality:** The resource belongs to everyone. P2 should also get it on time.

    > **Interview:** "What is convoy effect?" is asked directly in interviews.
