# Lecture 4: Components of OS

An OS is made of two components: the **user space** and the **kernel** (kernel space).

- These map to the two jobs of an OS: the kernel does the hardware interaction; the user space gives users/developers a convenient environment to run their apps.
- Only the kernel has access to the underlying hardware. Apps run in the user space.
- User space interacts with the kernel; the kernel interacts with the hardware. User space + kernel together make the OS.

```
+--------------------+  -+
|     User space     |   |
+--------------------+   |  OS
|       Kernel       |   |
+--------------------+  -+
|      Hardware      |
+--------------------+
```

1. **Kernel:** A **kernel** is that part of the operating system which interacts directly with the hardware and performs the most crucial tasks.
   a. Heart of OS/Core component
   b. Very first part of OS to load on start-up.
      - When the OS is started, the kernel is the first component of the OS that comes up.
   - User space sends a command; the kernel reads it and gets that particular work done by the hardware.
   - User space has no direct hardware access, so it must request the kernel to get any hardware work done.
2. **User space:** Where application software runs, apps don't have privileged access to the underlying hardware. It interacts with kernel.
   a. GUI
      - Graphical User Interface. E.g. the Windows/Mac desktop with the Start button and icons; you click with the mouse to run an app.
   b. CLI
      - Command Line Interface. You type commands and they get executed.
   - Anything done through the GUI can also be done through the CLI. E.g. to make a new folder: right-click → New Folder in Windows, or run `mkdir` on the CLI.
   - The GUI's "New Folder" button internally runs the same `mkdir` command. `mkdir` in turn calls system calls, which ask the file management part of the kernel to create a directory.
   - Even the area where the user works has no direct hardware access; it still goes through the kernel. The OS is layered.
   - Example: a shell script `helloworld.sh` containing `echo "Hello World"`, run from the terminal as `./helloworld.sh`.
     - The terminal (CLI) where you run it is user space.
     - Printing needs some computation, so user space asks the kernel. The kernel requests CPU cycles from the CPU, the CPU does the computation, and "Hello World" appears as output on the command line.

A **shell**, also known as a command interpreter, is that part of the operating system that receives commands from the users and gets them executed.

- The shell is an implementation of the CLI.

## Functions of Kernel:

(A common interview question: list the functions of the kernel and explain each briefly.)

1. **Process management:**
   a. Scheduling processes and threads on the CPUs.
      - The user creates many processes (e.g. by double-clicking apps). The kernel decides how to run them on the CPU: maximum CPU utilisation, high-priority jobs get run, and no process starves.
      - Context switching and time sharing are also done by this part of the kernel.
   b. Creating & deleting both user and system process.
      - Process creation and termination.
   c. Suspending and resuming processes
   d. Providing mechanisms for process synchronization or process communication.
      - Any two processes P1 and P2 are isolated and have memory protection; they execute independently. Sometimes they still need to communicate or share information; the kernel provides the mechanism for this.
2. **Memory management:**
   a. Allocating and deallocating memory space as per need.
      - E.g. how to allocate/deallocate memory inside a 2 GB RAM.
   b. Keeping track of which part of memory are currently being used and by which process.
      - Free space management: processes exit now and then, and their memory areas become free. The kernel tracks which areas are free, because new jobs need space too.
3. **File management:**
   a. Creating and deleting files.
   b. Creating and deleting directories to organize files.
      - The OS keeps files and directories on the disk in a hierarchical, tree-like structure (like an n-ary tree).
      - E.g. in Linux: the root directory `/` (position zero of the disk), sub-directories under it (e.g. `lakshay`, `ramesh`), and further folders and files inside them (e.g. `lakshay/os/`, `lakshay/abcd/`, `lakshay.txt`).
      - A tree makes searching easy: go down into the right directory and search there. This is a real-life use of the tree data structure.

        ```
        /
        ├── lakshay
        │   ├── os
        │   ├── abcd
        │   └── lakshay.txt
        └── ramesh
        ```
   c. Mapping files into secondary storage.
   d. Backup support onto a stable storage media.
4. **I/O management:** to manage and control I/O operations and I/O devices
   - E.g. you plug in a game controller or a USB pen drive. The kernel detects it at the hardware level, notifies you that the device is connected, and provides a way to access it (e.g. via My Computer).
   - The kernel reads the device from the hardware and sends the information to user space; user space then lets you access the device through the GUI.
   a. Buffering (data copy between two devices), caching and spooling.
      i. Spooling
         1. Within differing speed two jobs.
         2. Eg. Print spooling and mail spooling.
         - Data is saved (spooled) in some storage area beforehand, between two jobs of different speeds.
         - E.g. you give the printer 10 PDFs to print at once. The jobs arrive fast but the printer prints slowly, so all 10 jobs are spooled into storage and printed one by one.
      ii. Buffering
         1. Within one job.
         2. Eg. Youtube video buffering
         - Inside one process, data that will be used shortly is loaded and kept ready in a buffer beforehand.
      iii. Caching
         1. Memory caching, Web caching etc.

## Types of Kernels:

1. Monolithic kernel
   a. All functions are in kernel itself.
      - All four functions (process, memory, file, I/O management) are centralised inside the kernel.
      - The oldest type of kernel; early kernels were all of this type.

      ```
      +--------------------------------------+
      |              User space              |
      +--------------------------------------+
      | Kernel: Process mgmt.  Memory mgmt.  |
      |         File mgmt.     I/O mgmt.     |
      +--------------------------------------+
      |               Hardware               |
      +--------------------------------------+
      ```
   b. Bulky in size.
      - A lot of code sits inside the kernel.
   c. Memory required to run is high.
   d. Less reliable, one module crashes -> whole kernel is down.
      - All modules are highly coupled in one place. If e.g. the memory management module crashes, the whole kernel goes down.
   e. High performance as communication is fast. (Less user mode, kernel mode overheads)
      - All modules are in the same space, so communication between the different components of the kernel is fast, with no overhead.
      - **User mode and kernel mode:** two separate "worlds" inside the OS. In kernel mode the CPU has direct hardware access; user mode is separate and interacts with the user. The OS keeps them apart. When the CPU is in user mode it does only user-mode work; when it switches to kernel mode it does kernel work.
      - The switch between user mode and kernel mode is done through a **software interrupt**.
      - **Interrupt:** a sudden notification that stops the current work so something else is handled first (like your father walking in while you study and telling you to drop everything and go do something).
        - Hardware interrupt: generated by hardware. E.g. the RAM suddenly fails or a part of it gets corrupted; it sends an interrupt that tells the OS, and execution has to stop.
        - Software interrupt: an interrupt generated by software, i.e. by the OS itself, not by hardware.
      - Example of switching: you type `mkdir` in the CLI → you are in user mode. On pressing Enter, the command is decoded; making a folder is file management's job, so the CPU switches to kernel mode and goes to the file management part of the kernel. The directory is created, the result ("making of directory has been successful") is returned, and the CPU switches back to user mode.
      - Every switch between the two modes costs time (a kind of context switch). In a monolithic kernel, the kernel's modules talk to each other without such switches.
   f. Eg. Linux, Unix, MS-DOS.
2. Micro Kernel
   a. Only major functions are in kernel.
      i. Memory mgmt.
      ii. Process mgmt.
      - The core functions, those with the most hardware interaction, stay in the kernel: memory management is related to RAM, process management to the CPU.
   b. File mgmt. and IO mgmt. are in User-space.

      ```
      +--------------------------------------+
      | User space:   File mgmt.  I/O mgmt.  |
      +--------------------------------------+
      | Kernel space: Memory mgmt.           |
      |               Process mgmt.          |
      +--------------------------------------+
      |               Hardware               |
      +--------------------------------------+
      ```
   c. smaller in size.
      - Less bulky than monolithic.
   d. More Reliable
      - If file management or I/O management crashes or gets corrupted, the kernel keeps running, since the main functions are in the kernel. Risk of a crash is reduced.
   e. More stable
      - More reliable → crashes less → more stable.
   f. Performance is slow.
   g. Overhead switching b/w user mode and kernel mode.
      - E.g. a process starts in user mode. It goes to process management (kernel mode) to be allocated resources, then memory management (kernel mode) for memory. It then needs to read from a USB, so it switches to user mode for I/O management. It then needs memory allocation/deallocation again → back to kernel mode. Then it must write a file → file management → back to user mode.
      - User → kernel → user → kernel → user: every switch has a cost (time), so the overhead piles up and performance drops.
      - So micro kernel is less bulky, more reliable and stable, but slower. Neither monolithic nor micro is clearly better, which leads to the hybrid kernel.
   h. Eg. L4 Linux, Symbian OS, MINIX etc.
      - L4 Linux is a type of Linux.
3. Hybrid Kernel:
   - When two extreme options each have advantages the other lacks, the easiest fix is to merge them: take the good parts of both (accepting small drawbacks) and build a hybrid.
   a. Advantages of both worlds. (File mgmt. in User space and rest in Kernel space. )
      - Rest = process management, memory management and I/O management. Compared to micro kernel, I/O management is moved back into the kernel.

      ```
      +--------------------------------------+
      | User space:   File mgmt.             |
      +--------------------------------------+
      | Kernel space: Process mgmt.          |
      |               Memory mgmt.  I/O mgmt.|
      +--------------------------------------+
      |               Hardware               |
      +--------------------------------------+
      ```
   b. Combined approach.
   c. Speed and design of mono.
      - Only one part (file management) is in user space, so the user mode/kernel mode switching overhead is reduced and speed increases.
   d. Modularity and stability of micro.
      - Some loopholes remain: if e.g. I/O management crashes, the kernel still goes down.
   e. Eg. MacOS, Windows NT/7/10
      - Windows 7 onwards are all called Windows NT. Today's market leaders (Mac and Windows) use this approach.
   f. IPC also happens but lesser overheads
4. Nano/Exo kernels…
   - Not very important from the interview point of view; read up on them on your own.

**Q.** How will communication happen between user mode and kernel mode?

- Interview question. E.g. in a micro kernel, file management runs as a process in user mode and memory management runs in kernel mode. How does a process of file management communicate with a process of memory management?

**Ans.** Inter process communication (**IPC**).

- The method is provided by the OS (its process management part).

1. Two processes executing independently, having independent memory space (Memory protection), But some may need to communicate to work.
   - Each process runs in isolation with its own resources and memory space; neither knows the other exists in memory.
2. Done by shared memory and message passing.
   - **Shared memory:** keep a block of memory between the two processes, P1 (say in user mode) and P2 (say in kernel mode). P1 writes its data (e.g. `123`) into the shared block; then P2 comes and reads `123` from it. The message has been passed through the shared memory.

     ```
     P1 --write "123"--> [ shared memory block ] --read "123"--> P2
     ```
   - **Message passing:** a logical pipe (a channel, not a physical pipe) is set up between the two processes and they communicate through it. The OS provides calls/functions for this (system calls, covered later). Communication follows protocols/policies using system calls; not any process can just talk to any other.

     ```
     P1 <====== logical pipe (via system calls) ======> P2
     ```
   - Both methods are supported and used in different scenarios.
