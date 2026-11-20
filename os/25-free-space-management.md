# Lecture 25: Free Space Management

This lecture covers how the OS manages free space in physical memory when it allocates and frees memory.

## Running example

Dynamic partitioning, 16KB RAM.

- **OS:** It occupies 0 to 4KB. Initially 4KB to 16KB (12KB) is free.
- **P1:** It requests 2KB and gets exactly 2KB (4 to 6KB). Allocating exactly as per need is dynamic partitioning.
- **P2:** It requests 8KB and gets 6 to 14KB.
- **P3:** It requests 2KB and gets 14 to 16KB. RAM is now full.
- **Exit:** After some time P1 and P3 exit. Their chunks (4 to 6KB and 14 to 16KB) become free. P2 is still allocated.
- **P4:** A new P4 asking for 2KB can be put in one of these 2KB free chunks.

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

## 1. Defragmentation/Compaction

a. Dynamic partitioning suffers from external fragmentation.
   - **Example:** P1 and P3 have exited. P4 needs 3KB. Total free memory is 4KB, but it is two separate 2KB chunks. The OS walks the free list. Neither 2KB node fits. It reaches NULL. The request fails.
   - **Meaning:** Free space is scattered, so a process that fits in the total cannot be allocated. This is external fragmentation.

b. Compaction minimizes the probability of external fragmentation.
   - It only minimizes the probability. It does not remove fragmentation fully. In the example, 1KB is still left over after P4 is placed.

c. All the free partitions are made contiguous, and all the loaded partitions are brought together.
   - **Loaded:** It means allocated. It is a kind of sorting: free space moves to one side, allocated space to the other.
   - **Shifting:** The OS physically shifts the live data of allocated processes. In the example, P2 (8KB at 6 to 14KB) is shifted 2KB down. Start 6 moves to 4, and end 14 moves to 12. Free space becomes one contiguous 4KB block (12 to 16KB).

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

   - **When it runs:** The OS keeps watching how much fragmentation there is. When it goes above some percentage (many small chunks), a kernel program runs and defragments the RAM.
   - **Does shifting disturb a running process?** No. The process works in its logical address space. Only the physical address changes. The OS updates the relocation (base) register. P2's base changes from 6 to 4, and the limit stays 8. The logical address space is still 0 to 8KB.
   - **Free list after compaction:** It has one 4KB node. The two 2KB nodes were shifted together and merged, since their addresses are contiguous. Now the 3KB request of P4 succeeds, and the free list becomes one 1KB node.

d. With this technique, bigger processes can be stored in memory. The free partitions are merged, so they can be allocated to the needs of new processes. This technique is also called **defragmentation**.

e. Compaction decreases the efficiency of the system, since all the free spaces are transferred from several places to a single place.
   - **Overhead:** Defragmentation is slow. The CPU is busy defragmenting, so user processes cannot work.
   - **Scale:** Real RAM is large (for example 16GB) with many small holes, so moving everything has high time complexity.
   - **Same on disk:** A hard disk (C drive, D drive on a Windows PC) also gets fragmented after installing and deleting many programs and games. Access, copy, paste and delete become slow. Windows has a defragmentation tool for drives (right click the drive, Properties).

## 2. How is free space stored and represented in the OS?

a. Free holes in memory are represented by a free list, which is a linked list data structure.
   - **Type:** It can be any linked list (singly, doubly). Each node is one free chunk and stores its starting address (and size).
   - **Free list through the running example:**

     | RAM state | Free list |
     |---|---|
     | Initial | [start 4KB, 12KB] -> NULL |
     | After P1 | [10KB] -> NULL |
     | After P2 | [2KB] -> NULL |
     | After P3 (RAM full) | NULL (nothing is free) |
     | After P1, P3 exit | [2KB] -> [2KB] -> NULL |

   - **Separate nodes:** The two 2KB chunks get separate nodes because they are not contiguous. They are far apart in memory.
   - **Merging:** If P2 also exits, an 8KB free node comes between them. The OS sees the addresses are contiguous and merges all into a single 12KB node.
   - **Use:** On every allocation the OS iterates this list to find which memory area is free.

## 3. How to satisfy a request of size n from a list of free holes?

- **Example:** The free list is 50KB -> 30KB -> 10KB -> 5KB -> NULL (4 free holes). P4 requests 20KB. It cannot go in 10KB or 5KB. It can go in either 50KB or 30KB. An algorithm decides which one to choose.
- **Running numbers:** The examples below use the free list 50KB -> 100KB -> 90KB -> 200KB -> 50KB -> NULL and a request of 90KB (P1).

a. The OS implements various algorithms to find holes in the linked list and allocate them to processes.

b. **First Fit**

   i. Allocate the first hole that is big enough.
      - **Example:** 50KB is too small. 100KB is the first hole big enough, so 90KB is allocated there and 10KB stays free. The free list becomes 50 -> 10 -> 90 -> 200 -> 50.

   ii. Simple and easy to implement.
      - Iterate and take the first block that is big enough. No comparisons are needed.

   iii. Fast, with lower time complexity.
      - It usually does not iterate the whole list. The worst case is still O(n), because the only fitting hole may be the last node.

c. **Next Fit**

   i. An enhancement on First Fit that always starts the search from the last allocated hole.
      - **Example:** The first 90KB request goes to the 100KB hole, the same as first fit. That leaves 10KB.
      - **Next request:** P2 (10KB) does not search from the start of the list. It starts from the position of the last allocation and moves forward from there.
      - **Extra work:** Only a pointer to the last allocation point must be saved. It is a tweak of first fit.

   ii. It has the same advantages as First Fit.

d. **Best Fit**

   i. Allocate the smallest hole that is big enough.
      - **Example:** For 90KB, look for the hole just bigger than (or equal to) the request. The 90KB hole leaves 0KB, the smallest leftover. So P1 goes there and that node is removed from the free list.

   ii. Less internal fragmentation.
      - It leaves the least space unused in the chosen hole.

   iii. It may create many small holes and cause major external fragmentation.
      - **Example:** An 85KB process placed in a 90KB hole leaves 5KB. After many such allocations, the free list becomes 2KB -> 3KB -> 5KB -> 1KB. A 7KB request fails even though total free space is more than 7KB, because no single contiguous hole is 7KB.

   iv. Slow, because it must iterate the whole free hole list.
      - Either sort the list by size or iterate the whole list. The best hole may be at the end.

e. **Worst Fit**

   i. Allocate the largest hole that is big enough.
      - **Example:** For 90KB, iterate and find the largest hole, 200KB. If a 300KB hole existed, it would be used. The first 90KB of it is allocated, and the remaining 110KB stays in the free list.
      - **Aim:** Leave the largest possible leftover space. It is greedy.

   ii. Slow, because it must iterate the whole free hole list.
      - The largest hole may be at the end of the list.

   iii. It leaves larger holes that may accommodate other processes.
      - This is the opposite of best fit. It gives less external fragmentation, since big leftover holes can still take other (even big) processes.

These algorithms are mostly used in contiguous allocation. Non-contiguous allocation is the next lecture.
