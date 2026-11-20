# Lecture 12: Intro to Process Scheduling | FCFS | Convoy Effect

- Before the scheduling algorithms themselves, a few terms (jargon) must be clear, since every later lecture uses them.

1. **Process Scheduling**
   a. Basis of Multi-programming OS.
   b. By switching the CPU among processes, the OS can make the computer more productive.
   c. Many processes are kept in memory at a time, when a process must wait or time quantum expires, the OS takes the CPU away from that process & gives the CPU to another process & this pattern continues.
   - Recap of the flow:
     - The LTS (long-term scheduler) brings processes (P1, P2, P3, ...) into the ready queue.
     - The OS picks one process from the ready queue and the STS (short-term scheduler) dispatches it to the CPU (running state).
     - It runs as per the algorithm in use. After its time quantum it goes back to the ready queue, or to the wait state if it does I/O, or exits when done.
   - Which process gets picked from the ready queue is decided by the process scheduling algorithm. This selection is also called CPU scheduling.
   - The module that actually gives control of the CPU to the selected process is the dispatcher.

   ```
            LTS                     STS / dispatcher
   New ─────────► Ready queue ─────────────────────► CPU (Running) ──► Exit
                  [P1 P2 P3 ...]                       │
                       ▲                               │
                       └── time quantum expires / ─────┘
                           back from I/O wait
   ```

2. **CPU Scheduler**
   a. Whenever the CPU become idle, OS must select one process from the ready queue to be executed.
   b. Done by STS.
   - Two types (paradigms) of scheduling: non-preemptive and preemptive.

3. **Non-Preemptive scheduling**
   a. Once CPU has been allocated to a process, the process keeps the CPU until it releases CPU either by terminating or by switching to wait-state.
      - Wait-state here means the process goes to do I/O.
      - Once a process gets the CPU, it keeps it. The time quantum / time sharing idea is missing here.
   b. Starvation, as a process with long burst time may starve less burst time process.
      - Starvation: a process is not getting the CPU at all, because another job (a high-priority job, or one that holds the CPU for long) keeps running, so the other jobs in the ready queue get no time.
      - Starvation is more in non-preemptive, because time sharing is missing. Example: a CPU-intensive job that runs 20-30 minutes with no I/O instructions. Every other process in the ready queue starves for those 20-30 minutes until it terminates.
   c. Low CPU utilization.

4. **Preemptive scheduling**
   a. CPU is taken away from a process after time quantum expires along with terminating or switching to wait-state.
      - The process releases the CPU when it terminates or goes for I/O, and also when its time quantum expires; it then goes back to the ready queue.
   b. Less Starvation
      - Not zero starvation, only less: every process gets some chance after a while, since the running process's time quantum must expire.
   c. High CPU utilization.
      - Processes get the chance to do their work, so at any particular time the CPU is working on a larger number of processes.
   d. Overhead is more in preemptive scheduling.
      - Apart from going for I/O and termination, there is the extra cost of switching the process every time quantum. With a 1 second time quantum, the process changes every second, so the STS must pick a new process each second (10 switches in 10 seconds).

   | | Non-preemptive | Preemptive |
   |---|---|---|
   | CPU released on | terminate, wait (I/O) | terminate, wait (I/O), time quantum expiry |
   | Starvation | more | less |
   | CPU utilization | low | high |
   | Overhead | less | more |

5. **Goals of CPU scheduling**
   - These are the parameters an OS designer keeps in mind when choosing/designing the CPU scheduling algorithm for the process management part of the OS.
   a. Maximum CPU utilization
      - CPU is the most important resource; it should not sit idle even for a few seconds.
   b. Minimum Turnaround time (TAT).
      - Once a process enters the ready queue, it should finish execution and exit as fast as possible.
   c. Min. Wait-time
      - Every process should wait for the CPU as little as possible (e.g. after being preempted back to the ready queue). Too much waiting leads to starvation.
   d. Min. response time.
      - A process put into the ready queue should get the CPU at least once as soon as possible, so its program at least starts executing. It should not sit in the ready queue for long without ever getting the CPU.
   e. Max. throughput of system.
      - Throughput is the measure of a CPU scheduling algorithm: the whole process management system with the CPU should complete the most processes per unit time.
   - The main aim behind all these goals is maximum CPU utilization, i.e. a fast, efficient system.

6. **Throughput**: No. of processes completed per unit time.

7. **Arrival time (AT)**: Time when process is arrived at the ready queue.
   - The system has a timeline (clock) starting at t = 0 when the system is switched on. AT is the point on this clock at which the process entered the ready queue.

8. **Burst time** (BT): The time required by the process for its execution.
   - BT is the time the process would take if it were the only process in the system, i.e. the single owner of the CPU, with nothing else in the ready queue.

9. **Turnaround** time (TAT): Time taken from first time process enters ready state till it terminates. (CT - AT)
   - In between, the process may go to the wait state for I/O, or be preempted back to the ready queue, many times. TAT covers everything from its first entry into the ready queue to its final exit.

10. **Wait** time (WT): Time process spends waiting for CPU. (WT = TAT – BT)
    - TAT is the time the process actually took; BT is the time it should ideally have taken (alone in the system). The difference is the time spent waiting.

11. **Response** time: Time duration between process getting into ready queue and process getting CPU for the first time.

12. **Completion** Time (CT): Time taken till process gets terminated.
    - On the timeline, CT is the clock time at which the process exits. Between arrival and completion the process travels through different states (scheduled first, goes to wait, back to ready queue, scheduled again, time quantum expires, back to ready queue, ...).
    - Don't confuse CT with TAT: TAT = CT − AT.

13. **FCFS** (First come-first serve):
    - Simplest CPU scheduling algorithm.
    a. Whichever process comes first in the ready queue will be given CPU first.
       - If P1, P2, P3 arrive in that order, the FCFS scheduler selects P1 first and tells the dispatcher to give it the CPU. When P1 finishes, P2 runs; when P2 finishes, P3 runs.
       - Values are computed with a **Gantt chart** (spelled G-A-N-T-T): a bar showing the full timeline of which process runs when.
       - Example 1 (long job first), all values in time units:

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

         - P1 arrives first (AT 0), runs 20 units. Then P2 runs 2 units (till 22), then P3 runs 2 units (till 24).
         - P1 waits 0, since it executes as soon as it arrives.
         - Average WT = (0 + 19 + 20) / 3 = 13.
       - Example 2 (same jobs, long job moved to the end of the ready queue):

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

         - Average WT = (0 + 1 + 2) / 3 = 1.
       - Only the order changed, yet average WT dropped from 13 to 1. This is the convoy effect.
    b. In this, if one process has longer BT. It will have major effect on average WT of diff processes, called **Convoy effect.**
       - When a heavy job (largest BT) comes first, all other jobs (P2, P3) wait for a long time behind it, which raises the average WT of the whole ready queue.
    c. Convoy Effect is a situation where many processes, who need to use a resource for a short time, are blocked by one process holding that resource for a long time.
       i. This cause poor resource management.
       - Not limited to the CPU, scheduling algorithms or FCFS: with any resource, if one process holds it for a very long time while others also want it, the waiting processes' wait time grows.
       - The resource belongs to everyone; the goal is no partiality, so P2 should also get the resource on time.
       - Interview tip: "What is convoy effect?" is asked directly in interviews.
