# Lecture 6: What happens when you turn on your computer?

Everything between pressing the power switch and seeing the OS GUI (Windows, macOS, Linux) is called the **boot process**.

- **Speed:** Modern PCs boot in seconds, but the same steps happen every time.
- **Steps:** There are 5 steps, i to v.

## i. PC On

- **Power supply:** Switching on sends electricity to the power supply. The wall wire plugs into it and many wires come out of it.
- **Wires:** They carry power to the motherboard, CPU, hard disk and other storage, GPU and so on.

## ii. CPU initializes itself and looks for the firmware program (BIOS)

The firmware program is stored in the BIOS chip. It is a ROM chip on the motherboard that allows access to and setup of the computer system at the most basic level.

1. In modern PCs, the CPU loads UEFI (Unified Extensible Firmware Interface).

- **CPU:** It is the most important player in the whole boot process.
- **BIOS chip:** It is a non-volatile chip (ROM), so the program in it survives power-off. That program is also called BIOS.
- **BIOS:** Basic Input Output System, the traditional firmware, still used in some systems.
- **UEFI:** It is the upgraded version of BIOS and is used nowadays. Whatever BIOS does in the steps below, UEFI does too.
- **Order:** The CPU initializes itself first. Then it loads the small program from the BIOS chip.

## iii. CPU runs the BIOS (POST)

The CPU runs the BIOS. The BIOS tests and initializes system hardware and loads configuration settings. If something is not appropriate, such as missing RAM, an error is thrown and the boot process stops. This is called the **POST** (Power on self-test) process.

- **UEFI:** It can do much more than initialize hardware. It is really a tiny operating system. For example, Intel CPUs have the Intel Management Engine. One of its features powers Intel's Active Management Technology, which allows remote management of business PCs.

- **Settings first:** BIOS first loads its low-level settings from a small memory area. RAM and disk are not loaded yet.
- **CMOS battery:** This area is powered by a CMOS battery (Complementary Metal Oxide Semiconductor), a small cell on the motherboard. It keeps the area powered when the PC is off.
- **CMOS area stores:**
  1. **BIOS settings:** The settings needed to start the BIOS.
  2. **Basic clock:** It keeps running while the PC is off. The system clock syncs with the internet after boot, but the internet may not be available at boot.
- **Example:** Remove the CMOS cell and power on. The PC only beeps and does not start, even with the power supply on. The settings area was reset, so BIOS cannot get its settings.
- **BIOS program:** It loads with these settings and runs POST.
- **POST:** It runs test cases on each hardware component. Example: for RAM, write some memory and delete it to check that RAM works.
- **Outcome:** If all essential hardware is present and working, boot continues. If something essential is missing, such as RAM removed, an error message is shown and boot stops.

## iv. BIOS hands over to the bootloader

BIOS hands off responsibility for booting your PC to your OS's bootloader.

1. BIOS looks at the MBR (master boot record), a special boot sector at the beginning of a disk. It contains code that loads the rest of the operating system, known as a "bootloader". The BIOS executes the bootloader. The bootloader takes over and begins booting the actual operating system, such as Windows or Linux. In other words, the BIOS or UEFI examines a storage device to look for a small program, either in the MBR or on an EFI system partition, and runs it.

- **Bootloader:** A program which, when executed, turns on the actual OS.
- **Boot device:** The device where the bootloader (the OS boot instructions) is stored. It can be one of these:
  1. Disk (HDD or SSD).
  2. CD drive.
  3. USB drive. Example: when a system has no OS, you boot from a Windows bootable USB or CD.
- **Loading:** BIOS finds the boot device. The bootloader is loaded into memory (RAM) and given all further work.
- **Where the bootloader lives:** It is in one of 2 places.

| Location | Details | Used by |
|----------|---------|---------|
| **MBR (Master Boot Record)** | It sits at index 0, the very start, of the disk. | BIOS (old systems) |
| **EFI system partition** | EFI means Extensible Firmware Interface. A separate partition is made on the disk, the way a disk is split into C: drive, E: drive and so on. The bootloader is kept in it instead of index 0. | UEFI |

- **Handover:** Once the bootloader is found and loaded into memory, the BIOS program's responsibility ends.

## v. The bootloader boots the OS

The bootloader is a small program with the large task of booting the rest of the operating system. It boots the kernel first, then user space.

- **Examples:** Windows uses Windows Boot Manager (Bootmgr.exe). Most Linux systems use GRUB. Macs use boot.efi.
- **Who handles what:** BIOS handled steps i to iv. The bootloader handles step v and loads the full OS.
- **Not universal:** Each OS has its own bootloader.
- **After this:** The work is OS-specific. The OS finds and starts the GUI, runs various checks, turns on startup devices and runs startup programs.
