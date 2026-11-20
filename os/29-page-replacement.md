# Lecture 29: Page Replacement Algorithms

## Background: page fault

- **Frames:** RAM is divided into frames that hold pages of many processes (for example P1, P2 and P3).
- **Partial loading:** To keep the degree of multiprogramming high, the OS loads only some important pages of each process into RAM. The rest stay in the swap area (on disk). So RAM can be completely full.
- **Missing page:** An instruction in P1 may say "go to page 3 of P1". Page 3 is in the swap area, not in RAM.
- **Free frame:** If a frame is free, the OS loads the new page there. No other page is removed.
- **No free frame:** The OS must deallocate a frame. Some page of P1, P2 or P3 is swapped out, and only then is the new page swapped in.
- **Page fault:** It is an interrupt saying "this page is in the swap area. Bring it into RAM (and swap out some current page if needed)".
- **Page fault service time:** Swapping a page out and another in takes time. This overhead is called the **page fault service time**.

1. A **page fault** occurs when a process tries to access a page that is not currently present in a frame. The OS must bring the page from swap space to a frame.
2. If all frames are busy (high utilization), the OS must replace one allocated page with the new page.
3. The **page replacement algorithm** decides which memory page is replaced. Some allocated page is swapped out from its frame, and the new page is swapped into the freed frame.
   - **Rule:** The new page must be brought into RAM at any cost. The algorithm only decides which page in RAM is removed.
4. **Types** of page replacement algorithm. The **AIM** is to have the minimum page faults.
   - **Cost of a fault:** Every page fault reads the swap area on disk, whose access time is very high.
   - **Quality:** More page faults means more overhead and a worse algorithm.
   - **Reference string:** It is the sequence of page numbers the process requests, serviced in order. The examples assume 3 empty frames (the rest of RAM is full) and one process.
   - **Page hit:** The referenced page is already in a frame, so there is no fault.
   - **Page miss:** The referenced page is not in a frame, so a page fault occurs.

   a. **FIFO**

      i. Allocate a frame to the page as it comes into memory by **replacing the oldest page.**
         - If a frame is empty, the page is put there. No page is freed.
         - **Example:** Reference string `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1`, 3 frames (F = page fault):

           | Reference | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
           |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
           | Frame 1 | 7 | 7 | 7 | 2 | 2 | 2 | 2 | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 7 | 7 |
           | Frame 2 |  | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
           | Frame 3 |  |  | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 1 |
           | Page fault? | F | F | F | F |  | F | F | F | F | F | F |  |  | F | F |  |  | F | F | F |

           - 7, 0 and 1 fill the empty frames (3 faults).
           - 2 replaces the oldest page, 7. 0 is a hit. 3 replaces 0. 0 replaces 1. 4 replaces 2. And so on.
           - **Total:** **15 page faults** with FIFO.

      ii. It is easy to implement.

      iii. Performance is **not** always good.
         - **Variable:** It depends on the reference string. There is no guarantee.
         - **Reason:** FIFO ignores how a page is used.

         1. The replaced page may be an initialization module that was used a long time ago. **(Good replacement candidate)**
            - In the example, FIFO replaced 7 when 2 arrived. Page 7 is not used again until near the end, so replacing it was good.

         2. The page may contain a heavily used variable that was initialized early and is in constant use. (**Will again cause a page fault**)
            - If the string had 7 right after 2, FIFO would remove 7 and bring it back, causing an extra page fault.
            - In real time, the OS does not know which page comes next. A page used again and again should not be removed, but FIFO does not consider this.

      iv. **Belady's** anomaly is present.

         1. **In LRU and optimal page replacement, the number of page faults is reduced if we increase the number of frames.** Belady found that in FIFO, the number of page faults can increase when the number of frames increases.
            - **Normal expectation:** Plot frames (x-axis) against page faults (y-axis). More frames mean more pages in RAM, so page faults keep decreasing.
            - **In FIFO:** Sometimes page faults increase even though frames increased.
            - **Example:** Reference string `1 2 3 4 1 2 5 1 2 3 4 5` with FIFO:

              | Number of frames | 2 | 3 | 4 | 5 | 6 |
              |---|---|---|---|---|---|
              | Page faults | 12 | 9 | 10 | 5 | 5 |

            - From 3 to 4 frames, page faults rise from 9 to 10. Then they drop drastically. This graph is Belady's anomaly.
            - 3 frames (9 faults):

              | Reference | 1 | 2 | 3 | 4 | 1 | 2 | 5 | 1 | 2 | 3 | 4 | 5 |
              |---|---|---|---|---|---|---|---|---|---|---|---|---|
              | Frame 1 | 1 | 1 | 1 | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 5 |
              | Frame 2 |  | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 3 | 3 | 3 |
              | Frame 3 |  |  | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 4 | 4 |
              | Page fault? | F | F | F | F | F | F | F |  |  | F | F |  |

            - 4 frames (10 faults):

              | Reference | 1 | 2 | 3 | 4 | 1 | 2 | 5 | 1 | 2 | 3 | 4 | 5 |
              |---|---|---|---|---|---|---|---|---|---|---|---|---|
              | Frame 1 | 1 | 1 | 1 | 1 | 1 | 1 | 5 | 5 | 5 | 5 | 4 | 4 |
              | Frame 2 |  | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 5 |
              | Frame 3 |  |  | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 2 | 2 |
              | Frame 4 |  |  |  | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 3 |
              | Page fault? | F | F | F | F |  |  | F | F | F | F | F | F |

         2. FIFO shows this behavior **only in some cases** (some reference strings).

   b. **Optimal** page replacement
      - **Best:** It gives the minimum possible page faults. It is the ideal algorithm.
      - **Problem:** It is almost impossible to implement.

      i. Find a page that is never referenced in the future. If such a page exists, replace it with the new page.
         If no such page exists, find a page that is **referenced farthest in the future**. Replace that page with the new page.
         - The furthest page is the one whose next use is latest (furthest right in the reference string).
         - **Example:** Same reference string as FIFO, 3 frames:

           | Reference | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
           |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
           | Frame 1 | 7 | 7 | 7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 7 | 7 | 7 |
           | Frame 2 |  | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
           | Frame 3 |  |  | 1 | 1 | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
           | Page fault? | F | F | F | F |  | F |  | F |  |  | F |  |  | F |  |  |  | F |  |  |

           - 7, 0 and 1 fill the empty frames (3 faults).
           - 2 replaces 7 (next used latest, third-last position). 0 is a hit. 3 replaces 1 (next used latest). 0 is a hit. 4 replaces 0, giving 2, 4, 3. And so on.
           - **Total:** **9 page faults**, the minimum possible (against 15 in FIFO).

      ii. It has the **lowest** page fault rate of any algorithm.

      iii. It is difficult to implement, as the **OS requires future knowledge of the reference string.** This is nearly impossible. (Similar to SJF scheduling.)
         - **Like SJF:** SJF needs the burst time, which cannot be known in advance (for example the program may get stuck in a while loop).
         - **Heuristics:** An implementation would only guess (for example "7 will probably be used last"). Guesses are not reliable.
         - **Use:** It is the reference that other algorithms are compared against.

   c. Least-recently used (**LRU**)

      > **Interview:** LRU is very important. It is also asked as a DSA question: "Which page replacement algorithms exist? Explain LRU, how can it be implemented, write its code."

      i. We use the recent past as an approximation of the near future. We replace the page that has not been used for the longest period.
         - **Idea:** The future cannot be known, but the past can. The near past will probably repeat in the near future ("history repeats itself").
         - **Rule:** The page unused for the longest time is assumed not to be needed soon, so it is replaced.
         - **Hit:** A page that is referenced again becomes "new" again.
         - **Example:** Same reference string, 3 frames:

           | Reference | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
           |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
           | Frame 1 | 7 | 7 | 7 | 2 | 2 | 2 | 2 | 4 | 4 | 4 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
           | Frame 2 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
           | Frame 3 |  |  | 1 | 1 | 1 | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 7 | 7 | 7 |
           | Page fault? | F | F | F | F |  | F |  | F | F | F | F |  |  | F |  | F |  | F |  |  |

           - 7, 0 and 1 fill the empty frames (3 faults).
           - 2 replaces 7 (least recently used). 0 is a hit. 3 replaces 1, giving 2, 0, 3. 0 is a hit. 4 replaces 2, giving 4, 0, 3. 2 replaces 3, giving 4, 0, 2. 3 replaces 0, giving 4, 3, 2. And so on.
           - **Total:** **12 page faults**.
         - **Comparison:** FIFO has 15 faults, LRU 12 and Optimal 9. Optimal is hypothetical, so in practice **LRU is the best**.

      ii. It can be implemented in two ways.

         1. **Counters**
            a. Associate a time field with each page table entry.
            b. Replace the page with the smallest time value.
            - **How:** Keep one global counter that increments on every reference. Write its current value into the referenced page's entry. The smallest value is the oldest page, so it is replaced.
            - **Example (same string):** 7 gets 1, 0 gets 2 and 1 gets 3. 2 arrives. 7 has the smallest value (1), so it is replaced. 2 gets 4. 0 is referenced, so 0 becomes 5. 3 arrives. 1 has the smallest value (3), so it is replaced. 3 gets 6. And so on.
            - **Problem:** The counter can overflow. It is declared as, for example, an `int32` (range 2^32). Even unsigned or `int64` has a limit. Overflow is likelier on 32-bit than on 64-bit. So the stack approach is better.

         2. **Stack**
            a. Keep a stack of page numbers.
            b. Whenever a page is referenced, remove it from the stack and put it on the top.
            c. This way, the most recently used page is always on the top and the least recently used page is always on the bottom.
            d. Entries may be removed from the middle of the stack, so a doubly linked list can be used.
            - **Modified stack:** Entries can be inserted or deleted at the top, bottom and middle, but it is accessed like a stack.
            - **Operation:** The referenced page (anywhere in the stack) is taken out and put on top. On a page miss, the bottom page (least recently used) is replaced.
            - **Doubly linked list:** Pointers must be moved around, and this gives the minimum time complexity.
            - **Simulation:** Same string, 3 frames, stack shown top first.

              | Reference | Frames | Stack (top to bottom) | Action |
              |---|---|---|---|
              | 7 | 7 | 7 | fault, empty frame |
              | 0 | 7 0 | 0 7 | fault, empty frame |
              | 1 | 7 0 1 | 1 0 7 | fault, empty frame |
              | 2 | 2 0 1 | 2 1 0 | fault, bottom 7 removed |
              | 0 | 2 0 1 | 0 2 1 | hit, 0 moved to top |
              | 3 | 2 0 3 | 3 0 2 | fault, bottom 1 removed |
              | 0 | 2 0 3 | 0 3 2 | hit, 0 moved to top |
              | 4 | 4 0 3 | 4 0 3 | fault, bottom 2 removed |

         - **Implement it yourself:** LRU is the most important algorithm here. The same algorithm is used in cache design: recently used data stays in front and the least recently used data is removed (or kept at the back).

   d. **Counting**-based page replacement. Keep a counter of the number of references made to **each** page. (Reference counting)
      > **Interview:** Counting-based algorithms are not very important. Naming FIFO, Optimal and LRU is enough, but knowing these can help.

      - Each page keeps a reference count. It is incremented every time the page is referenced.

      i. Least frequently used (**LFU**)
         1. Actively used pages should have a large reference count.
         2. Replace the page with the smallest count.
         - The page with the smallest reference count is assumed to be used the least, so it is removed. Pages with the largest counts are kept.

      ii. Most frequently used (**MFU**)
         1. It is based on the argument that the page with the smallest count was probably just brought in and has yet to be used.
         - **Opposite of LFU:** The page with the smallest count is kept, since it still has to be used. The page with the largest count is replaced.

      iii. Neither MFU nor LFU replacement is common.
         - They are not used in practice. They are just concepts to know.
