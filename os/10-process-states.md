# Lecture 10: Process States | Process Queues

- **PCB field:** The PCB (previous lecture) has a field "Process state". It stores the current state of the process. This lecture expands that field.
- **Life cycle:** A process's life cycle runs from its creation (new) to its termination. On the way it passes through several states.

## 1. Process States

As a process executes, it changes state. Each process may be in one of the following states.

a. **New:** The OS is about to pick the program and convert it into a process, or the process is being created.
   - **PCB:** While the program is converted into a process (loaded from disk), the state field in its PCB says "new".

b. **Run:** Instructions are being executed. The CPU is allocated.
   - **PCB:** A process from the ready queue has been given the CPU and is executing. Its PCB state says "running".

c. **Waiting:** The process is waiting for IO.
   - **Cause:** While running, the process hits an I/O instruction and goes to the waiting state. It waits for the I/O to complete so it can continue.

d. **Ready:** The process is in memory, waiting to be assigned to a processor.
   - **Ready queue:** The process has been created and brought into memory. The area of memory where such processes sit is the ready queue.
   - **Needs only CPU:** It is ready for execution. It only needs the CPU. As soon as the CPU is scheduled to it, it runs.
   - **Many processes:** The ready queue can hold many processes at once. A multiprogramming OS keeps more than one process in the ready queue to increase the degree of multiprogramming.

e. **Terminated:** The process has finished execution. Its PCB entry is removed from the process table.
   - **Memory:** The process no longer exists in memory.

```mermaid
stateDiagram-v2
    direction LR
    new --> ready : admitted
    ready --> running : scheduler dispatch
    running --> ready : interrupt
    running --> waiting : I/O or event wait
    waiting --> ready : I/O or event completion
    running --> terminated : exit
```

Life cycle walkthrough (the diagram above):

1. **On disk:** Programs sit on disk. They are picked up and converted into processes. During this, the process is in the new state.
2. **Admitted:** Once fully created, the process is put in the ready state.
3. **Dispatch:** A separate OS module takes processes from the ready queue and dispatches the CPU to them (scheduler dispatch). The process is now running.
4. **While running:** One of three things happens.
   - **I/O:** The process goes for I/O. It moves to the waiting state.
   - **Time quantum expires:** This happens in time-sharing systems. The process goes back to the ready queue. This is handled as an interrupt. A software interrupt is generated: "P1, your time is up, come back".
   - **Finishes:** Its execution ends. It exits and is terminated.
5. **I/O completes:** A process whose I/O completes goes from waiting back to the ready queue.

Common doubt: after waiting (I/O), does the process go straight back to running?

- **No:** It first goes to the ready queue.
- **Then:** The scheduler gives it a chance again. This depends on its priority and the scheduling algorithm in use.

Example with P1, P2, P3 in the ready queue:

1. P3 is scheduled. It moves to the running state and leaves the ready queue.
2. P3 gets an I/O request. It moves to the waiting state. The CPU becomes free.
3. Within a fraction of a second, P2 is scheduled and starts executing. It leaves the ready queue.
4. P3 completes its I/O. It goes back into the ready queue, not to running, since P2 is executing.
5. P3 gets its chance again later.

## 2. Process Queues

| Queue | Holds | Location | Scheduler |
|-------|-------|----------|-----------|
| Job queue | Processes in new state | Secondary memory | Job scheduler (long-term scheduler, LTS) |
| Ready queue | Processes in ready state | Main memory | CPU scheduler (short-term scheduler, STS) |
| Waiting queue | Processes in wait state | | |

a. **Job queue:**
   1. Processes in new state.
   2. Present in secondary memory.
   3. **Job scheduler (long-term scheduler, LTS)** picks processes from the pool and loads them into memory for execution.
      - **The pool:** A large pool on disk holds many programs ready to be executed. The job scheduler picks them from disk, converts them to the new state, then puts them in the ready queue.
      - **Its work:** Moving processes from the job queue into the ready state is the job scheduler's work.

b. **Ready queue:**
   1. Processes in ready state.
   2. Present in main memory.
   3. **CPU scheduler (short-term scheduler, STS)** picks a process from the ready queue and dispatches it to the CPU.
      - **How:** It picks a process depending on the scheduling algorithm and priority.
      - **Its work:** Deciding which process goes from the ready state to the running state is the CPU scheduler's work.

c. **Waiting queue:**
   1. Processes in wait state.
      - **Example:** P1, P2, P3 are in the ready queue. P3 is scheduled, runs briefly, and goes for I/O. The CPU is free, so P2 is given the CPU. P2 also goes for I/O after a while. Now P2 and P3 are both doing I/O, and they wait in a queue. That queue is the waiting queue. P1 is scheduled next.

```
 Disk (pool)       Main memory                            CPU
┌───────────┐  LTS  ┌─────────────┐  STS (dispatch)  ┌─────────┐
│ Job queue │ ────► │ Ready queue │ ───────────────► │ Running │ ──► terminated
│ (new)     │       └─────────────┘ ◄─────────────── └─────────┘
└───────────┘             ▲           interrupt           │
                          │                               │ I/O
                          │      ┌───────────────┐        │
                          └───── │ Waiting queue │ ◄──────┘
                    I/O complete └───────────────┘
```

### Why "long-term" and "short-term" scheduler?

- **Names:** They depend on frequency. Frequency is how often each scheduler runs (the idle gap between two runs).
- **CPU scheduler is the short-term scheduler.** It works at very high frequency, with gaps of milliseconds.
  - **Example:** The CPU scheduler schedules P1. After only a few instruction cycles, P1 needs I/O and leaves. The CPU is now free.
  - **Why fast:** Suppose the CPU scheduler waited one minute before checking the ready queue again. The CPU would sit idle. The CPU must never sit idle.
  - **Minimal idle time:** After scheduling a job, it does not rely on that job. It keeps checking whether the CPU is free. As soon as it is, it picks another process (for example P3) and puts it in the running state.
- **Job scheduler is the long-term scheduler.** It is "lazy". The gap between its runs is larger.
  - **Example:** At t = 0 it puts 5 jobs into the ready queue. At t0 + 1 minute it checks again whether any new job has arrived to be put in the ready queue.

## 3. Degree of multi-programming

The degree of multi-programming is the number of processes in memory. It is how many processes can be in the ready queue at one time.

- **Example:** If only 5 processes can be in the ready queue at once, the degree of multiprogramming is 5.

a. **LTS** controls the degree of multi-programming.
   - **Why:** The LTS picks jobs from the pool (secondary storage) and puts them into the ready queue.

> **Interview:** "Who controls the degree of multiprogramming?" The answer is the LTS (long-term scheduler). This is a likely question.

## 4. Dispatcher

The **dispatcher** is the module of the OS that gives control of the CPU to a process selected by the **STS**.

- **Split of work:** The CPU scheduler (STS) decides which process to run. The dispatcher is the module that actually provides the CPU for it.
- **Why mentioned:** The term should be familiar when it appears in other texts.
