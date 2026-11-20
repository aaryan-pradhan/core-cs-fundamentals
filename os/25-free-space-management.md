# Lecture 25: Free Space Management

Context: previous lecture covered contiguous memory allocation (fixed partitioning and dynamic partitioning) and how a logical address is mapped to a physical address. This lecture: how the OS manages the free space in physical memory when it allocates and frees memory.

Running example (dynamic partitioning, 16KB RAM):

- OS occupies 0 to 4KB. Initially 4KB to 16KB (12KB) is free.
- P1 requests 2KB, gets exactly 2KB (4 to 6KB). Allocating exactly as per need = dynamic partitioning.
- P2 requests 8KB, gets 6 to 14KB.
- P3 requests 2KB, gets 14 to 16KB. RAM is now full.
- After some time P1 and P3 exit. Their chunks (4 to 6KB and 14 to 16KB) become free; P2 is still allocated.
- A new P4 asking for 2KB can be put in one of these 2KB free chunks.

```
 Initial          After P1,P2,P3     After P1, P3 exit
+--------+ 0      +--------+ 0       +--------+ 0
|   OS   |        |   OS   |         |   OS   |
+--------+ 4      +--------+ 4       +--------+ 4
|        |        |   P1   |         |  free  |  2KB
|  free  |        +--------+ 6       +--------+ 6
|  12KB  |        |   P2   |         |   P2   |  8KB
|        |        |  8KB   |         |        |
|        |        +--------+ 14      +--------+ 14
|        |        |   P3   |         |  free  |  2KB
+--------+ 16     +--------+ 16      +--------+ 16
```

1. **Defragmentation/Compaction**
   a. Dynamic partitioning suffers from external fragmentation.
      - In the example above (P1, P3 exited), P4 comes and needs 3KB. Total free memory is 4KB, but it is two separate 2KB chunks, not contiguous. The OS walks the free list: 2KB node, cannot fit; next 2KB node, cannot fit; reaches NULL. Request fails.
      - Free space is available but scattered (fragmented) here and there, so a process that fits in the total cannot be allocated. This is external fragmentation.
   b. Compaction to minimize the probability of external fragmentation.
      - It only minimizes the probability; it does not remove fragmentation fully (in the example, 1KB is still left over after P4 is placed).
   c. All the free partitions are made contiguous, and all the loaded partitions are brought together.
      - "Loaded" means allocated. A kind of sorting: all free space moves to one side, all allocated space to the other side.
      - The OS physically shifts the live data of allocated processes. In the example, P2 (8KB at 6 to 14KB) is shifted 2KB down: start 6 moves to 4, end 14 moves to 12. Free space becomes one contiguous 4KB block (12 to 16KB).

        ```
         Fragmented RAM     Defragmented RAM    After P4 (3KB)
        +--------+ 0        +--------+ 0        +--------+ 0
        |   OS   |          |   OS   |          |   OS   |
        +--------+ 4        +--------+ 4        +--------+ 4
        |  free  |          |   P2   |          |   P2   |
        +--------+ 6        |  8KB   |          |  8KB   |
        |   P2   |          |        |          |        |
        |  8KB   |          +--------+ 12       +--------+ 12
        |        |          |  free  |          |   P4   |
        +--------+ 14       |  4KB   |          +--------+ 15
        |  free  |          |        |          |  free  | 1KB
        +--------+ 16       +--------+ 16       +--------+ 16
        ```

      - The OS keeps watching how much fragmentation there is. When it goes above some percentage (many small chunks), a kernel program runs and defragments the RAM.
      - Does the shifting corrupt or disturb a running user process? No. The user process works in its logical address space; only the physical address changes. The OS just updates the relocation (base) register: P2's base changes from 6 to 4, the limit stays 8. The logical address space is still 0 to 8KB. The abstraction the OS provides hides this from the user program.
      - After compaction the free list has one 4KB node (the two 2KB nodes were shifted together and merged since their addresses are contiguous). Now the 3KB request of P4 succeeds; free list becomes one 1KB node.
   d. By applying this technique, we can store the bigger processes in the memory. The free partitions are merged which can now be allocated according to the needs of new processes. This technique is also called **defragmentation**.
   e. The efficiency of the system is decreased in the case of compaction since all the free spaces will be transferred from several places to a single place.
      - Defragmentation itself is time consuming; it is an overhead. While it runs, the CPU is busy defragmenting, so user processes cannot work.
      - The example used 2KB chunks; real RAM is large (e.g. 16GB) with many small holes, so moving everything together has high time complexity.
      - Same idea on disk: a hard disk (C drive, D drive on a Windows PC) also gets fragmented after installing/deleting lots of programs and games, so disk access, copy, paste and delete become slow. Windows provides a defragmentation tool for drives (right click the drive, Properties).

2. **How free space is stored/represented in OS?**
   a. Free holes in the memory are represented by a free list (Linked-List data structure).
      - Can be any linked list (singly, doubly). Each node is one free chunk and stores its starting address (and size).
      - Free list through the running example:

        | RAM state | Free list |
        |---|---|
        | Initial | [start 4KB, 12KB] -> NULL |
        | After P1 | [10KB] -> NULL |
        | After P2 | [2KB] -> NULL |
        | After P3 (RAM full) | NULL (nothing is free) |
        | After P1, P3 exit | [2KB] -> [2KB] -> NULL |

      - The two 2KB chunks get separate nodes because they are not contiguous (far apart in memory).
      - If P2 also exits, an 8KB free node comes between them. The OS checks the addresses, sees they are contiguous, and merges all of them into a single 12KB node.
      - On every allocation the OS iterates this list to find which memory area is free.

3. **How to satisfy a request of a of n size from a list of free holes?**
   - Example: free list 50KB -> 30KB -> 10KB -> 5KB -> NULL (4 free holes). P4 requests 20KB. It cannot go in 10KB or 5KB, but it can go in either 50KB or 30KB. Which one to choose is decided by an algorithm.
   - Examples below use free list 50KB -> 100KB -> 90KB -> 200KB -> 50KB -> NULL and a request of 90KB (P1).

   a. Various algorithms which are implemented by the Operating System in order to find out the holes in the linked list and allocate them to the processes.
   b. **First Fit**
      i. Allocate the first hole that is big enough.
         - 50KB is too small; 100KB is the first hole big enough, so 90KB is allocated there and 10KB stays free. Free list becomes 50 -> 10 -> 90 -> 200 -> 50.
      ii. Simple and easy to implement.
         - Just iterate and take the first block that is big enough; no comparisons.
      iii. Fast/Less time complexity
         - Usually does not iterate the whole list. Worst case is still O(n) (the only fitting hole may be the last node).
   c. **Next Fit**
      i. Enhancement on First fit but starts search always from last allocated hole.
         - First 90KB request goes to the 100KB hole (same as first fit), leaving 10KB.
         - Next request (P2, 10KB) does not search from the start of the list; it starts from the position where the last allocation happened and moves forward from there.
         - Only extra thing over first fit: a pointer to the last allocation point must be saved. It is a tweak of first fit.
      ii. Same advantages of First Fit.
   d. **Best Fit**
      i. Allocate smallest hole that is big enough.
         - For 90KB, look for the hole just bigger than (or equal to) the request. 90KB hole leaves 0KB, the smallest leftover, so P1 goes there and that node is removed from the free list.
      ii. Lesser internal fragmentation.
         - Leaves the least space unused in the chosen hole.
      iii. May create many small holes and cause major external fragmentation.
         - E.g. an 85KB process placed in a 90KB hole leaves 5KB. With many such allocations, the free list becomes 2KB -> 3KB -> 5KB -> 1KB. A 7KB request fails even though total free space is more than 7KB, because no single contiguous hole is 7KB.
      iv. Slow, as required to iterate whole free holes list.
         - Either sort the list by size or iterate the whole list (the best hole may be at the end).
   e. **Worst Fit**
      i. Allocate the largest hole that is big enough.
         - For 90KB, iterate and find the largest hole, 200KB (if a 300KB hole existed, it would be used). The first 90KB of it is allocated; the remaining 110KB stays in the free list.
         - Aim: leave the largest possible leftover space (greedy).
      ii. Slow, as required to iterate whole free holes list.
         - The largest hole may be at the end of the list.
      iii. Leaves larger holes that may accommodate other processes.
         - Opposite of best fit: lesser external fragmentation, since big leftover holes can still take other (even big) processes.

   - These algorithms are mostly used in contiguous allocation. Non-contiguous allocation is the next lecture.
