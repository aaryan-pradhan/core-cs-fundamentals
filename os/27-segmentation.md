# Lecture 27: Segmentation | Non-Contiguous Memory Allocation

## The problem with paging

- Paging divides the logical address space (user program) into fixed-size pages (e.g. every page 2 KB), and RAM into frames of the same size.
- Paging removes external fragmentation completely, which is its big win.
- Small issue: paging ignores what the code actually is.
  - Example: you write a function `fun` that takes 4 KB in the logical address space. Page size is 2 KB.
  - The OS still cuts it into two pages: page 0 (first half of `fun`) and page 1 (second half of `fun`).
  - Allocation is non-contiguous, so page 0 may go to frame 5 and page 1 to frame 2.
  - The CPU keeps generating logical addresses one after another and thinks it is still inside the same function.
  - Actually, once the first half of `fun` is over, the MMU's translation jumps from frame 5 to frame 2.
  - Executing within one frame gives fast, efficient memory access. Jumping to a far-off frame for the same function adds overhead, though the whole function could have run from one place.
- This is a small issue compared with the big one paging solves (external fragmentation, i.e. poor space utilisation), so paging is still used. The technique that solves this small issue is segmentation.

1. An important aspect of memory management that become unavoidable with paging is separation of user's view of memory from the actual physical memory.
2. Segmentation is memory management technique that supports the **user view of memory.**
3. A logical address space is a collection of segments, these segments are based on **user view** of logical memory.
4. Each segment has **segment number and offset,** defining a segment.
   **<segment-number, offset> {s,d}**
   - Every logical address the CPU generates is split in two: the starting bits give the segment number `s`, the remaining bits give the offset `d` (how far to go from that segment's base).
5. Process is divided into **variable segments based on user view.**
   - User here = the programmer. Code that belongs together (one whole function) goes into one segment; a different function (`fun` vs `fun2`) goes into a different segment.
   - So segmentation is variable partitioning of the logical address space; paging is fixed partitioning.
   - Example program split into segments: S0 = `main` function, S1 = `add` function, S2 = `divide` function, S3 = stack area of the process, S4 = `print` function. Each segment has a different size.
   - The compiler decides the segments: it sees, from the user's view, which functions should go into the same segment and which into separate ones.
6. **Paging** is closer to the Operating system rather than the **User**. It divides all the processes into the form of pages although a process can have some relative parts of functions which need to be loaded in the same page.
7. Operating system doesn't care about the **User's view** of the process. It may **divide the same function into different pages** and those **pages may or may not be loaded at the same time into the memory.** It decreases the efficiency of the system.
8. It is better to have segmentation which divides the process into the segments. Each segment contains the same type of functions such as the main function can be included in one segment and the library functions can be included in the other segment.
9. **Segmentation hardware**

```
                                    Segment table
                                  +-------+------+
                 +--------------->| limit | base |
                 |                +-------+------+
                 |                |       |      |   (row s)
                 |                +-------+------+
                 |                    |       |
+-----+  logical |                    | limit | base
| CPU |  address |                    v       v
|     |-------->[ s | d ]---d----->  < ? ----Yes----> ( + ) -------> physical memory
+-----+                            (d < limit)
                                       |
                                       No
                                       v
                             trap: addressing error
```

   - Works like paging (a segment table instead of a page table, indexed by `s`) mixed with contiguous allocation (each entry is like a relocation/base register plus a limit register).
   - Segments are of variable size, so each segment needs its own base (where it starts in RAM) and its own limit (its length).
   - Steps:
     1. CPU generates logical address `<s, d>`.
     2. Use `s` to index the segment table and read that segment's limit and base.
     3. Check `d < limit`, i.e. the offset does not go outside the segment. If not, trap: addressing error.
     4. If yes, physical address = base + d.
   - Bits example: logical address `01 | 111`, so s = 1, d = 7. Segment table entry 1: limit = 15, base = 20. Check 7 < 15: yes. Physical address = 20 + 7 = 27. Segment 1 occupies locations 20 to 35 (20 + 15), and location 27 lies inside it.
   - Decimal example: logical address space has segments subroutine, stack, symbol table, main program, `Sqrt`.

     | Segment | Limit | Base |
     |---|---|---|
     | 0 | 1000 | 1400 |
     | 1 | 400 | 6300 |
     | 2 | 400 | 4300 |
     | 3 | 1100 | 3200 |
     | 4 | 1000 | 4700 |

     - Limits differ for each segment (variable size), so each needs a different base and limit.
     - Reference to byte 53 of segment 2: 53 < 400 (within limit), so physical address = 4300 + 53 = 4353.

### External fragmentation in segmentation

- Each segment is allocated in RAM as a whole, contiguously.
- Example: RAM holds segments S0 and S1 of process P0. The free holes left are 2 KB, 2 KB and 1 KB (total 5 KB free, but not contiguous).
- Process P1 arrives with S0 = 2 KB and S1 = 3 KB.
- S0 fits in one of the 2 KB holes. S1 needs 3 KB contiguous, and no hole is that big, so it cannot be allocated.
- 5 KB is free, yet the 5 KB process P1 cannot be allocated: segmentation has external fragmentation.
- No internal fragmentation: a segment is given exactly as much memory as its size.

10. **Advantages**:
    a. No internal fragmentation.
    b. One segment has a contiguous allocation, hence efficient working within segment.
       - e.g. the whole `Sqrt` function sits in one contiguous segment, so execution inside it is efficient.
    c. The size of segment table is generally less than the size of page table.
       - e.g. a 100 KB program with 2 KB pages has 50 pages, so a 50-entry page table. The same program may have only two 50 KB segments, so a 2-entry segment table.
       - Pages are cut by page size, so there are more pages and more entries. A smaller segment table needs less memory to store.
    d. It results in a more efficient system because the compiler keeps the same type of functions in one segment.
       - Functions of the same nature (accessing the same area, doing the same work) sit in one segment, others in another, which makes the system more efficient from the user's perspective.
11. **Disadvantages**:
    a. External fragmentation.
    b. The different size of segment is not good that the time of swapping.
       - Swapping (seen with the medium-term scheduler): when the degree of multiprogramming rises, the OS swaps out some segments of a process to make room.
       - e.g. process P1 has been working only in a few of its segments for a long time. Segments 4 and 5 are sitting idle in main memory, so the OS moves them to the swap area.
       - Swap area = an area on the hard disk (backing store) that stores segments of main memory so they are ready to use by the process, i.e. disk space that behaves like RAM (virtual memory, next lecture).
       - If P1 then needs segment 4, the OS raises a fault and quickly brings the segment back from the swap area.
       - With different segment sizes, every swap-in/swap-out moves a different amount: big segments take more time, small ones less. Each segment takes a different time, estimation goes wrong, and the system is not efficient.
12. Modern System architecture provides both segmentation and paging implemented in some hybrid approach.
    - These concepts are theoretical; a real system (e.g. a MacBook) does not use only segmentation or only paging for logical-to-physical translation. Both are implemented in a hybrid approach.
    - Similarly, modern systems do not keep one fixed page size; two or three page sizes are defined.

### Internal fragmentation in paging

- Paging has internal fragmentation; segmentation does not.
- Example: program of 15 KB, page size 2 KB (decided by the architecture/system).
- 15 KB does not divide evenly (16 KB would). So 8 pages are needed, and the last 2 KB page stores only 1 KB; the other 1 KB stays empty.
- The matching 2 KB frame in RAM is also only half used, so RAM has 1 KB of internal fragmentation that cannot be avoided.
- Paging has to accept this problem; segmentation does not have it.
- Interview question: explain paging, explain segmentation, and compare the two.
