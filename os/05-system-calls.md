# Lecture 5: System Calls

**How do apps interact with Kernel?** -> using system calls.

- The OS has two separate spaces: user space (apps run here) and kernel space (core work happens here). Only the kernel has privileged access to hardware.
- An app that wants memory, CPU cycles or any hardware work must go to the kernel. Since user space and kernel space are separate, the OS gives a mechanism for them to communicate: system calls.
- Eg. `malloc`: the program needs some memory space, so it must switch from user mode to kernel mode; the system call makes that switch possible.
- Interview answer: "How do apps interact with kernel?" -> "System calls." Then expect to be asked for an example (the `mkdir` one below).

Eg. Mkdir laks

- Mkdir indirectly calls kernel and asked the file mgmt. module to create a new directory.
- Mkdir is just a wrapper of actual system calls.
- Mkdir interacts with kernel using system calls.
- Two ways to create a folder (eg. a "movies" folder):
  - GUI: right click -> New Folder, type the name. For standard users.
  - CLI: open a terminal and run `mkdir movies`.
  - Both do the same job: the GUI's New Folder button internally calls `mkdir` itself. The GUI only makes it look easy.
- What happens on `mkdir movies`:
  1. The command goes from user space to the **System Call Interface (SCI)**.
  2. The SCI is the entry point to kernel space. It finds the implementation corresponding to `mkdir` inside the kernel.
  3. Kernel space runs that implementation.
  4. The implementation goes to the current directory in the file system tree and adds a node named `movies` (eg. under root if run at root).
  5. Control returns to user space; the GUI now shows a folder named `movies`.

Eg. Creating a process.

- User executes a process. (User space)
- Gets system call. (US)
- Exec system call to create a process. (KS)
- Return to US.
- In detail (eg. running a compiled `hello world` executable):
  1. On run, it looks for the execution system call, which the SCI provides.
  2. The SCI switches to kernel mode.
  3. In kernel mode, process management creates the process: allocates memory for it in RAM, and the kernel also does any other work it needs (accessing hardware / I/O devices).
  4. Once the process is created, the kernel's work is over, so we switch back from kernel mode to user mode.
  5. The process info is given to user space; the process now shows in Task Manager / Activity Monitor, or its GUI appears.
- This user mode <-> kernel mode switching keeps happening internally for everything you run.

**Transitions from US to KS done by software interrupts.**

- Software interrupt: tells the CPU to pause the current work for a moment and quickly do this important work first.
- Software interrupts are used to switch from user mode to kernel mode and from kernel mode back to user mode.

**System calls** are implemented in C.

- Actually a lower-level kind of C than normal application C, one that can access and work with hardware directly.
- What you see (`mkdir`) is only the top layer. Inside, multiple processes / a lot of code may run to do the job. The system call you see is simply an interface to that C implementation.

A **system call** is a mechanism using which a user program can request a service from the kernel for which it does not have the permission to perform.
User programs typically do not have permission to perform operations like accessing I/O devices and communicating other programs.

- User mode has very limited access. Any work it cannot do itself is done by switching to kernel mode, and the mechanism for switching is the system call.

**System Calls** are the only way through which a process can go into **kernel mode from user mode.**

```
                    +---------------------------------+
                    |            User App             |
     User Mode      +---------------------------------+
         ^          |              Glibc              |
         |          +---------------------------------+
Software Interrupt ------------------------------------------------
         |          +---------------------------------+
         v          |   System Call Interface (SCI)   |
                    +---------------------------------+
    Kernel Mode     |             Kernel              |
                    +---------------------------------+
                    |            Hardware             |
                    +---------------------------------+
```

- Flow of a system call through the diagram (eg. `mkdir movies`):
  1. User app calls the library. In a normal Linux system this is glibc, a C (not C++) library used to call the SCI. We are still in user mode.
  2. A software interrupt is raised: move from user mode to kernel mode.
  3. In kernel mode the SCI is called. It looks up where the C implementation corresponding to `mkdir` is mapped in the kernel.
  4. The kernel runs that implementation.
  5. The work happens on the hardware: eg. the directory is created on the disk.
  6. Control retraces back up, and user mode gets the info that the `movies` folder is created.
- This diagram can be drawn in an interview to explain quickly.

## Types of System Calls:

1) Process Control (also called process management): system calls for creating, deleting, waiting for and terminating a process, allocating/freeing its memory, getting/setting its attributes.
   - a. end, abort
   - b. load, execute
   - c. create process, terminate process
   - d. get process attributes, set process attributes
   - e. wait for time
   - f. wait event, signal event
   - g. allocate and free memory

2) File Management
   - a. create file, delete file
   - b. open, close
   - c. read, write, reposition
     - Reposition: start reading from a chosen position instead of position 0, eg. from the 20th character.
   - d. get file attributes, set file attributes
     - Eg. security / permissions: a file `laks.txt` may be accessible only to user `laksh`; another user `ram` gets no access. Setting such attributes stops other users from modifying, deleting or creating it.

3) Device Management: read/write a device, get/set its attributes, attach/detach it.
   - a. request device, release device
   - b. read, write, reposition
   - c. get device attributes, set device attributes
   - d. logically attach or detach devices

4) Information maintenance: info of different processes, devices, the date & time, and system data; used to get/set these.
   - a. get time or date, set time or date
   - b. get system data, set system data
   - c. get process, file, or device attributes
   - d. set process, file, or device attributes

5) Communication Management: used for IPC (inter-process communication), ie. two processes running in separate spaces that need to communicate.
   - Eg. process A and process B need a pipe between them to communicate. Creating, maintaining and deleting the pipe is communication management.
   - a. create, delete communication connection
   - b. send, receive messages
   - c. transfer status information
   - d. attach or detach remote devices

## Examples of Windows & Unix System calls:

| Category | Windows | Unix |
|---|---|---|
| Process Control | CreateProcess() | fork() |
|  | ExitProcess() | exit() |
|  | WaitForSingleObject() | wait() |
| File Management | CreateFile() | open () |
|  | ReadFile() | read () |
|  | WriteFile() | write () |
|  | CloseHandle() | close () |
|  | SetFileSecurity() | chmod() |
|  | InitlializeSecurityDescriptor() | umask( |
|  | SetSecurityDescriptorGroup() | chown() |
| Device Management | SetConsoleMode() | ioctI() |
|  | ReadConsole() | read() |
|  | WriteConsole() | write() |
| Information Management | GetCurrentProcessID() | getpid () |
|  | SetTimer() | alarm () |
|  | Sleep() | sleep () |
| Communication | CreatePipe() | pipe () |
|  | CreateFileMapping() | shmget () |
|  | MapViewOfFile() | mmap() |

- `fork()`: creates a process, always as a child of an existing process.
  - When the computer boots, one root process starts first (call it process 0). Every process created after it is, in a way, its child.
  - Eg. you open a terminal and run an executable inside it: the terminal is the parent process, the executable is the child process.
  - So no process in the computer is created fresh; all are children of one another.
- `exit()`: exits the process: deallocates its memory etc., and marks in the task table that the process has exited.
- `chmod()`: sets the file's mode, ie. permissions: readable, writable, read-only, read-write.
- `chown()`: change ownership (ch = change, own = ownership). Eg. making a file accessible only by user `laksh`.
- `ioctl()`: used for device control, eg. setting the console mode.
- Information management also includes `date`: running `date` in a terminal shows the date and time.
- `pipe()`: sets up a pipe between process A and process B.
- IPC has two methods:
  - Message passing: done through `pipe()`.
  - Shared memory: done through `shmget()`, which gets the shared memory through which process A and process B communicate.
- `mmap()`: maps and unmaps a device (or file) into memory, including virtual memory. Covered later.
- In interviews nobody asks you to name all system calls. Know one or two names; mainly know what a system call is and how it works. Look up each call in the table once to get intuition.

### Demo: system calls while writing and running a script

1. Open a terminal, `cd` to Desktop, run `vim hello.sh`. Until saved, the document exists only in memory.
2. Write a bash script that prints in a loop:

   ```bash
   #!/bin/bash
   while true
   do
       echo "hello"
       sleep 1
   done
   ```

3. Save with `:wq`. File management system calls: `open()` creates a file descriptor, then `write()` creates the file in the Desktop folder of the file system tree and saves the content.
4. Run `bash hello.sh`. Process management system calls: `fork()` creates a child of the terminal process, named `hello.sh`.
5. Check with `ps -a` (from another terminal): the process is listed with its PID. Building that table uses information management system calls, eg. `getpid()` fetches the PID.
6. `ps -a` also shows a PPID (parent's PID): the parent is the terminal, which proves `fork()` made it a child.
7. Kill it: `kill -9 <pid>` (eg. `kill -9 19354`). `-9` kills forcefully.
   - `kill` is also a system call: it goes from user mode to kernel mode, the kernel finds the running PID, tells the CPU to stop working on it, and removes the process from memory.
8. `man kill` shows its manual: kill terminates or signals a process. Signals include 2 = interrupt, 3 = quit, 9 = kill, abort, alarm clock, etc. Use `man <command>` to read about any of the calls above.
- File management, then process management, then information management system calls all worked together in this one example.
