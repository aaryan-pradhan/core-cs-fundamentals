# Lecture 5: System Calls

**How do apps interact with the kernel?** Using system calls.

- **Two spaces:** User space is where apps run. Kernel space is where the core work happens. Only the kernel has privileged access to hardware.
- **Why system calls:** An app that wants memory, CPU cycles or any hardware work must go to the kernel. The two spaces are separate, so the system call is the mechanism to communicate.
- **Example (`malloc`):** The program needs memory, so it must switch from user mode to kernel mode. The system call makes that switch possible.

> **Interview:** "How do apps interact with the kernel?" Answer: "System calls." Then expect to be asked for an example. Use the `mkdir` one below.

## Example: `mkdir laks`

- **Indirect call:** `mkdir` asks the kernel's file management module to create a new directory.
- **Wrapper:** `mkdir` is just a wrapper of actual system calls. It interacts with the kernel using them.
- **Two ways to create a folder** (for example a "movies" folder):
  - **GUI:** Right-click, choose New Folder, then type the name. It is for standard users.
  - **CLI:** Open a terminal and run `mkdir movies`.
  - **Same job:** The GUI's New Folder button internally calls `mkdir`. The GUI only makes it look easy.

What happens on `mkdir movies`:

1. The command goes from user space to the **System Call Interface (SCI)**.
2. The SCI is the entry point to kernel space. It finds the implementation corresponding to `mkdir` inside the kernel.
3. Kernel space runs that implementation.
4. The implementation adds a node named `movies` in the current directory of the file system tree, for example under root.
5. Control returns to user space. The GUI now shows a folder named `movies`.

## Example: creating a process

- **Short form:** The user executes a process (user space). It gets a system call (user space). The exec system call creates the process (kernel space). Control returns to user space.

In detail, for a compiled `hello world` executable:

1. On run, it looks for the execution system call, which the SCI provides.
2. The SCI switches to kernel mode.
3. In kernel mode, process management creates the process and allocates memory for it in RAM. The kernel also does any other work needed, such as accessing hardware or I/O devices.
4. Once the process is created, the OS switches back to user mode.
5. The process info is given to user space. The process now shows in Task Manager or Activity Monitor, or its GUI appears.

- **Constant switching:** This user mode and kernel mode switching happens for everything you run.

## Software interrupts

Transitions from user space to kernel space are done by software interrupts.

- **Meaning:** A software interrupt tells the CPU to pause the current work and do this important work first.
- **Use:** It switches from user mode to kernel mode, and back.

## What a system call is

System calls are implemented in C.

- **Low-level C:** It is lower-level than normal application C and can work with hardware directly.
- **Top layer:** What you see (`mkdir`) is only the top layer. Inside, multiple processes and a lot of code may run. The system call is simply an interface to that C implementation.

A **system call** is a mechanism by which a user program can request a service from the kernel that it does not have permission to perform. User programs typically do not have permission to perform operations like accessing I/O devices and communicating with other programs.

- **Limited user mode:** User mode has very limited access. Work it cannot do is done by switching to kernel mode, through the system call.

System calls are the only way a process can go into **kernel mode from user mode**.

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

Flow of a system call through the diagram, for `mkdir movies`:

1. **User app:** It calls the library. On Linux this is glibc, a C (not C++) library used to call the SCI. This is still user mode.
2. **Interrupt:** A software interrupt is raised. It moves from user mode to kernel mode.
3. **SCI:** In kernel mode the SCI is called. It looks up where the C implementation for `mkdir` is mapped in the kernel.
4. **Kernel:** The kernel runs that implementation.
5. **Hardware:** The work happens on the hardware. For example, the directory is created on the disk.
6. **Return:** Control retraces back up. User mode learns that the `movies` folder is created.

> **Interview:** Draw this diagram in an interview to explain quickly.

## Types of System Calls

1. **Process Control** (also called process management): System calls for creating, deleting, waiting for and terminating a process. They also allocate and free its memory, and get and set its attributes.
   - a. end, abort
   - b. load, execute
   - c. create process, terminate process
   - d. get process attributes, set process attributes
   - e. wait for time
   - f. wait event, signal event
   - g. allocate and free memory

2. **File Management:**
   - a. create file, delete file
   - b. open, close
   - c. read, write, reposition
     - **Reposition:** Start reading from a chosen position instead of position 0. For example, start from the 20th character.
   - d. get file attributes, set file attributes
     - **Example:** Security and permissions. A file `laks.txt` may be accessible only to user `laksh`. User `ram` gets no access. Such attributes stop other users from modifying, deleting or creating it.

3. **Device Management:** Read and write a device, get and set its attributes, attach and detach it.
   - a. request device, release device
   - b. read, write, reposition
   - c. get device attributes, set device attributes
   - d. logically attach or detach devices

4. **Information maintenance:** These calls get and set info about different processes, devices, the date and time, and system data.
   - a. get time or date, set time or date
   - b. get system data, set system data
   - c. get process, file, or device attributes
   - d. set process, file, or device attributes

5. **Communication Management:** These calls are used for IPC (inter-process communication). Two processes running in separate spaces need to communicate.
   - **Example:** Processes A and B need a pipe between them. Creating, maintaining and deleting the pipe is communication management.
   - a. create, delete communication connection
   - b. send, receive messages
   - c. transfer status information
   - d. attach or detach remote devices

## Examples of Windows and Unix System calls

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

- **`fork()`:** It creates a process, always as a child of an existing process.
  - **Root process:** At boot, one root process (call it process 0) starts first. Every later process is, in a way, its child.
  - **Example:** You run an executable inside a terminal. The terminal is the parent. The executable is the child.
  - **Result:** All processes are children of one another.
- **`exit()`:** It exits the process, deallocates its memory and so on, and marks in the task table that it has exited.
- **`chmod()`:** It sets the file's mode, meaning its permissions: readable, writable, read-only or read-write.
- **`chown()`:** It changes ownership. Here "ch" means change and "own" means ownership. Example: making a file accessible only by user `laksh`.
- **`ioctl()`:** It is used for device control, for example setting the console mode.
- **`date`:** Information management also includes `date`. Running `date` in a terminal shows the date and time.
- **`pipe()`:** It sets up a pipe between process A and process B.
- **IPC methods:** IPC has two methods.
  - **Message passing:** It is done through `pipe()`.
  - **Shared memory:** It is done through `shmget()`. This gets the shared memory through which process A and process B communicate.
- **`mmap()`:** It maps and unmaps a device (or file) into memory, including virtual memory. It is covered later.

> **Interview:** Nobody asks you to name all system calls. Know one or two. Mainly know what a system call is and how it works. Look up each call in the table once.

### Demo: system calls while writing and running a script

1. **Open the editor:** In a terminal, `cd` to Desktop and run `vim hello.sh`. Until saved, the document exists only in memory.

2. **Write the script:** Write a bash script that prints in a loop.

   ```bash
   #!/bin/bash
   while true
   do
       echo "hello"
       sleep 1
   done
   ```

3. **Save:** Save with `:wq`. These are file management system calls. `open()` creates a file descriptor. `write()` creates the file in the Desktop folder of the file system tree and saves the content.

4. **Run:** Run `bash hello.sh`. These are process management system calls. `fork()` creates a child of the terminal process, named `hello.sh`.

5. **Check:** Run `ps -a` from another terminal. The process is listed with its PID. Building that table uses information management system calls. For example, `getpid()` fetches the PID.

6. **Parent:** `ps -a` also shows a PPID (the parent's PID), which is the terminal. This proves `fork()` made it a child.

7. **Kill:** Run `kill -9 <pid>`, for example `kill -9 19354`. The `-9` kills forcefully.
   - **System call:** `kill` is also a system call. It goes to kernel mode. The kernel finds the running PID, tells the CPU to stop it and removes the process from memory.

8. **Manual:** `man kill` shows that kill terminates or signals a process. Signals include 2 = interrupt, 3 = quit, 9 = kill, abort, alarm clock and others. Use `man <command>` to read about any of the calls above.

- **Summary:** File, process and information management system calls all worked together in this one example.
