# Lecture 29: Page Replacement Algorithms

## Background: page fault

- RAM is divided into frames. The frames hold pages of many processes (e.g. pages of P1, P2, P3).
- To keep the degree of multiprogramming high, the OS divides each process into multiple pages and loads only some of its important pages into RAM. The rest stay in the swap area (on disk).
- So RAM can be completely full, with pages of three processes in it.
- While P1's code runs, an instruction in one of its pages may say "go to page 3 of P1". Page 3 is not in RAM; it is in the swap area.
- If some frame of RAM is free, the OS simply loads the new page into that free frame. No other page has to be removed.
- If all frames are filled, the OS must find a frame it can deallocate: some page of P1, P2 or P3 is swapped out, and only then is the new page swapped in.
- The OS generates a **page fault** for this. A page fault is an interrupt saying "this page is not available in RAM, it is in the swap area; bring it into RAM (and swap out some current page if needed)".
- Swapping a page out and another page in takes time. This overhead is called the **page fault service time**.

1. Whenever **Page Fault** occurs, that is, a process tries to access a page which is not currently present in a frame and OS must bring the page from swap-space to a frame.
2. OS must do page replacement to accommodate new page into a free frame, but there might be a possibility the system is working in high utilization and all the frames are busy, in that case OS must replace one of the pages allocated into some frame with the new page.
3. The **page replacement algorithm** decides which memory page is to be replaced. Some allocated page is swapped out from the frame and new page is swapped into the freed frame.
   - The new page has to be brought into RAM at any cost. The algorithm only decides which page already in RAM is removed to make room for it.
4. **Types** of Page Replacement Algorithm: (**AIM** is to have minimum page faults)
   - Every page fault brings the page from the swap area, which is on disk, whose access time is very high. So every page fault costs page fault service time.
   - More page faults = more overhead = worse algorithm. Fewer page faults = less total page fault service time = everything runs faster.
   - **Reference string**: the sequence of page numbers the process requests, one after another, which must be serviced in that order. Examples below assume 3 empty frames (the rest of RAM is assumed full) and all pages belong to one process, to keep it simple.
   - **Page hit**: the referenced page is already in a frame (no fault). **Page miss**: it is not, so a page fault occurs.

   a. **FIFO**

      i. Allocate frame to the page as it comes into the memory by **replacing the oldest page.**
         - The oldest page is removed and the new page is put in its place, in order of arrival.
         - If a frame is empty, the page is simply put there; no page needs to be freed.
         - Example: reference string `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1`, 3 frames (F = page fault):

           | Reference | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
           |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
           | Frame 1 | 7 | 7 | 7 | 2 | 2 | 2 | 2 | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 7 | 7 |
           | Frame 2 |  | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
           | Frame 3 |  |  | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 1 |
           | Page fault? | F | F | F | F |  | F | F | F | F | F | F |  |  | F | F |  |  | F | F | F |

           - 7, 0, 1 go into the empty frames (3 faults).
           - 2 arrives, all frames full: 7 is the oldest, so 7 is replaced by 2.
           - 0 is already present: hit.
           - 3 arrives: 0 is now the oldest, so 0 is replaced by 3.
           - 0 arrives: 1 is the oldest, so 1 is replaced by 0.
           - 4 arrives: 2 is the oldest, so 2 is replaced by 4. And so on.
           - Total: **15 page faults** with FIFO.

      ii. Easy to implement.

      iii. Performance is **not** always good
         - Performance is variable: sometimes good, sometimes bad, depending on the reference string. There is no guarantee.
         - Reason: FIFO replaces the oldest page without looking at how the page is used.

         1. The page replaced may be an initialization module that was used long time ago **(Good replacement candidate)**
            - In the example, when 2 arrived, FIFO replaced 7. Page 7 is not referenced again until near the end of the string, so it was a good candidate: keeping it in RAM is useless. A page used once at the start and never again (like an initialization module) should be replaced.

         2. The page may contain a heavily used variable that was initialized early and is in constant use. (**Will again cause page fault**)
            - If the string had 7 right after 2, FIFO would have just removed 7 and would need to bring it back, causing an extra page fault. Not removing 7 would have saved a page fault.
            - In real time, many processes run and any page can be requested; the OS does not know which page comes next. A page that is used again and again should not be removed, but FIFO does not consider this.

      iv. **Belady’s** anomaly is present.

         1. **In the case of LRU and optimal page replacement algorithms, it is seen that the number of page faults will be reduced if we increase the number of frames.** However, Belady found that, In FIFO page replacement algorithm, the number of page faults will get increased with the increment in number of frames.
            - Normal expectation: plot number of frames (x-axis) vs number of page faults (y-axis). As frames increase, more pages fit in RAM, so page faults keep decreasing.
            - In FIFO, sometimes the number of page faults increases even though the number of frames increased.
            - Example: reference string `1 2 3 4 1 2 5 1 2 3 4 5` with FIFO:

              | Number of frames | 2 | 3 | 4 | 5 | 6 |
              |---|---|---|---|---|---|
              | Page faults | 12 | 9 | 10 | 5 | 5 |

            - Going from 3 frames to 4 frames, page faults rise from 9 to 10 (irregularity), then drop drastically. This graph is Belady's anomaly.
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

         2. This is the strange behavior shown by FIFO algorithm **in some of the cases.**
            - Even in FIFO it does not always happen; only some reference strings show it.

   b. **Optimal** page replacement
      - The best algorithm: it gives the minimum possible page faults. No algorithm can do better; it is the ideal algorithm.
      - Problem: it is almost impossible to implement.

      i. Find if a page that is never referenced in future. If such a page exists, replace this page with new page.
         If no such page exists, find a page that is **referenced farthest in future**. Replace this page with new page.
         - A page never referenced in future is lying in RAM uselessly, so remove it.
         - Otherwise remove the page whose next use is latest (furthest right in the reference string).
         - Example: same reference string as FIFO, 3 frames:

           | Reference | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
           |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
           | Frame 1 | 7 | 7 | 7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 7 | 7 | 7 |
           | Frame 2 |  | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
           | Frame 3 |  |  | 1 | 1 | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
           | Page fault? | F | F | F | F |  | F |  | F |  |  | F |  |  | F |  |  |  | F |  |  |

           - 7, 0, 1 go into empty frames (3 faults).
           - 2 arrives: among 7, 0, 1, page 7 is next used latest (third-last position); 0 and 1 are used before it. So 7 is replaced by 2.
           - 0: hit.
           - 3 arrives: among 2, 0, 1, page 1 is next used latest. So 1 is replaced by 3.
           - 0: hit.
           - 4 arrives: among 2, 0, 3, page 2 and 3 are used soon after; 0 is used latest. So 0 is replaced by 4, giving 2, 4, 3. And so on.
           - Total: **9 page faults**, the minimum possible (vs 15 in FIFO).

      ii. **Lowest** page fault rate among any algorithm.

      iii. Difficult to implement as **OS requires future knowledge of reference string** which is kind of impossible. (Similar to SJF scheduling)
         - While the OS runs many programs, it cannot predict exactly which page will not be used for the longest time.
         - Like SJF: SJF schedules the job with the smallest burst time, but the burst time cannot be known in advance (e.g. the program may get stuck in a while loop).
         - Even if implemented, it would use heuristics, i.e. guesses (e.g. "7 will probably be used last"), which are not reliable in the real world.
         - So it is used as a reference: other algorithms are compared against it.

   c. Least-recently used (**LRU**)
      - Very important. It is also asked as a DSA / interview question: "Which page replacement algorithms exist? Explain LRU, how can it be implemented, write its code."

      i. We can use recent past as an approximation of the near future then we can replace the page that has not been used for the longest period.
         - Optimal looks at the future. The future cannot be known, but the past can. Assumption: what happened in the near past will probably happen in the near future ("history repeats itself").
         - So the page that has been sitting unused for the longest time (the "oldest" by last use) is assumed not to be needed soon, and is replaced.
         - Whenever a page is referenced again (a hit), it becomes "new" again.
         - Example: same reference string, 3 frames:

           | Reference | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
           |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
           | Frame 1 | 7 | 7 | 7 | 2 | 2 | 2 | 2 | 4 | 4 | 4 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
           | Frame 2 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
           | Frame 3 |  |  | 1 | 1 | 1 | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 7 | 7 | 7 |
           | Page fault? | F | F | F | F |  | F |  | F | F | F | F |  |  | F |  | F |  | F |  |  |

           - 7, 0, 1 go into empty frames (3 faults).
           - 2 arrives: 7 is least recently used, so 7 is replaced by 2.
           - 0: page hit; 0 becomes most recently used.
           - 3 arrives (frames 2, 0, 1): 0 was just used, so 1 is least recently used. 1 is replaced by 3, giving 2, 0, 3.
           - 0: hit.
           - 4 arrives: 0 was just used, then 3; 2 is least recently used. 2 is replaced by 4, giving 4, 0, 3.
           - 2 arrives: 4 just came, then 0; 3 is least recently used. 3 is replaced, giving 4, 0, 2.
           - 3 arrives: 2 and 4 were just used; 0 is least recently used. 0 is replaced, giving 4, 3, 2. And so on.
           - Total: **12 page faults**.
         - Comparison on the same string: FIFO 15, LRU 12, Optimal 9. Optimal is best but hypothetical (needs future knowledge). So practically, **LRU is the best**.

      ii. Can be implemented by two ways

         1. **Counters**
            a. Associate time field with each page table entry.
            b. Replace the page with smallest time value.
            - Keep one global (shared) counter that increments on every reference. On each reference, write the current counter value into that page's entry. The smallest value = oldest = the page to replace.
            - Example (same string): 7 gets 1, 0 gets 2, 1 gets 3. 2 arrives: smallest value is 7's (1), so 7 is replaced; 2 gets 4 and 7's entry is removed. 0 is referenced: 0's value becomes 5. 3 arrives: smallest value is 1's (3), so 1 is replaced; 3 gets 6 and 1's entry is removed. And so on.
            - Problem: counter overflow. The counter is declared as e.g. an `int32` (range 2^32); even unsigned or `int64` has a limit, and the counter keeps increasing. On a 32-bit system it can overflow; on a 64-bit system it can too, but the chance is lower because the range is much bigger. So the stack approach is better.

         2. **Stack**
            a. Keep a stack of page number.
            b. Whenever page is referenced, it is removed from the stack & put on the top.
            c. By this, most recently used is always on the top, & least recently used is always on the bottom.
            d. As entries might be removed from the middle of the stack, so Doubly linked list can be used.
            - It is a modified stack: entries can be inserted/deleted at the top, the bottom and the middle, but it is accessed like a stack.
            - The referenced page may be anywhere (bottom, middle); it is taken out and put on top. On a page miss, the page at the bottom (least recently used) is the one replaced.
            - A doubly linked list is used because pointers have to be moved around; it gives the operations with minimum time complexity.
            - Simulation (same string, 3 frames, stack shown top first):

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

         - Implement LRU yourself; it is the most important algorithm here. It is not only for page replacement: the same algorithm is used in cache design, where the most recently used data is kept in front and the least recently used data is removed (or kept at the back).

   d. **Counting**-based page replacement – Keep a counter of the number of references that have been made to **each** page. (Reference counting)
      - Not very important for interviews; naming FIFO, Optimal and LRU is enough, but knowing these can help.
      - Each page keeps a reference count that is incremented every time the page is referenced.

      i. Least frequently used (**LFU**)
         1. Actively used pages should have a large reference count.
         2. Replace page with the smallest count.
         - The page with the smallest reference count is assumed to be used the least, so it is removed; pages with the largest counts are kept.

      ii. Most frequently used (**MFU**)
         1. Based on the argument that the page with the smallest count was probably just brought in and has yet to be used.
         - Opposite of LFU: the page with the smallest count is kept (it still has to be used), and the page with the largest count is replaced.

      iii. Neither MFU nor LFU replacement is common.
         - They are not used in practice; they are just concepts to know.
