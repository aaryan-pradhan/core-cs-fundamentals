# Lecture 11: Swapping | Context-Switching | Orphan process | Zombie process

- Four interview-important topics from process management: swapping, context switching, orphan processes, zombie processes.
- Orphan vs zombie difference is a common interview question.

### Recap: LTS and STS

- Short-term scheduler (STS) = CPU scheduler. Long-term scheduler (LTS) = job scheduler.

```
 Job queue (secondary storage) --LTS--> Ready queue --STS (dispatch)--> CPU
```

- LTS picks a good **mix of processes** from the many the user submitted (P1, P2, P3, ...) and puts them in the ready queue.
  - Mix = I/O-intensive + CPU-intensive processes.
  - All CPU-intensive or all I/O-intensive in the ready queue increases the chance of starvation; a mix keeps the ready queue healthy.
- STS picks one process from the ready queue and dispatches it to the CPU, depending on the scheduling algorithm chosen.
- A third type of scheduler sits between these two: the **medium-term scheduler (MTS)**.

1. **Swapping**
    1. Time-sharing system may have medium term schedular (MTS).
        - Classic OSes had only LTS and STS. MTS was introduced later; present-day systems have it.
    2. Remove processes from memory to reduce degree of multi-programming.
        - Degree of multi-programming = number of processes that can be in the ready queue (in memory).
        - LTS may raise the degree of multi-programming too high. Once the CPU starts running them, a few processes turn out to be very memory-intensive, and memory runs out: no space left to hold the whole ready queue.
        - So some processes must be **swapped out**, i.e. removed from the ready queue / main memory.
        - Example: ready queue has P1, P2, P3, P4. P1 and P2 become very memory-intensive, leaving no room for P3, P4. P3 and P4 are swapped out to a separate area called **swap space**.
        - P3, P4 are partially executed (that is why they are still in the ready queue), each waiting at its own program counter. That current state is saved in swap space.
        - Swap space is generally secondary storage (SSD / hard disk). Secondary storage is larger because it is cheaper (slower access), so there is room for these processes.
        - For the time being, the ready queue is shrunk and memory is saved from exhaustion; P1, P2 keep running.
        - Practical example: open many apps on a phone/computer. Recent apps resume instantly, but some older apps in the recents list take a long time to reload when tapped, because they were no longer in memory; they had been swapped out to another area.
    3. These removed processes can be reintroduced into memory, and its execution can be continued where it left off. This is called **Swapping.**
        - Example contd.: P1 (memory-intensive) terminates and frees space. P3, P4, whose current state was saved in secondary storage, are brought back into the ready queue: **swap-in**.
        - Swap-out + swap-in together = swapping.
    4. Swap-out and swap-in is done by MTS.
        - Swapping (like context switching) is instructions written in the kernel; the kernel performs it, and ultimately the CPU executes those instructions.
        - Swapping is a kind of context saving: the current context of a partially executed process is saved to swap space and restored later.
        - Shows how the OS optimises every small thing: LTS + STS worked, but real systems hit memory-intensive processes after many were admitted, so instead of relying on LTS again, a scheduler was added in between (MTS).
    5. Swapping is necessary to improve process mix or because a change in memory requirements has overcommitted available memory, requiring memory to be freed up.
    6. Swapping is a mechanism in which a process can be swapped temporarily out of main memory (or move) to secondary storage (disk) and make that memory available to other processes. At some later time, the system swaps back the process from the secondary storage to main memory.

```
            Swap-in   +------------------------------+   Swap-out
        +-------------| Partially executed swapped-  |<-------------+
        |             |        out processes         |              |
        |             +------------------------------+              |
        v                                                           |
 -------+------------> [      Ready queue      ] --------------> ( CPU ) ----> end
        ^                                                           |
        |                                                           |
        +-------- ( I/O ) <-------- [ I/O waiting queue ] <---------+
```

2. **Context-Switching**
    - Discussed informally since lecture 2–3; now formally, using the PCB.
    - Real-life analogy: you are listening to songs / playing a game. Your father asks you to collect a Swiggy delivery downstairs. You pause the song at the point you were at, put the phone on the table and remove the earphones (save the current context). You go down, take the delivery, give it to him (task B done). You come back, put the earphones on and resume the song where it stopped (restore the old context). This is context switching.
    1. Switching the CPU to another process requires performing a state save of the current process and a state restore of a different process.
        - Each process (P1, P2) has its own PCB (PCB1, PCB2). The PCB is the entry for that process in the process table: a data structure describing the process (program counter, registers, state, PID, open file descriptors / file handles, ...).
        - When a context switch is needed:
            - the running process goes to wait state (e.g. goes to do I/O), or
            - its time quantum expires (time-sharing systems).
        - The CPU will no longer be with that process, so its current context must be saved.
        - Save (P1): CPU is executing P1, say at instruction address 1, next instruction is 2.
            - Write the next instruction (2) into P1's program counter in PCB1.
            - Copy the current values of all CPU registers into the registers field of PCB1. (Register types and count differ between CPU architectures.)
            - Change P1's state; save open file descriptors and all other information of the current context into PCB1.
        - Restore (P2): P2 was saved at some earlier point. Load its saved register values from PCB2 back into the CPU registers, along with its open file descriptors / device descriptors, so P2 resumes from its saved program counter.
    2. When this occurs, the kernel saves the context of the old process in its PCB and loads the saved context of the new process scheduled to run.
        - Context switching is done by the kernel (low-level work), never by user space.
    3. It is pure overhead, because the system does no useful work while switching.
        - The context-switch code is itself a program in the kernel that the CPU executes. During that time the CPU runs none of the user's processes in the ready queue, so no user work moves forward: pure overhead from the user's perspective.
    4. Speed varies from machine to machine, depending on the memory speed, the number of registers that must be copied etc.
        - Time for a switch (milliseconds / instruction cycles) depends on register performance and the speed of memory where the context is saved.
        - Example: RAM went DDR2 → DDR3 → DDR4; faster RAM made context switches take less time, so the whole system got faster.
        - Differs machine to machine because architectures and memory speeds differ.

3. **Orphan process**
    - Orphan = one without parents.
    - Every process is created by `fork()`: a parent process calls fork and creates a child. So every process in an OS is someone's child, except the very first one.
    - In Linux the first process is `init`, PID 1. After init, the kernel's further processes are created, forming a **tree** of processes with init at the root.
    1. The process whose parent process has been terminated and it is still running.
        - Example: P1 (running) forks child P2 (running). P1 hits an exception and terminates, or the programmer did not put a `wait()`, so the parent exits first.
        - Norm: a programmer who forks a child must make the parent wait for the child.
        - P2 is now orphaned: detached from the tree, its parent gone. The OS still needs to track every process for process management.
    2. Orphan processes are adopted by init process.
        - The OS re-links the orphan's parent to init, so P2's parent (PPID) becomes init (PID 1).
    3. Init is the first process of OS.

### Orphan process demo (Linux terminal)

`orphan.sh`, first version (normal flow):

```bash
#!/bin/bash
sleep 200
```

- Terminal PID = 9161. Run `bash orphan.sh`, then `ps -l` in another view.
- `bash orphan.sh` has PID 9185, PPID 9161 (the terminal). `sleep 200` has PPID 9185.
- Chain: terminal → orphan.sh → sleep 200. orphan.sh waits for sleep. When sleep exits after 200 s, its parent learns of it and exits too; the terminal then learns that its child exited, and all entries disappear.
- A parent waits for its child to read what the child returned: did it execute successfully, what is its exit status. Only after the parent reads the exit status is the child's entry deleted from the process table.

`orphan.sh`, second version (creates an orphan):

```bash
#!/bin/bash
sleep 200 &
```

- `&` starts `sleep 200` as a separate, detached process; the script does not wait for it.
- Run it: control returns to the terminal immediately because `orphan.sh` exited.
- `ps -l` now shows `sleep 200` (PID 9228) with **PPID 1** = init.
- So: terminal forked orphan.sh, orphan.sh forked `sleep 200` and did not wait, orphan.sh exited, and `sleep 200` became an orphan adopted by init.

4. **Zombie process / Defunct process**
    - Some OSes name it "zombie" in the kernel/implementation, others "defunct process".
    - Example: P1 forks child P2. P2 executes and calls `exit()` early. Normally the parent waits for the child to exit, then reads its exit status using `wait()`; then the child's entry is deleted from the process table, and the parent can exit.
    - If P1 calls wait only after 5 minutes but P2 exits after 2 minutes, then for the 3-minute gap P2 is a zombie.
    1. A zombie process is a process whose execution is completed but it still has an entry in the process table.
        - On `exit()`, all resources the process had taken from the OS are released, but its entry stays in the process table.
        - The process table is itself a resource with a limit (every OS has a maximum size). Too many zombies fill it: no new process can be created and no new PID can be used. Problematic situation.
    2. Zombie processes usually occur for child processes, as the parent process still needs to read its child's exit status. Once this is done using the wait system call, the zombie process is eliminated from the process table. This is known as **reaping** the zombie process.
        - The parent calls `wait()` to be satisfied that its child exited properly and to note its exit status; only then is the entry deleted.
    3. It is because parent process may call wait () on child process for a longer time duration and child process got terminated much earlier.
    4. As entry in the process table can only be removed, after the parent process reads the exit status of child process. Hence, the child process remains a zombie till it is removed from the process table.
    - Parent never calls `wait()` (badly written program): no real resource leak of the child's resources (already released), but the process table gets exhausted.
    - If such zombies keep accumulating (e.g. the parent itself is gone and nobody reaps them), treat it as a bug in the OS: zombies pile up until the process table fills. The process table is a resource, so this is a resource leak.

### Zombie process demo (Linux terminal)

`zombie.sh`:

```bash
#!/bin/bash
for i in {1..100}; do
    sleep 1 &
done
exec sleep 100
```

- The loop launches 100 `sleep 1` processes in the background (`&`), quickly. Without `&`, the script would wait for each sleep to finish before starting the next.
- `exec sleep 100` replaces the script's code with `sleep 100` using the same PID, holding the script alive for 100 s without calling wait on its children.
- Before running: no zombie processes in the system (the only match is the `grep` command itself).
- After running, `ps -l` shows many `sleep` entries with state `Z+`: zombies.
  - Terminal PID 9161 launched the script, which now shows as `sleep 100` (PID 9569) because exec replaced it.
  - All the `sleep 1` processes have the same PPID 9569.
  - Each ran for 1 s and called exit, but their entries stay in the process table because their parent has not read their exit status.
- After 100 s the parent finishes and the exit statuses are read; `ps -l` shows only the terminal's entries. All zombie (`Z+`) entries are gone from the process table.
