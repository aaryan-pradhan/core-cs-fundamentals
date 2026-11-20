# Lecture 6: What happens when you turn on your computer?

- Everything between pressing the power switch and seeing the OS GUI (Windows, macOS, Linux) is called the **boot process**.
- Modern PCs boot in seconds, but the same steps still happen every time.
- The process is learnt in 5 steps (i to v below).

**i.** PC On

- Switching on sends electricity to the **power supply**: the component the wall wire plugs into, with many wires coming out of it.
- Those wires carry power to every hardware component: motherboard, CPU, hard disk / other storage devices, GPU, etc.

**ii.** CPU initializes itself and looks for a firmware program (BIOS) stored in BIOS Chip (Basic input-output system chip is a ROM chip found on mother board that allows to access & setup computer system at most basic level.)

1. In modern PCs, CPU loads UEFI (Unified extensible firmware interface)

- The CPU is the most important player in the whole boot process.
- The BIOS chip is a non-volatile chip (ROM), so the program stored in it survives power-off. That program is also called BIOS.
- BIOS = Basic Input Output System, the traditional firmware. Still used in some systems.
- UEFI is the upgraded, more advanced version of BIOS and is what is used nowadays. Whatever BIOS does in the steps below, UEFI does too.
- Order: CPU initializes itself first, then goes to the BIOS chip to load the small program that does the rest of the work.

**iii.** CPU runs the BIOS which tests and initializes system hardware. Bios loads configuration settings. If something is not appropriate (like missing RAM) error is thrown and boot process is stopped.
This is called **POST** (Power on self-test) process.
(UEFI can do a lot more than just initialize hardware; it's really a tiny operating system. For example, Intel CPUs have the Intel Management Engine. This provides a variety of features, including powering Intel's Active Management Technology, which allows for remote management of business PCs.)

- BIOS first loads its (low-level) settings from a small memory area. RAM and disk are not loaded yet at this point.
- This area is powered by a **CMOS battery** (Complementary Metal Oxide Semiconductor): a small cell on the motherboard that keeps the area powered even when the PC is switched off.
- The CMOS area stores:
  1. The BIOS settings needed to start the BIOS.
  2. A basic clock that keeps running while the PC is off. The system clock syncs with the internet after boot, but the internet may not be available at boot, so a basic clock is always kept running.
- Example: remove the CMOS cell and power on. The PC only beeps and does not start, even with the power supply on, because the settings area was reset and BIOS cannot get its settings.
- The actual BIOS program then loads with these settings and runs its instructions for POST.
- POST: go to each hardware component and run test cases on it. E.g. for RAM, write some memory and delete it to check that RAM is available and working.
- All essential hardware present and working: boot continues. Something essential missing (e.g. RAM removed): error message shown and boot stops.

**iv.** **BIOS** will handoff responsibility for booting your PC to your OS's bootloader.

1. BIOS looked at the MBR (master boot record), a special boot sector at the beginning of a disk. The MBR contains code that loads the rest of the operating system, known as a "bootloader." The BIOS executes the bootloader, which takes it from there and begins booting the actual operating system—Windows or Linux, for example.
   In other words,
   the BIOS or UEFI examines a storage device on your system to look for a small program, either in the MBR or on an EFI system partition, and runs it.

- By now all hardware is initialized and working. BIOS now needs the actual program that turns on the OS and hands it control.
- That program is the **bootloader**: a program which, when executed, turns on the actual OS.
- **Boot device**: the device where the bootloader (the OS boot instructions) is stored. It can be:
  1. Disk (HDD / SSD).
  2. CD drive.
  3. USB drive. E.g. when a system has no OS, you boot from a Windows bootable USB / CD.
- BIOS finds the boot device, the bootloader is loaded into memory (RAM), and the bootloader is given all further work.
- The bootloader is found in one of 2 places:
  1. **MBR (Master Boot Record)**: sits at index 0 (the very start) of the disk. Used by BIOS (old systems).
  2. **EFI system partition**: EFI = Extensible Firmware Interface. Instead of index 0 of the disk, a separate partition is made on the disk (the way a disk is split into C: drive, E: drive, etc.), and the bootloader is kept in it. Used by UEFI.
- Once the bootloader is found and loaded into memory, the BIOS program's responsibility ends.

**v.** The bootloader is a small program that has the large task of booting the rest of the operating system (Boots Kernel then, User Space). Windows uses a bootloader named Windows Boot Manager (Bootmgr.exe), most Linux systems use GRUB, and Macs use something called boot.efi

- Steps i to iv were handled by BIOS. Step v is handled by the bootloader itself: it loads the full OS.
- The bootloader is not one universal program for all OSs; each OS has its own.
- From here the work is OS-specific: find and start the GUI, run various checks, turn on startup devices and run startup programs.
