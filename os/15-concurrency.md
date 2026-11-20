# Lecture 15: Introduction to Concurrency

- **New module:** Concurrency. It covers:
  - What a thread is, why threads are needed, how threads are scheduled, how a thread differs from a process, and the advantages of threads.
  - Problems after breaking a process into threads: synchronization problems, and how to solve them.
  - The strategies used to solve synchronization bring another bug: deadlock.
- **This lecture:** What concurrency is, what a thread is, how threads are scheduled, benefits of multi-threading, and a hands-on multi-threaded C++ program.
- **Revise first:** Lecture 3 (Multitasking vs Multithreading), where threads were introduced.

1. **Concurrency** is the execution of multiple instruction sequences at the same time. It happens in the OS when several process threads run in parallel.
   - **How it is achieved:** Divide a process into threads (T1, T2, ...). Execute multiple instructions of the same process at the same time, in parallel.

2. **Thread:**
   - It is a single sequence stream within a process.
   - It is an independent path of execution in a process.
   - It is a light-weight process (LWP), a sub-process inside one process. It is not an actual process.
   - It is used to achieve parallelism by dividing a process's tasks into independent paths of execution.
     - **Example:** A process has independent Task A and Task B. Divide it into thread T1 (Task A) and thread T2 (Task B). Give T1 to CPU 1 and T2 to CPU 2. Both execute in parallel.
     - **Only multi-core:** Threads give an advantage only with a multi-core CPU. With a single core, threads are scheduled like two processes, with context switching. There is no real gain.
   - **Examples:** Multiple tabs in a browser. A text editor: while you type, spell checking, formatting of text and saving are done concurrently by multiple threads.
     - **MS Word:** One process with three tasks: text editor, spell checker, text formatting. Break it into three light-weight processes: thread 1, thread 2, thread 3.
     - **As one process:** The tasks run sequentially, and the user waits.
     - **With threads:** While you type, spell checking runs alongside (red underlines appear). Formatting runs alongside (pressing Enter moves text, bold, and so on).
     - **Benefit:** Responsiveness increases. This is the biggest advantage of concurrency.
   - **Memory: process vs thread**
     - **Process:** Each process gets its own address space, isolated from other processes' address spaces.
     - **Threads:** Process P1 is broken into threads T1, T2, T3. All three use the same address space, the one allocated to P1. A shared memory space is used among the threads.
     - This is the most important difference between a process and a thread.

     ```
     Process                     Threads of one process
     ┌──────────────┐            ┌───────────────────────┐
     │ P1           │            │ P1:  T1   T2   T3     │
     │ own address  │            │   └────┼────┘         │
     │ space        │            │  one shared address   │
     └──────────────┘            │  space                │
     (isolated from others)      └───────────────────────┘
     ```

   - **Memory layout:**
     - **Process:** text, data, heap and stack. Stack and heap grow towards each other.
     - **Multi-threaded process:** The same text, data and heap, but one stack per thread (stack 1 for thread 1, stack 2 for thread 2, ...). The heap stays one, shared by all threads.

     ```
     Process            Multi-threaded process
     ┌─────────┐        ┌─────────┐
     │ Stack   │        │ Stack 1 │  (T1)
     │   ↓     │        │ Stack 2 │  (T2)
     │         │        │   ↓     │
     │   ↑     │        │   ↑     │
     │ Heap    │        │ Heap    │  (shared by all threads)
     │ Data    │        │ Data    │
     │ Text    │        │ Text    │
     └─────────┘        └─────────┘
     ```

3. **Thread Scheduling:** The OS schedules threads based on their priority. The OS assigns all threads processor time slices.
   - Like process (CPU) scheduling, threads also have scheduling.
   - **Priority:** A higher priority thread gets more CPU access. Others get less.

4. **Threads context switching**
   - The OS saves the state of one thread and retrieves the state of another thread of the same process.
   - It does not switch the memory address space. The program counter, registers and stack are switched.
     - Both threads belong to the same process and use its address space.
   - **Fast:** Switching is fast compared to process switching, since only a few things (PC, registers) are switched.
   - **Cache:** The CPU's cache state is preserved. The same address space keeps cached instructions valid, so there is no need to reset the cache.

5. **How does each thread get access to the CPU?**
   - Each thread has its own program counter.
   - The OS schedules threads depending on the thread scheduling algorithm.
   - The OS fetches instructions corresponding to the PC of that thread and executes them.

6. **I/O or TQ based context switching is done here as well.**
   - **TCB (Thread control block):** It is like the PCB. It stores state during context switching.
     - Every thread has its own TCB, which holds the thread's own program counter.

7. **Does a single CPU system gain from multi-threading?**
   - **Never.**
   - Two threads have to context switch for that single CPU. The work is effectively sequential. Parallelism is not achieved.
   - **Best solution:** Use multi-threading only on multi-core systems (more CPUs). T1 runs on CPU 1 while T2 runs on CPU 2, independently.

8. **Benefits of Multi-threading.**
   - **Responsiveness**
     - **Example:** An interactive app takes user input, does I/O, fetches from the internet, syncs to the cloud, and runs a backup in the background. Each is an independent path. Divide them into threads.
     - If one thread is blocked on I/O (for example waiting for keyboard input), the other threads keep working. The process is not blocked.
     - Without threads, everything is sequential.
   - **Resource sharing:** Resource sharing is efficient.
     - **If tasks were processes:** They would need IPC (inter-process communication, via shared memory or message passing). Because of isolation between processes, establishing that communication is a big overhead.
     - **With threads:** They share the address space and the resources of their process. Sharing has the least overhead.
   - **Economy:** It is more economical to create and context switch threads.
     1. Allocating memory and resources for process creation is costly. So it is better to divide tasks into threads of the same process.
     - Context switching between processes is slower than between threads.
     - Creating a process needs separate resources and space. Threads come out of the resources already allocated to the process.
   - **Scalability:** Threads allow utilization of multiprocessor architectures to a greater scale and efficiency.
     - **Example:** With an 8-core (octa-core) CPU, one process can be divided into 8 independent tasks, one per CPU.
     - See the JPG-to-PNG converter example from Lecture 3.

## Hands-on: multi-threaded C++ program

- **Setup:** A process with two independent tasks, Task A and Task B (two functions). Each runs a loop that prints something, with `sleep(1)` in the loop.
- **Header:** Include `<thread>`.
- **Create T1:** `std::thread t1(taskA);` creates thread T1 that runs Task A. Arguments go after a comma: `std::thread t1(taskA, arg1, ...);`.
- **Create T2:** `std::thread t2(taskB);` creates thread T2 that runs Task B.

```cpp
#include <iostream>
#include <thread>
#include <unistd.h>
using namespace std;

void taskA() {
    for (int i = 0; i < 10; ++i) {
        sleep(1);
        printf("TaskA: %d\n", i);
        fflush(stdout);
    }
}

void taskB() {
    for (int i = 0; i < 10; ++i) {
        sleep(1);
        printf("TaskB: %d\n", i);
        fflush(stdout);
    }
}

int main() {
    thread t1(taskA);
    thread t2(taskB);

    t1.join();
    t2.join();
    return 0;
}
```

- **Three threads:** The main thread (`int main`) plus T1 and T2. Once launched, T1 and T2 work independently.
- **Without `join()`:** The main thread reaches the end and exits immediately. The program terminates with an error ("terminate called ..."), because the parent of T1 and T2 has gone.
- **`t1.join()`:** The main thread waits until T1 completes. The same holds for `t2.join()`.
- **With `join()`:** Both tasks run in parallel. On an 8-core machine, T1 probably got CPU 1 and T2 got CPU 2. T1 was launched first, so it was scheduled first. The outputs are interleaved.
- This is how one process is divided into threads to get the benefit of concurrency (multi-threading).
