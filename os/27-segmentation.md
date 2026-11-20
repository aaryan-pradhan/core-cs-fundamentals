# Lecture 27: Segmentation | Non-Contiguous Memory Allocation

## The problem with paging

- **Paging:** It divides the logical address space (the user program) into fixed-size pages, for example 2 KB. It divides RAM into frames of the same size.
- **Big win:** Paging removes external fragmentation completely.
- **Small issue:** Paging ignores what the code actually is.
  - **Example:** A function `fun` takes 4 KB. The page size is 2 KB. The OS cuts `fun` into page 0 and page 1.
  - Allocation is non-contiguous, so page 0 may go to frame 5 and page 1 to frame 2.
  - The CPU thinks it is still inside one function. But the MMU's translation jumps from frame 5 to frame 2.
  - Executing within one frame is fast and efficient. Jumping to a far-off frame for the same function adds overhead.
- **Why paging stays:** The issue is small next to the big one paging solves (external fragmentation, which is poor space utilisation). The technique that solves the small issue is segmentation.

1. Paging forces a separation between the user's view of memory and the actual physical memory.
2. Segmentation is a memory management technique that supports the **user view of memory.**
3. A logical address space is a collection of segments. The segments are based on the **user view** of logical memory.
4. Each segment is defined by a **segment number and an offset.**
   **<segment-number, offset> {s,d}**
   - **Split:** The starting bits of a logical address give the segment number `s`. The remaining bits give the offset `d`, which is how far to go from that segment's base.
5. A process is divided into **variable segments based on the user view.**
   - **User:** The user is the programmer. Code that belongs together (one whole function) goes into one segment. Another function (`fun` vs `fun2`) goes into another segment.
   - **Variable vs fixed:** Segmentation is variable partitioning of the logical address space. Paging is fixed partitioning.
   - **Example:** S0 is `main`, S1 is `add`, S2 is `divide`, S3 is the stack area and S4 is `print`. Each segment has a different size.
   - **Who decides:** The compiler decides the segments.
6. **Paging** is closer to the operating system than to the **user**. It divides every process into pages. A process may have related parts of a function that need to be loaded in the same page.
7. The OS does not care about the **user's view.** It may **divide the same function into different pages.** Those **pages may or may not be loaded into memory at the same time.** This lowers efficiency.
8. It is better to divide the process into segments. Each segment holds the same type of functions. For example, `main` sits in one segment and library functions in another.
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

   - **How it works:** It is like paging, with a segment table (indexed by `s`) instead of a page table. It is also like contiguous allocation, since each entry is a base (relocation) register plus a limit register.
   - **Base and limit:** Segments have variable size, so each needs its own base (start in RAM) and limit (length).
   - **Steps:**
     1. The CPU generates the logical address `<s, d>`.
     2. Use `s` to index the segment table. Read that segment's limit and base.
     3. Check `d < limit`. If not, trap with an addressing error.
     4. Otherwise physical address = base + d.
   - **Bits example:** The logical address is `01 | 111`, so s = 1 and d = 7. Segment table entry 1 has limit = 15 and base = 20. 7 < 15, so it passes. Physical address = 20 + 7 = 27. Segment 1 occupies locations 20 to 35 (20 + 15), and 27 lies inside it.
   - **Decimal example:** The segments are subroutine, stack, symbol table, main program and `Sqrt`.

     | Segment | Limit | Base |
     |---|---|---|
     | 0 | 1000 | 1400 |
     | 1 | 400 | 6300 |
     | 2 | 400 | 4300 |
     | 3 | 1100 | 3200 |
     | 4 | 1000 | 4700 |

     - Byte 53 of segment 2 passes, since 53 < 400. Physical address = 4300 + 53 = 4353.

### External fragmentation in segmentation

- **Contiguous segments:** Each segment is allocated in RAM as a whole, contiguously.
- **Example:** RAM holds segments S0 and S1 of process P0. The free holes are 2 KB, 2 KB and 1 KB (5 KB free, not contiguous).
- Process P1 arrives with S0 = 2 KB and S1 = 3 KB. S0 fits in a 2 KB hole. S1 needs 3 KB contiguous, and no hole is that big.
- **Result:** 5 KB is free, yet the 5 KB process P1 cannot be allocated. Segmentation has external fragmentation.
- **No internal fragmentation:** A segment gets exactly as much memory as its size.

10. **Advantages**:
    a. No internal fragmentation.
    b. One segment is allocated contiguously, so work within a segment is efficient.
       - **Example:** The whole `Sqrt` function sits in one contiguous segment.
    c. The segment table is generally smaller than the page table.
       - **Example:** A 100 KB program with 2 KB pages has 50 pages, so a 50-entry page table. The same program may have only two 50 KB segments, so a 2-entry segment table.
       - A smaller table needs less memory.
    d. The system is more efficient, because the compiler keeps the same type of functions in one segment.
       - Functions of the same nature (accessing the same area, doing the same work) sit together.
11. **Disadvantages**:
    a. External fragmentation.
    b. Different segment sizes are bad at swapping time.
       - **Swapping:** It was seen with the medium-term scheduler. When the degree of multiprogramming rises, the OS swaps out some segments of a process.
       - **Example:** P1 has worked only in a few segments for a long time. Segments 4 and 5 sit idle, so the OS moves them to the swap area.
       - **Swap area:** It is an area on the hard disk (backing store) that stores segments of main memory. It is disk space that behaves like RAM (virtual memory, next lecture).
       - If P1 then needs segment 4, the OS raises a fault and brings the segment back from the swap area.
       - **Problem:** Each swap moves a different amount. Big segments take more time and small ones less, so estimation goes wrong.
12. Modern system architecture provides both segmentation and paging, in a hybrid approach.
    - **Theory vs real:** A real system (for example a MacBook) does not use only segmentation or only paging for translation. It uses both.
    - **Page sizes:** Modern systems define two or three page sizes, not one fixed size.

### Internal fragmentation in paging

- Paging has internal fragmentation. Segmentation does not.
- **Example:** A program is 15 KB and the page size is 2 KB (decided by the architecture or system).
- 15 KB does not divide evenly (16 KB would), so 8 pages are needed. The last 2 KB page stores only 1 KB. The other 1 KB stays empty.
- The matching 2 KB frame in RAM is also half used, so RAM has 1 KB of unavoidable internal fragmentation.

> **Interview:** Explain paging, explain segmentation, and compare the two.
