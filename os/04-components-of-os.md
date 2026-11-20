# Lecture 4: Components of OS

An OS is made of two components: the **user space** and the **kernel** (kernel space).

- **Two jobs:** The kernel does the hardware interaction. The user space gives users and developers an environment to run their apps.
- **Hardware access:** Only the kernel has access to the underlying hardware. Apps run in the user space.
- **Layers:** User space interacts with the kernel. The kernel interacts with the hardware.

```
+--------------------+  -+
|     User space     |   |
+--------------------+   |  OS
|       Kernel       |   |
+--------------------+  -+
|      Hardware      |
+--------------------+
```

1. **Kernel:** The kernel is the part of the operating system that interacts directly with the hardware and performs the most crucial tasks.

   a. **Heart of the OS:** It is the core component.

   b. **First to load:** It is the very first part of the OS that comes up on start-up.

   - **How it works:** User space sends a command. The kernel reads it and gets that work done by the hardware.
   - **No direct access:** User space must request the kernel for any hardware work.

2. **User space:** This is where application software runs. Apps do not have privileged access to the hardware. User space interacts with the kernel.

   a. **GUI:** Graphical User Interface. Example: the Windows or Mac desktop with the Start button and icons. You click with the mouse to run an app.

   b. **CLI:** Command Line Interface. You type commands and they get executed.

   - **GUI and CLI:** Anything done through the GUI can also be done through the CLI. Example: to make a new folder, right-click and choose New Folder in Windows, or run `mkdir` on the CLI.
   - **Under the GUI:** The "New Folder" button internally runs the same `mkdir`. `mkdir` calls system calls, which ask the file management part of the kernel to create a directory.
   - **Layered OS:** Even the area where the user works has no direct hardware access. It goes through the kernel.
   - **Example:** A shell script `helloworld.sh` contains `echo "Hello World"` and runs as `./helloworld.sh`.
     - **User space:** The terminal (CLI) is user space.
     - **Kernel:** Printing needs computation, so user space asks the kernel. The kernel requests CPU cycles. The CPU computes and "Hello World" appears on the command line.

A **shell**, also known as a command interpreter, is the part of the operating system that receives commands from the users and gets them executed.

- **CLI:** The shell is an implementation of the CLI.

## Functions of Kernel

> **Interview:** A common question is to list the functions of the kernel and explain each briefly.

1. **Process management:**

   a. **Scheduling:** The kernel schedules processes and threads on the CPUs.
      - **Example:** The user creates many processes by double-clicking apps. The kernel decides how to run them on the CPU. It aims for maximum CPU utilisation, runs high-priority jobs and lets no process starve.
      - **Switching:** Context switching and time sharing are also done by this part of the kernel.

   b. **Create and delete:** The kernel creates and deletes both user and system processes. This covers process creation and termination.

   c. **Suspend and resume:** The kernel suspends and resumes processes.

   d. **Synchronization and communication:** The kernel provides mechanisms for process synchronization and process communication.
      - **Why:** Processes P1 and P2 are isolated, with memory protection, and execute independently. Sometimes they still need to share information. The kernel provides the mechanism.

2. **Memory management:**

   a. **Allocate and deallocate:** The kernel allocates and deallocates memory space as per need.
      - **Example:** How to allocate and deallocate memory inside a 2 GB RAM.

   b. **Tracking:** The kernel keeps track of which parts of memory are in use and by which process.
      - **Free space management:** Processes exit now and then, and their memory becomes free. The kernel tracks free areas, because new jobs need space.

3. **File management:**

   a. **Files:** Creating and deleting files.

   b. **Directories:** Creating and deleting directories to organize files.
      - **Structure:** The OS keeps files and directories on the disk in a hierarchical, tree-like structure, like an n-ary tree.
      - **Linux example:** The root directory `/` is position zero of the disk. Sub-directories sit under it, for example `lakshay` and `ramesh`. Folders and files sit inside them, for example `lakshay/os/`, `lakshay/abcd/` and `lakshay.txt`.
      - **Why a tree:** Searching is easy. You go down into the right directory. This is a real-life use of the tree data structure.

        ```
        /
        ├── lakshay
        │   ├── os
        │   ├── abcd
        │   └── lakshay.txt
        └── ramesh
        ```

   c. **Mapping:** Mapping files into secondary storage.

   d. **Backup:** Backup support onto a stable storage medium.

4. **I/O management:** The kernel manages and controls I/O operations and I/O devices.
   - **Example:** You plug in a game controller or a USB pen drive. The kernel detects it at the hardware level, notifies you and provides a way to access it, for example through My Computer.
   - **Flow:** The kernel reads the device from the hardware and sends the information to user space. User space lets you access it through the GUI.

   a. **Buffering, caching and spooling:** Buffering is a data copy between two devices.

      i. **Spooling:**
         1. It works between two jobs of differing speed.
         2. Examples: print spooling and mail spooling.
         - **Idea:** Data is saved (spooled) in a storage area beforehand, between two jobs of different speeds.
         - **Example:** You give the printer 10 PDFs at once. The jobs arrive fast and the printer is slow. All 10 are spooled into storage and printed one by one.

      ii. **Buffering:**
         1. It works within one job.
         2. Example: YouTube video buffering.
         - **Idea:** Inside one process, data that will be used shortly is loaded and kept ready in a buffer.

      iii. **Caching:**
         1. Examples: memory caching and web caching.

## Types of Kernels

### 1. Monolithic kernel

a. **All functions in the kernel:** All four functions (process, memory, file and I/O management) are centralised inside the kernel.
   - **Oldest type:** Early kernels were all of this type.

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

b. **Bulky in size:** A lot of code sits inside the kernel.

c. **High memory needed:** The memory required to run is high.

d. **Less reliable:** If one module crashes, the whole kernel is down.
   - **Why:** All modules are highly coupled in one place. If the memory management module crashes, the whole kernel goes down.

e. **High performance:** Communication is fast. There is less user mode and kernel mode overhead.
   - **Why:** All modules are in the same space, so communication between kernel components is fast.
   - **User mode and kernel mode:** These are two separate worlds inside the OS. In kernel mode the CPU has direct hardware access. User mode is separate and interacts with the user. In user mode the CPU does only user-mode work. In kernel mode it does kernel work.
   - **Switching:** The switch between the modes is done through a **software interrupt**.
   - **Interrupt:** It is a sudden notification that stops the current work so something else is handled first. **Analogy:** your father walks in while you study and tells you to drop everything and go do something.
     - **Hardware interrupt:** It is generated by hardware. Example: the RAM suddenly fails or gets corrupted. It sends an interrupt that tells the OS, and execution has to stop.
     - **Software interrupt:** It is generated by software, meaning by the OS itself.
   - **Switching example:** You type `mkdir` in the CLI, so you are in user mode. On Enter, the command is decoded. Making a folder is file management's job, so the CPU switches to kernel mode and goes to the file management part. The directory is created. The result ("making of directory has been successful") is returned. The CPU switches back to user mode.
   - **Cost:** Every mode switch costs time. It is a kind of context switch. In a monolithic kernel, the modules talk to each other without such switches.

f. **Examples:** Linux, Unix, MS-DOS.

### 2. Micro kernel

a. **Only major functions in the kernel:**
   - i. Memory management.
   - ii. Process management.
   - **Why these:** They have the most hardware interaction. Memory management relates to RAM. Process management relates to the CPU.

b. **File management and I/O management are in user space.**

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

c. **Smaller in size:** It is less bulky than monolithic.

d. **More reliable:** If file management or I/O management crashes or gets corrupted, the kernel keeps running, because the main functions are in the kernel. The risk of a crash is reduced.

e. **More stable:** More reliable means it crashes less, so it is more stable.

f. **Slow performance.**

g. **Overhead switching between user mode and kernel mode:**
   - **Example:** A process starts in user mode. It goes to process management (kernel mode) for resources, then memory management (kernel mode) for memory. It reads from a USB, so it switches to user mode for I/O management. It needs memory again, so it goes back to kernel mode. Then it writes a file, so it goes to file management in user mode.
   - **Chain:** The path is user, kernel, user, kernel, user. Every switch costs time. The overhead piles up and performance drops.
   - **Summary:** The micro kernel is less bulky, more reliable and stable, but slower. Neither monolithic nor micro is clearly better. This leads to the hybrid kernel.

h. **Examples:** L4 Linux, Symbian OS, MINIX and others.
   - **L4 Linux:** It is a type of Linux.

### 3. Hybrid kernel

When two extreme options each have advantages the other lacks, the easiest fix is to merge them. Take the good parts of both, accept small drawbacks, and build a hybrid.

a. **Advantages of both worlds:** File management is in user space and the rest is in kernel space.
   - **Rest:** Process management, memory management and I/O management. Compared to the micro kernel, I/O management moves back into the kernel.

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

b. **Combined approach.**

c. **Speed and design of monolithic:** Only file management is in user space, so the mode switching overhead is reduced and speed increases.

d. **Modularity and stability of micro:** Some loopholes remain. If I/O management crashes, the kernel still goes down.

e. **Examples:** MacOS, Windows NT/7/10.
   - **Windows NT:** Windows 7 onwards are all called Windows NT. Today's market leaders (Mac and Windows) use this approach.

f. **IPC:** It also happens, but with lower overheads.

### 4. Nano and Exo kernels

- **Interview relevance:** They are not very important for interviews. Read up on them on your own.

## Communication between user mode and kernel mode

**Q.** How does communication happen between user mode and kernel mode?

> **Interview:** This is a common question. In a micro kernel, file management runs as a process in user mode and memory management runs in kernel mode. How do they communicate?

**Ans.** Inter process communication (**IPC**).

- **Provided by:** The OS provides the method, through its process management part.

1. **Independent processes:** Two processes execute independently and have independent memory space (memory protection). But some need to communicate to work.
   - **Isolation:** Each process runs in isolation with its own resources and memory space. Neither knows the other exists in memory.

2. **Two methods:** IPC is done by shared memory and message passing.
   - **Shared memory:** A block of memory is kept between P1 (say in user mode) and P2 (say in kernel mode). P1 writes its data (for example `123`) into the block. P2 reads `123` from it.

     ```
     P1 --write "123"--> [ shared memory block ] --read "123"--> P2
     ```

   - **Message passing:** A logical pipe is set up between the two processes, and they communicate through it. It is a channel, not a physical pipe. The OS provides calls for this, which are system calls, covered later. Communication follows protocols and policies using system calls. Not any process can talk to any other.

     ```
     P1 <====== logical pipe (via system calls) ======> P2
     ```

   - **Use:** Both methods are supported and used in different scenarios.
