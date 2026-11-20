# Lecture 2: Types of OS

## OS goals –

The types of OS were built with these goals in mind; each type is judged by how well it meets them.

- Maximum CPU utilization
  - The CPU should never sit idle while there are processes waiting to run. A CPU is expensive and consumes electricity even when idle.
  - Example: CPU is running P1; P1 goes to do some I/O (e.g. a copy-paste). I/O may take a minute or two. Meanwhile the CPU should execute P2 instead of waiting.
- Less process starvation
  - Starvation: a process never gets a chance to run because another process is holding the CPU.
  - Example: CPU picks P1 first. P1 is a very long job, or a badly written program left in a `while(1)` infinite loop. P2 and P3 should not be denied the CPU forever just because of P1.
- Higher priority job execution
  - P1, P2, P3 are normal jobs executing turn by turn. A high-priority job P4 arrives; the OS should be able to set the others aside and run P4 at once.
  - Example: an antivirus is programmed so that as soon as a removable disk is inserted, a high-priority task arrives to scan it quickly, whatever else you are doing.

## Types of operating systems –

- Single process operating system [MS DOS, 1981]
- Batch-processing operating system [ATLAS, Manchester Univ., late 1950s – early 1960s]
- Multiprogramming operating system [THE, Dijkstra, early 1960s]
- Multitasking operating system [CTSS, MIT, early 1960s]
- Multi-processing operating system [Windows NT]
- Distributed system [LOCUS]
- Real time OS [ATCS]

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

- From the interview point of view, know all the names, and remember one example of each.
- The most important are single process, batch, multiprogramming, multitasking and multi-processing. Interviewers directly ask you to explain multiprogramming, multitasking and multi-processing, and people get confused between them.

**Single process OS**, only 1 process executes at a time from the ready queue. [Oldest]

- The simplest OS; the first OSes were of this type. No concept of multiple jobs at all.
- Example: P1, P2, P3 waiting. P1 executes first; only when P1's execution finishes does P2 get the CPU, then P3.
- Checking the goals:
  - Maximum CPU utilization: No. If P1 goes for I/O, P2 still gets no chance; the CPU sits idle.
  - Process starvation: Yes. If P1 is a huge, time-taking job (the `while(1)` example), P1 keeps executing and P2, P3 never get a chance.
  - High priority job execution: No. While P1 is executing, a high-priority job (e.g. the antivirus scan) cannot run until P1 finishes.
- Example: MS DOS.
- Why such an OS was built: development is incremental, and software requirements follow the hardware, never the other way round. The earliest hardware could handle only one process at a time, so the software was built the same way.

**Batch-processing OS**,

1. Firstly, user prepares his job using punch cards.
2. Then, he submits the job to the computer operator.
3. Operator collects the jobs from different users and sort the jobs into batches with similar needs.
4. Then, operator submits the batches to the processor one by one.
5. All the jobs of one batch are executed together.

- Priorities cannot be set, if a job comes with some higher priority.
- May lead to starvation. (A batch may take more time to complete)
- CPU may become idle in case of I/O operations.

```
(User 1) ──► [Job 1] ──┐
(User 2) ──► [Job 2] ──┼──► (Operator) ──►  Batch 2       Batch 1      ┌──────────────┐
   ⋮            ⋮      │                   ┌───────┐     ┌───────┐     │     CPU      │
(User n) ──► [Job n] ──┘                   │ Job 7 │     │ Job 4 │     │      +       │
                                           │ Job 5 │ ──► │ Job 1 │ ──► │      OS      │
                                           │ Job 2 │     └───────┘     │ User Program │
                                           └───────┘                   └──────────────┘
```

- Punch card: a physical paper card with many small circles; some circles are punched/filled and some are not, which stores binary information. The card is scanned and converted into digital information (like the magnetic strip on today's ATM/credit/debit card). The user brought his job to the computer in the form of a punch card.
- The operator (can be thought of as a piece of software) only looks at each job from the outside: what its requirements are. It cannot look inside a job to estimate how long it will take. It sorts the jobs by requirements in a brute-force way and divides them into batches of similar jobs (e.g. Batch 1 = Job 1, Job 4; Batch 2 = Job 2, Job 5, Job 7).
- Each batch is submitted to the CPU sequentially. Inside a batch the single CPU also works sequentially, like a single process OS: the OS gives Job 1 to the CPU, then Job 4. When Batch 1 completes, Batch 2 executes.
- Not much different from single process OS; the only optimisation is grouping jobs into batches.
- Checking the goals:
  - Maximum CPU utilization: No. If J1 in Batch 1 takes a long time in I/O, J4 just waits.
  - Process starvation: Yes. If J1 takes a long time, J4 keeps waiting. There is also batch starvation: if Batch 1 takes very long to execute, the later batches get no chance.
  - High priority job execution: No. A batch cannot start until the current batch completes; that is not allowed.
- Example: ATLAS.

**Multiprogramming** increases CPU utilization by keeping multiple jobs (code and data) in the **memory** so that the CPU always has one to execute in case some job gets busy with I/O.

- Single CPU
- Context switching for processes.
- Switch happens when current process goes to wait state.
- CPU idle time reduced.

- Ready queue: a queue (line data structure) holding all the jobs that are ready to be executed and only need the CPU to pick them up (J1, J2, J3, J4 …).
- Example: J1 goes for execution first (single CPU, so one job at a time). J1 gets a command to copy some data from a USB/pen drive, so it goes to do I/O. Until the I/O finishes, J1 cannot continue on the CPU. So J1 goes to the wait state until its I/O completes, and J2 is scheduled and starts executing, so the CPU does not stay idle.
- From this type onwards the goals start getting fulfilled. Multiprogramming, multitasking and multi-processing are frequently asked in interviews.
- Example: THE.

### Context switching

(Covered in detail later in process management.)

- Since there are many processes in memory and only one CPU, the CPU must switch from one process to another whenever a process goes to I/O or the wait state. This is done by context switching.
- Analogy: you are studying physics with all physics books and notes open on your table. At 11:00 you planned to switch to chemistry. You put bookmarks/pens where you are in each physics book (you will continue physics later), close them and keep them aside. Then you open the chemistry books at the bookmarks you left earlier and start studying. You saved the state of the physics material and restored the state of the chemistry material.
- Same with processes P1 and P2: the CPU is working on P1; P1 goes for I/O and P2 has to be brought into execution.
  - P1's current context (the position/address where it was executing, its call stack and the information on it) is saved in its PCB.
  - P2's information is taken from its PCB, P2's current state and stack are restored, and the CPU starts working on P2.
- This process of saving and restoring is called context switching.
- PCB (Process Control Block): a small data structure that stores information related to a process.

**Multitasking** is a logical extension of multiprogramming.

- Single CPU
- Able to run more than one task simultaneously.
- Context switching and time sharing used.
- Increases responsiveness.
- CPU idle time is further reduced.

- Multiprogramming and multitasking are similar: both have a single CPU and both use context switching. The deciding factor that makes multitasking better is time sharing.
- Problem with multiprogramming: a context switch happens only when a process goes to I/O or the wait state. A job that never goes for I/O keeps executing for a long time, and the other jobs can starve.
- Fix (time sharing): do not wait for I/O to trigger a context switch. Take a small time quantum, e.g. 100 ms. A job that has received its 100 ms has had one quantum of execution; stop it there and give the next job a chance.
- Example: P1, P2, P3 on one CPU. If a process goes for I/O, it still goes to wait and another gets the CPU (as in multiprogramming). If no process does I/O, P1 executes for 100 ms, then its execution is stopped right then and P2 gets 100 ms, then P3, and so on. Each process gets a little time in turn.
- Checking the goals:
  - Maximum CPU utilization: highest so far. The CPU is never idle; some job always gets the next 100 ms.
  - Process starvation: low. Even if P1 is a very heavy job, P2 gets an equal chance as soon as P1's time quantum ends.
  - High priority job execution: Yes. Context switching is available, so when a high-priority job (e.g. P4, antivirus scanning a USB drive) arrives, a software interrupt is raised, the running process is switched out and P4 gets the CPU immediately.
- Today's OSes that you use are multitasking: you run many apps, all of them feel responsive and none hangs, because time sharing is running.
- Example: CTSS.

**Multi-processing OS,** more than 1 CPU in a single computer.

- Increases reliability, 1 CPU fails, other can work
- Better throughput.
- Lesser process starvation, (if 1 CPU is working on some process, other can be executed on other CPU.

- Context switching and time sharing also apply here; the improvement is that the number of CPUs is greater than one.
- With multiple CPUs, CPU utilization can be even higher, more apps can run simultaneously, and starvation is reduced further.
- High priority job: if CPU 1 is busy, CPU 2 can run it.
- Modern CPUs: a CPU with 4 or 8 cores; 8 cores means 8 logical processors, i.e. it can be treated as 8 separate CPUs.
- Example: CPU 1 and CPU 2, processes P1, P2, P3, P4. P1 gets a time quantum on CPU 1, then P2; meanwhile P3 goes to CPU 2. Which job a CPU picks is decided by the OS through process scheduling algorithms (covered later).
- Reliability: in a single-CPU system, if that CPU fails (some hardware problem), the whole system goes down. Here, if CPU 1 fails, CPU 2 (and CPU 3 …) can still do the work.
- Interview recap: single process OS has a single processor; multiprogramming and multitasking also have a single processor; multi-processing has more than one processor, which increases throughput. Systems used today are multi-processing.
- Example: Windows.

**Distributed OS,**

- OS manages many bunches of resources, >=1 CPUs, >=1 memory, >=1 GPUs, etc
- **Loosely connected autonomous,** interconnected computer nodes.
- collection of independent, networked, communicating, and physically separate computational nodes.

- Also called a loosely coupled operating system.
- Until now there was one OS with one/many CPUs and one memory, all connected in a single box: one system. Here there are many CPUs and memories connected over a network: many separate computers (one at your home, one at mine, …) interconnected over the internet or a LAN, managed by one OS.
- Jobs P1, P2, P3, P4: the OS can send P1 to one machine, P2 to another, P3 and P4 to others.
- The nodes can have different configurations: one low-end, one high-end, one with a graphics card/GPU, one without.
- With so many resources, many jobs can be executed and there can be multiple users (U1, U2, …).
- Example: on LeetCode, when you press submit, your code runs on some Linux machine and is judged there. It is not one system but many; whichever one is free gets the job. The OS that manages such a set of computers connected over the internet is a distributed OS.
- Example: LOCUS.

**RTOS**

- **Real time** error free, computations within tight-time boundaries.
- Air Traffic control system, ROBOTS etc.

- RTOS = Real Time Operating System.
- Needed where there must be no chance of error: accuracy must be very high, even to many decimal places.
- Air traffic control (ATC): many flights in the air, and people's lives depend on the ATC's crucial duty. Computation must be error free and real time.
- Real time means execution must be very fast: a job given to the CPU must finish within seconds, i.e. within a certain deadline.
- Also used in industrial applications, e.g. the systems of a nuclear plant: highly demanding, error-free computation that must be done quickly within a deadline.
- Example: ATCS.
