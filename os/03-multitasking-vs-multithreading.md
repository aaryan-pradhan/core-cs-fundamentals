# Lecture 3: Multi-Tasking vs Multi-Threading

> **Interview:** A very common question is to explain multiprogramming, multiprocessing, multitasking and multithreading, and the differences between them. The first three were covered in the previous lecture (types of OS). This lecture adds multithreading.

To understand a thread, first understand a process. To understand a process, first understand a program.

## Program

A **program** is an executable file. It holds a set of instructions written to complete a specific job on your computer.

- **Compiled code:** It is ready to be executed.
- **Storage:** It is stored on disk.
- **Example:** C++ code to find prime numbers in a `.cpp` file is just text. The compiler produces an executable, such as a `.exe` file on Windows.
- **Not readable:** In a text editor an executable is raw bits and bytes, meant to be run by the OS.
- **Platform dependent:** A Mac executable differs from a Windows one.

## Process

A **process** is a program under execution. It resides in the computer's primary memory (RAM).

- **Example:** Double-click the MS Paint `.exe` and Task Manager shows a process named MS Paint. Any `.exe` turns into a process when double-clicked.
- **Under execution:** It means brought into memory. The CPU cannot work on a program on disk until it is loaded into RAM. The program in RAM is called a process.
- **Creation:** How a process is created, and what the OS does meanwhile, comes later in Process Management.

## Thread

- **Single sequence stream:** A thread is a single sequence stream within a process.
- **Independent path:** It is an independent path of execution in a process.
- **Light-weight process:** A thread is also called a light-weight process.
- **Purpose:** Threads achieve parallelism by dividing a process's tasks into independent paths of execution.
- **Examples:** Multiple tabs in a browser. A text editor: while you type, spell-checking, formatting and saving run concurrently on multiple threads.

### More on threads

1. **Definition:** A big program is made of many small steps, such as taking input, fetching data from the network, reading from disk, running the processing logic and doing I/O. A thread is the smallest unit of work inside it that can execute independently.

2. **Example (app saving to cloud):** An app takes details from the user, processes them and shows them on the display. Meanwhile it also writes the same data to the user's profile on the cloud.
   - **Independent:** Writing to the cloud does not depend on the main work (take input, process, display). The user need not know it is happening.
   - **Split:** The main flow is one part. The cloud write is an independent sub-task given to a thread.
   - **Name:** "Thread" is just the name for a way to get one independent piece of work done inside a process.

3. **Example (JPG to PNG converter):** The conversion logic converts only 100 x 100 pixels at a time. The input image is 100 x 200 (width 100, height 200). Break it into part A and part B, each 100 x 100.
   - **Sequential way:** Convert A to A1 (first iteration) and store it. Convert B to B1 (second iteration). Concatenate A1 and B1.
   - **Independent logic:** The conversion logic is an independent single sequence stream. It takes data and outputs data, with no other dependency.
   - **Multithreaded way:** Divide the process into threads T1 and T2. T1 converts A into A1. T2 converts B into B1. Both use the same logic. They have no dependency and no communication with each other.
   - **Time:** If one conversion takes 10 seconds, sequential takes 10 + 10 = 20 seconds. Two parallel threads finish in 10 seconds.

4. **Gain needs more than one CPU:**
   - **Ideal case:** CPU 1 executes T1 and CPU 2 executes T2, in parallel.
   - **Single CPU:** You can write multithreaded code, but there is no second CPU. The threads just context switch, so the work runs sequentially. There is no gain.
   - **Conclusion:** Multithreading benefits a multiprocessing environment (more than one CPU). Modern systems have many CPUs or cores. Cores can be thought of as logical CPUs.

5. **Children of a process:** A process with independent tasks A, B and C can be divided into threads T1, T2 and T3. Threads are like children of the process.

6. **Shared memory:** Threads use the same memory and resources that the OS gave their process. If the OS gave P1 one part of memory, T1, T2 and T3 all work inside it.

7. **No isolation between threads:** The OS isolates two processes. There is no isolation between threads of the same process. They are parts of one process, and one thread may even use another thread's work. The OS's isolation and memory protection do not apply between threads.

8. **Browser tabs:** Each new tab, where you open google.com or another site, is handled by a thread.

9. **Text editor (Notepad or Word):** While you type, the editor takes keystrokes and at the same time checks spelling, checks types and formats the text. Typing, spell-checking, formatting and background auto-save are sub-tasks of the same writing process. Each is done by a different thread, concurrently.

10. **Without multithreading:** A single process does everything sequentially. You type "My name is Lakshay". While typing, spell-check and formatting do not run at all. Then the process does typing, spell-check, formatting and save one by one. Until all four finish, you cannot get back to typing. This is why multithreading is needed.

## Multi-Tasking vs Multi-Threading

| | Multi-Tasking | Multi-Threading |
|---|---|---|
| **Meaning** | The execution of more than one task simultaneously. | A process is divided into several sub-tasks called threads. Each has its own path of execution. |
| **Context switching** | More than one process is context switched. | More than one thread exists. Threads are context switched. |
| **No. of CPUs** | 1 | 1 or more. It is better to have more than 1. |
| **Isolation and memory protection** | **Exists.** The OS must allocate separate memory and resources to each program the CPU is executing. | **Does not exist.** Resources are shared among the threads of that process. The OS allocates memory to a process. Its threads share the same memory and resources. |

1. **Concept:**
   - **Multitasking:** Many processes time-share one CPU. The CPU keeps switching between processes. The "task" here is a process. Processes are scheduled by time sharing and context switching.
   - **Multithreading:** One task (process) is divided into sub-tasks, which are light-weight processes. Each does an independent execution of a workflow. Many threads of the same process are scheduled.

2. **Context switching:** In multitasking, processes are context switched. In multithreading, threads of one process are context switched.

3. **Number of CPUs:**
   - **Multithreading on 1 CPU:** The threads of one process just context switch among themselves (thread 1, then thread 2, then thread 3). The code runs, but there is no gain. The real purpose is not fulfilled.
   - **Gain:** It comes only with more than 1 CPU (or core). Each CPU picks up one thread and runs it.

   > **Interview:** How many threads should multithreading use? As many as the hardware supports. With 4 cores (4 logical CPUs or processors), dividing the program into 4 threads is good practice. Number of threads equals number of cores.

   > **Interview:** If multithreading is so good, why not divide a process into 1, 2 or 3 lakh threads? The code will run, but you do not have that many cores. Even a recent MacBook Air has only 8. Spawn threads based on the number of cores. Multithreading does not mean creating as many threads as possible.

4. **Isolation and memory protection:**
   - **Multitasking:** It works between separate processes. Each runs as a separate entity in its own memory block. The OS ensures each process gets its own, independently allocated memory block.
   - **Multithreading:** A thread is part of a process. All its threads use the same memory block that the OS allocated to the process. Any other resources the OS allocated to the process are also shared.

```
              RAM
+-----------------------------+
| P1's memory                 |
|   T1, T2 work in this area  |
+-----------------------------+
| P2's memory                 |
+-----------------------------+
P1 and P2 are isolated from each other.
T1 and T2 share P1's area: no isolation between them.
```

5. **Scheduling:**
   - **Multitasking:** Processes are scheduled to CPUs. For example, CPU 1 runs P1 and CPU 2 runs P2.
   - **Multithreading:** Threads within a process are scheduled. For example, T1 goes to CPU 1 and T2 goes to CPU 2.

6. **Follow-up questions:** The interviewer may ask about multiprogramming vs multitasking, or multiprocessing vs multitasking, to check that all of these are clear (see the previous lecture).

## Thread Scheduling

Threads are scheduled for execution based on their priority. Even though threads execute within the runtime, the operating system assigns all threads processor time slices.

- **Same as processes:** Processes are scheduled on a CPU one after another (P1, then P2). Threads are scheduled in a similar way. The OS does the scheduling, depending on priority.
- **Spawning:** Process P1 creates threads T1 and T2. Creating a thread is called **spawning** a thread.
- **Priority:** When spawning, you give each thread a priority. T1 can be higher, T2 can be higher, or both the same. If both are the same, the default behaviour applies.
- **Time split:** The CPU comes back to P1 every so often, so P1 gets some CPU time. Within P1, the higher-priority thread (say T1) gets more of that time.

## Difference between Thread Context Switching and Process Context Switching

| | Thread context switching | Process context switching |
|---|---|---|
| **What happens** | The OS saves the current state of the thread and switches to another thread of the same process. | The OS saves the current state of the process and switches to another process by restoring its state. |
| **Memory address space** | Not switched. The program counter, registers and stack are included. | Switched. |
| **Speed** | Fast. | Slow. |
| **CPU cache** | The state is preserved. | The state is flushed. |

1. **Context switching:** In both cases it means saving the current state, then restoring the state of the next thread or process.

2. **Memory address space:** This is the area of RAM (the addresses) a process works in.
   - **Thread switch:** Threads of one process use the same memory area, so it does not change.
   - **Process switch:** It changes, because isolation and memory protection give different processes different memory blocks.

3. **Speed:** Switching the memory address space is the heaviest part of a context switch. A thread switch skips it, so it is faster. A process switch is comparatively slow.

4. **Cache:**
   - **What it is:** Cache is a separate physical storage, faster than RAM. It is covered in detail later.
   - **Example:** A program keeps referring to a hash table. The OS puts it in the cache, so accesses and the whole process speed up.
   - **Per process:** A process has one cache area. When another process comes in, the cached items must be removed. They belong to the previous program, and the new process may not use that hash table at all.
   - **Thread switch:** It is the same process and memory area, so the cache is not flushed. The next thread may use it.
   - **Process switch:** The CPU cache state is flushed.

5. **Importance:** Threads can feel confusing at first. They come up again in Process Management and are very important for interviews.
