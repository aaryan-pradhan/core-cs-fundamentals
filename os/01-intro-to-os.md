# Lecture 1: An Introduction to Operating Systems

UNIT 1

**Application software** performs specific task for the user.

**System software** operates and controls the computer system and provides a platform to run application software.

An **operating system** is a piece of software that manages all the resources of a computer system, both hardware and software, and provides an environment in which the user can execute his/her programs in a convenient and efficient manner by hiding underlying complexity of the hardware and acting as a resource manager.

- **Just software:** the OS is a program, like the apps you write.
- **Resources:** the OS manages both hardware and software resources.
- **Convenient and efficient:** you never worry about how memory gets allocated. You can run many programs side by side. No app can hijack the system.

> **Interview:** An OS does two things. It hides hardware complexity, and it manages resources.

## Why OS?

Picture a minimal computer with no OS. It has a CPU, memory, a GPU, and a disk.

1. What if there is no OS?

   a. Bulky and complex app. (Hardware interaction code must be in app's code base)
      - **Repeated code:** each app writes its own hardware and memory management code. TikTok and PUBG both carry the same code.
      - **Breaks DRY:** apps become bulky and messy. DRY means "Do not Repeat Yourself": write a function once (e.g. a prime check) and call it everywhere.
      - **With an OS:** memory management, scheduling and process management live once, in the OS. An app developer (e.g. of a weather app) writes only the app's own logic.

   b. Resource exploitation by 1 App.
      - **Hijacking:** TikTok opens and takes all the CPU, memory and GPU.
      - **Result:** PUBG hangs and cannot start, even though the machine has enough for both.
      - **With an OS:** the OS sits between apps and hardware. It gives each app only a share, so both run together:

        | App | CPU | Memory | GPU |
        |-----|-----|--------|-----|
        | TikTok | 5% | 10% | 12% |
        | PUBG (heavier) | 50% | 60% | 60% |

      - **Resource management:** this sharing out is the first job of an OS.

   c. No memory protection.
      - **No isolation:** memory is split into blocks. Nothing keeps one app's blocks apart from another's.
      - **Isolation:** the two apps' memory is logically separate. TikTok should not even know PUBG exists.
      - **The danger:** TikTok could overwrite PUBG's player health from 100% to 0%. PUBG then kills the player. A buggy or malicious app can corrupt another app.
      - **With an OS:** the OS records which range each app owns. Each app stays inside its range and cannot see the other. This is **memory protection and isolation**.

        ```
        Memory:  [ TikTok: 0 .. X ][ PUBG: X .. Y ]
                  OS enforces the bounds. Neither app sees the other.
        ```

2. What is an OS made up of?

   a. Collection of system software.

## An operating system function -

- Access to the computer hardware.
  - **Only the OS:** user apps have no direct access to the hardware. Every program goes through the OS.
- interface between the user and the computer hardware
  - **Interface:** the OS sits between the user (apps like TikTok, PUBG) and the hardware.
  - **Analogy:** a bank clerk. You give the clerk a slip, the clerk fetches cash from the vault. You are the app, the clerk is the OS, the vault is the hardware.
- **Resource management (Aka, Arbitration) (memory, device, file, security, process etc)**

  > **Interview:** "Arbitration" is the fancier word for resource management.

- **Hides the underlying complexity of the hardware. (Aka, Abstraction)**
  - **Example:** in C/C++ you call `malloc` (or `new`) for 10 bytes. You get the memory. You never see how the OS finds free memory, or in which sector.
  - **Abstraction:** the OS keeps all hardware code in its own code base and hides it from you.
- facilitates execution of application programs by providing isolation and protection.

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

The operating system provides the means for proper use of the resources in the operation of the computer system.
