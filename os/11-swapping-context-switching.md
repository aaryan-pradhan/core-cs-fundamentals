# Lecture 11: Swapping | Context-Switching | Orphan process | Zombie process

- **Topics:** Four interview-important topics from process management: swapping, context switching, orphan processes and zombie processes.
- **Common question:** The difference between orphan and zombie is asked often.

### Recap: LTS and STS

- **Names:** The short-term scheduler (STS) is the CPU scheduler. The long-term scheduler (LTS) is the job scheduler.

```
 Job queue (secondary storage) --LTS--> Ready queue --STS (dispatch)--> CPU
```

- **LTS:** It picks a good **mix of processes** from the many the user submitted (P1, P2, P3, ...) and puts them in the ready queue.
  - **Mix:** The mix is I/O-intensive plus CPU-intensive processes.
  - **Why:** All CPU-intensive or all I/O-intensive processes increase the chance of starvation. A mix keeps the ready queue healthy.
- **STS:** It picks one process from the ready queue and dispatches it to the CPU, using the scheduling algorithm chosen.
- **Third scheduler:** A third type of scheduler sits between these two. It is the **medium-term scheduler (MTS)**.

1. **Swapping**
    1. A time-sharing system may have a medium-term scheduler (MTS).
        - **History:** Classic OSes had only LTS and STS. MTS was introduced later. Present-day systems have it.
    2. It removes processes from memory to reduce the degree of multi-programming.
        - **Degree:** The degree of multi-programming is the number of processes that can be in the ready queue (in memory).
        - **Problem:** The LTS may raise the degree too high. Once the CPU starts running them, a few processes turn out to be very memory-intensive. Memory runs out, with no space left to hold the whole ready queue.
        - **Swap out:** So some processes must be **swapped out**, that is, removed from the ready queue and main memory.
        - **Example:** The ready queue has P1, P2, P3, P4. P1 and P2 become very memory-intensive, leaving no room for P3 and P4. P3 and P4 are swapped out to a separate area called **swap space**.
        - **Saved state:** P3 and P4 are partially executed, which is why they are still in the ready queue. Each waits at its own program counter. That current state is saved in swap space.
        - **Swap space:** It is generally secondary storage (SSD or hard disk). Secondary storage is larger because it is cheaper (slower access), so there is room.
        - **Effect:** For the time being, the ready queue shrinks and memory is saved from exhaustion. P1 and P2 keep running.
        - **Practical example:** Open many apps on a phone or computer. Recent apps resume instantly. Some older apps in the recents list take long to reload when tapped, because they had been swapped out of memory.
    3. Removed processes can be reintroduced into memory. Their execution continues where it left off. This is called **swapping.**
        - **Example continued:** P1 (memory-intensive) terminates and frees space. P3 and P4, whose state was saved in secondary storage, are brought back into the ready queue. This is **swap-in**.
        - **Definition:** Swap-out plus swap-in together make swapping.
    4. Swap-out and swap-in are done by the MTS.
        - **Kernel:** Swapping, like context switching, is instructions written in the kernel. The kernel performs it, and ultimately the CPU executes them.
        - **Context saving:** Swapping is a kind of context saving. The current context of a partially executed process is saved to swap space and restored later.
        - **Why MTS exists:** It shows how the OS optimises every small thing. LTS and STS worked, but real systems hit memory-intensive processes after many were admitted. So a scheduler was added in between (MTS), instead of relying on the LTS again.
    5. Swapping is necessary to improve the process mix, or when a change in memory requirements has overcommitted available memory and memory must be freed up.
    6. Swapping is a mechanism in which a process can be swapped temporarily out of main memory (or moved) to secondary storage (disk). This makes that memory available to other processes. At some later time, the system swaps the process back from secondary storage to main memory.

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
    - **Earlier:** It was discussed informally since lecture 2-3. Now it is covered formally, using the PCB.
    - **Analogy:** You are listening to songs or playing a game. Your father asks you to collect a Swiggy delivery downstairs. You pause the song, put the phone down and remove the earphones (save the current context). You hand him the delivery (task B done). You put the earphones back on and resume the song where it stopped (restore the old context).
    1. Switching the CPU to another process requires a state save of the current process and a state restore of a different process.
        - **PCB:** Each process (P1, P2) has its own PCB (PCB1, PCB2). The PCB is its entry in the process table, a data structure describing the process: program counter, registers, state, PID, open file descriptors (file handles), and so on.
        - **When needed:** A context switch is needed in two cases.
            - The running process goes to wait state, for example to do I/O.
            - Its time quantum expires (time-sharing systems).
        - **Why save:** The CPU leaves that process, so its current context must be saved.
        - **Save (P1):** The CPU is executing P1, say at instruction address 1. The next instruction is 2.
            - Write the next instruction (2) into P1's program counter in PCB1.
            - Copy the current values of all CPU registers into the registers field of PCB1. Register types and count differ between CPU architectures.
            - Change P1's state. Save open file descriptors and all other information of the current context into PCB1.
        - **Restore (P2):** P2 was saved earlier. Load its saved register values from PCB2 back into the CPU registers, with its open file descriptors and device descriptors. Then P2 resumes from its saved program counter.
    2. The kernel saves the context of the old process in its PCB. It loads the saved context of the new process scheduled to run.
        - **Kernel only:** Context switching is done by the kernel (low-level work), never by user space.
    3. It is pure overhead, because the system does no useful work while switching.
        - **Why:** The context-switch code is itself a kernel program that the CPU executes. During that time the CPU runs none of the user's processes in the ready queue, so no user work moves forward.
    4. Speed varies from machine to machine. It depends on the memory speed, the number of registers that must be copied, and so on.
        - **Time:** A switch (milliseconds or instruction cycles) depends on register performance and the speed of the memory where the context is saved.
        - **Example:** RAM went DDR2, DDR3, DDR4. Faster RAM made context switches quicker, so the whole system got faster.
        - **Why it differs:** Architectures and memory speeds differ between machines.

3. **Orphan process**
    - **Meaning:** An orphan is a process without a parent.
    - **fork():** Every process is created by `fork()`: a parent calls fork and creates a child. So every process is someone's child, except the very first one.
    - **init:** In Linux the first process is `init`, PID 1. The kernel's further processes are created after it, forming a **tree** with init at the root.
    1. An orphan is a process whose parent has terminated while it is still running.
        - **Example:** P1 (running) forks child P2 (running). P1 hits an exception and terminates, or the programmer did not put a `wait()`, so the parent exits first.
        - **Norm:** A programmer who forks a child must make the parent wait for it.
        - **Result:** P2 is now orphaned: detached from the tree, its parent gone. The OS still needs to track every process.
    2. Orphan processes are adopted by the init process.
        - **Re-link:** The OS re-links the orphan's parent to init, so P2's parent (PPID) becomes init (PID 1).
    3. Init is the first process of the OS.

### Orphan process demo (Linux terminal)

`orphan.sh`, first version (normal flow):

```bash
#!/bin/bash
sleep 200
```

- **PIDs:** The terminal PID is 9161. Run `bash orphan.sh`, then `ps -l` in another view. `bash orphan.sh` has PID 9185 and PPID 9161 (the terminal). `sleep 200` has PPID 9185.
- **Chain:** Terminal, then orphan.sh, then sleep 200. orphan.sh waits for sleep.
- **Exit:** When sleep exits after 200 s, its parent learns of it and exits too. Then the terminal learns its child exited. All entries disappear.
- **Why a parent waits:** It reads what the child returned: whether it executed successfully and its exit status. Only then is the child's entry deleted from the process table.

`orphan.sh`, second version (creates an orphan):

```bash
#!/bin/bash
sleep 200 &
```

- **`&`:** It starts `sleep 200` as a separate, detached process. The script does not wait for it.
- **Run:** Control returns to the terminal immediately because `orphan.sh` exited.
- **Result:** `ps -l` now shows `sleep 200` (PID 9228) with **PPID 1**, which is init.
- **Story:** The terminal forked orphan.sh, which forked `sleep 200` and exited without waiting. `sleep 200` became an orphan adopted by init.

4. **Zombie process / Defunct process**
    - **Names:** Some OSes call it "zombie" in the kernel. Others call it "defunct process".
    - **Example:** P1 forks child P2. P2 executes and calls `exit()` early. Normally the parent waits for the child to exit, reads its exit status using `wait()`, and then the child's entry is deleted from the process table. The parent can then exit.
    - **Gap:** Say P1 calls wait only after 5 minutes, but P2 exits after 2 minutes. For the 3-minute gap, P2 is a zombie.
    1. A zombie process is a process whose execution is completed but which still has an entry in the process table.
        - **On `exit()`:** All resources the process had taken from the OS are released. Its entry stays in the process table.
        - **Danger:** The process table is a resource with a limit. Every OS has a maximum size. Too many zombies fill it. Then no new process can be created and no new PID can be used.
    2. Zombie processes usually occur for child processes, as the parent process still needs to read its child's exit status. Once this is done using the wait system call, the zombie is eliminated from the process table. This is known as **reaping** the zombie process.
        - **`wait()`:** The parent calls `wait()` to be satisfied that its child exited properly and to note its exit status. Only then is the entry deleted.
    3. This happens because the parent process may call wait() on the child process after a long time, while the child terminated much earlier.
    4. An entry in the process table can be removed only after the parent process reads the exit status of the child process. Hence, the child process remains a zombie until it is removed from the process table.
    - **Parent never calls `wait()`:** This is a badly written program. The child's resources are already released, so there is no real leak of them. But the process table gets exhausted.
    - **Accumulation:** Zombies may keep accumulating, for example when the parent itself is gone and nobody reaps them. Treat this as a bug in the OS. They pile up until the process table fills. The table is a resource, so this is a resource leak.

### Zombie process demo (Linux terminal)

`zombie.sh`:

```bash
#!/bin/bash
for i in {1..100}; do
    sleep 1 &
done
exec sleep 100
```

- **Loop:** It quickly launches 100 `sleep 1` processes in the background (`&`). Without `&`, the script would wait for each sleep to finish first.
- **`exec sleep 100`:** It replaces the script's code with `sleep 100` (same PID), holding the script alive for 100 s without calling wait on its children.
- **Before running:** No zombie processes are in the system. The only match is the `grep` command itself.
- **After running:** `ps -l` shows many `sleep` entries with state `Z+`. These are zombies.
  - **Parent:** Terminal PID 9161 launched the script. It now shows as `sleep 100` (PID 9569) because exec replaced it.
  - **Children:** All the `sleep 1` processes have the same PPID 9569.
  - **Why zombies:** Each ran for 1 s and called exit. Their entries stay because their parent has not read their exit status.
- **After 100 s:** The parent finishes and the exit statuses are read. `ps -l` shows only the terminal's entries. All `Z+` entries are gone.
