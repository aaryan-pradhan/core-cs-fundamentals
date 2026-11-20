# Lecture 28: What is Virtual Memory? || Demand Paging || Page Faults

1. **Virtual memory** lets processes run without being completely in memory. It gives the user an illusion of a very big main memory. It does this by treating a part of secondary memory as main memory (swap space).
   - **Recap:** RAM holds the physical address space. Each process has its own logical address space, divided into pages. RAM is divided into frames.
   - **Problem without virtual memory:** Every page of every process is loaded.
     - RAM = 12KB and page size = 1KB, so 12 frames.
     - P1 = 6KB gets 6 frames. P2 = 5KB gets 5 frames. 1 frame is free.
     - P3 = 5KB needs 5 free frames, so it cannot be allocated. A 12KB RAM runs only 2 processes.
   - **Real PCs:** A 16GB RAM runs the OS, background programs, a music player and GTA 5 (a 30-40GB game) together. The game does not fit in RAM, yet it runs. Virtual memory makes this work.
   - **Why:** RAM is small (16GB, 32GB) and costly. Disk is huge (1TB, 2TB). Programs are often bigger than RAM.
   - **Idea:** When a process becomes ready or running, allocate frames to only the pages needed right now.
     - A process never uses all its code at once. Execution starts at `main`, then a few functions are called. Maybe only 3 pages are in use.
     - Some code (for example some `switch` cases for user input) may never execute. Those pages are never needed.
   - **Same example with only needed pages loaded:**
     - P1 needs 3 pages, P2 needs 1 and P3 needs 2. Only 6 frames are used, so 6 are free.
     - P4 (3KB, all 3 pages needed) arrives and is also allocated.
     - Loading only the needed pages (and pages near them) uses **locality of reference**.
   - **Where do the not-needed pages go?**
     - The OS reserves a small area of the disk (for example 1GB of a 1TB disk). The user does not notice.
     - The not-needed pages of every process are stored there. No user program can touch it.
     - This reserved area (not the whole disk) is the **swap space**.
   - **The trick:** The user thinks all pages are in RAM. Only the needed pages are. The rest are in swap space.
   - **Access to a missing page:** When P1 reaches its 3rd page, the CPU assumes the page is in RAM. The OS knows it is not. A trap (exception) is raised, and the OS loads the page into RAM.
     - The OS finds a free frame. If all frames are full, it frees a frame whose page is not needed now (for example P1's page 0).
     - **Swap in:** Bring a needed page from swap space into RAM.
     - **Swap out:** Move a not-needed page from RAM to swap space.
   - **Total:** P1 6KB + P2 5KB + P3 5KB + P4 3KB = 19KB run in a 12KB RAM.
   - **GTA 5:** It is 30GB on 16GB RAM. Only the important related pages (say 3-4GB) stay in RAM. The game runs by swapping pages in and out.
   - **RAM + swap space together form the virtual memory arrangement.** Both together behave like one big RAM. That big RAM does not really exist, so it is called virtual memory.
     - From the user's view, RAM is 12KB + 1GB of swap space. The swap area works as RAM stored on the disk.
2. **Advantage:** Programs can be larger than physical memory.
   - **Example:** A single process P5 is 20KB (20 pages). Even with the whole 12KB RAM empty, 20 frames cannot be given. The OS finds the needed pages (say the first 5), allocates 5 free frames and runs the process.
3. Instructions must be in physical memory to execute. This limits a program to the size of physical memory. But often the entire program is not needed at once. Running a partially loaded program gives benefits:
   1. A program is no longer limited by the available physical memory.
   2. Each program takes less physical memory, so more programs run at once. This **increases CPU utilization and throughput.**
      - Many processes fit (a higher degree of multiprogramming). If one process goes for I/O, the CPU goes to another at once.
   3. It benefits **both the system and the user.**
      - **User:** Can run a program bigger than physical memory.
      - **System:** Gets more CPU utilization and throughput.
4. The programmer gets a very large virtual memory when only a smaller physical memory is available.
   - A programmer does not have to limit a program to 1GB because the PC has 1GB RAM. A 10GB program can be written. The OS keeps the needed pages in RAM and the rest in the swap area. It swaps pages in and out as needed.
5. **Demand Paging** is a popular method of **virtual memory management.**
   - It is the popular way to implement the scheme above. Pages are loaded on demand.
6. In demand paging, the least used pages of a process are stored in secondary memory.
7. A page is copied to main memory when it is demanded, which is when a **page fault** occurs. **Page replacement algorithms** decide which pages get replaced.
   - **Page fault:** P1's 3rd page is loaded only when the CPU demands it. The demand sends an interrupt to the OS, called a **page fault**. The page is in the swap area, so it must be swapped in.
   - **Full RAM:** If RAM is full, the OS must decide which page to swap out to swap space. This mechanism is the page replacement algorithm (covered in the next lecture).
8. Rather than swapping the entire process into memory, we use a **Lazy Swapper.** It never swaps a page into memory unless that page will be needed.
   - At the start, the OS swaps in only the page containing `main`. The rest stays in the backing store (swap space). Pages are swapped in on a need basis (demand paging).
9. We view a process as a sequence of pages, not one large contiguous address space. So the term **swapper is technically incorrect**. A swapper manipulates entire processes. A **Pager** is concerned with individual pages of a process.
   - **Swapper:** The Medium-Term Scheduler (MTS) swaps a whole process out to the swap area when the degree of multiprogramming gets too high.
   - **Pager:** Here only some pages of a process move, never the whole process.
10. **How Demand Paging works?**
    1. When a process is swapped in, the pager guesses which pages will be used.
       - **Example:** The pager guessed that 3 pages of P1 will be used.
    2. The pager brings only those pages into memory. This avoids reading **into memory pages that will not be used anyway.**
       - Code on the 5th page may never be accessed in the whole run. No frame is given to it.
       - **GTA 5 example:** The city map has many areas. If you play only in the north-west area, only that area's pages are loaded. If you never drive to the south-west area, its pages are never loaded.
    3. This way, the **OS decreases the swap time and the amount of physical memory needed.**
    4. The **valid-invalid bit scheme in the page table** distinguishes pages in memory from pages on the disk.
       - It is one more column in the page table. It tells how many pages of P1 are in RAM and how many are in the swap area.
       1. Valid-invalid bit **1** means the page is both legal and in memory.
          - **Legal:** The address belongs to the logical address space of that same process (isolation, memory protection).
          - **In memory:** The page is in actual RAM.
       2. Valid-invalid bit **0** means the page is not valid (not in the LAS of the process), or it is valid but currently on the disk.
          - **On the disk:** The page is in the swap area.
    5. **Page table when some pages are not in memory**

       Logical memory (LAS of 8 pages, A to H) and its page table:

       | Page | Content | Frame | Valid-invalid bit |
       |------|---------|-------|-------------------|
       | 0 | A | 4 | 1 |
       | 1 | B |   | 0 |
       | 2 | C | 6 | 1 |
       | 3 | D |   | 0 |
       | 4 | E |   | 0 |
       | 5 | F | 9 | 1 |
       | 6 | G |   | 0 |
       | 7 | H |   | 0 |

       Physical memory (frames 0-15): frame 4 = A, frame 6 = C, frame 9 = F, other frames not used by this process.

       Swap space: B, D, E, G, H.

       - **Bits:** Pages in RAM (A, C, F) have bit 1. The rest have bit 0 and lie in the swap area.
       - **Together:** The page table, physical memory and swap area tell the system where a page is.
       - **Example:** The process needs page E (page 4). Its bit is 0, so it is in the swap area. The OS puts E in a free frame (say frame 14), sets page 4's entry to frame 14 and its bit to 1.
    6. If a process never accesses a page with an invalid bit, **it executes successfully without the pages present in the swap space.**
    7. Access to a page marked invalid causes a **page fault.** The paging hardware notices the invalid bit and causes **a trap to the OS.**
    8. **The procedure to handle the page fault:**
       1. Check an internal table (in the PCB of the process) to see whether the reference was valid or an invalid memory access.
       2. If the reference was invalid, the process throws an exception.
          If it is valid, the pager swaps in the page.
          - **Invalid reference:** The address does not belong to this process at all (for example the program added too much to an address and it went into another process's space). A trap or exception is raised.
       3. Find a free frame (from the free-frame list).
       4. Schedule a disk operation to read the desired page into the new frame.
       5. When the disk read is complete, modify the page table to say the page is in memory.
       6. Restart the instruction that the trap interrupted. The process can now access the page as though it had always been in memory.
    9. **Steps in handling a page fault**

       ![Steps in handling a page fault](img/lec-28-page-fault-steps.png)

       - **Start:** The CPU generates a logical address (instruction `load M`). Page M is in the swap space.
       - **(1) Reference:** Look up page M in the page table. Its bit is 0, so the page is not in any frame.
       - **(2) Trap:** An exception goes to the OS. The OS checks the address. It is valid.
       - **(3) Page is on backing store:** The OS locates the page in the swap space and schedules a disk read.
       - **(4) Bring in missing page:** A free frame is found from the free-frame list, and page M is loaded into it.
       - **(5) Reset page table:** Write the frame number (for example frame 2) in page M's entry and set its bit to 1.
       - **(6) Restart instruction:** The instruction that caused the trap runs again.
       - **Hidden from the user:** All this runs in the background. It looks as if the whole program was always in RAM.
    10. **Pure Demand Paging**
        1. In the extreme case, a process starts with no pages in memory. The OS sets the instruction pointer to the first instruction, which is not in memory. The process immediately faults, and the page is brought in.
           - All pages of P1 start in the swap area. When `main` executes, a page fault loads that page. Soon the second page is needed, so another page fault occurs, and so on.
        2. Never bring a page into memory until it is required.
        - **Problem:** Many page faults happen initially. Disk access is slower than RAM, so each swap is a costly overhead. So pure demand paging is not good in practice.
    11. We use **locality of reference** to get reasonable performance from demand paging.
        - The pager also loads pages it expects to be needed: not just `main`, but also the pages of the 3-4 functions called inside `main`. An algorithm behind the pager decides this.
        - Related pages load together, so there are fewer page faults.
11. **Advantages of Virtual memory**
    1. The degree of multiprogramming increases.
       - With 12KB RAM and all pages loaded, only P1 (6KB) + P2 (5KB) = 11KB fit, and P3 could not be loaded. Loading only some pages of each lets more processes run.
    2. The user can run large apps with less real physical memory.
       - A single 19KB process cannot run in 12KB RAM normally. With virtual memory, if only 2 pages (1KB each) are needed, only those 2 are loaded and the other 17 stay in the swap area.
12. **Disadvantages of Virtual Memory**
    1. The system can become slower, because swapping takes time.
       - If many pages of many programs are in the swap area, swap in and swap out happen again and again. Disk is slow, so lag is felt while multitasking.
       - The best way to get a high degree of multiprogramming is more RAM. RAM is expensive and not everyone can afford it, so the OS gives virtual memory.
    2. **Thrashing** may occur.
       - Thrashing is covered in the next lecture.

> **Interview:** Questions from this lecture:
> - What is a page fault?
> - Where are page replacement algorithms needed?
> - What is a lazy swapper, and why is the term pager, not swapper?
> - How does demand paging work?
> - What is the valid-invalid bit in the page table?
> - How is a page fault handled, and how is the page table reset?
> - What is pure demand paging?
> - What is locality of reference?
