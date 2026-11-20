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

- Hierarchy from top to bottom: closest to the CPU (fastest, costliest, smallest) at the top, farthest at the bottom.
- Storage holds files, data and instructions. Besides the familiar RAM and hard disk, a computer uses several other kinds of storage.
- Storages broadly divide into two types:
  - Primary memory: register, cache, main memory.
  - Secondary memory: the different kinds of disks. The fastest secondary storage today is the SSD (solid state drive).

1. **Register**: Smallest unit of storage. It is a part of CPU itself.
   A register may hold an instruction, a storage address, or any data (such as bit sequence or individual characters).
   Registers are a type of computer memory used to quickly accept, store, and transfer data and instructions that are being used immediately by the CPU.
   - Closest to the CPU.
   - An array-like structure that stores bits (0s and 1s). A computer works in binary: each bit is a high or low voltage.
   - The CPU works directly on registers. Instructions are fetched into registers, and operations like addition and deletion happen there.
2. **Cache**: Additional memory system that temporarily stores frequently used instructions and data for quicker processing by the CPU.
   - A program has lots of instructions and works on lots of data. Some instructions repeat (e.g. sorting code called many times), and some data areas or a few particular files are used very heavily.
   - The OS recognises the instructions/data the program uses again and again over its life cycle.
   - Instead of fetching them from main memory every time, it copies that particular bunch (not all instructions; those stay in the main memory) into the cache, i.e. keeps them closer to the CPU.
   - "Cost" here means access time: how many milliseconds it takes to get the data. Among primary memories, accessing main memory costs the most; accessing cache costs less.
   - So the CPU does not have to go "far" for repeated items, and the overall program executes faster.
3. **Main Memory**: RAM.
   - Processes reside here. The CPU talks to main memory and gets its instructions from there.
4. **Secondary Memory**: Storage media, on which computer can store data & programs.
   - E.g. hard disk. Holds files, media (audio, video), projects and programs.
   - A program lies in secondary memory; when it is brought into main memory it becomes a process (a program under execution is a process).

## Comparison

1. **Cost**:
   a. Primary storages are costly.
   b. Registers are most expensive due to expensive semiconductors & labour.
   c. Secondary storages are cheaper than primary.
   - Cost here means money: the manufacturing cost.
   - Registers are made of transistors (billions of them) using silicon and similar rare materials. The CPU talks to them directly, so they must have no access delay; they are built from the best material, which makes them costly.
   - Order (most to least costly): register, then cache (cheaper than register but still costlier than main memory), then main memory, then secondary storage.
   - E.g. a 1 TB hard disk is cheap (a few thousand rupees), but a few thousand rupees buys only a few GB of RAM; 1 TB of RAM is not something you can buy.
2. **Access Speed**:
   a. Primary has higher access speed than secondary memory.
   b. Registers has highest access speed, then comes cache, then main memory.
   - Secondary memory is the slowest of all.
3. **Storage size**:
   a. Secondary has more space.
   - Register is the smallest: one register is 32-bit or 64-bit, so it stores only 32 (or 64) bits of information.
   - Cache: a little more, in KBs.
   - Main memory: in GBs nowadays.
   - Hard disk: in TBs (1 TB, 2 TB).
   - Why are register and cache kept small? Mainly cost. A 1 TB register or cache would cost so much that nobody would buy that computer.
4. **Volatility**:
   a. Primary memory is volatile.
   b. Secondary is non-volatile.
   - Volatile: when the computer shuts down, all data in registers, cache and main memory is lost (flushed off). The processes that were running are gone.
   - Non-volatile: data in secondary storage is not flushed; it stays saved.
