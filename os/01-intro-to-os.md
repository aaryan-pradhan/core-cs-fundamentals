# Lecture 1: An Introduction to Operating Systems

UNIT 1

**Application software** performs specific task for the user.

**System software** operates and controls the computer system and provides a platform to run application software.

An **operating system** is a piece of software that manages all the resources of a computer system, both hardware and software, and provides an environment in which the user can execute his/her programs in a convenient and efficient manner by hiding underlying complexity of the hardware and acting as a resource manager.

- The OS is itself just a piece of software, like the apps you write.
- "Resources" means both hardware and software resources; the OS manages both.
- "Convenient and efficient": the user/developer does not worry about how memory gets allocated, and can run multiple programs side by side with no app hijacking the system.
- The two ways it achieves this (remember these for interviews):
  1. Hiding the underlying complexity of the hardware.
  2. Acting as a resource manager.

## Why OS?

A minimal computer has at least four components: CPU, memory, GPU and disk. Imagine this computer with no OS and see what goes wrong.

1. What if there is no OS?
   a. Bulky and complex app. (Hardware interaction code must be in app's code base)
      - Without an OS, every app must contain its own hardware interaction and resource management code (memory management, etc.).
      - E.g. the TikTok developer writes memory management code inside TikTok; the PUBG developer writes the same memory management code again inside PUBG. Every app on the machine carries the same code.
      - Apps become bulky, everything is mixed together, and this violates the **DRY principle (Do Not Repeat Yourself)**.
      - DRY: if a function (e.g. one that checks for prime numbers) is needed in many places in your code, you write it once and call it wherever needed, instead of copying the code each time.
      - With an OS: all resource management code (memory management, scheduling, process management, etc.) lives once, in the OS's code base. An app developer (e.g. writing a weather app) only thinks about the app's own logic, not about how to manage resources.

   b. Resource exploitation by 1 App.
      - E.g. you open TikTok. With no OS, TikTok takes (hijacks) all the CPU, memory and GPU.
      - Now you want to play PUBG. Enough resources exist in the machine for both, but TikTok has grabbed them all, so PUBG goes into a hang state and cannot even start.
      - Fix: put an OS layer between the apps and the hardware. The OS gives each app only a share of the resources, e.g. TikTok gets 5% CPU, 10% memory, 12% GPU; PUBG (a heavier app) gets 50% CPU, 60% memory, 60% GPU.
      - Now both apps can be in memory and run together. This sharing out of resources is **resource management**, the first job of an OS.

   c. No memory protection.
      - Memory is divided into blocks; TikTok takes some blocks and PUBG takes some blocks.
      - With no OS there is no isolation: nothing guarantees the two apps' memory is kept apart.
      - Isolation means the memory of the two apps is logically separate; TikTok should not even know that PUBG exists in memory.
      - Without it, TikTok could go and write to the location where PUBG stores the player's health (100%) and overwrite it with 0%. PUBG's code then reads 0% health and kills the player. A buggy or malicious app can corrupt another app this way.
      - With an OS: the OS records which memory range it gave to each app (e.g. TikTok gets location 0 to X, PUBG gets X to Y) and makes sure each app stays in its own range and cannot see the other. This is **memory protection and isolation**.

2. What is an OS made up of?
   a. Collection of system software.

## An operating system function -

- Access to the computer hardware.
  - User apps do not have access to the computer hardware; only the OS has it.
  - Any program that wants to interact with the hardware must go through the OS.
- interface between the user and the computer hardware
  - The OS sits between the two entities, the user (apps like TikTok, PUBG) and the computer hardware, and acts as an interface.
  - Bank analogy: you want to withdraw ₹10,000. You do not walk into the bank's vault (treasury) yourself. You fill a slip and give it to the clerk at the counter; the clerk goes to the vault, gets the cash and gives it to you. The clerk is the interface.
  - Mapping: you = user/app (e.g. TikTok); the clerk = OS (the interface); the vault of money = resources (CPU, GPU, memory, etc.).
- **Resource management (Aka, Arbitration) (memory, device, file, security, process etc)**
  - "Arbitration" is the fancier word for resource management, useful in interviews.
- **Hides the underlying complexity of the hardware. (Aka, Abstraction)**
  - E.g. in C/C++ you call `malloc` (or `new` in C++) and ask for 10 bytes. You get the memory without knowing how the OS goes into memory or from which sector it finds free memory. You only care about your app's logic.
  - The OS keeps all hardware interaction code in its own code base and hides it from you; this is called **abstraction**.
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
