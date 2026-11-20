# Lecture 2: Types of OS

## OS goals

Each type of OS is judged by how well it meets these goals.

- **Maximum CPU utilization:** The CPU should never sit idle while processes wait. An idle CPU still costs electricity.
  - **Example:** The CPU runs P1. P1 goes to I/O, such as a copy-paste, which may take a minute or two. The CPU should run P2 meanwhile.

- **Less process starvation:** Starvation means a process never gets the CPU because another process holds it.
  - **Example:** P1 is a very long job, or a bad program stuck in a `while(1)` loop. P2 and P3 should not be denied the CPU forever.

- **Higher priority job execution:** P1, P2 and P3 run turn by turn. A high-priority job P4 arrives. The OS should set the others aside and run P4 at once.
  - **Example:** An antivirus starts a high-priority scan as soon as a removable disk is inserted, whatever else is running.

## Types of operating systems

| Type | Example |
|------|---------|
| Single process operating system | MS DOS, 1981 |
| Batch-processing operating system | ATLAS, Manchester Univ., late 1950s to early 1960s |
| Multiprogramming operating system | THE, Dijkstra, early 1960s |
| Multitasking operating system | CTSS, MIT, early 1960s |
| Multi-processing operating system | Windows NT |
| Distributed system | LOCUS |
| Real time OS | ATCS |

```
Types of OS
   │
   ├──► Single process operating system
   ├──► Batch-processing operating system
   ├──► Multi-programming operating system
   ├──► Multitasking operating system
   ├──► Multi-processing operating system
   ├──► Distributed operating system
   └──► Real Time OS
```

> **Interview:** Know all the names and one example of each.

> **Interview:** Single process, batch, multiprogramming, multitasking and multi-processing matter most. Interviewers directly ask you to explain multiprogramming, multitasking and multi-processing. People confuse them.

### Single process OS

Only one process executes at a time from the ready queue. This is the oldest and simplest type. There is no concept of multiple jobs.

- **Example:** P1, P2 and P3 wait. P2 gets the CPU only when P1 finishes. Then P3 runs.
- **Real example:** MS DOS.
- **Why it was built:** Software requirements follow the hardware, never the other way round. The earliest hardware handled only one process at a time.

| Goal | Met? | Why |
|------|------|-----|
| Maximum CPU utilization | No | If P1 goes for I/O, P2 still gets no chance. The CPU sits idle. |
| Process starvation | Yes (starvation happens) | If P1 is huge (the `while(1)` example), P2 and P3 never run. |
| High priority job execution | No | The antivirus scan cannot run until P1 finishes. |

### Batch-processing OS

1. The user prepares a job using punch cards.
2. The user submits the job to the computer operator.
3. The operator collects jobs from different users and sorts them into batches with similar needs.
4. The operator submits the batches to the processor one by one.
5. All the jobs of one batch are executed together.

- **Priorities:** They cannot be set if a job comes with a higher priority.
- **Starvation:** It may happen, because a batch may take long to complete.
- **Idle CPU:** The CPU may become idle during I/O.

```
(User 1) ──► [Job 1] ──┐
(User 2) ──► [Job 2] ──┼──► (Operator) ──►  Batch 2       Batch 1      ┌──────────────┐
   ⋮            ⋮      │                   ┌───────┐     ┌───────┐     │     CPU      │
(User n) ──► [Job n] ──┘                   │ Job 7 │     │ Job 4 │     │      +       │
                                           │ Job 5 │ ──► │ Job 1 │ ──► │      OS      │
                                           │ Job 2 │     └───────┘     │ User Program │
                                           └───────┘                   └──────────────┘
```

- **Punch card:** A paper card with small circles, some punched and some not. This stores binary information. The card is scanned into digital information, like the magnetic strip on today's ATM, credit and debit cards.
- **Operator:** It can be thought of as software. It sees only each job's requirements from the outside. It cannot estimate how long a job takes. It sorts jobs by requirements in a brute-force way. Example: Batch 1 holds Job 1 and Job 4. Batch 2 holds Job 2, Job 5 and Job 7.
- **Execution:** Batches go to the CPU one after another. Inside a batch, the single CPU runs one job at a time, like a single process OS. Batch 2 starts when Batch 1 completes.
- **Difference from single process OS:** The only optimisation is grouping jobs into batches.

| Goal | Met? | Why |
|------|------|-----|
| Maximum CPU utilization | No | If J1 in Batch 1 takes long in I/O, J4 just waits. |
| Process starvation | Yes (starvation happens) | If J1 takes long, J4 waits. There is also batch starvation: if Batch 1 takes very long, later batches get no chance. |
| High priority job execution | No | A batch cannot start until the current batch completes. |

**Real example:** ATLAS.

### Multiprogramming OS

Multiprogramming increases CPU utilization. It keeps multiple jobs (code and data) in **memory**. The CPU always has a job to run if some job is busy with I/O.

- **CPU:** Single CPU.
- **Context switching:** It is used for processes.
- **When it switches:** The switch happens when the current process goes to the wait state.
- **Idle time:** CPU idle time is reduced.

- **Ready queue:** A queue of all jobs that are ready and only need the CPU (J1, J2, J3, J4 and so on).
- **Example:** J1 runs first, because there is one CPU. J1 copies data from a USB/pen drive, so it goes to I/O and then to the wait state. J2 is scheduled. The CPU does not stay idle.
- **Goals:** From this type onwards the goals start getting fulfilled.

> **Interview:** Multiprogramming, multitasking and multi-processing are frequently asked.

**Real example:** THE.

#### Context switching

This is covered in detail later in process management.

- **Why it is needed:** Many processes are in memory and there is one CPU. The CPU must switch whenever a process goes to I/O or the wait state.
- **Analogy:** Studying physics, you bookmark each book, close it and set it aside. Then you open the chemistry books at their bookmarks. You saved the physics state and restored the chemistry state.
- **With processes:** The CPU runs P1. P1 goes for I/O, so P2 must run.
  - **Save:** P1's context is saved in its PCB. The context is the address where it was executing, its call stack and the information on it.
  - **Restore:** P2's information is taken from its PCB. P2's state and stack are restored. The CPU works on P2.
- **Definition:** This saving and restoring is called context switching.
- **PCB (Process Control Block):** A small data structure that stores information related to a process.

### Multitasking OS

Multitasking is a logical extension of multiprogramming.

- **CPU:** Single CPU.
- **Tasks:** It can run more than one task simultaneously.
- **Techniques:** Context switching and time sharing are used.
- **Responsiveness:** It increases responsiveness.
- **Idle time:** CPU idle time is reduced further.

- **Similarity with multiprogramming:** Both have a single CPU and use context switching. Time sharing makes multitasking better.
- **Problem with multiprogramming:** A context switch happens only on I/O or the wait state. A job that never does I/O keeps executing, and other jobs can starve.
- **Fix (time sharing):** Do not wait for I/O. Use a small time quantum, for example 100 ms. A job that has had its 100 ms is stopped and the next job gets a chance.
- **Example:** P1, P2 and P3 run on one CPU. If a process does I/O, it goes to wait and another gets the CPU, as in multiprogramming. Otherwise P1 runs 100 ms, then P2 gets 100 ms, then P3, and so on.
- **Today's OSes:** They are multitasking. All apps feel responsive and none hangs, because of time sharing.

| Goal | Met? | Why |
|------|------|-----|
| Maximum CPU utilization | Highest so far | The CPU is never idle. Some job always gets the next 100 ms. |
| Process starvation | Low | Even if P1 is very heavy, P2 gets an equal chance when P1's quantum ends. |
| High priority job execution | Yes | When a high-priority job arrives (P4, the antivirus scanning a USB drive), a software interrupt is raised. The running process is switched out and P4 gets the CPU immediately. |

**Real example:** CTSS.

### Multi-processing OS

A multi-processing OS has more than one CPU in a single computer.

- **Reliability:** It increases reliability. If one CPU fails, the other can work.
- **Throughput:** It gives better throughput.
- **Starvation:** It gives less process starvation. While one CPU works on a process, another process can run on the other CPU.

- **Same techniques:** Context switching and time sharing also apply. The difference is more than one CPU.
- **Utilization:** CPU utilization can be even higher. More apps run simultaneously and starvation is reduced further.
- **High priority job:** If CPU 1 is busy, CPU 2 can run it.
- **Modern CPUs:** A CPU may have 4 or 8 cores. Eight cores means 8 logical processors, which can be treated as 8 separate CPUs.
- **Example:** CPU 1 and CPU 2 run P1, P2, P3 and P4. P1 gets a quantum on CPU 1, then P2. Meanwhile P3 goes to CPU 2. The OS decides which job a CPU picks through process scheduling algorithms, covered later.
- **Reliability example:** In a single-CPU system, a hardware failure of that CPU takes the whole system down. Here, if CPU 1 fails, CPU 2 (and CPU 3 and so on) can still work.

> **Interview:** Single process OS has a single processor. Multiprogramming and multitasking also have a single processor. Multi-processing has more than one processor, which increases throughput. Systems used today are multi-processing.

**Real example:** Windows.

### Distributed OS

- **Resources:** The OS manages many bunches of resources: one or more CPUs, memories, GPUs, and so on.
- **Loosely connected autonomous nodes:** The nodes are interconnected computers.
- **Definition:** It is a collection of independent, networked, communicating and physically separate computational nodes.
- **Other name:** It is also called a loosely coupled operating system.

- **Difference from before:** Until now there was one OS with one or many CPUs and one memory in a single box. Here there are many CPUs and memories connected over a network. They are separate computers, such as one at your home and one at mine, connected over the internet or a LAN and managed by one OS.
- **Job placement:** The OS can send P1 to one machine, P2 to another, and P3 and P4 to others.
- **Different nodes:** Nodes can differ. One may be low-end, one high-end, one with a GPU, one without.
- **Many users:** Many jobs can execute and there can be multiple users (U1, U2 and so on).
- **Example:** On LeetCode, pressing submit runs your code on some free Linux machine, where it is judged. It is many systems, not one. The OS managing such computers over the internet is a distributed OS.

**Real example:** LOCUS.

### RTOS

RTOS means Real Time Operating System.

- **Real time:** It does error-free computation within tight time boundaries.
- **Uses:** Air traffic control systems, robots and so on.

- **Accuracy:** It is needed where there must be no chance of error. Accuracy must be very high, even to many decimal places.
- **Air traffic control (ATC):** Many flights are in the air and lives depend on the ATC. Computation must be error free and real time.
- **Meaning of real time:** Execution must be very fast. A job must finish within seconds, which means within a deadline.
- **Industrial use:** It is also used in industrial applications, for example a nuclear plant's systems. These need demanding, error-free computation done quickly within a deadline.

**Real example:** ATCS.
