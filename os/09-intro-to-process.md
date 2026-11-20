# Lecture 9: Introduction to Process

1. What is a program? It is compiled code that is ready to execute.
   - **How made:** You write code in a text file (for example `.cpp`). The compiler converts it to machine code and produces an executable. That executable is the program.
   - **Not ready:** The source text file is not ready to execute. The executable is.
   - **Location:** A program resides on disk, like a game until you double-click it.
2. What is a process? It is a program under execution.
   - **Conversion:** When a program is run, the OS converts it into a process.
   - **Unit of work:** A process is a unit of work done by a computer.
   - **Why a process:** It is the way a user gets work done by the computer. The user writes code, the compiler turns it into a program, and the OS turns the program into a process and executes it.
3. How does the OS create a process? It converts the program into a process.

   **Steps:**

   a. Load the program and static data into memory.
      - **Memory:** Here memory means RAM (main memory). The program's instructions and data are copied from disk into memory.
      - **Static data:** It is data used for initialisation, written in the program itself (not dynamically allocated).
      - **Example:** In `char *name = "Lakshay";` the string is static data. When the process creates the variable `name`, the OS must know what to initialise it with. So it copies this data and assigns it.
      - **Example:** In `int a = 0;` the value `0` used to initialise `a` is static data.

   b. Allocate the runtime stack.
      - **Stack:** It is the part of memory used for local variables, function arguments and return values.
      - **Why needed:** Function calls and recursion need it. When a function calls another, the caller's data is saved on the stack and control jumps to the called function.

   c. Allocate heap memory.
      - **Heap:** It is the part of memory for dynamic allocation.
      - **Use:** Data declared in code (`int a`, `int b`) is already there. At runtime the program may need more memory for a while. It asks the heap for it through `malloc` or `new`.

   d. Set up IO tasks.
      - **Unix:** After the above steps, three IO descriptors (handles) are created: input, output and errors.
      - **Input handle:** The process reads input from here.
      - **Output handle:** The program's output is written here.
      - **Error handle:** The program's errors go here.
      - **Example:** `fprintf(stderr, "...")`. The first argument of `fprintf` can be a file descriptor (to write into a file) or an error handle. `stderr` is the standard error handle. It prints the error on the console.

   e. The OS hands control to `main()`.
      - **Ready:** The OS has allocated sufficient stack and heap and handled IO. Now the program's instructions start executing.
      - **Why `main`:** Execution always starts from `main()` because the OS knows only `main`, not any other function.
      - **OS steps back:** Once the OS calls `main`, the process controls the CPU and the memory the OS allocated to it. The OS's job of creating the process is done.
      - **`return 0`:** Every process is created as a child of some parent process. Here, think of the parent as the OS. When the child finishes, the parent must know whether execution was successful. Then the programmer can, for example, show an error otherwise.
        - **Success:** `return 0` (or `exit(0)`) tells the OS the program executed successfully.
        - **Failure:** If the program exits earlier with, for example, `exit(-1)`, the OS sees that it did not return or exit 0. This means something went wrong. The program handles that error its own way.
4. **Architecture** of a process.

   The process as it sits logically in memory:

   ```
   ┌───────────────────┐
   │       Stack       │  Local variables, function arguments & return values
   │         │         │
   │         ▼         │  (stack grows down)
   │                   │
   │         ▲         │  (heap grows up)
   │         │         │
   │       Heap        │  Dynamically allocated variables
   ├───────────────────┤
   │       Data        │  Global & Static data
   ├───────────────────┤
   │       Text        │  Compiled code (Loaded from disk)
   └───────────────────┘
   ```

   - **Text:** It is the compiled code loaded from disk. An executable is still a file. Notepad shows strange characters, because it cannot read machine code.
   - **Data:** It holds global variables and static data. A global variable can be global to a file or to the whole program. For example, with external linkage a variable from one module is accessible in another.
   - **Heap and stack:** At the start, the OS keeps the stack and heap far apart, so each has sufficient space.
   - **Stack overflow:**
     - **Cause:** Each recursive call stores its variables on the stack and allocates another stack area for the next call with its arguments.
     - **No base case:** With no base case (exit condition), calls keep piling up and the stack keeps growing.
     - **Result:** After a certain limit, the stack meets the heap. Then the OS throws a stack overflow error before the whole memory gets corrupted.
   - **Out of memory error:** Some systems call it a memory insufficient error.
     - **Limit:** RAM is limited. Each process gets only a certain limit, since the OS has many processes.
     - **Languages:** Java has a garbage collector, so you need not free memory. C++ demands discipline. If you allocate on the heap, freeing it is your responsibility.
     - **Cause:** A developer keeps allocating on the heap (for example 100 MB at a time) and never frees it. At some point the heap touches the stack and an out of memory error is thrown.
   - **Both are "memory ran out" errors.** How to avoid them:

     - **Stack overflow:** In recursive calls, set a base case. Recursion then stops, returns, and unwinds the stack.
     - **Stack unwinding:** Each recursive call adds a level on the stack. When the base condition hits, the calls return one by one and the stack is freed back. Without unwinding, stack overflow occurs.
     - **Out of memory:** Deallocate unnecessary objects you allocated on the heap.
5. **Attributes** of a process.

   a. Attributes are features that identify a process uniquely.
      - **Why:** Many processes are loaded at once (P1, P2, ...). The OS tells them apart by attributes.

   b. Process table
      - i. The OS tracks all processes using a table-like data structure.
      - ii. Each entry in that table is a process control block (PCB).
      - **Manager:** The OS is a manager. It writes all processes (P1, P2, P4, ...) in the process table, so it knows which it currently has.

   c. PCB: It stores the information and attributes of a process.
      - i. It is a data structure used for each process. It stores information such as process id, program counter, process state, priority and so on.
      - **Own PCB:** Every process has its own PCB. The OS identifies a process only through its PCB. So logically the PCB is the process.
      - **Context switching:** It saves a process's data temporarily in its PCB. (Covered in the previous lecture.)
6. **PCB structure:**

   - **Data structure:** The exact data structure used for the PCB does not matter. Visualise it as blocks holding 7 types of information.
   - **Process ID:** It is the unique identifier. The OS runs a counter from 0 since boot. Each new process gets the next number (for example 23, then 24).
   - **Program Counter (PC):** It holds the next instruction address of the program.
     - **Instructions:** After compiling, a program becomes a collection of CPU instructions (for example an `ADD` instruction), at positions 0, 1, 2, ...
     - **CPU:** The CPU is "dumb". It just executes instructions in sequence as they are given.
     - **Start:** The OS associates a program counter with each process. It is initialised to 0, because the first instruction is at position 0.
     - **Role:** The PC stores the address of the instruction to run, like a pointer. It tracks where the process is. Without it, the CPU would not know the next instruction.
     - **Flow:**

       ```mermaid
       flowchart LR
           A["Fetch instruction from address in PC"] --> B["PC++"]
           B --> C["Execute instruction"]
           C --> A
       ```

     - **Walk-through:** The CPU checks the PC (say 1), fetches and decodes the instruction at address 1, increments the PC (now 2) and executes the instruction. Then it moves to address 2, and so on until the program terminates.
   - **Process State:** It is the current state of the process: new, wait, run (got the CPU, executing), and so on. (States are covered in the next lecture.)
   - **Priority:** A high priority job must be executed first. Its priority is written in its PCB. Based on it, the process gets CPU time and the CPU scheduler treats it.
   - **Registers:** The CPU has many registers, for example SP (stack pointer, points to the stack), BP (base pointer) and CR (control registers).
     - **Saved:** When running process P1 must go to wait state for IO, or its time quantum expires, the CPU register values are saved as-is into the PCB's registers block during the context switch.
     - **Restored:** When P1 is scheduled again, they are restored into the CPU registers.
   - **List of open files:** These are file descriptors (FDs) of files the process has opened to read or write.
   - **List of open devices:** These are device descriptors of devices (IO) the process has opened, for example to read from.
   - **Lookup:** Whenever the OS needs any information about a process, it finds it in that process's PCB.

**Registers in the PCB:**

- **Swap out:** When a running process's time slice expires, the current values of its process-specific registers are stored in the PCB. The process is swapped out.
- **Swap in:** When it is scheduled again, the values are read from the PCB and written to the CPU registers. This is the main purpose of the registers in the PCB.
