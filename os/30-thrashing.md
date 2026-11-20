# Lecture 30: Thrashing

- Thrashing builds on paging, virtual memory, swap space, page faults, page-fault service time and page replacement algorithms (lectures 26, 27, 28). A plain "What is thrashing?" in an interview tests all of that paging knowledge at once.
- Thrashing is a very likely question when the interviewer wants to discuss memory management.

1. **Thrashing**
   - Example: two RAMs, each with 6 frames.

     | Frame | Situation 1 | Situation 2 |
     |---|---|---|
     | 1 | P1 page 1 | P1 page 1 |
     | 2 | P1 page 2 | P2 page 1 |
     | 3 | P1 page 3 | P3 page 1 |
     | 4 | P2 page 1 | P4 page 1 |
     | 5 | P2 page 2 | P5 page 1 |
     | 6 | P2 page 3 | P6 page 1 |

   - Recap: a page fault happens when an instruction needs a page that is not in RAM. An interrupt goes to the OS, the page is brought from swap space and put in a free frame. If no frame is free, an already allocated page (e.g. P2 page 1) must be **swapped out**, and the new page is **swapped in**.
   - Page fault is pure overhead: while a page fault is being serviced, the CPU does no useful work (no process instruction executes).
   - Question: which situation has more page faults? **Situation 2.**
     - Situation 2 has the higher degree of multiprogramming (number of processes in memory): 6 processes vs only 2. Still, situation 1 performs better.
     - When a process starts, the page of its main code is loaded, along with the pages of the nearby code area. If only one page of a process is loaded, it finishes that page quickly and the request for page 2 causes a page fault; then page 3, and so on. Each fault = interrupt to OS + page-fault service time.
     - In situation 1, P1 has 3 pages loaded, so it runs for a while before it faults. By the time P3 needs a page, P1 and P2 may have finished, so their frames can be freed easily.
     - In situation 2, P1 faults right after its first page. To load more P1 pages, a page of another process (e.g. P5 page 1) must be swapped out, though it is still needed. Then P1 goes for I/O, P3 runs a little and faults again, and so on.
     - So in situation 2 the CPU is busier servicing page faults than executing processes: CPU cycles go to swap-in / swap-out, throughput drops, processes run very slowly.
     - Situation 1: fewer page faults, more throughput, higher CPU utilization. Situation 2: high degree of multiprogramming, but thrashing.
   1. If the process doesn’t have the number of frames it needs to support pages in active use, it will quickly page-fault. At this point, it must replace some page. However, since all its pages are in active use, it must replace a page that will be needed again right away. Consequently, it quickly faults again, and again, and again, replacing pages that it must bring back in immediately.
      - When a process is loaded, the OS should load some amount of its pages (say 5-6), not just one, so the code in active use around the current point is in RAM and fewer page faults occur.
      - Replacing a page means a swap-out and a swap-in. Both are slow because swap space is on disk, and disk access time is high.
      - "All its pages are in active use": every page in RAM (P2 page 1, P3 page 1, ...) is in use, so whichever one is replaced for P1 page 2 will be needed again right away. After a context switch, that process faults too, then the next one, and so on.
      - Example: P3 page 1 is swapped out to bring in P1 page 2. Next, P3 runs and needs P3 page 1, so it must be swapped in, which replaces another page in active use.
   2. This **high paging activity is called Thrashing.**
      - High paging activity = continuous swap-in / swap-out.
   3. A system is Thrashing when it **spends more time servicing the page faults than executing processes.**

      ```
      CPU utilization
        ^
        |                        |-------> thrashing
        |                  ___
        |             _.-'    '.
        |         _.-'          \
        |     _.-'               \
        | _.-'                    \__
        +-----------------------------------> degree of multiprogramming
                           ^
                           peak = thrashing point (λ)
      ```

      - Degree of multiprogramming = number of processes allocated in RAM (in the form of pages). In the example: 6 in situation 2, 2 in situation 1.
      - Low degree of multiprogramming gives low CPU utilization: with only 2 processes, if both go for I/O and no other process is in RAM, the CPU sits idle.
      - Increasing the degree of multiprogramming raises CPU utilization: with a 3rd process, the CPU runs P3 while P1 and P2 do I/O; if P3 also goes for I/O, it brings P4.
      - But the system has a peak (call it λ), the **thrashing point**. Beyond it thrashing starts and CPU utilization drops drastically. RAM is full of processes, but all of them are busy with page faults: each one that runs needs another page, servicing it evicts another process's page, that process later faults to get it back, and all time goes in swap-in / swap-out.
      - How it happens (the cycle):
        1. Initially CPU utilization is low.
        2. The system sees low CPU utilization and asks the long-term scheduler (LTS) for more processes, so more processes are loaded into RAM in the form of pages. CPU utilization rises, and the system keeps asking for more.
        3. A global page replacement algorithm replaces pages without regard to the process they belong to. To fit new processes, it keeps evicting some pages of the other processes into the swap area, until each process has only 2-3 pages (finally 1 page) in RAM and the rest is in swap area.
        4. A process may need more pages, so it page-faults again, and other processes' frames are replaced, though they may be needed soon. Those processes fault again in turn.
        5. Many page faults are generated, and requests queue up at the paging device (page fault of process 1, process 2, ...). The paging device's load keeps growing and the CPU does no useful work, so useful CPU utilization goes down.
        6. The CPU scheduler sees CPU utilization going down (processes are not executing, they are busy faulting) and increases the degree of multiprogramming again by bringing more processes.
        7. Finally the degree of multiprogramming is so high that CPU utilization drops drastically. At the thrashing point no useful work is done; all time goes in servicing page faults.
      - This graph is very important for interviews.
   4. Technique to Handle Thrashing
      1. **Working set model**
         1. This model is based on the concept of the **Locality** Model.
            - Locality = the local area of a process the code is currently working in, e.g. main and the functions near it. If main calls 5 functions, the pages of those 5 functions are also loaded into RAM.
         2. The basic principle states that if we allocate enough frames to a process to accommodate its current locality, it will only fault whenever it **moves to some new locality**. But if the allocated frames are lesser than the size of the current locality, **the process is bound to thrash.**
            - Page faults still happen, but fewer, because enough pages of the current locality are loaded.
            - Nature of code: it works in one particular locality for some time (moving to and fro inside it), then moves to another locality. So load the current locality; a page fault then comes only on entering a new locality.
            - Example: the current locality is 5 pages, but only 2 frames are allocated, so page faults are many and the process thrashes.
            - Working set model rule: always allocate a process enough frames that its current locality is loaded.
            - This model tries to stop thrashing from happening at all, by allocating enough frames from the start.
      2. **Page Fault frequency**
         - Here the page-fault rate is treated as a tuning parameter: observe it closely and push it up or down.
         1. **Thrashing** has a high page-fault rate.
         2. We want to **control** the page-fault rate.
         3. When it is too high, the process needs more frames. Conversely, if the page-fault rate is too low, then the process may have too many frames.
            - Too high: e.g. situation 2, one frame per process. Give P1 more frames and its page-fault frequency decreases.
            - Too low: extreme case, whole processes are loaded (e.g. 2 complete processes). Then there are no page faults, but the degree of multiprogramming is very low, so more processes could be loaded. Paging exists so that processes are split into small pages and only some pages of each are loaded, to raise the degree of multiprogramming.
            - So take frames away from such a process (its pages go to the swap area) to accommodate pages of other processes.
         4. We establish upper and lower bounds on the desired page fault rate.
         5. If pf-rate exceeds the upper limit, allocate the process another frame, if pf-rate fails falls below the lower limit, remove a frame from the process.
            - Above the upper limit (thrashing has started): give the process more frames, i.e. grow its locality in RAM. To make room, other processes may have to be swapped out fully to the swap area by the medium-term scheduler (put in wait state, not executing for now).
            - Below the lower limit (almost no page faults): take frames back from that process, swap those pages out, and give the frames to new processes. This raises the degree of multiprogramming.
         6. By controlling pf-rate, thrashing can be prevented.

         ```
         page-fault rate
           ^
           |\
           | \
           |  \   increase number of frames
           |---\------------------------------- upper bound
           |    '.
           |      '-._
           |          '--.__
           |----------------'''---.___--------- lower bound
           |                decrease number of frames
           +-------------------------------------> number of frames
         ```

         - Few frames for a process (e.g. 1 page per process) means a very high page-fault rate. If it crosses the upper bound, increase that process's number of frames and bring in its current locality.
           - Example: 6 processes with 1 page each become 4 processes with 3 frames each (the other processes swapped out fully). The page-fault rate decreases.
         - Between the two bounds the page-fault rate is fine.
         - If a process has so many frames that it barely page-faults (below the lower bound), remove frames from it (e.g. take back 2-3 frames from several processes and swap those pages out). This frees RAM to accommodate more processes and raise the degree of multiprogramming.
         - Aim: keep the page-fault rate in the middle band. Both ends give low CPU utilization:
           - Too many page faults: thrashing, CPU time goes in servicing page faults.
           - Too few page faults: too many frames per process, so few processes in RAM (low degree of multiprogramming); if those few all go for I/O, the CPU sits idle.
      - Page faults, degree of multiprogramming, number of frames allocated and thrashing are all related. Paging was used to raise the degree of multiprogramming; its side effect is page faults, which must be serviced; we want neither too many nor too few.

- After memory management (this was its last topic) comes storage management, which has low priority for interviews (hard disk design, sectors, etc.; SSDs are used anyway). Only "files and directories" (how files are managed) is somewhat important; it is left for self-study and not covered in this course. Most interview questions come from memory management.
