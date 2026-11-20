# Lecture 1: An Introduction to Operating Systems

UNIT 1

**Application software** does a specific task for the user.

**System software** runs and controls the computer. It gives application software a platform to run on.

An **operating system (OS)** is a piece of software.

- It manages all the resources of a computer, both hardware and software.
- It gives the user an easy and efficient place to run programs.
- It does this in two ways:
  1. It hides the complexity of the hardware.
  2. It acts as a resource manager.

> **Interview:** An OS does two things. It hides hardware complexity, and it manages resources.

- **Just software:** The OS is a program, like the apps you write.
- **Easy and efficient:** You never worry about how memory gets allocated. You can run many programs at once. No app can take over the system.

## Why OS?

Picture a simple computer with no OS. It has a CPU, memory, a GPU, and a disk.

1. What if there is no OS?

   a. Apps become bulky and complex. Each app must contain its own hardware code.
      - **Repeated code:** TikTok and PUBG both write the same memory management code.
      - **Breaks DRY:** DRY means "Do not Repeat Yourself". You write a function once, like a prime check, and call it everywhere.
      - **With an OS:** Memory management, scheduling and process management live once, in the OS. An app developer writes only the app's own logic.

   b. One app can grab all the resources.
      - **Hijacking:** TikTok opens and takes all the CPU, memory and GPU.
      - **Result:** PUBG hangs and cannot start. This happens even though the machine has enough for both.
      - **With an OS:** The OS sits between the apps and the hardware. It gives each app only a share. So both apps run together.

        | App | CPU | Memory | GPU |
        |-----|-----|--------|-----|
        | TikTok | 5% | 10% | 12% |
        | PUBG (heavier) | 50% | 60% | 60% |

      - **Resource management:** This sharing out is the first job of an OS.

   c. There is no memory protection.
      - **No isolation:** Memory is split into blocks. Nothing keeps one app's blocks apart from another's.
      - **Isolation:** Each app's memory is kept separate. TikTok should not even know PUBG exists.
      - **The danger:** TikTok could change PUBG's player health from 100% to 0%. Then PUBG kills the player. A buggy or harmful app can break another app.
      - **With an OS:** The OS records which memory range each app owns. Each app stays inside its own range. It cannot see the other app. This is **memory protection and isolation**.

        ```
        Memory:  [ TikTok: 0 .. X ][ PUBG: X .. Y ]
                  OS enforces the bounds. Neither app sees the other.
        ```

2. What is an OS made of?

   a. An OS is a collection of system software.

## Functions of an operating system

1. **It controls access to the hardware.**
   - User apps cannot touch the hardware directly.
   - Every program must go through the OS.

2. **It is the interface between the user and the hardware.**
   - The OS sits between the user's apps (like TikTok) and the hardware.
   - **Analogy:** A bank clerk. You give the clerk a slip. The clerk brings cash from the vault. You are the app, the clerk is the OS, and the vault is the hardware.

3. **It manages resources.** These include memory, devices, files, security and processes.
   > **Interview:** Resource management is also called **arbitration**.

4. **It hides the complexity of the hardware.** This is called **abstraction**.
   - **Example:** In C/C++ you call `malloc` (or `new`) for 10 bytes. You get the memory. You never see how the OS finds free memory.
   - The OS keeps all hardware code in its own code base. It hides that code from you.

5. **It helps apps run safely.** It keeps apps isolated and protected from each other.

```
          O
         /|\
         / \
         User
+------------------------+
|  Application programs  |
+------------------------+
|    Operating system    |
+------------------------+
|   Computer hardware    |
+------------------------+
```

The OS makes sure the computer's resources are used properly.
