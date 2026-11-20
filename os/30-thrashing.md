# Lecture 30: Thrashing

- **Builds on:** Thrashing builds on paging, virtual memory, swap space, page faults, page-fault service time and page replacement algorithms (lectures 26, 27, 28).

> **Interview:** A plain "What is thrashing?" tests all of that paging knowledge at once. Thrashing is a very likely question when the interviewer wants to discuss memory management.

1. **Thrashing**
   - **Example:** Two RAMs, each with 6 frames.

     | Frame | Situation 1 | Situation 2 |
     |---|---|---|
     | 1 | P1 page 1 | P1 page 1 |
     | 2 | P1 page 2 | P2 page 1 |
     | 3 | P1 page 3 | P3 page 1 |
     | 4 | P2 page 1 | P4 page 1 |
     | 5 | P2 page 2 | P5 page 1 |
     | 6 | P2 page 3 | P6 page 1 |

   - **Recap:** A page fault happens when an instruction needs a page not in RAM. The page is brought from swap space into a free frame. If no frame is free, an allocated page (for example P2 page 1) is **swapped out** and the new page is **swapped in**.
   - **Pure overhead:** While a page fault is serviced, the CPU does no useful work.
   - **Question:** Which situation has more page faults? **Situation 2.**
     - **Degree of multiprogramming:** Situation 2 has the higher degree (number of processes in memory): 6 processes against only 2. Still, situation 1 performs better.
     - **Loading:** A starting process loads its main code page and nearby pages. With only one page loaded, it finishes that page quickly. Page 2 then faults, then page 3, and so on. Each fault costs an interrupt plus page-fault service time.
     - **Situation 1:** P1 has 3 pages loaded, so it runs a while before it faults. By the time P3 needs a page, P1 and P2 may have finished, so their frames are freed easily.
     - **Situation 2:** P1 faults right after its first page. Another process's page (for example P5 page 1) must be swapped out, though still needed. Then P1 goes for I/O, P3 runs a little and faults, and so on.
     - **CPU time:** In situation 2 the CPU services page faults more than it executes processes. Throughput drops and processes run very slowly.
     - **Summary:** Situation 1 has fewer page faults, more throughput and higher CPU utilization. Situation 2 has a high degree of multiprogramming, but thrashing.
   1. If a process does not have the frames it needs for its pages in active use, it quickly page-faults. All its pages are in active use, so it replaces a page that will be needed again right away. So it faults again, and again, and again.
      - **Load enough pages:** The OS should load some pages (say 5-6) of a process, not just one. Then the code in active use is in RAM and fewer faults occur.
      - **Slow replacement:** A replacement is a swap-out plus a swap-in. Both are slow because swap space is on disk.
      - **"All its pages are in active use":** Every page in RAM (P2 page 1, P3 page 1, ...) is in use. So whichever page is replaced for P1 page 2 is needed again right away. After a context switch, that process faults too, then the next one.
      - **Example:** P3 page 1 is swapped out for P1 page 2. P3 then runs and needs P3 page 1, which replaces another page in active use.
   2. This **high paging activity is called Thrashing.**
      - **High paging activity:** Continuous swap-in and swap-out.
   3. A system is thrashing when it **spends more time servicing page faults than executing processes.**

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

      - **Degree of multiprogramming:** It is the number of processes in RAM (as pages). In the example it is 6 in situation 2 and 2 in situation 1.
      - **Low degree:** It gives low CPU utilization. With only 2 processes, if both go for I/O, the CPU sits idle.
      - **Raising the degree:** It raises CPU utilization. With a 3rd process, the CPU runs P3 while P1 and P2 do I/O. If P3 also goes for I/O, it brings P4.
      - **Thrashing point:** The system has a peak (call it λ), the **thrashing point**. Beyond it CPU utilization drops drastically. RAM is full of processes, but all are busy with page faults. Servicing one process evicts another process's page, which faults later to get it back. All time goes in swap-in and swap-out.
      - **How it happens (the cycle):**
        1. Initially CPU utilization is low.
        2. The system asks the long-term scheduler (LTS) for more processes, loaded into RAM as pages. CPU utilization rises, and the system keeps asking for more.
        3. A global page replacement algorithm replaces pages without regard to the owning process. To fit new processes, it keeps evicting other processes' pages to the swap area, until each process has only 2-3 pages (finally 1 page) in RAM.
        4. A process needing more pages faults again. Other processes' frames are replaced, though they may be needed soon. Those processes fault in turn.
        5. Page fault requests queue up at the paging device (process 1, process 2, ...). Its load keeps growing and the CPU does no useful work.
        6. The CPU scheduler sees CPU utilization going down (processes are busy faulting). It increases the degree of multiprogramming again by bringing more processes.
        7. Finally the degree is so high that CPU utilization drops drastically. At the thrashing point all time goes in servicing page faults.
      - > **Interview:** This graph is very important.
   4. Techniques to handle thrashing
      1. **Working set model**
         1. This model is based on the **Locality** model.
            - **Locality:** It is the area of a process the code is currently working in, for example main and the functions near it. If main calls 5 functions, their pages are also loaded into RAM.
         2. The basic principle: if we allocate enough frames to a process to hold its current locality, it faults only when it **moves to some new locality**. If the allocated frames are fewer than the size of the current locality, **the process is bound to thrash.**
            - Page faults still happen, but fewer.
            - **Nature of code:** Code works in one locality for some time (moving to and fro inside it), then moves to another. A fault then comes only on entering a new locality.
            - **Example:** The current locality is 5 pages, but only 2 frames are allocated. Page faults are many and the process thrashes.
            - **Rule:** Always allocate enough frames to hold the current locality.
            - **Goal:** It tries to stop thrashing from the start.
      2. **Page fault frequency**
         - The page-fault rate is a tuning parameter to push up or down.
         1. **Thrashing** has a high page-fault rate.
         2. We want to **control** the page-fault rate.
         3. When it is too high, the process needs more frames. When it is too low, the process may have too many frames.
            - **Too high:** For example situation 2, with one frame per process. Give P1 more frames and its page-fault frequency decreases.
            - **Too low:** In the extreme case, whole processes are loaded (for example 2 complete processes). There are no page faults, but the degree of multiprogramming is very low. Paging exists to load only some pages of each process and raise the degree.
            - So take frames away from such a process (its pages go to the swap area) for other processes.
         4. We establish upper and lower bounds on the desired page fault rate.
         5. If the pf-rate exceeds the upper limit, allocate the process another frame. If the pf-rate falls below the lower limit, remove a frame from the process.
            - **Above the upper limit:** Thrashing has started. Give the process more frames to grow its locality in RAM. To make room, the medium-term scheduler may swap other processes fully out to the swap area (wait state, not executing for now).
            - **Below the lower limit:** There are almost no page faults. Take frames back, swap those pages out, and give the frames to new processes. This raises the degree of multiprogramming.
         6. By controlling the pf-rate, thrashing can be prevented.

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

         - **Few frames:** With few frames per process (for example 1 page per process), the page-fault rate is very high. If it crosses the upper bound, increase that process's number of frames and bring in its current locality.
           - **Example:** 6 processes with 1 page each become 4 processes with 3 frames each (the other processes swapped out fully). The page-fault rate decreases.
         - **Between the bounds:** The page-fault rate is fine.
         - **Many frames:** If a process barely page-faults (below the lower bound), remove frames from it (for example take back 2-3 frames from several processes and swap those pages out). This frees RAM for more processes.
         - **Aim:** Keep the page-fault rate in the middle band. Both ends give low CPU utilization:
           - **Too many page faults:** Thrashing. CPU time goes in servicing page faults.
           - **Too few page faults:** Too many frames per process, so few processes are in RAM. If those all go for I/O, the CPU sits idle.
      - **Everything is related:** Page faults, degree of multiprogramming, frames allocated and thrashing are related. Paging raises the degree of multiprogramming. Its side effect is page faults. We want neither too many nor too few.

- **What comes next:** Memory management was the last topic of this part. After it comes storage management, which has low priority for interviews (hard disk design, sectors, etc.; SSDs are used anyway). Only "files and directories" (how files are managed) is somewhat important. It is left for self-study and is not covered in this course. Most interview questions come from memory management.
