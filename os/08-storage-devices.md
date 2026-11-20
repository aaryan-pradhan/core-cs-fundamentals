# Lecture 8: Storage Devices Basics

What are the different memory present in the computer system?

```
                         ◄──┐
   ┌─────────────────┐      │
   │     Register    │      │
   └─────────────────┘      │
   ┌─────────────────┐      │
   │      Cache      │      ├─ Primary Memory
   └─────────────────┘      │
   ┌─────────────────┐      │
   │   Main Memory   │      │
   └─────────────────┘      │
                         ◄──┘
                         ◄──┐
   ┌─────────────────┐      │
   │ Electronic Disk │      │
   └─────────────────┘      │
   ┌─────────────────┐      │
   │  Magnetic Disk  │      │
   └─────────────────┘      ├─ Secondary Memory
   ┌─────────────────┐      │
   │   Optical Disk  │      │
   └─────────────────┘      │
   ┌─────────────────┐      │
   │  Magnetic Tapes │      │
   └─────────────────┘      │
                         ◄──┘
```

- **Hierarchy:** It runs from top to bottom. The top is closest to the CPU (fastest, costliest, smallest). The bottom is farthest.
- **Storage:** Storage holds files, data and instructions. A computer uses several kinds of storage, not just the familiar RAM and hard disk.
- **Two types:** Storage divides broadly into primary and secondary memory.

| Type | Members |
|------|---------|
| Primary memory | Register, cache, main memory |
| Secondary memory | The different kinds of disks. The fastest secondary storage today is the SSD (solid state drive). |

1. **Register:** It is the smallest unit of storage. It is part of the CPU itself.
   - **Holds:** A register may hold an instruction, a storage address, or any data (such as a bit sequence or individual characters).
   - **Purpose:** Registers quickly accept, store and transfer the data and instructions that the CPU is using right now.
   - **Closest:** It is the memory closest to the CPU.
   - **Structure:** It is an array-like structure that stores bits (0s and 1s). A computer works in binary. Each bit is a high or low voltage.
   - **Use:** The CPU works directly on registers. Instructions are fetched into registers. Operations like addition and deletion happen there.
2. **Cache:** It is an additional memory system. It temporarily stores frequently used instructions and data for quicker processing by the CPU.
   - **Why:** A program has many instructions and works on much data. Some instructions repeat, such as sorting code called many times. Some data areas or a few particular files are used very heavily.
   - **Recognition:** The OS recognises the instructions and data that the program uses again and again over its life cycle.
   - **Copying:** The OS does not fetch them from main memory every time. It copies that particular bunch into the cache, which is closer to the CPU. It does not copy all instructions. Those stay in main memory.
   - **Cost here:** "Cost" means access time, which is how many milliseconds it takes to get the data. Among primary memories, accessing main memory costs the most. Accessing cache costs less.
   - **Result:** The CPU does not have to go "far" for repeated items. So the overall program executes faster.
3. **Main memory:** It is RAM.
   - **Processes:** Processes reside here. The CPU talks to main memory and gets its instructions from there.
4. **Secondary memory:** It is the storage media on which a computer can store data and programs.
   - **Example:** A hard disk holds files, media (audio, video), projects and programs.
   - **Program vs process:** A program lies in secondary memory. When it is brought into main memory, it becomes a process. A program under execution is a process.

## Comparison

1. **Cost**
   - Primary storages are costly.
   - Registers are the most expensive, due to expensive semiconductors and labour.
   - Secondary storages are cheaper than primary.
   - **Meaning:** Cost here means money, which is the manufacturing cost.
   - **Why registers cost most:** Registers are made of billions of transistors, using silicon and similar rare materials. The CPU talks to them directly, so they must have no access delay. They are built from the best material, which makes them costly.
   - **Order (most to least costly):** Register, then cache, then main memory, then secondary storage. Cache is cheaper than a register but still costlier than main memory.
   - **Example:** A 1 TB hard disk is cheap (a few thousand rupees). A few thousand rupees buys only a few GB of RAM. You cannot buy 1 TB of RAM.
2. **Access speed**
   - Primary has higher access speed than secondary memory.
   - Registers have the highest access speed, then cache, then main memory.
   - Secondary memory is the slowest of all.
3. **Storage size**
   - Secondary has more space.

   | Storage | Size |
   |---------|------|
   | Register | Smallest. One register is 32-bit or 64-bit, so it stores only 32 (or 64) bits. |
   | Cache | A little more, in KBs |
   | Main memory | GBs nowadays |
   | Hard disk | TBs (1 TB, 2 TB) |

   - **Why register and cache are small:** Mainly cost. A 1 TB register or cache would cost so much that nobody would buy that computer.
4. **Volatility**
   - Primary memory is volatile.
   - Secondary memory is non-volatile.
   - **Volatile:** When the computer shuts down, all data in registers, cache and main memory is lost (flushed off). The processes that were running are gone.
   - **Non-volatile:** Data in secondary storage is not flushed. It stays saved.
