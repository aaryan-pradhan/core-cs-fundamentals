# Lecture 3: Multi-Tasking vs Multi-Threading

A very common interview question: explain multiprogramming, multiprocessing, multitasking and multithreading, and the differences between them. Multiprogramming, multiprocessing and multitasking were covered in the previous lecture (types of OS). This lecture adds multithreading. To understand a thread, first understand a process; to understand a process, first understand a program.

**Program**: A Program is an executable file which contains a certain set of instructions written to complete the specific job or operation on your computer.

- It's a compiled code. Ready to be executed.
- Stored in Disk
- E.g. you write C++ code to find prime numbers in a `.cpp` file. That file is just text (a collection of characters).
- The compiler compiles the `.cpp` code and produces an executable (e.g. a `.exe` file on Windows).
- Open the executable in a text editor and you cannot read any code: it is compiled code, raw bits and bytes, meant to be run by the OS.
- The executable is platform dependent: a Mac executable differs from a Windows one.

**Process**: Program under execution. Resides in Computer's primary memory (RAM).

- E.g. double-click the MS Paint `.exe` and a big window opens; Task Manager now shows a process named MS Paint. Any `.exe`, when double-clicked, turns into a process.
- "Under execution" means brought into memory. The program sits on disk, but the CPU cannot work on it until it is loaded into actual memory (RAM). On double-click, the program is loaded from disk into RAM; the program in RAM is called a process.
- How a process is created and what the OS does while creating it comes later, in Process Management.

**Thread**:

- Single sequence stream within a process.
- An independent path of execution in a process.
- Light-weight process.
- Used to achieve parallelism by dividing a process's tasks which are independent path of execution.
- E.g., Multiple tabs in a browser, text editor (When you are typing in an editor, spell-checking, formatting of text and saving the text are done concurrently by multiple threads.)

More on threads:

1. A big program (a whole software) is made of many small steps: take input, fetch data from the network, read from disk, run the processing logic, do I/O, and so on. A thread is the smallest unit of work inside it that can execute independently.
2. Example (app saving to cloud): an app takes details from the user, processes them and shows them on the display. Meanwhile it also writes the same data to the user's profile on the cloud.
   - Writing to the cloud does not depend on the main work (take input, process, display); the user does not need to know it is happening in the background.
   - So the process is split in two: the main flow, plus a sub-task that writes to the cloud. That independent sub-task is given to a thread.
   - "Thread" is just the name for a way to get one independent piece of work done inside a process.
3. Example (JPG to PNG converter):
   - The conversion logic takes a 100 x 100 pixel JPG and outputs a 100 x 100 pixel PNG. It can handle only 100 x 100 at a time.
   - Input image is 100 x 200 (width 100, height 200). Break it into part A and part B, each 100 x 100.
   - **Sequential way**: the program converts A to get A1 (first iteration), stores it, then converts B to get B1 (second iteration), then concatenates A1 and B1.
   - The conversion logic is an independent execution, a single sequence stream: it takes data and outputs data, with no dependency on anything else.
   - **Multithreaded way**: divide the process into two threads T1 and T2. T1 converts A into A1; T2 converts B into B1, both using the same conversion logic. The two have no dependency and no communication with each other.
   - Time: if one 100 x 100 conversion takes 10 seconds, sequential takes 10 + 10 = 20 seconds. With two threads running in parallel, both finish in 10 seconds. Multithreading made the code faster.
4. Multithreading gives a real gain only with more than one CPU:
   - Ideally CPU 1 executes T1 and CPU 2 executes T2, in parallel.
   - With a single CPU you can still write multithreaded code, but no second CPU is available, so the work effectively runs sequentially (the threads just context switch). No gain.
   - So multithreading benefits a multiprocessing environment (more than one CPU). Modern systems are multiprocessing, with many CPUs/cores. Cores can be thought of as logical CPUs.
5. A process with tasks A, B, C that run independently can be divided into three threads T1, T2, T3. Threads are like children of the process.
6. Threads use the same memory and resources that the OS gave their process. If the OS gave process P1 one part of memory, T1, T2, T3 all work inside that same part.
7. The OS provides isolation between two processes, but there is no isolation between threads of the same process. They are parts of the same process, and one thread may even use another thread's work. So the OS's isolation and memory protection do not apply between threads.
8. Browser tabs: clicking for a new tab opens a tab like the previous one, in which you open google.com or another site; each tab is handled by a thread.
9. Text editor (e.g. Notepad or Word): while you type, the editor takes your keystrokes as input and at the same time checks spelling, checks types and formats the text. Actual typing, spell-checking, formatting and background auto-save are each sub-tasks of the same writing process, each done by a different thread, concurrently.
10. Without multithreading (a single process doing it all sequentially): you type "My name is Lakshay"; while typing, spell-check and formatting do not run at all. Then the process does the tasks one by one: typing, then spell-check, then formatting, then save. Until all four finish, you cannot get back to typing. This is why multithreading is needed.

## Multi-Tasking vs Multi-Threading

| Multi-Tasking | Multi-Threading |
|---|---|
| The execution of more than one task simultaneously is called as multitasking. | A process is divided into several different sub-tasks called as threads, which has its own path of execution. This concept is called as multithreading. |
| Concept of more than 1 processes being context switched. | Concept of more than 1 thread. Threads are context switched. |
| No. of CPU 1. | No. of CPU >= 1. (Better to have more than 1) |
| **Isolation and memory protection** exists. OS must allocate separate memory and resources to each program that CPU is executing. | **No isolation and memory protection**, resources are shared among threads of that process. OS allocates memory to a process; multiple threads of that process share the same memory and resources allocated to the process. |

1. Concept:
   - Multitasking: many processes time-share one CPU; the CPU keeps switching between processes (the "task" here is a process), scheduling them by time sharing and context switching.
   - Multithreading: one task (process) is divided into sub-tasks, i.e. light-weight processes. Each does an independent execution of a workflow. Many threads of the same process are scheduled.
2. Context switching: in multitasking, processes are context switched. In multithreading, threads of one process are context switched.
3. Number of CPUs:
   - Multithreading on 1 CPU: the threads of one process just context switch among themselves (thread 1 runs, then thread 2, then thread 3). The code runs, but there is no gain; the real purpose is not fulfilled.
   - Gain comes only with more than 1 CPU (or core), where each CPU picks up one thread and runs it.
   - Interview question: how many CPUs/threads should multithreading use? As many threads as the hardware supports. If the hardware has 4 cores (4 logical CPUs/processors), dividing the program into 4 threads is good coding practice: number of threads = number of cores.
   - Interview question: if multithreading is so good, why not divide a process into 1, 2 or 3 lakh threads? The code will run, but you do not have that many cores (even a recent MacBook Air has only 8 cores). Design the code and spawn threads based on the number of cores. Multithreading does not mean creating as many threads as possible.
4. Isolation and memory protection:
   - Multitasking is between separate processes. Each process runs as a separate entity in its own memory block; the OS ensures each process gets its own, independently allocated memory block.
   - Multithreading: a thread is part of a process, so all its threads use the same memory block that the OS allocated to the process. Any other resources the OS allocated to the process are also shared by its threads.

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

5. Scheduling:
   - Multitasking: processes are scheduled to CPUs (e.g. CPU 1 runs P1, CPU 2 runs P2).
   - Multithreading: threads within a process are scheduled (e.g. T1 goes to CPU 1, T2 goes to CPU 2).
6. The interviewer may build on this and ask about multiprogramming vs multitasking, or multiprocessing vs multitasking, to check that all of these are clear (see the previous lecture).

## Thread Scheduling:

Threads are scheduled for execution based on their priority. Even though threads are executing within the runtime, all threads are assigned processor time slices by the operating system.

- Processes are scheduled on a CPU one after another (P1 runs, then P2). Threads are scheduled in a similar way; the OS does the scheduling, depending on priority.
- E.g. process P1 creates threads T1 and T2. Creating a thread is called **spawning** a thread.
- When spawning threads you give each a priority: T1 higher, T2 higher, or both the same (then the default behaviour applies).
- The CPU comes back to execute P1 every so often, i.e. some CPU time is allocated to P1. Within P1, the thread with the higher priority (say T1) gets more of that time.

## Difference between Thread Context Switching and Process Context Switching:

| Thread Context switching | Process context switching |
|---|---|
| OS saves current state of thread & switches to another thread of same process. | OS saves current state of process & switches to another process by restoring its state. |
| Doesn't includes switching of memory address space. (But Program counter, registers & stack are included.) | Includes switching of memory address space. |
| Fast switching. | Slow switching. |
| CPU's cache state is preserved. | CPU's cache state is flushed. |

1. Context switching in both cases means: save the current state, then restore the state of the next thread or process.
2. Memory address space: the memory address space is the area of RAM (the addresses) a process works in. Threads of one process use the same memory area, so a thread switch does not change it; a process switch does, because isolation and memory protection give different processes different memory blocks.
3. Speed: switching the memory address space is the heaviest part of a context switch. A thread switch skips it, so it is faster; a process switch is comparatively slow.
4. Cache:
   - Cache is a separate physical storage, faster than RAM. (Covered in detail later.)
   - E.g. a program keeps referring to a hash table throughout its code. The OS puts that hash table in the cache, so accesses become much faster and the whole process speeds up.
   - A process has one cache area. When another process comes in, the cached items must be removed: they belong to the previous program, and the new process may not use that hash table at all (it does not know what the first process had).
   - Thread switch: same process, same memory area, so the cache is not flushed; the next thread may use it. CPU cache state is preserved.
   - Process switch: CPU cache state is flushed.
5. Threads can feel confusing at first. They come up again in detail in Process Management, and are very important from the interview perspective.
